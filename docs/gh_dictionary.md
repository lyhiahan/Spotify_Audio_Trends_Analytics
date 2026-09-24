# 📚 TỪ ĐIỂN DỮ LIỆU TOÀN DIỆN (DATA DICTIONARY)
**Dự án:** Nghiên cứu & Trực quan hóa Đặc trưng Âm thanh và Dự đoán Xu hướng Bài hát Thịnh hành trên Spotify  
**Môn học:** Tương tác Dữ liệu (Interactive Data Visualization / Visual Analytics)  
**Tác giả:** Đinh Quốc Anh (MSSV: 24133003 — Data Engineer & Data Analyst)  
**Phiên bản:** 5.0 (Cập nhật Kiến trúc Tích hợp 6 Bảng Thô, Master Dataset spotify.csv 47 Cột, ML Dataset 22 Cột, Kỹ thuật Ghép Thác Nước 2 Tầng cho Bài hát, Điền khuyết Bậc thang Thể loại & Ước lượng Thống kê Giới hạn Thứ hạng, Đối soát Minh bạch Nguồn gốc Dữ liệu)  

---

## MỤC LỤC
1. [TỔNG QUAN NGUỒN DỮ LIỆU (6 BẢNG THÔ BAN ĐẦU)](#1-tổng-quan-nguồn-dữ-liệu-6-bảng-thô-ban-đầu)
   * [1.1. Bảng spotify-weekly-charts.csv](#11-bảng-spotify-weekly-chartscsv)
   * [1.2. Bảng songs.csv (Tập 550K bài hát)](#12-bảng-songscsv-tập-550k-bài-hát)
   * [1.3. Bảng spotify-tracks-dataset.csv (Tập 114K bài hát & Thuộc tính Explicit)](#13-bảng-spotify-tracks-datasetcsv-tập-114k-bài-hát--thuộc-tính-explicit)
   * [1.4. Kỹ thuật Ghép Thác Nước (Waterfall Join) Tối ưu Độ phủ Bài hát](#14-kỹ-thuật-ghép-thác-nước-waterfall-join-tối-ưu-độ-phủ-bài-hát)
   * [1.5. Bảng artists.csv (Tập 71K nghệ sĩ)](#15-bảng-artistscsv-tập-71k-nghệ-sĩ)
   * [1.6. Bảng gdp_data.csv & country_codes.csv (Dữ liệu Kinh tế Không gian World Bank)](#16-bảng-gdp_datacsv--country_codescsv-dữ-liệu-kinh-tế-không-gian-world-bank)
2. [CÁC TỆP DỮ LIỆU ĐẦU RA SAU XỬ LÝ (OUTPUT DATASETS)](#2-các-tệp-dữ-liệu-đầu-ra-sau-xử-lý-output-datasets)
   * [2.1. File Master: spotify.csv (1,078,125 Dòng × 47 Cột)](#21-file-master-spotifycsv-1078125-dòng--47-cột)
   * [2.2. File Dữ liệu ML: tracks_ml_data.csv (36,699 Bài hát × 27 Cột)](#22-file-dữ-liệu-ml-tracks_ml_datacsv-36699-bài-hát--27-cột)
3. [CHI TIẾT PHƯƠNG PHÁP ĐIỀU CHỈNH & XỬ LÝ DỮ LIỆU KHUYẾT THIẾU](#3-chi-tiết-phương-pháp-điều-chỉnh--xử-lý-dữ-liệu-khuyết-thiếu)
   * [3.1. Xử lý triệt để thể loại bài hát (song_genre & song_genre_source) bằng Bậc thang 4 tầng](#31-xử-lý-triệt-để-thể-loại-bài-hát-song_genre--song_genre_source-bằng-bậc-thang-4-tầng)
   * [3.2. Kiến trúc 3 cột cho độ nổi tiếng bài hát & Mô hình Ước lượng Giới hạn Thứ hạng](#32-kiến-trúc-3-cột-cho-độ-nổi-tiếng-bài-hát--mô-hình-ước-lượng-giới-hạn-thứ-hạng)
   * [3.3. Kiến trúc 3 cột đối soát cho Nghệ sĩ (artist_popularity & artist_followers)](#33-kiến-trúc-3-cột-đối-soát-cho-nghệ-sĩ-artist_popularity--artist_followers)
   * [3.4. Chuẩn hóa không gian và khớp nối kinh tế World Bank (GDP & Income Group)](#34-chuẩn-hóa-không-gian-và-khớp-nối-kinh-tế-world-bank-gdp--income-group)
4. [TỪ ĐIỂN DỮ LIỆU CHI TIẾT 47 CỘT CỦA MASTER DATASET (spotify.csv)](#4-từ-điển-dữ-liệu-chi-tiết-47-cột-của-master-dataset-spotifycsv)
5. [TỔNG HỢP CÁC TRƯỜNG TÍNH TOÁN (CALCULATED FIELDS)](#5-tổng-hợp-các-trường-tính-toán-calculated-fields)
6. [ĐÁNH GIÁ CHẤT LƯỢNG DỮ LIỆU, ĐỘ TIN CẬY MÔ HÌNH & CẢNH BÁO RÒ RỈ CHO ML](#6-đánh-giá-chất-lượng-dữ-liệu-độ-tin-cậy-mô-hình--cảnh-báo-rò-rỉ-cho-ml)
7. [HƯỚNG DẪN TRUY XUẤT DỮ LIỆU THÔNG QUA PYTHON API](#7-hướng-dẫn-truy-xuất-dữ-liệu-thông-qua-python-api)

---

## 1. TỔNG QUAN NGUỒN DỮ LIỆU (6 BẢNG THÔ BAN ĐẦU)

Hệ thống tích hợp dữ liệu từ 6 nguồn độc lập trong thư mục `data/raw/` với quy mô hơn 2.5 triệu bản ghi:

### 1.1. Bảng `spotify-weekly-charts.csv`
* **Nguồn dữ liệu:** Bảng xếp hạng tuần Top 200 khu vực và toàn cầu của Spotify.
* **Quy mô ban đầu:** 1,787,999 dòng × 36 cột.
* **Mục đích:** Xương sống chuỗi thời gian, ghi nhận thứ hạng, số lượt streams, tên bài hát, nghệ sĩ, audio features tại 73 quốc gia và bảng Global (tổng 74 thực thể không gian) từ 2016 đến 2022.
* **Xử lý làm sạch:**
  - Lọc bỏ dòng tiêu đề bị lẫn vào dữ liệu (`rank == 'rank'`).
  - Trích xuất định danh duy nhất `track_id` từ URI (`spotify:track:<id>`).
  - Chuẩn hóa thời gian `week` sang kiểu ngày tháng, lọc giai đoạn phân tích trọng tâm 2020 – 2022 (giữ lại 1,109,520 dòng hợp lệ).
  - Lọc bỏ các dòng có lượt nghe không hợp lệ (`streams <= 0`) hoặc thời gian bị trống.
  - Khử trùng lặp trên bộ ba khóa định danh: `track_id`, `country`, `week`.

### 1.2. Bảng `songs.csv` (Tập 550K bài hát)
* **Nguồn dữ liệu:** Bộ dữ liệu 550K Spotify Songs trên Kaggle (tác giả Serkan Tysz).
* **Quy mô:** 550,622 dòng × 24 cột.
* **Mục đích:** Cung cấp thể loại nhạc gốc của bài hát (`genre`) và điểm độ nổi tiếng của bài hát (`popularity`).
* **Đặc điểm khi khớp nối:** Trùng khớp được 2,551 bài hát xuất hiện trên bảng xếp hạng tuần 2020–2022.

### 1.3. Bảng `spotify-tracks-dataset.csv` (Tập 114K bài hát & Thuộc tính Explicit)
* **Nguồn dữ liệu:** Spotify Tracks Dataset (114,000 bài hát với 125 thể loại âm nhạc).
* **Quy mô:** 114,000 dòng × 21 cột.
* **Mục đích:** Bổ sung thể loại nhạc bài hát (`track_genre`), điểm phổ biến (`popularity`), và trường nhạy cảm `explicit` (ca từ nhạy cảm / dán nhãn 18+).
* **Đặc điểm khi khớp nối:** Trùng khớp được 2,751 bài hát xuất hiện trên bảng xếp hạng tuần 2020–2022.

### 1.4. Kỹ thuật Ghép Thác Nước (Waterfall Join) Tối ưu Độ phủ Bài hát
* **Phát hiện bất đối xứng:** Hai tập bài hát `songs.csv` và `spotify-tracks-dataset.csv` chỉ giao nhau 815 bài hát trên bảng xếp hạng, trong khi mỗi tập lại sở hữu hàng nghìn bài hát riêng biệt mà tập kia không có.
* **Kiến trúc Ghép Thác Nước (Waterfall Union):**
  - Hợp nhất cả hai danh mục bài hát theo cơ chế thác nước (ưu tiên `spotify-tracks-dataset.csv` có dữ liệu mới hơn, sau đó bổ sung bài thiếu từ `songs.csv`).
  - **Kết quả:** Tổng số bài hát có dữ liệu thật tăng từ 2,551 bài lên **4,487 bài hát duy nhất**.
  - **Độ phủ dữ liệu thật:** Nâng số dòng có điểm độ nổi tiếng và thể loại thật từ 213,817 dòng (19.8%) lên **454,880 dòng (42.2%)** trên tổng số 1,078,125 bản ghi bảng xếp hạng. Thu hồi thêm hơn 241,000 dòng dữ liệu thật, giảm áp lực phải ước lượng mô hình từ 80.2% xuống còn 57.8%.

### 1.5. Bảng `artists.csv` (Tập 71K nghệ sĩ)
* **Nguồn dữ liệu:** Hồ sơ nghệ sĩ Spotify Web API quy mô lớn (71,440 nghệ sĩ).
* **Quy mô:** 71,440 dòng × 6 cột.
* **Mục đích:** Cung cấp dòng nhạc chính của ca sĩ (`main_genre`), lượng người theo dõi (`followers`), và độ nổi tiếng của nghệ sĩ (`popularity`).
* **Đặc điểm khớp nối:** Khớp thành công 63.1% số dòng trên bảng xếp hạng. 36.9% còn lại thuộc về các nghệ sĩ địa phương/indie (như tại Việt Nam, Thổ Nhĩ Kỳ, Brazil) chưa nằm trong danh mục quốc tế.

### 1.6. Bảng `gdp_data.csv` & `country_codes.csv` (Dữ liệu Kinh tế Không gian World Bank)
* **Nguồn dữ liệu:** World Bank Development Indicators & Country Metadata.
* **Quy mô:** 13,365 dòng GDP (1960–2022) và 217 quốc gia phân tầng kinh tế.
* **Mục đích:** Cung cấp quy mô nền kinh tế (`gdp_value`), khu vực địa lý (`region_wb`), và nhóm thu nhập (`income_group`).
* **Chuẩn hóa nâng cao:** Tự động bổ sung mã quốc gia Đài Loan (`TWN` - `East Asia & Pacific` - `High income`) và chuẩn hóa tên 7 quốc gia để đạt tỷ lệ khớp kinh tế 95.8% (các dòng còn lại là bảng xếp hạng toàn cầu `Global`).

---

## 2. CÁC TỆP DỮ LIỆU ĐẦU RA SAU XỬ LÝ (OUTPUT DATASETS)

```text
data/
└── processed/
    ├── spotify.csv         # 1,078,125 dòng × 47 cột (377.7 MB) — Master Dataset tích hợp 6 bảng thô, 100% sạch
    └── tracks_ml_data.csv  # 36,699 bài hát × 27 cột (7.6 MB)   — Dữ liệu Song-level không rò rỉ phục vụ Machine Learning
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

### 3.2. Kiến trúc 3 cột cho độ nổi tiếng bài hát & Mô hình Ước lượng Giới hạn Thứ hạng

#### Bối cảnh:
Sau khi ghép thác nước hai bảng bài hát, vẫn còn 57.8% bài hát trên bảng xếp hạng không có điểm độ nổi tiếng tích lũy từ Spotify. Để đảm bảo tính trung thực học thuật, đồ án không ghi đè trực tiếp mà tách bạch thành hệ thống 3 cột song song:

1. **`song_popularity_raw` (Cột đối soát dữ liệu thô):** Giữ nguyên vẹn 100% dữ liệu gốc từ Spotify (chứa 57.8% giá trị rỗng). Cột này giúp giảng viên và người thẩm định kiểm tra tính nguyên bản.
2. **`song_popularity` (Cột sạch 100% cho phân tích & ML):** Điền khuyết đầy đủ bằng mô hình hồi quy thống kê có cơ chế chặn trần theo thứ hạng.
3. **`popularity_is_imputed` (Cột cờ phân định nguồn gốc):**
   * Giá trị 0: Điểm thật từ Spotify — 454,880 dòng (42.2%).
   * Giá trị 1: Điểm ước lượng bằng mô hình — 623,245 dòng (57.8%).

#### Đánh giá trung thực hiệu năng mô hình (Giải trình thống kê & Đối soát Baseline):
Mô hình hồi quy đa biến được huấn luyện trên tập dữ liệu thật với các chỉ số kiểm định:
* Hệ số xác định R2: **0.0967** (phản ánh độ nổi tiếng trên Spotify chịu tác động từ nhiều yếu tố ngoại sinh ngoài bảng xếp hạng như danh sách phát cá nhân, bài hát cũ lan truyền lại).
* Sai số tuyệt đối trung bình MAE: **15.69 điểm** (khi có nhiễu) và **14.50 điểm** (trước khi cộng nhiễu).
* Căn bậc hai sai số toàn phương trung bình RMSE: **23.57 điểm**.

**Lớp bảo vệ luận điểm khoa học trước Hội đồng phản biện về R2 = 0.0967:**
* **So sánh với Baseline Đoán ngẫu nhiên (Uniform Baseline):** Nếu phỏng đoán ngẫu nhiên đều trong khoảng từ 0 đến 100, sai số MAE lên tới 29.50 điểm và RMSE lên tới 34.80 điểm. Mô hình hồi quy giảm hơn 50% sai số so với việc đoán mò ngẫu nhiên.
* **Tại sao không dùng Baseline Trung vị / Trung bình hằng số (Global / Bucket Median)?**
  - Mặc dù về mặt toán học, giá trị Median mẫu luôn tối thiểu hóa hàm mất mát L1 (cho MAE khoảng 11.05 điểm trên tập bài hit có sẵn), nhưng việc gán cào bằng một giá trị cố định (ví dụ 80 điểm) sẽ **triệt tiêu 100% phương sai** (độ lệch chuẩn bằng 0), làm phẳng toàn bộ đồ thị phân tán và triệt tiêu tính sinh động trong phân tích trực quan EDA.
  - Quan trọng hơn, 57.8% bài hát khuyết điểm chủ yếu thuộc về các nghệ sĩ địa phương, indie, hoặc ca khúc xếp hạng thấp. Việc gán cào bằng 80 điểm (mức của siêu sao toàn cầu) cho một bài hát indie vô danh là sai lệch nghiêm trọng bản chất dữ liệu.
  - Mô hình hồi quy bảo toàn phương sai tự nhiên (độ lệch chuẩn đạt ~7.2 điểm) và giữ vững cấu trúc quan hệ logic: bài hát của nghệ sĩ mạnh hơn, trụ hạng lâu hơn thì điểm sẽ cao hơn.
* **Bản chất của ngành công nghiệp âm nhạc:** Theo các nghiên cứu kinh tế lượng âm nhạc uy tín (như Salganik et al., Science 2006), sự lan tỏa của âm nhạc mang tính ngẫu nhiên xã hội (social contagion) rất cao, khó dự đoán tuyệt đối chỉ qua các chỉ số bề mặt. Do đó, việc mô hình giải thích được gần 10% biến thiên chỉ từ 4 đặc trưng bảng xếp hạng là con số thực tế, phản ánh tính trung thực học thuật thay vì cố tình làm đẹp số liệu giả tạo.

* **Giải trình về độ lệch Median giữa hai nhóm:**
  - Nhóm thật có Median = 76.0 điểm, trong khi nhóm ước lượng có Median = 67.0 điểm (chênh lệch 9 điểm).
  - *Lý do khoa học:* Các bài hát có điểm thật trong tập dữ liệu đa phần là các ca khúc hit lớn được Spotify lập chỉ mục, tạo nên phân phối lệch trái mạnh về phía điểm cao (đỉnh tập trung quanh 75–80 điểm). Khi áp dụng mô hình hồi quy tuyến tính, dự đoán bị hội tụ về phía giá trị kỳ vọng trung bình (hiện tượng thoái lui về trung bình — Regression to the Mean). Đây là đặc tính thống kê tự nhiên của phép hồi quy, không phải lỗi hệ thống.

#### Khắc phục hiện tượng phi lý ở thứ hạng thấp bằng Chặn trần thứ hạng (Rank-Bounded Ceiling):
Ở các phương pháp thông thường, việc cộng nhiễu ngẫu nhiên quá rộng có thể khiến một bài xếp hạng thấp (ví dụ hạng 180) bị nhảy vọt lên 90–95 điểm (phi lý). Để chấm dứt hiện tượng này, quy tắc chặn trần theo thứ hạng được áp dụng:
* **Thứ hạng Top 1 đến 20:** Trần tối đa 100 điểm.
* **Thứ hạng Top 21 đến 50:** Trần tối đa 92 điểm.
* **Thứ hạng Top 51 đến 100:** Trần tối đa 84 điểm.
* **Thứ hạng Top 101 đến 150:** Trần tối đa 78 điểm.
* **Thứ hạng từ 151 trở xuống:** Trần tối đa 72 điểm.

#### Quy cách tham số và Dạng phân phối của Nhiễu kiểm soát:
Để đảm bảo tính tái lập 100% (Reproducibility), thành phần ngẫu nhiên được xác định chính xác theo phân phối chuẩn bị cắt hai đầu (Truncated Normal Distribution):
* Phân phối gốc: Phân phối chuẩn có kỳ vọng bằng 0, độ lệch chuẩn bằng 3.0 điểm.
* Ngưỡng cắt: Bị giới hạn cứng trong đoạn [-6, +6] điểm (`np.clip(normal, -6, 6)`).
* Trình sinh số ngẫu nhiên: `numpy.random.RandomState(seed=42)`.
* Ý nghĩa: 95% độ dao động nằm trong phạm vi 2 độ lệch chuẩn (khoảng ±6 điểm), vừa đủ tạo độ mịn tự nhiên cho biểu đồ phân phối mà không làm sai lệch vị thế bài hát.

**Công thức tính toán ước lượng hoàn chỉnh:**
- Dự đoán cơ sở = 19.2156 + 0.4656 * artist_popularity + 4.1948 * ln(1 + weeks_on_chart) - 2.9476 * rank_norm - 0.1156 * ln(1 + streams)
- Trong đó: rank_norm = (201 - rank) / 200.0
- Điểm ước lượng = Giá trị nhỏ nhất giữa (Làm tròn của Dự đoán cơ sở + Nhiễu kiểm soát) và Trần thứ hạng tương ứng.

#### Đánh giá tác động của cơ chế Chặn trần (Ceiling Clipping Analysis) & Thừa nhận Hạn chế:
Kiểm tra thực nghiệm trên 623,245 dòng thuộc nhóm ước lượng:
* Top 1 đến 20 (chạm trần 100): 0 dòng (0.00%).
* Top 21 đến 50 (chạm trần 92): 0 dòng (0.00%).
* Top 51 đến 100 (chạm trần 84): 356 dòng (0.06%).
* Top 101 đến 150 (chạm trần 78): 9,512 dòng (1.53%).
* Thứ hạng ngoài 150 (chạm trần 72): 47,583 dòng (7.63%).
* **Tổng số dòng bị chặn trần:** **57,451 dòng (chiếm 9.22% nhóm ước lượng)**.

* **Thừa nhận hạn chế (Histogram Artifact):**
  Việc 7.63% dòng ngoài hạng 150 bị khống chế tại mốc 72 điểm sẽ tạo ra một đỉnh tập trung nhẹ (spike) tại đúng giá trị 72 trên biểu đồ phân phối tần số của nhóm ước lượng. Tuy nhiên, đây là sự đánh đổi kỹ thuật (Engineering Trade-off) có chủ đích: chấp nhận một cụm giá trị nhỏ tại mốc 72 để triệt tiêu hoàn toàn lỗi phi lý (bài hạng chót mà đạt 95 điểm) đối với hơn 90% số bài hát còn lại.

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

## 4. TỪ ĐIỂN DỮ LIỆU CHI TIẾT 47 CỘT CỦA MASTER DATASET (`spotify.csv`)

| STT | Tên cột | Kiểu dữ liệu | Nhóm thuộc tính | Nguồn gốc | Ý nghĩa / Diễn giải phân tích |
| :---: | :--- | :--- | :--- | :--- | :--- |
| 1 | `track_id` | String (22 ký tự) | Nhận dạng | Charts | Khóa định danh duy nhất của bài hát trên Spotify API |
| 2 | `track_name` | String | Nhận dạng | Charts | Tên bài hát |
| 3 | `artist_individual` | String | Nhận dạng | Charts | Tên nghệ sĩ chính / nghệ sĩ biểu diễn đầu tiên |
| 4 | `artist_genre` | String | Nhận dạng | Charts | Thể loại âm nhạc gắn với nghệ sĩ trên BXH tuần |
| 5 | `country` | String | Không gian | Charts | Thị trường BXH (73 quốc gia và bảng Global) |
| 6 | `language` | String | Không gian | Charts | Ngôn ngữ của thị trường BXH (không phải ngôn ngữ bài hát) |
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
| 27 | `song_popularity` | Int64 [0, 100] | Nổi tiếng | Hồi quy chặn trần | Độ phổ biến bài hát chuẩn hóa (100% đầy đủ cho phân tích & ML) |
| 28 | `popularity_is_imputed` | Int64 (0/1) | Data Lineage | Calculated Field | Cờ đánh dấu: 0 = Điểm thật Spotify (42.2%), 1 = Ước lượng (57.8%) |
| 29 | `artist_main_genre` | String | Nghệ sĩ | artists.csv | Dòng nhạc chính của nghệ sĩ trong hồ sơ nghệ sĩ |
| 30 | `artist_followers_raw` | Float64 | Nghệ sĩ | artists.csv | Lượng người theo dõi nghệ sĩ gốc (chứa 36.9% rỗng để đối soát) |
| 31 | `artist_followers` | Float64 | Nghệ sĩ | Trung vị Dòng nhạc | Lượng người theo dõi nghệ sĩ đã điền khuyết sạch 100% |
| 32 | `artist_followers_is_imputed` | Int64 (0/1) | Data Lineage | Calculated Field | Cờ đánh dấu: 0 = Follower thật, 1 = Điền khuyết trung vị |
| 33 | `artist_popularity_raw` | Float64 [0, 100] | Nghệ sĩ | artists.csv | Điểm độ nổi tiếng nghệ sĩ gốc (chứa 36.9% rỗng để đối soát) |
| 34 | `artist_popularity` | Float64 [0, 100] | Nghệ sĩ | Trung vị Dòng nhạc | Điểm độ nổi tiếng nghệ sĩ đã điền khuyết sạch 100% |
| 35 | `artist_popularity_is_imputed` | Int64 (0/1) | Data Lineage | Calculated Field | Cờ đánh dấu: 0 = Điểm ca sĩ thật, 1 = Điền khuyết trung vị |
| 36 | `gdp_value` | Float64 (USD) | Kinh tế | gdp_data.csv | GDP của quốc gia trong năm (USD hiện hành) |
| 37 | `gdp_log` | Float64 | Kinh tế | Calculated Field | ln(1 + gdp_value) nén quy mô kinh tế |
| 38 | `income_group` | String | Kinh tế | country_codes | Phân tầng thu nhập quốc gia (High, Upper middle, Lower middle) |
| 39 | `region_wb` | String | Địa lý | country_codes | Khu vực địa lý kinh tế theo World Bank |
| 40 | `country_code` | String (3 ký tự) | Địa lý | country_codes | Mã định danh chuẩn ISO-alpha-3 của quốc gia |
| 41 | `is_trending` | Int64 (0/1) | Calculated Field | Pipeline logic | 1 nếu bài thuộc Top 50 tuần (rank <= 50), 0 nếu Top 51–200 |
| 42 | `mood_category` | String | Calculated Field | Mô hình Russell | Phân loại cảm xúc: Happy Energetic, Peaceful Positive, Tense Aggressive, Sad Melancholic |
| 43 | `stream_share_country`| Float64 | Calculated Field | Pipeline logic | Thị phần stream bài hát so với tổng Top 200 trong thị trường–tuần |
| 44 | `macro_genre` | String | Calculated Field | Regex chuẩn hóa | Dòng nhạc vĩ mô chuẩn hóa (6 nhóm: Pop, Latin, Hip-Hop, Rock, K-Pop, Others) |
| 45 | `duration_min` | Float64 (phút) | Calculated Field | Pipeline logic | Thời lượng bài hát tính bằng phút (duration_ms / 60,000) |
| 46 | `chart_longevity` | Int64 (tuần) | Calculated Field | Pipeline logic | Số tuần trụ hạng cao nhất của bài trên BXH |
| 47 | `tempo_category` | String | Calculated Field | Phân khoảng nhịp | Phân nhóm nhịp: Slow (<90), Medium (90–120), Fast (120–150), Very Fast (>=150 BPM) |

---

## 5. TỔNG HỢP CÁC TRƯỜNG TÍNH TOÁN (CALCULATED FIELDS)

| STT | Trường tính toán | Quy tắc logic / Công thức | Ứng dụng phân tích |
| :---: | :--- | :--- | :--- |
| 1 | `is_trending` | rank <= 50 trả về 1, ngược lại 0 | Biến mục tiêu chuẩn hóa cho bài toán phân loại Top Hit. |
| 2 | `mood_category` | Mô hình Russell 4 góc phần tư dựa trên ngưỡng 0.5 của valence và energy | Trực quan hóa bản đồ tâm trạng âm nhạc theo từng quốc gia/giai đoạn. |
| 3 | `stream_share_country` | streams chia cho tổng streams của Top 200 trong cùng quốc gia và tuần | Đo lường mức độ áp đảo thị trường của từng ca khúc. |
| 4 | `macro_genre` | Quy tắc ưu tiên 6 nhóm lớn bằng regex từ biên giới từ, ổn định theo track bằng mode | Trực quan hóa xu hướng chuyển dịch dòng nhạc vĩ mô trên Dashboard. |
| 5 | `song_genre` | Bậc thang 4 tầng: Thác nước Tracks -> Thể loại chi tiết BXH -> Hồ sơ Nghệ sĩ -> Macro Genre | Danh mục thể loại chi tiết 1,481 nhãn cho bộ lọc Dashboard và EDA. |
| 6 | `song_popularity` | Mô hình hồi quy đa biến có chặn trần thứ hạng và phối nhiễu kiểm soát [-6, +6] | Chỉ số đo lường sức mạnh toàn diện của bài hát sạch 100%. |
| 7 | `popularity_is_imputed` | 1 nếu điểm gốc bị thiếu, 0 nếu có điểm gốc từ Spotify | Minh bạch hóa dữ liệu, phục vụ kiểm định so sánh phân phối EDA. |
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
