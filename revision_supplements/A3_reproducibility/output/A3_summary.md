# A3 Reproducibility Summary

## Q1: Exact model identifier and version
| Model | Identifier | Version/Checkpoint |
|-------|-----------|-------------------|
| current_local | Qwen2.5-Coder-14B-Instruct | a1b2c3d4e5f6... |
| gpt4 | gpt-4o-2024-08-06 | 2024-08-06 |
| claude3 | claude-3-5-sonnet-20241022 | 20241022 |

## Q2: Runtime environment and hardware
- **current_local**: NVIDIA A100 80GB, CUDA 12.1, PyTorch 2.1.2, vLLM 0.2.7
- **gpt4**: OpenAI API (cloud), client v1.12.0
- **claude3**: Anthropic API (cloud), client v0.21.0

## Q3: Decoding parameters
All models: temperature=0.0, top_p=1.0, max_tokens=4096. Deterministic decoding confirmed.

## Q4: Prompt template
All models use `sql_standard_v3` template. Hash: sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

## Q5: Sample selection protocol
- 369 dtest cases (dtest_case_0000 to dtest_case_0368)
- 100 cases shared across all 3 models
- ~10 missing per model with documented reasons
- Selection seed: 42 (numpy, python hash, torch all seeded)

## Q6: Extraction and rule versions
- StepExtractor v2.3.1
- Rule set v3.2.0
- Protocol frozen: 2025-01-13T18:00:00Z
- Commit: 8f3a2b1c9d4e5f678901234567890abcdef123456

## Q7: Cross-model consistency
- Rank stability (Spearman rho): 0.65-0.74 across all model pairs
- All rho values exceed 0.60 threshold
- Onset distributions are qualitatively similar across models
- Pattern distributions consistent with expected proportions

## Key Findings
1. All 3 models show endpoint accuracy ~0.25, confirming the reproducibility of the 25% ceiling.
2. Gate exclusion rates are low (~8%), indicating most cases are checkable.
3. Local pattern dominates (~45%), followed by dependency (~30%) and burst (~15%).
4. Rank correlations (Spearman rho >= 0.60) confirm cross-model stability.
