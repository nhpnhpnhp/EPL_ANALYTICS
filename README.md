# ⚽ ĐỒ ÁN PHÂN TÍCH DỮ LIỆU BÓNG ĐÁ NGOẠI HẠNG ANH (EPL ANALYTICS)

[![Python](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](#)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#)

> **Đề tài:** Thống kê, phân tích lịch sử giải bóng đá Ngoại hạng Anh (English Premier League – EPL), hiệu suất cầu thủ ($xG/xA$) và xây dựng mô hình AI dự đoán kết quả trận đấu.  
> **Chuyên ngành:** Kỹ thuật Dữ liệu (Data Engineering) / Khoa học Dữ liệu (Data Science).  
> **Thực hiện:** Nhóm 2 sinh viên.

---

## 📑 Mục Lục
1. [Giới Thiệu Đề Tài & Điểm Nổi Bật](#1-giới-thiệu-đề-tài--điểm-nổi-bật)
2. [Cấu Trúc Thư Mục Chuẩn (Project Structure)](#2-cấu-trúc-thư-mục-chuẩn-project-structure)
3. [Quy Mô Dữ Liệu Lịch Sử (Datasets)](#3-quy-mô-dữ-liệu-lịch-sử-datasets)
4. [Hướng Dẫn Cài Đặt & Chạy Trên Mọi Máy (Quick Start)](#4-hướng-dẫn-cài-đặt--chạy-trên-mọi-máy-quick-start)
   - [Yêu cầu tiên quyết](#yêu-cầu-tiên-quyết)
   - [Bước 1: Clone Repository](#bước-1-clone-repository)
   - [Bước 2: Cài đặt Môi Trường Ảo & Thư Viện](#bước-2-cài-đặt-môi-trường-ảo--thư-viện)
   - [Bước 3: Khởi chạy Streamlit Dashboard](#bước-3-khởi-chạy-streamlit-dashboard)
   - [Bước 4: Mở và Chạy Jupyter Notebook](#bước-4-mở-và-chạy-jupyter-notebook)
5. [Tóm Tắt Kết Quả 8 Câu Hỏi Nghiên Cứu (Research Findings)](#5-tóm-tắt-kết-quả-8-câu-hỏi-nghiên-cứu-research-findings)
6. [Mô Hình Học Máy Dự Đoán Trận Đấu (AI Match Predictor)](#6-mô-hình-học-máy-dự-đoán-trận-đấu-ai-match-predictor)
7. [Khắc Phục Sự Cố Thường Gặp (Troubleshooting & FAQ)](#7-khắc-phục-sự-cố-thường-gặp-troubleshooting--faq)

---

## 1. Giới Thiệu Đề Tài & Điểm Nổi Bật

Dự án **EPL Analytics** là một giải pháp phân tích dữ liệu thể thao toàn diện, kết hợp chặt chẽ giữa:
- **Data Engineering**: Thu thập, chuẩn hóa và tổng hợp dữ liệu trận đấu qua 20 mùa giải và dữ liệu cầu thủ chuyên sâu qua 11 mùa giải.
- **Exploratory Data Analysis (EDA)**: Giải quyết 8 câu hỏi nghiên cứu then chốt của bóng đá hiện đại với biểu đồ trực quan cao cấp (Matplotlib, Seaborn, Plotly).
- **Machine Learning**: Xây dựng mô hình phân loại dự đoán kết quả trận đấu (Thắng - Hòa - Thua) dựa trên chuỗi phong độ cuốn chiếu (Rolling 5 matches), kiểm thử ngoài thời gian (Out-of-Time Validation) hoàn toàn không rò rỉ dữ liệu (No Data Leakage).
- **Interactive Web App**: Ứng dụng **Streamlit Interactive Hub** cung cấp giao diện trực quan hóa dữ liệu theo chuẩn phong cách Premier League, cho phép người dùng tùy biến phân tích và dự đoán trận đấu theo thời gian thực.

---

## 2. Cấu Trúc Thư Mục Chuẩn (Project Structure)

```text
EPL_ANALYTICS/
│
├── EPL_Data_Analysis.ipynb         # Notebook phân tích chính (73 cells chạy tuần tự từ A -> Z)
│
├── data/
│   ├── raw/
│   │   ├── matches/                # 20 file CSV kết quả trận đấu (từ mùa 2005-06 đến 2024-25)
│   │   └── players/                # Dữ liệu cầu thủ chi tiết từ Understat (11 mùa giải)
│   │
│   └── processed/
│       ├── matches_clean.csv       # 7,601 trận đấu sau khi làm sạch & feature engineering
│       └── players_clean.csv       # 5,887 bản ghi cầu thủ chuẩn hóa với số liệu xG/xA
│
├── dashboard/                      # Thư mục ứng dụng Streamlit Dashboard
│   ├── app.py                      # Mã nguồn chính của ứng dụng Dashboard (5 trang chuyên sâu)
│   └── README_Dashboard.md         # Tài liệu hướng dẫn riêng cho Dashboard
│
├── report/                         # Thư mục chứa báo cáo đồ án (PDF/Word)
│   └── .gitkeep
│
├── slides/                         # Thư mục chứa slide thuyết trình bảo vệ đồ án (PPTX/PDF)
│   └── .gitkeep
│
├── run_dashboard.bat               # Script khởi chạy 1-click cho Windows
├── run_dashboard.sh                # Script khởi chạy 1-click cho macOS / Linux
├── requirements.txt                # Danh sách thư viện Python phụ thuộc
├── .gitignore                      # Cấu hình loại bỏ file rác, cache và môi trường ảo
├── .gitattributes                  # Cấu hình chuẩn hóa ký tự xuống dòng
└── README.md                       # Tài liệu tổng thể hướng dẫn đồ án
```

---

## 3. Quy Mô Dữ Liệu Lịch Sử (Datasets)

Dự án khai thác 2 nguồn dữ liệu lớn, uy tín hàng đầu thế giới về thống kê bóng đá:

1. **Dữ liệu trận đấu (Match Data - Football-Data.co.uk):**
   - **Phạm vi:** **20 mùa giải liên tiếp (2005/06 – 2024/25)**.
   - **Quy mô:** **7,601 trận đấu**.
   - **Chỉ số:** Tỷ số hiệp 1 & chung cuộc, cú sút (`HS`, `AS`), sút trúng đích (`HST`, `AST`), phạt góc (`HC`, `AC`), phạm lỗi (`HF`, `AF`), thẻ vàng (`HY`, `AY`), thẻ đỏ (`HR`, `AR`).

2. **Dữ liệu cầu thủ đa mùa giải (Player Data - Understat):**
   - **Phạm vi:** **11 mùa giải liên tiếp (2014/15 – 2024/25)**.
   - **Quy mô:** **5,887 bản ghi cầu thủ** thi đấu tại Premier League.
   - **Chỉ số:** Số trận, số phút thi đấu, bàn thắng, kiến tạo, cú sút, đường chuyền quyết định (*Key Passes*), thẻ phạt và các thông số kỳ vọng hiện đại ($xG, xA, npxG, xG90, xA90$).

---

## 4. Hướng Dẫn Cài Đặt & Chạy Trên Mọi Máy (Quick Start)

Dự án được cấu hình độc lập hoàn toàn với đường dẫn tuyệt đối, cho phép chạy ngay trên **Windows**, **macOS** hoặc **Linux**.

### Yêu cầu tiên quyết
- Đã cài đặt **Python 3.9 trở lên** (khuyến nghị Python 3.10, 3.11 hoặc 3.12). Tải tại: [python.org](https://www.python.org/downloads/).
  *(Trên Windows, nhớ tích chọn **"Add Python to PATH"** trong quá trình cài đặt).*
- Đã cài đặt **Git** (hoặc tải trực tiếp mã nguồn bằng file ZIP từ GitHub).

---

### Bước 1: Clone Repository
Mở Terminal / PowerShell và tải repo về máy:
```bash
git clone https://github.com/nhpnhpnhp/EPL_ANALYTICS.git
cd EPL_ANALYTICS
```

---

### Bước 2: Cài đặt Môi Trường Ảo & Thư Viện

Khuyến nghị luôn sử dụng môi trường ảo (`.venv`) để tránh xung đột phiên bản thư viện giữa các dự án:

#### 🔹 Trên Windows (Command Prompt hoặc PowerShell):
```cmd
# 1. Tạo môi trường ảo
python -m venv .venv

# 2. Kích hoạt môi trường ảo
# Nếu dùng CMD:
.venv\Scripts\activate.bat
# Nếu dùng PowerShell:
.venv\Scripts\Activate.ps1

# 3. Nâng cấp pip và cài đặt thư viện
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### 🔹 Trên macOS / Linux (Terminal):
```bash
# 1. Tạo môi trường ảo
python3 -m venv .venv

# 2. Kích hoạt môi trường ảo
source .venv/bin/activate

# 3. Nâng cấp pip và cài đặt thư viện
pip install --upgrade pip
pip install -r requirements.txt
```

---

### Bước 3: Khởi chạy Streamlit Dashboard

Bạn có thể chạy ứng dụng theo một trong hai cách:

#### ⚡ Cách 1: Chạy bằng Script 1-Click (Tự động hoàn toàn)
- **Trên Windows**: Nhấp đúp (Double-click) vào file `run_dashboard.bat` (hoặc gõ `.\run_dashboard.bat` trong terminal). Script sẽ tự động kiểm tra, tạo môi trường nếu chưa có và bật Dashboard ngay lập tức.
- **Trên macOS / Linux**: Mở Terminal và chạy:
  ```bash
  chmod +x run_dashboard.sh
  ./run_dashboard.sh
  ```

#### 🛠️ Cách 2: Chạy thủ công qua lệnh
Đảm bảo đã kích hoạt `.venv`, sau đó chạy:
```bash
streamlit run dashboard/app.py
```

Sau khi khởi chạy, ứng dụng sẽ tự động mở trên trình duyệt tại:  
👉 **`http://localhost:8501`**

---

### Bước 4: Mở và Chạy Jupyter Notebook

File `EPL_Data_Analysis.ipynb` chứa toàn bộ 73 cells code, từ khâu làm sạch dữ liệu thô đến EDA, kiểm định giả thuyết thống kê và huấn luyện mô hình Machine Learning.

1. **Khởi chạy bằng Jupyter Notebook / Jupyter Lab**:
   ```bash
   # Kích hoạt .venv rồi chạy:
   jupyter notebook EPL_Data_Analysis.ipynb
   ```
2. **Khởi chạy trên Visual Studio Code (Khuyên dùng)**:
   - Mở thư mục dự án trong VS Code (`File > Open Folder... > EPL_ANALYTICS`).
   - Mở file `EPL_Data_Analysis.ipynb`.
   - Ở góc trên cùng bên phải của Notebook, nhấp vào **Select Kernel** -> Chọn **Python Environments...** -> Chọn môi trường ảo `.venv` vừa tạo.
   - Bạn có thể xem ngay các biểu đồ có sẵn hoặc bấm **"Run All"** để tái hiện toàn bộ phân tích từ đầu đến cuối một cách mượt mà.

---

## 5. Tóm Tắt Kết Quả 8 Câu Hỏi Nghiên Cứu (Research Findings)

| Mã RQ | Câu hỏi nghiên cứu | Phát hiện & Kết luận chính |
| :--- | :--- | :--- |
| **RQ1** | Xu hướng bàn thắng EPL thay đổi thế nào qua 20 năm? | Giai đoạn 2005-2010 duy trì ổn định ~2.5 bàn/trận; giai đoạn 2022-2024 tăng vọt lên mức kỷ lục **3.28 bàn/trận** nhờ triết lý pressing tầm cao và quy định cộng bù giờ mới. |
| **RQ2** | Lợi thế sân nhà (*Home Advantage*) có thực sự tồn tại? | Duy trì vững chắc suốt 20 năm (~47% chủ nhà thắng). Riêng mùa dịch COVID 2020-21 (sân không khán giả), tỷ lệ chủ nhà thắng giảm chạm đáy còn **37.9%**, chứng minh vai trò to lớn của sức ép cổ động viên. |
| **RQ3** | Đội bóng nào ổn định và xuất sắc nhất qua 2 thập kỷ? | **Man City, Man United, Chelsea, Arsenal, Liverpool** thống trị tuyệt đối với trên 400-450 trận thắng. Trong đó Man City thể hiện sự vượt trội áp đảo ở thập kỷ gần nhất (tỷ lệ thắng >70%). |
| **RQ4** | Mối quan hệ giữa số cú sút và bàn thắng? | Sút trúng đích (*Shots on Target*) có tương quan tuyến tính rất mạnh với số bàn thắng ($r \approx 0.98$). Tuy nhiên, chỉ số chất lượng vị trí dứt điểm ($xG$) mang tính quyết định cao hơn tổng số lượng sút. |
| **RQ5** | Cầu thủ nào có hiệu suất ghi bàn xuất sắc nhất thập kỷ? | **Harry Kane** và **Mohamed Salah** là 2 chân sút ổn định nhất (>150-200 bàn). **Erling Haaland** thiết lập hiệu suất vô tiền khoáng hậu (>1.0 bàn/90 phút). **Kevin De Bruyne** thống trị về kiến tạo (>100 assists). |
| **RQ6** | Hiệu suất thi đấu khác biệt thế nào theo vị trí? | Phân hóa rõ rệt: Tiền đạo tối ưu hóa số cú sút & tỷ lệ chuyển hóa bàn thắng; Tiền vệ kiến thiết cơ hội ($xA$, *Key Passes*); Hậu vệ đóng góp ổn định qua thu hồi bóng và dâng cao hỗ trợ biên. |
| **RQ7** | Chỉ số trong trận nào tác động mạnh nhất đến kết quả? | Số cú sút trúng đích (`HST`, `AST`) và thẻ phạt ảnh hưởng trực tiếp nhất đến kết quả chung cuộc. Phạt góc có tương quan tương đối thấp với khả năng tạo bàn thắng. |
| **RQ8** | Có thể dự đoán kết quả trận đấu mà không bị rò rỉ dữ liệu? | Áp dụng mô hình **Random Forest** dựa trên 5 trận gần nhất (*Rolling 5-match form*), độ chính xác đạt **~51%** trên tập kiểm thử ngoài thời gian (2 mùa giải 2023-2025). |

---

## 6. Mô Hình Học Máy Dự Đoán Trận Đấu (AI Match Predictor)

Mô hình dự đoán trong đồ án được thiết kế với chuẩn mực chống rò rỉ dữ liệu nghiêm ngặt:
- **Phương pháp kỹ thuật đặc trưng**: Tính toán trung bình trượt của 5 trận đấu gần nhất (*Rolling 5-match window*) theo từng đội bóng cho các chỉ số: Số bàn thắng/bàn thua, số cú sút, sút trúng đích, phạt góc, tỷ lệ điểm kiếm được.
- **Phân chia dữ liệu theo thời gian (Out-of-Time Split)**:
  - **Tập Train**: 18 mùa giải đầu (2005/06 đến 2022/23, ~6,840 trận).
  - **Tập Test**: 2 mùa giải gần nhất (2023/24 và 2024/25, ~760 trận).
- **Thuật toán áp dụng**: So sánh giữa `Logistic Regression` (Baseline) và `Random Forest Classifier`.
- **Tích hợp Dashboard**: Trang 5 của Streamlit Hub cho phép chọn 2 CLB bất kỳ để mô phỏng trận đấu và xuất ra xác suất % Thắng - Hòa - Thua theo thời gian thực.

---

## 7. Khắc Phục Sự Cố Thường Gặp (Troubleshooting & FAQ)

### ❓ 1. Lỗi PowerShell: "running scripts is disabled on this system"
**Nguyên nhân:** Chính sách bảo mật mặc định của Windows PowerShell không cho phép thực thi script kích hoạt `.venv\Scripts\Activate.ps1`.  
**Cách xử lý:** Mở PowerShell và cấp quyền tạm thời cho phiên làm việc hiện tại:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```
*Hoặc đơn giản hơn: sử dụng Command Prompt (`cmd.exe`) và chạy `.venv\Scripts\activate.bat`, hoặc nhấp đúp vào `run_dashboard.bat`.*

### ❓ 2. Lỗi "streamlit: command not found" hoặc "The term 'streamlit' is not recognized"
**Nguyên nhân:** Bạn chưa kích hoạt môi trường ảo `.venv` hoặc chưa cài đặt `requirements.txt`.  
**Cách xử lý:**
```bash
# Đảm bảo đã kích hoạt môi trường ảo trước:
# Trên Windows:
.venv\Scripts\activate
# Trên macOS/Linux:
source .venv/bin/activate

# Cài đặt lại thư viện:
pip install -r requirements.txt
```
*Bạn cũng có thể chạy trực tiếp thông qua Python:*
```bash
python -m streamlit run dashboard/app.py
```

### ❓ 3. Lỗi xung đột cổng: "Port 8501 is already in use"
**Cách xử lý:** Chỉ định một cổng khả dụng khác (ví dụ `8502`):
```bash
streamlit run dashboard/app.py --server.port 8502
```

### ❓ 4. VS Code không nhận diện kernel của `.venv` khi mở Notebook
**Cách xử lý:**
1. Cài đặt tiện ích mở rộng **Python** và **Jupyter** trên VS Code.
2. Mở file `EPL_Data_Analysis.ipynb`.
3. Bấm vào nút chọn Kernel ở góc phải trên -> chọn **Enter interpreter path...** -> Duyệt đến file `.venv/Scripts/python.exe` (Windows) hoặc `.venv/bin/python` (macOS/Linux).

### ❓ 5. Không tìm thấy dữ liệu khi chạy Dashboard
**Cách xử lý:** Đảm bảo bạn đang đứng tại thư mục gốc của repository khi chạy lệnh:
```bash
# ĐÚNG:
streamlit run dashboard/app.py

# Nếu đứng trong thư mục dashboard/:
streamlit run app.py
```
*(Hệ thống đã được lập trình dự phòng đa tầng để tự động tìm kiếm thư mục dữ liệu ở cả thư mục cha và thư mục hiện hành).*

---

## 📜 Giấy Phép & Bản Quyền (License)
Dự án được phân phối dưới giấy phép mã nguồn mở MIT License. Dữ liệu phục vụ cho mục đích học tập và nghiên cứu phi thương mại.
