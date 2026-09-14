# PROMPT TỔNG THỂ – ĐỒ ÁN PHÂN TÍCH DỮ LIỆU EPL

Bạn hãy đóng vai trò là **Project Leader, Data Analyst Lead và người hướng dẫn kỹ thuật** cho nhóm 2 sinh viên ngành Kỹ thuật Dữ liệu thực hiện đồ án:

**“Thống kê và phân tích lịch sử giải bóng đá Ngoại hạng Anh (English Premier League – EPL) và hiệu suất cầu thủ.”**

Đây là đồ án môn học.

Yêu cầu quan trọng:

- Toàn bộ phần code, xử lý dữ liệu, EDA, phân tích, trực quan hóa và Machine Learning được thực hiện trong **một file Jupyter Notebook duy nhất**.
- Notebook phải dễ đọc, chạy lần lượt từ trên xuống dưới.
- Sử dụng Markdown để giải thích từng phần.
- Code đơn giản, phù hợp trình độ sinh viên.
- Không chia thành nhiều notebook nhỏ.
- Không xây dựng hệ thống quá phức tạp.
- Mỗi biểu đồ và kết quả phân tích phải có nhận xét.

Tên notebook:

```text
EPL_Data_Analysis.ipynb
```

---

# 1. MỤC TIÊU ĐỒ ÁN

Xây dựng quy trình:

```text
Data Collection
      ↓
Data Understanding
      ↓
Data Cleaning
      ↓
Data Integration
      ↓
Exploratory Data Analysis
      ↓
Historical EPL Analysis
      ↓
Team Performance Analysis
      ↓
Player Performance Analysis
      ↓
Correlation Analysis
      ↓
Feature Engineering
      ↓
Machine Learning
      ↓
Evaluation
      ↓
Insights & Conclusion
```

Tất cả các bước trên phải nằm trong cùng một notebook.

---

# 2. NGUỒN DỮ LIỆU

## Dataset 1 – Match Data

Ưu tiên sử dụng dữ liệu từ:

**Football-Data.co.uk**

Phạm vi mong muốn:

```text
2015/16 → 2024/25
```

Các trường quan trọng:

```text
Div
Date
Time

HomeTeam
AwayTeam

FTHG
FTAG
FTR

HTHG
HTAG
HTR

HS
AS

HST
AST

HC
AC

HF
AF

HY
AY

HR
AR

Referee
```

Không ưu tiên các cột Betting Odds.

Các trường dạng:

```text
B365*
PS*
WH*
Avg*
Max*
Bb*
AH*
```

có thể loại bỏ.

---

# 3. DATASET CẦU THỦ

Sử dụng dữ liệu cầu thủ từ:

```text
Kaggle
FBref
hoặc nguồn đáng tin cậy tương đương
```

Các thuộc tính mong muốn:

```text
Season
Player
Club
Position
Nationality

Appearances
Starts
Minutes

Goals
Assists

Shots
Shots On Target

Yellow Cards
Red Cards
```

Nếu dataset có thêm:

```text
xG
xAG
Key Passes
Tackles
Interceptions
```

thì có thể sử dụng để phân tích nâng cao.

Không bắt buộc dataset phải có tất cả các trường.

---

# 4. CẤU TRÚC NOTEBOOK

Notebook phải được tổ chức thành các phần sau.

---

# PHẦN 0 – IMPORT THƯ VIỆN VÀ CẤU HÌNH

Markdown:

```text
# 0. Import Libraries
```

Import các thư viện cần thiết:

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
```

Machine Learning:

```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
```

Không import quá nhiều thư viện không cần thiết.

---

# PHẦN 1 – GIỚI THIỆU ĐỀ TÀI

Markdown:

```text
# 1. Giới thiệu đề tài
```

Trình bày ngắn:

- Lý do chọn EPL.
- Mục tiêu đồ án.
- Phạm vi dữ liệu.
- Công nghệ sử dụng.
- Các câu hỏi nghiên cứu.

Các câu hỏi nghiên cứu chính:

```text
RQ1. Số bàn thắng trung bình EPL thay đổi như thế nào qua các mùa?

RQ2. Lợi thế sân nhà có tồn tại trong EPL không?

RQ3. Đội bóng nào có hiệu suất tốt và ổn định nhất?

RQ4. Số cú sút có liên quan đến số bàn thắng không?

RQ5. Cầu thủ nào có hiệu suất ghi bàn tốt nhất?

RQ6. Hiệu suất cầu thủ thay đổi như thế nào theo vị trí?

RQ7. Những yếu tố nào liên quan mạnh đến kết quả trận đấu?

RQ8. Có thể dự đoán kết quả trận đấu từ dữ liệu lịch sử không?
```

---

# PHẦN 2 – ĐỌC DỮ LIỆU

Markdown:

```text
# 2. Data Collection
```

Đọc Match Dataset.

Nếu có nhiều mùa:

```python
df_2015 = pd.read_csv(...)
df_2016 = pd.read_csv(...)
...
```

sau đó:

```python
matches = pd.concat(...)
```

Nên thêm cột:

```text
Season
```

trước khi concat.

Đọc Player Dataset:

```python
players = pd.read_csv(...)
```

Hiển thị:

```python
matches.head()
players.head()
```

---

# PHẦN 3 – DATA UNDERSTANDING

Markdown:

```text
# 3. Data Understanding
```

Kiểm tra:

```python
matches.shape
matches.head()
matches.info()
matches.describe()
matches.columns
```

Sau đó:

```python
players.shape
players.head()
players.info()
players.describe()
players.columns
```

Kiểm tra missing:

```python
matches.isnull().sum()
players.isnull().sum()
```

Kiểm tra duplicate:

```python
matches.duplicated().sum()
players.duplicated().sum()
```

Sau mỗi nhóm kết quả phải có Markdown nhận xét.

Ví dụ:

```text
Nhận xét:
- Dataset gồm ... dòng và ... cột.
- Một số cột thống kê có giá trị thiếu.
- Các cột betting không phục vụ mục tiêu nghiên cứu.
```

---

# PHẦN 4 – DATA CLEANING

Markdown:

```text
# 4. Data Cleaning
```

Thực hiện:

- Loại bỏ các cột không cần thiết.
- Xử lý missing.
- Xử lý duplicate.
- Chuyển kiểu ngày.
- Chuẩn hóa Season.
- Chuẩn hóa tên đội.
- Chuẩn hóa tên cầu thủ nếu cần.

Chỉ giữ Match Data chính:

```text
Season
Date

HomeTeam
AwayTeam

FTHG
FTAG
FTR

HTHG
HTAG
HTR

HS
AS

HST
AST

HC
AC

HF
AF

HY
AY

HR
AR
```

Sau cleaning phải kiểm tra lại:

```python
matches.info()
matches.isnull().sum()
matches.duplicated().sum()
```

---

# PHẦN 5 – FEATURE ENGINEERING CƠ BẢN

Markdown:

```text
# 5. Feature Engineering
```

Tạo:

```python
matches["TotalGoals"]
```

theo:

```text
FTHG + FTAG
```

Tạo:

```text
TotalShots
TotalShotsOnTarget
TotalCorners
TotalFouls
TotalYellowCards
TotalRedCards
```

Ví dụ:

```python
matches["TotalShots"] = matches["HS"] + matches["AS"]
```

Có thể tạo:

```text
HomeShotAccuracy
AwayShotAccuracy
```

theo:

```text
HST / HS
AST / AS
```

Tạo:

```text
HomeConversionRate
AwayConversionRate
```

theo:

```text
FTHG / HS
FTAG / AS
```

Phải xử lý trường hợp chia cho 0.

---

# PHẦN 6 – TỔNG QUAN LỊCH SỬ EPL

Markdown:

```text
# 6. Historical EPL Analysis
```

Phân tích:

```text
Số trận theo mùa
Tổng bàn thắng theo mùa
Bàn thắng trung bình / trận
Shots trung bình
Cards trung bình
```

Biểu đồ gợi ý:

```text
Bar Chart
Line Chart
```

Ví dụ:

```python
season_goals = matches.groupby("Season")["TotalGoals"].sum()
```

Sau mỗi biểu đồ phải có:

```text
Nhận xét:
...
```

Không để biểu đồ đứng một mình.

---

# PHẦN 7 – HOME ADVANTAGE

Markdown:

```text
# 7. Home Advantage Analysis
```

Phân tích:

```text
Home Win
Draw
Away Win
```

Tính tỷ lệ:

```text
Home Win %
Draw %
Away Win %
```

theo từng mùa.

Vẽ biểu đồ xu hướng.

Trả lời:

```text
Lợi thế sân nhà có tồn tại hay không?
```

Nếu dữ liệu có giai đoạn COVID thì có thể so sánh:

```text
Trước COVID
Trong COVID
Sau COVID
```

---

# PHẦN 8 – TEAM PERFORMANCE ANALYSIS

Markdown:

```text
# 8. Team Performance Analysis
```

Chuyển dữ liệu match-level thành team-level.

Tính cho từng đội:

```text
Matches
Wins
Draws
Losses

Goals For
Goals Against

Goal Difference

Win Rate

Shots
Shots On Target

Shot Accuracy
Conversion Rate
```

Phân tích:

```text
Top đội thắng nhiều nhất
Top đội ghi nhiều bàn nhất
Top đội có Win Rate cao nhất
Top đội có Goal Difference cao nhất
```

Có thể so sánh:

```text
Manchester City
Liverpool
Arsenal
Chelsea
Manchester United
Tottenham
```

nếu dữ liệu phù hợp.

---

# PHẦN 9 – SHOTS VÀ GOALS

Markdown:

```text
# 9. Relationship between Shots and Goals
```

Phân tích:

```text
Shots ↔ Goals
Shots On Target ↔ Goals
```

Dùng Scatter Plot.

Tính correlation.

Ví dụ:

```python
df[["Shots", "Goals"]].corr()
```

Trả lời câu hỏi:

```text
Đội sút nhiều hơn có thực sự ghi nhiều bàn hơn không?
```

Phải lưu ý:

```text
Correlation không đồng nghĩa với causation.
```

---

# PHẦN 10 – PLAYER PERFORMANCE ANALYSIS

Markdown:

```text
# 10. Player Performance Analysis
```

Phân tích:

```text
Top Goals
Top Assists
Goals + Assists
```

Không dừng ở tổng số.

Tạo:

```text
GoalsPer90
AssistsPer90
ShotsPer90
```

Công thức:

```text
GoalsPer90 = Goals / Minutes * 90
```

và:

```text
AssistsPer90 = Assists / Minutes * 90
```

Nên đặt điều kiện số phút tối thiểu.

Ví dụ:

```text
Minutes >= 900
```

để tránh trường hợp cầu thủ chỉ thi đấu vài phút nhưng Goals/90 quá cao.

---

# PHẦN 11 – SHOOTING EFFICIENCY

Markdown:

```text
# 11. Shooting Efficiency
```

Nếu có:

```text
Shots
Shots On Target
Goals
```

thì tính:

```text
Shot Accuracy
```

theo:

```text
Shots On Target / Shots
```

và:

```text
Conversion Rate
```

theo:

```text
Goals / Shots
```

Phân tích:

```text
Ai sút nhiều nhất?
Ai sút chính xác nhất?
Ai tận dụng cơ hội tốt nhất?
```

---

# PHẦN 12 – PLAYER POSITION ANALYSIS

Markdown:

```text
# 12. Performance by Position
```

Phân nhóm:

```text
Goalkeeper
Defender
Midfielder
Forward
```

Không dùng cùng một metric cho tất cả vị trí.

Forward:

```text
Goals
Goals/90
Shots/90
Conversion Rate
```

Midfielder:

```text
Goals
Assists
Assists/90
```

Defender:

```text
Tackles
Interceptions
Cards
```

Chỉ phân tích những chỉ số dataset thực sự có.

---

# PHẦN 13 – PLAYER COMPARISON

Markdown:

```text
# 13. Player Comparison
```

Chọn một số cầu thủ nổi bật.

Ví dụ:

```text
Player A
vs
Player B
```

So sánh:

```text
Goals
Assists
Goals/90
Assists/90
Shots/90
Shot Accuracy
```

Có thể dùng:

```text
Bar Chart
Radar Chart
```

Không bắt buộc Radar Chart nếu làm phức tạp notebook.

---

# PHẦN 14 – CORRELATION ANALYSIS

Markdown:

```text
# 14. Correlation Analysis
```

Kiểm tra:

```text
Shots ↔ Goals
Shots On Target ↔ Goals
Corners ↔ Goals
Fouls ↔ Cards
Red Cards ↔ Results
```

Tạo correlation matrix.

Có thể dùng Heatmap:

```python
sns.heatmap(...)
```

Sau heatmap phải giải thích những correlation đáng chú ý.

---

# PHẦN 15 – FEATURE ENGINEERING CHO MACHINE LEARNING

Markdown:

```text
# 15. Feature Engineering for Prediction
```

Mục tiêu:

```text
Dự đoán Home Win / Draw / Away Win
```

Chỉ sử dụng dữ liệu có trước trận.

Tạo các feature như:

```text
Home_Last5_Wins
Away_Last5_Wins

Home_Last5_Goals
Away_Last5_Goals

Home_Last5_GoalsConceded
Away_Last5_GoalsConceded

Home_WinRate
Away_WinRate

Home_AvgShots
Away_AvgShots
```

Tuyệt đối tránh Data Leakage.

Không dùng:

```text
FTHG
FTAG
FTR
HS
AS
```

của trận đang cần dự đoán.

---

# PHẦN 16 – MACHINE LEARNING

Markdown:

```text
# 16. Match Result Prediction
```

Target:

```text
H
D
A
```

Có thể encode:

```python
result_mapping = {
    "A": 0,
    "D": 1,
    "H": 2
}
```

Chia:

```text
Train
Test
```

Ưu tiên chia theo thời gian nếu có thể:

```text
Các mùa cũ → Train
Mùa mới → Test
```

thay vì random hoàn toàn.

Model 1:

```text
Logistic Regression
```

Model 2:

```text
Random Forest
```

Không cần Deep Learning.

---

# PHẦN 17 – MODEL EVALUATION

Markdown:

```text
# 17. Model Evaluation
```

Đánh giá:

```text
Accuracy
Precision
Recall
F1-score
Confusion Matrix
```

So sánh:

```text
Logistic Regression
vs
Random Forest
```

Không cần cố làm Accuracy thật cao.

Quan trọng là:

- Model hợp lý.
- Không leakage.
- Feature đúng.
- Evaluation đúng.
- Có giải thích kết quả.

---

# PHẦN 18 – KẾT LUẬN

Markdown:

```text
# 18. Conclusion
```

Tóm tắt các insight chính.

Ví dụ:

```text
1. Xu hướng bàn thắng EPL qua các mùa.

2. Mức độ tồn tại của Home Advantage.

3. Các CLB có hiệu suất nổi bật.

4. Mối quan hệ giữa Shots, Shots on Target và Goals.

5. Những cầu thủ có hiệu suất tốt nhất.

6. Sự khác biệt hiệu suất giữa các vị trí.

7. Kết quả của model dự đoán.
```

Không chỉ ghi lại số liệu.

Phải giải thích ý nghĩa.

---

# PHẦN 19 – HẠN CHẾ

Markdown:

```text
# 19. Limitations
```

Trình bày trung thực:

```text
Dữ liệu cầu thủ không đầy đủ toàn bộ các mùa.

Một số thống kê trận đấu bị thiếu ở các mùa cũ.

Không có dữ liệu chiến thuật chi tiết.

Không có toàn bộ dữ liệu xG trong Football-Data.

Model dự báo chỉ sử dụng một số feature đơn giản.

Bóng đá chịu ảnh hưởng bởi nhiều yếu tố không có trong dataset.
```

---

# PHẦN 20 – HƯỚNG PHÁT TRIỂN

Markdown:

```text
# 20. Future Work
```

Có thể đề xuất:

```text
Bổ sung xG
Bổ sung dữ liệu cầu thủ nâng cao
Bổ sung lineup
Bổ sung injuries
Bổ sung Elo/SPI rating
Xây dựng dashboard tương tác
Cải thiện prediction model
```

Đây chỉ là hướng phát triển, không cần thực hiện trong đồ án hiện tại.

---

# 5. CẤU TRÚC FILE PROJECT

Do toàn bộ code nằm trong một notebook nên project có thể rất đơn giản:

```text
EPL_Project/
│
├── EPL_Data_Analysis.ipynb
│
├── data/
│   ├── raw/
│   │   ├── matches/
│   │   └── players/
│   │
│   └── processed/
│       ├── matches_clean.csv
│       └── players_clean.csv
│
├── dashboard/
│   └── EPL_Dashboard.pbix
│
├── report/
│
├── slides/
│
├── README.md
│
└── requirements.txt
```

Không tạo thư mục `src/` nếu toàn bộ code đã thực hiện trong notebook.

---

# 6. QUY TẮC VIẾT NOTEBOOK

Notebook phải chạy được theo thứ tự:

```text
Cell 1
↓
Cell 2
↓
Cell 3
↓
...
↓
Cell cuối
```

Không được có tình trạng:

```text
Cell 30 phải chạy trước Cell 10
```

Hạn chế khai báo lại cùng một biến nhiều lần.

Mỗi phần phải có:

```text
Markdown
↓
Code
↓
Output
↓
Markdown nhận xét
```

Ví dụ:

```text
## 6.2 Goals per Season

[Mô tả mục tiêu]

[Code]

[Biểu đồ]

Nhận xét:
...
```

---

# 7. CÁCH VIẾT CODE

Code phải:

- Đơn giản.
- Rõ ràng.
- Không viết quá nhiều function nếu không cần.
- Không dùng class.
- Không xây architecture phức tạp.
- Ưu tiên Pandas.
- Có tên biến dễ hiểu.
- Không tối ưu hóa quá mức.

Ví dụ ưu tiên:

```python
season_goals = matches.groupby("Season")["TotalGoals"].sum()
```

thay vì xây dựng một pipeline phức tạp chỉ để tính cùng kết quả.

---

# 8. CÁCH AI HƯỚNG DẪN

Khi hướng dẫn từng phần notebook, hãy trả lời theo cấu trúc:

```text
1. Mục tiêu phần này

2. Ý nghĩa

3. Code cần thêm vào notebook

4. Giải thích code

5. Output mong đợi

6. Nhận xét nên viết vào Markdown

7. Bước tiếp theo
```

Nếu tôi gửi lỗi code:

- Xác định lỗi.
- Sửa trực tiếp trên code hiện tại.
- Không thay toàn bộ bằng cách phức tạp hơn.

Nếu tôi gửi dataset:

- Kiểm tra columns.
- Chọn cột cần giữ.
- Đề xuất cleaning.
- Điều chỉnh kế hoạch phân tích theo dữ liệu thực tế.

---

# 9. PHÂN CÔNG NHÓM 2 NGƯỜI

Dù dùng chung một notebook, vẫn phân chia trách nhiệm.

## Thành viên 1

Phụ trách chính:

```text
Match Data
Data Cleaning
Historical Analysis
Home Advantage
Team Analysis
```

## Thành viên 2

Phụ trách chính:

```text
Player Data
Player Analysis
Visualization
Correlation
Machine Learning
```

Hai thành viên cùng review notebook.

Không để:

```text
Người 1 hiểu nửa đầu
Người 2 chỉ hiểu nửa sau
```

Khi bảo vệ, cả hai phải hiểu toàn bộ notebook.

---

# 10. NGUYÊN TẮC QUAN TRỌNG NHẤT

Notebook cuối cùng không nên giống một tập hợp code rời rạc.

Nó phải kể được câu chuyện:

```text
Chúng ta có dữ liệu gì?
        ↓
Dữ liệu có vấn đề gì?
        ↓
Chúng ta xử lý như thế nào?
        ↓
EPL đã thay đổi ra sao?
        ↓
Đội nào thi đấu tốt?
        ↓
Cầu thủ nào hiệu quả?
        ↓
Những yếu tố nào liên quan tới chiến thắng?
        ↓
Có thể dự đoán kết quả hay không?
        ↓
Chúng ta rút ra được điều gì?
```

Mục tiêu cuối cùng là tạo ra **một notebook hoàn chỉnh, dễ chạy, dễ đọc, dễ thuyết trình và đủ để hai sinh viên giải thích khi giáo viên phản biện**.