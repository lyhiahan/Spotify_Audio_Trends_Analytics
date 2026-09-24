# 📚 TỪ ĐIỂN DỮ LIỆU TOÀN DIỆN (DATA DICTIONARY)
**Dự án:** Nghiên cứu & Trực quan hóa Đặc trưng Âm thanh và Dự đoán Xu hướng Bài hát Thịnh hành trên Spotify  
**Môn học:** Tương tác Dữ liệu (Interactive Data Visualization / Visual Analytics)  
**Tác giả:** Lý Gia Hân (MSSV: 24133016 — Visualization Specialist & Dashboard Dev)  
**Phiên bản:** 6.2 (Cập nhật Chi Tiết Từng Trường Của 6 Bảng Thô, Master Dataset spotify.csv 44 Cột, ML Dataset 26 Cột, Chuẩn hóa tên cột chart_week/chart_year/chart_month, Tinh giản loại bỏ các cột phụ, Kỹ thuật Ghép Thác Nước Tối Ưu Độ Phủ, Bậc Thang Thể Loại 4 Tầng & Phương Án A: Bảo Tồn Dữ Liệu Gốc Cho Khai Phá EDA)  

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
   * [2.1. File Master: spotify.csv (1,078,125 Dòng × 44 Cột)](#21-file-master-spotifycsv-1078125-dòng--44-cột)
   * [2.2. File Dữ liệu ML: tracks_ml_data.csv (36,699 Bài hát × 26 Cột)](#22-file-dữ-liệu-ml-tracks_ml_datacsv-36699-bài-hát--26-cột)
3. [CHI TIẾT PHƯƠNG PHÁP ĐIỀU CHỈNH & XỬ LÝ DỮ LIỆU KHUYẾT THIẾU](#3-chi-tiết-phương-pháp-điều-chỉnh--xử-lý-dữ-liệu-khuyết-thiếu)
   * [3.1. Xử lý triệt để thể loại bài hát (song_genre & song_genre_source) bằng Bậc thang 4 tầng](#31-xử-lý-triệt-để-thể-loại-bài-hát-song_genre--song_genre_source-bằng-bậc-thang-4-tầng)
   * [3.2. Phương án A: Bảo toàn Dữ liệu Gốc cho Khai phá EDA & Tách bạch Trách nhiệm Machine Learning](#32-phương-án-a-bảo-toàn-dữ-liệu-gốc-cho-khai-phá-eda--tách-bạch-trách-nhiệm-machine-learning)
   * [3.3. Xử lý dữ liệu Nghệ sĩ (artist_popularity & artist_followers_raw)](#33-xử-lý-dữ-liệu-nghệ-sĩ-artist_popularity--artist_followers_raw)
   * [3.4. Chuẩn hóa không gian và khớp nối kinh tế World Bank (GDP & Income Group)](#34-chuẩn-hóa-không-gian-và-khớp-nối-kinh-tế-world-bank-gdp--income-group)
4. [TỪ ĐIỂN DỮ LIỆU CHI TIẾT 44 CỘT CỦA MASTER DATASET (spotify.csv)](#4-từ-điển-dữ-liệu-chi-tiết-44-cột-của-master-dataset-spotifycsv)
5. [TỔNG HỢP CÁC TRƯỜNG TÍNH TOÁN (CALCULATED FIELDS)](#5-tổng-hợp-các-trường-tính-toán-calculated-fields)
6. [ĐÁNH GIÁ CHẤT LƯỢNG DỮ LIỆU, ĐỘ TIN CẬY MÔ HÌNH & CẢNH BÁO RÒ RỈ CHO ML](#6-đánh-giá-chất-lượng-dữ-liệu-độ-tin-cậy-mô-hình--cảnh-báo-rò-rỉ-cho-ml)
7. [HƯỚNG DẪN TRUY XUẤT DỮ LIỆU THÔNG QUA PYTHON API](#7-hướng-dẫn-truy-xuất-dữ-liệu-thông-qua-python-api)

---

## 1. TỔNG QUAN NGUỒN DỮ LIỆU & CHI TIẾT TỪNG TRƯỜNG CỦA 6 BẢNG THÔ (RAW DATA)

Hệ thống tích hợp dữ liệu từ 6 nguồn độc lập trong thư mục `data/raw/` với quy mô hơn 2.5 triệu bản ghi. Dưới đây là mô tả chi tiết từng trường của từng bảng dữ liệu thô và vai trò cụ thể trong quá trình ghép nối (JOIN) và phân tích:

### 1.1. Bảng `spotify-weekly-charts.csv` (Bảng Xương Sống Chuỗi Thời Gian)
* **Nguồn dữ liệu:** Bảng xếp hạng tuần khu vực và toàn cầu của Spotify (Top 200 Weekly Charts).
* **Quy mô ban đầu:** 1,787,999 dòng × 36 cột | **Dung lượng:** ~796.6 MB.
* **Mục đích:** Xương sống chuỗi thời gian (Fact Table), ghi nhận thứ hạng, số lượt streams, tên bài hát, nghệ sĩ tại 73 quốc gia và bảng Global (tổng 74 thực thể không gian) từ 2016 đến 2022.
* **Xử lý làm sạch:**
  - Trích xuất `track_id` từ URI (`spotify:track:<id>`).
  - Ép kiểu `week` sang chuẩn datetime (`YYYY-MM-DD`), lọc giữ giai đoạn trọng tâm 2020–2022 (1,078,125 dòng), tách `chart_year` và `chart_month`, đổi tên thành `chart_week`.
  - Lọc bỏ triệt để các bản ghi có `streams <= 0` hoặc `week` bị rỗng.
  - Khử trùng lặp bộ ba định danh `(track_id, chart_week, chart_country)`.
  - Đổi tên `country` $\to$ `chart_country`, `language` $\to$ `chart_language` để phân định rõ với quốc tịch ca sĩ và ngôn ngữ bài hát.
  - Loại bỏ sớm 15 cột phụ không mang giá trị cho insight (`Unnamed: 0`, `uri`, `artist_names`, `artists_num`, `artist_id`, `key`, `mode`, `source`, `album_num_tracks`, `collab`, `release_date`, `previous_rank`, `artist_img`, `album_cover`, `pivot`, `region`).

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
| 20 | `week` | Date | Ngày bắt đầu của tuần ghi nhận BXH (YYYY-MM-DD) | **Trục thời gian chính:** Phân tích chuỗi thời gian, lọc mốc 2020–2022. Trong Master Dataset được đổi tên thành `chart_week` để tránh nhầm lẫn với tuần/ngày phát hành bài hát. |
| 21 | `danceability` | Float64 | Mức độ phù hợp khiêu vũ / vũ đạo [0.0, 1.0] | 1 trong 9 Audio Features mô tả đặc trưng âm học |
| 22 | `energy` | Float64 | Cường độ năng lượng, độ sôi động [0.0, 1.0] | Kết hợp với `valence` để phân loại cảm xúc theo mô hình Russell |
| 23 | `key` | Int64 | Cao độ nốt nhạc chủ đạo (`0 = C, 1 = C#, ..., 11 = B`) | Phân tích nhạc lý và hòa thanh thị hiếu |
| 24 | `mode` | Int64 | Thang âm chủ đạo (`0 hoặc 1`: 1 = Trưởng/Major, 0 = Thứ/Minor) | Phân loại sắc thái bài hát tươi sáng (trưởng) hay trầm buồn (thứ) |
| 25 | `loudness` | Float64 | Độ to âm lượng tổng thể tính bằng Decibel ([-60, 5] dB) | Đo lường độ lớn sản xuất kỹ thuật âm thanh |
| 26 | `speechiness` | Float64 | Tỷ lệ xuất hiện của lời nói / rap trong track [0.0, 1.0] | Phân biệt nhạc thuần rap/spoken word với ca khúc giai điệu |
| 27 | `acousticness` | Float64 | Mức độ mộc / nhạc cụ acoustic không điện tử [0.0, 1.0] | Khảo sát xu hướng nhạc mộc vs nhạc điện tử qua các năm |
| 28 | `instrumentalness`| Float64 | Tỷ lệ không có lời hát (nhạc không lời) [0.0, 1.0] | Phát hiện các bản beat, nhạc thiền hoặc nhạc nền lọt top |
| 29 | `liveness` | Float64 | Xác suất bài hát được thu âm trực tiếp [0.0, 1.0] | Phát hiện các phiên bản Live Concert lọt bảng xếp hạng |
| 30 | `valence` | Float64 | Tính tích cực, vui tươi của giai điệu [0.0, 1.0] | Trục tâm trạng cốt lõi mô hình cảm xúc 4 góc phần tư |
| 31 | `tempo` | Float64 | Tốc độ nhịp đập bài hát tính theo Beats Per Minute (BPM) | Phân loại nhịp điệu bài hát (`tempo_category`: Slow, Medium, Fast, Very Fast) |
| 32 | `duration` | Int64 (ms) | Thời lượng bài hát tính bằng mili-giây | Chia 60,000 để tạo biến thời lượng phút (`duration_min`) |
| 33 | `country` | String | Thị trường BXH (73 quốc gia và bảng Global) | **Khóa JOIN không gian:** Khớp với `country_codes.csv` và `gdp_data.csv`. Trong Master Dataset được đổi tên thành `chart_country` để tránh nhầm lẫn với quốc tịch nghệ sĩ. |
| 34 | `region` | String | Phân vùng khu vực ban đầu trong file cào | Tham khảo phân vùng địa lý sơ cấp |
| 35 | `language` | String | Ngôn ngữ chính thức của thị trường BXH | Khảo sát thị hiếu ngôn ngữ âm nhạc theo khu vực. Trong Master Dataset được đổi tên thành `chart_language` để tránh nhầm lẫn với ngôn ngữ lời bài hát. |
| 36 | `pivot` | String/Int | Cờ kỹ thuật hỗ trợ xoay trục dữ liệu | Bỏ qua khi lưu trữ Master Dataset |

---

### 1.2. Bảng `songs.csv` (Kho Dữ Liệu 550K Bài Hát)
* **Nguồn dữ liệu:** Kho dữ liệu Kaggle *"550K Spotify Songs: Audio, Lyrics & Genres"* (Serkan Tysz).
* **Quy mô ban đầu:** 550,622 dòng × 24 cột | **Dung lượng:** ~856.4 MB.
* **Mục đích:** Bảng Chiều Bài hát (Song Dimension Table), cung cấp thể loại chi tiết cấp bài hát (`genre`) và điểm độ nổi tiếng tích lũy từ Spotify (`popularity`). Khớp thành công 2,551 bài hát trên BXH tuần 2020–2022.
* **Xử lý làm sạch:**
  - Trích xuất khóa `id` thành mã định danh chuẩn `track_id` (chuỗi 22 ký tự).
  - Khử trùng lặp theo `track_id`, ưu tiên giữ bản ghi có điểm `popularity` cao nhất.
  - Làm sạch chuỗi thể loại `genre`: loại bỏ triệt để các chuỗi rác (`'0'`, `''`, `'none'`, `'unknown'`, `'[]'`), chuyển toàn bộ về chữ thường (lowercase).
  - Chuẩn hóa thang đo `popularity` về đoạn $[0, 100]$, ép kiểu `Float64`.
  - Chọn lọc lấy 3 trường phục vụ ghép Thác nước (`track_id`, `genre`, `popularity`), loại bỏ các cột lời bài hát dài (`lyrics`) và các đặc trưng trùng lặp để tối ưu RAM.

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
* **Nguồn dữ liệu:** Bộ dữ liệu Spotify Tracks Dataset (114,000 bài hát với 125 nhãn thể loại).
* **Quy mô ban đầu:** 114,000 dòng × 22 cột | **Dung lượng:** ~20.8 MB.
* **Mục đích:** Bảng Chiều Bài hát bổ trợ thứ hai trong kiến trúc Ghép Thác Nước (Waterfall Join), giúp thu hồi thêm 1,936 bài hát độc lập mà `songs.csv` không có, nâng độ phủ dữ liệu thật từ 19.8% lên 42.2% trên toàn BXH (tương ứng 454,880 dòng).
* **Xử lý làm sạch:**
  - Khử trùng lặp khóa bài hát `track_id`, giữ lại bài hát có điểm `popularity` cao nhất.
  - Chuẩn hóa thể loại `track_genre`: chuyển về chữ thường, thay thế chuỗi rác bằng `np.nan`.
  - Hợp nhất Thác Nước (Waterfall Union) với `songs.csv`: Ưu tiên dữ liệu mới hơn từ `spotify-tracks-dataset.csv`, sau đó bổ sung bằng `songs.csv` (`combine_first`).
  - Loại bỏ cột `explicit` do độ bao phủ quá thấp (chỉ ~2,751 bài khớp, thiếu hơn 97%), tránh làm thiên lệch phân tích tổng thể.
  - Loại bỏ các cột chỉ số dòng cào thô (`Unnamed: 0.1`, `Unnamed: 0`) và các trường nhạc lý bổ trợ không dùng (`time_signature`).

| STT | Tên trường thô | Kiểu dữ liệu | Miền giá trị / Đơn vị | Ý nghĩa / Diễn giải cụ thể | Vai trò trong quá trình JOIN & Phân tích |
| :---: | :--- | :--- | :--- | :--- | :--- |
| 1–2 | `Unnamed: 0.1`, `Unnamed: 0` | Int64 | Số nguyên $\ge 0$ | Chỉ số dòng thô từ file cào | Bỏ qua khi nạp |
| 3 | `track_id` | String | `4cOdK2wGLETKBW3PvgPWqT` | Khóa định danh bài hát trên Spotify (22 ký tự) | **Khóa JOIN chính:** Khớp trực tiếp với `track_id` của bảng charts |
| 4 | `artists` | String | `Taylor Swift` | Tên các nghệ sĩ biểu diễn | Đối soát thông tin ca sĩ |
| 5 | `album_name` | String | `Midnights` | Tên album chứa bài hát | Thông tin bổ trợ album |
| 6 | `track_name` | String | `Anti-Hero` | Tên bài hát | Đối soát tên bài hát |
| 7 | `popularity` | Float64 | `[0, 100]` | Điểm độ nổi tiếng tích lũy từ Spotify API | **Thác nước bổ sung `song_popularity` thật:** Bổ sung điểm thật cho bài thiếu |
| 8 | `duration_ms` | Int64 | `Mili-giây ( > 0)` | Thời lượng bài hát tính bằng mili-giây | Đối soát độ dài bài hát |
| 9 | `explicit` | Boolean / Float64 | `True / False` | Cờ dán nhãn ca từ nhạy cảm / 18+ | Thuộc tính từ tập 114K bài (loại bỏ khỏi Master để tránh thiếu hụt) |
| 10 | `danceability` | Float64 | `[0.0, 1.0]` | Mức độ phù hợp khiêu vũ / vũ đạo | Đặc trưng âm học |
| 11 | `energy` | Float64 | `[0.0, 1.0]` | Cường độ năng lượng, độ sôi động | Đặc trưng âm học |
| 12 | `key` | Int64 | `0 = C, 1 = C#, ..., 11 = B` | Cao độ nốt nhạc chủ đạo | Phân tích nhạc lý và hòa thanh thị hiếu |
| 13 | `loudness` | Float64 | `Decibel ( dB ), thường  [-60, 5]` | Độ to âm lượng tổng thể tính bằng Decibel | Đo lường độ lớn kỹ thuật âm thanh |
| 14 | `mode` | Int64 | `0 hoặc 1` | Thang âm chủ đạo (1 = Trưởng/Major, 0 = Thứ/Minor) | Phân loại sắc thái bài hát tươi sáng hay trầm buồn |
| 15 | `speechiness` | Float64 | `[0.0, 1.0]` | Tỷ lệ xuất hiện của lời nói / rap trong track | Phân biệt nhạc rap/spoken word với ca khúc giai điệu |
| 16 | `acousticness` | Float64 | `[0.0, 1.0]` | Mức độ mộc / nhạc cụ acoustic không điện tử | Khảo sát xu hướng nhạc mộc vs nhạc điện tử |
| 17 | `instrumentalness`| Float64 | `[0.0, 1.0]` | Tỷ lệ không có lời hát (nhạc không lời) | Phát hiện bản beat, nhạc thiền hoặc nhạc nền |
| 18 | `liveness` | Float64 | `[0.0, 1.0]` | Xác suất bài hát được thu âm trực tiếp | Phát hiện các bản thu Live Concert |
| 19 | `valence` | Float64 | `[0.0, 1.0]` | Tính tích cực, vui tươi của giai điệu | Trục tâm trạng cốt lõi mô hình Russell |
| 20 | `tempo` | Float64 | `BPM ( > 0)` | Tốc độ nhịp đập bài hát theo Beats Per Minute | Phân loại nhịp điệu bài hát (`tempo_category`) |
| 21 | `time_signature` | Int64 | `3, 4, 5, 6, 7` | Số phách trong một ô nhịp (nhịp 3/4, 4/4,...) | Đặc trưng nhạc lý bổ trợ |
| 22 | `track_genre` | String | 125 nhãn thể loại | Thể loại âm nhạc của bài hát | **Thác nước bổ sung `song_genre` Tầng 1:** Bổ sung thể loại thật cấp bài hát |

---

### 1.4. Bảng `artists.csv` (Hồ Sơ 71K Nghệ Sĩ)
* **Nguồn dữ liệu:** Dữ liệu hồ sơ nghệ sĩ quy mô lớn từ Spotify Web API (71,440 nghệ sĩ).
* **Quy mô ban đầu:** 71,440 dòng × 6 cột | **Dung lượng:** ~5.4 MB.
* **Mục đích:** Bảng Chiều Hồ sơ Nghệ sĩ (Artist Dimension Table), cung cấp thông tin năng lực tiền phát hành của ca sĩ (`followers`, `popularity`, `main_genre`). Khớp thành công 63.1% số dòng trên bảng xếp hạng tuần.
* **Xử lý làm sạch:**
  - Chuẩn hóa tên nghệ sĩ `name` (xóa khoảng trắng thừa, hạ chữ thường để đối soát) và chuẩn hóa khóa `id` (`artist_id`).
  - Khử trùng lặp theo `artist_id` hoặc tên nghệ sĩ, giữ hồ sơ có lượng `followers` lớn nhất.
  - Xử lý chuỗi thể loại `main_genre` và `genres`: bóc tách chuỗi list dạng text, loại bỏ nhãn rác, chuyển về chữ thường.
  - Bảo tồn nguyên vẹn lượng người theo dõi gốc trong `artist_followers_raw` (chứa 36.9% rỗng tự nhiên từ hồ sơ nghệ sĩ).
  - Điền khuyết minh bạch điểm nổi tiếng `artist_popularity` bằng trung vị theo siêu dòng nhạc `macro_genre` và gắn cờ kiểm soát nguồn gốc `artist_popularity_is_imputed`.

| STT | Tên trường thô | Kiểu dữ liệu | Ý nghĩa / Diễn giải cụ thể | Vai trò trong quá trình JOIN & Phân tích |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `id` | String | Khóa định danh duy nhất của nghệ sĩ trên Spotify | **Khóa JOIN:** Khớp với `artist_id` hoặc tên ca sĩ trong bảng charts |
| 2 | `name` | String | Tên chính thức của nghệ sĩ | Khóa khớp phụ đối chiếu tên nghệ sĩ |
| 3 | `followers` | Float64 | Số lượng người theo dõi nghệ sĩ trên Spotify | **Cung cấp `artist_followers_raw`** (đo lường quy mô người hâm mộ gốc từ hồ sơ nghệ sĩ) |
| 4 | `popularity` | Float64 [0, 100] | Điểm độ nổi tiếng của nghệ sĩ từ Spotify API | **Cung cấp `artist_popularity`** (đo lường sức ảnh hưởng ca sĩ, điền khuyết minh bạch theo macro_genre) |
| 5 | `genres` | String (danh sách) | Chuỗi danh sách tất cả các thể loại ca sĩ từng hát | Tra cứu phong cách âm nhạc đa dạng của ca sĩ |
| 6 | `main_genre` | String | Thể loại âm nhạc chính đại diện của nghệ sĩ | **Nguồn Tầng 3 trong Bậc thang thể loại:** Cung cấp `artist_main_genre` |

---

### 1.5. Bảng `gdp_data.csv` (Dữ Liệu Kinh Tế Chuỗi Thời Gian World Bank)
* **Nguồn dữ liệu:** World Bank Development Indicators (Chuỗi thời gian kinh tế vĩ mô 1960 – 2022).
* **Quy mô ban đầu:** 13,365 dòng × 4 cột | **Dung lượng:** ~456 KB.
* **Mục đích:** Bảng Chiều Kinh tế Vĩ mô (Macroeconomic Dimension Table), liên kết quy mô kinh tế của từng quốc gia theo từng năm vào bảng xếp hạng để khảo sát mối tương quan giữa quy mô kinh tế/GDP và thị hiếu âm nhạc.
* **Xử lý làm sạch:**
  - Lọc dữ liệu trong khung thời gian phân tích của đồ án (2020 – 2022).
  - Chuẩn hóa tên quốc gia và mã ISO-alpha-3: Ánh xạ 7 quốc gia có tên khác biệt giữa hệ thống Spotify và World Bank (`Czechia` $\to$ Czech Republic, `Egypt` $\to$ Egypt Arab Rep., `Hong Kong SAR` $\to$ Hong Kong SAR China, `Korea Rep.` $\to$ Korea Rep., `Slovak Republic` $\to$ Slovakia, `Turkiye` $\to$ Turkey, `Venezuela` $\to$ Venezuela RB).
  - Khớp nối kép (Composite Key JOIN) theo cặp khóa `[country_code, chart_year]`.
  - Tính toán trường phái sinh logarit kinh tế: `gdp_log = ln(1 + gdp_value)` để nén độ lệch phải hàng nghìn tỷ USD giữa các nền kinh tế.

| STT | Tên trường thô | Kiểu dữ liệu | Ý nghĩa / Diễn giải cụ thể | Vai trò trong quá trình JOIN & Phân tích |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `country_name` | String | Tên quốc gia đầy đủ theo chuẩn World Bank | Đối soát tên thị trường kinh tế |
| 2 | `country_code` | String (3 ký tự) | Mã quốc gia chuẩn quốc tế ISO-alpha-3 | **Khóa JOIN không gian:** Khớp với mã quốc gia của bảng charts |
| 3 | `year` | Int64 | Năm ghi nhận chỉ số GDP (1960 – 2022) | **Khóa JOIN thời gian:** Khớp với năm phát hành bảng xếp hạng (`year`) |
| 4 | `value` | Float64 (USD) | Tổng sản phẩm quốc nội GDP tính theo USD hiện hành | **Cung cấp `gdp_value` và `gdp_log`:** Đo lường quy mô kinh tế của thị trường nghe nhạc |

---

### 1.6. Bảng `country_codes.csv` (Phân Tầng Địa Lý & Thu Nhập World Bank)
* **Nguồn dữ liệu:** World Bank Open Data Country Metadata.
* **Quy mô ban đầu:** 217 dòng × 3 cột | **Dung lượng:** ~9 KB.
* **Mục đích:** Bảng Chiều Không gian Địa lý (Geographical Dimension Table), ánh xạ mã quốc gia sang khu vực địa lý toàn cầu (`region_wb`) và phân tầng mức thu nhập (`income_group`).
* **Xử lý làm sạch:**
  - Chuẩn hóa mã định danh quốc tế `country_code` chuẩn ISO-alpha-3 (3 ký tự viết hoa).
  - Bổ sung thực thể lãnh thổ bị thiếu trong bảng World Bank gốc: Thêm thủ công mã vùng Đài Loan (`TWN` - `East Asia & Pacific` - `High income`) giúp tỷ lệ khớp địa lý đạt 95.8% (4.2% còn lại thuộc về bảng toàn cầu `Global`).
  - Chuẩn hóa tên cột: đổi `region` thành `region_wb` để phân biệt rõ với phân vùng cào thô ban đầu của Spotify.
  - Đồng bộ phân tầng thu nhập `income_group` thành 4 nhóm chuẩn: `High income`, `Upper middle income`, `Lower middle income`, `Low income`.

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

> [!IMPORTANT]
> 📂 **Kho Dữ Liệu Đồ Án Đầy Đủ (Google Drive):**  
> Do giới hạn 100MB của GitHub đối với các tệp dữ liệu lớn (`songs.csv` ~856 MB, `spotify-weekly-charts.csv` ~796 MB, `spotify.csv` ~390 MB), toàn bộ tệp dữ liệu thô và Master Dataset đầy đủ được lưu trữ tại:  
> 👉 **[TươngTacData - Google Drive](https://drive.google.com/drive/u/0/folders/1TN3uZLE9xYq-DDukDzQRbkzJK8wCtMYi)**

```text
data/
└── processed/
    ├── spotify.csv         # 1,078,125 dòng × 44 cột (390.5 MB) — Master Dataset tích hợp 6 bảng thô, chuẩn Phương án A
    └── tracks_ml_data.csv  # 36,699 bài hát × 26 cột (7.8 MB)   — Dữ liệu Song-level không rò rỉ phục vụ Machine Learning
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

### 3.3. Xử lý Dữ liệu Nghệ sĩ (`artist_popularity` & `artist_followers_raw`)

#### Bối cảnh:
Trong bảng `artists.csv` (71K ca sĩ), có 36.9% dòng trên bảng xếp hạng không tìm thấy hồ sơ ca sĩ do họ là các nghệ sĩ bản địa / indie (đặc biệt tại các thị trường đang phát triển).

#### Tại sao không xóa dòng:
Nếu xóa bỏ các dòng thiếu nghệ sĩ, **thị trường Việt Nam sẽ bị xóa mất 61.3% dữ liệu**, Brazil mất 77.6%, Thổ Nhĩ Kỳ mất 82.0%. Cấu trúc Top 200 tuần sẽ bị gãy vụn (chỉ còn trung bình 126 bài/tuần), làm mất đi tính toàn vẹn của bảng xếp hạng.

#### Thiết kế tinh gọn và minh bạch:
* `artist_followers_raw`: Giữ nguyên dữ liệu người theo dõi gốc từ hồ sơ nghệ sĩ (chứa 36.9% NA, phản ánh trung thực thực tế không gán số lượng người theo dõi giả định cho các nghệ sĩ indie).
* `artist_popularity`: Dữ liệu độ nổi tiếng nghệ sĩ đã được điền khuyết sạch 100% bằng trung vị có điều kiện theo dòng nhạc (`macro_genre`).
* `artist_popularity_is_imputed`: Cột cờ đánh dấu (0 = dữ liệu thật từ hồ sơ 71K nghệ sĩ, 1 = dữ liệu được điền khuyết).

#### Kỹ thuật điền khuyết bằng Trung vị Dòng nhạc & Thừa nhận Hạn chế (Selection Bias):
Dữ liệu khuyết độ nổi tiếng được điền bằng **Trung vị (Median)** theo từng dòng nhạc vĩ mô (`macro_genre`):
* Dòng Pop: nhận trung vị 68 điểm.
* Dòng Hip-Hop/Rap: nhận trung vị 65 điểm.
* Dòng Rock/Metal: nhận trung vị 58 điểm.
* *Thừa nhận giới hạn khoa học:* Tập `artists.csv` chủ yếu gồm các nghệ sĩ quốc tế có mức độ nhận diện cao, nên trung vị 68 điểm có thể hơi ưu ái đối với một nghệ sĩ indie mới ra mắt tại Việt Nam. Đây là một sự đánh đổi kỹ thuật có chủ đích (Engineering Trade-off) nhằm bảo toàn cấu trúc bảng xếp hạng và giữ trọn vẹn thị trường Việt Nam cho phân tích trực quan. Nhờ cột cờ `artist_popularity_is_imputed`, bất kỳ nhà nghiên cứu nào cũng có thể lọc riêng tập nghệ sĩ thuần túy khi cần.

---

### 3.4. Chuẩn hóa không gian và khớp nối kinh tế World Bank (GDP & Income Group)

* **Khớp nối kinh tế đa tầng:** Kết hợp `gdp_data.csv` (13,365 dòng chuỗi thời gian) và `country_codes.csv` (217 quốc gia) dựa trên mã quốc gia và năm phát hành bảng xếp hạng.
* **Chuẩn hóa danh xưng quốc tế:** Thiết lập ánh xạ cho 7 quốc gia có tên khác biệt giữa hệ thống Spotify và World Bank (Czechia, Egypt, Hong Kong SAR, Korea Rep., Slovak Republic, Turkiye, Venezuela).
* **Bổ sung thực thể lãnh thổ:** Bổ sung thủ công mã vùng Đài Loan (`TWN` - `East Asia & Pacific` - `High income`) giúp tỷ lệ khớp đạt **95.8%** (4.2% còn lại thuộc về bảng xếp hạng toàn cầu `Global`).
* **Trường logarit kinh tế:** Tạo trường `gdp_log` bằng công thức `ln(1 + gdp_value)` nhằm nén biên độ chênh lệch hàng nghìn tỷ USD giữa các nền kinh tế.

---

## 4. TỪ ĐIỂN DỮ LIỆU CHI TIẾT 44 CỘT CỦA MASTER DATASET (`spotify.csv`)

| STT | Tên cột | Kiểu dữ liệu | Nhóm thuộc tính | Nguồn gốc | Ý nghĩa / Diễn giải phân tích |
| :---: | :--- | :--- | :--- | :--- | :--- |
| 1 | `track_id` | String (22 ký tự) | Nhận dạng | Charts | Khóa định danh duy nhất của bài hát trên Spotify API |
| 2 | `track_name` | String | Nhận dạng | Charts | Tên bài hát |
| 3 | `artist_individual` | String | Nhận dạng | Charts | Tên nghệ sĩ chính / nghệ sĩ biểu diễn đầu tiên |
| 4 | `artist_genre` | String | Nhận dạng | Charts | Thể loại âm nhạc gắn với nghệ sĩ trên BXH tuần |
| 5 | `chart_country` | String | Không gian | Charts | Quốc gia / Thị trường BXH (73 quốc gia và bảng Global, đổi tên từ `country` để tránh nhầm với quốc tịch nghệ sĩ) |
| 6 | `chart_language` | String | Không gian | Charts | Ngôn ngữ của thị trường BXH (đổi tên từ `language` để tránh nhầm với ngôn ngữ lời bài hát) |
| 7 | `chart_week` | Date (YYYY-MM-DD)| Thời gian | Charts | Ngày bắt đầu của tuần ghi nhận BXH (đổi tên từ `week` để tránh nhầm với tuần/ngày phát hành bài hát) |
| 8 | `chart_year` | Int64 | Thời gian | Charts | Năm phát hành bảng xếp hạng (2020, 2021, 2022, đổi tên từ `year` để tránh nhầm với năm phát hành bài hát) |
| 9 | `chart_month` | Int64 | Thời gian | Charts | Tháng trong năm ghi nhận BXH (1 đến 12, đổi tên từ `month`) |
| 10 | `rank` | Int64 | Xếp hạng | Charts | Thứ hạng của bài hát trên Top 200 tuần (từ 1 đến 200) |
| 11 | `streams` | Int64 | Lượt nghe | Charts | Số lượt stream tích lũy trong tuần tại thị trường |
| 12 | `weeks_on_chart` | Int64 | Trụ hạng | Charts | Số tuần liên tục hoặc tích lũy có mặt trên BXH |
| 13 | `peak_rank` | Int64 | Trụ hạng | Charts | Thứ hạng cao nhất bài hát từng đạt được trên BXH |
| 14 | `danceability` | Float64 | Audio Feature | Charts | Mức độ phù hợp khiêu vũ / vũ đạo [0.0, 1.0] |
| 15 | `energy` | Float64 | Audio Feature | Charts | Cường độ năng lượng, độ sôi động [0.0, 1.0] |
| 16 | `loudness` | Float64 | Audio Feature | Charts | Độ to âm lượng tổng thể tính bằng Decibel ([-60, 5] dB) |
| 17 | `speechiness` | Float64 | Audio Feature | Charts | Tỷ lệ xuất hiện của lời nói / rap trong track [0.0, 1.0] |
| 18 | `acousticness` | Float64 | Audio Feature | Charts | Mức độ mộc / nhạc cụ acoustic không điện tử [0.0, 1.0] |
| 19 | `instrumentalness`| Float64 | Audio Feature | Charts | Tỷ lệ không có lời hát (nhạc không lời) [0.0, 1.0] |
| 20 | `liveness` | Float64 | Audio Feature | Charts | Xác suất bài hát được thu âm trực tiếp [0.0, 1.0] |
| 21 | `valence` | Float64 | Audio Feature | Charts | Tính tích cực, vui tươi của giai điệu [0.0, 1.0] |
| 22 | `tempo` | Float64 | Audio Feature | Charts | Tốc độ nhịp đập bài hát tính theo Beats Per Minute (BPM) |
| 23 | `song_genre` | String | Thể loại | Bậc thang 4 tầng | Thể loại bài hát chuẩn hóa (100% đầy đủ, 1,481 nhãn chi tiết) |
| 24 | `song_genre_source` | String | Data Lineage | Calculated Field | Nguồn điền thể loại: track_dataset, artist_detailed_chart, artist_main_profile, macro_fallback |
| 25 | `song_popularity_raw` | Float64 [0, 100] | Nổi tiếng | Thác nước Tracks | Điểm độ phổ biến gốc từ Spotify (chứa 57.8% rỗng để đối soát) |
| 26 | `song_popularity` | Float64 [0, 100] | Nổi tiếng | Phương án A | Điểm độ nổi tiếng thật từ Spotify API (42.2% có điểm, 57.8% để trống tự nhiên) |
| 27 | `has_song_popularity` | Int64 (0/1) | Phân loại EDA | Calculated Field | 1 = Bài có điểm thật Spotify (42.2%), 0 = Bài chưa lập chỉ mục Unindexed (57.8%) |
| 28 | `popularity_status` | String | Phân loại EDA | Calculated Field | Phân nhóm trực quan: Official Spotify Score vs Unindexed / Regional Hits |
| 29 | `artist_main_genre` | String | Nghệ sĩ | artists.csv | Dòng nhạc chính của nghệ sĩ trong hồ sơ nghệ sĩ |
| 30 | `artist_followers_raw` | Float64 | Nghệ sĩ | artists.csv | Lượng người theo dõi nghệ sĩ gốc (chứa 36.9% rỗng từ hồ sơ nghệ sĩ) |
| 31 | `artist_popularity` | Float64 [0, 100] | Nghệ sĩ | Trung vị Dòng nhạc | Điểm độ nổi tiếng nghệ sĩ đã điền khuyết sạch 100% |
| 32 | `artist_popularity_is_imputed` | Int64 (0/1) | Data Lineage | Calculated Field | Cờ đánh dấu: 0 = Điểm ca sĩ thật, 1 = Điền khuyết trung vị |
| 33 | `gdp_value` | Float64 | Kinh tế World Bank | gdp_data.csv | Tổng sản phẩm quốc nội USD hiện hành (khuyết ở bảng Global và TWN/VEN) |
| 34 | `gdp_log` | Float64 | Kinh tế | Calculated Field | ln(1 + gdp_value) nén quy mô kinh tế |
| 35 | `income_group` | String | Kinh tế | country_codes | Phân tầng thu nhập quốc gia (High, Upper middle, Lower middle) |
| 36 | `region_wb` | String | Địa lý | country_codes | Khu vực địa lý kinh tế theo World Bank |
| 37 | `country_code` | String (3 ký tự) | Địa lý | country_codes | Mã định danh chuẩn ISO-alpha-3 của quốc gia |
| 38 | `is_trending` | Int64 (0/1) | Calculated Field | Pipeline logic | 1 nếu bài thuộc Top 50 tuần (rank <= 50), 0 nếu Top 51–200 |
| 39 | `mood_category` | String | Calculated Field | Mô hình Russell | Phân loại cảm xúc: Happy Energetic, Peaceful Positive, Tense Aggressive, Sad Melancholic |
| 40 | `stream_share_country`| Float64 | Calculated Field | Pipeline logic | Thị phần stream bài hát so với tổng Top 200 trong thị trường–tuần |
| 41 | `macro_genre` | String | Calculated Field | Regex chuẩn hóa | Dòng nhạc vĩ mô chuẩn hóa (6 nhóm: Pop, Latin, Hip-Hop, Rock, K-Pop, Others) |
| 42 | `duration_min` | Float64 (phút) | Calculated Field | Pipeline logic | Thời lượng bài hát tính bằng phút (duration_ms / 60,000) |
| 43 | `chart_longevity` | Int64 (tuần) | Calculated Field | Pipeline logic | Số tuần trụ hạng cao nhất của bài trên BXH |
| 44 | `tempo_category` | String | Calculated Field | Phân khoảng nhịp | Phân nhóm nhịp: Slow (<90), Medium (90–120), Fast (120–150), Very Fast (>=150 BPM) |

---

## 5. TỔNG HỢP CÁC TRƯỜNG TÍNH TOÁN (CALCULATED FIELDS)

Master Dataset được thiết kế với **12 trường tính toán phái sinh (Calculated Fields)** nhằm phục vụ trực tiếp cho trực quan hóa tương tác Bento Grid, phân tích chuyên sâu EDA và xây dựng bài toán Machine Learning.

### 5.1. Bảng tóm tắt các trường tính toán

| STT | Trường tính toán | Kiểu dữ liệu | Nhóm bản chất | Công thức / Phương pháp cốt lõi | Mục đích phân tích & Ứng dụng |
| :---: | :--- | :--- | :--- | :--- | :--- |
| 1 | `is_trending` | Int64 (0/1) | Xếp hạng tuần | $\text{rank} \le 50 \implies 1$, ngược lại $0$ | Biến nhãn mục tiêu (Target Label) cho bài toán Machine Learning dự đoán Hit. |
| 2 | `mood_category` | String | Cảm xúc âm học | Mô hình Russell 4 góc phần tư (`valence` vs `energy` cắt ngưỡng 0.5) | Bản đồ phân bổ tâm trạng người nghe theo quốc gia, mùa vụ và dòng nhạc. |
| 3 | `stream_share_country` | Float64 [0, 1] | Thị phần stream | $\frac{\text{streams}}{\sum \text{streams}_{\text{Top 200 (quốc gia, tuần)}}}$ | Chuẩn hóa quy mô lượt nghe giữa các nước, đo lường mức độ thống trị thị trường. |
| 4 | `macro_genre` | String | Dòng nhạc vĩ mô | Regex 6 siêu nhóm có ranh giới từ $\to$ Ổn định hóa theo Mode của `track_id` | Lọc phân tích cấp vĩ mô trên Dashboard, giải quyết phân mảnh 1,481 thể loại. |
| 5 | `song_genre` & `song_genre_source` | String | Thể loại chuẩn | Bậc thang thác nước 4 tầng (Track Dataset $\to$ Chart Detail $\to$ Artist Profile $\to$ Macro) | Đạt độ phủ sạch 100% dữ liệu, truy vết nguồn gốc minh bạch từng dòng. |
| 6 | `has_song_popularity` & `popularity_status` | Int64 / String | Trạng thái chỉ mục | Kiểm tra $\text{song\_popularity}$ IS NOT NULL | Phân định trực quan giữa Mainstream toàn cầu vs Indie/Bản địa trong EDA. |
| 7 | `artist_popularity` & `artist_popularity_is_imputed` | Float64 / Int64 | Năng lực ca sĩ | Điền Median có điều kiện theo `macro_genre` kèm cờ đánh dấu nguồn gốc | Cung cấp biến liên tục cho mô hình dự báo mà không xóa mất thị trường Việt Nam. |
| 8 | `duration_min` | Float64 (phút) | Thời lượng | $\frac{\text{duration}}{60{,}000}$ (làm tròn 3 chữ số thập phân) | Khảo sát xu hướng rút ngắn độ dài ca khúc trong thời đại streaming và TikTok. |
| 9 | `chart_longevity` | Int64 (tuần) | Độ bền bỉ | $\max(\text{weeks\_on\_chart})$ theo từng `track_id` | Phân loại ca khúc: Hiện tượng nhất thời (Viral Hit) vs Bản hit kinh điển (Evergreen). |
| 10 | `tempo_category` | String | Nhịp độ âm nhạc | Phân đoạn 4 khoảng nhịp: Slow, Medium, Fast, Very Fast theo BPM | Phân tích gu thưởng thức tốc độ nhịp điệu theo khu vực địa lý và văn hóa. |
| 11 | `gdp_log` | Float64 | Kinh tế lượng | $\ln(1 + \text{gdp\_value})$ | Nén biên độ chênh lệch hàng nghìn tỷ USD, đưa GDP về phân phối chuẩn cho hồi quy. |
| 12 | `chart_year` & `chart_month` | Int64 | Trục thời gian | Trích xuất thành phần năm và tháng từ ngày đầu tuần `chart_week` | Phân tích chu kỳ mùa vụ (Seasonality) và xu hướng dài hạn qua các năm 2020–2022. |

---

### 5.2. Chi tiết công thức toán học & Phương pháp thực thi từng trường

#### 1. `is_trending` — Nhãn Trạng Thái Thịnh Hành (Trending Binary Target)
* **Phương pháp & Định nghĩa:** Cắt ngưỡng nhị phân dựa trên thứ hạng bài hát trên Top 200 tuần. Ngưỡng Top 50 là ranh giới chuẩn mực công nghiệp âm nhạc: Các bài hát thuộc Top 50 nhận được hơn 70% tổng lượt nghe của bảng xếp hạng, thường xuyên xuất hiện trên các playlist biên tập lớn của Spotify (như *Today's Top Hits*) và có độ lan tỏa đại chúng vượt trội so với nhóm Top 51–200.
* **Công thức toán học:**
  $$\text{is\_trending}_{i, c, w} = \begin{cases} 1 & \text{nếu } \text{rank}_{i, c, w} \le 50 \\ 0 & \text{nếu } 51 \le \text{rank}_{i, c, w} \le 200 \end{cases}$$
* **Mã nguồn thực thi Python (`src/data_loader.py`):**
  ```python
  TRENDING_THRESHOLD = 50
  df["is_trending"] = (df["rank"] <= TRENDING_THRESHOLD).astype(int)
  ```
* **Ứng dụng:** Làm biến mục tiêu chuẩn hóa (Supervised Learning Label) cho các mô hình phân loại dự đoán ca khúc tiềm năng lọt Top Hit.

---

#### 2. `mood_category` — Phân Loại Cảm Xúc Âm Nhạc (Russell's Circumplex Model of Affect)
* **Phương pháp & Cơ sở lý thuyết:** Ứng dụng mô hình cảm xúc vòng tròn 2 chiều kinh điển của nhà tâm lý học James Russell (1980). Không gian cảm xúc âm nhạc được cấu thành từ 2 trục tọa độ âm học chuẩn hóa $[0, 1]$ từ Spotify API:
  - **Trục hoành — Valence (Hóa trị cảm xúc):** Thước đo sắc thái tích cực, vui tươi, tươi sáng ($0.0$: bi thương, u uất $\to 1.0$: vui vẻ, phấn khởi).
  - **Trục tung — Energy (Cường độ năng lượng):** Thước đo cường độ kích thích, độ sôi động, dồn dập ($0.0$: êm dịu, tĩnh lặng $\to 1.0$: bùng nổ, ồn ào).
* **Công thức phân vùng 4 góc phần tư (ngưỡng cắt $\theta = 0.5$):**
  $$\text{mood\_category} = \begin{cases} 
  \text{"Happy Energetic"} & \text{nếu } \text{valence} \ge 0.5 \land \text{energy} \ge 0.5 \\
  \text{"Peaceful Positive"} & \text{nếu } \text{valence} \ge 0.5 \land \text{energy} < 0.5 \\
  \text{"Tense Aggressive"} & \text{nếu } \text{valence} < 0.5 \land \text{energy} \ge 0.5 \\
  \text{"Sad Melancholic"} & \text{nếu } \text{valence} < 0.5 \land \text{energy} < 0.5 \\
  \text{"Unknown"} & \text{nếu thiếu dữ liệu audio features}
  \end{cases}$$
* **Mã nguồn thực thi Python (`src/data_loader.py`):**
  ```python
  has_audio = df["valence"].notna() & df["energy"].notna()
  v_hi = df["valence"] >= 0.5
  e_hi = df["energy"] >= 0.5
  df["mood_category"] = "Unknown"
  df.loc[has_audio & v_hi & e_hi, "mood_category"] = "Happy Energetic"
  df.loc[has_audio & v_hi & ~e_hi, "mood_category"] = "Peaceful Positive"
  df.loc[has_audio & ~v_hi & e_hi, "mood_category"] = "Tense Aggressive"
  df.loc[has_audio & ~v_hi & ~e_hi, "mood_category"] = "Sad Melancholic"
  ```
* **Ứng dụng:** Trực quan hóa bản đồ cảm xúc âm nhạc (Mood Map Scatter Plot), phân tích sự dịch chuyển tâm trạng nghe nhạc của công chúng theo mùa trong năm và giữa các nền văn hóa.

---

#### 3. `stream_share_country` — Thị Phần Lượt Nghe Trong Thị Trường Tuần (Relative Stream Share)
* **Phương pháp & Vấn đề giải quyết:** Do quy mô dân số và độ phủ dịch vụ streaming giữa các quốc gia chênh lệch khổng lồ (ví dụ: một bản hit Top 1 tại Mỹ thu hút hơn 30 triệu streams/tuần, trong khi Top 1 tại Việt Nam năm 2020 chỉ đạt khoảng 600,000 streams/tuần), việc so sánh trực tiếp số lượt nghe thô (`streams`) sẽ tạo ra thiên lệch lớn về phía các thị trường phương Tây. Trường `stream_share_country` chuẩn hóa mức độ áp đảo của một ca khúc so với toàn bộ dung lượng thị trường Top 200 tại quốc gia đó trong tuần tương ứng.
* **Công thức toán học:**
  $$\text{stream\_share\_country}_{i, c, w} = \frac{\text{streams}_{i, c, w}}{\sum_{k \in \text{Top 200}(c, w)} \text{streams}_{k, c, w}}$$
  Trong đó: $i$ là bài hát, $c$ là thị trường quốc gia (`chart_country`), $w$ là tuần bảng xếp hạng (`chart_week`).
* **Mã nguồn thực thi Python (`src/data_loader.py`):**
  ```python
  total_streams = df.groupby(["chart_country", "chart_week"])["streams"].transform("sum")
  df["stream_share_country"] = np.where(total_streams > 0, df["streams"] / total_streams, 0)
  ```
* **Ứng dụng:** Đo lường mức độ tập trung thị trường, phát hiện các siêu hit "quốc dân" có thị phần vượt trội (thị phần $> 5\%$ trong tổng Top 200 cả nước).

---

#### 4. `macro_genre` — Siêu Dòng Nhạc Vĩ Mô & Thuật Toán Ổn Định Hóa (Macro Genre Mapping & Mode Stabilization)
* **Phương pháp & Vấn đề giải quyết:** Bảng xếp hạng Spotify chứa tới **1,481 nhãn thể loại vi mô** (`artist_genre`) rất phân mảnh (ví dụ: `vietnamese hip hop`, `v-pop`, `trap latino`, `german metalcore`). Nhằm phục vụ trực quan hóa cấp cao trên Dashboard và làm tầng điều kiện phân nhóm điền khuyết, hệ thống ánh xạ 1,481 nhãn này về **6 siêu dòng nhạc vĩ mô chuẩn mực**: `Pop`, `Latin`, `Hip-Hop`, `Rock`, `K-Pop`, `Others`.
* **Thuật toán Khớp Mẫu Biểu Thức Chính Quy (Regex Word Boundary Matching):**
  Để tránh hiện tượng nuốt nhãn sai lệch (ví dụ chữ "pop" trong "k-pop" nếu quét không cẩn thận sẽ bị biến thành Pop thay vì K-Pop), hệ thống thiết lập thứ tự ưu tiên nghiêm ngặt với ranh giới từ `\b...\b`:
  1. **K-Pop (Độ ưu tiên 1):** Khớp các từ khóa `\b(k-pop|korean pop|kpop)\b`.
  2. **Latin (Độ ưu tiên 2):** Khớp các từ khóa `\b(latin|reggaeton|urbano|salsa|bachata|trap latino|sertanejo|forro|mpb)\b`.
  3. **Hip-Hop (Độ ưu tiên 3):** Khớp các từ khóa `\b(hip hop|hip-hop|rap|trap|drill|r&b|soul)\b`.
  4. **Rock (Độ ưu tiên 4):** Khớp các từ khóa `\b(rock|metal|punk|indie rock|grunge|alt-rock)\b`.
  5. **Pop (Độ ưu tiên 5):** Khớp các từ khóa `\b(pop|dance pop|synth-pop|electropop|indie pop)\b`.
  6. **Others (Độ ưu tiên 6):** Tất cả các dòng nhạc còn lại (EDM, Classical, Jazz, Country, Folk, Soundtrack,...).
* **Kỹ thuật Ổn định hóa cấp Bài hát (Track-level Mode Stabilization):**
  Trong dữ liệu tuần, thể loại của một nghệ sĩ có thể biến động nhẹ giữa các tuần. Để đảm bảo tính nhất quán khoa học — **một bài hát duy nhất chỉ được mang đúng 1 siêu dòng nhạc duy nhất xuyên suốt thời gian có mặt trên BXH**, hệ thống áp dụng kỹ thuật tính giá trị xuất hiện nhiều nhất (Mode) theo từng `track_id`:
  $$\text{macro\_genre}_i = \text{Mode}(\{\text{macro\_genre}_{i, w}\}_{w=1}^{T_i})$$
* **Mã nguồn thực thi Python (`src/data_loader.py`):**
  ```python
  df["macro_genre"] = compute_macro_genre(df)
  track_macro_mode = (
      df.groupby("track_id")["macro_genre"]
      .agg(lambda x: x.value_counts().index[0])
  )
  df["macro_genre"] = df["track_id"].map(track_macro_mode)
  ```

---

#### 5. `song_genre` & `song_genre_source` — Bậc Thang Thể Loại 4 Tầng (Fallback Hierarchy)
* **Phương pháp & Quy trình xử lý:** Thể loại âm nhạc là đặc trưng phân loại quan trọng nhất trong nghiên cứu âm nhạc, nhưng các nguồn dữ liệu thô đều bị thiếu hụt nặng nề nếu chỉ lấy đơn lẻ. Pipeline triển khai cơ chế Thác nước 4 tầng ưu tiên giảm dần, đồng thời sinh cột `song_genre_source` để ghi nhận tính minh bạch nguồn gốc:
  - **Tầng 1 (`track_dataset`):** Lấy thể loại cụ thể của bài hát từ bảng hợp nhất `songs.csv` và `spotify-tracks-dataset.csv`.
  - **Tầng 2 (`artist_detailed_chart`):** Nếu Tầng 1 khuyết, lấy thể loại chi tiết của nghệ sĩ gắn với bài trên BXH tuần (`artist_genre` — phủ 100% Top 200, chứa 1,481 nhãn bản địa).
  - **Tầng 3 (`artist_main_profile`):** Nếu Tầng 2 khuyết, lấy thể loại chính từ hồ sơ nghệ sĩ lớn `artists.csv` (`artist_main_genre`).
  - **Tầng 4 (`macro_fallback`):** Lưới an toàn cuối cùng, quy đổi về siêu dòng nhạc vĩ mô (`macro_genre`).
* **Mã nguồn thực thi Python (`src/data_loader.py`):**
  ```python
  df["song_genre"] = (
      song_genre_raw_clean
      .fillna(artist_genre_clean)
      .fillna(artist_main_clean)
      .fillna(df["macro_genre"].str.lower())
  )
  df["song_genre_source"] = np.where(
      song_genre_raw_clean.notna(), "track_dataset",
      np.where(artist_genre_clean.notna(), "artist_detailed_chart",
      np.where(artist_main_clean.notna(), "artist_main_profile", "macro_fallback"))
  )
  ```
* **Kết quả:** Đạt **100.0% độ phủ sạch (0% Missing Values)**, bảo tồn nguyên vẹn tính đa dạng với **1,481 nhãn thể loại chi tiết**.

---

#### 6. `has_song_popularity` & `popularity_status` — Cờ Phân Định Điểm Độ Nổi Tiếng Thật (Method A Data Lineage)
* **Phương pháp & Định hướng:** Thực hiện chuẩn mực Phương án A — **Bảo toàn dữ liệu thật, không tạo số liệu giả bằng mô hình hồi quy ở tiền xử lý**. 
  - Điểm độ nổi tiếng `song_popularity` được giữ nguyên vẹn từ Spotify Web API (42.2% có điểm thật từ các bài quốc tế, 57.8% bài indie/bản địa để trống tự nhiên).
  - Sinh 2 trường chỉ báo để hỗ trợ lọc và phân tích trực quan EDA:
* **Công thức toán học:**
  $$\text{has\_song\_popularity}_i = \begin{cases} 1 & \text{nếu } \text{song\_popularity}_i \ne \text{NaN} \\ 0 & \text{nếu } \text{song\_popularity}_i = \text{NaN} \end{cases}$$
  $$\text{popularity\_status}_i = \begin{cases} \text{"Official Spotify Score"} & \text{nếu } \text{has\_song\_popularity}_i = 1 \\ \text{"Unindexed / Regional Hits"} & \text{nếu } \text{has\_song\_popularity}_i = 0 \end{cases}$$
* **Mã nguồn thực thi Python (`src/data_loader.py`):**
  ```python
  df["song_popularity"] = df["song_popularity_raw"]
  df["has_song_popularity"] = df["song_popularity"].notna().astype(int)
  df["popularity_status"] = np.where(
      df["song_popularity"].notna(),
      "Official Spotify Score",
      "Unindexed / Regional Hits"
  )
  ```
* **Ứng dụng:** Phục vụ trực tiếp cho tham số `hue="popularity_status"` trên biểu đồ phân tích Seaborn/Plotly, chỉ ra thiên kiến lập chỉ mục địa lý của Spotify.

---

#### 7. `artist_popularity` & `artist_popularity_is_imputed` — Điền Khuyết Minh Bạch Năng Lực Ca Sĩ
* **Phương pháp & Giải pháp:** Có 36.9% dòng trên BXH thuộc về các nghệ sĩ indie hoặc nghệ sĩ bản địa không có hồ sơ trong bảng quốc tế `artists.csv`. Nếu xóa bỏ các dòng này, bảng xếp hạng Việt Nam sẽ mất 61.3% dữ liệu. Để giải quyết, hệ thống áp dụng kỹ thuật điền trung vị có điều kiện theo dòng nhạc vĩ mô và gắn cờ minh bạch:
  1. Gán cờ `artist_popularity_is_imputed = 1` nếu nghệ sĩ khuyết điểm, `= 0` nếu là điểm thật từ hồ sơ 71K ca sĩ.
  2. Tính trung vị điểm nổi tiếng $\text{Median}(\text{artist\_popularity\_raw})$ cho từng nhóm `macro_genre` (Pop: 68, Hip-Hop: 65, Rock: 58,...).
  3. Điền giá trị trung vị này vào các vị trí trống.
* **Công thức toán học:**
  $$\text{artist\_popularity}_i = \begin{cases} 
  \text{artist\_popularity\_raw}_i & \text{nếu có dữ liệu thật} \\
  \text{Median}(\text{artist\_popularity\_raw} \mid \text{macro\_genre}_i) & \text{nếu khuyết dữ liệu} \\
  50 & \text{dự phòng toàn cục (Global fallback)}
  \end{cases}$$
* **Mã nguồn thực thi Python (`src/data_loader.py`):**
  ```python
  df["artist_popularity_is_imputed"] = df["artist_popularity_raw"].isna().astype(int)
  macro_art_pop_med = df.groupby("macro_genre")["artist_popularity_raw"].transform("median")
  df["artist_popularity"] = df["artist_popularity_raw"].fillna(macro_art_pop_med).fillna(50)
  ```

---

#### 8. `duration_min` — Thời Lượng Bài Hát Tính Theo Phút
* **Phương pháp:** Trong dữ liệu thô Spotify Web API, thời lượng bài hát được lưu dưới dạng mili-giây nguyên số (`duration` $\in \mathbb{N}$). Nhằm phục vụ trực quan hóa thân thiện với người dùng và các biểu đồ phân tích xu hướng độ dài, giá trị này được quy đổi về đơn vị phút và làm tròn 3 chữ số thập phân.
* **Công thức toán học:**
  $$\text{duration\_min} = \frac{\text{duration}}{60{,}000}$$
* **Mã nguồn thực thi Python (`src/data_loader.py`):**
  ```python
  df["duration_min"] = (df["duration"] / 60_000).round(3)
  ```
* **Ứng dụng:** Khảo sát hiện tượng thời lượng bài hát trung bình ngày càng ngắn lại (từ ~3.8 phút năm 2020 xuống ~3.1 phút năm 2022) do thuật toán chi trả bản quyền stream và thói quen nghe lướt của thế hệ trẻ.

---

#### 9. `chart_longevity` — Độ Bền Bỉ Trụ Hạng Tối Đa Của Bài Hát
* **Phương pháp & Định nghĩa:** Cột `weeks_on_chart` ghi nhận số tuần tích lũy tại tuần hiện tại. Để đánh giá sức sống trường tồn xuyên suốt của một ca khúc trong toàn bộ giai đoạn 2020–2022, trường `chart_longevity` tổng hợp giá trị lớn nhất của số tuần có mặt trên BXH cho từng mã định danh bài hát `track_id`.
* **Công thức toán học:**
  $$\text{chart\_longevity}_i = \max_{t \in T_i} (\text{weeks\_on\_chart}_{i, t})$$
  Trong đó $T_i$ là tập hợp tất cả các tuần bài hát $i$ xuất hiện trên bảng xếp hạng.
* **Mã nguồn thực thi Python (`src/data_loader.py`):**
  ```python
  df["chart_longevity"] = df.groupby("track_id")["weeks_on_chart"].transform("max")
  ```
* **Ứng dụng:** Phân biệt bài hát "chóng nở chóng tàn" (Flash-in-the-pan, trụ hạng < 4 tuần) với ca khúc bất hủ (Evergreen / Sleeper Hits, trụ hạng liên tục > 52 tuần như *Blinding Lights* của The Weeknd hay *Heat Waves* của Glass Animals).

---

#### 10. `tempo_category` — Phân Khoảng Tốc Độ Nhịp Đập Âm Nhạc
* **Phương pháp:** Trường `tempo` thể hiện số nhịp đập mỗi phút (Beats Per Minute - BPM) là biến liên tục từ 0 đến 250 BPM. Để dễ dàng tạo bộ lọc trên Bento Grid Dashboard và phân tích thị hiếu nhóm nhịp điệu, trường này được rời rạc hóa (discretized) thành 4 phân khoảng chuẩn nhạc lý:
  - **Slow (< 90 BPM):** Nhạc chậm, ballad, chillout, lofi.
  - **Medium (90 – 120 BPM):** Nhịp độ vừa phải, pop tiêu chuẩn, R&B, hip-hop melodic.
  - **Fast (120 – 150 BPM):** Nhịp sôi động, dance pop, EDM house, reggaeton.
  - **Very Fast ( $\ge$ 150 BPM):** Nhịp dồn dập, rock/metal nhanh, drum & bass, trap bùng nổ.
* **Công thức toán học:**
  $$\text{tempo\_category} = \begin{cases} 
  \text{"Slow"} & \text{nếu } 0 \le \text{tempo} < 90 \\
  \text{"Medium"} & \text{nếu } 90 \le \text{tempo} < 120 \\
  \text{"Fast"} & \text{nếu } 120 \le \text{tempo} < 150 \\
  \text{"Very Fast"} & \text{nếu } \text{tempo} \ge 150 \\
  \text{"Unknown"} & \text{nếu khuyết tempo}
  \end{cases}$$
* **Mã nguồn thực thi Python (`src/data_loader.py`):**
  ```python
  df["tempo_category"] = pd.cut(
      df["tempo"],
      bins=[0, 90, 120, 150, 300],
      labels=["Slow", "Medium", "Fast", "Very Fast"],
      right=False
  ).astype(str).replace("nan", "Unknown")
  ```

---

#### 11. `gdp_log` — Logarit Tự Nhiên Nén Quy Mô Kinh Tế Quốc Gia
* **Phương pháp & Vấn đề giải quyết:** Chỉ số GDP thu thập từ World Bank (`gdp_value`) có khoảng biến thiên cực kỳ rộng, từ vài tỷ USD (các quốc gia nhỏ như Iceland: ~25 tỷ USD) đến hơn 25,000 tỷ USD (Mỹ). Dữ liệu này bị lệch phải nghiêm trọng (Extreme Right-skewed Distribution). Việc đưa trực tiếp biến GDP thô vào biểu đồ tán xạ hoặc mô hình tuyến tính sẽ khiến các quốc gia nhỏ bị dồn cục lại ở góc đồ thị và làm bóp méo trọng số hồi quy.
* **Công thức toán học:** Áp dụng hàm logarit tự nhiên mở rộng $\ln(1+x)$:
  $$\text{gdp\_log} = \ln(1 + \text{gdp\_value})$$
  *(Sử dụng $\ln(1+x)$ thay vì $\ln(x)$ để bảo đảm tính liên tục và xác định toán học ngay cả khi giá trị tiến gần $0$).*
* **Mã nguồn thực thi Python (`src/data_loader.py`):**
  ```python
  df["gdp_log"] = np.log1p(df["gdp_value"]).round(3)
  ```
* **Ứng dụng:** Trực quan hóa tương quan giữa quy mô kinh tế và hành vi tiêu thụ âm nhạc, chuẩn hóa đầu vào cho các thuật toán phân tích đa biến.

---

#### 12. `chart_year` & `chart_month` — Bóc Tách Thành Phần Thời Gian Tuần BXH
* **Phương pháp:** Trích xuất các thành phần năm và tháng từ chuỗi ngày bắt đầu của tuần ghi nhận BXH (`chart_week` có định dạng chuẩn `YYYY-MM-DD`). 
  - Việc đổi tên thành `chart_year` và `chart_month` thay vì để `year` và `month` đơn thuần giúp phân định tuyệt đối rõ ràng giữa **Thời điểm ghi nhận thứ hạng trên BXH** và **Năm phát hành gốc của ca khúc** (`release_date` hoặc `year` trong bảng `songs.csv`).
* **Công thức toán học:**
  $$\text{chart\_year} = \text{dt.year}(\text{chart\_week}) \in \{2020, 2021, 2022\}$$
  $$\text{chart\_month} = \text{dt.month}(\text{chart\_week}) \in \{1, 2, \dots, 12\}$$
* **Mã nguồn thực thi Python (`src/data_loader.py`):**
  ```python
  df["chart_week"] = pd.to_datetime(df["chart_week"], errors="coerce")
  df["chart_year"] = df["chart_week"].dt.year.astype("Int64")
  df["chart_month"] = df["chart_week"].dt.month.astype("Int64")
  ```
* **Ứng dụng:** Xây dựng bộ lọc thời gian trên Dashboard, khảo sát xu hướng phân bổ lượt nghe theo mùa (ví dụ: các ca khúc giáng sinh của Mariah Carey hay Wham! bùng nổ mạnh mẽ vào `chart_month` = 11, 12 hàng năm).

---

## 6. ĐÁNH GIÁ CHẤT LƯỢNG DỮ LIỆU, ĐỘ TIN CẬY MÔ HÌNH & CẢNH BÁO RÒ RỈ CHO ML

### 6.1. Đánh giá chất lượng dữ liệu sau tiền xử lý
* **Độ sạch Missing Values:** Toàn bộ các trường phân tích trọng tâm đều đạt 100% dữ liệu sạch: `song_genre` (0% NA), `song_popularity` (0% NA), `artist_popularity` (0% NA). Audio features chỉ khuyết 0.01% (do Spotify chưa lập chỉ mục một số bài hiếm), GDP chỉ khuyết 4.19% (hoàn toàn thuộc về bảng xếp hạng `Global`), `artist_followers_raw` giữ nguyên 63.1% từ hồ sơ nghệ sĩ gốc.
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
> * Thuộc tính bài hát: `duration_min`, `song_genre`, `macro_genre`, `tempo_category`.
> * Thuộc tính nghệ sĩ tiền phát hành: `artist_popularity` (kèm cờ `artist_popularity_is_imputed`) hoặc `artist_followers_raw`.

---

## 7. HƯỚNG DẪN TRUY XUẤT DỮ LIỆU THÔNG QUA PYTHON API

Mô-đun `src/data_loader.py` cung cấp sẵn các hàm tiện ích chuẩn hóa:

```python
# 1. Nạp Master Dataset (spotify.csv):
from src.data_loader import load_master_data

df = load_master_data()  # hoặc load_master_data(nrows=50000)
print(f"Master Dataset: {df.shape}")  # (1,078,125 dòng, 44 cột)

# Kiểm tra phân bố độ phổ biến theo trạng thái lập chỉ mục:
print(df.groupby("has_song_popularity")["song_popularity"].describe())

# 2. Nạp dữ liệu Song-level cho Machine Learning:
from src.data_loader import load_ml_data

df_ml = load_ml_data()
print(f"ML Dataset: {df_ml.shape}")   # (36,699 bài hát, 26 cột)
print(f"Tỷ lệ bài Hit (is_trending=1): {df_ml['is_trending'].mean():.1%}")
```
