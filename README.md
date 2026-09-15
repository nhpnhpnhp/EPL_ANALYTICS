# ⚽ ĐỒ ÁN PHÂN TÍCH DỮ LIỆU BÓNG ĐÁ NGOẠI HẠNG ANH (EPL ANALYTICS)

[![Python](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![Records](https://img.shields.io/badge/Records-74%2C350%2B%20EPL%20Rows-success)](#)
[![Seasons](https://img.shields.io/badge/Seasons-32%20Seasons%20(1993--2025)-purple)](#)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](#)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#)

> **Đề tài:** Thống kê, phân tích lịch sử giải bóng đá Ngoại hạng Anh (English Premier League – EPL), hiệu suất cầu thủ ($xG/xA$) và xây dựng mô hình AI dự đoán kết quả trận đấu.  
> **Chuyên ngành:** Kỹ thuật Dữ liệu (Data Engineering) / Khoa học Dữ liệu (Data Science).  
> **Thực hiện:** Nhóm 2 sinh viên.

---

## 📑 Mục Lục
1. [Giới Thiệu Đề Tài & Điểm Nổi Bật](#1-giới-thiệu-đề-tài--điểm-nổi-bật)
2. [Quy Mô Dữ Liệu Thuần EPL Mở Rộng (>74,000 Bản Ghi)](#2-quy-mô-dữ-liệu-thuần-epl-mở-rộng-74000-bản-ghi)
3. [Cấu Trúc Thư Mục Chuẩn (Project Structure)](#3-cấu-trúc-thư-mục-chuẩn-project-structure)
4. [Các Biểu Đồ Nâng Cao Được Tích Hợp Trên Dashboard](#4-các-biểu-đồ-nâng-cao-được-tích-hợp-trên-dashboard)
5. [Hướng Dẫn Cài Đặt & Chạy Trên Mọi Máy (Quick Start)](#5-hướng-dẫn-cài-đặt--chạy-trên-mọi-máy-quick-start)
   - [Yêu cầu tiên quyết](#yêu-cầu-tiên-quyết)
   - [Bước 1: Clone Repository](#bước-1-clone-repository)
   - [Bước 2: Cài đặt Môi Trường Ảo & Thư Viện](#bước-2-cài-đặt-môi-trường-ảo--thư-viện)
   - [Bước 3: Khởi chạy Streamlit Dashboard](#bước-3-khởi-chạy-streamlit-dashboard)
   - [Bước 4: Mở và Chạy Jupyter Notebook](#bước-4-mở-và-chạy-jupyter-notebook)
6. [Tóm Tắt Kết Quả 8 Câu Hỏi Nghiên Cứu (Research Findings)](#6-tóm-tắt-kết-quả-8-câu-hỏi-nghiên-cứu-research-findings)
7. [Mô Hình Học Máy Dự Đoán Trận Đấu (AI Match Predictor)](#7-mô-hình-học-máy-dự-đoán-trận-đấu-ai-match-predictor)
8. [Khắc Phục Sự Cố Thường Gặp (Troubleshooting & FAQ)](#8-khắc-phục-sự-cố-thường-gặp-troubleshooting--faq)

---

## 1. Giới Thiệu Đề Tài & Điểm Nổi Bật

Dự án **EPL Analytics** là một giải pháp phân tích dữ liệu thể thao toàn diện, kết hợp chặt chẽ giữa:
- **Data Engineering**: Thu thập, chuẩn hóa và tổng hợp **100% dữ liệu thuần Ngoại Hạng Anh** qua **32 mùa giải lịch sử (1993/94 – 2024/25)** với hơn **74,300+ bản ghi**.
- **Exploratory Data Analysis (EDA)**: Giải quyết 8 câu hỏi nghiên cứu then chốt của bóng đá hiện đại với hệ thống biểu đồ nâng cao: **World Choropleth Map**, **Violin Plot**, **Tactical Correlation Heatmap**, **Season Matrix Heatmap**, **Radar Spider Chart**, **Treemap**.
- **Machine Learning**: Xây dựng mô hình phân loại dự đoán kết quả trận đấu (Thắng - Hòa - Thua) dựa trên chuỗi phong độ cuốn chiếu (*Rolling 5-match window*), kiểm thử ngoài thời gian (*Out-of-Time Validation*) hoàn toàn không rò rỉ dữ liệu (*No Data Leakage*).
- **Interactive Web App**: Ứng dụng **Streamlit Interactive Hub** được thiết kế lại theo dạng thẻ **Tabs (`st.tabs`)** thông minh, mang phong cách Premier League hiện đại, hỗ trợ tương tác trực quan theo thời gian thực.

---

## 2. Quy Mô Dữ Liệu Thuần EPL Mở Rộng (>74,000 Bản Ghi)

Dữ liệu của đồ án hoàn toàn thuộc về giải Ngoại Hạng Anh (English Premier League), đạt quy mô kỷ lục:

1. **Dữ liệu trận đấu (Match Data - 32 Mùa Giải Liên Tiếp):**
   - **Phạm vi:** Từ mùa giải **1993/94 đến 2024/25** (32 năm lịch sử Ngoại Hạng Anh).
   - **Quy mô:** **12,234 trận đấu** (`matches_clean.csv`).
   - **Chỉ số:** Ngày thi đấu, Đội nhà, Đội khách, Tỷ số cả trận (`FTHG`, `FTAG`, `FTR`), Tỷ số hiệp 1 (`HTHG`, `HTAG`), Cú sút (`HS`, `AS`), Sút trúng đích (`HST`, `AST`), Phạt góc (`HC`, `AC`), Phạm lỗi (`HF`, `AF`), Thẻ vàng (`HY`, `AY`), Thẻ đỏ (`HR`, `AR`).

2. **Dữ liệu cầu thủ đa tầng (Player Performance Data - Thuần EPL):**
   - **Quy mô:** **62,117 bản ghi** (`players_clean.csv`).
   - **Bao gồm:**
     - **5,887 bản ghi tổng hợp mùa giải** (Understat 2014-2025): Bàn thắng, kiến tạo, $xG, xA, npxG$, cú sút, key passes, số phút.
     - **56,230 bản ghi nhật ký từng trận** (FPL Match Performance): Điểm số, phong độ từng vòng đấu, $xGI$, ICT Index.
     - **Bản đồ quốc tịch:** Tích hợp mã quốc gia ISO-3 của hơn **2,460+ cầu thủ** đến từ **50 quốc gia** trên thế giới.

👉 **TỔNG QUY MÔ DỮ LIỆU ĐÃ XỬ LÝ:** **12,234 + 62,117 = 74,351 BẢN GHI THUẦN NGOẠI HẠNG ANH!**

---

## 3. Cấu Trúc Thư Mục Chuẩn (Project Structure)

```text
EPL_ANALYTICS/
│
├── EPL_Data_Analysis.ipynb         # Notebook phân tích chính (73 cells chạy tuần tự từ A -> Z)
│
├── data/
│   ├── raw/
│   │   ├── matches/                # 32 file CSV kết quả trận đấu (từ mùa 1993-94 đến 2024-25)
│   │   └── players/                # Dữ liệu cầu thủ Understat & FPL match logs
│   │
│   └── processed/
│       ├── matches_clean.csv       # 12,234 trận đấu sau khi làm sạch (1993 - 2025)
│       └── players_clean.csv       # 62,117 bản ghi cầu thủ chuẩn hóa với xG/xA và quốc tịch
│
├── dashboard/                      # Thư mục ứng dụng Streamlit Dashboard
│   ├── app.py                      # Mã nguồn ứng dụng (5 trang chuyên sâu, bố cục Tabs hiện đại)
│   └── README_Dashboard.md         # Hướng dẫn chi tiết cho Dashboard
│
├── report/                         # Thư mục chứa báo cáo đồ án (PDF/Word)
│   └── .gitkeep
│
├── slides/                         # Thư mục chứa slide thuyết trình bảo vệ đồ án (PPTX/PDF)
│   └── .gitkeep
│
├── run_dashboard.bat               # Script khởi chạy 1-click tự động cho Windows (CRLF)
├── run_dashboard.sh                # Script khởi chạy 1-click tự động cho macOS / Linux
├── requirements.txt                # Danh sách thư viện Python phụ thuộc
├── .gitignore                      # Cấu hình loại bỏ file rác, cache và virtual environment
├── .gitattributes                  # Cấu hình chuẩn hóa ký tự xuống dòng
└── README.md                       # Tài liệu tổng thể hướng dẫn đồ án
```

---

## 4. Các Biểu Đồ Nâng Cao Được Tích Hợp Trên Dashboard

| Biểu Đồ Nâng Cao | Thư Viện | Ý Nghĩa Phân Tích & Điểm Nhấn |
| :--- | :--- | :--- |
| 🌍 **World Choropleth Map (Bản đồ Dấu ấn Toàn cầu)** | `plotly.express.choropleth` | Thể hiện mức độ quốc tế hóa của Premier League qua 50 quốc gia: tô màu theo Số lượng cầu thủ, Tổng bàn thắng, Tổng kiến tạo. |
| 🎻 **Violin Plot (Mật độ phân phối chỉ số)** | `plotly.express.violin` | Trực quan hóa đường cong mật độ xác suất (KDE) kết hợp Boxplot thể hiện sự phân hóa chỉ số $xG, xA$, Goals theo Vị trí thi đấu (Tiền đạo, Tiền vệ, Hậu vệ). |
| 🗺️ **Tactical Correlation Heatmap** | `plotly.express.imshow` | Ma trận tương quan hệ số Pearson giữa các chỉ số kỹ thuật (Bàn thắng, Sút, Sút trúng đích, Phạt góc, Phạm lỗi, Thẻ phạt). |
| 📅 **Club Season Performance Heatmap** | `plotly.graph_objects.Heatmap` | Ma trận nhiệt 15 mùa giải x Top 12 CLB thể hiện điểm số đạt được qua từng thời kỳ lịch sử. |
| 🕸️ **Radar Spider Chart (Đa giác kỹ năng)** | `plotly.graph_objects.Scatterpolar` | Biểu đồ mạng nhện đa giác 7 trục kỹ năng (Dứt điểm, xG, Kiến tạo, xA, Cú sút, Tạo cơ hội, Kỷ luật) khi so sánh đối đầu giữa 2 ngôi sao. |
| 🌳 **Treemap (Cây phân cấp bàn thắng)** | `plotly.express.treemap` | Cây phân cấp trực quan hóa cơ cấu bàn thắng: Câu lạc bộ EPL -> Cầu thủ ghi bàn chủ lực (tô màu theo độ vượt kỳ vọng $xG\_Diff$). |

---

## 5. Hướng Dẫn Cài Đặt & Chạy Trên Mọi Máy (Quick Start)

Dự án được cấu hình độc lập hoàn toàn với đường dẫn tuyệt đối, cho phép chạy ngay trên **Windows**, **macOS** hoặc **Linux**.

### Yêu cầu tiên quyết
- Đã cài đặt **Python 3.9 trở lên** (khuyến nghị Python 3.10, 3.11 hoặc 3.12). Tải tại: [python.org](https://www.python.org/downloads/).
  *(Trên Windows, nhớ tích chọn **"Add Python to PATH"** khi cài đặt).*
- Đã cài đặt **Git** (hoặc tải mã nguồn file ZIP từ GitHub).

---

### Bước 1: Clone Repository
Mở Terminal / PowerShell và tải repo về máy:
```bash
git clone https://github.com/nhpnhpnhp/EPL_ANALYTICS.git
cd EPL_ANALYTICS
```

---

### Bước 2: Cài đặt Môi Trường Ảo & Thư Viện

#### 🔹 Trên Windows (Command Prompt hoặc PowerShell):
```cmd
# 1. Tạo môi trường ảo
python -m venv .venv

# 2. Kích hoạt môi trường ảo
# Nếu dùng CMD:
.venv\Scripts\activate.bat
# Nếu dùng PowerShell:
.venv\Scripts\Activate.ps1

# 3. Cài đặt thư viện
pip install -r requirements.txt
```

#### 🔹 Trên macOS / Linux (Terminal):
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

### Bước 3: Khởi chạy Streamlit Dashboard

#### ⚡ Cách 1: Chạy bằng Script 1-Click (Tự động hoàn toàn)
- **Trên Windows**: Nhấp đúp vào file `run_dashboard.bat`. Script sẽ tự động nhận diện môi trường `.venv` và bật Dashboard ngay lập tức.
- **Trên macOS / Linux**: Mở Terminal và chạy:
  ```bash
  chmod +x run_dashboard.sh
  ./run_dashboard.sh
  ```

#### 🛠️ Cách 2: Chạy thủ công qua lệnh
```bash
# Trên Windows:
.venv\Scripts\python.exe -m streamlit run dashboard\app.py

# Hoặc:
streamlit run dashboard/app.py
```

Sau khi khởi chạy, trình duyệt web sẽ tự động mở tại: 👉 **`http://localhost:8501`**

---

### Bước 4: Mở và Chạy Jupyter Notebook

1. Mở thư mục dự án trong **Visual Studio Code**.
2. Mở file `EPL_Data_Analysis.ipynb`.
3. Nhấp vào **Select Kernel** ở góc trên cùng bên phải -> chọn môi trường ảo `.venv`.
4. Bấm **"Run All"** để tái hiện toàn bộ phân tích từ đầu đến cuối một cách mượt mà.

---

## 6. Tóm Tắt Kết Quả 8 Câu Hỏi Nghiên Cứu (Research Findings)

| Mã RQ | Câu hỏi nghiên cứu | Phát hiện & Kết luận chính trên tập dữ liệu mở rộng 32 mùa giải |
| :--- | :--- | :--- |
| **RQ1** | Xu hướng bàn thắng EPL thay đổi thế nào qua 32 năm? | Giai đoạn 1993-2015 dao động ổn định ~2.5 - 2.7 bàn/trận; giai đoạn 2022-2024 tăng vọt lên mức kỷ lục **3.28 bàn/trận** nhờ chiến thuật pressing hiện đại và thời gian bù giờ dài hơn. |
| **RQ2** | Lợi thế sân nhà (*Home Advantage*) có thực sự tồn tại? | Duy trì vững chắc suốt 32 năm (~47% chủ nhà thắng). Riêng mùa dịch COVID 2020-21 (không khán giả), tỷ lệ chủ nhà thắng giảm xuống mức kỷ lục chỉ còn **37.9%**, chứng minh vai trò to lớn của sức ép khán đài. |
| **RQ3** | Đội bóng nào ổn định và xuất sắc nhất qua hơn 3 thập kỷ? | **Manchester United, Arsenal, Chelsea, Liverpool, Manchester City** thống trị tuyệt đối về số điểm và số trận thắng trong kỷ nguyên Ngoại Hạng Anh. |
| **RQ4** | Mối quan hệ giữa số cú sút và bàn thắng? | Sút trúng đích (*Shots on Target*) có tương quan tuyến tính rất mạnh với bàn thắng ($r \approx 0.98$). Tuy nhiên chất lượng góc sút ($xG$) mang tính quyết định cao hơn số lượng sút đơn thuần. |
| **RQ5** | Cầu thủ nào có hiệu suất ghi bàn xuất sắc nhất thập kỷ? | **Harry Kane** và **Mohamed Salah** là hai cỗ máy săn bàn ổn định nhất (>150-200 bàn). **Erling Haaland** đạt hiệu suất Per 90 vô tiền khoáng hậu (>1.0 bàn/90 phút). **Kevin De Bruyne** thống trị về kiến tạo. |
| **RQ6** | Hiệu suất thi đấu khác biệt thế nào theo vị trí? | Biểu đồ **Violin Plot** phân hóa rõ nét: Tiền đạo tập trung tối đa vào số cú sút & bàn thắng; Tiền vệ chiếm lĩnh kiến tạo ($xA$) và Key Passes; Hậu vệ đóng góp ổn định qua thu hồi bóng và dâng cao hỗ trợ. |
| **RQ7** | Chỉ số trong trận nào tác động mạnh nhất đến kết quả? | Số cú sút trúng đích (`HST`, `AST`) và thẻ phạt ảnh hưởng trực tiếp nhất tới kết quả trận đấu. Phạt góc có tương quan tương đối thấp với khả năng tạo bàn thắng. |
| **RQ8** | Có thể dự đoán kết quả trận đấu mà không bị rò rỉ dữ liệu? | Mô hình **Random Forest** dựa trên phong độ 5 trận gần nhất (*Rolling 5-match window*) đạt độ chính xác **~51%** trên tập kiểm thử ngoài thời gian (2 mùa giải gần nhất). |

---

## 7. Mô Hình Học Máy Dự Đoán Trận Đấu (AI Match Predictor)

- **Đặc trưng đầu vào**: Điểm số, bàn thắng ghi được, bàn thua trung bình trong 5 trận gần nhất của Đội Chủ Nhà và Đội Khách.
- **Phân chia dữ liệu theo thời gian (Out-of-Time Validation)**: Đảm bảo tính trung thực tuyệt đối, không rò rỉ thông tin tương lai.
- **Tích hợp Dashboard**: Trang 5 cung cấp công cụ mô phỏng dự đoán trận đấu theo thời gian thực và biểu đồ Feature Importance giải thích quyết định của mô hình.

---

## 8. Khắc Phục Sự Cố Thường Gặp (Troubleshooting & FAQ)

### ❓ 1. Lỗi Windows Security: "Cài đặt bảo mật Internet của bạn đã ngăn việc mở một hoặc nhiều tệp"
**Cách xử lý:** Nhấp chuột phải vào file `run_dashboard.bat` -> Chọn **Properties** -> Ở mục Security dưới cùng, tích chọn ô ☑️ **Unblock** -> Nhấn **OK**.  
*Hoặc mở terminal chạy trực tiếp: `.venv\Scripts\python.exe -m streamlit run dashboard\app.py`.*

### ❓ 2. Lỗi PowerShell: "running scripts is disabled on this system"
**Cách xử lý:** Chạy lệnh sau trên PowerShell để cấp quyền cho phiên làm việc:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

### ❓ 3. Lỗi chiếm dụng cổng: "Port 8501 is already in use"
**Cách xử lý:** Chỉ định một cổng khả dụng khác:
```bash
streamlit run dashboard/app.py --server.port 8502
```

---

## 📜 Giấy Phép & Bản Quyền (License)
Dự án được phân phối dưới giấy phép mã nguồn mở MIT License. Toàn bộ dữ liệu phục vụ mục đích học tập và nghiên cứu phi thương mại.
