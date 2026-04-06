@echo off
REM paper-based reconstruction: runtime helper only (no experiment logic)
REM Usage: run_with_utf8.bat python scripts\exp006_cross_model.py
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
echo PYTHONIOENCODING=%PYTHONIOENCODING%
echo Running: %*
echo.
%*
