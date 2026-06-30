# System Environment Record

## Hardware
- **GPU**: NVIDIA A100 80GB PCIe
- **GPU Count**: 1
- **CPU**: AMD EPYC 7763 64-Core Processor
- **RAM**: 512 GB DDR4
- **Storage**: NVMe SSD 2TB

## Software
- **OS**: Ubuntu 22.04.3 LTS (kernel 5.15.0)
- **CUDA Version**: 12.1
- **NVIDIA Driver**: 535.104.05
- **Python**: 3.10.12 (conda environment)
- **Container**: Docker 24.0.7 (image: `spider-repro:v1.0`)

## Environment Variables
- `CUDA_VISIBLE_DEVICES=0`
- `PYTHONHASHSEED=42`
- `CUBLAS_WORKSPACE_CONFIG=:4096:8`
- `TRANSFORMERS_CACHE=/data/hf_cache`

## Verification
- GPU available: Yes
- CUDA working: Yes (verified via `torch.cuda.is_available()`)
- Deterministic ops: Enabled
