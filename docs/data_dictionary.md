# 📚 TỪ ĐIỂN DỮ LIỆU TOÀN DIỆN (DATA DICTIONARY)
**Dự án:** Nghiên cứu & Trực quan hóa Đặc trưng Âm thanh và Dự đoán Xu hướng Bài hát Thịnh hành trên Spotify  
**Môn học:** Tương tác Dữ liệu (Interactive Data Visualization / Visual Analytics)  
**Tác giả:** Đinh Quốc Anh (MSSV: 24133003 — Data Engineer & Data Analyst)  
**Phiên bản:** 3.4 (Master Dataset 38 Cột — sửa macro_genre, bỏ 3 cột yếu, thêm chart_longevity & tempo_category, ML Dataset 19 Cột)  

---

## MỤC LỤC
1. [TỔNG QUAN NGUỒN DỮ LIỆU (5 BẢNG THÔ BAN ĐẦU)](#1-tổng-quan-nguồn-dữ-liệu-5-bảng-thô-ban-đầu)
   * [1.1. Bảng `best-selling-artists.csv`](#11-bảng-best-selling-artistscsv)
   * [1.2. Bảng `country_codes.csv`](#12-bảng-country_codescsv)
   * [1.3. Bảng `gdp_data.csv`](#13-bảng-gdp_datacsv)
   * [1.4. Bảng `spotify-tracks-dataset.csv`](#14-bảng-spotify-tracks-datasetcsv)
   * [1.5. Bảng `spotify-weekly-charts.csv`](#15-bảng-spotify-weekly-chartscsv)
2. [CÁC TỆP DỮ LIỆU ĐẦU RA SAU XỬ LÝ (OUTPUT DATASETS)](#2-các-tệp-dữ-liệu-đầu-ra-sau-xử-lý-output-datasets)
   * [2.1. File Master: `merged_spotify_data.csv` (39 Cột Phục vụ Insight)](#21-file-master-merged_spotify_datacsv-39-cột-phục-vụ-insight)
   * [2.2. File Dữ liệu ML: `tracks_ml_data.csv` (17 Cột Cấp độ Bài hát cho ML)](#22-file-dữ-liệu-ml-tracks_ml_datacsv-17-cột-cấp-độ-bài-hát-cho-ml)
3. [KHẢO SÁT CHẤT LƯỢNG DỮ LIỆU, DỊ BIỆT & CẢNH BÁO RÒ RỈ](#3-khảo-sát-chất-lượng-dữ-liệu-dị-biệt--cảnh-báo-rò-rỉ)
   * [3.1. Tính bất ổn định và gán nhãn của các trường dữ liệu](#31-tính-bất-ổn-định-và-gán-nhãn-của-các-trường-dữ-liệu)
   * [3.2. Thống kê các giá trị dị biệt (Outliers)](#32-thống-kê-các-giá-trị-dị-biệt-outliers)
   * [3.3. Cảnh báo rò rỉ dữ liệu (Data Leakage) khi huấn luyện mô hình](#33-cảnh-báo-rò-rỉ-dữ-liệu-data-leakage-khi-huấn-luyện-mô-hình)
4. [TỔNG HỢP 10 CALCULATED FIELDS & CÔNG THỨC TOÁN HỌC](#4-tổng-hợp-10-calculated-fields--công-thức-toán-học)
5. [HƯỚNG DẪN TRUY XUẤT DỮ LIỆU THÔNG QUA PYTHON API](#5-hướng-dẫn-truy-xuất-dữ-liệu-thông-qua-python-api)

---

## 1. TỔNG QUAN NGUỒN DỮ LIỆU (5 BẢNG THÔ BAN ĐẦU)

Hệ thống tích hợp dữ liệu từ 5 nguồn độc lập với tổng quy mô **hơn 1.9 triệu bản ghi thô**:

### 1.1. Bảng `best-selling-artists.csv`
* **Nguồn dữ liệu:** Wikipedia / RIAA Historical Records.
* **Quy mô:** 121 dòng × 7 cột | **Dung lượng:** ~16 KB
* **Mục đích:** Bổ sung danh sách nghệ sĩ huyền thoại/di sản (Legacy Artists) có doanh số bán đĩa được chứng nhận cao nhất lịch sử.

| Tên trường | Kiểu dữ liệu | Ý nghĩa / Diễn giải | Ví dụ mẫu |
| :--- | :--- | :--- | :--- |
| `Artist name` | Text / String | Tên nghệ sĩ hoặc ban nhạc | `The Beatles`, `Michael Jackson` |
| `Country` | Text / String | Quốc gia xuất thân của nghệ sĩ | `United Kingdom`, `United States` |
| `Active years` | Text / String | Khoảng thời gian hoạt động âm nhạc chính | `1960–1970` |
| `Release year of first charted record` | Integer | Năm phát hành bản ghi đầu tiên lọt bảng xếp hạng | `1962` |
| `Genre` | Text / String | Dòng nhạc chính của nghệ sĩ | `Rock / Pop` |
| `Total certified units` | Text / String | Doanh số đĩa chứng nhận chính thức | `292.1 million` |
| `Claimed sales` | Text / String | Doanh số đĩa ước tính / công bố toàn cầu | `600 million` |

---

### 1.2. Bảng `country_codes.csv`
* **Nguồn dữ liệu:** World Bank Open Data (Bảng phân loại quốc gia theo khu vực và thu nhập).
* **Quy mô:** 217 dòng × 3 cột | **Dung lượng:** ~8 KB
* **Mục đích:** Ánh xạ mã quốc gia ISO-3 sang khu vực địa lý và phân tầng nhóm thu nhập quốc gia.
* **Lưu ý quan trọng về nhóm thu nhập:** Trong tập dữ liệu Spotify (73 quốc gia), **chỉ tồn tại 3 nhóm thu nhập:** `High income`, `Upper middle income`, và `Lower middle income`. **Hoàn toàn không có quốc gia nào thuộc nhóm "Low income"** lọt vào danh sách có bảng xếp hạng Spotify.

| Tên trường | Kiểu dữ liệu | Ý nghĩa / Diễn giải | Giá trị hợp lệ / Ví dụ |
| :--- | :--- | :--- | :--- |
| `country_code` | String (3 ký tự) | Mã định danh quốc gia chuẩn ISO-alpha-3 | `USA`, `VNM`, `GBR`, `BRA` |
| `region` | String | Khu vực địa lý theo phân loại World Bank | `East Asia & Pacific`, `Europe & Central Asia`, `Latin America & Caribbean`,... |
| `income_group` | String | Phân tầng nhóm thu nhập quốc gia | `High income`, `Upper middle income`, `Lower middle income` (không có Low income) |

---

### 1.3. Bảng `gdp_data.csv`
* **Nguồn dữ liệu:** World Bank Development Indicators (Chuỗi thời gian chỉ số kinh tế thế giới).
* **Quy mô:** 13,365 dòng × 4 cột | **Dung lượng:** ~395 KB
* **Mục đích:** Cung cấp tổng sản phẩm quốc nội (GDP quy đổi USD) theo từng quốc gia qua từng năm (1960 – 2022).

| Tên trường | Kiểu dữ liệu | Ý nghĩa / Diễn giải | Ví dụ mẫu |
| :--- | :--- | :--- | :--- |
| `country_name` | String | Tên quốc gia chuẩn hóa bằng tiếng Anh | `Vietnam`, `United States`, `Brazil` |
| `country_code` | String (3 ký tự) | Mã ISO-alpha-3 của quốc gia | `VNM`, `USA`, `BRA` |
| `year` | Integer | Năm ghi nhận giá trị GDP (1960 – 2022) | `2021`, `2022` |
| `value` | Float / Numeric | Tổng sản phẩm quốc nội tính bằng USD hiện hành | `366137591461.0` (~366 tỷ USD) |

---

### 1.4. Bảng `spotify-tracks-dataset.csv`
* **Nguồn dữ liệu:** Spotify Web API (Trích xuất từ Kaggle Spotify Audio Dataset).
* **Quy mô:** ~114,000 dòng × 22 cột | **Dung lượng:** ~19.8 MB
* **Mục đích:** Bổ sung thể loại nhạc gốc (`track_genre`) và điểm phổ biến tích lũy toàn cầu (`popularity`) cho các bài hát.

| Tên trường | Kiểu dữ liệu | Ý nghĩa / Diễn giải | Miền giá trị / Đơn vị |
| :--- | :--- | :--- | :--- |
| `track_id` | String (22 ký tự) | Khóa định danh duy nhất bài hát trên Spotify | `4cOdK2wGLETKBW3PvgPWqT` |
| `artists` | String | Danh sách nghệ sĩ biểu diễn | `Taylor Swift` |
| `album_name` | String | Tên album chứa bài hát | `Midnights` |
| `track_name` | String | Tên bài hát | `Anti-Hero` |
| `popularity` | Integer | Điểm độ phổ biến toàn cầu của Spotify | `[0, 100]` |
| `duration_ms` | Integer | Thời lượng bài hát tính bằng mili-giây | Mili-giây ($> 0$) |
| `explicit` | Boolean | Cờ cảnh báo nội dung nhạy cảm | `True` / `False` |
| `danceability` | Float | Mức độ bắt nhịp, phù hợp để khiêu vũ | `[0.0, 1.0]` |
| `energy` | Float | Cường độ năng lượng, độ sôi động | `[0.0, 1.0]` |
| `key` | Integer | Cao độ nốt nhạc chủ đạo (Pitch class) | `0 = C, 1 = C#, ..., 11 = B` |
| `loudness` | Float | Độ lớn âm thanh trung bình | Decibel (`dB`), thường `[-60, 5]` |
| `mode` | Binary | Điệu thức bài hát (1: Major - Trưởng, 0: Minor - Thứ) | `0` hoặc `1` |
| `speechiness` | Float | Tỷ lệ lời nói/đọc rap xuất hiện trong bản nhạc | `[0.0, 1.0]` |
| `acousticness` | Float | Mức độ mộc, dùng nhạc cụ acoustic không điện tử | `[0.0, 1.0]` |
| `instrumentalness` | Float | Tỷ lệ không có lời hát (nhạc không lời) | `[0.0, 1.0]` |
| `liveness` | Float | Xác suất bản thu âm diễn ra trực tiếp (Live) | `[0.0, 1.0]` |
| `valence` | Float | Mức độ tích cực, vui tươi của giai điệu | `[0.0, 1.0]` (0: buồn, 1: vui) |
| `tempo` | Float | Tốc độ nhịp đập bài hát | Nhịp/phút (`BPM`) |
| `time_signature` | Integer | Số chỉ nhịp (ví dụ nhịp 3/4, 4/4) | Thường từ `3` đến `7` |
| `track_genre` | String | Thể loại phân loại chi tiết của Spotify | `pop`, `acoustic`, `k-pop`, `latin`,... |

---

### 1.5. Bảng `spotify-weekly-charts.csv`
* **Nguồn dữ liệu:** Bảng xếp hạng tuần khu vực và toàn cầu của Spotify (Top 200 Weekly Charts).
* **Quy mô ban đầu:** 1,787,999 dòng × 36 cột | **Dung lượng:** ~796.6 MB
* **Mục đích:** Xương sống chuỗi thời gian, ghi nhận thứ hạng, số lượt streams, tên bài hát, nghệ sĩ tại **73 quốc gia và bảng Global** (tổng 74 thực thể không gian) từ 2016 đến 2022.
* **Xử lý làm sạch:**
  - Trích xuất `track_id` từ URI (`spotify:track:<id>`).
  - Ép kiểu `week` sang chuẩn `datetime`, tách `year`, `month`.
  - Lọc bỏ triệt để các bản ghi có `streams <= 0` hoặc `week` bị rỗng.
  - Khử trùng lặp bộ ba định danh `(track_id, week, country)`.
  - Loại bỏ sớm 15 cột phụ không mang giá trị cho insight (`Unnamed: 0`, `uri`, `artist_names`, `artists_num`, `artist_id`, `key`, `mode`, `source`, `album_num_tracks`, `collab`, `release_date`, `previous_rank`, `artist_img`, `album_cover`, `pivot`, `region`).

---

## 2. CÁC TỆP DỮ LIỆU ĐẦU RA SAU XỬ LÝ (OUTPUT DATASETS)

Hệ thống ETL hợp nhất dữ liệu vào thư mục `data/processed/` gồm 2 tệp dữ liệu chính:

```text
data/
└── processed/
    ├── merged_spotify_data.csv # 1,078,125 dòng × 38 cột (~300 MB) — Master Dataset chuẩn hóa
    └── tracks_ml_data.csv     # 36,699 bài hát × 19 cột (~5.5 MB) — Dữ liệu Song-level cho ML
```

---

### 2.1. File Master: `merged_spotify_data.csv` (38 Cột Phục vụ Insight)
* **Quy mô:** 1,078,125 dòng × 38 cột | **Dung lượng:** ~300 MB
* **Đặc điểm kiến trúc:**
  - Hợp nhất toàn bộ dữ liệu **73 quốc gia và 1 bảng Global** giai đoạn 2020 – 2022.
  - Chuẩn hóa tên 7 quốc gia World Bank (`Korea`, `Turkey`, `Czech Republic`, `Hong Kong`, `Egypt`, `Slovakia`, `Venezuela`) và gán mã ISO-3, nâng tỷ lệ khớp GDP lên **98.2%**.
  - Chuẩn hóa phân loại thể loại vĩ mô `macro_genre` (6 nhóm: `Pop`, `Latin`, `Hip-Hop/Rap`, `Rock/Metal`, `K-Pop`, `Others`) **chỉ dựa trên `artist_genre` và `track_genre`**, sử dụng regex word boundary (`\b`) để tránh gán sai (ví dụ `"uk pop"` không match `"k pop"`). KHÔNG dùng cột `language` vì đó là ngôn ngữ thị trường BXH, không phải ngôn ngữ bài hát. Mỗi `track_id` chỉ có **1 macro_genre duy nhất** (ổn định bằng mode).
  - Loại bỏ 5 cột yếu/gây nhiễu: `log_streams`, `covid_phase`, `is_popular` (66% NaN), `energy_loudness_index` (2 biến tương quan cao r≈0.8), `audio_diversity_score` (thiếu cơ sở khoa học).
  - Thêm 2 cột mới: `chart_longevity` (số tuần trụ hạng cao nhất) và `tempo_category` (Slow/Medium/Fast/Very Fast).
  - Lưu giữ chính xác **38 cột cốt lõi phục vụ Insight** cho đồ án.

#### Từ điển chi tiết 39 cột của `merged_spotify_data.csv`:

| STT | Tên cột | Kiểu dữ liệu | Nhóm thuộc tính | Ý nghĩa / Diễn giải phân tích |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `track_id` | String (22 ký tự) | Nhận dạng | Mã định danh duy nhất của bài hát trên Spotify |
| 2 | `track_name` | String | Nhận dạng | Tên bài hát |
| 3 | `artist_individual` | String | Nhận dạng | **Nghệ sĩ chính / nghệ sĩ đầu tiên** biểu diễn (bóc tách từ chuỗi hợp tác) |
| 4 | `artist_genre` | String | Nhận dạng | Thể loại âm nhạc gắn với nghệ sĩ (**⚠ biến động** giữa các tuần/nước — 47% bài có ≥2 nhãn) |
| 5 | `country` | String | Không gian | **Thị trường BXH** — 73 quốc gia và `Global` (⚠ `Global` không phải quốc gia, GDP/income_group sẽ NaN) |
| 6 | `language` | String | Không gian | **⚠ Ngôn ngữ THỊ TRƯỜNG BXH** (quốc gia phát hành bảng xếp hạng), **KHÔNG phải ngôn ngữ bài hát** |
| 7 | `week` | Date (YYYY-MM-DD) | Thời gian | Ngày đầu tiên của tuần ghi nhận bảng xếp hạng |
| 8 | `year` | Int64 | Thời gian | Năm phát hành bảng xếp hạng (`2020`, `2021`, `2022`) |
| 9 | `month` | Int64 | Thời gian | Tháng trong năm (`1` đến `12`) |
| 10 | `rank` | Int64 | Xếp hạng | Thứ hạng của bài hát trên Top 200 tuần (`1` đến `200`) |
| 11 | `streams` | Int64 | Lượt nghe | Số lượt phát trực tuyến tích lũy trong tuần |
| 12 | `weeks_on_chart` | Int64 | Trụ hạng | Số tuần bài hát duy trì có mặt trên bảng xếp hạng |
| 13 | `peak_rank` | Int64 | Trụ hạng | Thứ hạng cao nhất bài hát đạt được **trong phạm vi dữ liệu quan sát** |
| 14 | `danceability` | Float64 | Audio Feature | Mức độ phù hợp khiêu vũ / vũ đạo $[0.0, 1.0]$ |
| 15 | `energy` | Float64 | Audio Feature | Cường độ năng lượng, độ sôi động $[0.0, 1.0]$ |
| 16 | `loudness` | Float64 | Audio Feature | Độ to âm lượng tổng thể tính bằng Decibel ($[-60, 5]$ dB) |
| 17 | `speechiness` | Float64 | Audio Feature | Tỷ lệ xuất hiện của lời nói / rap trong track $[0.0, 1.0]$ |
| 18 | `acousticness` | Float64 | Audio Feature | Mức độ mộc / nhạc cụ acoustic không điện tử $[0.0, 1.0]$ |
| 19 | `instrumentalness`| Float64 | Audio Feature | Tỷ lệ không có lời hát (nhạc không lời) $[0.0, 1.0]$ |
| 20 | `liveness` | Float64 | Audio Feature | Xác suất bài hát được thu âm trực tiếp $[0.0, 1.0]$ |
| 21 | `valence` | Float64 | Audio Feature | Tính tích cực, vui tươi của giai điệu $[0.0, 1.0]$ |
| 22 | `tempo` | Float64 | Audio Feature | Tốc độ nhịp đập bài hát tính theo Beats Per Minute (BPM) |
| 23 | `gdp_value` | Float64 | Kinh tế World Bank| Tổng sản phẩm quốc nội USD hiện hành (khuyết ở bảng Global và TWN/VEN) |
| 24 | `gdp_log` | Float64 | Kinh tế World Bank| $\ln(1 + \text{gdp\_value})$ nén quy mô GDP hàng nghìn tỷ USD |
| 25 | `income_group` | String | Kinh tế World Bank| Phân tầng thu nhập (`High income`, `Upper middle`, `Lower middle`) |
| 26 | `region_wb` | String | Địa lý World Bank | Khu vực địa lý kinh tế theo phân loại chuẩn World Bank |
| 27 | `country_code` | String (3 ký tự) | Địa lý World Bank | Mã định danh ISO-alpha-3 của quốc gia |
| 28 | `is_trending` | Int64 (0/1) | Calculated Field | $1$ nếu bài hát xếp hạng Top 50 tuần ($\text{rank} \le 50$), $0$ nếu Top 51-200 |
| 29 | `mood_category` | String | Calculated Field | Phân loại **đặc tính cảm xúc bài hát** theo mô hình Russell 4 góc phần tư (`Unknown` khi thiếu audio) |
| 30 | `stream_share_country`| Float64 | Calculated Field | **Tỷ trọng lượt stream so với tổng stream của Top 200** trong thị trường–tuần |
| 31 | `macro_genre` | String | Calculated Field | **Dòng nhạc vĩ mô chuẩn hóa** — ổn định per track_id bằng mode (`Pop`, `Latin`, `Hip-Hop/Rap`, `Rock/Metal`, `K-Pop`, `Others`) |
| 32 | `is_legacy_artist`| Int64 (0/1) | Calculated Field | $1$ nếu nghệ sĩ nằm trong danh sách bán đĩa chạy nhất lịch sử (121 nghệ sĩ) |
| 33 | `duration_min` | Float64 | Calculated Field | Thời lượng bài hát tính theo phút ($\text{duration} / 60{,}000$) |
| 34 | `chart_longevity` | Int64 | Calculated Field | Số tuần trụ hạng cao nhất của bài ($\max(\text{weeks\_on\_chart})$ per track_id) — phân biệt flash hit vs evergreen |
| 35 | `tempo_category` | String | Calculated Field | Phân nhóm tốc độ nhịp: `Slow` (<90), `Medium` (90–120), `Fast` (120–150), `Very Fast` (≥150 BPM) |
| 36 | `track_genre` | String | Khám phá bổ trợ | Thể loại âm nhạc chi tiết của track từ bảng Tracks (⚠ NaN ở 66% dòng) |
| 37 | `popularity` | Float64 | Khám phá bổ trợ | Điểm số độ phổ biến toàn cầu của bài hát $[0, 100]$ (⚠ NaN ở 66% dòng) |
| 38 | `explicit` | Boolean | Khám phá bổ trợ | Cờ cảnh báo nội dung nhạy cảm / ca từ thô tục (`True`/`False`/`<NA>`) |

---

### 2.2. File Dữ liệu ML: `tracks_ml_data.csv` (19 Cột Cấp độ Bài hát cho ML)
* **Vị trí lưu trữ:** `data/processed/tracks_ml_data.csv`
* **Quy mô:** 36,699 bài hát độc nhất × 19 cột | **Dung lượng:** ~5.5 MB
* **Phục vụ chính:** Đỗ Thanh Thành Tài (ML Engineer — huấn luyện mô hình Logistic Regression & Linear Regression).
* **Đặc tính kỹ thuật & Chống rò rỉ dữ liệu (Data Leakage):**
  - **Cấp độ bài hát (Song-level):** Mỗi bài hát chỉ xuất hiện **duy nhất 1 dòng**, gom nhóm (groupby) theo `track_id`.
  - **Loại bỏ hoàn toàn biến không gian & thời gian:** Không chứa `country`, `week`, `year`, `streams` $\rightarrow$ Triệt tiêu rủi ro rò rỉ dữ liệu khi chia tập Train / Test.
  - **Cột categorical dùng `mode`** (giá trị xuất hiện nhiều nhất) thay vì `first` cho `artist_genre` và `language` — đảm bảo ổn định.
  - **Tỷ lệ nhãn cân bằng:** Tỷ lệ nhãn Hit (`is_trending = 1`) đạt **~35.9%** (rất lý tưởng cho mô hình phân loại nhị phân).
  - **⚠ Lưu ý:** `chart_longevity` là biến hậu phát hành — **KHÔNG dùng làm feature ML**, chỉ dùng cho EDA.
* **Cấu trúc 19 cột:** `track_id`, `track_name`, `artist_individual`, `artist_genre`, `language`, `danceability`, `energy`, `loudness`, `speechiness`, `acousticness`, `instrumentalness`, `liveness`, `valence`, `tempo`, `duration_min`, `macro_genre`, `tempo_category`, `chart_longevity`, `is_trending` (nhãn mục tiêu).

---

## 3. KHẢO SÁT CHẤT LƯỢNG DỮ LIỆU, DỊ BIỆT & CẢNH BÁO RÒ RỈ

Trong quá trình phân tích sâu dữ liệu thô và đối soát kiểm thử, một số hiện tượng đặc thù kỹ thuật đã được làm rõ:

### 3.1. Tính bất ổn định và gán nhãn của các trường dữ liệu
1. **Trường `language`:**
   - Trong dữ liệu Spotify Charts, giá trị trường `language` được **gán cố định theo quốc gia/thị trường phát hành bảng xếp hạng**, không phải ngôn ngữ thực tế của bài hát thu âm.
   - *Hệ quả:* Một bài hát phát hành toàn cầu có thể mang tới **40 nhãn ngôn ngữ khác nhau** giữa các dòng xếp hạng tại các quốc gia.
2. **Tính bất ổn định của `artist_genre`:**
   - Trường thể loại nghệ sĩ không bất biến. Thống kê cho thấy **17,272 trên tổng số 36,699 bài hát độc nhất (47.07%)** mang nhiều nhãn thể loại khác nhau giữa các dòng xếp hạng (ví dụ ca khúc *"Mr. Brightside"* của The Killers mang tới 5 nhãn thể loại khác nhau).
   - *Giải pháp:* Gom nhóm về `macro_genre` bằng cách kết hợp `artist_genre` và `track_genre` với regex word boundary (`\b`), tuyệt đối không dùng `language`, và ổn định duy nhất 1 nhãn per `track_id` bằng hàm `mode`.
3. **Định nghĩa `is_trending` ở cấp bài hát:**
   - Ở cấp độ bài hát (song-level trong `tracks_ml_data.csv`), nhãn `is_trending` được tính bằng `max(is_trending)`.
   - *Bản chất:* Mang ý nghĩa *"bài hát từng ít nhất 1 lần lọt vào Top 50 ở bất kỳ bảng xếp hạng nào (kể cả bảng Global)"*.
   - *Thiên lệch mẫu:* Các bài hát phát hành quốc tế, xuất hiện ở nhiều quốc gia, hoặc trụ hạng nhiều tuần có xác suất đạt nhãn 1 cao hơn các ca khúc nội địa; các ca khúc ra mắt muộn vào cuối năm 2022 có ít thời gian tích lũy để lọt top hơn.
4. **Dữ liệu Global 2020:**
   - Trong tập dữ liệu Spotify Weekly Charts, năm 2020 **chỉ có duy nhất bảng xếp hạng Global** (chưa ghi nhận 73 quốc gia thành viên).
   - Do đó, nếu gán nhãn giai đoạn đại dịch tĩnh theo năm (`covid_phase = "Lockdown & Shock"` cho 2020), toàn bộ các dòng này sẽ trùng lẫn hoàn toàn với thực thể Global và đều khuyết quốc gia, mã ISO, GDP và nhóm thu nhập. Vì vậy, cột `covid_phase` đã được loại bỏ khỏi Master Dataset để tránh sai lệch phân tích.

### 3.2. Thống kê các giá trị dị biệt (Outliers)
Qua kiểm tra toàn bộ 1,078,125 bản ghi:
* **145 dòng thiếu đặc trưng âm thanh:** Một số bản ghi trong bảng charts không có đầy đủ audio features do Spotify API chưa kịp lập chỉ mục.
* **87 dòng có thời lượng dài hơn 15 phút ($> 15$ phút):** Thường là các bản podcast, bản hòa tấu nhạc kịch dài hoặc bản mix DJ live được đưa lên Spotify.
* **34 dòng có độ to âm lượng cực nhỏ ($\text{loudness} < -30\text{ dB}$):** Thuộc về các bản ghi âm thiền, tiếng ồn trắng (white noise) hoặc nhạc ru ngủ môi trường.

### 3.3. Cảnh báo rò rỉ dữ liệu (Data Leakage) khi huấn luyện mô hình
Khi xây dựng mô hình dự báo mức độ thịnh hành của bài hát (`is_trending`), người thực hiện (Đỗ Thanh Thành Tài) cần lưu ý:
> [!WARNING]
> **Các cột phản ánh kết quả sau phát hành (Post-release Metrics):**
> - `streams`, `stream_share_country`, `weeks_on_chart`, `peak_rank`, `chart_longevity` cũng như biến phái sinh `log_streams` là những thông tin chỉ xuất hiện **sau khi** ca khúc đã được phát hành và được khán giả nghe thực tế trên thị trường.
> - **Tuyệt đối không sử dụng** các cột này làm đặc trưng đầu vào (input features) khi huấn luyện mô hình Machine Learning dự báo bài hát thịnh hành, vì sẽ gây ra hiện tượng **Rò rỉ dữ liệu (Data Leakage)** nghiêm trọng, làm mô hình đạt độ chính xác ảo (over-optimistic) nhưng vô dụng trong thực tế.

---

## 4. TỔNG HỢP 9 CALCULATED FIELDS & CÔNG THỨC TOÁN HỌC

Trong Master Dataset 38 cột, có **9 Calculated Fields** được tính toán và chuẩn hóa:

| STT | Trường tính toán | Quy tắc logic / Công thức toán học | Ứng dụng phân tích |
| :---: | :--- | :--- | :--- |
| 1 | `is_trending` | $$\text{is\_trending} = \mathbb{I}(\text{rank} \le 50)$$ | Biến phụ thuộc mục tiêu phân loại Top Hit. |
| 2 | `mood_category` | $$\begin{cases} \text{Happy Energetic} & \text{valence} \ge 0.5 \land \text{energy} \ge 0.5 \\ \text{Peaceful Positive} & \text{valence} \ge 0.5 \land \text{energy} < 0.5 \\ \text{Tense Aggressive} & \text{valence} < 0.5 \land \text{energy} \ge 0.5 \\ \text{Sad Melancholic} & \text{valence} < 0.5 \land \text{energy} < 0.5 \\ \text{Unknown} & \text{valence hoặc energy là NaN} \end{cases}$$ | Phân loại **đặc tính cảm xúc bài hát** (không phải tâm trạng người nghe) theo mô hình Russell 4 góc phần tư. |
| 3 | `stream_share_country` | $$\text{share}_{i, c, w} = \frac{\text{streams}_{i, c, w}}{\sum_{k \in \text{Top200}(c, w)} \text{streams}_{k, c, w}}$$ | Tỷ trọng thống trị của bài hát tại thị trường trong tuần. |
| 4 | `macro_genre` | Phân loại ưu tiên 6 nhóm bằng regex có word boundary (`\b`):<br>1. **K-Pop:** `\b(k-pop|kpop|k pop|k-rap)\b`<br>2. **Latin:** `\b(latin|reggaeton|salsa|...)\b`<br>3. **Hip-Hop/Rap:** `\b(hip hop|hip-hop|rap|trap)\b`<br>4. **Rock/Metal:** `\b(rock|metal|punk)\b`<br>5. **Pop:** `\b(pop|electropop)\b`<br>6. **Others:** các thể loại còn lại<br>**⚠ KHÔNG dùng `language`** (vì đó là ngôn ngữ thị trường). Ổn định per track_id bằng mode. | Danh mục dòng nhạc vĩ mô đồng nhất, ổn định 1 nhãn duy nhất cho mỗi bài hát. |
| 5 | `is_legacy_artist` | $$\mathbb{I}(\text{legacy\_artist\_name is not Null})$$ | Đánh dấu các nghệ sĩ huyền thoại bán đĩa chạy nhất lịch sử (121 nghệ sĩ). |
| 6 | `duration_min` | $$\text{duration\_min} = \frac{\text{duration}}{60{,}000}$$ | Quy đổi thời lượng sang phút để phân tích xu hướng rút ngắn track. |
| 7 | `chart_longevity` | $$\text{chart\_longevity} = \max_{\text{per track\_id}}(\text{weeks\_on\_chart})$$ | Số tuần trụ hạng cao nhất — phân biệt flash hit (1-2 tuần) vs evergreen (nhiều tháng). |
| 8 | `tempo_category` | $$\begin{cases} \text{Slow} & \text{tempo} < 90 \\ \text{Medium} & 90 \le \text{tempo} < 120 \\ \text{Fast} & 120 \le \text{tempo} < 150 \\ \text{Very Fast} & \text{tempo} \ge 150 \end{cases}$$ | Phân nhóm tốc độ nhịp phục vụ trực quan hóa phân bổ tempo trên Dashboard. |
| 9 | `gdp_log` | $$\text{gdp\_log} = \ln(1 + \text{gdp\_value})$$ | Nén biên độ GDP hàng nghìn tỷ USD phục vụ phân tích tương quan kinh tế. |

---

## 5. HƯỚNG DẪN TRUY XUẤT DỮ LIỆU THÔNG QUA PYTHON API

Module [`src/data_loader.py`](file:///d:/uni/hk1nam3/idvi/idvi-final_project/Spotify_Audio_Trends_Analytics/src/data_loader.py) cung cấp các hàm nạp tiện ích:

```python
# 1. Nạp tệp Master dữ liệu lớn (merged_spotify_data.csv):
from src.data_loader import load_master_data
df_master = load_master_data()  # hoặc load_master_data(nrows=50000)
print(f"Master Dataset: {df_master.shape}")  # (1,078,125 dòng x 39 cột)

# 2. Nạp tệp Song-level cho Machine Learning:
from src.data_loader import load_ml_data
df_ml = load_ml_data()
print(f"ML Dataset: {df_ml.shape}")          # (36,699 bài x 17 cột)
```
