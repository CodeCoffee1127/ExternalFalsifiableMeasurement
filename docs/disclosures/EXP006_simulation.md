# EXP006 (C27): simulation-based cross-model generalization

## Paper narrative

Main text Table `tab:cross-model` reports \(R^2\), Ljung-Box \(p\), RMSE across **Current-Local / GPT-4 / Claude-3**.

## Source-backed behavior (`scripts/exp006_cross_model.py`)

1. Optionally reads baseline \(R^2\) and Ljung-Box \(p\) from `results/exp003_final/`.
2. For each named model, calls **`simulate_model_results`**: adds **Gaussian noise** around the baseline — **no** calls to OpenAI, Anthropic, or other external chat APIs.

## Classification

- **paper-backed missing** for a **literal** multi-vendor online replication.
- **source-backed** for the **simulation stub** that produces `results/exp006_cross_model/cross_model_results.json`.

## Recovery action

The script is copied without logic changes so behavior is auditable. This file states the limitation explicitly for reviewers.
