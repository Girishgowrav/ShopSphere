@echo off
setlocal
cd /d "%~dp0"
where python >nul 2>nul || (echo Python 3 is not available on PATH. & exit /b 1)
if not exist .venv\Scripts\python.exe python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m pytest tests\test_*.py -v --html=reports\report.html --self-contained-html
exit /b %errorlevel%
