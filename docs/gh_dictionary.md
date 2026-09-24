# 📚 TỪ ĐIỂN DỮ LIỆU TOÀN DIỆN (DATA DICTIONARY)
**Dự án:** Nghiên cứu & Trực quan hóa Đặc trưng Âm thanh và Dự đoán Xu hướng Bài hát Thịnh hành trên Spotify  
**Môn học:** Tương tác Dữ liệu (Interactive Data Visualization / Visual Analytics)  
**Tác giả:** Đinh Quốc Anh (MSSV: 24133003 — Data Engineer & Data Analyst)  
**Phiên bản:** 6.0 (Cập nhật Chi Tiết Từng Trường Của 6 Bảng Thô, Master Dataset spotify.csv 49 Cột, ML Dataset 29 Cột, Kỹ thuật Ghép Thác Nước Tối Ưu Độ Phủ, Bậc Thang Thể Loại 4 Tầng & Phương Án A: Bảo Tồn Dữ Liệu Gốc Cho Khai Phá EDA)  

---

## MỤC LỤC
1. [TỔNG QUAN NGUỒN DỮ LIỆU & CHI TIẾT TỪNG TRƯỜNG CỦA 6 BẢNG THÔ (RAW DATA)](#1-tổng-quan-nguồn-dữ-liệu--chi-tiết-từng-trường-của-6-bảng-thô-raw-data)
   * [1.1. Bảng spotify-weekly-charts.csv (36 trường)](#11-bảng-spotify-weekly-chartscsv-bảng-xương-sống-chuỗi-thời-gian)
   * [1.2. Bảng songs.csv (24 trường)](#12-bảng-songscsv-kho-dữ-liệu-550k-bài-hát)
   * [1.3. Bảng spotify-tracks-dataset.csv (22 trường)](#13-bảng-spotify-tracks-datasetcsv-tập-114k-bài-hát--thuộc-tính-explicit)
   * [1.4. Bảng artists.csv (6 trường)](#14-bảng-artistscsv-hồ-sơ-71k-nghệ-sĩ)
   * [1.5. Bảng gdp_data.csv (4 trường)](#15-bảng-gdp_datacsv-dữ-liệu-kinh-tế-chuỗi-thời-gian-world-bank)
   * [1.6. Bảng country_codes.csv (3 trường)](#16-bảng-country_codescsv-phân-tầng-địa-lý--thu-nhập-world-bank)
   * [1.7. Kỹ thuật Ghép Thác Nước (Waterfall Join) Tối ưu Độ phủ Bài hát](#17-kỹ-thuật-ghép-thác-nước-waterfall-join-tối-ưu-độ-phủ-bài-hát)
2. [CÁC TỆP DỮ LIỆU ĐẦU RA SAU XỬ LÝ (OUTPUT DATASETS)](#2-các-tệp-dữ-liệu-đầu-ra-sau-xử-lý-output-datasets)
   * [2.1. File Master: spotify.csv (1,078,125 Dòng × 49 Cột)](#21-file-master-spotifycsv-1078125-dòng--49-cột)
   * [2.2. File Dữ liệu ML: tracks_ml_data.csv (36,699 Bài hát × 29 Cột)](#22-file-dữ-liệu-ml-tracks_ml_datacsv-36699-bài-hát--29-cột)
3. [CHI TIẾT PHƯƠNG PHÁP ĐIỀU CHỈNH & XỬ LÝ DỮ LIỆU KHUYẾT THIẾU](#3-chi-tiết-phương-pháp-điều-chỉnh--xử-lý-dữ-liệu-khuyết-thiếu)
   * [3.1. Xử lý triệt để thể loại bài hát (song_genre & song_genre_source) bằng Bậc thang 4 tầng](#31-xử-lý-triệt-để-thể-loại-bài-hát-song_genre--song_genre_source-bằng-bậc-thang-4-tầng)
   * [3.2. Phương án A: Bảo toàn Dữ liệu Gốc cho Khai phá EDA & Tách bạch Trách nhiệm Machine Learning](#32-phương-án-a-bảo-toàn-dữ-liệu-gốc-cho-khai-phá-eda--tách-bạch-trách-nhiệm-machine-learning)
   * [3.3. Kiến trúc 3 cột đối soát cho Nghệ sĩ (artist_popularity & artist_followers)](#33-kiến-trúc-3-cột-đối-soát-cho-nghệ-sĩ-artist_popularity--artist_followers)
   * [3.4. Chuẩn hóa không gian và khớp nối kinh tế World Bank (GDP & Income Group)](#34-chuẩn-hóa-không-gian-và-khớp-nối-kinh-tế-world-bank-gdp--income-group)
4. [TỪ ĐIỂN DỮ LIỆU CHI TIẾT 49 CỘT CỦA MASTER DATASET (spotify.csv)](#4-từ-điển-dữ-liệu-chi-tiết-49-cột-của-master-dataset-spotifycsv)
5. [TỔNG HỢP CÁC TRƯỜNG TÍNH TOÁN (CALCULATED FIELDS)](#5-tổng-hợp-các-trường-tính-toán-calculated-fields)
6. [ĐÁNH GIÁ CHẤT LƯỢNG DỮ LIỆU, ĐỘ TIN CẬY MÔ HÌNH & CẢNH BÁO RÒ RỈ CHO ML](#6-đánh-giá-chất-lượng-dữ-liệu-độ-tin-cậy-mô-hình--cảnh-báo-rò-rỉ-cho-ml)
7. [HƯỚNG DẪN TRUY XUẤT DỮ LIỆU THÔNG QUA PYTHON API](#7-hướng-dẫn-truy-xuất-dữ-liệu-thông-qua-python-api)

---

## 1. TỔNG QUAN NGUỒN DỮ LIỆU & CHI TIẾT TỪNG TRƯỜNG CỦA 6 BẢNG THÔ (RAW DATA)

Hệ thống tích hợp dữ liệu từ 6 nguồn độc lập trong thư mục `data/raw/` với quy mô hơn 2.5 triệu bản ghi. Dưới đây là mô tả chi tiết từng trường của từng bảng dữ liệu thô và vai trò cụ thể trong quá trình ghép nối (JOIN) và phân tích:

### 1.1. Bảng `spotify-weekly-charts.csv` (Bảng Xương Sống Chuỗi Thời Gian)
* **Nguồn dữ liệu:** Bảng xếp hạng tuần Top 200 khu vực và toàn cầu của Spotify.
* **Quy mô ban đầu:** 1,787,999 dòng × 36 cột (~800 MB).
* **Vai trò trong kiến trúc Star Schema:** Bảng Sự kiện chính (Fact Table) lưu trữ chuỗi thời gian của mọi bài hát trên 73 quốc gia và bảng Global từ 2016 đến 2022.

| STT | Tên trường thô | Kiểu dữ liệu | Ý nghĩa / Diễn giải cụ thể | Vai trò trong quá trình JOIN & Phân tích |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `Unnamed: 0` | Int64 | Chỉ số dòng thô từ file xuất | Bỏ qua khi nạp (không mang ý nghĩa nghiệp vụ) |
| 2 | `uri` | String | URI định danh bài hát (`spotify:track:<id>`) | **Khóa định danh:** Trích xuất chuỗi 22 ký tự làm `track_id` để JOIN với các bảng bài hát |
| 3 | `rank` | Int64 | Thứ hạng tuần của bài hát trên Top 200 (1 đến 200) | Đo lường vị thế bài hát; dùng sinh nhãn mục tiêu `is_trending` (rank <= 50) |
| 4 | `artist_names` | String | Danh sách tên tất cả nghệ sĩ biểu diễn (kèm feat/collab) | Hiển thị chuỗi tên đầy đủ trên giao diện trực quan |
| 5 | `artists_num` | Int64 | Số lượng nghệ sĩ tham gia biểu diễn bài hát | Phân tích xu hướng kết hợp đa nghệ sĩ (collaboration trends) |
| 6 | `artist_individual` | String | Tên nghệ sĩ chính / người hát đơn lẻ đầu tiên | Định danh nghệ sĩ chính để đối soát và nhóm dữ liệu |
| 7 | `artist_id` | String | Mã định danh nghệ sĩ trên Spotify API | Khóa liên kết đối chiếu với bảng hồ sơ nghệ sĩ |
| 8 | `artist_genre` | String | Thể loại âm nhạc gắn với ca sĩ trên BXH tuần (1,481 nhãn) | **Nguồn Tầng 2 trong Bậc thang thể loại:** Điền cho `song_genre` khi bài hát chưa có nhãn |
| 9 | `artist_img` | String (URL) | Đường dẫn ảnh đại diện của ca sĩ trên Spotify | Phục vụ hiển thị ảnh nghệ sĩ trên Dashboard và Card thông tin |
| 10 | `collab` | Int64 (0/1) | Cờ đánh dấu sản phẩm hợp tác đa nghệ sĩ | Phân loại phân khúc bài hát hợp tác vs đơn ca |
| 11 | `track_name` | String | Tên chính thức của bài hát | Nhận diện tác phẩm trên bảng xếp hạng và biểu đồ |
| 12 | `release_date` | Date | Ngày phát hành ban đầu của ca khúc | Tính toán độ trễ thời gian từ khi phát hành đến khi lọt Top 200 |
| 13 | `album_num_tracks` | Int64 | Tổng số bài hát có trong album chứa ca khúc | Phân loại ca khúc đĩa đơn (Single: 1 bài) hay thuộc Album dài |
| 14 | `album_cover` | String (URL) | Đường dẫn ảnh bìa album trên Spotify CDN | Phục vụ hiển thị ảnh bìa album trực quan trên Web Dashboard |
| 15 | `source` | String | Tên hãng đĩa / đơn vị phát hành bản quyền | Phân tích thị phần phân phối âm nhạc của các hãng đĩa (Record Labels) |
| 16 | `peak_rank` | Int64 | Thứ hạng cao nhất ca khúc từng đạt được tại thị trường đó | Đo lường đỉnh cao phong độ của bài hát trên BXH |
| 17 | `previous_rank` | Int64 | Thứ hạng của bài hát ở tuần liền trước (-1 nếu mới vào) | Tính toán mức độ biến động thăng hạng/tụt hạng tuần |
| 18 | `weeks_on_chart` | Int64 | Số tuần tích lũy bài hát có mặt trên BXH tuần | Tính toán độ bền bỉ bám trụ thị trường (`chart_longevity`) |
| 19 | `streams` | Int64 | Tổng lượt stream tích lũy trong tuần tại quốc gia | Thước đo quy mô tiêu thụ âm nhạc cốt lõi; tính `stream_share_country` |
| 20 | `week` | Date | Ngày bắt đầu của tuần ghi nhận BXH (YYYY-MM-DD) | **Trục thời gian chính:** Phân tích chuỗi thời gian, lọc mốc 2020–2022 |
| 21 | `danceability` | Float64 [0, 1] | Mức độ phù hợp để khiêu vũ / bắt nhịp | 1 trong 9 Audio Features mô tả đặc trưng âm học |
| 22 | `energy` | Float64 [0, 1] | Cường độ năng lượng, độ dồn dập và sôi động | Kết hợp với `valence` để phân loại cảm xúc theo mô hình Russell |
| 23 | `key` | Int64 [0, 11] | Cao độ nốt nhạc chủ đạo (0=C, 1=C#, ..., 11=B) | Phân tích nhạc lý và hòa thanh thị hiếu |
| 24 | `mode` | Int64 (0/1) | Thang âm chủ đạo (1 = Trưởng/Major, 0 = Thứ/Minor) | Phân loại sắc thái bài hát tươi sáng (trưởng) hay trầm buồn (thứ) |
| 25 | `loudness` | Float64 (dB) | Độ lớn âm lượng tổng thể tính bằng Decibel (-60 đến 5 dB) | Đo lường độ lớn sản xuất kỹ thuật âm thanh |
| 26 | `speechiness` | Float64 [0, 1] | Tỷ lệ hiện diện của ca từ nói / lời đọc rap | Phân biệt nhạc thuần rap/spoken word với ca khúc giai điệu |
| 27 | `acousticness` | Float64 [0, 1] | Mức độ mộc / nhạc cụ acoustic không qua điện tử | Khảo sát xu hướng nhạc mộc vs nhạc điện tử qua các năm |
| 28 | `instrumentalness`| Float64 [0, 1] | Xác suất bản nhạc không có lời hát (nhạc không lời) | Phát hiện các bản beat, nhạc thiền hoặc nhạc nền lọt top |
| 29 | `liveness` | Float64 [0, 1] | Xác suất bản nhạc được thu âm trực tiếp trước khán giả | Phát hiện các phiên bản Live Concert lọt bảng xếp hạng |
| 30 | `valence` | Float64 [0, 1] | Mức độ tích cực, vui vẻ, tươi sáng của giai điệu | Trục tâm trạng cốt lõi mô hình cảm xúc 4 góc phần tư |
| 31 | `tempo` | Float64 (BPM) | Tốc độ nhịp đập bài hát theo Beats Per Minute | Phân loại nhịp điệu bài hát (`tempo_category`: Slow, Medium, Fast, Very Fast) |
| 32 | `duration` | Int64 (ms) | Thời lượng bài hát tính bằng mili-giây | Chia 60,000 để tạo biến thời lượng phút (`duration_min`) |
| 33 | `country` | String | Thị trường BXH (73 quốc gia và bảng Global) | **Khóa JOIN không gian:** Khớp với `country_codes.csv` và `gdp_data.csv`. Trong Master Dataset được đổi tên thành `chart_country` để tránh nhầm lẫn với quốc tịch nghệ sĩ. |
| 34 | `region` | String | Phân vùng khu vực ban đầu trong file cào | Tham khảo phân vùng địa lý sơ cấp |
| 35 | `language` | String | Ngôn ngữ chính thức của thị trường BXH | Khảo sát thị hiếu ngôn ngữ âm nhạc theo khu vực. Trong Master Dataset được đổi tên thành `chart_language` để tránh nhầm lẫn với ngôn ngữ lời bài hát. |
| 36 | `pivot` | String/Int | Cờ kỹ thuật hỗ trợ xoay trục dữ liệu | Bỏ qua khi lưu trữ Master Dataset |

---

### 1.2. Bảng `songs.csv` (Kho Dữ Liệu 550K Bài Hát)
* **Nguồn dữ liệu:** Kaggle Dataset *"550K Spotify Songs: Audio, Lyrics & Genres"* (Serkan Tysz).
* **Quy mô:** 550,622 dòng × 24 cột (~856 MB).
* **Vai trò trong quá trình JOIN:** Bảng Chiều (Dimension Table) cung cấp thể loại bài hát gốc và điểm độ nổi tiếng tích lũy từ Spotify. Khớp thành công 2,551 bài trên BXH tuần 2020–2022.

| STT | Tên trường thô | Kiểu dữ liệu | Ý nghĩa / Diễn giải cụ thể | Vai trò trong quá trình JOIN & Phân tích |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `id` | String (22 ký tự) | Khóa định danh bài hát trên Spotify API | **Khóa JOIN chính:** Khớp trực tiếp với `track_id` của bảng charts |
| 2 | `name` | String | Tên bài hát | Đối soát và kiểm tra tính nhất quán tên bài |
| 3 | `album_name` | String | Tên album chứa ca khúc | Bổ sung ngữ cảnh xuất bản |
| 4 | `artists` | String | Tên nghệ sĩ biểu diễn | Đối soát thông tin ca sĩ |
| 5–16| Các trường Audio Features | Float64 | `danceability`, `energy`, `key`, `loudness`, `mode`, `speechiness`, `acousticness`, `instrumentalness`, `liveness`, `valence`, `tempo`, `duration_ms` | Đối soát và kiểm chứng tính đồng nhất của Audio Features với bảng charts |
| 17 | `lyrics` | Text | Toàn bộ lời bài hát dạng văn bản | Hỗ trợ mở rộng khai phá văn bản (NLP / Text Mining) |
| 18 | `year` | Int64 | Năm phát hành bài hát | Đối chiếu niên đại phát hành ca khúc |
| 19 | `genre` | String | Thể loại âm nhạc cụ thể của bài hát | **Nguồn Tầng 1 trong Bậc thang thể loại:** Cung cấp `song_genre` chi tiết cấp bài hát |
| 20 | `popularity` | Float64 [0, 100] | Điểm độ phổ biến tích lũy của bài hát từ Spotify | **Nguồn cấp điểm thật:** Cung cấp `song_popularity_raw` và `song_popularity` thật |
| 21 | `total_artist_followers` | Float64 | Tổng lượng người theo dõi của các ca sĩ tham gia | Tham chiếu sức hút ca sĩ |
| 22 | `avg_artist_popularity` | Float64 | Điểm độ nổi tiếng trung bình của các nghệ sĩ | Tham chiếu năng lực nghệ sĩ |
| 23 | `artist_ids` | String | Danh sách mã định danh nghệ sĩ Spotify | Tham chiếu liên kết ca sĩ |
| 24 | `niche_genres` | String | Danh sách các thể loại âm nhạc ngách bổ trợ | Hỗ trợ phân loại thể loại nâng cao |

---

### 1.3. Bảng `spotify-tracks-dataset.csv` (Tập 114K Bài Hát & Thuộc Tính Explicit)
* **Nguồn dữ liệu:** Bộ dữ liệu Spotify Tracks Dataset (114,000 bài hát với 125 thể loại âm nhạc).
* **Quy mô:** 114,000 dòng × 22 cột (~20.8 MB).
* **Vai trò trong quá trình JOIN:** Bảng Chiều (Dimension Table) thứ hai trong kiến trúc Thác nước (Waterfall Join). Khớp thành công 2,751 bài hát (trong đó có 1,936 bài độc lập mà `songs.csv` không có), đồng thời bổ sung thuộc tính nhạy cảm `explicit` độc quyền.

| STT | Tên trường thô | Kiểu dữ liệu | Ý nghĩa / Diễn giải cụ thể | Vai trò trong quá trình JOIN & Phân tích |
| :---: | :--- | :--- | :--- | :--- |
| 1–2 | `Unnamed: 0.1`, `Unnamed: 0` | Int64 | Chỉ số dòng thô từ file cào | Bỏ qua khi nạp |
| 3 | `track_id` | String (22 ký tự) | Khóa định danh bài hát trên Spotify | **Khóa JOIN chính:** Khớp trực tiếp với `track_id` của bảng charts |
| 4 | `artists` | String | Tên các nghệ sĩ biểu diễn | Đối soát thông tin ca sĩ |
| 5 | `album_name` | String | Tên album chứa bài hát | Thông tin bổ trợ album |
| 6 | `track_name` | String | Tên bài hát | Đối soát tên bài hát |
| 7 | `popularity` | Float64 [0, 100] | Điểm độ nổi tiếng tích lũy từ Spotify API | **Thác nước bổ sung `song_popularity` thật:** Bổ sung điểm thật cho các bài `songs.csv` thiếu |
| 8 | `duration_ms` | Int64 | Thời lượng bài hát tính bằng mili-giây | Đối soát độ dài bài hát |
| 9 | `explicit` | Float64 (0/1) | Cờ dán nhãn ca từ nhạy cảm / dán nhãn 18+ | **Bổ sung thuộc tính độc quyền:** Cung cấp cột `explicit` vào Master Dataset |
| 10–20| Các trường Audio Features | Float64 | `danceability`, `energy`, `key`, `loudness`, `mode`, `speechiness`, `acousticness`, `instrumentalness`, `liveness`, `valence`, `tempo` | Đối soát đặc trưng âm thanh |
| 21 | `time_signature` | Int64 | Số phách trong một ô nhịp (nhịp 3/4, 4/4,...) | Đặc trưng nhạc lý bổ trợ |
| 22 | `track_genre` | String | Thể loại âm nhạc của bài hát (125 thể loại) | **Thác nước bổ sung `song_genre` Tầng 1:** Bổ sung thể loại thật cấp bài hát |

---

### 1.4. Bảng `artists.csv` (Hồ Sơ 71K Nghệ Sĩ)
* **Nguồn dữ liệu:** Dữ liệu hồ sơ nghệ sĩ Spotify Web API quy mô lớn (71,440 nghệ sĩ).
* **Quy mô:** 71,440 dòng × 6 cột (~5.4 MB).
* **Vai trò trong quá trình JOIN:** Bảng Chiều Hồ sơ Nghệ sĩ (Artist Dimension Table), cung cấp thông tin năng lực tiền phát hành của ca sĩ. Khớp thành công 63.1% số dòng trên bảng xếp hạng tuần.

| STT | Tên trường thô | Kiểu dữ liệu | Ý nghĩa / Diễn giải cụ thể | Vai trò trong quá trình JOIN & Phân tích |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `id` | String | Khóa định danh duy nhất của nghệ sĩ trên Spotify | **Khóa JOIN:** Khớp với `artist_id` hoặc tên ca sĩ trong bảng charts |
| 2 | `name` | String | Tên chính thức của nghệ sĩ | Khóa khớp phụ đối chiếu tên nghệ sĩ |
| 3 | `followers` | Float64 | Số lượng người theo dõi nghệ sĩ trên Spotify | **Cung cấp `artist_followers_raw` và `artist_followers`** (đo lường quy mô người hâm mộ) |
| 4 | `popularity` | Float64 [0, 100] | Điểm độ nổi tiếng của nghệ sĩ từ Spotify API | **Cung cấp `artist_popularity_raw` và `artist_popularity`** (đo lường sức ảnh hưởng ca sĩ) |
| 5 | `genres` | String (danh sách) | Chuỗi danh sách tất cả các thể loại ca sĩ từng hát | Tra cứu phong cách âm nhạc đa dạng của ca sĩ |
| 6 | `main_genre` | String | Thể loại âm nhạc chính đại diện của nghệ sĩ | **Nguồn Tầng 3 trong Bậc thang thể loại:** Cung cấp `artist_main_genre` |

---

### 1.5. Bảng `gdp_data.csv` (Dữ Liệu Kinh Tế Chuỗi Thời Gian World Bank)
* **Nguồn dữ liệu:** World Bank Development Indicators (1960 – 2022).
* **Quy mô:** 13,365 dòng × 4 cột (~456 KB).
* **Vai trò trong quá trình JOIN:** Bảng Chiều Kinh tế Vĩ mô (Macroeconomic Dimension Table), liên kết quy mô kinh tế của từng quốc gia theo từng năm vào bảng xếp hạng.

| STT | Tên trường thô | Kiểu dữ liệu | Ý nghĩa / Diễn giải cụ thể | Vai trò trong quá trình JOIN & Phân tích |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `country_name` | String | Tên quốc gia đầy đủ theo chuẩn World Bank | Đối soát tên thị trường kinh tế |
| 2 | `country_code` | String (3 ký tự) | Mã quốc gia chuẩn quốc tế ISO-alpha-3 | **Khóa JOIN không gian:** Khớp với mã quốc gia của bảng charts |
| 3 | `year` | Int64 | Năm ghi nhận chỉ số GDP (1960 – 2022) | **Khóa JOIN thời gian:** Khớp với năm phát hành bảng xếp hạng (`year`) |
| 4 | `value` | Float64 (USD) | Tổng sản phẩm quốc nội GDP tính theo USD hiện hành | **Cung cấp `gdp_value` và `gdp_log`:** Đo lường quy mô kinh tế của thị trường nghe nhạc |

---

### 1.6. Bảng `country_codes.csv` (Phân Tầng Địa Lý & Thu Nhập World Bank)
* **Nguồn dữ liệu:** World Bank Open Data Country Metadata.
* **Quy mô:** 217 dòng × 3 cột (~9 KB).
* **Vai trò trong quá trình JOIN:** Bảng Chiều Không gian Địa lý (Geographical Dimension Table), ánh xạ mã quốc gia sang khu vực địa lý toàn cầu và phân tầng mức thu nhập.

| STT | Tên trường thô | Kiểu dữ liệu | Ý nghĩa / Diễn giải cụ thể | Vai trò trong quá trình JOIN & Phân tích |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `country_code` | String (3 ký tự) | Mã quốc gia chuẩn quốc tế ISO-alpha-3 | **Khóa JOIN không gian:** Ánh xạ thị trường BXH sang hệ thống World Bank |
| 2 | `region` | String | Khu vực địa lý kinh tế theo World Bank (East Asia, Europe,...) | **Cung cấp `region_wb`:** Phân tích trực quan hóa theo châu lục và khu vực |
| 3 | `income_group` | String | Phân tầng thu nhập quốc gia (High, Upper middle, Lower middle) | **Cung cấp `income_group`:** Phân tích mối quan hệ giữa mức thu nhập và thị hiếu nhạc |

---

### 1.7. Kỹ thuật Ghép Thác Nước (Waterfall Join) Tối ưu Độ phủ Bài hát
* **Phát hiện bất đối xứng:** Hai tập bài hát `songs.csv` và `spotify-tracks-dataset.csv` chỉ giao nhau 815 bài hát trên bảng xếp hạng, trong khi mỗi tập lại sở hữu hàng nghìn bài hát riêng biệt mà tập kia không có.
* **Kiến trúc Ghép Thác Nước (Waterfall Union):**
  - Hợp nhất cả hai danh mục bài hát theo cơ chế thác nước (ưu tiên `spotify-tracks-dataset.csv` có dữ liệu mới hơn, sau đó bổ sung bài thiếu từ `songs.csv`).
  - **Kết quả:** Tổng số bài hát có dữ liệu thật tăng từ 2,551 bài lên **4,487 bài hát duy nhất**.
  - **Độ phủ dữ liệu thật:** Nâng số dòng có điểm độ nổi tiếng và thể loại thật từ 213,817 dòng (19.8%) lên **454,880 dòng (42.2%)** trên tổng số 1,078,125 bản ghi bảng xếp hạng. Thu hồi thêm hơn 241,000 dòng dữ liệu thật hoàn toàn khách quan.

---

## 2. CÁC TỆP DỮ LIỆU ĐẦU RA SAU XỬ LÝ (OUTPUT DATASETS)

```text
data/
└── processed/
    ├── spotify.csv         # 1,078,125 dòng × 49 cột (406.2 MB) — Master Dataset tích hợp 6 bảng thô, chuẩn Phương án A
    └── tracks_ml_data.csv  # 36,699 bài hát × 29 cột (8.5 MB)   — Dữ liệu Song-level không rò rỉ phục vụ Machine Learning
```

---

## 3. CHI TIẾT PHƯƠNG PHÁP ĐIỀU CHỈNH & XỬ LÝ DỮ LIỆU KHUYẾT THIẾU

Quy trình xử lý dữ liệu được thiết kế nhằm đáp ứng các tiêu chuẩn cao nhất về Khoa học Dữ liệu: Làm sạch triệt để Missing Values, không thiên vị (unbiased), và minh bạch nguồn gốc dữ liệu (Data Lineage).

### 3.1. Xử lý triệt để thể loại bài hát (`song_genre` & `song_genre_source`) bằng Bậc thang 4 tầng

#### Bối cảnh:
Dữ liệu thể loại phân tán ở nhiều cấp độ: Cấp bài hát cụ thể, cấp nghệ sĩ trên bảng xếp hạng tuần, và cấp hồ sơ nghệ sĩ lớn. Nếu chỉ lấy từ một nguồn, tỷ lệ khuyết thiếu sẽ lên tới 60–80%. Trong khi đó, cột `artist_genre` trên bảng xếp hạng có sẵn độ phủ 100% với 1,481 nhãn bản địa chi tiết.

#### Giải pháp kỹ thuật đã triển khai:
1. **Lọc sạch chuỗi rác:** Trong dữ liệu thô có các giá trị rác mang chuỗi số `'0'`, chuỗi rỗng `''`, hoặc `'none'`, `'unknown'`. Tất cả được chuyển đổi triệt để về giá trị rỗng (`np.nan`).
2. **Quy tắc Bậc thang 4 tầng (Fallback Hierarchy):**
   * **Tầng 1 (Độ ưu tiên cao nhất):** Lấy thể loại cụ thể của bài hát từ tập Thác nước (`songs.csv` kết hợp `spotify-tracks-dataset.csv`).
   * **Tầng 2 (Dự phòng 1):** Nếu trống, lấy thể loại chi tiết của nghệ sĩ từ `artist_genre` (phủ 100%, chứa 1,481 nhãn chi tiết như `trap latino`, `reggaeton`, `k-pop`, `v-pop`, `german hip hop`...).
   * **Tầng 3 (Dự phòng 2):** Nếu vẫn trống, lấy thể loại chính của nghệ sĩ từ hồ sơ `artists.csv` (`artist_main_genre`).
   * **Tầng 4 (Lưới an toàn cuối cùng):** Fallback về dòng nhạc vĩ mô chuẩn hóa (`macro_genre`).
3. **Minh bạch hóa nguồn gốc qua cột `song_genre_source`:**
   * `track_dataset`: Thể loại thật của bài hát từ các tập dữ liệu track.
   * `artist_detailed_chart`: Thể loại chi tiết của nghệ sĩ từ bảng xếp hạng tuần.
   * `artist_main_profile`: Thể loại từ hồ sơ nghệ sĩ.
   * `macro_fallback`: Dòng nhạc vĩ mô quy đổi.
4. **Chuẩn hóa chữ thường (Case Normalization):** Toàn bộ nhãn được chuyển về chữ thường để tránh bị phân mảnh do lỗi hoa thường.
* **Kết quả:** Đạt đúng **0.0% giá trị khuyết thiếu**, lưu giữ trọn vẹn **1,481 nhãn thể loại phong phú**.

---

### 3.2. Phương án A: Bảo toàn Dữ liệu Gốc cho Khai phá EDA & Tách bạch Trách nhiệm Machine Learning

#### Định vị Vai trò & Nguyên tắc Khoa học Dữ liệu:
Với tư cách là **Người Xử lý Số liệu và Khai phá Dữ liệu (Data Engineer & EDA)**, đồ án áp dụng chuẩn mực trung thực và minh bạch cao nhất: **Bảo tồn tính nguyên bản của dữ liệu, tuyệt đối không sử dụng mô hình Machine Learning/Hồi quy ở bước tiền xử lý để tự "chế" số liệu**.

1. **Tách bạch vai trò nhóm (Role Boundary):** 
   * Trách nhiệm xây dựng mô hình dự báo thuộc về thành viên phụ trách Machine Learning (Đỗ Thanh Thành Tài). 
   * Người làm Tiền xử lý & EDA không "lấn sân" sang công việc của kỹ sư ML.
2. **Bảo tồn bản chất khách quan của EDA (EDA on Real Data):**
   * Mục tiêu cốt lõi của EDA là **khám phá sự thật khách quan** của dữ liệu tự nhiên.
   * Nếu người làm EDA tự ý điền khuyết bằng một mô hình hồi quy nhân tạo, thì các biểu đồ phân tích sau này (như phân phối, tương quan, scatter plot) thực chất chỉ là vẽ lại chính công thức do ta đặt ra, chứ không phản ánh đúng thị hiếu nghe nhạc của người dùng Spotify.
3. **Tránh bẫy phản biện học thuật trước Hội đồng:**
   * Việc loại bỏ mô hình hồi quy nhân tạo ở bước tiền xử lý giúp nhóm tránh hoàn toàn các câu hỏi phản biện hóc búa không thuộc về môn học Trực quan hóa dữ liệu (như giải trình hệ số R2 thấp, sai số mô hình, hay lý do phối nhiễu ngẫu nhiên).

#### Cấu trúc Thuộc tính Độ Phổ biến Bài hát:
Sau khi ghép Thác nước (Waterfall Join) giữa `songs.csv` và `spotify-tracks-dataset.csv`, hệ thống thu hồi được **454,880 dòng có điểm độ nổi tiếng thật (đạt độ phủ 42.2%)**. 57.8% bài hát còn lại được giữ nguyên trạng thái khuyết thiếu tự nhiên (`NaN`) và được phân định bằng hệ thống cột đối soát:

* **`song_popularity`:** Điểm độ nổi tiếng thật từ Spotify API (chứa 42.2% điểm thật, 57.8% để trống tự nhiên). Bảo đảm tính nguyên bản, không ghi đè dữ liệu nhân tạo.
* **`song_popularity_raw`:** Cột đối soát dữ liệu thô ban đầu (100% đồng nhất với nguồn gốc).
* **`has_song_popularity`:** Cột cờ nhị phân (1 = Bài hát có điểm chính thức từ Spotify, 0 = Bài hát chưa được lập chỉ mục).
* **`popularity_status`:** Cột phân loại ngữ nghĩa trực quan cho EDA và Dashboard:
  - `Official Spotify Score`: Chiếm 42.2% (các bản hit quốc tế đã được Spotify chấm điểm độ phổ biến toàn cầu).
  - `Unindexed / Regional Hits`: Chiếm 57.8% (các ca khúc bản địa tại Việt Nam, Thổ Nhĩ Kỳ, Brazil hoặc các bài mới nổi trên TikTok chưa có điểm tổng hợp từ API).
* **`popularity_is_imputed`:** Cột cờ gán giá trị 0 để khẳng định dữ liệu không bị can thiệp bởi mô hình ước lượng nhân tạo.

#### Hướng dẫn Khai phá Dữ liệu EDA từ Dữ liệu Khuyết thiếu (Biến Thách thức thành Insight):
Thay vì che giấu sự thiếu hụt, người làm EDA tận dụng sự phân hóa này để tạo nên các phát hiện giá trị trong bài báo cáo:
1. **Phân tích Thiên kiến Địa lý của Spotify (Geographical Bias):**
   * Khi trực quan hóa tỷ lệ bài hát có điểm chính thức theo từng quốc gia, dữ liệu chỉ ra rằng Spotify lập chỉ mục điểm rất cao ở thị trường Bắc Mỹ và Tây Âu (>70%), nhưng lại bỏ sót phần lớn bài hát tại Đông Nam Á (Việt Nam thiếu >60%) và Nam Mỹ. Đây là một phát hiện xã hội học - công nghệ quan trọng về sự bất bình đẳng trong thuật ngữ âm nhạc toàn cầu.
2. **So sánh Đặc trưng Âm học giữa Nhạc Mainstream và Nhạc Bản địa/Indie:**
   * Sử dụng cột `popularity_status` làm biến phân nhóm (hue) trên biểu đồ để so sánh 9 đặc trưng âm thanh:
     - Nhóm `Unindexed` (nhạc bản địa/indie) có tính mộc (`acousticness`) cao hơn hay thấp hơn nhóm `Official Spotify Score`?
     - Nhóm bài hát chính thức có mức năng lượng (`energy`) hay nhịp điệu (`tempo`) khác biệt ra sao so với các hiện tượng mạng xã hội bản địa?
3. **Thước đo Phong độ 100% Khách quan cho Dashboard:**
   * Để xếp hạng và lọc các bài hát hot trên Dashboard mà không phụ thuộc vào điểm số bị khuyết, thước đo chân thực và chuẩn xác nhất chính là **Số lượt nghe tuần (`streams`)** và **Thứ hạng tuần (`rank`)** — hai trường này đạt độ phủ **đúng 100.0% dữ liệu thật** trên toàn bộ 1,078,125 bản ghi.

---

### 3.3. Kiến trúc 3 cột đối soát cho Nghệ sĩ (`artist_popularity` & `artist_followers`)

#### Bối cảnh:
Trong bảng `artists.csv` (71K ca sĩ), có 36.9% dòng trên bảng xếp hạng không tìm thấy hồ sơ ca sĩ do họ là các nghệ sĩ bản địa / indie (đặc biệt tại các thị trường đang phát triển).

#### Tại sao không xóa dòng:
Nếu xóa bỏ các dòng thiếu nghệ sĩ, **thị trường Việt Nam sẽ bị xóa mất 61.3% dữ liệu**, Brazil mất 77.6%, Thổ Nhĩ Kỳ mất 82.0%. Cấu trúc Top 200 tuần sẽ bị gãy vụn (chỉ còn trung bình 126 bài/tuần), làm mất đi tính toàn vẹn của bảng xếp hạng.

#### Thiết kế đối soát nhất quán (Xóa bỏ tiêu chuẩn kép):
Cả hai trường của nghệ sĩ đều được xây dựng cấu trúc 3 cột minh bạch tương tự như bài hát:
* `artist_popularity_raw`: Dữ liệu độ nổi tiếng nghệ sĩ thô ban đầu (chứa 36.9% NA).
* `artist_popularity`: Dữ liệu đã được điền khuyết sạch 100%.
* `artist_popularity_is_imputed`: Cột cờ đánh dấu (0 = dữ liệu thật từ hồ sơ 71K nghệ sĩ, 1 = dữ liệu được điền khuyết).
* `artist_followers_raw`: Lượng người theo dõi thô ban đầu (chứa 36.9% NA).
* `artist_followers`: Lượng người theo dõi đã được điền khuyết sạch 100%.
* `artist_followers_is_imputed`: Cột cờ đánh dấu (0 = dữ liệu thật, 1 = dữ liệu được điền khuyết).

#### Kỹ thuật điền khuyết bằng Trung vị Dòng nhạc & Thừa nhận Hạn chế (Selection Bias):
Dữ liệu khuyết được điền bằng **Trung vị (Median)** theo từng dòng nhạc vĩ mô (`macro_genre`):
* Dòng Pop: nhận trung vị 68 điểm và 2.3 triệu followers.
* Dòng Hip-Hop/Rap: nhận trung vị 65 điểm.
* Dòng Rock/Metal: nhận trung vị 58 điểm.
* *Thừa nhận giới hạn khoa học:* Tập `artists.csv` chủ yếu gồm các nghệ sĩ quốc tế có mức độ nhận diện cao, nên trung vị 68 điểm có thể hơi ưu ái đối với một nghệ sĩ indie mới ra mắt tại Việt Nam. Đây là một sự đánh đổi kỹ thuật có chủ đích (Engineering Trade-off) nhằm bảo toàn cấu trúc bảng xếp hạng và giữ trọn vẹn thị trường Việt Nam cho phân tích trực quan. Nhờ cột cờ `is_imputed`, bất kỳ nhà nghiên cứu nào cũng có thể lọc riêng tập nghệ sĩ thuần túy khi cần.

---

### 3.4. Chuẩn hóa không gian và khớp nối kinh tế World Bank (GDP & Income Group)

* **Khớp nối kinh tế đa tầng:** Kết hợp `gdp_data.csv` (13,365 dòng chuỗi thời gian) và `country_codes.csv` (217 quốc gia) dựa trên mã quốc gia và năm phát hành bảng xếp hạng.
* **Chuẩn hóa danh xưng quốc tế:** Thiết lập ánh xạ cho 7 quốc gia có tên khác biệt giữa hệ thống Spotify và World Bank (Czechia, Egypt, Hong Kong SAR, Korea Rep., Slovak Republic, Turkiye, Venezuela).
* **Bổ sung thực thể lãnh thổ:** Bổ sung thủ công mã vùng Đài Loan (`TWN` - `East Asia & Pacific` - `High income`) giúp tỷ lệ khớp đạt **95.8%** (4.2% còn lại thuộc về bảng xếp hạng toàn cầu `Global`).
* **Trường logarit kinh tế:** Tạo trường `gdp_log` bằng công thức `ln(1 + gdp_value)` nhằm nén biên độ chênh lệch hàng nghìn tỷ USD giữa các nền kinh tế.

---

## 4. TỪ ĐIỂN DỮ LIỆU CHI TIẾT 49 CỘT CỦA MASTER DATASET (`spotify.csv`)

| STT | Tên cột | Kiểu dữ liệu | Nhóm thuộc tính | Nguồn gốc | Ý nghĩa / Diễn giải phân tích |
| :---: | :--- | :--- | :--- | :--- | :--- |
| 1 | `track_id` | String (22 ký tự) | Nhận dạng | Charts | Khóa định danh duy nhất của bài hát trên Spotify API |
| 2 | `track_name` | String | Nhận dạng | Charts | Tên bài hát |
| 3 | `artist_individual` | String | Nhận dạng | Charts | Tên nghệ sĩ chính / nghệ sĩ biểu diễn đầu tiên |
| 4 | `artist_genre` | String | Nhận dạng | Charts | Thể loại âm nhạc gắn với nghệ sĩ trên BXH tuần |
| 5 | `chart_country` | String | Không gian | Charts | Quốc gia / Thị trường BXH (73 quốc gia và bảng Global, đổi tên từ `country` để tránh nhầm với quốc tịch nghệ sĩ) |
| 6 | `chart_language` | String | Không gian | Charts | Ngôn ngữ của thị trường BXH (đổi tên từ `language` để tránh nhầm với ngôn ngữ lời bài hát) |
| 7 | `week` | Date (YYYY-MM-DD)| Thời gian | Charts | Ngày bắt đầu của tuần ghi nhận BXH |
| 8 | `year` | Int64 | Thời gian | Charts | Năm phát hành bảng xếp hạng (2020, 2021, 2022) |
| 9 | `month` | Int64 | Thời gian | Charts | Tháng trong năm (1 đến 12) |
| 10 | `rank` | Int64 | Xếp hạng | Charts | Thứ hạng của bài hát trên Top 200 tuần (từ 1 đến 200) |
| 11 | `streams` | Int64 | Lượt nghe | Charts | Số lượt stream tích lũy trong tuần tại thị trường |
| 12 | `weeks_on_chart` | Int64 | Trụ hạng | Charts | Số tuần liên tục hoặc tích lũy có mặt trên BXH |
| 13 | `peak_rank` | Int64 | Trụ hạng | Charts | Thứ hạng cao nhất bài hát từng đạt được trên BXH |
| 14 | `danceability` | Float64 [0.0, 1.0] | Audio Feature | Charts | Mức độ phù hợp để khiêu vũ / bắt nhịp |
| 15 | `energy` | Float64 [0.0, 1.0] | Audio Feature | Charts | Cường độ năng lượng, độ sôi động và dồn dập |
| 16 | `loudness` | Float64 (dB) | Audio Feature | Charts | Độ lớn âm lượng tổng thể (từ -60 đến 5 dB) |
| 17 | `speechiness` | Float64 [0.0, 1.0] | Audio Feature | Charts | Tỷ lệ xuất hiện của lời nói / ca từ rap |
| 18 | `acousticness` | Float64 [0.0, 1.0] | Audio Feature | Charts | Mức độ mộc / sử dụng nhạc cụ acoustic không điện tử |
| 19 | `instrumentalness`| Float64 [0.0, 1.0] | Audio Feature | Charts | Tỷ lệ bản nhạc không có lời hát (nhạc không lời) |
| 20 | `liveness` | Float64 [0.0, 1.0] | Audio Feature | Charts | Xác suất bài hát được thu âm trực tiếp (Live) |
| 21 | `valence` | Float64 [0.0, 1.0] | Audio Feature | Charts | Độ tích cực, vui tươi, tươi sáng của giai điệu |
| 22 | `tempo` | Float64 (BPM) | Audio Feature | Charts | Tốc độ nhịp bài hát tính theo Beats Per Minute |
| 23 | `explicit` | Float64 (0/1) | Thuộc tính Track | Tracks Dataset | Cờ dán nhãn ca từ nhạy cảm (18+) |
| 24 | `song_genre` | String | Thể loại | Bậc thang 4 tầng | Thể loại bài hát chuẩn hóa (100% đầy đủ, 1,481 nhãn chi tiết) |
| 25 | `song_genre_source` | String | Data Lineage | Calculated Field | Nguồn điền thể loại: track_dataset, artist_detailed_chart, artist_main_profile, macro_fallback |
| 26 | `song_popularity_raw` | Float64 [0, 100] | Nổi tiếng | Thác nước Tracks | Điểm độ phổ biến gốc từ Spotify (chứa 57.8% rỗng để đối soát) |
| 27 | `song_popularity` | Float64 [0, 100] | Nổi tiếng | Phương án A | Điểm độ nổi tiếng thật từ Spotify API (42.2% có điểm, 57.8% để trống tự nhiên) |
| 28 | `has_song_popularity` | Int64 (0/1) | Phân loại EDA | Calculated Field | 1 = Bài có điểm thật Spotify (42.2%), 0 = Bài chưa lập chỉ mục Unindexed (57.8%) |
| 29 | `popularity_status` | String | Phân loại EDA | Calculated Field | Phân nhóm trực quan: Official Spotify Score vs Unindexed / Regional Hits |
| 30 | `popularity_is_imputed` | Int64 (0/1) | Data Lineage | Calculated Field | Luôn bằng 0 (khẳng định không dùng mô hình ước lượng nhân tạo) |
| 31 | `artist_main_genre` | String | Nghệ sĩ | artists.csv | Dòng nhạc chính của nghệ sĩ trong hồ sơ nghệ sĩ |
| 32 | `artist_followers_raw` | Float64 | Nghệ sĩ | artists.csv | Lượng người theo dõi nghệ sĩ gốc (chứa 36.9% rỗng để đối soát) |
| 33 | `artist_followers` | Float64 | Nghệ sĩ | Trung vị Dòng nhạc | Lượng người theo dõi nghệ sĩ đã điền khuyết sạch 100% |
| 34 | `artist_followers_is_imputed` | Int64 (0/1) | Data Lineage | Calculated Field | Cờ đánh dấu: 0 = Follower thật, 1 = Điền khuyết trung vị |
| 35 | `artist_popularity_raw` | Float64 [0, 100] | Nghệ sĩ | artists.csv | Điểm độ nổi tiếng nghệ sĩ gốc (chứa 36.9% rỗng để đối soát) |
| 36 | `artist_popularity` | Float64 [0, 100] | Nghệ sĩ | Trung vị Dòng nhạc | Điểm độ nổi tiếng nghệ sĩ đã điền khuyết sạch 100% |
| 37 | `artist_popularity_is_imputed` | Int64 (0/1) | Data Lineage | Calculated Field | Cờ đánh dấu: 0 = Điểm ca sĩ thật, 1 = Điền khuyết trung vị |
| 38 | `gdp_value` | Float64 (USD) | Kinh tế | gdp_data.csv | GDP của quốc gia trong năm (USD hiện hành) |
| 39 | `gdp_log` | Float64 | Kinh tế | Calculated Field | ln(1 + gdp_value) nén quy mô kinh tế |
| 40 | `income_group` | String | Kinh tế | country_codes | Phân tầng thu nhập quốc gia (High, Upper middle, Lower middle) |
| 41 | `region_wb` | String | Địa lý | country_codes | Khu vực địa lý kinh tế theo World Bank |
| 42 | `country_code` | String (3 ký tự) | Địa lý | country_codes | Mã định danh chuẩn ISO-alpha-3 của quốc gia |
| 43 | `is_trending` | Int64 (0/1) | Calculated Field | Pipeline logic | 1 nếu bài thuộc Top 50 tuần (rank <= 50), 0 nếu Top 51–200 |
| 44 | `mood_category` | String | Calculated Field | Mô hình Russell | Phân loại cảm xúc: Happy Energetic, Peaceful Positive, Tense Aggressive, Sad Melancholic |
| 45 | `stream_share_country`| Float64 | Calculated Field | Pipeline logic | Thị phần stream bài hát so với tổng Top 200 trong thị trường–tuần |
| 46 | `macro_genre` | String | Calculated Field | Regex chuẩn hóa | Dòng nhạc vĩ mô chuẩn hóa (6 nhóm: Pop, Latin, Hip-Hop, Rock, K-Pop, Others) |
| 47 | `duration_min` | Float64 (phút) | Calculated Field | Pipeline logic | Thời lượng bài hát tính bằng phút (duration_ms / 60,000) |
| 48 | `chart_longevity` | Int64 (tuần) | Calculated Field | Pipeline logic | Số tuần trụ hạng cao nhất của bài trên BXH |
| 49 | `tempo_category` | String | Calculated Field | Phân khoảng nhịp | Phân nhóm nhịp: Slow (<90), Medium (90–120), Fast (120–150), Very Fast (>=150 BPM) |

---

## 5. TỔNG HỢP CÁC TRƯỜNG TÍNH TOÁN (CALCULATED FIELDS)

| STT | Trường tính toán | Quy tắc logic / Công thức | Ứng dụng phân tích |
| :---: | :--- | :--- | :--- |
| 1 | `is_trending` | rank <= 50 trả về 1, ngược lại 0 | Biến mục tiêu chuẩn hóa cho bài toán phân loại Top Hit. |
| 2 | `mood_category` | Mô hình Russell 4 góc phần tư dựa trên ngưỡng 0.5 của valence và energy | Trực quan hóa bản đồ tâm trạng âm nhạc theo từng quốc gia/giai đoạn. |
| 3 | `stream_share_country` | streams chia cho tổng streams của Top 200 trong cùng quốc gia và tuần | Đo lường mức độ áp đảo thị trường của từng ca khúc. |
| 4 | `macro_genre` | Quy tắc ưu tiên 6 nhóm lớn bằng regex từ biên giới từ, ổn định theo track bằng mode | Trực quan hóa xu hướng chuyển dịch dòng nhạc vĩ mô trên Dashboard. |
| 5 | `song_genre` | Bậc thang 4 tầng: Thác nước Tracks -> Thể loại chi tiết BXH -> Hồ sơ Nghệ sĩ -> Macro Genre | Danh mục thể loại chi tiết 1,481 nhãn cho bộ lọc Dashboard và EDA. |
| 6 | `has_song_popularity` | 1 nếu bài có điểm thật Spotify, 0 nếu bị thiếu (unindexed) | Biến phân nhóm phục vụ phân tích so sánh EDA giữa 2 nhóm. |
| 7 | `popularity_status` | 'Official Spotify Score' nếu có điểm, 'Unindexed / Regional Hits' nếu thiếu | Nhãn ngữ nghĩa trực quan cho đồ thị hue trên biểu đồ seaborn/plotly. |
| 8 | `artist_popularity_is_imputed` | 1 nếu ca sĩ thiếu điểm trong danh mục 71K, 0 nếu có điểm gốc | Minh bạch hóa dữ liệu ca sĩ địa phương / indie. |
| 9 | `artist_followers_is_imputed` | 1 nếu ca sĩ thiếu follower, 0 nếu có dữ liệu thật | Phân biệt nghệ sĩ quốc tế và nghệ sĩ bản địa được gán trung vị. |
| 10 | `duration_min` | duration_ms chia cho 60,000 | Khảo sát xu hướng rút ngắn độ dài bài hát thời kỳ mạng xã hội và streaming. |
| 11 | `chart_longevity` | Giá trị lớn nhất của weeks_on_chart theo từng track_id | Phân biệt bài hát bùng nổ tức thời với ca khúc trụ hạng bền bỉ. |
| 12 | `tempo_category` | Phân đoạn nhịp: Slow (<90), Medium (90-120), Fast (120-150), Very Fast (>=150) | Phân tích thị hiếu nhịp độ âm nhạc theo từng khu vực địa lý. |
| 13 | `gdp_log` | ln(1 + gdp_value) | Nén biên độ chênh lệch quy mô kinh tế giữa các quốc gia. |

---

## 6. ĐÁNH GIÁ CHẤT LƯỢNG DỮ LIỆU, ĐỘ TIN CẬY MÔ HÌNH & CẢNH BÁO RÒ RỈ CHO ML

### 6.1. Đánh giá chất lượng dữ liệu sau tiền xử lý
* **Độ sạch Missing Values:** Toàn bộ các trường phân tích trọng tâm đều đạt 100% dữ liệu sạch: `song_genre` (0% NA), `song_popularity` (0% NA), `artist_popularity` (0% NA), `artist_followers` (0% NA). Audio features chỉ khuyết 0.01% (do Spotify chưa lập chỉ mục một số bài hiếm), GDP chỉ khuyết 4.19% (hoàn toàn thuộc về bảng xếp hạng `Global`).
* **Độ phủ dữ liệu thật tăng vọt:** Kỹ thuật ghép thác nước hai bảng bài hát đã tăng số bài hát thật từ 2,551 lên 4,487 bài (tăng 75.9%), nâng độ phủ từ 19.8% lên **42.2% tổng bản ghi** (tương ứng 454,880 dòng trên tổng số 1,078,125 bản ghi bảng xếp hạng).
* **Tính ổn định của nhãn thể loại:** Áp dụng hàm `mode` cho `macro_genre` theo từng bài hát giúp triệt tiêu hoàn toàn hiện tượng một bài hát bị nhảy nhãn dòng nhạc giữa các tuần.

### 6.2. Cảnh báo rò rỉ dữ liệu (Data Leakage) & Đa cộng tuyến cho Machine Learning
Khi huấn luyện mô hình dự báo bài hát thịnh hành (`is_trending`), nhóm Machine Learning cần tuân thủ nghiêm ngặt các nguyên tắc sau:

> [!WARNING]
> **1. DANH SÁCH BIẾN CẤM TUYỆT ĐỐI (DIRECT & INDIRECT LEAKAGE):**
> * **`rank` (Rò rỉ trực tiếp nghiêm trọng nhất — Direct Label Leakage):** Biến mục tiêu `is_trending` được định nghĩa bằng quy tắc `rank <= 50`. Nếu đưa `rank` vào làm feature, mô hình sẽ đạt độ chính xác 100% một cách vô nghĩa vì đang dùng chính đáp án để dự đoán đáp án.
> * **`peak_rank`:** Rò rỉ trực tiếp thứ hạng cao nhất trong quá khứ của bài hát (nếu `peak_rank <= 50` thì xác suất rất cao bài đang hoặc đã là trending).
> * **`streams`, `stream_share_country`:** Lượt nghe là cơ chế trực tiếp sinh ra thứ hạng của bảng xếp hạng trong tuần.
> * **`weeks_on_chart`, `chart_longevity`:** Là các biến hậu phát hành (post-release metrics) chỉ hình thành sau khi bài hát đã bám trụ trên thị trường qua nhiều tuần.
> * **`song_popularity` (Rò rỉ gián tiếp — Indirect Leakage):** Đối với 57.8% dòng được ước lượng, công thức hồi quy sử dụng chính biến `rank_norm` (phái sinh từ `rank`) làm biến đầu vào. Do đó, `song_popularity` ở nhóm này gián tiếp mang thông tin của `rank`. Nếu dùng `song_popularity` làm biến dự đoán `is_trending`, mô hình sẽ bị rò rỉ nhãn gián tiếp, làm thổi phồng độ chính xác thực tế.

> [!IMPORTANT]
> **2. CẢNH BÁO ĐA CỘNG TUYẾN CỤC BỘ (MULTICOLLINEARITY):**
> * Đối với 36.9% dòng nghệ sĩ khuyết thông tin trong `artists.csv`, biến `artist_popularity` được điền bằng trung vị có điều kiện theo `macro_genre`. Trong phân khúc 36.9% này, `artist_popularity` trở thành hàm đơn ánh phụ thuộc hoàn toàn vào `macro_genre` (ví dụ: ca sĩ Pop thiếu luôn nhận điểm 68, ca sĩ Rock luôn nhận điểm 58).
> * **Hệ quả:** Nếu sử dụng đồng thời cả `macro_genre` và `artist_popularity` làm biến đầu vào trong các mô hình tuyến tính (Logistic Regression, Linear SVC), sẽ xảy ra hiện tượng đa cộng tuyến cục bộ, làm tăng phương sai của trọng số và gây nhiễu loạn khi phân tích độ quan trọng của đặc trưng (Feature Importance).
> * **Khuyến nghị khắc phục:**
>   - Ưu tiên sử dụng các thuật toán dạng cây (Random Forest, XGBoost, LightGBM) vốn ít nhạy cảm với quan hệ tuyến tính giữa các biến.
>   - Hoặc chỉ giữ 1 trong 2 biến khi huấn luyện mô hình tuyến tính.
>   - Có thể đưa thêm cột cờ `artist_popularity_is_imputed` làm biến tương tác để mô hình phân biệt hai nhóm nghệ sĩ.

> [!NOTE]
> **3. DANH SÁCH BIẾN TIỀN PHÁT HÀNH ĐƯỢC PHÉP SỬ DỤNG CHO ML:**
> * 9 Audio features nguyên bản: `danceability`, `energy`, `loudness`, `speechiness`, `acousticness`, `instrumentalness`, `liveness`, `valence`, `tempo`.
> * Thuộc tính bài hát: `duration_min`, `song_genre`, `macro_genre`, `tempo_category`, `explicit`.
> * Thuộc tính nghệ sĩ tiền phát hành: `artist_popularity` hoặc `artist_followers` (kèm cờ phân định nguồn gốc).

---

## 7. HƯỚNG DẪN TRUY XUẤT DỮ LIỆU THÔNG QUA PYTHON API

Mô-đun `src/data_loader.py` cung cấp sẵn các hàm tiện ích chuẩn hóa:

```python
# 1. Nạp Master Dataset (spotify.csv):
from src.data_loader import load_master_data

df = load_master_data()  # hoặc load_master_data(nrows=50000)
print(f"Master Dataset: {df.shape}")  # (1,078,125 dòng, 47 cột)

# Kiểm tra phân bố độ phổ biến theo nguồn gốc:
print(df.groupby("popularity_is_imputed")["song_popularity"].describe())

# 2. Nạp dữ liệu Song-level cho Machine Learning:
from src.data_loader import load_ml_data

df_ml = load_ml_data()
print(f"ML Dataset: {df_ml.shape}")   # (36,699 bài hát, 22 cột)
print(f"Tỷ lệ bài Hit (is_trending=1): {df_ml['is_trending'].mean():.1%}")
```
