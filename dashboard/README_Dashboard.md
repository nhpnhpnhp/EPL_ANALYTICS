# HƯỚNG DẪN KHỞI CHẠY STREAMLIT DASHBOARD (EPL ANALYTICS)

Dự án đã được tích hợp một ứng dụng **Streamlit Interactive Dashboard** trực quan, hiện đại tại [dashboard/app.py](file:///c:/Users/Admin/Desktop/ttdltq/dashboard/app.py).

---

## 1. Cách Khởi Chạy Dashboard

Mở Terminal hoặc PowerShell tại thư mục dự án và chạy lệnh:

```bash
# Kích hoạt môi trường và chạy Streamlit
streamlit run dashboard/app.py
```
Hoặc nếu chạy qua môi trường ảo:
```bash
.venv\Scripts\streamlit.exe run dashboard/app.py
```

Sau khi chạy lệnh, trình duyệt sẽ tự động mở tại địa chỉ:  
👉 **`http://localhost:8501`**

---

## 2. Các Chức Năng Nổi Bật Của Dashboard

Ứng dụng gồm **5 trang phân tích chuyên sâu** với giao diện mang phong cách Premier League hiện đại:

1. **📊 Trang 1 - Tổng Quan & Lịch Sử EPL (Overview & Trends):**
   - KPI Cards: Tổng số trận (7,601), Tổng bàn thắng, Bàn thắng TB/trận, Tỷ lệ chủ nhà thắng, Cú sút TB/trận.
   - Bộ lọc đa mùa giải (20 mùa từ 2005 đến 2025).
   - Biểu đồ kết hợp Bar + Line Chart thể hiện xu hướng gia tăng bàn thắng kỷ lục.
   - Donut Chart phân bố tỷ lệ Thắng/Hòa/Thua.
   - Phân tích lợi thế sân nhà và vùng highlight đặc biệt của mùa dịch COVID-19 (2020-21).

2. **🏆 Trang 2 - Hiệu Suất Câu Lạc Bộ & Bảng Xếp Hạng (Club Performance):**
   - Chế độ xem bảng tổng sắp 20 năm lịch sử HOẶC xem riêng từng mùa giải.
   - Bảng xếp hạng tương tác đầy đủ: Điểm, Thắng, Hòa, Thua, Bàn thắng, Bàn thua, Hiệu số, Tỷ lệ chuyển hóa cơ hội.
   - Top CLB ghi bàn nhiều nhất và so sánh trực diện nhóm "Big Six".

3. **👟 Trang 3 - Phân Tích Cầu Thủ & xG (Player Analytics):**
   - Kho dữ liệu hơn 5,800 cầu thủ qua 11 mùa giải.
   - Bộ lọc: Mùa giải, Câu lạc bộ, Vị trí (Forward, Midfielder, Defender, Goalkeeper), Số phút tối thiểu.
   - **Interactive Scatter Plot: Bàn Thắng Thực Tế vs Bàn Thắng Kỳ Vọng ($xG$)** kèm đường chuẩn để nhận diện ngay ai là sát thủ vượt kỳ vọng (Overperformer) và ai phung phí cơ hội.

4. **⚔️ Trang 4 - So Sánh Đối Đầu Cầu Thủ (Head-to-Head Comparison):**
   - Cho phép chọn bất kỳ 2 cầu thủ để so sánh trực diện toàn bộ sự nghiệp (ví dụ: Harry Kane vs Mohamed Salah, hoặc Erling Haaland vs Sergio Agüero).
   - Profile card và Bar Chart so sánh đa chiều các chỉ số: Goals, Assists, Per 90 metrics, Shot Accuracy, $xG, xA$.

5. **🔮 Trang 5 - AI Match Predictor (Mô Phỏng Dự Đoán Trận Đấu):**
   - Chọn Đội Chủ Nhà và Đội Khách bất kỳ tại Premier League.
   - Hệ thống tự động trích xuất phong độ 5 trận gần nhất và áp dụng mô hình Machine Learning Random Forest để đưa ra **xác suất Thắng - Hòa - Thua** theo thời gian thực.
