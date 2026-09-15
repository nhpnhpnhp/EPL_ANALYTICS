@echo off
setlocal EnableDelayedExpansion
title EPL Analytics Hub

cd /d "%~dp0"

echo ============================================================
echo         EPL ANALYTICS HUB - STREAMLIT DASHBOARD
echo ============================================================
echo.

REM 1. Neu da co .venv san trong project, chay ngay lap tuc
if exist "%~dp0.venv\Scripts\python.exe" (
    echo [1/2] Phat hien moi truong ao .venv san co trong du an.
    echo [2/2] Dang khoi chay Streamlit Dashboard tai http://localhost:8501 ...
    echo Nhan Ctrl+C de dung ung dung.
    echo.
    "%~dp0.venv\Scripts\python.exe" -m streamlit run "%~dp0dashboard\app.py"
    goto :done
)

REM 2. Neu chua co .venv, tim Python tren he thong
set "PY_CMD="

where python >nul 2>nul
if !errorlevel! equ 0 (
    set "PY_CMD=python"
) else (
    where py >nul 2>nul
    if !errorlevel! equ 0 (
        set "PY_CMD=py"
    )
)

if "!PY_CMD!"=="" (
    for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
        if exist "%%D\python.exe" set "PY_CMD=%%D\python.exe"
    )
)

if "!PY_CMD!"=="" (
    for /d %%D in ("%APPDATA%\uv\python\cpython-*") do (
        if exist "%%D\python.exe" set "PY_CMD=%%D\python.exe"
    )
)

if "!PY_CMD!"=="" (
    echo [LOI] Khong tim thay Python tren he thong cua ban!
    echo Vui long cai dat Python 3.9 tro len tu: https://www.python.org/downloads/
    echo (Nho tich chon "Add Python to PATH" khi cai dat)
    echo.
    pause
    exit /b 1
)

REM 3. Khoi tao .venv va cai dat thu vien phu thuoc
echo [1/3] Dang khoi tao moi truong ao .venv bang "!PY_CMD!" ...
"!PY_CMD!" -m venv "%~dp0.venv"
if !errorlevel! neq 0 (
    echo [LOI] Khong the tao moi truong ao .venv.
    pause
    exit /b 1
)

echo [2/3] Dang cai dat thu vien tu requirements.txt...
echo (Qua trinh nay chi dien ra 1 lan duy nhat luc ban dau, vui long doi vai phut...)
"%~dp0.venv\Scripts\python.exe" -m pip install --upgrade pip
"%~dp0.venv\Scripts\python.exe" -m pip install -r "%~dp0requirements.txt"
if !errorlevel! neq 0 (
    echo [LOI] Gap su co khi cai dat requirements.txt.
    pause
    exit /b 1
)

REM 4. Khoi chay Streamlit
echo.
echo [3/3] Dang khoi chay Streamlit Dashboard tai http://localhost:8501 ...
echo Nhan Ctrl+C de dung Dashboard.
echo.
"%~dp0.venv\Scripts\python.exe" -m streamlit run "%~dp0dashboard\app.py"

:done
if %errorlevel% neq 0 (
    echo.
    echo [THONG BAO] Dashboard da dung.
    pause
)

