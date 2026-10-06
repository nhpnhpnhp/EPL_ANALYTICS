# Nguồn và quy trình lấy dữ liệu raw

## 1. Dữ liệu trận đấu

Nguồn: [Football-Data.co.uk](https://www.football-data.co.uk/data.php).

Script sử dụng mẫu URL:

```text
https://www.football-data.co.uk/mmz4281/{YY}{YY}/E0.csv
```

Trong đó `E0` là mã giải English Premier League. Ví dụ mùa `2024-2025` được tải từ:

```text
https://www.football-data.co.uk/mmz4281/2425/E0.csv
```

Mỗi file được lưu tại `data/raw/matches/` theo quy ước:

```text
EPL_YYYY-YYYY.csv
```

Mặc định script tải từ mùa `1993-1994` đến `2024-2025`. Có thể thay đổi phạm vi bằng `--start-season` và `--end-season`.

## 2. Dữ liệu cầu thủ

Nguồn gốc: [Understat](https://understat.com/).

Understat không cung cấp một file CSV bulk duy nhất. Dữ liệu được lấy theo từng mùa từ trang/API EPL tương ứng. Trang kiểm tra thủ công của mùa `2014/15` là:

```text
https://understat.com/league/EPL/2014
```

Endpoint dữ liệu mà script sử dụng là:

```text
https://understat.com/getLeagueData/EPL/{year}
```

`{year}` là năm bắt đầu của mùa giải. Ví dụ:

| Mùa giải | URL dữ liệu |
| --- | --- |
| 2014/15 | `https://understat.com/getLeagueData/EPL/2014` |
| 2020/21 | `https://understat.com/getLeagueData/EPL/2020` |
| 2024/25 | `https://understat.com/getLeagueData/EPL/2024` |

Script trước tiên mở trang mùa giải để nhận session cookie của Understat, sau đó gọi endpoint JSON với `Referer` và `X-Requested-With`. Script lấy danh sách `players` từ mỗi phản hồi JSON, sau đó gắn thêm:

- `league`: luôn là `EPL`
- `year`: năm bắt đầu mùa
- `season`: dạng `YYYY/YY`
- `scrape_timestamp`: thời điểm tải dữ liệu UTC
- `primary_position`: vị trí chính suy ra từ `position` nếu API chưa trả về

Các chỉ số gốc gồm `games`, `goals`, `assists`, `shots`, `key_passes`, `xG`, `xA`, `npxG`, `xGChain` và `xGBuildup`.

Mặc định script lấy 11 mùa từ `2014-2015` đến `2024-2025`, rồi lưu thành:

```text
data/raw/players/understat_players_2014_2024.csv
```

Lưu ý: file hiện có trong repository được ghi nhận là dữ liệu Understat, với `scrape_timestamp` trong dữ liệu là `2025-09-01`. Script mới tái tạo dữ liệu trực tiếp từ endpoint Understat, nên kết quả có thể thay đổi nếu Understat cập nhật dữ liệu.

## 3. Dữ liệu sân vận động và vị trí địa lý (Stadiums & Geographic Dataset)

**Mục đích:** Đây là **Bảng dữ liệu thứ 3** của đồ án, cung cấp thông tin thực địa, sức chứa và tọa độ địa lý của 46 câu lạc bộ từng tranh tài tại Premier League trong 25 năm thế kỷ 21 (2000 – 2025). Dữ liệu này dùng để thực hiện thao tác **Join/Merge với bảng trận đấu** (qua khóa `HomeTeam = Club`) và trực quan hóa **Bản đồ không gian tương tác (Geographic Map)** trên Dashboard, đáp ứng trực tiếp tiêu chí Barem 1.1 ($\ge 3$ bảng) và Barem 2.3 (ít nhất 1 biểu đồ dạng bản đồ).

### 3.1. Nguồn gốc dữ liệu (Data Provenance)
Dữ liệu được thu thập và tổng hợp chuẩn hóa (Curated & Verified Dataset) từ các nguồn chính thống và dữ liệu mở của bóng đá Anh:
1. **Thông tin CLB & Sân vận động chính thức:** Trích xuất từ hồ sơ câu lạc bộ trên trang chủ Ban tổ chức giải Ngoại hạng Anh: [PremierLeague.com/clubs](https://www.premierleague.com/clubs). Cung cấp tên câu lạc bộ (`Club`), tên sân nhà chính thức (`Stadium`), sức chứa khán đài chuẩn (`Capacity`) và năm thành lập (`Founded`).
2. **Thông tin địa lý & Thành phố:** Tra cứu và chuẩn hóa từ cơ sở dữ liệu sân vận động Vương quốc Anh: [Wikipedia: List of Premier League stadiums](https://en.wikipedia.org/wiki/List_of_Premier_League_stadiums) và [Football Ground Guide](https://footballgroundguide.com/leagues/england/premier-league). Cung cấp thành phố (`City`) và phân vùng hành chính chính thức của Vương quốc Anh (`Region`: *Greater London, North West, West Midlands, Yorkshire, North East, East Midlands, South East, South West, East of England, Wales*).
3. **Tọa độ địa lý GPS (WGS84):** Lấy theo hệ tọa độ chuẩn vĩ độ và kinh độ (`Latitude`, `Longitude`) từ OpenStreetMap / Ordnance Survey UK cho từng sân bóng (ví dụ: Old Trafford: `53.4631, -2.2913`, Emirates: `51.5549, -0.1084`, Anfield: `53.4308, -2.9608`...).

### 3.2. Quy trình tổng hợp và chuẩn hóa (Compilation Pipeline)
1. **Trích xuất danh sách CLB:** Quét danh sách duy nhất các đội bóng xuất hiện ở cột `HomeTeam` trong 9,410 trận đấu lịch sử của `matches_clean.csv` để thu được tập hợp 46 câu lạc bộ duy nhất thế kỷ 21.
2. **Đồng bộ khóa kết nối:** Chuẩn hóa tên CLB trùng khớp 100% với tên gọi trong bảng thi đấu (ví dụ: `Manchester City`, `Tottenham`, `Wolverhampton`, `Nott'm Forest`).
3. **Kiểm định tọa độ (Geocoding Validation):** Toàn bộ tọa độ được kiểm tra định vị chuẩn xác trên lãnh thổ Vương quốc Anh (Vĩ độ: 50°N – 56°N, Kinh độ: -5°W đến +2°E).
4. **Lưu trữ chuẩn:** Xuất ra file dữ liệu sạch tại:
   ```text
   data/processed/stadiums_clean.csv
   ```

## 4. Cách chạy

Chạy từ thư mục gốc `EPL ANALYTICS`:

```powershell
.\.venv\Scripts\python.exe scripts\download_raw_data.py
```

Chỉ tải một mùa trận đấu và một mùa cầu thủ để kiểm tra:

```powershell
.\.venv\Scripts\python.exe scripts\download_raw_data.py `
  --start-season 2024-2025 `
  --end-season 2024-2025 `
  --players-start-season 2024-2025 `
  --players-end-season 2024-2025
```

Tải lại và ghi đè toàn bộ file:

```powershell
.\.venv\Scripts\python.exe scripts\download_raw_data.py --force
```

Xem đầy đủ tham số:

```powershell
.\.venv\Scripts\python.exe scripts\download_raw_data.py --help
```

## 5. Cơ chế an toàn

- Tự retry các lỗi HTTP tạm thời như `429`, `500`, `502`, `503`, `504`.
- Dùng User-Agent nhận diện rõ project.
- Bỏ qua file đã tồn tại nếu không có `--force`.
- Ghi file qua file tạm rồi đổi tên, tránh để lại CSV bị thiếu khi mạng ngắt.
- Không lưu API key hoặc thông tin đăng nhập.
