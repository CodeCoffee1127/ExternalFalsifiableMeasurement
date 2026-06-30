# API Call Record: Claude-3

## Model Details
- **actual_api_model_name**: claude-3-5-sonnet-20241022
- **provider**: Anthropic
- **api_version**: 2024-10-22

## Call Metadata
- **call_date**: 2025-01-16
- **response_count**: 369

## Decoding Parameters
- **temperature**: 0.0
- **top_p**: 1.0
- **max_tokens**: 4096

## Input/Output References
- **prompt_template_id**: `sql_standard_v3`
- **sample_ids_file**: `A3_reproducibility/input/cross_model_sample_ids.csv`
- **raw_output_archive_path**: `A3_reproducibility/input/raw_outputs_claude3.tar.gz`

## Notes
- All 369 dtest cases processed sequentially
- Rate limiting: 40 RPM with token-based throttling
- Total API cost: ~$12.15 for input + output tokens
- One transient 529 error on case dtest_case_0184; auto-retried successfully
