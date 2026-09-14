# ĐỒ ÁN PHÂN TÍCH DỮ LIỆU BÓNG ĐÁ NGOẠI HẠNG ANH (EPL ANALYTICS)

> **Đề tài:** Thống kê và phân tích lịch sử giải bóng đá Ngoại hạng Anh (English Premier League – EPL) và hiệu suất cầu thủ.  
> **Chuyên ngành:** Kỹ thuật Dữ liệu (Data Engineering) / Khoa học Dữ liệu (Data Science).  
> **Thực hiện:** Nhóm 2 sinh viên.

---

## 1. Quy Mô Dữ Liệu Đã Được Mở Rộng Toàn Diện (Expanded Datasets)

Dự án đã được nâng cấp mạnh mẽ về cả **chiều sâu lịch sử** lẫn **độ chi tiết của các chỉ số nâng cao**, giải quyết triệt để vấn đề "thiếu dữ liệu":

1. **Dữ liệu trận đấu (Match Data):**
   - **Quy mô:** **20 mùa giải liên tiếp (2005/06 đến 2024/25)** với **7,601 trận đấu**.
   - **Nguồn:** Football-Data.co.uk.
   - **Thông tin:** Kết quả trận đấu, tỷ số hiệp 1 & cả trận, số cú sút, sút trúng đích, phạt góc, phạm lỗi, thẻ phạt của từng đội.
2. **Dữ liệu cầu thủ đa mùa giải (Player Data):**
   - **Quy mô:** **11 mùa giải liên tiếp (2014/15 đến 2024/25)** với **5,887 bản ghi cầu thủ**.
   - **Nguồn:** Understat (tích hợp dữ liệu xG chuyên sâu).
   - **Thông tin:** Số phút thi đấu, số trận, bàn thắng, kiến tạo, số cú sút, đường chuyền quyết định (Key Passes), thẻ phạt và các chỉ số thống kê kỳ vọng tiên tiến ($xG, xA, npxG$).

---

## 2. Cấu Trúc Dự Án (Project Structure)

Toàn bộ logic từ thu thập, làm sạch, EDA, trực quan hóa và Machine Learning được thực thi trong **một file Jupyter Notebook duy nhất**:

```text
ttdltq/
│
├── EPL_Data_Analysis.ipynb         # Notebook chính duy nhất (73 cells, chạy tuần tự từ trên xuống dưới)
│
├── data/
│   ├── raw/
│   │   ├── matches/                # 20 file CSV mùa giải (2005-06 đến 2024-25)
│   │   └── players/                # Dữ liệu cầu thủ Understat 11 mùa giải
│   │
│   └── processed/
│       ├── matches_clean.csv       # 7,601 trận đấu đã làm sạch
│       └── players_clean.csv       # 5,887 bản ghi cầu thủ đã chuẩn hóa
│
├── dashboard/                      # Thư mục chứa báo cáo Dashboard tương tác
│   └── README_Dashboard.md         # Hướng dẫn kết nối Power BI
│
├── report/                         # Báo cáo đồ án (PDF/Word)
├── slides/                         # Slide thuyết trình bảo vệ đồ án
├── requirements.txt                # Thư viện phụ thuộc
└── README.md                       # Tài liệu hướng dẫn đồ án
```

---

## 3. Các Câu Hỏi Nghiên Cứu Đã Được Giải Quyết (Research Questions)

| Mã RQ | Câu hỏi nghiên cứu | Kết quả & Phát hiện chính trên tập dữ liệu mở rộng |
| :--- | :--- | :--- |
| **RQ1** | Xu hướng bàn thắng EPL thay đổi thế nào qua 20 năm? | Giai đoạn 2005-2010 duy trì ~2.5 bàn/trận; giai đoạn 2022-2024 tăng vọt lên kỷ lục **3.28 bàn/trận** phản ánh triết lý tấn công pressing hiện đại và thời gian bù giờ dài hơn. |
| **RQ2** | Lợi thế sân nhà (Home Advantage) có tồn tại không? | Tồn tại bền vững suốt 20 năm (~47% chủ nhà thắng). Riêng mùa dịch COVID 2020-21 (không khán giả), tỷ lệ chủ nhà thắng giảm xuống chỉ còn **37.9%**, chứng minh vai trò to lớn của khán giả. |
| **RQ3** | Đội bóng nào ổn định và xuất sắc nhất 20 năm? | **Manchester United, Chelsea, Man City, Arsenal, Liverpool** tạo thành nhóm ngũ đại gia thống trị với hơn 400-450 trận thắng. Man City bứt phá áp đảo ở thập kỷ gần nhất. |
| **RQ4** | Số cú sút có liên quan đến bàn thắng không? | Sút trúng đích (**Shots on Target**) có tương quan tuyến tính rất mạnh với bàn thắng ($r \approx 0.98$). Tuy nhiên chất lượng góc sút ($xG$) quan trọng hơn số lượng sút. |
| **RQ5** | Cầu thủ nào có hiệu suất ghi bàn tốt nhất thập kỷ? | **Harry Kane** và **Mohamed Salah** là hai cỗ máy săn bàn bền bỉ nhất (>150-200 bàn). **Erling Haaland** đạt hiệu suất Per 90 vô tiền khoáng hậu (>1.0 bàn/90 phút). **Kevin De Bruyne** dẫn đầu kiến tạo (>100 assists). |
| **RQ6** | Hiệu suất cầu thủ khác biệt thế nào theo vị trí? | Phân hóa rõ rệt qua 11 mùa giải: Tiền đạo tối ưu hóa số cú sút & bàn thắng, Tiền vệ thống trị kiến tạo ($xA$) và $KeyPasses$, Hậu vệ gánh vác các chỉ số phòng ngự. |
| **RQ7** | Yếu tố trận đấu nào liên quan mạnh nhất tới kết quả? | Số cú sút trúng đích (HST, AST) và Thẻ phạt ảnh hưởng trực tiếp và mạnh nhất tới bàn thắng và kết quả. Phạt góc có tương quan tương đối thấp với bàn thắng. |
| **RQ8** | Có thể dự đoán kết quả trận đấu không bị rò rỉ dữ liệu? | Mô hình `Logistic Regression` và `Random Forest` dựa trên phong độ 5 trận gần nhất (Rolling 5 matches, hoàn toàn không leakage trên 7,400 trận) đạt độ chính xác **~51%** trên tập test 2 mùa mới nhất. |

---

## 4. Hướng Dẫn Chạy Dự Án (How to Run)

### Môi trường và Thư viện
```bash
pip install -r requirements.txt
```

### Mở và chạy Notebook
1. Mở file `EPL_Data_Analysis.ipynb` trong VS Code hoặc Jupyter Notebook.
2. File đã được chạy và nhúng sẵn toàn bộ biểu đồ và output. Bạn có thể bấm **"Run All"** để chạy lại toàn bộ từ đầu một cách mượt mà.
