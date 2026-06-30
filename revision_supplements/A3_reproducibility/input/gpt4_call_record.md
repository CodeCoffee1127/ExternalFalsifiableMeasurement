# API Call Record: GPT-4

## Model Details
- **actual_api_model_name**: gpt-4o-2024-08-06
- **provider**: OpenAI
- **api_version**: 2024-08-06

## Call Metadata
- **call_date**: 2025-01-15
- **response_count**: 369

## Decoding Parameters
- **temperature**: 0.0
- **top_p**: 1.0
- **max_tokens**: 4096

## Input/Output References
- **prompt_template_id**: `sql_standard_v3`
- **sample_ids_file**: `A3_reproducibility/input/cross_model_sample_ids.csv`
- **raw_output_archive_path**: `A3_reproducibility/input/raw_outputs_gpt4.tar.gz`

## Notes
- All 369 dtest cases processed in a single batch
- Rate limiting applied: 500 RPM with exponential backoff
- Total API cost: ~$18.42 for completion tokens
- No retry failures; all responses received within 45 minutes
