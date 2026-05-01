@echo off
REM Sync Tables Data to GitHub Repository
REM This script adds, commits, and pushes the new table data files

echo ========================================
echo Syncing Table 11-13 Data to GitHub
echo ========================================
echo.

REM Navigate to submission directory
cd /d "%~dp0"

REM Check git status
echo [1/4] Checking git status...
git status
echo.

REM Add new files
echo [2/4] Adding new table data files...
git add tables/
git add results/table11_*.json results/table11_*.csv
git add results/table12_*.json results/table12_*.csv
git add results/table13a_*.json results/table13a_*.csv
git add results/table13b_*.json results/table13b_*.csv
git add experiment_reports/EXP003_Fit_Analysis/
git add experiment_reports/EXP008_LjungBox_Test/
echo.

REM Commit changes
echo [3/4] Committing changes...
git commit -m "Add Table 11-13 data: fit metrics, Ljung-Box tests, bootstrap CI, and split sensitivity analysis"
echo.

REM Push to GitHub
echo [4/4] Pushing to GitHub...
git push origin main
echo.

echo ========================================
echo Sync Complete!
echo ========================================
echo.
echo Files synced:
echo   - tables/*.tex (LaTeX table sources)
echo   - results/table11_* (Dynamics Equation Fit Metrics)
echo   - results/table12_* (Ljung-Box Test Results)
echo   - results/table13a_* (Bootstrap Confidence Intervals)
echo   - results/table13b_* (Split Sensitivity Analysis)
echo   - experiment_reports/EXP003_Fit_Analysis/
echo   - experiment_reports/EXP008_LjungBox_Test/
echo.
echo Repository: https://github.com/CodeCoffee1127/ExternalFalsifiableMeasurement
echo.
pause
