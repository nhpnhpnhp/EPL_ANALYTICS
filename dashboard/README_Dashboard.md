# HƯỚNG DẪN KHỞI CHẠY STREAMLIT DASHBOARD (EPL ANALYTICS)

Dự án đã được tích hợp một ứng dụng **Streamlit Interactive Dashboard** trực quan, hiện đại tại [dashboard/app.py](app.py) với quy mô **74,351 bản ghi thuần Ngoại Hạng Anh (EPL)** và hệ thống biểu đồ nâng cao chuyên sâu.

---

## 1. Cách Khởi Chạy Dashboard

### ⚡ Cách 1: Khởi chạy 1-Click tự động (Khuyên dùng)
- **Trên Windows**: Double-click vào file `run_dashboard.bat` (hoặc mở terminal gõ `.\run_dashboard.bat`). File script sẽ tự động kiểm tra môi trường, nhận diện `.venv` và khởi chạy ngay ứng dụng.
- **Trên macOS / Linux**: Mở Terminal tại thư mục gốc dự án và chạy:
  ```bash
  chmod +x run_dashboard.sh
  ./run_dashboard.sh
  ```

---

### 🛠️ Cách 2: Khởi chạy thủ công qua dòng lệnh

#### Trên Windows (PowerShell / Command Prompt):
```powershell
# Cách nhanh nhất:
.venv\Scripts\python.exe -m streamlit run dashboard\app.py

# Hoặc kích hoạt môi trường ảo:
.venv\Scripts\activate
streamlit run dashboard/app.py
```

#### Trên macOS / Linux (Terminal):
```bash
source .venv/bin/activate
streamlit run dashboard/app.py
```

Sau khi chạy lệnh thành công, trình duyệt web sẽ tự động mở tại địa chỉ:  
👉 **`http://localhost:8501`**

---

## 2. Các Chức Năng & Biểu Đồ Nâng Cao Nổi Bật

Ứng dụng được thiết kế lại với cấu trúc **Tabbed Navigation (`st.tabs`)** hiện đại, mang đậm phong cách Premier League:

1. **📊 Trang 1 - Tổng Quan & Lịch Sử EPL (32 Mùa Giải 1993 - 2025):**
   - **KPI Cards:** Tổng số trận (12,234), Tổng bàn thắng, Bàn thắng TB/trận, Tỷ lệ chủ nhà thắng, Cú sút TB/trận.
   - *Tab 1: Xu hướng bàn thắng & Tỷ lệ kết quả:* Bar + Line Chart xu hướng bàn thắng 32 năm và Donut Chart kết quả Thắng/Hòa/Thua.
   - *Tab 2: Lợi thế sân nhà & Tác động COVID-19:* Phân tích tỷ lệ thắng sân nhà và vùng trũng lịch sử mùa dịch 2020-21 (37.9%).
   - *Tab 3: 🌍 Bản đồ Dấu ấn Toàn cầu (World Choropleth Map):* Bản đồ nhiệt tương tác toàn cầu thể hiện số lượng cầu thủ, tổng bàn thắng và $xG$ theo từng quốc gia tại EPL.

2. **🏆 Trang 2 - Hiệu Suất Câu Lạc Bộ & Chiến Thuật:**
   - *Tab 1: Bảng xếp hạng & Bàn thắng CLB:* Tùy chọn xem Bảng tổng sắp 32 năm lịch sử HOẶC xem riêng từng mùa giải cụ thể.
   - *Tab 2: 🗺️ Ma trận tương quan (Tactical Correlation Heatmap) & Heatmap 32 năm:* Phân tích tương quan giữa các chỉ số kỹ thuật và Heatmap điểm số CLB qua các thời kỳ.
   - *Tab 3: ⚔️ So sánh nhóm "Big Six":* Tổng điểm kỷ nguyên EPL và biểu đồ phân tán hiệu suất sút trúng đích vs chuyển hóa bàn thắng.

3. **👟 Trang 3 - Phân Tích Cầu Thủ & Chỉ Số Kỳ Vọng ($xG, xA$):**
   - Kho dữ liệu hơn **62,000 bản ghi** cầu thủ EPL (tổng kết mùa giải & nhật ký từng trận).
   - *Tab 1: 🎯 Bàn thắng thực tế vs Bàn thắng kỳ vọng ($xG$):* Interactive Scatter Plot kèm đường chuẩn $y=x$ nhận diện Overperformer & Underperformer.
   - *Tab 2: 🎻 Phân phối mật độ (Violin Plot):* Trực quan hóa đường cong mật độ xác suất và boxplot của $xG, xA$, Bàn thắng, Số phút theo từng Vị trí thi đấu.
   - *Tab 3: 🌳 Cây phân cấp bàn thắng (Treemap):* Cấu trúc đóng góp bàn thắng CLB -> Cầu thủ với màu sắc thể hiện độ vượt kỳ vọng.
   - *Tab 4: 📊 Bảng xếp hạng chi tiết:* Bảng số liệu đa chỉ số có gradient nổi bật.

4. **⚔️ Trang 4 - So Sánh Đối Đầu Cầu Thủ (Head-to-Head):**
   - *Tab 1: 🕸️ Biểu đồ Radar đa giác kỹ năng (Spider Chart):* So sánh trực diện 2 ngôi sao trên 7 trục kỹ năng (Goals/90, xG/90, Assists/90, xA/90, Shots/90, KeyPasses/90, Kỷ luật).
   - *Tab 2: 📋 Thống kê chi tiết & Profile Cards:* Thẻ hồ sơ và Bar Chart so sánh ngang các chỉ số Per 90.

5. **🔮 Trang 5 - AI Match Predictor (Dự Đoán Trận Đấu):**
   - *Tab 1: 🔮 Mô phỏng dự đoán kết quả:* Machine Learning Random Forest tính toán xác suất Thắng - Hòa - Thua theo thời gian thực dựa trên Rolling 5-match form.
   - *Tab 2: 🧠 Tầm quan trọng đặc trưng (Feature Importance):* Giải thích trực quan yếu tố phong độ nào ảnh hưởng mạnh nhất tới kết quả.
