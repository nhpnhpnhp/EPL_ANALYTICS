# HƯỚNG DẪN KHỞI CHẠY STREAMLIT DASHBOARD (EPL ANALYTICS)

Dự án đã được tích hợp một ứng dụng **Streamlit Interactive Dashboard** trực quan, hiện đại tại [dashboard/app.py](app.py).

---

## 1. Cách Khởi Chạy Dashboard

### Cách 1: Khởi chạy 1-Click tự động (Khuyên dùng)
- **Trên Windows**: Double-click vào file `run_dashboard.bat` (hoặc mở terminal gõ `.\run_dashboard.bat`). File script sẽ tự động kiểm tra môi trường, tạo virtual environment và cài đặt thư viện nếu chưa có, sau đó khởi chạy ngay ứng dụng.
- **Trên macOS / Linux**: Mở Terminal tại thư mục gốc dự án và chạy:
  ```bash
  chmod +x run_dashboard.sh
  ./run_dashboard.sh
  ```

---

### Cách 2: Khởi chạy thủ công qua dòng lệnh

#### Trên Windows (PowerShell / Command Prompt):
```powershell
# 1. Kích hoạt môi trường ảo
.venv\Scripts\activate

# 2. Chạy ứng dụng Streamlit
streamlit run dashboard/app.py
```

#### Trên macOS / Linux (Terminal):
```bash
# 1. Kích hoạt môi trường ảo
source .venv/bin/activate

# 2. Chạy ứng dụng Streamlit
streamlit run dashboard/app.py
```

Sau khi chạy lệnh thành công, trình duyệt web sẽ tự động mở tại địa chỉ:  
👉 **`http://localhost:8501`**

> [!TIP]
> Nếu cổng `8501` đang bị chiếm dụng bởi ứng dụng khác, bạn có thể chỉ định cổng khác bằng lệnh:
> ```bash
> streamlit run dashboard/app.py --server.port 8502
> ```

---

## 2. Các Chức Năng Nổi Bật Của Dashboard

Ứng dụng gồm **5 trang phân tích chuyên sâu** với giao diện mang phong cách Premier League hiện đại (Dark purple & neon green):

1. **📊 Trang 1 - Tổng Quan & Lịch Sử EPL (Overview & Trends):**
   - **KPI Cards**: Tổng số trận (7,601), Tổng bàn thắng, Bàn thắng TB/trận, Tỷ lệ chủ nhà thắng, Cú sút TB/trận.
   - **Bộ lọc đa mùa giải**: 20 mùa giải liên tiếp từ 2005 đến 2025.
   - **Biểu đồ xu hướng bàn thắng**: Bar + Line Chart thể hiện mức tăng bàn thắng kỷ lục trong các mùa gần đây.
   - **Donut Chart**: Phân bổ tỷ lệ Thắng - Hòa - Thua của đội nhà.
   - **Lợi thế sân nhà (Home Advantage)**: Phân tích trực quan tác động của khán giả và vùng highlight đặc biệt mùa dịch COVID-19 (2020-21).

2. **🏆 Trang 2 - Hiệu Suất Câu Lạc Bộ & Bảng Xếp Hạng (Club Performance):**
   - **Chế độ xem linh hoạt**: Bảng tổng sắp toàn bộ 20 năm lịch sử HOẶC xem riêng từng mùa giải cụ thể.
   - **Bảng xếp hạng tương tác**: Điểm số, Trận thắng/hòa/thua, Bàn thắng, Bàn thua, Hiệu số, Tỷ lệ chuyển hóa cơ hội.
   - **Top CLB ghi bàn nhiều nhất** và biểu đồ so sánh trực diện nhóm **Big Six**.

3. **👟 Trang 3 - Phân Tích Cầu Thủ & xG (Player Analytics):**
   - Kho dữ liệu hơn **5,800 cầu thủ** qua 11 mùa giải Understat.
   - Bộ lọc chi tiết: Mùa giải, Câu lạc bộ, Vị trí (Forward, Midfielder, Defender, Goalkeeper), Số phút thi đấu tối thiểu.
   - **Interactive Scatter Plot: Bàn Thắng Thực Tế vs Bàn Thắng Kỳ Vọng ($xG$)** kèm đường chuẩn $y=x$ để nhận diện ngay các chân sút vượt kỳ vọng (Overperformers) và phung phí cơ hội (Underperformers).

4. **⚔️ Trang 4 - So Sánh Đối Đầu Cầu Thủ (Head-to-Head Comparison):**
   - Cho phép chọn bất kỳ 2 cầu thủ để đối đầu trực tiếp toàn bộ sự nghiệp (ví dụ: *Harry Kane vs Mohamed Salah*, *Erling Haaland vs Sergio Agüero*).
   - Profile card và Bar Chart so sánh đa chiều: Bàn thắng, Kiến tạo, Hiệu suất Per 90, Độ chính xác sút bóng, $xG, xA$.

5. **🔮 Trang 5 - AI Match Predictor (Mô Phỏng Dự Đoán Trận Đấu):**
   - Chọn Đội Chủ Nhà và Đội Khách bất kỳ tại Premier League.
   - Hệ thống tự động trích xuất phong độ 5 trận gần nhất (Rolling 5-match form) và áp dụng mô hình Machine Learning **Random Forest Classifier** để đưa ra xác suất **Thắng - Hòa - Thua** theo thời gian thực.
