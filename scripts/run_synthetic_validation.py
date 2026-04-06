#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合成預驗證（§10.4）- 父消融貢獻方向性驗證

實驗A：正貢獻驗證（I_+ 抑制熵增）
  - 高支持組：gold SQL 驗證（多數通過）
  - 對照組：corrupted SQL 驗證（多數失敗）
  - 通過標準：高支持組驗證熵顯著低於對照組（Mann-Whitney U, p<0.05）

實驗B：負貢獻級聯（I_- 驅動熵增）
  - 植入誤導後，後續步驟熵增與初始 I_- 顯著正相關
  - 通過標準：Spearman ρ>0.5, p<0.05
"""

import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any
import numpy as np

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from scipy import stats
from loguru import logger

from pipeline.experiment_pipeline import ExperimentPipeline
from generation.candidate_generator import inject_schema_error, inject_syntax_error


def load_calibration_samples(config: dict, n: int = 50) -> List[Dict]:
    """載入校準樣本"""
    from data.mini_dataset import load_calibration_for_exp003
    data_dir = Path(config.get("paths", {}).get("data_dir", "data"))
    samples = load_calibration_for_exp003(str(data_dir), mini=True, n_samples=n, seed=42)
    pipe = ExperimentPipeline(config)
    return pipe._enrich_schema(samples)


def compute_Hv_from_verifications(verifications: List, prior_alpha: float = 1.0, prior_beta: float = 1.0) -> float:
    """從驗證結果計算驗證熵 Hv"""
    successes = sum(1 for r in verifications if (r.pass_verification if hasattr(r, 'pass_verification') else r))
    n = len(verifications)
    if n == 0:
        return 0.5
    a = prior_alpha + successes
    b = prior_beta + (n - successes)
    A_t = a / (a + b)
    A_t = np.clip(A_t, 1e-10, 1 - 1e-10)
    return -(A_t * np.log2(A_t) + (1 - A_t) * np.log2(1 - A_t))


def experiment_positive_reflow(
    pipeline: ExperimentPipeline,
    samples: List[Dict],
    n_trials: int = 50,
) -> Dict[str, Any]:
    """
    實驗A：正貢獻驗證（I_+ 抑制熵增）
    高支持組（80% gold + 20% corrupted）→ p≈0.8 → H 較低
    對照組（50% gold + 50% corrupted）→ p≈0.5 → H 較高（熵最大）
    通過標準：H_high_support 顯著低於 H_control（Mann-Whitney U, p<0.05）
    """
    H_high_support = []
    H_control = []
    for sample in samples[:n_trials]:
        schema = sample.get('schema', {})
        if not schema.get('table_names') and not schema.get('tables'):
            continue
        query = sample.get('query', '')
        if not query:
            continue
        verifier = pipeline._get_verifier(schema)
        neg_sql = inject_schema_error(query, schema)
        if neg_sql == query:
            neg_sql = inject_syntax_error(query)

        # 高支持：8 gold + 2 變體
        cand_high = [query] * 8 + [neg_sql] * 2
        v_high = verifier.batch_verify(cand_high, n_jobs=pipeline.n_jobs)
        H_high_support.append(compute_Hv_from_verifications(v_high))

        # 對照：5 gold + 5 corrupted（混合）
        cand_ctrl = [query] * 5 + [neg_sql] * 5
        v_ctrl = verifier.batch_verify(cand_ctrl, n_jobs=pipeline.n_jobs)
        H_control.append(compute_Hv_from_verifications(v_ctrl))

    H_high_arr = np.array(H_high_support)
    H_ctrl_arr = np.array(H_control)

    # 高支持組 p≈0.8 → H 較低；對照組 p≈0.5 → H 較高
    # 所以 H_high < H_control。Mann-Whitney 檢驗高支持組是否顯著低
    stat, p_val = stats.mannwhitneyu(H_high_arr, H_ctrl_arr, alternative='less')
    passed = p_val < 0.05

    return {
        "experiment": "positive_reflow",
        "n_trials": len(H_high_arr),
        "H_high_support_mean": float(np.mean(H_high_arr)),
        "H_control_mean": float(np.mean(H_ctrl_arr)),
        "mann_whitney_stat": float(stat),
        "mann_whitney_p": float(p_val),
        "passed": passed,
        "criterion": "H_high_support < H_control (p<0.05)",
    }


def experiment_negative_cascade(
    pipeline: ExperimentPipeline,
    samples: List[Dict],
    chain_length: int = 5,
    n_trials: int = 50,
) -> Dict[str, Any]:
    """
    實驗B：負貢獻級聯（I_- 驅動熵增）
    誤導植入後，後續步驟熵增與初始 I_- 顯著正相關
    通過標準：Spearman ρ>0.5, p<0.05
    """
    I_neg_list = []
    H_final_list = []

    for sample in samples[:n_trials]:
        schema = sample.get('schema', {})
        if not schema.get('table_names') and not schema.get('tables'):
            continue
        query = sample.get('query', '')
        if not query:
            continue

        verifier = pipeline._get_verifier(schema)
        deps = pipeline.cpfc.extract_dependencies(query)
        clauses_with_parents = [c for c in deps if deps.get(c) and len(deps.get(c, [])) > 0]
        if not clauses_with_parents:
            continue

        candidates = [query] * 10
        candidates = pipeline._inject_errors_into_candidates(candidates, schema, ratio=0.2)
        current_clause = clauses_with_parents[0]
        for p in ['where', 'having', 'group_by', 'order_by', 'select']:
            if p in clauses_with_parents:
                current_clause = p
                break

        I_plus, I_minus = pipeline.state_calc.compute_parent_ablation_strength(
            verifier, candidates, deps, current_clause,
            schema=schema, n_jobs=pipeline.n_jobs,
        )
        verif = verifier.batch_verify(candidates, n_jobs=pipeline.n_jobs)
        H_full = pipeline.state_calc.compute_Hv(
            pipeline.state_calc.compute_At(verif)
        )

        I_neg_list.append(I_minus)
        H_final_list.append(H_full)

    I_neg_arr = np.array(I_neg_list)
    H_arr = np.array(H_final_list)

    if len(I_neg_arr) < 10:
        return {
            "experiment": "negative_cascade",
            "n_trials": len(I_neg_arr),
            "passed": False,
            "reason": "insufficient_samples",
            "spearman_rho": None,
            "spearman_p": None,
        }

    rho, p_val = stats.spearmanr(I_neg_arr, H_arr)
    passed = rho > 0.5 and p_val < 0.05

    return {
        "experiment": "negative_cascade",
        "n_trials": len(I_neg_arr),
        "spearman_rho": float(rho),
        "spearman_p": float(p_val),
        "passed": passed,
        "criterion": "Spearman ρ>0.5 and p<0.05",
    }


def main():
    parser = argparse.ArgumentParser(description="合成預驗證 §10.4")
    parser.add_argument("--experiment", choices=["positive_reflow", "negative_cascade", "all"], default="all")
    parser.add_argument("--n_trials", type=int, default=50)
    parser.add_argument("--chain_length", type=int, default=5)
    parser.add_argument("--output", default="experiment_reports/EXP003/SYNTHETIC_VALIDATION_REPORT.json")
    parser.add_argument("--config", default="configs/experiment_config.yaml")
    args = parser.parse_args()

    import yaml
    with open(Path(args.config), "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    pipeline = ExperimentPipeline(config)
    samples = load_calibration_samples(config, n=args.n_trials * 2)

    results = {"experiments": [], "all_passed": True}

    if args.experiment in ("positive_reflow", "all"):
        logger.info("執行實驗A：正貢獻驗證（I_+ 抑制熵增）")
        r_a = experiment_positive_reflow(pipeline, samples, n_trials=args.n_trials)
        results["experiments"].append(r_a)
        if not r_a.get("passed", False):
            results["all_passed"] = False
        logger.info(f"  實驗A: passed={r_a.get('passed')}, p={r_a.get('mann_whitney_p', 'N/A')}")

    if args.experiment in ("negative_cascade", "all"):
        logger.info("執行實驗B：負貢獻級聯（I_- 驅動熵增）")
        r_b = experiment_negative_cascade(
            pipeline, samples, chain_length=args.chain_length, n_trials=args.n_trials
        )
        results["experiments"].append(r_b)
        if not r_b.get("passed", False):
            results["all_passed"] = False
        logger.info(f"  實驗B: passed={r_b.get('passed')}, ρ={r_b.get('spearman_rho', 'N/A')}")

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    logger.info(f"報告已保存: {out_path}")
    logger.info(f"all_passed={results['all_passed']}")
    return 0 if results["all_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
