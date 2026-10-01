# TỪ ĐIỂN DỮ LIỆU ĐỒ ÁN IDVI (DATA DICTIONARY)
**Dự án:** Trực quan hóa dữ liệu tương tác — Khảo sát xu hướng âm nhạc số Spotify trong bối cảnh đại dịch COVID-19 và kinh tế vĩ mô toàn cầu  
**Thời gian cập nhật:** Tháng 10/2026  
**Phạm vi tài liệu:** Ghi nhận cấu trúc chi tiết của 5 tập tin dữ liệu thô tại `data/raw/`, 5 tập tin dữ liệu sạch cốt lõi và 4 tập tin Data Marts tinh gọn tại `data/processed/` phục vụ trực tiếp 3 Dashboard và bài toán Machine Learning, được xử lý đồng bộ từ notebook [`notebooks/test_preprocess.ipynb`](file:///d:/uni/hk1nam3/idvi/idvi-final_project/project-indv/notebooks/test_preprocess.ipynb).

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
   - [5.1. Chú thích 12 Đặc Trưng Âm Học Spotify](#51-chú-thích-12-đặc-trưng-âm-học-spotify)
   - [5.2. Chú thích Công Thức Tính pop_score & Cân Bằng Nhãn ML](#52-chú-thích-công-thức-tính-pop_score--cân-bằng-nhãn-ml)
   - [5.3. Chú thích Phòng Chống Rò Rỉ Dữ Liệu (Data Leakage)](#53-chú-thích-phòng-chống-rò-rỉ-dữ-liệu-data-leakage)
   - [5.4. Chú thích Bước Nhảy Thang Đo Báo Cáo Hạnh Phúc WHS](#54-chú-thích-bước-nhảy-thang-đo-báo-cáo-hạnh-phúc-whs)
   - [5.5. Chú thích Đồng Bộ Thời Gian COVID-19 & Số Ca Tử Vong Âm](#55-chú-thích-đồng-bộ-thời-gian-covid-19--số-ca-tử-vong-âm)
   - [5.6. Chú thích Về Hiện Tượng Collab & Hai Dòng Mismatch Bodø Domkor](#56-chú-thích-về-hiện-tượng-collab--hai-dòng-mismatch-bodø-domkor)

---

## 1. DỮ LIỆU THÔ (RAW DATA - `data/raw/`)

### 1.1. `spotify-weekly-charts.csv`
- **Dung lượng:** 796.63 MB
- **Kích thước:** 1,787,999 dòng, 36 cột.
- **Mô tả:** Bảng xếp hạng Top 200 ca khúc hàng tuần trên 73 quốc gia và thị trường Global từ ngày 29/12/2016 đến ngày 14/07/2022.
- **Lưu ý chất lượng:** Chứa 73 dòng header rác (`rank == 'rank'`); có 395 dòng khuyết toàn bộ 12 đặc trưng âm học (thuộc 12 ca khúc duy nhất, đã loại bỏ); cột `uri` và `artist_id` chứa tiền tố `spotify:track:` và `spotify:artist:`.

### 1.2. `global_deaths.csv`
- **Dung lượng:** 2.05 MB
- **Kích thước:** 289 dòng (thực thể/tỉnh bang), 1,144 cột (ngày từ 22/01/2020 đến 09/03/2023).
- **Mô tả:** Dữ liệu số ca tử vong tích lũy do COVID-19 toàn cầu từ Đại học Johns Hopkins (JHU CSSE).
- **Lưu ý chất lượng:** Cần gộp dữ liệu tỉnh bang về quốc gia, xử lý Hong Kong tách khỏi Trung Quốc, chuyển đổi dạng ngang sang dạng dọc, tính toán số ca tử vong ngày và đồng bộ theo tuần chốt thứ Năm của Spotify.

### 1.3. `gdp_data.csv`
- **Dung lượng:** 350.77 KB
- **Kích thước:** 11,508 dòng, 4 cột (`country_name`, `country_code`, `year`, `value`).
- **Mô tả:** Dữ liệu tổng sản phẩm quốc nội (GDP theo USD hiện giá) từ World Bank giai đoạn 1960–2022.
- **Lưu ý chất lượng:** Chứa cả 217 quốc gia độc lập và 48 nhóm khu vực kinh tế tổng hợp vĩ mô.

### 1.4. `country_codes.csv`
- **Dung lượng:** 14.16 KB
- **Kích thước:** 218 dòng, 3 cột (`country_code`, `region`, `income_group`).
- **Mô tả:** Phân loại địa lý và nhóm thu nhập kinh tế của World Bank theo chuẩn mã ISO Alpha-3.

### 1.5. `whs_years_updated.csv`
- **Dung lượng:** 241.13 KB
- **Kích thước:** 1,511 dòng, 47 cột.
- **Mô tả:** Tổng hợp 10 ấn bản Báo cáo Hạnh phúc Thế giới (World Happiness Report) từ năm 2015 đến năm 2024.
- **Lưu ý chất lượng:** Các năm sử dụng tên cột và thang đo nhân tố phân rã khác nhau; năm 2022 có 2 dòng Cyprus (một dòng điểm thấp là Bắc Síp). Cần sử dụng `happiness_score` làm biến so sánh liên năm chính và chuẩn hóa Z-score cho 6 nhân tố.

---

## 2. DỮ LIỆU SẠCH CỐT LÕI (CORE PROCESSED DATA - `data/processed/`)

### 2.1. `charts_clean.parquet`
- **Dung lượng:** 64.9 MB (định dạng nén tối ưu, thay thế file CSV 469MB).
- **Kích thước:** 1,787,531 dòng, 34 cột.
- **Cấp độ hạt (Grain):** `(track_id, artist_id, chart_country, week)`. Khóa duy nhất 100%.
- **Các trường chính:** `track_id`, `track_name`, `artist_id`, `artist_names`, `artists_num`, `artist_genre`, `week`, `year`, `month`, `chart_country`, `chart_region`, `chart_language`, `rank`, `previous_rank`, `is_new_entry`, `peak_rank`, `weeks_on_chart`, `streams`, `release_date_clean`, `release_year`, `days_to_chart`, cùng 12 đặc trưng âm học chuẩn (`danceability`, `energy`, `key`, `mode`, `loudness`, `speechiness`, `acousticness`, `instrumentalness`, `liveness`, `valence`, `tempo`, `duration`).

### 2.2. `tracks_dimension.csv`
- **Dung lượng:** 7.55 MB
- **Kích thước:** 39,190 dòng, 21 cột.
- **Cấp độ hạt (Grain):** `track_id` duy nhất 100%.
- **Mô tả:** Lưu trữ siêu dữ liệu (`artist_id`, `artist_names`, `artists_num`, `artist_genre`, `release_year`, `release_date_clean`) và 12 đặc trưng âm học không đổi của từng bài hát.

### 2.3. `country_lookup.csv`
- **Dung lượng:** 6.06 KB
- **Kích thước:** 73 dòng, 8 cột.
- **Cấp độ hạt (Grain):** `chart_country` duy nhất 100%.
- **Mô tả:** Bảng cầu nối liên kết 73 quốc gia Spotify với siêu dữ liệu World Bank và thuộc tính bảng xếp hạng.
- **Các trường:** `chart_country`, `country_code`, `wb_country_name`, `wb_region`, `wb_income_group`, `chart_region`, `chart_language`, `n_weeks`.

### 2.4. `covid_weekly_clean.csv`
- **Dung lượng:** 358 KB
- **Kích thước:** 12,136 dòng, 4 cột.
- **Cấp độ hạt (Grain):** `(country, week)`. Khóa duy nhất 100%.
- **Mô tả:** Số ca tử vong tuần được lọc tinh gọn cho đúng 74 thực thể phân tích (73 quốc gia Spotify và Global).
- **Các trường:** `country`, `week`, `weekly_deaths`, `cumulative_deaths`.

### 2.5. `whs_clean.csv`
- **Dung lượng:** 151.5 KB
- **Kích thước:** 1,510 dòng, 10 cột.
- **Cấp độ hạt (Grain):** `(country, year)`. Khóa duy nhất 100%.
- **Các trường:** `country`, `year`, `happiness_rank`, `happiness_score`, `gdp_factor`, `social_support`, `healthy_life`, `freedom`, `generosity`, `corruption`.

---

## 3. DỮ LIỆU DATA MARTS (DASHBOARD & MACHINE LEARNING)

Nhằm tối ưu hóa hiệu năng, loại bỏ độ trễ tính toán trực tiếp từ bảng 65MB, toàn bộ các chỉ số phân tích được tổng hợp sẵn thành 4 bảng Data Marts:

### 3.1. `mart_audio_trend_weekly.parquet` (Dashboard 1 & 3)
- **Dung lượng:** 1.13 MB
- **Kích thước:** 5,548 dòng, 29 cột.
- **Cấp độ hạt (Grain):** `(chart_country, week)`.
- **Mô tả:** Xu hướng âm nhạc theo tuần của 73 quốc gia và Global sau khi đã loại bỏ nhân bản collab.
- **Các trường:**
  * Khóa: `chart_country`, `week`.
  * Khối lượng: `total_streams`, `track_count`, `new_entries`.
  * 12 Đặc trưng âm học trung bình thường: `danceability_mean`, `energy_mean`, ..., `duration_mean`.
  * 12 Đặc trưng âm học có trọng số lượt nghe: `danceability_weighted`, `energy_weighted`, ..., `duration_weighted`.

### 3.2. `mart_artist_chart.parquet` (Dashboard 1 - 0% NaN)
- **Dung lượng:** 826 KB
- **Kích thước:** 15,254 dòng, 7 cột.
- **Cấp độ hạt (Grain):** `artist_id`.
- **Mô tả:** Thống kê thành tích trên BXH của các nghệ sĩ có ca khúc lọt Top 200, **trích xuất trực tiếp từ bảng xếp hạng sạch với 100% đầy đủ tên nghệ sĩ và thể loại (0% giá trị khuyết thiếu)**.
- **Các trường:** `artist_id`, `artist_name`, `artist_genre`, `chart_streams`, `n_chart_tracks`, `peak_rank`, `weeks_on_chart`.

### 3.3. `mart_country_year.parquet` (Dashboard 2)
- **Dung lượng:** 65.6 KB
- **Kích thước:** 141 dòng, 42 cột.
- **Cấp độ hạt (Grain):** `(chart_country, year)`. Khớp đúng 141 cặp quốc gia - năm của Spotify Charts.
- **Mô tả:** Ghép nối đặc trưng âm học năm của từng quốc gia với điểm số hạnh phúc thế giới WHS và siêu dữ liệu địa lý kinh tế.
- **Các trường:** `chart_country`, `year`, `yearly_streams`, `slot_count`, `n_weeks`, 12 chỉ số audio unweighted & weighted, `country_code`, `wb_region`, `wb_income_group`, `chart_region`, `chart_language`, `happiness_rank`, `happiness_score`, cùng 6 nhân tố WHS.

### 3.4. `ml_tracks.parquet` & `ml_tracks.csv` (Machine Learning - 0% NaN)
- **Dung lượng:** 4.27 MB (Parquet) / 9.50 MB (CSV).
- **Kích thước:** 39,190 dòng, 30 cột.
- **Cấp độ hạt (Grain):** `track_id` duy nhất 100%.
- **Mô tả:** Tập dữ liệu phục vụ huấn luyện mô hình Hồi quy (Ridge / Linear Regression) và Phân loại (Logistic Regression), **bảo đảm 0% khuyết thiếu trên toàn bộ các cột**.
- **Phân tách biến nghiêm ngặt tránh rò rỉ dữ liệu (Data Leakage):**
  * **Biến mục tiêu ($Y$):**
    - `pop_score`: Biến liên tục (0–100) cho bài toán Hồi quy.
    - `is_hit`: Biến nhị phân cân bằng (ngưỡng $\ge 50$ điểm, chiếm **13.9%** tổng bài hát, giải quyết triệt để mất cân bằng cực đoan).
    - `is_mega_hit`: Biến nhị phân hiện tượng toàn cầu (ngưỡng $\ge 70$ điểm, chiếm **1.6%**).
    - `hit_tier`: Phân loại 4 mức ordinal (*Niche*, *Moderate*, *Popular*, *Mega Hit*).
  * **Biến hậu nghiệm (Chỉ để kiểm chứng, cấm đưa vào $X$):** `peak_rank`, `nweek`, `total_streams`, `n_countries`.
  * **Đặc trưng dự báo hợp lệ ($X$):** 12 đặc trưng âm học nội tại (`danceability`, `energy`, `valence`...), `artists_num`, `artist_genre`, `release_year`, `release_month`.

---

## 4. BẢNG KHÓA GHÉP NỐI & QUAN HỆ THỰC THỂ

| Bảng nguồn A | Bảng đích B | Khóa ghép nối | Kiểu quan hệ | Mục đích |
| :--- | :--- | :--- | :--- | :--- |
| `charts_clean` | `tracks_dimension`| `track_id` | N : 1 | Tra cứu 12 chỉ số âm học nội tại và phát hành của bài hát |
| `mart_audio_trend_weekly` | `covid_weekly_clean` | `(chart_country = country, week)` | 1 : 1 | Phân tích biến động âm nhạc theo ca tử vong COVID-19 |
| `mart_country_year` | `whs_clean` | `(chart_country = country, year)` | 1 : 1 | Đo lường tương quan giữa hạnh phúc và gu âm nhạc |
| `mart_country_year` | `country_lookup` | `chart_country` | N : 1 | Bổ sung khu vực địa lý `wb_region` và nhóm thu nhập |
| `tracks_dimension` | `ml_tracks` | `track_id` | 1 : 1 | Cung cấp đầu vào đặc trưng âm học cho mô hình ML |

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
   *Đo lường khả năng viral đỉnh cao.* Ca khúc đạt vị trí #1 nhận điểm số 1.0; ca khúc chạm rank #200 nhận điểm số 0.0.
2. **Sức bền trên BXH ($s_{\text{weeks}}$ - Trọng số 25%):**
   $$s_{\text{weeks}} = \frac{\min(\text{nweek}, Q_{0.99})}{Q_{0.99}}$$
   *Đo lường tuổi thọ ca khúc.* Được cắt trần (cap) tại percentile 99% để triệt tiêu ảnh hưởng của các ngoại lai cực đoan (như các ca khúc trụ bảng hơn 100 tuần kéo giãn phân bố).
3. **Độ phủ quốc tế ($s_{\text{countries}}$ - Trọng số 20%):**
   $$s_{\text{countries}} = \frac{\text{n\_countries}}{73}$$
   *Đo lường tầm ảnh hưởng toàn cầu.* Số quốc gia độc lập ca khúc xuất hiện (chỉ đếm 73 quốc gia thực tế, loại trừ Global), chia cho tối đa 73.
4. **Quy mô người nghe ($s_{\text{streams}}$ - Trọng số 25%):**
   $$s_{\text{streams}} = \frac{\log(1 + \text{total\_streams}) - \min(\log)}{\max(\log) - \min(\log)}$$
   *Đo lường sức hấp dẫn thương mại.* Áp dụng biến đổi Logarit trước khi chuẩn hóa Min-Max để đưa phân bố lượt nghe (vốn lệch phải cực nặng theo luật lũy thừa - Power Law) về phân bố đối xứng cân bằng.

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
