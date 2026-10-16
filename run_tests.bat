@echo off
cd /d "%~dp0"
if exist ".\venv\Scripts\python.exe" (
    set "PYTHON_EXE=.\venv\Scripts\python.exe"
) else (
    set "PYTHON_EXE=python"
)
%PYTHON_EXE% manage.py test -v 2 > test-output.txt 2>&1
if errorlevel 1 (
    echo ERRO_TESTES
) else (
    echo OK_TESTES
)
type test-output.txt
