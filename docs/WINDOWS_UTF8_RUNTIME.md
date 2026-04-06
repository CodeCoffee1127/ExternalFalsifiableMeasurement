# Windows UTF-8 runtime (required for several scripts)

## Problem

On Chinese Windows, the default console code page is often **GBK (cp936)**. Several experiment scripts print Unicode characters such as:

- `R²` (U+00B2 superscript)
- `✓` / `✗` (checkmarks)

This triggers **`UnicodeEncodeError: 'gbk' codec can't encode character ...`** during `print()`, **before** any scientific logic completes.

## Recommended fix

### Option A — environment variable (minimal)

In **cmd** before running Python:

```bat
set PYTHONIOENCODING=utf-8
python scripts\exp006_cross_model.py
```

In **PowerShell**:

```powershell
$env:PYTHONIOENCODING = "utf-8"
python scripts\exp010_vsp_calibration_corrected.py
```

### Option B — helper batch file

Use `scripts\run_with_utf8.bat` (see repo) to wrap commands.

### Option C — UTF-8 terminal

Use Windows Terminal with UTF-8 code page (`chcp 65001`) **and** a font that supports the glyphs.

## Scripts verified affected

| Script | Symptom without UTF-8 |
|--------|------------------------|
| `scripts/exp006_cross_model.py` | Fails on `R²` in table header |
| `scripts/exp010_vsp_calibration_corrected.py` | Fails on `✓`/`✗` in Step 1 prints |

Other scripts may print loguru ANSI codes; those are stderr noise in PowerShell but usually non-fatal.

## Policy for this bundle

All documented “chain” smoke tests in Phase 4.6 assume **`PYTHONIOENCODING=utf-8`** unless stated otherwise.
