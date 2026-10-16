@echo off
cd /d "%~dp0"
if exist ".\venv\Scripts\python.exe" (
    set "PYTHON_EXE=.\venv\Scripts\python.exe"
) else (
    set "PYTHON_EXE=python"
)
%PYTHON_EXE% manage.py test feedback.tests.FeedbackViewsTests.test_dashboard_atualizar_status -v 2 > single-test-output.txt 2>&1
if errorlevel 1 (
    echo ERRO_TESTE
) else (
    echo OK_TESTE
)
type single-test-output.txt
