@echo off
cd /d "%~dp0"
"%~dp0venv\Scripts\python.exe" debug_dashboard.py > debug-output.txt 2>&1
if errorlevel 1 (
    echo ERRO_DEBUG
) else (
    echo OK_DEBUG
)
type debug-output.txt
