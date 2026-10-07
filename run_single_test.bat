@echo off
cd /d "C:\Users\ACER\Downloads\PoloFeedback-main\PoloFeedback-main"
"C:\Users\ACER\Downloads\PoloFeedback-main\PoloFeedback-main\venv\Scripts\python.exe" manage.py test feedback.tests.FeedbackViewsTests.test_dashboard_atualizar_status -v 2 > single-test-output.txt 2>&1
if errorlevel 1 (
    echo ERRO_TESTE
) else (
    echo OK_TESTE
)
type single-test-output.txt
