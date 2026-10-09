# LUỒNG TIỀN XỬ LÝ DỮ LIỆU TẦNG LÕI (CORE DATA PROCESSING FLOW)

Tài liệu này mô tả chi tiết kiến trúc và toàn bộ tiến trình xử lý dữ liệu thực tế đang được triển khai trong notebook [`notebooks/01_preprocess.ipynb`](../notebooks/01_preprocess.ipynb) của dự án Tương tác dữ liệu trực quan (IDVI).

Luồng xử lý được thiết kế theo nguyên tắc:

1. **Module `src/data_loader.py` tinh gọn:** Chỉ đảm nhiệm nạp dữ liệu thô từ đĩa, kiểm tra tính tồn tại của file và lưu trữ các hằng số tham chiếu chuẩn hóa.
2. **Notebook kiểm soát toàn diện:** Mọi logic làm sạch sâu, biến đổi cấu trúc, kiểm tra cấp độ hạt (grain verification), trích xuất đặc trưng và xuất tập tin sạch cốt lõi và các bảng Data Marts được thực hiện minh bạch từng bước, tuân thủ nghiêm ngặt quy tắc phong cách (mỗi ô một việc, có markdown giải thích, kiểm tra assertion trước/sau).
3. **Kiến trúc dữ liệu phân tầng tinh gọn (Data Lakehouse / Medallion Pattern):**
   * **Tầng Bronze (Raw Data):** 5 tập tin dữ liệu thô ban đầu (~800MB bảng xếp hạng, dữ liệu dịch tễ, GDP, mã quốc gia, WHS).
   * **Tầng Silver (Clean Tables):** Chỉ lưu trữ các bảng sạch cốt lõi ở định dạng tối ưu (`charts_clean.parquet`, `tracks_dimension.csv`, `country_lookup.csv`, `covid_weekly_clean.csv`). Dữ liệu WHS được làm sạch trong bộ nhớ (`df_whs_clean`) để ghép nối trực tiếp sang Data Mart.
   * **Tầng Gold (Data Marts):** Tổng hợp sẵn các chỉ số thống kê phục vụ trực tiếp Dashboard 1, 2, 3 (`mart_audio_trend_weekly.parquet`, `mart_artist_chart.parquet` / `.csv`, `mart_country_year.parquet`). Dữ liệu Machine Learning được trích xuất độc lập từ `charts_clean.parquet` tại `03_model.ipynb`.

---

## 1. SƠ ĐỒ LUỒNG XỬ LÝ TỔNG THỂ (MERMAID FLOWCHART)

```mermaid
flowchart TD
    subgraph S0["Nguồn Dữ Liệu Thô (data/raw/)"]
        R1["spotify-weekly-charts.csv<br/>(~797MB, 1.78M dòng, 36 cột)"]
        R2["global_deaths.csv<br/>(2.05MB, 289 thực thể, 1,144 ngày)"]
        R3["country_codes.csv<br/>(14KB, 218 dòng, 3 cột)"]
        R4["gdp_data.csv<br/>(351KB, 11.5k dòng, 4 cột)"]
        R5["whs_years_updated.csv<br/>(241KB, 1,511 dòng, 47 cột)"]
    end

    subgraph S1["Module 1 & 2: Làm Sạch & Kiểm Tra Hạt Bảng Xếp Hạng"]
        B1["load_charts_raw()<br/>- Đọc theo chunk 500k dòng (29 cột)<br/>- Loại bỏ 73 dòng header rác<br/>- Ép kiểu int64, int32, float32, datetime"]
        B2["Làm sạch sâu & Tối ưu kiểu dữ liệu:<br/>- Tách track_id & artist_id (22 ký tự)<br/>- Tạo is_new_entry & previous_rank Int16<br/>- Ép Int8 cho key/mode; category cho địa lý/thể loại<br/>- Loại bỏ 395 dòng thiếu audio (12 bài)<br/>- Lọc 34 cột chuẩn"]
        B3["Kiểm tra Cấp độ hạt & Tính bất biến:<br/>- Assert khóa hạt (track_id, artist_id, country, week) duy nhất 100%<br/>- Hiển thị 2 nhóm mismatch Bodø Domkor do nghệ sĩ N/A<br/>- Assert 100% tuần chốt vào thứ Năm<br/>- Assert 12 audio features + release_date hằng số theo track<br/>- Xuất tracks_dimension.csv (39,190 bài hát)<br/>- Xuất charts_clean.parquet (65MB, không xuất CSV 470MB)"]
        B1 --> B2 --> B3
    end

    subgraph S2["Module 3 & 4: Chuẩn Hóa Mã & Dữ Liệu GDP Vĩ Mô"]
        B4["load_country_codes_raw() & load_gdp_raw()<br/>- Chuẩn hóa wb_region, wb_income_group<br/>- Tách 217 quốc gia độc lập và 48 nhóm khu vực tổng hợp vĩ mô trong bộ nhớ"]
    end

    subgraph S3["Module 5: Xây Dựng & Làm Giàu Bảng Cầu Nối Quốc Gia"]
        B5["Xây dựng country_lookup:<br/>- Ghép tên World Bank với mã ISO-3<br/>- Ánh xạ 7 alias và assert tường minh Đài Loan (TWN)<br/>- Làm giàu thêm chart_region, chart_language, n_weeks từ charts<br/>- Xuất country_lookup.csv (73 quốc gia, 8 cột)"]
        B4 --> B5
    end

    subgraph S4["Module 6: Chuẩn Hóa Dữ Liệu Tử Vong COVID-19"]
        B6["load_covid_raw()<br/>- Melt bảng ngang sang dọc (1,143 ngày)<br/>- Tách Hong Kong, gộp bang về quốc gia<br/>- Đồng bộ tuần thứ Năm theo Spotify<br/>- Tạo chuỗi Global, bảo toàn tổng 6,881,785 ca tử vong<br/>- Lọc giữ đúng 74 thực thể (73 nước + Global)<br/>- Xuất covid_weekly_clean.csv (12,136 dòng)"]
    end

    subgraph S5["Module 7: Chuẩn Hóa Báo Cáo Hạnh Phúc WHS (In-Memory)"]
        B7["load_whs_raw()<br/>- Thống kê phân bố 10 năm (2015-2024)<br/>- Nhận diện bước nhảy thang đo nhân tố phân rã giữa 2021-2022<br/>- Sử dụng happiness_score làm biến chuẩn liên năm<br/>- Đổi tên Bắc Síp năm 2022 và ánh xạ 6 alias (60 dòng)<br/>- Lưu df_whs_clean trong bộ nhớ (1,510 dòng, 10 cột)"]
    end

    subgraph S6["Module 8: Kiểm Tra Chéo Độc Lập (Cross-Validation)"]
        B8["Thẩm định ghép nối:<br/>- COVID: 100% tuần đại dịch khớp, 160 tuần trước dịch thuộc Global<br/>- WHS: Khớp 141/141 cặp quốc gia - năm (100%)<br/>- GDP: Khớp 138/141 cặp quốc gia - năm (97.9%)"]
        B3 --> B8
        B5 --> B8
        B6 --> B8
        B7 --> B8
    end

    subgraph S7["Module 9: Xây Dựng 3 Bảng Data Marts Tinh Gọn (01_preprocess)"]
        M1["mart_audio_trend_weekly.parquet<br/>(5,548 dòng, 29 cột)<br/>- Deduplicate slot vị trí xếp hạng<br/>- Tính Unweighted & Streams-Weighted Audio Means<br/>- Dùng cho Dashboard 1 & 3"]
        M2["mart_artist_chart.parquet<br/>(15,254 dòng, 10 cột)<br/>- Trích xuất 100% từ charts_clean<br/>- Tổng streams, n_tracks, peak_rank, n_weeks, genre<br/>- Dùng cho Dashboard 1"]
        M3["mart_country_year.parquet<br/>(141 dòng, 42 cột)<br/>- Ghép audio năm với country_lookup & df_whs_clean<br/>- Dùng cho Dashboard 2"]
        B3 --> M1
        B3 --> M2
        B3 --> M3
        B5 --> M3
        B7 --> M3
    end

    subgraph S8["Phân Hệ Machine Learning Độc Lập (03_model.ipynb)"]
        ML1["Dự báo Global Top 50 trong 8 tuần<br/>- Đọc trực tiếp charts_clean.parquet<br/>- 12 biến X: 10 audio + rank_first_week + log_streams_first_week<br/>- Biến mục tiêu Y: hit_next_8_weeks<br/>- Mô hình Logistic Regression<br/>- Báo cáo: reports/global_top50_first_week/"]
        B3 -.-> ML1
    end
```

---

## 2. NGUYÊN TẮC THIẾT KẾ CÁC BẢNG DATA MARTS VÀ PHÒNG CHỐNG DATA LEAKAGE

### 2.1. Bản chất của việc Deduplicate trước khi Aggregate

* **Hiện tượng Collab:** Trên bảng xếp hạng tuần của Spotify, một vị trí xếp hạng (slot) có thể chứa từ 2 đến 10 nghệ sĩ. Trong bảng `charts_clean`, dữ liệu được nhân bản dòng cho từng nghệ sĩ (hệ số trung bình 1.61).
* **Quy tắc tính toán:**
  * **Khi tính xu hướng âm thanh (Dashboard 1, 2, 3) hoặc chỉ số bài hát (ML):** Bắt buộc phải `drop_duplicates(subset=["chart_country", "week", "rank"])` trước khi `groupby`. Nếu không, các bài hát collab sẽ bị phóng đại trọng số (2x-3x) so với bài hát đơn ca, làm sai lệch phân bố âm thanh.
  * **Khi tính thành tích nghệ sĩ (`mart_artist_chart`):** Dùng toàn bộ bảng `charts_clean` để ghi nhận công bằng lượt nghe và thứ hạng cho mọi nghệ sĩ tham gia.

### 2.2. Dữ liệu đầu vào của mô hình hiện tại

Mô hình trong `03_model.ipynb` dự báo `hit_next_8_weeks`: bài đạt Global Top 50 ít nhất một lần trong tám tuần sau tuần đầu quan sát, không tính tuần đầu. Chỉ gán nhãn khi đủ tám tuần Top 50; các trường hợp thiếu cửa sổ không được coi là nhãn âm.

X gồm 10 audio liên tục (thời lượng dùng `duration_min`) cùng `rank_first_week` và `log_streams_first_week`. Các tổng thành tích cả lịch sử không thuộc X. Chia dữ liệu theo thời gian, purge cửa sổ nhãn tại biên và fit bộ xử lý trên Train. ID bài tách biệt giữa các tập, nhưng chưa đảm bảo nghệ sĩ hoặc các bản thu khác ID tách biệt.

Xem [từ điển dữ liệu](data_dictionary.md#4-cohort-và-nhãn-dự-báo-trong-03_modelipynb) để biết schema, nhãn và giới hạn. Các điểm `pop_score`/`is_hit` của nhánh cũ không thuộc pipeline hiện tại.

---

## 3. HƯỚNG DẪN KỸ THUẬT VÀ CHÚ THÍCH CHO TỪNG DASHBOARD & MÔ HÌNH HÓA

> [!TIP]
> Mỗi Dashboard và bài toán mô hình đều có một Data Mart tương ứng được thiết kế tối ưu sẵn. Bạn không cần nạp file `charts_clean.parquet` nặng 65MB vào ứng dụng giao diện.

### 3.1. Dashboard 1: Xu Hướng Đặc Trưng Âm Thanh BXH & Phân Tích Nghệ Sĩ

* **Tập tin sử dụng:** `mart_audio_trend_weekly.parquet` và `mart_artist_chart.parquet`.
* **Mục tiêu trực quan:**
  * Theo dõi biến thiên của các chỉ số âm thanh theo thời gian (2017–2022).
  * Khảo sát mức độ chuyển dịch thể loại âm nhạc thịnh hành qua các năm.
  * Xếp hạng nghệ sĩ thành công nhất theo tổng lượt streams trên bảng xếp hạng và số lượng ca khúc lọt top (**100% đầy đủ tên nghệ sĩ và thể loại**).
* **Chú thích toán học (Unweighted Mean vs. Streams-Weighted Mean):**
  * *Unweighted Mean ($\text{feature\_mean}$):* Trung bình cộng đều của 200 vị trí, phản ánh xu hướng sản xuất của toàn bộ thị trường âm nhạc.
  * *Streams-Weighted Mean ($\text{feature\_weighted}$):* Trung bình có trọng số lượt nghe:
    $$\text{Weighted Feature} = \frac{\sum_{i=1}^{200} (\text{feature}_i \times \text{streams}_i)}{\sum_{i=1}^{200} \text{streams}_i}$$
    Phản ánh chính xác gu nghe nhạc thực tế của người dùng.

---

### 3.2. Dashboard 2: Tương Quan Âm Thanh Theo Quốc Gia & Mức Độ Hạnh Phúc

* **Tập tin sử dụng:** `mart_country_year.parquet`.
* **Cấp độ hạt (Grain):** `(chart_country, year)` — đúng **141 dòng** (khớp 100% các chu kỳ năm có dữ liệu quốc gia của Spotify Charts).
* **Mục tiêu trực quan:**
  * Scatter plot tương quan giữa điểm số hạnh phúc (`happiness_score`) và các chỉ số tâm trạng âm nhạc (`valence`, `danceability`, `energy`).
  * Phân cụm so sánh văn hóa nghe nhạc theo khu vực địa lý (`wb_region`) hoặc nhóm thu nhập World Bank (`wb_income_group`).
* **Chú thích nghiệp vụ quan trọng:**
  * Bảng xếp hạng các quốc gia của Spotify chỉ bắt đầu xuất hiện từ năm 2021 đến 2022.
  * **Luôn dùng `happiness_score`** (thang Cantril 0–10) làm trục chính để so sánh giữa 2021 và 2022.

---

### 3.3. Dashboard 3: Xu Hướng Biến Động Âm Nhạc Trong Thời Kỳ Đại Dịch COVID-19

* **Tập tin sử dụng:** Ghép nối `mart_audio_trend_weekly.parquet` với `covid_weekly_clean.csv` trên cặp khóa `(chart_country = country, week)`.
* **Mục tiêu trực quan:**
  * Quan sát sự thay đổi của chỉ số tâm trạng tích cực `valence` và năng lượng `energy` khi số ca tử vong tuần `weekly_deaths` đạt đỉnh.
  * Kiểm chứng giả thuyết *Âm nhạc giải tỏa (Escapism Hypothesis)*: Người nghe có xu hướng tìm đến âm nhạc hoài niệm hoặc tiết tấu nhẹ nhàng (`acousticness` tăng) trong giai đoạn phong tỏa xã hội nghiêm ngặt.
* **Kỹ thuật Phân Tích Độ Trễ (Lagged Cross-Correlation):**
  * Tính toán hệ số tương quan Pearson giữa `weekly_deaths` ở tuần $t$ với `valence` ở các tuần $t, t+1, t+2$.

---

### 3.4. Phân Hệ Machine Learning Độc Lập (03_model.ipynb): Dự Báo Global Top 50 Trong 8 Tuần

* **Tập tin sử dụng:** Đọc trực tiếp từ `charts_clean.parquet` để trích xuất trạng thái quan sát đầu tiên của bài hát trên bảng xếp hạng Global Top 200.
* **Câu hỏi nghiên cứu:** Khi một bài hát lần đầu xuất hiện trên Global Top 200, dựa vào đặc trưng âm thanh và tín hiệu tuần đầu (thứ hạng và lượt nghe), liệu bài hát có khả năng lọt vào **Global Top 50 ít nhất một lần trong 8 tuần tiếp theo** hay không?
* **Kiến trúc bài toán:**
  1. **Tập dữ liệu phân tích:** Một dòng cho mỗi bài hát tại tuần đầu quan sát (`rank_first_week`, `log_streams_first_week`).
  2. **Biến mục tiêu ($Y$):** `hit_next_8_weeks` (nhị phân: 1 nếu đạt rank $\le 50$ trong vòng 8 tuần kế tiếp, 0 nếu không).
  3. **Tập đặc trưng dự báo ($X$ - 12 biến):**
     * 10 đặc trưng âm học: `danceability`, `energy`, `loudness`, `speechiness`, `acousticness`, `instrumentalness`, `liveness`, `valence`, `tempo`, `duration_min`.
     * 2 tín hiệu thị trường tuần đầu: `rank_first_week`, `log_streams_first_week`.
  4. **Mô hình triển khai:** Logistic Regression với chuẩn hóa `StandardScaler`.
  5. **Đánh giá hiệu năng:** ROC-AUC, PR-AUC, F1-Score, Brier Score, Odds Ratio phân tích tầm quan trọng của từng đặc trưng. Báo cáo chỉ số hiện có tại `reports/global_top50_first_week/model_metrics.json`; không coi artifact trong `models/` là cùng phiên bản nếu chưa đối chiếu.
* *Lưu ý:* Tập dữ liệu `ml_tracks.parquet` cũ (dựa trên điểm tổng hợp `pop_score` toàn lịch sử) đã được chuyển vào `archive/superseded_ml_tracks/` để đảm bảo không rò rỉ dữ liệu tương lai và giữ `data/processed/` tinh gọn tuyệt đối.

---

## 4. BẢNG TỔNG HỢP CÁC RÀNG BUỘC VÀ QUY TẮC KIỂM TOÁN DỮ LIỆU (AUDIT CONSTRAINTS)

| Mục kiểm toán | Điều kiện Assert / Ràng buộc | Trạng thái đạt được | Ý nghĩa nghiệp vụ |
| :--- | :--- | :--- | :--- |
| **Khóa hạt bảng xếp hạng** | `dup_grain_count == 0` | 0 dòng trùng lặp | Đảm bảo tính duy nhất của bộ khóa `(track_id, artist_id, chart_country, week)`. |
| **Tính bất biến âm học** | `audio_invariance == 1` | 100% đạt chuẩn | Đảm bảo 12 đặc trưng âm học không bị thay đổi theo thời gian hay quốc gia. |
| **Chu kỳ xếp hạng** | `dayofweek == 3` (Thứ Năm) | 100% đúng thứ Năm | Đồng bộ nhịp thời gian chốt tuần giữa Spotify và dữ liệu COVID-19. |
| **Ghép nối Báo cáo Hạnh phúc** | `missing_whs == 0` | 141/141 cặp (100%) | Đảm bảo mọi chu kỳ năm quốc gia của Spotify đều có điểm số hạnh phúc tương ứng trong bộ nhớ. |
| **Ghép nối Dịch tễ COVID-19** | `(left_only['country'] == 'Global').all()` | Đúng 160 tuần Global | Xác nhận toàn bộ giai đoạn khuyết dữ liệu dịch tễ nằm trước khi đại dịch bùng phát. |
| **Xử lý ngoại lệ Đài Loan** | `sc == 'Taiwan' -> code = 'TWN'` | Xử lý tường minh | World Bank không báo cáo riêng lẻ Đài Loan; bổ sung thủ công chuẩn hóa mã ISO. |
| **Dị biệt nghệ sĩ Bodø Domkor** | `mismatch == 2` | Đúng 2 slot xác định | Ca khúc *"Ja, Vi Elsker Dette Landet"* có nghệ sĩ thứ nhất là `"N/A"`, giải thích hoàn toàn dị biệt số dòng. |
| **Tỷ lệ đầy đủ của Data Marts** | `null_count == 0` | 100% hoàn chỉnh | Cả 3 Data Marts không còn khuyết thiếu tên nghệ sĩ, thuộc tính hoặc giá trị tổng hợp. |

