@echo off
cd /d "C:\Users\ACER\Downloads\PoloFeedback-main\PoloFeedback-main"
"C:\Users\ACER\Downloads\PoloFeedback-main\PoloFeedback-main\venv\Scripts\python.exe" debug_dashboard.py > debug-output.txt 2>&1
if errorlevel 1 (
    echo ERRO_DEBUG
) else (
    echo OK_DEBUG
)
type debug-output.txt
