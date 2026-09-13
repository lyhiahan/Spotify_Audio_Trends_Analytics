# TỪ ĐIỂN DỮ LIỆU (DATA DICTIONARY)
**Dự án:** Nghiên cứu và trực quan hóa các đặc trưng âm thanh và dự đoán xu hướng bài hát thịnh hành trên Spotify

---

## 1. Bảng `best-selling-artists.csv`
* **Nguồn:** Wikipedia / RIAA Historical Records (Dữ liệu lịch sử nghệ sĩ bán đĩa chạy nhất).
* **Số dòng:** 121 | **Số cột:** 7

| Tên trường | Kiểu dữ liệu | Ý nghĩa / Diễn giải |
| :--- | :--- | :--- |
| `Artist name` | Text / String | Tên nghệ sĩ hoặc ban nhạc |
| `Country` | Text / String | Quốc gia xuất thân của nghệ sĩ |
| `Active years` | Text / String | Khoảng thời gian hoạt động âm nhạc (Ví dụ: `1960–1970`) |
| `Release year of first charted record` | Integer | Năm phát hành bản ghi đầu tiên lọt bảng xếp hạng |
| `Genre` | Text / String | Dòng nhạc chính (Pop, Rock, R&B, Hip hop,...) |
| `Total certified units` | Text / String | Tổng số lượng đĩa/bản ghi đã được chứng nhận bởi các hiệp hội thu âm |
| `Claimed sales` | Text / String | Doanh số đĩa ước tính / công bố (Ví dụ: `500 million`) |

---

## 2. Bảng `country_codes.csv`
* **Nguồn:** World Bank Open Data (Phân loại quốc gia theo khu vực và thu nhập).
* **Số dòng:** 217 | **Số cột:** 3

| Tên trường | Kiểu dữ liệu | Ý nghĩa / Diễn giải |
| :--- | :--- | :--- |
| `country_code` | String (3 ký tự) | Mã quốc gia theo tiêu chuẩn ISO-alpha-3 (Ví dụ: `USA`, `VNM`, `GBR`,...) |
| `region` | String | Khu vực địa lý (Ví dụ: `East Asia & Pacific`, `Europe & Central Asia`,...) |
| `income_group` | String | Phân loại nhóm thu nhập quốc gia (`High income`, `Upper middle income`, `Lower middle income`, `Low income`) |

---

## 3. Bảng `gdp_data.csv`
* **Nguồn:** World Bank Development Indicators (Dữ liệu chuỗi thời gian GDP thế giới).
* **Số dòng:** 13,365 | **Số cột:** 4

| Tên trường | Kiểu dữ liệu | Ý nghĩa / Diễn giải |
| :--- | :--- | :--- |
| `country_name` | String | Tên quốc gia đầy đủ |
| `country_code` | String (3 ký tự) | Mã ISO-alpha-3 quốc gia (Dùng để JOIN với `country_codes`) |
| `year` | Integer (1960 - 2022) | Năm ghi nhận chỉ số GDP |
| `value` | Float / Numeric | Giá trị tổng sản phẩm quốc nội (GDP) quy đổi theo USD |

---

## 4. Bảng `spotify-tracks-dataset.csv`
* **Nguồn:** Spotify Web API / Kaggle Spotify Tracks Dataset.
* **Số dòng:** ~114,000 | **Số cột:** 22

| Tên trường | Kiểu dữ liệu | Ý nghĩa / Diễn giải |
| :--- | :--- | :--- |
| `track_id` | String (22 ký tự) | Mã định danh duy nhất của bài hát trên Spotify |
| `artists` | String | Danh sách các nghệ sĩ thể hiện bài hát |
| `album_name` | String | Tên album chứa bài hát |
| `track_name` | String | Tên bài hát |
| `popularity` | Integer (0 - 100) | Điểm độ phổ biến toàn cầu của bài hát trên Spotify |
| `duration_ms` | Integer | Thời lượng bài hát (mili-giây) |
| `explicit` | Boolean (0/1) | Bài hát có chứa từ ngữ nhạy cảm/gắn mác 18+ hay không |
| `danceability` | Float (0.0 - 1.0) | Mức độ phù hợp để nhảy múa dựa trên nhịp điệu và độ ổn định |
| `energy` | Float (0.0 - 1.0) | Mức độ sôi động, cường độ cảm giác của bài hát |
| `key` | Integer (0 - 11) | Cao độ nốt nhạc chủ đạo (Pitch class: 0=C, 1=C#, 2=D,...) |
| `loudness` | Float (dB) | Độ to âm lượng tổng thể tính bằng Decibel (thường từ -60 đến 0 dB) |
| `mode` | Binary (0/1) | Giọng điệu của bài hát (1: Major - Trưởng, 0: Minor - Thứ) |
| `speechiness` | Float (0.0 - 1.0) | Tỷ lệ xuất hiện của lời nói / rap trong track |
| `acousticness` | Float (0.0 - 1.0) | Mức độ mộc / sử dụng nhạc cụ acoustic (không điện tử) |
| `instrumentalness` | Float (0.0 - 1.0) | Mức độ không có giọng hát (càng gần 1.0 càng là bài không lời) |
| `liveness` | Float (0.0 - 1.0) | Xác suất bài hát được thu âm trực tiếp (live concert) |
| `valence` | Float (0.0 - 1.0) | Tính tích cực âm nhạc (gần 1: vui tươi, hào hứng; gần 0: buồn bã, u tối) |
| `tempo` | Float (BPM) | Tốc độ nhịp đập bài hát (Beats Per Minute) |
| `time_signature` | Integer | Số chỉ nhịp (ví dụ nhịp 3/4, 4/4) |
| `track_genre` | String | Thể loại âm nhạc của bài hát (acoustic, pop, rock, k-pop, r-n-b,...) |

---

## 5. Bảng `spotify-weekly-charts.csv`
* **Nguồn:** Spotify Weekly Regional & Global Charts (~2021 - 2022).
* **Số dòng:** 314,727 (đã làm sạch & khử trùng lặp bản ghi hợp tác) | **Số cột:** 33 | **Dung lượng:** ~94.2 MB

| Tên trường | Kiểu dữ liệu | Ý nghĩa / Diễn giải |
| :--- | :--- | :--- |
| `uri` | String | Spotify URI (`spotify:track:<track_id>`) |
| `rank` | Integer (1 - 200) | Thứ hạng bài hát trong tuần |
| `artist_names` | String | Chuỗi danh sách tất cả nghệ sĩ tham gia |
| `artist_individual` | String | Tên từng nghệ sĩ riêng biệt (dùng để phân tích cá nhân & join) |
| `track_name` | String | Tên bài hát trên bảng xếp hạng |
| `streams` | Integer / Float | Số lượt phát trực tuyến (streams) bài hát đạt được trong tuần |
| `week` | Date (YYYY-MM-DD) | Tuần ghi nhận xếp hạng |
| `country` | String | Thị trường quốc gia của bảng xếp hạng (ví dụ: `Vietnam`, `United States`) |
| `peak_rank` | Integer | Thứ hạng cao nhất bài hát từng đạt được |
| `previous_rank` | Integer | Thứ hạng của bài hát ở tuần liền trước |
| `weeks_on_chart` | Integer | Số tuần bài hát trụ hạng trên Top Charts |
| `danceability`, `energy`,... | Float | Các đặc trưng âm học tương ứng của track trong tuần |
