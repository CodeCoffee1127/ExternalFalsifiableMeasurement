"""
父消融貢獻度計算（論文 §7 嚴格定義）

ΔH(q_i→p_t) = H_ν(p_t; Pa(p_t)\{q_i}) - H_ν(p_t; Pa(p_t))
- H_full = H_ν(p_t; Pa) 完整父集下的驗證熵
- H_minus = H_ν(p_t; Pa\{q_i}) 移除父節點 q_i 後的驗證熵
- delta_H = H_minus - H_full
- ΔH > 0：移除後熵增 → 父節點降低原熵（正貢獻）→ I_+
- ΔH < 0：移除後熵減 → 父節點增加原熵（負貢獻）→ I_-
"""

import re
import random
from typing import Dict, List, Tuple, Any, Optional, Union
import numpy as np

from loguru import logger

from generation.candidate_generator import inject_schema_error

# 診斷統計（跨調用累積，供驗證腳本讀取）
ABLATION_DIAGNOSTICS: Dict[str, Any] = {
    "n_calls": 0,
    "n_parents_total": 0,
    "n_delta_significant": 0,  # |delta_H| > 0.01
    "n_zero_delta": 0,
    "delta_H_values": [],
    "zero_delta_details": [],
}


# 無效標識符，確保 Verifier 返回 violated
_INVALID_COL = "NON_EXISTENT_COLUMN_XYZ"
_INVALID_OP = "INVALID_OPERATOR"


def _corrupt_clause_in_sql(sql: str, clause: str, schema: Optional[dict] = None) -> str:
    """
    針對指定子句進行消融式破壞，必須確保 Verifier 返回 violated（0）
    """
    clause_upper = clause.upper().replace("_", " ")

    if clause_upper == "FROM":
        return _corrupt_from_clause(sql, schema)
    if "SELECT" in clause_upper:
        return _corrupt_select_clause(sql)
    if clause_upper == "WHERE":
        return _corrupt_where_clause(sql)
    if "GROUP" in clause_upper and "BY" in clause_upper:
        return _corrupt_group_by_clause(sql)
    if clause_upper == "HAVING":
        return _corrupt_having_clause(sql)
    if "ORDER" in clause_upper and "BY" in clause_upper:
        return _corrupt_order_by_clause(sql)

    return _corrupt_aggressive(sql)


def _corrupt_aggressive(sql: str) -> str:
    """強破壞：替換列引用為無效標識符，確保語法/模式違規"""
    return re.sub(r"\b[A-Za-z_][A-Za-z0-9_]*\.[A-Za-z_][A-Za-z0-9_]*\b", _INVALID_COL, sql, count=1)


def _corrupt_from_clause(sql: str, schema: Optional[dict]) -> str:
    """破壞 FROM：替換表名為不存在的表"""
    result = inject_schema_error(sql, schema or {})
    if result == sql:
        return _corrupt_aggressive(sql)
    return result


def _corrupt_select_clause(sql: str) -> str:
    """破壞 SELECT：引入語法錯誤或無效列引用"""
    m = re.search(r"\bSELECT\s+(.+?)\s+FROM", sql, re.IGNORECASE | re.DOTALL)
    if m:
        return re.sub(r"\bSELECT\b", "SELEC", sql, count=1, flags=re.IGNORECASE)
    return _corrupt_aggressive(sql)


def _corrupt_where_clause(sql: str) -> str:
    """破壞 WHERE：替換 table.col 為無效列，或 = 為無效運算符"""
    if "WHERE" not in sql.upper():
        return sql
    s = re.sub(r"\b[A-Za-z_][A-Za-z0-9_]*\.[A-Za-z_][A-Za-z0-9_]*\b", _INVALID_COL, sql, count=1)
    if s == sql:
        s = re.sub(r"\s+=\s+", " INVALID_OPERATOR ", sql, count=1)
    return s


def _corrupt_group_by_clause(sql: str) -> str:
    """破壞 GROUP BY：引入語法錯誤"""
    if "GROUP BY" not in sql.upper():
        return sql
    return re.sub(r"\bGROUP\s+BY\b", "GROUPBY", sql, flags=re.IGNORECASE)


def _corrupt_having_clause(sql: str) -> str:
    """破壞 HAVING：引入語法錯誤或無效條件"""
    if "HAVING" not in sql.upper():
        return sql
    s = re.sub(r"\bHAVING\s+", "HAVNG ", sql, count=1, flags=re.IGNORECASE)
    if s == sql:
        s = re.sub(r"\s+=\s+", " INVALID_OPERATOR ", sql, count=1)
    return s


def _corrupt_order_by_clause(sql: str) -> str:
    """破壞 ORDER BY：引入語法錯誤"""
    if "ORDER BY" not in sql.upper():
        return sql
    return re.sub(r"\bORDER\s+BY\b", "ORDERBY", sql, flags=re.IGNORECASE)


def compute_Hv_from_verifications(
    verification_results: List[Union[bool, object]],
    prior_alpha: float = 1.0,
    prior_beta: float = 1.0,
    epsilon: float = 1e-10,
) -> float:
    """
    從驗證結果計算 H_ν（使用 Beta 後驗均值，論文 §7）
    H_ν = -A_t·log2(A_t) - (1-A_t)·log2(1-A_t)
    """
    successes = sum(
        1 for r in verification_results
        if (r.pass_verification if hasattr(r, "pass_verification") else r)
    )
    n = len(verification_results)
    if n == 0:
        return 0.5

    a = prior_alpha + successes
    b = prior_beta + (n - successes)
    A_t = a / (a + b)
    A_t = np.clip(A_t, epsilon, 1 - epsilon)
    return -(A_t * np.log2(A_t) + (1 - A_t) * np.log2(1 - A_t))


def compute_parent_ablation_strength(
    verifier: Any,
    candidates: List[str],
    dependencies: Dict[str, List[str]],
    current_clause: str,
    schema: Optional[dict] = None,
    n_jobs: int = 1,
    prior_alpha: float = 1.0,
    prior_beta: float = 1.0,
) -> Tuple[float, float]:
    """
    論文 §7：父消融貢獻度 I_+, I_-

    對每個父節點 q_i ∈ Pa(current_clause)：
    - H_full = H_ν(完整候選驗證)
    - H_ablated = H_ν(消融候選驗證，即破壞父子句後的候選)
    - delta_H = H_ablated - H_full
    - I_+ += max(delta_H, 0), I_- += max(-delta_H, 0)

    返回：(I_plus, I_minus)
    """
    parents = dependencies.get(current_clause, [])
    if not parents or not candidates:
        if parents is not None and len(parents) == 0:
            logger.debug(f"parent_ablation skip: current_clause={current_clause}, deps={list(dependencies.keys())}")
        return 0.0, 0.0

    batch_verify = getattr(verifier, "batch_verify", None)
    if not batch_verify:
        return 0.0, 0.0

    verifications_full = batch_verify(candidates, n_jobs=n_jobs)
    H_full = compute_Hv_from_verifications(
        verifications_full, prior_alpha, prior_beta
    )

    I_plus = 0.0
    I_minus = 0.0

    for parent in parents:
        ablated = [
            _corrupt_clause_in_sql(c, parent, schema)
            for c in candidates
        ]
        verifications_ablated = batch_verify(ablated, n_jobs=n_jobs)
        H_ablated = compute_Hv_from_verifications(
            verifications_ablated, prior_alpha, prior_beta
        )

        delta_H = H_ablated - H_full
        I_plus += max(delta_H, 0.0)
        I_minus += max(-delta_H, 0.0)

        # 診斷：記錄 delta_H 與零差異
        ABLATION_DIAGNOSTICS["n_parents_total"] += 1
        ABLATION_DIAGNOSTICS["delta_H_values"].append(delta_H)
        if abs(delta_H) > 0.01:
            ABLATION_DIAGNOSTICS["n_delta_significant"] += 1
        else:
            ABLATION_DIAGNOSTICS["n_zero_delta"] += 1
            if len(ABLATION_DIAGNOSTICS["zero_delta_details"]) < 5:
                ABLATION_DIAGNOSTICS["zero_delta_details"].append({
                    "parent": parent,
                    "H_full": H_full,
                    "H_ablated": H_ablated,
                    "current_clause": current_clause,
                })

    ABLATION_DIAGNOSTICS["n_calls"] += 1
    return I_plus, I_minus


def get_ablation_diagnostics() -> Dict[str, Any]:
    """返回父消融診斷統計，供驗證腳本使用"""
    d = ABLATION_DIAGNOSTICS.copy()
    vals = d.get("delta_H_values", [])
    if vals:
        d["pct_delta_significant"] = (
            sum(1 for v in vals if abs(v) > 0.01) / len(vals) * 100
        )
        d["delta_H_mean"] = float(np.mean(vals))
        d["delta_H_std"] = float(np.std(vals))
    return d


def reset_ablation_diagnostics() -> None:
    """重置診斷統計（新實驗前調用）"""
    ABLATION_DIAGNOSTICS.update({
        "n_calls": 0,
        "n_parents_total": 0,
        "n_delta_significant": 0,
        "n_zero_delta": 0,
        "delta_H_values": [],
        "zero_delta_details": [],
    })
