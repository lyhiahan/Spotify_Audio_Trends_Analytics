# TỪ ĐIỂN DỮ LIỆU ĐỒ ÁN IDVI (DATA DICTIONARY)

**Đề tài:** Nghiên cứu và trực quan hóa các đặc trưng âm thanh và tương quan với các vấn đề xã hội. Phân tích dự đoán xu hướng bài hát thịnh hành trên Spotify  
**Thời gian cập nhật:** Tháng 10/2026  
**Phạm vi tài liệu:** Ghi nhận cấu trúc chi tiết của 5 tập tin dữ liệu thô tại [`data/raw/`](file:///d:/uni/hk1nam3/idvi/idvi-final_project/project-indv/data/raw), 5 tập tin dữ liệu sạch cốt lõi (Tầng Silver) và 4 tập tin Data Marts tinh gọn (Tầng Gold) tại [`data/processed/`](file:///d:/uni/hk1nam3/idvi/idvi-final_project/project-indv/data/processed) phục vụ trực tiếp 3 Dashboard và bài toán Machine Learning, được xử lý đồng bộ từ notebook [`notebooks/01_preprocess.ipynb`](file:///d:/uni/hk1nam3/idvi/idvi-final_project/project-indv/notebooks/01_preprocess.ipynb).

---

## MỤC LỤC
1. [Dữ Liệu Thô (Raw Data - data/raw/)](#1-dữ-liệu-thô-raw-data---dataraw)
   - [1.1. spotify-weekly-charts.csv](#11-spotify-weekly-chartscsv)
   - [1.2. global_deaths.csv](#12-global_deathscsv)
   - [1.3. gdp_data.csv](#13-gdp_datacsv)
   - [1.4. country_codes.csv](#14-country_codescsv)
   - [1.5. whs_years_updated.csv](#15-whs_years_updatedcsv)
2. [Dữ Liệu Sạch Cốt Lõi (Core Processed Data - data/processed/)](#2-dữ-liệu-sạch-cốt-lõi-core-processed-data---dataprocessed)
   - [2.1. charts_clean.parquet](#21-charts_cleanparquet)
   - [2.2. tracks_dimension.csv](#22-tracks_dimensioncsv)
   - [2.3. country_lookup.csv](#23-country_lookupcsv)
   - [2.4. covid_weekly_clean.csv](#24-covid_weekly_cleancsv)
   - [2.5. whs_clean.csv](#25-whs_cleancsv)
3. [Dữ Liệu Data Marts (Dashboard & Machine Learning)](#3-dữ-liệu-data-marts-dashboard--machine-learning)
   - [3.1. mart_audio_trend_weekly.parquet (Dashboard 1 & 3)](#31-mart_audio_trend_weeklyparquet-dashboard-1--3)
   - [3.2. mart_artist_chart.parquet (Dashboard 1 - 0% NaN)](#32-mart_artist_chartparquet-dashboard-1---0-nan)
   - [3.3. mart_country_year.parquet (Dashboard 2)](#33-mart_country_yearparquet-dashboard-2)
   - [3.4. ml_tracks.parquet & ml_tracks.csv (Machine Learning - 0% NaN)](#34-ml_tracksparquet--ml_trackscsv-machine-learning---0-nan)
4. [Bảng Khóa Ghép Nối & Quan Hệ Thực Thể](#4-bảng-khóa-ghép-nối--quan-hệ-thực-thể)
5. [Chú Thích Nghiệp Vụ & Kỹ Thuật Chuyên Sâu](#5-chú-thích-nghiệp-vụ--kỹ-thuật-chuyên-sâu)

---

## 1. DỮ LIỆU THÔ (RAW DATA - `data/raw/`)

### 1.1. `spotify-weekly-charts.csv`
- **Dung lượng:** 796.63 MB | **Kích thước:** 1,787,999 dòng, 36 cột.
- **Mô tả:** Bảng xếp hạng Top 200 ca khúc hàng tuần trên 73 quốc gia và thị trường Global từ ngày 29/12/2016 đến ngày 14/07/2022.

| Tên biến | Kiểu dữ liệu | Ý nghĩa và Mô tả chi tiết |
| :--- | :---: | :--- |
| `Unnamed: 0` | `int64` | Chỉ số index tự sinh khi xuất tệp CSV ban đầu (loại bỏ trong tiền xử lý). |
| `uri` | `object` | Mã định danh Spotify URI dạng chuỗi `spotify:track:ID` (tách lấy 22 ký tự ID). |
| `rank` | `int64` | Thứ hạng của bài hát trong tuần xếp hạng (từ 1 đến 200). Trong tệp thô có 73 dòng header rác được làm sạch khi nạp. |
| `peak_rank` | `int64` | Thứ hạng cao nhất ca khúc từng đạt được tính đến tuần xếp hạng. |
| `previous_rank` | `int64` | Thứ hạng của bài hát ở tuần trước đó (-1 đại diện cho ca khúc mới lọt bảng). |
| `weeks_on_chart` | `int64` | Tổng số tuần ca khúc đã hiện diện liên tục hoặc ngắt quãng trên bảng xếp hạng. |
| `streams` | `int64` | Tổng lượt stream của ca khúc trong tuần xếp hạng. |
| `week` | `object` | Ngày bắt đầu tuần xếp hạng (định dạng YYYY-MM-DD, chốt vào thứ Năm). |
| `track_name` | `object` | Tên tác phẩm âm nhạc (bài hát). |
| `artist_names` | `object` | Danh sách tên toàn bộ các nghệ sĩ tham gia biểu diễn ca khúc. |
| `artist_id` | `object` | Mã định danh nghệ sĩ Spotify URI dạng `spotify:artist:ID` (tách 22 ký tự ID). |
| `artist_img` | `object` | Đường dẫn URL ảnh đại diện của nghệ sĩ (loại bỏ do nhiều ô trống). |
| `album_cover` | `object` | Đường dẫn URL ảnh bìa album (loại bỏ do nhiều ô trống). |
| `album_num_tracks`| `float64` | Tổng số lượng bài hát có trong album chứa ca khúc. |
| `release_date` | `object` | Ngày phát hành ban đầu của ca khúc (định dạng YYYY-MM-DD, YYYY-MM hoặc YYYY). |
| `country` | `object` | Mã hoặc tên quốc gia của bảng xếp hạng (73 nước và Global). |
| `region` | `object` | Khu vực địa lý của quốc gia theo phân loại của Spotify. |
| `language` | `object` | Ngôn ngữ chiếm ưu thế của quốc gia xếp hạng. |
| `collab` | `int64` | Cờ nhị phân biểu thị ca khúc hợp tác (1 nếu có nhiều nghệ sĩ, 0 nếu đơn ca). |
| `pivot` | `int64` | Cột kỹ thuật nội bộ sinh ra khi crawl dữ liệu gốc (loại bỏ). |
| `artist_individual`| `object` | Tên của từng nghệ sĩ riêng lẻ tương ứng 1:1 với `artist_id` (được giữ lại phục vụ nhận diện chính xác cá nhân nghệ sĩ). |
| `artists_num` | `int64` | Số lượng nghệ sĩ tham gia biểu diễn trong ca khúc (từ 1 đến 12). |
| `artist_genre` | `object` | Thể loại âm nhạc chính của bài hát / nghệ sĩ. |
| `source` | `object` | Nhà phát hành hoặc hãng thu âm phát hành ca khúc. |
| `danceability` | `float64` | Độ phù hợp để khiêu vũ dựa trên nhịp điệu và độ ổn định phách (thang đo 0.0 - 1.0). |
| `energy` | `float64` | Cường độ hoạt động, tốc độ và độ sôi động của âm thanh (thang đo 0.0 - 1.0). |
| `key` | `float64` | Cung nốt nhạc cơ bản của bài hát theo hệ Pitch Class (0 = C, 1 = C#, ..., 11 = B). |
| `mode` | `float64` | Thang âm của bài hát (1 = Trưởng / Major, 0 = Thứ / Minor). |
| `loudness` | `float64` | Âm lượng tổng thể trung bình của bản thu tính bằng Decibel (dB, từ -60 đến 0 dB). |
| `speechiness` | `float64` | Mức độ xuất hiện của từ ngữ nói / lời rap trong ca khúc (thang đo 0.0 - 1.0). |
| `acousticness` | `float64` | Mức độ âm thanh mộc, không dùng nhạc cụ điện tử (thang đo 0.0 - 1.0). |
| `instrumentalness`| `float64` | Đo lường mức độ không có giọng hát trong ca khúc (thang đo 0.0 - 1.0). |
| `liveness` | `float64` | Phát hiện sự hiện diện của khán giả, bản thu trực tiếp live (thang đo 0.0 - 1.0). |
| `valence` | `float64` | Cảm xúc tích cực của âm nhạc (0.0 = buồn bã/tiêu cực, 1.0 = vui tươi/hân hoan). |
| `tempo` | `float64` | Tốc độ nhịp ước tính của ca khúc tính bằng BPM (nhịp trên phút). |
| `duration` | `float64` | Thời lượng phát của bài hát tính bằng mili-giây (milliseconds). |

---

### 1.2. `global_deaths.csv`
- **Dung lượng:** 2.05 MB | **Kích thước:** 289 dòng (thực thể/tỉnh bang), 1,144 cột.
- **Mô tả:** Số ca tử vong tích lũy do COVID-19 toàn cầu từ Đại học Johns Hopkins (JHU CSSE).

| Tên biến | Kiểu dữ liệu | Ý nghĩa và Mô tả chi tiết |
| :--- | :---: | :--- |
| `Province/State` | `object` | Tên tỉnh bang hoặc vùng lãnh thổ hải ngoại (được gộp về cấp quốc gia). |
| `Country/Region` | `object` | Tên quốc gia hoặc vùng lãnh thổ báo cáo dịch bệnh. |
| `Lat` | `float64` | Vĩ độ địa lý của trung tâm hành chính / quốc gia. |
| `Long` | `float64` | Kinh độ địa lý của trung tâm hành chính / quốc gia. |
| `1/22/20 ... 3/9/23` | `int64` | 1,140 cột ngày ghi nhận số ca tử vong tích lũy hàng ngày (chuyển sang dạng dọc). |

---

### 1.3. `gdp_data.csv`
- **Dung lượng:** 350.77 KB | **Kích thước:** 11,508 dòng, 4 cột.
- **Mô tả:** Tổng sản phẩm quốc nội (GDP danh nghĩa theo USD hiện giá) từ World Bank giai đoạn 1960–2022.

| Tên biến | Kiểu dữ liệu | Ý nghĩa và Mô tả chi tiết |
| :--- | :---: | :--- |
| `country_name` | `object` | Tên quốc gia hoặc tên nhóm khu vực kinh tế tổng hợp vĩ mô. |
| `country_code` | `object` | Mã tiêu chuẩn quốc tế ISO 3166-1 Alpha-3 của quốc gia / vùng lãnh thổ. |
| `year` | `int64` | Năm ghi nhận chỉ số GDP (từ năm 1960 đến 2022). |
| `value` | `float64` | Quy mô GDP danh nghĩa tính bằng đô la Mỹ hiện giá (USD). |

---

### 1.4. `country_codes.csv`
- **Dung lượng:** 14.16 KB | **Kích thước:** 218 dòng, 3 cột.
- **Mô tả:** Siêu dữ liệu phân loại địa lý và thu nhập quốc gia của World Bank.

| Tên biến | Kiểu dữ liệu | Ý nghĩa và Mô tả chi tiết |
| :--- | :---: | :--- |
| `country_code` | `object` | Mã tiêu chuẩn quốc tế ISO 3166-1 Alpha-3 (Khóa chính). |
| `region` | `object` | Phân loại 7 khu vực địa lý vĩ mô của World Bank (*East Asia & Pacific, Europe...*). |
| `income_group` | `object` | Phân nhóm 4 mức thu nhập kinh tế của World Bank (*High, Upper-Mid, Lower-Mid, Low*). |

---

### 1.5. `whs_years_updated.csv`
- **Dung lượng:** 241.13 KB | **Kích thước:** 1,511 dòng, 47 cột.
- **Mô tả:** Dữ liệu Báo cáo Hạnh phúc Thế giới (World Happiness Report) qua 10 ấn bản (2015–2024).

| Tên biến | Kiểu dữ liệu | Ý nghĩa và Mô tả chi tiết |
| :--- | :---: | :--- |
| `Country name` | `object` | Tên quốc gia tham gia khảo sát hạnh phúc của Gallup World Poll. |
| `year` | `int64` | Năm xuất bản báo cáo (2015 đến 2024). |
| `Ladder score / Score` | `float64` | Điểm số hạnh phúc quốc gia tổng hợp theo thang Cantril Ladder (0.0 đến 10.0). |
| `Explained by: Log GDP per capita` | `float64` | Mức đóng góp của năng lực kinh tế vào điểm số hạnh phúc. |
| `Explained by: Social support` | `float64` | Mức đóng góp của hỗ trợ xã hội và tình thân khi gặp khó khăn. |
| `Explained by: Healthy life expectancy` | `float64` | Mức đóng góp của kỳ vọng sống khỏe mạnh. |
| `Explained by: Freedom to make life choices`| `float64` | Mức đóng góp của quyền tự do lựa chọn cuộc sống. |
| `Explained by: Generosity` | `float64` | Mức đóng góp của lòng hảo tâm và hoạt động thiện nguyện. |
| `Explained by: Perceptions of corruption` | `float64` | Mức đóng góp từ niềm tin vào sự trong sạch của chính phủ và doanh nghiệp. |
| `Dystopia + residual` | `float64` | Giá trị điểm sàn Dystopia cộng với phần dư mô hình hồi quy. |

---

## 2. DỮ LIỆU SẠCH CỐT LÕI (CORE PROCESSED DATA - `data/processed/`)

### 2.1. `charts_clean.parquet` (Bảng Sự Kiện Trung Tâm - Fact Table)
- **Dung lượng:** 64.2 MB | **Kích thước:** 1,787,531 dòng, 35 cột.
- **Cấp độ hạt (Grain):** `(track_id, artist_id, chart_country, week)` duy nhất 100%.

| Tên biến | Kiểu dữ liệu | Ý nghĩa và Mô tả chi tiết |
| :--- | :---: | :--- |
| `track_id` | `object` | Mã định danh chuẩn của bài hát trên Spotify (chuỗi 22 ký tự). |
| `track_name` | `object` | Tên ca khúc (đầy đủ ký tự UTF-8). |
| `artist_id` | `object` | Mã định danh nghệ sĩ Spotify (chuỗi 22 ký tự). |
| `artist_names` | `object` | Tên các nghệ sĩ biểu diễn (nghệ sĩ chính và nghệ sĩ hợp tác). |
| `artist_individual` | `object` | Tên nghệ sĩ cá nhân độc lập tương ứng 1:1 với `artist_id` (tránh nhầm lẫn với chuỗi hợp tác). |
| `artists_num` | `int64` | Số lượng nghệ sĩ tham gia biểu diễn trong bài hát (từ 1 đến 12). |
| `artist_genre` | `category` | Thể loại âm nhạc chính của bài hát. |
| `week` | `datetime64[ns]` | Ngày bắt đầu tuần xếp hạng (100% là ngày thứ Năm hàng tuần). |
| `year` | `int32` | Năm của tuần xếp hạng (2016–2022). |
| `month` | `int32` | Tháng của tuần xếp hạng (1–12). |
| `chart_country` | `category` | Quốc gia của bảng xếp hạng (73 quốc gia và `Global`). |
| `chart_region` | `category` | Khu vực địa lý của bảng xếp hạng theo phân loại Spotify. |
| `chart_language` | `category` | Ngôn ngữ chiếm ưu thế của quốc gia xếp hạng. |
| `rank` | `int32` | Thứ hạng của bài hát trong tuần (1 đến 200). |
| `previous_rank` | `Int16` (Nullable) | Thứ hạng tuần trước (Null đại diện tự nhiên cho bài hát mới lọt bảng). |
| `is_new_entry` | `int8` | Cờ nhị phân: 1 nếu là ca khúc mới lọt bảng tuần này, 0 nếu là bài hát cũ. |
| `peak_rank` | `int32` | Thứ hạng cao nhất bài hát từng đạt được tính đến tuần này (1–200). |
| `weeks_on_chart` | `int32` | Tổng số tuần bài hát đã hiện diện trên BXH tính đến tuần này. |
| `streams` | `int64` | Tổng số lượt stream được tính điểm trong tuần xếp hạng. |
| `release_date` | `object` | Chuỗi ngày phát hành nguyên bản từ nhà sản xuất. |
| `release_date_clean` | `datetime64[ns]` | Ngày phát hành chuẩn hóa về định dạng ngày tháng chuẩn. |
| `release_year` | `int32` | Năm phát hành ca khúc. |
| `days_to_chart` | `float64` | Số ngày từ lúc phát hành đến khi lọt vào tuần bảng xếp hạng này. |
| `danceability` | `float32` | Độ phù hợp để khiêu vũ dựa trên nhịp điệu (thang đo 0.0 - 1.0). |
| `energy` | `float32` | Cường độ năng lượng, độ ồn và tốc độ âm thanh (thang đo 0.0 - 1.0). |
| `key` | `int8` | Cung nốt nhạc cơ bản theo thang Pitch Class (0 đến 11). |
| `mode` | `int8` | Thang âm (1 = Trưởng / Major, 0 = Thứ / Minor). |
| `loudness` | `float32` | Âm lượng tổng thể bản thu tính bằng Decibel (dB, phổ biến -12 đến -3 dB). |
| `speechiness` | `float32` | Mức độ hiện diện của lời nói / đọc rap (thang đo 0.0 - 1.0). |
| `acousticness` | `float32` | Mức độ âm thanh mộc cơ học (thang đo 0.0 - 1.0). |
| `instrumentalness`| `float32` | Đo lường mức độ không có giọng hát trong bài (thang đo 0.0 - 1.0). |
| `liveness` | `float32` | Phát hiện âm thanh biểu diễn trực tiếp trước khán giả (thang đo 0.0 - 1.0). |
| `valence` | `float32` | Cảm xúc tích cực, tươi vui của âm nhạc (thang đo 0.0 - 1.0). |
| `tempo` | `float32` | Tốc độ nhịp ước tính của bài hát tính bằng BPM (nhịp/phút). |
| `duration` | `float32` | Thời lượng phát của bài hát tính bằng mili-giây (ms). |

---

### 2.2. `tracks_dimension.csv` (Bảng Chiều Bài Hát - Dimension Table)
- **Dung lượng:** 7.20 MB | **Kích thước:** 39,190 dòng, 21 cột.
- **Độ đầy đủ:** **100.0% (0 Nulls).**
- **Cấp độ hạt (Grain):** `track_id` duy nhất 100%.

| Tên biến | Kiểu dữ liệu | Ý nghĩa và Mô tả chi tiết |
| :--- | :---: | :--- |
| `track_id` | `object` | Mã định danh chuẩn của bài hát trên Spotify (Khóa chính). |
| `track_name` | `object` | Tên bài hát. |
| `artist_id` | `object` | Mã định danh nghệ sĩ biểu diễn chính. |
| `artist_names` | `object` | Danh sách tên toàn bộ nghệ sĩ tham gia. |
| `artists_num` | `int64` | Số lượng nghệ sĩ biểu diễn ca khúc. |
| `artist_genre` | `object` | Thể loại âm nhạc chính của bài hát. |
| `release_date` | `object` | Chuỗi ngày phát hành nguyên bản. |
| `release_date_clean` | `object` | Ngày phát hành ca khúc đã được chuẩn hóa. |
| `release_year` | `int64` | Năm phát hành ca khúc. |
| `danceability` | `float64` | Độ phù hợp để khiêu vũ (0.0 - 1.0). |
| `energy` | `float64` | Cường độ hoạt động, năng lượng âm thanh (0.0 - 1.0). |
| `key` | `int64` | Cung nốt nhạc cơ bản Pitch Class (0 = C, 1 = C#, ..., 11 = B). |
| `mode` | `int64` | Thang âm Trưởng/Thứ (1 = Major, 0 = Minor). |
| `loudness` | `float64` | Âm lượng tổng thể tính bằng Decibel (dB). |
| `speechiness` | `float64` | Mức độ xuất hiện của từ ngữ nói (0.0 - 1.0). |
| `acousticness` | `float64` | Mức độ âm thanh mộc (0.0 - 1.0). |
| `instrumentalness`| `float64` | Mức độ không có giọng hát (0.0 - 1.0). |
| `liveness` | `float64` | Bản thu trực tiếp có khán giả (0.0 - 1.0). |
| `valence` | `float64` | Mức độ tích cực, tươi vui của âm nhạc (0.0 - 1.0). |
| `tempo` | `float64` | Tốc độ nhịp bài hát (BPM). |
| `duration` | `float64` | Thời lượng bài hát (mili-giây). |

---

### 2.3. `country_lookup.csv` (Bảng Cầu Nối Quốc Gia - Bridge Table)
- **Dung lượng:** 6.06 KB | **Kích thước:** 73 dòng, 8 cột.
- **Độ đầy đủ:** **100.0% (0 Nulls).**
- **Cấp độ hạt (Grain):** `chart_country` duy nhất 100%.

| Tên biến | Kiểu dữ liệu | Ý nghĩa và Mô tả chi tiết |
| :--- | :---: | :--- |
| `chart_country` | `object` | Tên thị trường quốc gia trên Spotify Charts (Khóa chính). |
| `country_code` | `object` | Mã tiêu chuẩn quốc tế ISO 3166-1 Alpha-3 (đã chuẩn hóa Đài Loan `TWN`). |
| `wb_country_name` | `object` | Tên quốc gia chuẩn hóa theo World Bank sau khi ánh xạ alias. |
| `wb_region` | `object` | Phân loại 7 khu vực địa lý vĩ mô của World Bank. |
| `wb_income_group` | `object` | Phân nhóm 4 mức thu nhập kinh tế của World Bank (*High, Upper-Mid...*). |
| `chart_region` | `object` | Khu vực địa lý theo phân loại Spotify. |
| `chart_language` | `object` | Ngôn ngữ chiếm ưu thế của quốc gia xếp hạng. |
| `n_weeks` | `int64` | Số lượng tuần bảng xếp hạng quốc gia xuất hiện (tối đa 76 tuần). |

---

### 2.4. `covid_weekly_clean.csv` (Bảng Dịch Tễ COVID-19 Tuần)
- **Dung lượng:** 341 KB | **Kích thước:** 12,136 dòng, 4 cột.
- **Độ đầy đủ:** **100.0% (0 Nulls).**
- **Cấp độ hạt (Grain):** `(country, week)` duy nhất 100%.

| Tên biến | Kiểu dữ liệu | Ý nghĩa và Mô tả chi tiết |
| :--- | :---: | :--- |
| `country` | `object` | Tên quốc gia hoặc thực thể phân tích (73 quốc gia và `Global`). |
| `week` | `object` | Ngày bắt đầu tuần dịch tễ (đồng bộ 100% vào thứ Năm theo Spotify). |
| `weekly_deaths` | `float64` | Tổng số ca tử vong ghi nhận mới trong chu kỳ 7 ngày tuần đó. |
| `cumulative_deaths`| `int64` | Tổng số ca tử vong do COVID-19 tích lũy từ đầu đại dịch đến tuần đó. |

---

### 2.5. `whs_clean.csv` (Bảng Báo Cáo Hạnh Phúc Thế Giới Sạch)
- **Dung lượng:** 145 KB | **Kích thước:** 1,510 dòng, 10 cột.
- **Cấp độ hạt (Grain):** `(country, year)` duy nhất 100%.

| Tên biến | Kiểu dữ liệu | Ý nghĩa và Mô tả chi tiết |
| :--- | :---: | :--- |
| `country` | `object` | Tên quốc gia đã được chuẩn hóa theo alias Spotify Charts. |
| `year` | `int64` | Năm ấn bản Báo cáo Hạnh phúc Thế giới (2015–2024). |
| `happiness_rank` | `int64` | Thứ hạng hạnh phúc toàn cầu của quốc gia trong năm đó. |
| `happiness_score` | `float64` | Điểm số hạnh phúc quốc gia thang Cantril (0.0 đến 10.0, 100% đầy đủ). |
| `gdp_factor` | `float64` | Điểm phân rã đóng góp từ thu nhập bình quân đầu người GDP. |
| `social_support` | `float64` | Điểm phân rã đóng góp từ mạng lưới hỗ trợ xã hội. |
| `healthy_life` | `float64` | Điểm phân rã đóng góp từ tuổi thọ kỳ vọng sống khỏe mạnh. |
| `freedom` | `float64` | Điểm phân rã đóng góp từ sự tự do lựa chọn cuộc sống. |
| `generosity` | `float64` | Điểm phân rã đóng góp từ lòng rộng lượng, thiện nguyện. |
| `corruption` | `float64` | Điểm phân rã đóng góp từ mức độ kiểm soát tham nhũng. |

---

## 3. DỮ LIỆU DATA MARTS (DASHBOARD & MACHINE LEARNING)

### 3.1. `mart_audio_trend_weekly.parquet` (Dashboard 1 & 3)
- **Dung lượng:** 1.08 MB | **Kích thước:** 5,548 dòng, 29 cột | **Độ đầy đủ: 100% (0 Nulls).**
- **Cấp độ hạt (Grain):** `(chart_country, week)`.

| Tên biến | Kiểu dữ liệu | Ý nghĩa và Mô tả chi tiết |
| :--- | :---: | :--- |
| `chart_country` | `object` | Tên quốc gia hoặc thị trường xếp hạng (`Global` hoặc 73 quốc gia). |
| `week` | `datetime64[ns]` | Ngày bắt đầu tuần xếp hạng (thứ Năm). |
| `total_streams` | `int64` | Tổng số lượt streams của toàn bộ bảng xếp hạng trong tuần đó. |
| `track_count` | `int64` | Số lượng vị trí ca khúc hợp lệ trong tuần (chuẩn 200 vị trí). |
| `new_entries` | `int64` | Số lượng ca khúc mới lọt vào bảng xếp hạng trong tuần (`is_new_entry == 1`). |
| `danceability_mean` | `float32` | Trung bình cộng đều (Unweighted) độ khiêu vũ của Top 200 bài hát. |
| `danceability_weighted` | `float64` | Trung bình có trọng số lượt nghe (Streams-Weighted) độ khiêu vũ. |
| `energy_mean` | `float32` | Trung bình cộng đều năng lượng của Top 200 bài hát. |
| `energy_weighted` | `float64` | Trung bình có trọng số lượt nghe năng lượng âm thanh. |
| `key_mean` | `float32` | Trung bình cộng nốt nhạc chủ âm Pitch Class. |
| `key_weighted` | `float64` | Trung bình có trọng số lượt nghe nốt nhạc chủ âm. |
| `mode_mean` | `float32` | Tỷ lệ bài hát cung Trưởng (Major mode ratio) trong tuần. |
| `mode_weighted` | `float64` | Tỷ lệ bài hát cung Trưởng có trọng số lượt nghe. |
| `loudness_mean` | `float32` | Âm lượng trung bình cộng đều (Decibel). |
| `loudness_weighted`| `float64` | Âm lượng trung bình có trọng số lượt nghe (Decibel). |
| `speechiness_mean` | `float32` | Trung bình cộng độ nói/rap của Top 200 bài hát. |
| `speechiness_weighted`| `float64` | Trung bình có trọng số lượt nghe độ nói/rap. |
| `acousticness_mean`| `float32` | Trung bình cộng độ mộc âm thanh của Top 200 bài hát. |
| `acousticness_weighted`| `float64` | Trung bình có trọng số lượt nghe độ mộc âm thanh. |
| `instrumentalness_mean`| `float32` | Trung bình cộng độ không lời của Top 200 bài hát. |
| `instrumentalness_weighted`| `float64` | Trung bình có trọng số lượt nghe độ không lời. |
| `liveness_mean` | `float32` | Trung bình cộng tỷ lệ bản thu trực tiếp. |
| `liveness_weighted`| `float64` | Trung bình có trọng số lượt nghe bản thu trực tiếp. |
| `valence_mean` | `float32` | Trung bình cộng cảm xúc tích cực (chỉ số tâm trạng sản xuất âm nhạc). |
| `valence_weighted` | `float64` | Trung bình có trọng số lượt nghe cảm xúc tích cực (thị hiếu nghe thực tế). |
| `tempo_mean` | `float32` | Nhịp độ trung bình cộng đều của bài hát (BPM). |
| `tempo_weighted` | `float64` | Nhịp độ trung bình có trọng số lượt nghe (BPM). |
| `duration_mean` | `float32` | Thời lượng phát trung bình cộng đều (mili-giây). |
| `duration_weighted`| `float64` | Thời lượng phát trung bình có trọng số lượt nghe (mili-giây). |

---

### 3.2. `mart_artist_chart.parquet` (Dashboard 1 - Xếp Hạng Nghệ Sĩ)
- **Dung lượng:** 820 KB | **Kích thước:** 15,254 dòng, 10 cột | **Độ đầy đủ: 100% (0 Nulls).**
- **Cấp độ hạt (Grain):** `artist_id` duy nhất 100%.
- **Ghi chú nghiệp vụ:** Tên nghệ sĩ được trích xuất từ `artist_individual` (100% tên nghệ sĩ độc lập cá nhân, triệt tiêu lỗi chuỗi hợp tác). Lượt streams và thành tích được phân tách độc lập giữa bảng xếp hạng `Global` và 73 bảng xếp hạng quốc gia (`Country`) để tránh hiện tượng cộng dồn hai lần (double-counting). Lượt streams của các ca khúc hợp tác được quy gán cho từng nghệ sĩ tham gia và mang tính định danh theo nghệ sĩ (không cộng dồn qua lại giữa các nghệ sĩ).

| Tên biến | Kiểu dữ liệu | Ý nghĩa và Mô tả chi tiết |
| :--- | :---: | :--- |
| `artist_id` | `object` | Mã định danh chuẩn của nghệ sĩ trên Spotify (Khóa chính). |
| `artist_name` | `object` | Tên nghệ sĩ biểu diễn độc lập cá nhân từ `artist_individual` (100% đầy đủ, không còn chuỗi collab). |
| `artist_genre` | `object` | Thể loại âm nhạc chính của nghệ sĩ (100% đầy đủ). |
| `n_chart_tracks` | `int64` | Tổng số lượng ca khúc độc nhất của nghệ sĩ từng lọt vào Top 200 trên toàn bộ các thị trường. |
| `global_streams` | `int64` | Tổng số lượt streams tích lũy của nghệ sĩ trên bảng xếp hạng Global (0 nếu chưa lọt BXH Global). |
| `country_streams` | `int64` | Tổng số lượt streams tích lũy của nghệ sĩ trên 73 bảng xếp hạng quốc gia (0 nếu chỉ lọt BXH Global). |
| `global_peak_rank` | `int64` | Thứ hạng cao nhất mà nghệ sĩ từng đạt được trên bảng xếp hạng Global (-1 nếu chưa lọt BXH Global). |
| `country_peak_rank` | `int64` | Thứ hạng cao nhất mà nghệ sĩ từng đạt được trên bất kỳ bảng xếp hạng quốc gia nào (-1 nếu chỉ lọt Global). |
| `global_weeks_on_chart` | `int64` | Tổng số tuần nghệ sĩ có tác phẩm xuất hiện trên bảng xếp hạng Global. |
| `country_weeks_on_chart` | `int64` | Tổng số tuần nghệ sĩ có tác phẩm xuất hiện trên các bảng xếp hạng quốc gia. |

---

### 3.3. `mart_country_year.parquet` (Dashboard 2 - Hạnh Phúc & Âm Nhạc)
- **Dung lượng:** 63 KB | **Kích thước:** 141 dòng, 42 cột | **Độ đầy đủ: 100% (0 Nulls).**
- **Cấp độ hạt (Grain):** `(chart_country, year)` — Khớp trọn vẹn 141 cặp quốc gia - năm của Spotify (2021 và 2022).

| Tên biến | Kiểu dữ liệu | Ý nghĩa và Mô tả chi tiết |
| :--- | :---: | :--- |
| `chart_country` | `object` | Tên quốc gia trên bảng xếp hạng Spotify. |
| `year` | `int64` | Năm phân tích (2021 hoặc 2022). |
| `yearly_streams` | `int64` | Tổng lượt streams toàn bộ các ca khúc của quốc gia trong cả năm. |
| `slot_count` | `int64` | Tổng số vị trí xếp hạng tuần được ghi nhận trong năm. |
| `n_weeks` | `int64` | Số tuần xếp hạng có dữ liệu của quốc gia trong năm đó. |
| `danceability_mean / _weighted` | `float64` | Mức độ khiêu vũ trung bình năm (Unweighted và Streams-Weighted). |
| `energy_mean / _weighted` | `float64` | Mức năng lượng trung bình năm (Unweighted và Streams-Weighted). |
| `key_mean / _weighted` | `float64` | Cung nốt nhạc trung bình năm (Unweighted và Streams-Weighted). |
| `mode_mean / _weighted` | `float64` | Tỷ lệ bài hát cung Trưởng trung bình năm (Unweighted và Streams-Weighted). |
| `loudness_mean / _weighted` | `float64` | Âm lượng Decibel trung bình năm (Unweighted và Streams-Weighted). |
| `speechiness_mean / _weighted` | `float64` | Mức độ lời nói/rap trung bình năm (Unweighted và Streams-Weighted). |
| `acousticness_mean / _weighted`| `float64` | Mức độ âm thanh mộc trung bình năm (Unweighted và Streams-Weighted). |
| `instrumentalness_mean / _weighted`| `float64` | Mức độ không lời trung bình năm (Unweighted và Streams-Weighted). |
| `liveness_mean / _weighted` | `float64` | Tỷ lệ bản thu trực tiếp live trung bình năm (Unweighted và Streams-Weighted). |
| `valence_mean / _weighted` | `float64` | Mức độ tích cực, tươi vui trung bình năm (Unweighted và Streams-Weighted). |
| `tempo_mean / _weighted` | `float64` | Tốc độ nhịp BPM trung bình năm (Unweighted và Streams-Weighted). |
| `duration_mean / _weighted` | `float64` | Thời lượng bài hát trung bình năm (Unweighted và Streams-Weighted). |
| `country_code` | `object` | Mã ISO 3166-1 Alpha-3 của quốc gia. |
| `wb_region` | `object` | Phân loại khu vực địa lý World Bank (7 vùng). |
| `wb_income_group` | `object` | Nhóm thu nhập kinh tế World Bank (4 nhóm). |
| `chart_region` | `object` | Khu vực địa lý của Spotify. |
| `chart_language` | `object` | Ngôn ngữ chiếm ưu thế của quốc gia. |
| `happiness_rank` | `int64` | Thứ hạng hạnh phúc toàn cầu trong ấn bản Báo cáo Hạnh phúc Thế giới năm đó. |
| `happiness_score` | `float64` | Điểm số hạnh phúc quốc gia thang Cantril (0.0 đến 10.0). |
| `gdp_factor` | `float64` | Điểm đóng góp từ kinh tế GDP bình quân đầu người. |
| `social_support` | `float64` | Điểm đóng góp từ mạng lưới an sinh xã hội. |
| `healthy_life` | `float64` | Điểm đóng góp từ kỳ vọng sống khỏe mạnh. |
| `freedom` | `float64` | Điểm đóng góp từ quyền tự do lựa chọn cuộc sống. |
| `generosity` | `float64` | Điểm đóng góp từ lòng rộng lượng, thiện nguyện. |
| `corruption` | `float64` | Điểm đóng góp từ mức độ kiểm soát tham nhũng. |

---

### 3.4. `ml_tracks.parquet` & `ml_tracks.csv` (Dashboard 4 & Machine Learning)
- **Dung lượng:** 4.07 MB (Parquet) / 9.06 MB (CSV) | **Kích thước:** 39,190 dòng, 30 cột.
- **Độ đầy đủ:** **100.0% (Nulls = 0 trên toàn bộ 30 cột).**
- **Cấp độ hạt (Grain):** `track_id` duy nhất 100%.

| Tên biến | Kiểu dữ liệu | Vai trò trong ML | Ý nghĩa và Mô tả chi tiết |
| :--- | :---: | :---: | :--- |
| `track_id` | `object` | Khóa chính | Mã định danh Spotify của bài hát (22 ký tự). |
| `track_name` | `object` | Metadata | Tên tác phẩm âm nhạc. |
| `artist_id` | `object` | Metadata | Mã định danh nghệ sĩ biểu diễn chính. |
| `artist_names` | `object` | Metadata | Danh sách tên toàn bộ nghệ sĩ tham gia. |
| `artists_num` | `int64` | **Đặc trưng ($X$)** | Số lượng nghệ sĩ biểu diễn (phân biệt đơn ca hay hợp tác collab). |
| `artist_genre` | `object` | **Đặc trưng ($X$)** | Thể loại âm nhạc chính của bài hát. |
| `release_date` | `object` | Metadata | Chuỗi ngày phát hành nguyên bản. |
| `release_date_clean` | `object` | Metadata | Ngày phát hành đã chuẩn hóa định dạng ngày. |
| `release_year` | `int64` | **Đặc trưng ($X$)** | Năm phát hành ca khúc. |
| `release_month` | `int64` | **Đặc trưng ($X$)** | Tháng phát hành ca khúc (1–12, phản ánh tính mùa vụ âm nhạc). |
| `danceability` | `float64` | **Đặc trưng ($X$)** | Độ phù hợp để khiêu vũ (thang 0.0 - 1.0). |
| `energy` | `float64` | **Đặc trưng ($X$)** | Cường độ năng lượng âm thanh (thang 0.0 - 1.0). |
| `key` | `int64` | **Đặc trưng ($X$)** | Cung nốt nhạc cơ bản Pitch Class (0 đến 11). |
| `mode` | `int64` | **Đặc trưng ($X$)** | Thang âm Trưởng hoặc Thứ (1 = Major, 0 = Minor). |
| `loudness` | `float64` | **Đặc trưng ($X$)** | Âm lượng tổng thể Decibel (dB). |
| `speechiness` | `float64` | **Đặc trưng ($X$)** | Mức độ lời nói / đọc rap (thang 0.0 - 1.0). |
| `acousticness` | `float64` | **Đặc trưng ($X$)** | Mức độ âm thanh mộc cơ học (thang 0.0 - 1.0). |
| `instrumentalness`| `float64` | **Đặc trưng ($X$)** | Mức độ không có giọng hát (thang 0.0 - 1.0). |
| `liveness` | `float64` | **Đặc trưng ($X$)** | Bản thu trực tiếp có khán giả (thang 0.0 - 1.0). |
| `valence` | `float64` | **Đặc trưng ($X$)** | Cảm xúc tích cực, tươi vui (thang 0.0 - 1.0). |
| `tempo` | `float64` | **Đặc trưng ($X$)** | Tốc độ nhịp bài hát tính bằng BPM. |
| `duration` | `float64` | **Đặc trưng ($X$)** | Thời lượng bài hát tính bằng mili-giây. |
| `pop_score` | `float64` | **Mục tiêu ($Y_{\text{reg}}$)** | Điểm số phổ biến tổng hợp liên tục (thang 0.0 - 100.0) cho mô hình Hồi quy. |
| `is_hit` | `int32` | **Mục tiêu ($Y_{\text{clf}}$)** | Nhãn nhị phân ca khúc Hit cân bằng (1 nếu pop_score $\ge 50$, chiếm 13.94%). |
| `is_mega_hit` | `int32` | Mục tiêu phụ | Nhãn nhị phân hiện tượng toàn cầu (1 nếu pop_score $\ge 70$, chiếm 1.59%). |
| `hit_tier` | `object` | Mục tiêu phụ | Phân hạng 4 mức: *Niche (0-25), Moderate (25-50), Popular (50-75), Mega Hit (75-100)*. |
| `peak_rank` | `int32` | **Hậu nghiệm (CẤM)** | Thứ hạng cao nhất bài hát từng đạt được (chỉ dùng kiểm chứng/giải thích). |
| `nweek` | `int64` | **Hậu nghiệm (CẤM)** | Tổng số tuần bài hát trụ lại trên BXH (chỉ dùng kiểm chứng/giải thích). |
| `total_streams` | `int64` | **Hậu nghiệm (CẤM)** | Tổng lượt stream tích lũy toàn cầu (chỉ dùng kiểm chứng/giải thích). |
| `n_countries` | `int64` | **Hậu nghiệm (CẤM)** | Số quốc gia bài hát lọt vào BXH (chỉ dùng kiểm chứng/giải thích). |

---

## 4. BẢNG KHÓA GHÉP NỐI & QUAN HỆ THỰC THỂ

| Bảng nguồn A | Bảng đích B | Khóa ghép nối | Kiểu quan hệ | Tỷ lệ khớp thực tế | Mục đích nghiệp vụ |
| :--- | :--- | :--- | :---: | :---: | :--- |
| `charts_clean` | `tracks_dimension` | `track_id` | N : 1 | **100.0%** (39,190 / 39,190) | Tra cứu 12 chỉ số âm học nội tại và thuộc tính phát hành của bài hát |
| `charts_clean` | `country_lookup` | `chart_country` | N : 1 | **100.0%** (73 / 73 quốc gia) | Bổ sung khu vực địa lý `wb_region` và nhóm thu nhập World Bank |
| `country_lookup` | `whs_clean` | `chart_country = country` | 1 : N | **100.0%** (73 / 73 quốc gia) | Ghép nối dữ liệu hạnh phúc qua 6 alias tên nước chuẩn hóa |
| `country_lookup` | `covid_weekly_clean` | `chart_country = country` | 1 : N | **100.0%** (74 / 74 thực thể) | Ghép nối số ca tử vong COVID-19 (bao gồm cả Global) |
| `mart_audio_trend_weekly` | `covid_weekly_clean` | `(chart_country = country, week)` | 1 : 1 | **100.0%** (trong kỳ dịch) | Đo lường biến động âm nhạc theo các đợt bùng phát dịch bệnh |
| `mart_country_year` | `whs_clean` | `(chart_country = country, year)` | 1 : 1 | **100.0%** (141 / 141 cặp) | Đo lường tương quan giữa điểm số hạnh phúc và gu thưởng thức âm nhạc |
| `tracks_dimension` | `ml_tracks` | `track_id` | 1 : 1 | **100.0%** (39,190 / 39,190) | Cung cấp đầu vào đặc trưng âm học cho mô hình Machine Learning |

---

## 5. CHÚ THÍCH NGHIỆP VỤ & KỸ THUẬT CHUYÊN SÂU

> [!NOTE]
> Phần chú thích này cung cấp nền tảng toán học, cơ sở lý thuyết âm nhạc và các ràng buộc dữ liệu thực tế giúp đảm bảo độ chuẩn xác khi xây dựng biểu đồ trực quan và mô hình hóa.

### 5.1. Chú thích 12 Đặc Trưng Âm Học Spotify
Spotify sử dụng các thuật toán phân tích tín hiệu âm thanh kỹ thuật số (Echo Nest Audio Engine) để tính toán 12 chỉ số nội tại cho từng bài hát:

| Biến âm học | Thang đo | Ý nghĩa âm nhạc & cảm xúc | Phân phối & Lưu ý |
| :--- | :--- | :--- | :--- |
| `danceability` | `[0.0, 1.0]` | Độ phù hợp để khiêu vũ dựa trên nhịp điệu, độ ổn định của phách và sức mạnh tổng thể. | Phân phối chuẩn, trung bình ~0.65 trên BXH. |
| `energy` | `[0.0, 1.0]` | Cường độ hoạt động, tốc độ và độ ồn (nhạc Rock/EDM có energy cao, cổ điển thấp). | Trung bình ~0.65–0.70. |
| `valence` | `[0.0, 1.0]` | **Tâm trạng tích cực của âm nhạc.** Điểm cao = vui vẻ, hân hoan, yêu đời; điểm thấp = u sầu, buồn bã, giận dữ. | **Chỉ số vàng** đo lường cảm xúc xã hội trong thời kỳ COVID-19. |
| `acousticness` | `[0.0, 1.0]` | Mức độ âm thanh mộc (nhạc cụ cơ học, không khuếch đại điện tử). | Lệch phải (phần lớn bài hát hiện đại có acousticness < 0.25). |
| `instrumentalness` | `[0.0, 1.0]` | Đo lường bài hát không có giọng hát (lời nói/tiếng hát càng ít, giá trị càng tiệm cận 1.0). | Phần lớn bài hát trên BXH có giá trị tiệm cận 0.0 (nhạc có lời). |
| `liveness` | `[0.0, 1.0]` | Phát hiện sự hiện diện của khán giả trong bản thu (thu âm biểu diễn trực tiếp / live). | Giá trị > 0.8 biểu thị bản thu live. |
| `speechiness` | `[0.0, 1.0]` | Mức độ xuất hiện của từ ngữ nói (Podcast, Rap có giá trị cao; Pop thường < 0.1). | Phân phối lệch phải mạnh. |
| `loudness` | `[-60.0, 0.0]` dB | Âm lượng tổng thể tính bằng Decibel (dB). | Giá trị phổ biến từ -10 dB đến -3 dB (nhạc được master to). |
| `tempo` | `BPM (nhịp/phút)` | Tốc độ nhịp ước tính của bài hát. | Phổ biến trong khoảng 90–140 BPM. |
| `duration` | `Milliseconds` | Thời lượng bài hát tính bằng mili-giây. | Trung bình khoảng 180,000–220,000 ms (3–3.5 phút). |
| `key` | `Int8 [0, 11]` | Cung nốt nhạc cơ bản theo chuẩn Pitch Class (0 = C, 1 = C#, 2 = D, ..., 11 = B). | Biến định danh (Categorical / One-Hot). |
| `mode` | `Int8 {0, 1}` | Thang âm Trưởng (`Major = 1`) hoặc Thứ (`Minor = 0`). | Nhạc điệu Thứ thường buồn hơn, Trưởng tươi sáng hơn. |

---

### 5.2. Chú thích Công Thức Tính `pop_score` & Cân Bằng Nhãn ML
Do dữ liệu bảng xếp hạng không có sẵn một chỉ số duy nhất đo lường thành công toàn diện của bài hát, `pop_score` được xây dựng bằng cách kết hợp 4 khía cạnh:

$$\text{pop\_score} = \left( 0.30 \times s_{\text{rank}} + 0.25 \times s_{\text{weeks}} + 0.20 \times s_{\text{countries}} + 0.25 \times s_{\text{streams}} \right) \times 100$$

1. **Thứ hạng đỉnh cao ($s_{\text{rank}}$ - Trọng số 30%):**
   $$s_{\text{rank}} = 1 - \frac{\text{peak\_rank} - 1}{199}$$
   Ca khúc đạt vị trí #1 nhận điểm số 1.0; ca khúc chạm rank #200 nhận điểm số 0.0.
2. **Sức bền trên BXH ($s_{\text{weeks}}$ - Trọng số 25%):**
   $$s_{\text{weeks}} = \frac{\min(\text{nweek}, Q_{0.99})}{Q_{0.99}}$$
   Được cắt trần (cap) tại percentile 99% để triệt tiêu ảnh hưởng của các ngoại lai cực đoan (như các ca khúc trụ bảng hơn 100 tuần kéo giãn phân bố).
3. **Độ phủ quốc tế ($s_{\text{countries}}$ - Trọng số 20%):**
   $$s_{\text{countries}} = \frac{\text{n\_countries}}{73}$$
   Số quốc gia độc lập ca khúc xuất hiện (chỉ đếm 73 quốc gia thực tế, loại trừ Global), chia cho tối đa 73.
4. **Quy mô người nghe ($s_{\text{streams}}$ - Trọng số 25%):**
   $$s_{\text{streams}} = \frac{\log(1 + \text{total\_streams}) - \min(\log)}{\max(\log) - \min(\log)}$$
   Áp dụng biến đổi Logarit trước khi chuẩn hóa Min-Max để đưa phân bố lượt nghe (vốn lệch phải cực nặng theo luật lũy thừa - Power Law) về phân bố đối xứng cân bằng.

* **Chiến lược cân bằng nhãn mục tiêu trong Machine Learning:**
  * **Nhãn `is_hit` ($\ge 50$ điểm):** Chiếm **13.94%** (5,463 bài hát), tương ứng các ca khúc thuộc nhóm Popular và Mega Hit. Tỷ lệ này tạo độ cân bằng tốt cho mô hình Logistic Regression (không bị mất cân bằng cực đoan 1.5%).
  * **Nhãn `is_mega_hit` ($\ge 70$ điểm):** Chiếm **1.59%** (625 bài hát), dành cho bài toán phát hiện ngoại lệ hiện tượng toàn cầu.
  * **Phân loại 4 mức (`hit_tier`):**
    * `[0, 25]`: **Niche** (35.0% - 13,716 bài).
    * `(25, 50]`: **Moderate** (51.1% - 20,011 bài).
    * `(50, 75]`: **Popular** (13.0% - 5,102 bài).
    * `(75, 100]`: **Mega Hit** (0.9% - 361 bài).

---

### 5.3. Chú thích Phòng Chống Rò Rỉ Dữ Liệu (Data Leakage)
> [!CAUTION]
> **Ranh giới sống còn trong Machine Learning**:
> * **Biến mục tiêu ($Y$):** `pop_score`, `is_hit`, `is_mega_hit`, `hit_tier`.
> * **Biến hậu nghiệm (Post-hoc metrics):** `peak_rank`, `nweek`, `total_streams`, `n_countries`, `rank`, `previous_rank`, `weeks_on_chart`.
> * **CẤM TUYỆT ĐỐI** đưa các biến hậu nghiệm vào tập $X$. Nếu một mô hình được cung cấp `total_streams` hay `peak_rank` để dự đoán `pop_score`, mô hình sẽ đạt $R^2 = 1.0$ giả tạo nhưng hoàn toàn vô giá trị trong ứng dụng thực tế.
> * **Tập $X$ chuẩn xác:** Chỉ gồm những thông tin đã biết trước/tại thời điểm phát hành (12 Audio Features, số lượng nghệ sĩ hợp tác `artists_num`, thể loại nhạc `artist_genre`, năm phát hành `release_year`, tháng phát hành `release_month`).

---

### 5.4. Chú thích Bước Nhảy Thang Đo Báo Cáo Hạnh Phúc WHS
* **Vấn đề phát hiện:** Khi phân tích 6 nhân tố phân rã của Báo cáo Hạnh phúc Thế giới (`gdp_factor`, `social_support`, `healthy_life`, `freedom`, `generosity`, `corruption`), số liệu cho thấy các bước nhảy bất thường:
  * `gdp_factor` nhảy từ **0.977** (2021) lên **1.410** (2022) do WHR cập nhật phương trình baseline Dystopia.
  * `social_support` nhảy từ **1.156** (2020) xuống **0.793** (2021).
  * `healthy_life` thay đổi từ số năm tuổi thọ sang điểm Cantril phân rã.
* **Hướng dẫn phân tích:**
  * **Dashboard 2 bắt buộc sử dụng `happiness_score`** (thang Cantril Ladder 0–10) làm biến tương quan chính qua các năm, vì điểm số khảo sát từ Gallup hoàn toàn nhất quán.
  * Nếu phân tích 6 nhân tố thành phần, chỉ thực hiện so sánh cắt ngang trong từng năm riêng biệt hoặc chuẩn hóa Z-score theo từng năm trước khi so sánh liên thời gian.

---

### 5.5. Chú thích Đồng Bộ Thời Gian COVID-19 & Số Ca Tử Vong Âm
1. **Chu kỳ tuần thứ Năm:** Spotify chốt dữ liệu Top 200 vào thứ Năm hàng tuần. Do đó, dữ liệu COVID-19 được gom nhóm từ thứ Sáu tuần trước đến thứ Năm tuần này để đảm bảo đồng pha thời gian 100%.
2. **160 tuần Global trước dịch:** Giai đoạn từ `2017-01-05` đến `2020-01-23` là giai đoạn chuẩn đối chứng (Baseline). Toàn bộ 160 dòng `left_only` khi ghép nối bảng xếp hạng với COVID đều thuộc thị trường Global trước khi đại dịch bùng phát.
3. **33 tuần có số ca tử vong âm:** Trong dữ liệu Johns Hopkins CSSE, có 33 dòng ghi nhận `weekly_deaths < 0` tại các quốc gia như Bỉ, Áo, Andorra... Đây không phải lỗi code mà là do cơ quan y tế các nước này tiến hành **điều chỉnh hồi tố (retrospective revision)** số liệu tử vong bị thống kê dư thừa trong các tuần trước đó.

---

### 5.6. Chú thích Về Hiện Tượng Collab & Hai Dòng Mismatch Bodø Domkor
* **Hệ số nhân Collab 1.61:** Trong dữ liệu bảng xếp hạng, một bài hát có nhiều nghệ sĩ biểu diễn sẽ có số dòng đúng bằng số lượng nghệ sĩ (`group_size == artists_num`).
* **Trường hợp ngoại lệ duy nhất (2 dòng mismatch):** Ca khúc *"Ja, Vi Elsker Dette Landet"* (ID: `0GEeVI8Wa1KXGTStgBUerG`) xuất hiện tại 2 tuần `2021-05-20` và `2022-05-19` trên BXH Na Uy. Chuỗi nghệ sĩ gốc là `'N/A, Bodø Domkor'` (`artists_num = 2`), nhưng nghệ sĩ thứ nhất bị khuyết mã ID hợp lệ nên chỉ có 1 dòng đại diện cho dàn hợp xướng Bodø Domkor (`group_size = 1`). Việc kiểm tra xác nhận 100% các bài hát còn lại đều khớp tuyệt đối với số lượng nghệ sĩ tham gia.
