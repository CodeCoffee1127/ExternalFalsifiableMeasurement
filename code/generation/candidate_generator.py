# -*- coding: utf-8 -*-
"""
候選多樣性增強模組（EXP002 準備）

實現：
1. 溫度分層採樣（0.1 / 0.7 / 1.5）
2. 錯誤注入機制（語法/模式/語義）
3. 多樣性檢查

確保 $A_t$ 分布在 [0.2, 0.8]，避免 EXP001 中 $A_t$ 恒為 1.0 或 0.0
"""

import re
import random
from typing import List, Dict, Optional, Tuple, Any
import numpy as np

try:
    from joblib import Parallel, delayed
    HAS_JOBLIB = True
except ImportError:
    HAS_JOBLIB = False


# ========== 錯誤注入函數 ==========

def inject_syntax_error(sql: str) -> str:
    """語法錯誤注入：隨機刪除關鍵字（如 SELECT→SELEC）"""
    syntax_typos = [
        ("SELECT", "SELEC"),
        ("SELECT", "SELET"),
        ("FROM", "FORM"),
        ("WHERE", "WHRE"),
        ("GROUP BY", "GROUPBY"),
        ("ORDER BY", "ORDERBY"),
        ("COUNT", "COUT"),
        ("COUNT", "CNT"),
    ]
    for correct, wrong in syntax_typos:
        if correct.upper() in sql.upper():
            return sql.replace(correct, wrong).replace(correct.upper(), wrong)
    return sql.replace("SELECT", "SELEC") if "SELECT" in sql.upper() else sql


def inject_schema_error(sql: str, schema: dict) -> str:
    """模式錯誤注入：替換表名為不存在的表"""
    tables = schema.get("table_names_original", schema.get("table_names", []))
    if not tables:
        return sql
    fake_tables = ["nonexistent_table", "fake_table", "invalid_table", "wrong_table"]
    for t in tables:
        t_str = str(t).replace(" ", "_")
        if t_str.upper() in sql.upper():
            fake = random.choice(fake_tables)
            return re.sub(rf"\b{re.escape(t_str)}\b", fake, sql, flags=re.IGNORECASE)
    return sql


def inject_semantic_error(sql: str) -> str:
    """語義錯誤注入：添加 HAVING 但無 GROUP BY"""
    sql_upper = sql.upper()
    if "HAVING" in sql_upper:
        return sql
    if "GROUP BY" in sql_upper:
        return sql
    return sql.rstrip().rstrip(";") + " HAVING 1=0"


# ========== 多樣性檢查 ==========

def validate_diversity(
    candidates: List[str],
    verifier: Any,
    min_std: float = 0.2,
    pass_rate_min: float = 0.2,
    pass_rate_max: float = 0.8,
    min_unique: int = 5,
) -> Tuple[bool, Dict]:
    """
    確保候選集滿足多樣性：
    1. 驗證結果標準差 > min_std（不能全相同）
    2. 通過率 ∈ [pass_rate_min, pass_rate_max]
    3. 至少 min_unique 個不同 SQL 文本

    返回：(是否通過, 詳細指標)
    """
    if not candidates:
        return False, {"pass_rate": 0, "std": 0, "unique_count": 0}

    results = [verifier.verify_single(c).pass_verification for c in candidates]
    pass_rate = sum(results) / len(results)
    std = np.std(results) if len(results) > 1 else 0
    unique_count = len(set(c.strip().upper() for c in candidates))

    ok = (
        pass_rate_min <= pass_rate <= pass_rate_max
        and std >= min_std
        and unique_count >= min_unique
    )

    return ok, {
        "pass_rate": pass_rate,
        "std": std,
        "unique_count": unique_count,
        "n_pass": sum(results),
        "n_total": len(results),
    }


# ========== 候選生成器 ==========

class DiverseCandidateGenerator:
    """
    多樣性候選生成器
    溫度分層 + 錯誤注入，確保 $A_t$ 有變異
    """

    def __init__(
        self,
        llm_api: Optional[Any] = None,
        inject_ratio: float = 0.2,
        n_jobs: int = 8,
    ):
        self.llm_api = llm_api
        self.inject_ratio = inject_ratio
        self.n_jobs = n_jobs

    def _generate_with_temp(
        self,
        question: str,
        schema: dict,
        temperature: float,
        n: int,
    ) -> List[str]:
        """使用指定 temperature 生成 n 個候選"""
        if not self.llm_api:
            return []
        if HAS_JOBLIB and n > 1:
            return Parallel(n_jobs=min(self.n_jobs, n))(
                delayed(self.llm_api.generate_sql_single)(
                    question, schema, temperature
                )
                for _ in range(n)
            )
        return [
            self.llm_api.generate_sql_single(question, schema, temperature)
            for _ in range(n)
        ]

    def generate_diverse_candidates(
        self,
        question: str,
        schema: dict,
        n: int = 30,
        use_error_injection: bool = True,
    ) -> List[str]:
        """
        生成多樣性候選
        
        溫度分層：10 低(0.1) + 10 中(0.7) + 10 高(1.5)
        錯誤注入：每類約 20%，確保有負樣本
        """
        if not self.llm_api:
            raise ValueError("LLM API 未設置")

        n_low = n // 3
        n_mid = n // 3
        n_high = n - n_low - n_mid

        candidates = []
        candidates += self._generate_with_temp(question, schema, 0.1, n_low)
        candidates += self._generate_with_temp(question, schema, 0.7, n_mid)
        candidates += self._generate_with_temp(question, schema, 1.5, n_high)

        if use_error_injection and len(candidates) >= 6:
            n_inject_per_type = max(1, int(len(candidates) * self.inject_ratio))
            indices = list(range(len(candidates)))
            random.shuffle(indices)

            # 語法錯誤注入（約 20%）
            for i in indices[:n_inject_per_type]:
                candidates[i] = inject_syntax_error(candidates[i])

            # 模式錯誤注入（約 20%）
            for i in indices[n_inject_per_type : 2 * n_inject_per_type]:
                if i < len(candidates):
                    candidates[i] = inject_schema_error(candidates[i], schema)

            # 語義錯誤注入（約 20%）
            for i in indices[2 * n_inject_per_type : 3 * n_inject_per_type]:
                if i < len(candidates):
                    candidates[i] = inject_semantic_error(candidates[i])

        return candidates[:n]

    def generate_diverse_candidates_mock(
        self,
        gold_sql_list: List[str],
        schema: dict,
        n: int = 30,
        target_pass_rate: float = 0.5,
    ) -> List[str]:
        """
        模擬模式：不調用 API，用金標準 SQL + 錯誤注入生成
        用於測試多樣性邏輯（無需 API key）
        """
        if not gold_sql_list:
            return ["SELECT 1"] * n

        candidates = []
        n_correct = int(n * target_pass_rate)
        n_wrong = n - n_correct

        for _ in range(n_correct):
            sql = random.choice(gold_sql_list)
            candidates.append(sql)

        for _ in range(n_wrong):
            sql = random.choice(gold_sql_list)
            err_type = random.choice(["syntax", "schema", "semantic"])
            if err_type == "syntax":
                candidates.append(inject_syntax_error(sql))
            elif err_type == "schema":
                candidates.append(inject_schema_error(sql, schema))
            else:
                candidates.append(inject_semantic_error(sql))

        random.shuffle(candidates)
        return candidates[:n]
