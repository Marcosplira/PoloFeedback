@echo off
cd /d "C:\Users\ACER\Downloads\PoloFeedback-main\PoloFeedback-main"
"C:\Users\ACER\Downloads\PoloFeedback-main\PoloFeedback-main\venv\Scripts\python.exe" manage.py test -v 2 > test-output.txt 2>&1
if errorlevel 1 (
    echo ERRO_TESTES
) else (
    echo OK_TESTES
)
type test-output.txt
