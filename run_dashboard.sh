#!/usr/bin/env bash
# ============================================================
# EPL ANALYTICS HUB - STREAMLIT LAUNCHER (macOS / Linux)
# ============================================================

set -e

# Chuyển về thư mục chứa script
cd "$(dirname "$0")"

echo "============================================================"
echo "        EPL ANALYTICS HUB - STREAMLIT DASHBOARD"
echo "============================================================"
echo ""

# 1. Kiểm tra python3
if ! command -v python3 &> /dev/null; then
    echo "[LỖI] Không tìm thấy python3 trên hệ thống của bạn!"
    echo "Vui lòng cài đặt Python 3.9 trở lên từ: https://www.python.org/downloads/"
    exit 1
fi

# 2. Kiểm tra hoặc khởi tạo virtualenv .venv
if [ ! -f ".venv/bin/activate" ]; then
    echo "[1/3] Phát hiện chưa có môi trường ảo (.venv)."
    echo "[2/3] Đang khởi tạo .venv và cài đặt các thư viện phụ thuộc..."
    echo "(Quá trình chỉ diễn ra một lần, vui lòng đợi giây lát...)"
    echo ""
    python3 -m venv .venv
    .venv/bin/python3 -m pip install --upgrade pip
    .venv/bin/python3 -m pip install -r requirements.txt
    echo "[HOÀN TẤT] Cài đặt thư viện thành công!"
    echo ""
fi

# 3. Kích hoạt và chạy Streamlit
echo "[3/3] Đang khởi chạy Streamlit Dashboard..."
echo "Nhấn Ctrl+C để dừng Dashboard."
echo ""

source .venv/bin/activate
python3 -m streamlit run dashboard/app.py
