@echo off
chcp 65001 > nul
title EPL Analytics Hub - Khoi Chay Ung Dung

echo ============================================================
echo         EPL ANALYTICS HUB - STREAMLIT DASHBOARD
echo ============================================================
echo.

:: Di chuyển đến thư mục chứa file script
cd /d "%~dp0"

:: 1. Kiểm tra Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [LOI] Khong tim thay Python tren he thong cua ban!
    echo Vui long cai dat Python 3.9 tro len tu: https://www.python.org/downloads/
    echo Nho tich chon "Add Python to PATH" khi cai dat.
    echo.
    pause
    exit /b 1
)

:: 2. Kiểm tra hoặc tạo môi trường ảo .venv
if not exist ".venv\Scripts\activate.bat" (
    echo [1/3] Phat hien chua co moi truong ao (.venv).
    echo [2/3] Dang khoi tao .venv va cai dat thu vien phu thuoc...
    echo (Qua trinh nay chi dien ra 1 lan duy nhat luc ban dau, vui long doi giay lat...)
    echo.
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo [LOI] Khong the tao moi truong ao .venv.
        pause
        exit /b 1
    )
    .venv\Scripts\python.exe -m pip install --upgrade pip
    .venv\Scripts\python.exe -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [LOI] Gap su co khi cai dat thu vien tu requirements.txt.
        pause
        exit /b 1
    )
    echo [HOAN TAT] Cai dat thu vien thanh cong!
    echo.
)

:: 3. Chạy Streamlit Dashboard
echo [3/3] Dang khoi chay Streamlit Dashboard tai http://localhost:8501 ...
echo Nhan Ctrl+C tren cua so nay de dung Dashboard.
echo.

if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe -m streamlit run dashboard\app.py
) else (
    python -m streamlit run dashboard\app.py
)

if %errorlevel% neq 0 (
    echo.
    echo [THONG BAO] Ung dung da dong hoac gap loi khi chay.
    pause
)
