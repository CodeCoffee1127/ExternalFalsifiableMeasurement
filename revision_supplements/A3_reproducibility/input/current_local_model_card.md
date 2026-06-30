# Model Card: current_local

## Base Model
- **base_model_name**: Qwen2.5-Coder-14B-Instruct
- **checkpoint_path_or_hash**: `/checkpoints/qwen2.5-coder-14b-instruct-v1.0` (sha256: `a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456`)
- **fine_tuning_status**: none (base model, no fine-tuning applied)

## Runtime Environment
- **runtime_environment**: Python 3.10.12, PyTorch 2.1.2, CUDA 12.1
- **hardware**: NVIDIA A100 80GB
- **dependency_versions**: See `requirements_freeze.txt` for complete list
- **requirements_freeze_path**: `A3_reproducibility/input/requirements_freeze.txt`
- **conda_env_export_path**: `A3_reproducibility/input/conda_env_export.yaml`

## Decoding Parameters
- **temperature**: 0.0
- **top_p**: 1.0
- **top_k**: not specified (default)
- **max_tokens**: 4096
- **num_return_sequences**: 1
- **prompt_template_id**: `sql_standard_v3`

## Generation Metadata
- **date_generated**: 2025-01-14T09:23:17Z
- **raw_output_archive_path**: `A3_reproducibility/input/raw_outputs_current_local.tar.gz`

## Notes
- Model executed locally via vLLM 0.2.7 serving framework
- Deterministic decoding (temperature=0.0) ensures reproducibility given identical inputs
- GPU memory utilization capped at 0.90 to accommodate batch processing
