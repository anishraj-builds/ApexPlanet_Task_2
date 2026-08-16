@echo off

echo ========================================
echo TASK-2 DATA ANALYTICS PROJECT
echo ========================================

cd /d "%~dp0code"

echo.
echo [1/7] Data Quality Check
python check.py
if errorlevel 1 goto ERROR

echo.
echo [2/7] Statistical Analysis
python stats.py
if errorlevel 1 goto ERROR

echo.
echo [3/7] Chart Generation
python charts.py
if errorlevel 1 goto ERROR

echo.
echo [4/7] Multivariate Analysis
python multi.py
if errorlevel 1 goto ERROR

echo.
echo [5/7] SQLite Database Creation
python sql.py
if errorlevel 1 goto ERROR

echo.
echo [6/7] SQL Result Generation
python run_sql.py
if errorlevel 1 goto ERROR

echo.
echo [7/7] Final Validation
python validate_outputs.py
if errorlevel 1 goto ERROR

echo.
echo ========================================
echo PROJECT COMPLETED SUCCESSFULLY
echo ========================================

pause
exit /b 0

:ERROR
echo.
echo ========================================
echo PROJECT EXECUTION FAILED
echo ========================================
echo Check the error shown above.
pause
exit /b 1