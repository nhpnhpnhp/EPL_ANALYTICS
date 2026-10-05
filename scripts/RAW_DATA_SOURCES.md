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

## 3. Cách chạy

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

## 4. Cơ chế an toàn

- Tự retry các lỗi HTTP tạm thời như `429`, `500`, `502`, `503`, `504`.
- Dùng User-Agent nhận diện rõ project.
- Bỏ qua file đã tồn tại nếu không có `--force`.
- Ghi file qua file tạm rồi đổi tên, tránh để lại CSV bị thiếu khi mạng ngắt.
- Không lưu API key hoặc thông tin đăng nhập.
