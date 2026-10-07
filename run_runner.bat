@echo off
cd /d "C:\Users\ACER\Downloads\PoloFeedback-main\PoloFeedback-main"
"C:\Users\ACER\Downloads\PoloFeedback-main\PoloFeedback-main\venv\Scripts\python.exe" test_runner.py > runner-output.txt 2>&1
if errorlevel 1 (
    echo ERRO
) else (
    echo OK
)
type runner-output.txt
