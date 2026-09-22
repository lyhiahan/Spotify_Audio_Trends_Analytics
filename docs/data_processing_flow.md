# 🔄 TÀI LIỆU KIẾN TRÚC LUỒNG XỬ LÝ DỮ LIỆU HỢP NHẤT
## (UNIFIED MASTER DATA PROCESSING PIPELINE ARCHITECTURE)

* **Môn học:** Tương tác Dữ liệu (Interactive Data Visualization / Visual Analytics)
* **Đề tài:** Nghiên cứu & Trực quan hóa Đặc trưng Âm thanh và Dự đoán Xu hướng Thịnh hành trên Spotify
* **Người thực hiện:** Đinh Quốc Anh (MSSV: 24133003) — Vai trò: Data Engineer & Data Analyst
* **Module kỹ thuật:** [`src/data_loader.py`](file:///d:/uni/hk1nam3/idvi/idvi-final_project/Spotify_Audio_Trends_Analytics/src/data_loader.py) & [`notebooks/01_preprocess.ipynb`](file:///d:/uni/hk1nam3/idvi/idvi-final_project/Spotify_Audio_Trends_Analytics/notebooks/01_preprocess.ipynb)
* **Phiên bản tài liệu:** 3.4 (Master Dataset 38 Cột — sửa macro_genre, bỏ 3 cột yếu, thêm 2 cột mới, ML Dataset 19 Cột)

---

## MỤC LỤC
1. [TỔNG QUAN KIẾN TRÚC MASTER DATASET HỢP NHẤT](#1-tổng-quan-kiến-trúc-master-dataset-hợp-nhất)
2. [ĐẶC TẢ CHI TIẾT CÁC GIAI ĐOẠN XỬ LÝ](#2-đặc-tả-chi-tiết-các-giai-đoạn-xử-lý)
   * [Giai đoạn 1: Nạp và Làm sạch độc lập 5 bảng dữ liệu thô](#giai-đoạn-1-nạp-và-làm-sạch-độc-lập-5-bảng-dữ-liệu-thô)
   * [Giai đoạn 2: Hợp nhất Master Dataset (4 phép LEFT JOIN có thứ tự)](#giai-đoạn-2-hợp-nhất-master-dataset-4-phép-left-join-có-thứ-tự)
   * [Giai đoạn 3: Tính toán 9 Calculated Fields & Lọc 38 Cột Insight](#giai-đoạn-3-tính-toán-9-calculated-fields--lọc-38-cột-insight)
   * [Giai đoạn 4: Trích xuất Dữ liệu Cấp Bài hát Chống Rò rỉ cho Machine Learning](#giai-đoạn-4-trích-xuất-dữ-liệu-cấp-bài-hát-chống-rò-rỉ-cho-machine-learning)
3. [CÔNG THỨC TOÁN HỌC & Ý NGHĨA 9 CALCULATED FIELDS](#3-công-thức-toán-học--ý-nghĩa-9-calculated-fields)
4. [ĐẶC TẢ LƯỢC ĐỒ 38 CỘT PHỤC VỤ CÁC BÀI TOÁN INSIGHT](#4-đặc-tả-lược-đồ-38-cột-phục-vụ-các-bài-toán-insight)
5. [HƯỚNG DẪN THỰC THI & TÍCH HỢP HỆ THỐNG](#5-hướng-dẫn-thực-thi--tích-hợp-hệ-thống)
6. [ĐỐI CHIẾU TIÊU CHÍ BAREM CHẤM ĐIỂM (RUBRIC ALIGNMENT)](#6-đối-chiếu-tiêu-chí-barem-chấm-điểm-rubric-alignment)

---

## 1. TỔNG QUAN KIẾN TRÚC MASTER DATASET HỢP NHẤT

Hệ thống ETL được thiết kế tối ưu theo mô hình **Hợp nhất Dữ liệu Toàn diện (Unified Master Pipeline)**:
* **Tệp Master duy nhất (`merged_spotify_data.csv`):** Tích hợp số liệu Kinh tế - Xã hội 73 quốc gia và bảng Global, chuẩn hóa dòng nhạc vĩ mô `macro_genre` bằng regex word boundary (`\b`) chỉ dựa trên genre (KHÔNG dùng `language`), lưu giữ đúng **38 cột phục vụ Insight**.
* **Tệp dữ liệu ML (`tracks_ml_data.csv`):** Tinh gọn ở cấp độ bài hát (Song-level, 36,699 dòng × 19 cột) với nhãn `is_trending`, triệt tiêu hoàn toàn nguy cơ rò rỉ dữ liệu (Data Leakage).

```mermaid
flowchart TD
    subgraph S1["1. NGUỒN DỮ LIỆU THÔ (DATA/RAW/)"]
        RAW_C["spotify-weekly-charts.csv<br/>1.78M dòng × 36 cột (796.6 MB)"]
        RAW_T["spotify-tracks-dataset.csv<br/>114K dòng × 22 cột (19.8 MB)"]
        RAW_G["gdp_data.csv<br/>13.3K dòng × 4 cột (395 KB)"]
        RAW_CC["country_codes.csv<br/>217 dòng × 3 cột (8 KB)"]
        RAW_A["best-selling-artists.csv<br/>121 dòng × 7 cột (16 KB)"]
    end

    subgraph S2["2. TIỀN XỬ LÝ ĐỘC LẬP TỪNG BẢNG (DATA CLEANING)"]
        CLEAN_C["clean_raw_charts()<br/>• Trích track_id từ URI, ép kiểu 9 audio features<br/>• Clip audio [0,1], loudness [-60,5], tempo [0,300]<br/>• Parse week (year, month), lọc streams <= 0<br/>• Dedup (track_id, week, country), loại 15 cột rác"]
        CLEAN_T["clean_raw_tracks()<br/>• Dedup track_id theo popularity cao nhất<br/>• Chỉ giữ: track_id, track_genre, popularity, explicit"]
        CLEAN_A["clean_raw_artists()<br/>• Clean artist name (lower, strip)"]
        CLEAN_G["clean_raw_gdp()<br/>• Chuẩn hóa: country_name, year, gdp_value"]
        CLEAN_CC["clean_raw_country_codes()<br/>• Chuẩn hóa: country_code, region_wb, income_group<br/>• Bổ sung TWN chuẩn World Bank"]
    end

    subgraph S3["3. XÂY DỰNG MASTER DATASET (4 PHÉP LEFT JOIN)"]
        BUILD["build_master_dataset()<br/>• Lọc chuỗi thời gian trọng tâm 2020-2022 (1.07M dòng)<br/>• Ánh xạ tên 7 nước chuẩn World Bank<br/>• JOIN 1: Charts ⋈ GDP (country_code, year)<br/>• JOIN 2: + Country Codes (country_code)<br/>• JOIN 3: + Tracks Dataset (track_id)<br/>• JOIN 4: + Best-Selling Artists (artist_clean)<br/>• Tính toán 9 Calculated Fields, macro_genre (word boundary)<br/>• Ổn định macro_genre per track_id (mode)<br/>• Lọc chuẩn hóa chính xác 38 cột cốt lõi"]
    end

    subgraph S4["4. CÁC TỆP DỮ LIỆU ĐẦU RA"]
        OUT_M["data/processed/merged_spotify_data.csv<br/>1,078,125 dòng × 38 cột (~308 MB)<br/>★ Master Dataset chứa toàn bộ Insight đồ án"]
        OUT_S2["data/processed/tracks_ml_data.csv<br/>36,699 bài hát × 19 cột (~5.5 MB)<br/>★ Phục vụ: Thành Tài train Logistic & Linear Regression"]
    end

    RAW_C --> CLEAN_C
    RAW_T --> CLEAN_T
    RAW_A --> CLEAN_A
    RAW_G --> CLEAN_G
    RAW_CC --> CLEAN_CC

    CLEAN_C & CLEAN_G & CLEAN_CC & CLEAN_T & CLEAN_A --> BUILD

    BUILD --> OUT_M
    BUILD --> OUT_S2
```

---

## 2. ĐẶC TẢ CHI TIẾT CÁC GIAI ĐOẠN XỬ LÝ

### Giai đoạn 1: Nạp và Làm sạch độc lập 5 bảng dữ liệu thô

* **1. `clean_raw_charts()`:**
  - Loại bỏ các cột chỉ mục thừa (`Unnamed: 0`).
  - Trích xuất `track_id` chuẩn (22 ký tự) từ chuỗi `spotify:track:<track_id>`.
  - Chuyển trường `week` sang định dạng `Datetime`, bóc tách các thành phần thời gian: `year`, `month`.
  - Ép kiểu số nguyên cho `streams`, loại bỏ triệt để các bản ghi có `streams <= 0`.
  - Ép kiểu số thực tường minh cho 9 đặc trưng âm học (`danceability`, `energy`, `loudness`, `speechiness`, `acousticness`, `instrumentalness`, `liveness`, `valence`, `tempo`).
  - **Clip giá trị về đúng miền vật lý:** 7 audio features $[0, 1]$, `loudness` $[-60, 5]$ dB, `tempo` $[0, 300]$ BPM.
  - Khử trùng lặp bản ghi trên bộ ba khóa định danh `(track_id, week, country)`.
  - Loại bỏ sớm 15 cột phụ không phục vụ insight: `uri`, `artist_names`, `artists_num`, `artist_id`, `key`, `mode`, `source`, `album_num_tracks`, `collab`, `release_date`, `previous_rank`, `artist_img`, `album_cover`, `pivot`, `region`.

* **2. `clean_raw_tracks()`:**
  - Sắp xếp theo `popularity` giảm dần và khử trùng lặp theo `track_id` (chỉ giữ bản ghi có độ phổ biến cao nhất, từ 114,000 còn 89,741 bài hát độc nhất).
  - Lọc chỉ giữ lại các trường cốt lõi phục vụ JOIN: `track_id`, `track_genre`, `popularity`, `explicit` (audio features đến từ charts, clip thực hiện ở `clean_raw_charts()`).

* **3. `clean_raw_artists()`:**
  - Chuẩn hóa tên nghệ sĩ về chữ thường không dấu cách thừa (`artist_name_clean = lower().strip()`).

* **4. `clean_raw_gdp()` & `clean_raw_country_codes()`:**
  - Chuẩn hóa tên trường thống nhất: `gdp_value`, `region_wb`, `income_group`.
  - Bổ sung bản ghi cho Đài Loan (`TWN`, `High income`, `East Asia & Pacific`).

---

### Giai đoạn 2: Hợp nhất Master Dataset (4 phép LEFT JOIN có thứ tự)

* **Lọc chuỗi thời gian trọng tâm (2020 – 2022):**
  - Giữ lại 1,078,125 dòng bao quát đầy đủ cả giai đoạn đại dịch COVID-19 (bắt đầu từ 2020 trên bảng `Global`) và dữ liệu 73 quốc gia (từ 2021 đến 2022).
* **4 phép LEFT JOIN tuần tự:**
  1. *Charts ⋈ GDP* trên cặp khóa `(country_code, year)` sau khi chuẩn hóa 7 quốc gia World Bank (`Korea, Rep.`, `Turkiye`, `Czechia`, `Hong Kong SAR, China`, `Egypt, Arab Rep.`, `Slovak Republic`, `Venezuela, RB`): Bổ sung chỉ số kinh tế `gdp_value`. Với các dòng quốc gia, tỷ lệ khớp GDP đạt **98.23%**. Riêng dòng `Global` nhận giá trị `NaN` ở GDP là hoàn toàn chính xác về mặt ý nghĩa kinh tế (vì Global không phải là một quốc gia).
  2. *+ Country Codes* trên khóa `country_code`: Bổ sung khu vực địa lý (`region_wb`) và phân tầng thu nhập (`income_group`), đạt tỷ lệ khớp **100%** (0 dòng thiếu).
  3. *+ Tracks Dataset* trên khóa `track_id`: Bổ sung thể loại âm nhạc (`track_genre`), điểm phổ biến toàn cầu (`popularity`) và cờ nhạy cảm (`explicit`).
  4. *+ Best-Selling Artists* trên tên nghệ sĩ chuẩn hóa `artist_individual`: Đánh dấu nghệ sĩ di sản (`is_legacy_artist`).

---

### Giai đoạn 3: Tính toán 9 Calculated Fields & Lọc 38 Cột Insight

* Tính toán đầy đủ 9 biến phái sinh:
  - `macro_genre`: Chuẩn hóa 6 dòng nhạc vĩ mô bằng regex có **word boundary (`\b`)**, **KHÔNG dùng `language`** (vì đó là ngôn ngữ thị trường BXH, không phải ngôn ngữ bài hát). Ổn định 1 nhãn duy nhất per `track_id` bằng mode.
  - `mood_category` (4 góc phần tư Russell: *Happy Energetic*, *Peaceful Positive*, *Tense Aggressive*, *Sad Melancholic*, *Unknown* khi thiếu audio).
  - `chart_longevity` (max weeks_on_chart per track_id), `tempo_category` (Slow/Medium/Fast/Very Fast).
  - `stream_share_country`, `is_legacy_artist`, `duration_min`, `is_trending`, `gdp_log`.
* **Loại bỏ 5 cột gây rò rỉ/thiên lệch/yếu:**
  - `log_streams`: Biến dẫn xuất thuần túy $\ln(1 + \text{streams})$.
  - `covid_phase`: Trùng lẫn hoàn toàn với thực thể Global năm 2020.
  - `is_popular`: 66% NaN do thiếu `popularity` → gán sai 0.
  - `energy_loudness_index`: `energy` và `loudness` tương quan cao ($r \approx 0.8$), trung bình 2 biến không tạo insight mới.
  - `audio_diversity_score`: StdDev 4 features cherry-picked thiếu cơ sở, `valence` leak khi dùng làm ML target.
* **Lọc chuẩn hóa chính xác 38 cột cốt lõi phục vụ Insight** và lưu thành tệp: `data/processed/merged_spotify_data.csv` (1,078,125 dòng × 38 cột, dung lượng ~308 MB).

---

### Giai đoạn 4: Trích xuất Dữ liệu Cấp Bài hát Chống Rò rỉ cho Machine Learning

* **`tracks_ml_data.csv` (36,699 bài hát độc nhất × 19 cột, dung lượng ~5.5 MB):**
  - Lưu tại: `data/processed/tracks_ml_data.csv`.
  - Gom nhóm (groupby) theo `track_id` độc nhất từ tập bài hát trong Master Dataset.
  - **Chống rò rỉ dữ liệu (Data Leakage):** Mỗi bài hát chỉ xuất hiện duy nhất 1 dòng. Tách hoàn toàn các biến kết quả sau phát hành (`country`, `week`, `year`, `streams`, `stream_share_country`, `weeks_on_chart`, `peak_rank`).
  - **Cột categorical dùng `mode`** (giá trị xuất hiện nhiều nhất) thay vì `first` cho `artist_genre` và `language` — đảm bảo ổn định.
  - Nhãn mục tiêu ($y$): `is_trending = 1` nếu bài hát từng lọt vào Top 50 BXH bất kỳ, $0$ nếu chỉ ở Top 51–200 (Tỷ lệ nhãn Hit: **35.9%** rất cân bằng).
  - **⚠ Lưu ý:** `chart_longevity` là biến hậu phát hành — KHÔNG dùng làm feature ML, chỉ dùng cho EDA.
  - Phục vụ Đỗ Thanh Thành Tài huấn luyện mô hình Logistic & Linear Regression.

---

## 3. CÔNG THỨC TOÁN HỌC & Ý NGHĨA 9 CALCULATED FIELDS

| STT | Trường tính toán | Quy tắc logic / Công thức toán học | Ý nghĩa phân tích & Trực quan |
| :---: | :--- | :--- | :--- |
| 1 | `is_trending` | $$\text{is\_trending} = \mathbb{I}(\text{rank} \le 50)$$ | Biến mục tiêu phân loại Top Hit cho mô hình Machine Learning. |
| 2 | `mood_category` | $$\begin{cases} \text{Happy Energetic} & \text{valence} \ge 0.5 \land \text{energy} \ge 0.5 \\ \text{Peaceful Positive} & \text{valence} \ge 0.5 \land \text{energy} < 0.5 \\ \text{Tense Aggressive} & \text{valence} < 0.5 \land \text{energy} \ge 0.5 \\ \text{Sad Melancholic} & \text{valence} < 0.5 \land \text{energy} < 0.5 \\ \text{Unknown} & \text{valence hoặc energy là NaN} \end{cases}$$ | Phân loại **đặc tính cảm xúc bài hát** (không phải tâm trạng người nghe) 4 góc phần tư Russell. |
| 3 | `stream_share_country` | $$\text{share}_{i, c, w} = \frac{\text{streams}_{i, c, w}}{\sum_{k \in \text{Top200}(c, w)} \text{streams}_{k, c, w}}$$ | Đo lường thị phần chi phối lượt nghe của bài hát tại thị trường trong tuần. |
| 4 | `macro_genre` | Phân loại ưu tiên 6 nhóm bằng regex có word boundary (`\b`):<br>• **K-Pop:** `\b(k-pop\|kpop\|k pop\|k-rap)\b`<br>• **Latin:** `\b(latin\|reggaeton\|salsa\|...)\b`<br>• **Hip-Hop/Rap:** `\b(hip hop\|hip-hop\|rap\|trap)\b`<br>• **Rock/Metal:** `\b(rock\|metal\|punk)\b`<br>• **Pop:** `\b(pop\|electropop)\b`<br>• **Others:** Các trường hợp còn lại<br>**⚠ KHÔNG dùng `language`** (ngôn ngữ thị trường). Ổn định per track_id bằng mode. | Danh mục dòng nhạc vĩ mô đồng nhất, ổn định 1 nhãn cho mỗi bài hát. |
| 5 | `is_legacy_artist` | $$\mathbb{I}(\text{legacy\_artist\_name is not Null})$$ | Khảo sát mức độ trụ hạng của nghệ sĩ huyền thoại (The Beatles, Queen). |
| 6 | `duration_min` | $$\text{duration\_min} = \frac{\text{duration}}{60{,}000}$$ | Thời lượng bài hát tính theo phút phục vụ nghiên cứu xu hướng rút ngắn track. |
| 7 | `chart_longevity` | $$\text{chart\_longevity} = \max_{\text{per track\_id}}(\text{weeks\_on\_chart})$$ | Số tuần trụ hạng cao nhất — phân biệt flash hit vs evergreen. |
| 8 | `tempo_category` | $$\begin{cases} \text{Slow} & \text{tempo} < 90 \\ \text{Medium} & 90 \le \text{tempo} < 120 \\ \text{Fast} & 120 \le \text{tempo} < 150 \\ \text{Very Fast} & \text{tempo} \ge 150 \end{cases}$$ | Phân nhóm tốc độ nhịp phục vụ trực quan hóa trên Dashboard. |
| 9 | `gdp_log` | $$\text{gdp\_log} = \ln(1 + \text{gdp\_value})$$ | Nén biên độ GDP hàng nghìn tỷ USD phục vụ vẽ biểu đồ phân tán Scatter Plot. |

---

## 4. ĐẶC TẢ LƯỢC ĐỒ 38 CỘT PHỤC VỤ CÁC BÀI TOÁN INSIGHT

Cấu trúc 38 cột của Master Dataset phân bố thành 5 cụm:
* **Nhóm 1 — Định danh, Không gian & Thời gian (9 cột):** `track_id`, `track_name`, `artist_individual`, `artist_genre`, `country`, `language`, `week`, `year`, `month`.
* **Nhóm 2 — Xếp hạng & Lượt nghe (4 cột):** `rank`, `streams`, `weeks_on_chart`, `peak_rank`.
* **Nhóm 3 — 9 Audio Features (9 cột):** `danceability`, `energy`, `loudness`, `speechiness`, `acousticness`, `instrumentalness`, `liveness`, `valence`, `tempo`.
* **Nhóm 4 — Kinh tế World Bank (5 cột):** `gdp_value`, `gdp_log`, `income_group`, `region_wb`, `country_code`.
* **Nhóm 5 — Trường tính toán & Bổ trợ Insight (11 cột):** `is_trending`, `mood_category`, `stream_share_country`, `macro_genre`, `is_legacy_artist`, `duration_min`, `chart_longevity`, `tempo_category`, `track_genre`, `popularity`, `explicit`.

---

## 5. HƯỚNG DẪN THỰC THI & TÍCH HỢP HỆ THỐNG

### 5.1. Thực thi toàn bộ Pipeline từ dòng lệnh:
```bash
# Tự động nạp, làm sạch và xuất Master Dataset + tệp dữ liệu ML:
python src/data_loader.py
```

### 5.2. Các hàm nạp dữ liệu tiện ích (Dành cho Dashboard và Notebooks):
```python
from src.data_loader import (
    load_master_data,   # Nạp file Master 38 cột (merged_spotify_data.csv ~308 MB)
    load_ml_data        # Nạp file dữ liệu bài hát cho Thành Tài làm ML (tracks_ml_data.csv ~4.8 MB)
)

# Ví dụ nạp dữ liệu Master:
df_master = load_master_data()

# Ví dụ nạp dữ liệu huấn luyện ML:
df_ml = load_ml_data()
```

---

## 6. ĐỐI CHIẾU TIÊU CHÍ BAREM CHẤM ĐIỂM (RUBRIC ALIGNMENT)

| Tiêu chí Barem | Điểm tối đa | Mức độ đáp ứng của Pipeline mới | Bằng chứng thực nghiệm |
| :--- | :---: | :--- | :--- |
| **Xác định bài toán & Dataset** | **0.5 đ** | • Sử dụng **5 tập dữ liệu đa nguồn** (>1.9 triệu dòng thô).<br>• Từ điển dữ liệu chuẩn xác chi tiết trong `docs/data_dictionary.md`. | `load_raw_data()`<br>`docs/data_dictionary.md` |
| **Làm sạch dữ liệu (Data Cleaning)** | **0.5 đ** | • Xử lý triệt để missing, loại `streams <= 0`.<br>• Khử trùng lặp đa khóa, clip boundary âm học $[0, 1]$.<br>• Chuẩn hóa tên 7 quốc gia World Bank và gán mã ISO-3 (khớp 98.2% GDP, 0 dòng thiếu income_group). | `clean_raw_charts()`<br>`clean_raw_tracks()`<br>`clean_raw_country_codes()` |
| **Biến đổi dữ liệu (Feature Engineering & Join)** | **0.75 đ** | • **Kiến trúc Master Dataset** tích hợp 4 phép LEFT JOIN.<br>• Giữ chuẩn xác **38 cột phục vụ Insight**.<br>• Chuẩn hóa **`macro_genre`** (word boundary, ổn định per track_id) và **9 Calculated Fields**. | `build_master_dataset()`<br>`generate_ml_dataset()` |
| **Khám phá dữ liệu (EDA tĩnh)** | **0.75 đ** | • Notebook `02_eda.ipynb` tích hợp **8 biểu đồ tĩnh** Seaborn/Matplotlib chuẩn mực tập trung chuyên sâu vào phân tích phân phối & xu hướng theo đúng barem: (1) Phân phối 9 đặc trưng âm học 3x3 kèm Skewness & Kurtosis, (2) Phân phối Lượt nghe Streams & Biến đổi $\ln(1+\text{streams})$, (3) Ma trận tương quan Pearson & Cặp tương quan mạnh, (4) Boxplot Hit vs Non-hit kèm kiểm định Mann-Whitney U & Cohen's d, (5) Xu hướng biến động tăng/giảm theo chuỗi thời gian 2020 - 2022, (6) So sánh phân phối 6 dòng nhạc vĩ mô `macro_genre` qua Violin plots, (7) Phân tích Vòng đời Trụ hạng Flash Hit (1-2 tuần) vs Evergreen (>20 tuần) qua `chart_longevity`, (8) Phân tích Nhịp độ âm nhạc `tempo_category` & Khả năng bứt phá Top Hit. | `notebooks/02_eda.ipynb` |

---
*Tài liệu được cập nhật hoàn chỉnh phục vụ báo cáo Đồ án môn học Tương tác Dữ liệu — Nhóm Spotify Audio Trends Analytics.*
