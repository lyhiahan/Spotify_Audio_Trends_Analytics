# 📚 TỪ ĐIỂN DỮ LIỆU TOÀN DIỆN (DATA DICTIONARY)
**Dự án:** Nghiên cứu & Trực quan hóa Đặc trưng Âm thanh và Dự đoán Xu hướng Bài hát Thịnh hành trên Spotify  
**Môn học:** Tương tác Dữ liệu (Interactive Data Visualization / Visual Analytics)  
**Tác giả:** Đinh Quốc Anh (Data Engineer & Data Analyst)  
**Phiên bản:** 3.1 (Kiến trúc Master Dataset Hợp nhất 41 Cột & Các Tệp Sample)  

---

## MỤC LỤC
1. [TỔNG QUAN NGUỒN DỮ LIỆU (5 BẢNG THÔ BAN ĐẦU)](#1-tổng-quan-nguồn-dữ-liệu-5-bảng-thô-ban-đầu)
   * [1.1. Bảng `best-selling-artists.csv`](#11-bảng-best-selling-artistscsv)
   * [1.2. Bảng `country_codes.csv`](#12-bảng-country_codescsv)
   * [1.3. Bảng `gdp_data.csv`](#13-bảng-gdp_datacsv)
   * [1.4. Bảng `spotify-tracks-dataset.csv`](#14-bảng-spotify-tracks-datasetcsv)
   * [1.5. Bảng `spotify-weekly-charts.csv`](#15-bảng-spotify-weekly-chartscsv)
2. [CÁC TỆP DỮ LIỆU ĐẦU RA SAU XỬ LÝ (OUTPUT DATASETS)](#2-các-tệp-dữ-liệu-đầu-ra-sau-xử-lý-output-datasets)
   * [2.1. File Master: `merged_spotify_data.csv` (41 Cột Phục vụ Insight)](#21-file-master-merged_spotify_datacsv-41-cột-phục-vụ-insight)
   * [2.2. File Sample 1: `spotify_sample_merged.csv` (Bản mẫu Dashboard & EDA)](#22-file-sample-1-spotify_sample_mergedcsv-bản-mẫu-dashboard--eda)
   * [2.3. File Sample 2: `tracks_sample_ml.csv` (Dữ liệu Song-level cho Thành Tài làm ML)](#23-file-sample-2-tracks_sample_mlcsv-dữ-liệu-song-level-cho-thành-tài-làm-ml)
3. [TỔNG HỢP 13 CALCULATED FIELDS & CÔNG THỨC TOÁN HỌC](#3-tổng-hợp-13-calculated-fields--công-thức-toán-học)
4. [HƯỚNG DẪN TRUY XUẤT DỮ LIỆU THÔNG QUA PYTHON API](#4-hướng-dẫn-truy-xuất-dữ-liệu-thông-qua-python-api)

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

| Tên trường | Kiểu dữ liệu | Ý nghĩa / Diễn giải | Giá trị hợp lệ / Ví dụ |
| :--- | :--- | :--- | :--- |
| `country_code` | String (3 ký tự) | Mã định danh quốc gia chuẩn ISO-alpha-3 | `USA`, `VNM`, `GBR`, `BRA` |
| `region` | String | Khu vực địa lý theo phân loại World Bank | `East Asia & Pacific`, `Europe & Central Asia`, `Latin America & Caribbean`,... |
| `income_group` | String | Phân tầng nhóm thu nhập quốc gia | `High income`, `Upper middle income`, `Lower middle income`, `Low income` |

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
| `explicit` | Boolean / Int | Cờ cảnh báo nội dung nhạy cảm | `True` (1) / `False` (0) |
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
* **Mục đích:** Xương sống chuỗi thời gian, ghi nhận thứ hạng, số lượt streams, tên bài hát, nghệ sĩ tại 74 quốc gia và bảng Global từ 2016 đến 2022.
* **Xử lý làm sạch:**
  - Trích xuất `track_id` từ URI (`spotify:track:<id>`).
  - Ép kiểu `week` sang chuẩn `datetime`, tách `year`, `month`, `quarter`.
  - Lọc bỏ triệt để các bản ghi có `streams <= 0` hoặc `week` bị rỗng.
  - Khử trùng lặp bộ ba định danh `(track_id, week, country)`.
  - Loại bỏ sớm 15 cột phụ không mang giá trị cho insight (`Unnamed: 0`, `uri`, `artist_names`, `artists_num`, `artist_id`, `key`, `mode`, `source`, `album_num_tracks`, `collab`, `release_date`, `previous_rank`, `artist_img`, `album_cover`, `pivot`, `region`).

---

## 2. CÁC TỆP DỮ LIỆU ĐẦU RA SAU XỬ LÝ (OUTPUT DATASETS)

Hệ thống ETL hợp nhất dữ liệu vào **1 tệp Master lớn duy nhất** trong `data/processed/` và sinh **2 tệp sample gọn nhẹ** trong `data/sample/`:

```text
data/
├── processed/
│   └── merged_spotify_data.csv # 1,078,125 dòng × 41 cột (407.4 MB) — Master Dataset
└── sample/
    ├── spotify_sample_merged.csv # 20,000 dòng × 41 cột (7.6 MB) — Bản mẫu Dashboard & EDA
    └── tracks_sample_ml.csv     # 36,699 bài hát × 18 cột (5.7 MB) — Song-level ML cho Thành Tài
```

---

### 2.1. File Master: `merged_spotify_data.csv` (41 Cột Phục vụ Insight)
* **Quy mô:** 1,078,125 dòng × 41 cột | **Dung lượng:** ~407.4 MB
* **Đặc điểm kiến trúc:**
  - Hợp nhất toàn bộ dữ liệu 74 quốc gia và bảng Global giai đoạn 2020 – 2022.
  - Tích hợp cả số liệu Kinh tế - Xã hội World Bank và phân kỳ 3 giai đoạn đại dịch COVID-19 (`covid_phase`).
  - Lưu giữ chính xác **41 cột cốt lõi phục vụ Insight** cho đồ án, loại bỏ hoàn toàn các cột dư thừa từ raw.

#### Từ điển chi tiết 41 cột của `merged_spotify_data.csv`:

| STT | Tên cột | Kiểu dữ liệu | Nhóm thuộc tính | Ý nghĩa / Diễn giải phân tích |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `track_id` | String (22 ký tự) | Nhận dạng | Mã định danh duy nhất của bài hát trên Spotify |
| 2 | `track_name` | String | Nhận dạng | Tên bài hát |
| 3 | `artist_individual` | String | Nhận dạng | Tên từng nghệ sĩ riêng biệt biểu diễn bản thu |
| 4 | `artist_genre` | String | Nhận dạng | Thể loại âm nhạc gắn với nghệ sĩ |
| 5 | `country` | String | Không gian | Tên quốc gia của bảng xếp hạng (74 quốc gia và `Global`) |
| 6 | `language` | String | Nhận dạng | Ngôn ngữ chính thể hiện bài hát (English, Spanish,...) |
| 7 | `week` | Date (YYYY-MM-DD) | Thời gian | Ngày đầu tiên của tuần ghi nhận bảng xếp hạng |
| 8 | `year` | Int64 | Thời gian | Năm phát hành bảng xếp hạng (`2020`, `2021`, `2022`) |
| 9 | `month` | Int64 | Thời gian | Tháng trong năm (`1` đến `12`) |
| 10 | `quarter` | Int64 | Thời gian | Quý trong năm (`1` đến `4`) |
| 11 | `rank` | Int64 | Xếp hạng | Thứ hạng của bài hát trên Top 200 tuần (`1` đến `200`) |
| 12 | `streams` | Int64 | Lượt nghe | Số lượt phát trực tuyến tích lũy trong tuần |
| 13 | `log_streams` | Float64 | Lượt nghe | $\ln(1 + \text{streams})$ giúp chuẩn hóa phân phối lệch phải |
| 14 | `weeks_on_chart` | Int64 | Trụ hạng | Số tuần bài hát duy trì có mặt trên bảng xếp hạng |
| 15 | `peak_rank` | Int64 | Trụ hạng | Thứ hạng cao nhất bài hát từng đạt được lịch sử |
| 16 | `danceability` | Float64 | Audio Feature | Mức độ phù hợp khiêu vũ / vũ đạo $[0.0, 1.0]$ |
| 17 | `energy` | Float64 | Audio Feature | Cường độ năng lượng, độ sôi động $[0.0, 1.0]$ |
| 18 | `loudness` | Float64 | Audio Feature | Độ to âm lượng tổng thể tính bằng Decibel ($[-60, 5]$ dB) |
| 19 | `speechiness` | Float64 | Audio Feature | Tỷ lệ xuất hiện của lời nói / rap trong track $[0.0, 1.0]$ |
| 20 | `acousticness` | Float64 | Audio Feature | Mức độ mộc / nhạc cụ acoustic không điện tử $[0.0, 1.0]$ |
| 21 | `instrumentalness`| Float64 | Audio Feature | Tỷ lệ không có lời hát (nhạc không lời) $[0.0, 1.0]$ |
| 22 | `liveness` | Float64 | Audio Feature | Xác suất bài hát được thu âm trực tiếp $[0.0, 1.0]$ |
| 23 | `valence` | Float64 | Audio Feature | Tính tích cực, vui tươi của giai điệu $[0.0, 1.0]$ |
| 24 | `tempo` | Float64 | Audio Feature | Tốc độ nhịp đập bài hát tính theo Beats Per Minute (BPM) |
| 25 | `gdp_value` | Float64 | Kinh tế World Bank| Tổng sản phẩm quốc nội tính bằng USD hiện hành (với các quốc gia) |
| 26 | `gdp_log` | Float64 | Kinh tế World Bank| $\ln(1 + \text{gdp\_value})$ nén quy mô GDP hàng nghìn tỷ USD |
| 27 | `income_group` | String | Kinh tế World Bank| Phân tầng thu nhập (`High`, `Upper middle`, `Lower middle`, `Low`) |
| 28 | `region_wb` | String | Địa lý World Bank | Khu vực địa lý kinh tế theo World Bank |
| 29 | `country_code` | String (3 ký tự) | Địa lý World Bank | Mã định danh ISO-alpha-3 của quốc gia |
| 30 | `is_trending` | Int64 (0/1) | Calculated Field | $1$ nếu bài hát xếp hạng Top 50 tuần ($\text{rank} \le 50$), $0$ nếu Top 51-200 |
| 31 | `is_popular` | Int64 (0/1) | Calculated Field | $1$ nếu điểm phổ biến toàn cầu $\text{popularity} \ge 70$, $0$ nếu $< 70$ |
| 32 | `mood_category` | String | Calculated Field | Phân loại tâm trạng theo mô hình Russell 4 góc phần tư |
| 33 | `stream_share_country`| Float64 | Calculated Field | Tỷ trọng lượt stream của bài hát so với tổng stream của nước trong tuần |
| 34 | `covid_phase` | String | Calculated Field | 3 giai đoạn đại dịch (`Lockdown & Shock`, `Vaccine & Escapism`, `Reopening & New Normal`) |
| 35 | `energy_loudness_index`| Float64 | Calculated Field | Chỉ số cường độ âm thanh tổng hợp chuẩn hóa $[0, 1]$ |
| 36 | `is_latin` | Int64 (0/1) | Calculated Field | $1$ nếu là bài hát thuộc dòng nhạc Latin hoặc tiếng Tây Ban Nha/Bồ Đào Nha |
| 37 | `is_kpop` | Int64 (0/1) | Calculated Field | $1$ nếu là bài hát K-Pop hoặc tiếng Hàn Quốc |
| 38 | `is_legacy_artist`| Int64 (0/1) | Calculated Field | $1$ nếu nghệ sĩ nằm trong danh sách bán đĩa chạy nhất lịch sử |
| 39 | `duration_min` | Float64 | Calculated Field | Thời lượng bài hát tính theo phút |
| 40 | `audio_diversity_score`| Float64 | Calculated Field | Độ lệch chuẩn giữa 4 đặc trưng âm học chính của bài hát |
| 41 | `track_genre` | String | Khám phá bổ trợ | Thể loại âm nhạc chi tiết của track từ bảng Tracks |

---

### 2.2. File Sample 1: `spotify_sample_merged.csv` (Bản mẫu Dashboard & EDA)
* **Quy mô:** 20,000 dòng × 41 cột | **Dung lượng:** ~7.6 MB
* **Nguồn gốc:** Lấy mẫu ngẫu nhiên có cố định hạt giống (`random_state=42`) từ Master Dataset.
* **Mục đích:** Giúp nhóm phát triển giao diện Streamlit Dashboard và kiểm thử nhanh các biểu đồ Plotly trong 0.2 giây mà không cần nạp tệp 407 MB.

---

### 2.3. File Sample 2: `tracks_sample_ml.csv` (Dữ liệu Song-level cho Thành Tài làm ML)
* **Quy mô:** 36,699 bài hát độc nhất × 18 cột | **Dung lượng:** ~5.7 MB
* **Phục vụ chính:** Đỗ Thanh Thành Tài (ML Engineer — huấn luyện mô hình Logistic Regression dự báo Top Hit).
* **Đặc tính kỹ thuật & Chống rò rỉ dữ liệu (Data Leakage):**
  - **Cấp độ bài hát (Song-level):** Mỗi bài hát chỉ xuất hiện **duy nhất 1 dòng**.
  - **Loại bỏ hoàn toàn biến không gian & thời gian:** Không chứa `country`, `week`, `year`, `streams` $\rightarrow$ Triệt tiêu 100% rủi ro Data Leakage khi chia tập Train / Test.
  - **Tỷ lệ nhãn cân bằng:** Tỷ lệ nhãn Hit (`is_trending = 1`) đạt **35.9%** (rất lý tưởng cho mô hình phân loại nhị phân).
* **Cấu trúc 18 cột:** `track_id`, `track_name`, `artist_individual`, `artist_genre`, `language`, `danceability`, `energy`, `loudness`, `speechiness`, `acousticness`, `instrumentalness`, `liveness`, `valence`, `tempo`, `duration_min`, `is_latin`, `is_kpop`, `is_trending` (nhãn mục tiêu).

---

## 3. TỔNG HỢP 13 CALCULATED FIELDS & CÔNG THỨC TOÁN HỌC

| STT | Tên trường tính toán | Công thức toán học / Quy tắc logic | Ứng dụng cụ thể trong đề tài |
| :---: | :--- | :--- | :--- |
| 1 | `is_trending` | $\text{is\_trending} = \mathbb{I}(\text{rank} \le 50)$ | Biến phụ thuộc (nhãn phân loại) cho bài toán dự báo Top Hit. |
| 2 | `is_popular` | $\text{is\_popular} = \mathbb{I}(\text{popularity} \ge 70)$ | Đo lường độ lan tỏa quốc tế của bản thu dựa trên thuật toán Spotify. |
| 3 | `mood_category` | $\begin{cases} \text{Happy Energetic} & \text{valence} \ge 0.5 \land \text{energy} \ge 0.5 \\ \text{Peaceful Positive} & \text{valence} \ge 0.5 \land \text{energy} < 0.5 \\ \text{Tense Aggressive} & \text{valence} < 0.5 \land \text{energy} \ge 0.5 \\ \text{Sad Melancholic} & \text{valence} < 0.5 \land \text{energy} < 0.5 \end{cases}$ | Trực quan hóa bản đồ tâm trạng người nghe 4 góc phần tư trên Dashboard. |
| 4 | `stream_share_country` | $\text{share}_{i, c, w} = \frac{\text{streams}_{i, c, w}}{\sum_{k \in c, w} \text{streams}_{k, c, w}}$ | Đo lường tỷ trọng thống trị của bài hát tại thị trường quốc gia trong tuần. |
| 5 | `covid_phase` | $\begin{cases} \text{Lockdown \& Shock} & \text{year} \le 2020 \\ \text{Vaccine \& Escapism} & \text{year} = 2021 \\ \text{Reopening \& New Normal} & \text{year} \ge 2022 \end{cases}$ | Phân tích biến động âm nhạc qua 3 cột mốc lịch sử đại dịch toàn cầu. |
| 6 | `energy_loudness_index` | $\text{loud\_norm} = \frac{\text{loudness} - \min(\text{loudness})}{\max(\text{loudness}) - \min(\text{loudness})}$<br>$\text{index} = \frac{\text{energy} + \text{loud\_norm}}{2}$ | Chỉ số gộp đại diện cho cường độ âm thanh tổng hợp của track. |
| 7 | `is_latin` | $(\text{genre} \text{ match 32 keywords Latin}) \lor (\text{lang} \in \{\text{es}, \text{pt}\})$ | Định lượng sự trỗi dậy của âm nhạc Latin trên thị trường thế giới. |
| 8 | `is_kpop` | $(\text{genre} \text{ match } \{\text{k-pop}, \text{kpop}, \text{korean}\}) \lor (\text{lang} == \text{ko})$ | Định lượng làn sóng Hallyu / K-Pop vươn ra quốc tế. |
| 9 | `is_legacy_artist` | $\mathbb{I}(\text{legacy\_artist\_name} \neq \text{Null})$ | Khảo sát mức độ trụ hạng của các tên tuổi huyền thoại (The Beatles, Queen). |
| 10 | `duration_min` | $\text{duration\_min} = \frac{\text{duration\_ms}}{60,000}$ | Quy đổi thời lượng sang phút để phân tích xu hướng rút ngắn bài hát. |
| 11 | `audio_diversity_score`| $\text{StdDev}(\text{danceability}, \text{energy}, \text{valence}, \text{acousticness})$ | Đo lường sự đa dạng / xung đột cảm xúc trong cùng một bài hát. |
| 12 | `log_streams` | $\log(1 + \text{streams})$ | Đưa phân phối lượt nghe lệch phải về phân phối chuẩn Gauss. |
| 13 | `gdp_log` | $\log(1 + \text{gdp\_value})$ | Nén biên độ chênh lệch GDP giữa các siêu cường và các nước nhỏ. |

---

## 4. HƯỚNG DẪN TRUY XUẤT DỮ LIỆU THÔNG QUA PYTHON API

Module [`src/data_loader.py`](file:///d:/uni/hk1nam3/idvi/idvi-final_project/Spotify_Audio_Trends_Analytics/src/data_loader.py) cung cấp sẵn 3 hàm nạp tiện ích:

```python
# 1. Nạp tệp Master dữ liệu lớn (merged_spotify_data.csv):
from src.data_loader import load_master_data
df_master = load_master_data()  # hoặc load_master_data(nrows=50000)
print(f"Master Dataset: {df_master.shape}")

# 2. Nạp tệp Sample 20,000 dòng có đầy đủ 41 cột (phục vụ Dashboard và EDA):
from src.data_loader import load_sample_data
df_sample = load_sample_data()
print(f"Sample Dashboard: {df_sample.shape}")

# 3. Nạp tệp Song-level Sample cho Thành Tài làm Machine Learning:
from src.data_loader import load_ml_sample
df_ml = load_ml_sample()
print(f"ML Sample: {df_ml.shape}")
```
