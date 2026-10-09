# 🎵 SPOTIFY AUDIO TRENDS & ANALYTICS
## Nghiên cứu - trực quan hóa các đặc trưng âm thanh và dự đoán xu hướng bài hát thịnh hành trên Spotify.

> **Đồ án môn học:** Tương tác Dữ liệu (Interactive Data Visualization / Visual Analytics)  
> **Nền tảng phát triển:** Python 3.10+, Streamlit, Plotly Interactive, Scikit-learn, Pandas, Seaborn.  
> **Kiến trúc dữ liệu:** Hệ thống Data Marts Chuyên biệt — `charts_clean`, `ml_tracks`, `mart_audio_trend_weekly`, `mart_country_year`, `mart_artist_chart` (Parquet + CSV).

---

## 📌 1. Giới thiệu đề tài và mục tiêu nghiên cứu

Trong kỷ nguyên số hóa âm nhạc trực tuyến, sự thành công của một bản thu không chỉ phụ thuộc vào độ nhận diện của nghệ sĩ mà còn gắn liền mật thiết với **các đặc trưng âm thanh (Audio Features)** nội tại (như *danceability*, *energy*, *valence*, *tempo*, *acousticness*), **chiến lược phát hành** (đơn ca vs. hợp tác biểu diễn), cũng như **bản sắc văn hóa - xã hội** và **các biến cố thời gian** (tính mùa vụ, đại dịch toàn cầu).

Đề tài giải quyết trọn vẹn 4 mục tiêu học thuật và ứng dụng thực tiễn:
1. **Kiến trúc Master Pipeline & Data Marts:** Tích hợp 5 tập dữ liệu đa nguồn (>1.9 triệu dòng thô), làm sạch và xuất ra hệ thống Data Marts tối ưu hóa định dạng Parquet/CSV, phục vụ song song cho phân tích trực quan hóa quy mô lớn và mô hình học máy cấp bài hát không rò rỉ dữ liệu.
2. **Khám phá insight và kể chuyện bằng dữ liệu (Data Storytelling) qua 3 Trụ cột cốt truyện:**
   * **Trụ cột 1 — Công thức tạo Hit & Xu hướng Thời đại (Hit Formula & Dynamics):**
     * *Phân tầng thứ hạng:* Ma trận z-score bóc tách sự khác biệt âm học giữa nhóm dẫn đầu (Top 1–10) và nhóm bám đuổi (Top 101–200).
     * *Sức mạnh Hợp tác (Collab vs. Solo):* Đơn ca chiếm tới ~59% số lượng phát hành, nhưng các dự án Hợp tác (Collab) có **trung vị lượt stream/bài cao hơn** Đơn ca (~28.5M so với ~23.5M), gợi ý hợp tác là đòn bẩy chiến lược đáng xem xét (phân tích theo bộ lọc 2020–2022, Global chart).
     * *Hiện tượng "TikTok-hóa" âm nhạc (2017 – 2022):* Thời lượng bài hát sụt giảm mạnh từ **218 giây xuống còn 198 giây** (mất 20 giây chỉ sau 3 năm) dưới tác động của cơ chế chi trả bản quyền streaming 30 giây và văn hóa video ngắn.
   * **Trụ cột 2 — Bản sắc Địa lý & Văn hóa Âm nhạc (Cultural & Geographic Audio DNA):**
     * *Bản đồ thế giới Choropleth:* Bóc tách sự phân hóa cảm xúc (*Valence* cực đại tại Mỹ Latinh) và mức độ bắt nhịp (*Danceability*).
     * *Dấu vân tay ADN âm nhạc (Việt Nam vs. Nhật Bản):* Radar Chart đối đầu chứng minh sự đối lập 180 độ ngay trong Châu Á: Việt Nam chuộng Pop Ballad mộc mạc và trầm buồn (*Acousticness* 0.47, *Energy* 0.53, *Valence* 0.46); trong khi Nhật Bản dẫn đầu thế giới về J-Pop/J-Rock và Anime OST dồn dập (*Energy* 0.73, *Acousticness* 0.17).
   * **Trụ cột 3 — Tính Chu kỳ Thời gian & Đại dịch COVID-19 (Seasonality & Crisis Dynamics):**
     * *Tính mùa vụ 12 tháng:* Danceability ổn định quanh mức 0.70 từ tháng 1 đến 11, nhưng giảm sâu vào tháng 12 nhường chỗ cho Acousticness tăng vọt (nhạc Giáng sinh/nghỉ lễ).
     * *Tác động của đại dịch COVID-19 (2020 – 2022):* Khám phá quy luật tâm lý **"Êm hơn nhưng không buồn hơn"** — khi số ca tử vong lập đỉnh, Acousticness tăng mạnh, Energy giảm sâu, nhưng Valence kiên định đi ngang trên mốc 0.50 để xoa dịu tâm lý cộng đồng.
3. **Mô hình Học máy Dự báo Xu hướng (Machine Learning):** Áp dụng thuật toán **Hồi quy Logistic (Logistic Regression)** trên tập dữ liệu cấp độ bài hát (Song-level) độc nhất, **triệt tiêu 100% rủi ro rò rỉ dữ liệu (Data Leakage)** để dự báo xác suất một bài hát trở thành Top Hit (`is_trending`).
4. **Hệ thống Dashboard Tương tác Đa chiều (Interactive Visual Analytics):** Xây dựng bảng điều khiển Streamlit gồm các trang chuyên sâu với các biểu đồ tương tác thời gian thực (Plotly Choropleth, Radar Chart đối đầu quốc gia, Dual-axis Bar/Line, Treemap phân cấp).

---

## 🗂️ 2. Cấu trúc Thư mục Dự án

```text
PROJECT/
├── .gitignore                          # Cấu hình bỏ qua file lớn >100MB, theo dõi file ML
├── requirements.txt                    # Danh sách thư viện Python cần cài đặt
├── README.md                           # Giới thiệu đồ án, hướng dẫn cài đặt và tổng kết
│
├── data/                               # Quản trị dữ liệu đa nguồn
│   ├── raw/                            # Dữ liệu bổ trợ (⚠️ spotify-weekly-charts.csv tải từ Google Drive)
│   │   ├── country_codes.csv           # 217 dòng × 3 cột (Mã ISO-3, vùng địa lý, nhóm thu nhập)
│   │   ├── gdp_data.csv                # 13,365 dòng × 4 cột (Chuỗi thời gian GDP World Bank)
│   │   ├── global_deaths.csv           # 1,143 dòng × 290 cột (Tử vong COVID-19 theo ngày — JHU CSSE)
│   │   └── whs_years_updated.csv       # 1,510 dòng × 46 cột (World Happiness Report 2015–2024)
│   │
│   └── processed/                      # Hệ sinh thái dữ liệu sạch và Data Marts chuẩn mực
│       ├── charts_clean.parquet        # Bảng sự kiện Top 200 làm sạch (1.787M dòng × 34 cột)
│       ├── charts_clean.csv            # Bản CSV của charts_clean (dùng khi debug)
│       ├── tracks_dimension.csv        # 39,190 bài hát (12 đặc trưng âm thanh & metadata)
│       ├── ml_tracks.parquet           # 39,190 bài hát × 30 cột — tập ML chống rò rỉ dữ liệu
│       ├── ml_tracks.csv               # Bản CSV của ml_tracks
│       ├── ml_market_week_forecast.parquet  # Dự báo hit theo tuần đầu xuất hiện — 56MB
│       ├── mart_audio_trend_weekly.parquet  # Chuỗi thời gian 290 tuần xu hướng âm học
│       ├── mart_audio_trend_weekly.csv      # Bản CSV của mart_audio_trend_weekly
│       ├── mart_artist_chart.parquet   # Thống kê thành tích & lượt stream theo nghệ sĩ
│       ├── mart_artist_chart.csv       # Bản CSV tương thích của mart_artist_chart
│       ├── mart_artist_popularity.parquet   # Chỉ số phổ biến nghệ sĩ
│       ├── mart_country_year.parquet   # Dữ liệu âm học & báo cáo hạnh phúc WHS (73 quốc gia)
│       ├── mart_country_year.csv       # Bản CSV của mart_country_year
│       ├── covid_weekly_clean.csv      # Chuỗi thời gian số ca tử vong COVID-19 theo tuần
│       ├── whs_clean.csv               # World Happiness Report đã làm sạch
│       └── country_lookup.csv          # Bảng cầu nối mã quốc gia ISO-3 và phân vùng World Bank
│
├── notebooks/                          # Jupyter Notebooks nghiên cứu theo Barem đồ án
│   ├── 01_preprocess.ipynb             # Minh họa tiền xử lý, Master Pipeline, 9 biến & EDA tĩnh
│   ├── 02_eda.ipynb                    # Phân tích khám phá dữ liệu (EDA) đa biến chuyên sâu
│   ├── 03_model.ipynb                  # Huấn luyện mô hình Logistic Regression & trực quan hóa ML
│   └── 04_story.ipynb                  # Khai thác Insight chuyên sâu qua 9 biểu đồ tương tác (Lý Gia Hân)
│
├── src/                                # Module mã nguồn dùng chung
│   ├── __init__.py
│   └── data_loader.py                  # Pipeline ETL Master Dataset & các hàm nạp dữ liệu tiện ích
│
├── dashboard/                          # Ứng dụng Story tương tác — chạy bằng start_story.ps1
│   ├── story_app.py                    # Entry point: streamlit run dashboard/story_app.py (cổng 8502)
│   ├── story_canvas.py                 # Dựng workbook/payload cho từng story point
│   ├── story_charts.py                 # Các thành phần biểu đồ Plotly tương tác
│   ├── story_data.py                   # Đọc & khử đếm lặp dữ liệu từ data/processed/
│   ├── story_analysis.py               # Tính toán insight tự động theo bộ lọc
│   ├── eda_data.py                     # Đọc hình PNG tĩnh từ 02_eda.ipynb cho Story Point 1
│   ├── story_canvas.html               # Bố cục HTML canvas no-scroll (1440×900)
│   ├── story_interactions.js           # Logic tổng hợp, vẽ & cross-filter (Plotly events)
│   ├── index.html                      # Build tĩnh của story canvas (dùng khi xuất HTML offline)
│   └── pages/                          # Sub-pages phân tích chuyên sâu (EDA Dashboard)
│       ├── 1_📊_Tong_Quan_Du_Lieu.py  # Tổng quan dữ liệu: KPI, phân phối, bản đồ
│       └── 2_🎵_Dac_Trung_Am_Thanh.py # Đặc trưng âm thanh & Hit Simulator (ML)
│
├── docs/                               # Tài liệu học thuật & Báo cáo kỹ thuật
│   ├── data_dictionary.md              # Từ điển dữ liệu toàn diện (bảng thô, Data Marts & ML Dataset)
│   ├── data_processing_flow.md         # Tài liệu kiến trúc luồng dữ liệu hợp nhất
│   ├── BAO_CAO_CUOI_KI_CO_SO_PIPELINE_EDA.md  # Báo cáo chuyên sâu: Pipeline, EDA, Data Marts
│   ├── BAO_CAO_DU_LIEU_PROCESSED.md    # Báo cáo mô tả dữ liệu đã xử lý
│   ├── BAO_CAO_KHAO_SAT_DU_LIEU.md     # Báo cáo khảo sát dữ liệu thô
│   ├── BAO_CAO_DANH_GIA_REPOSITORY.md  # Báo cáo đánh giá repository
│   ├── KICH_BAN_THUYET_TRINH_DASHBOARD.md  # Kịch bản thuyết trình chi tiết từng phút
│   ├── team_tasks_assignment.md        # Bảng phân công trách nhiệm nhóm theo barem 10 điểm
│   ├── story_studio.md                 # Hướng dẫn dashboard, phạm vi & kiểm tra số liệu
│   └── spotify_data_story.html         # Bản story tương tác độc lập (13MB, chạy offline)
│
├── models/                             # Metrics & kết quả mô hình Machine Learning
│   └── model_metrics.json              # Chỉ số đánh giá mô hình Logistic Regression
│
└── reports/                            # Báo cáo kết quả & mô hình đã huấn luyện
    ├── Bao_cao_Spotify_Chuong_1_3_4.docx   # Báo cáo Word đồ án (Chương 1, 3, 4)
    └── global_top50_first_week/        # Mô hình dự báo Global Top 50 tuần đầu
        ├── selected_logistic.joblib    # Mô hình Logistic Regression đã huấn luyện
        ├── model_metrics.json          # AUC=0.811, Accuracy=83.7% trên tập test
        ├── first_week_forecast.parquet # Bảng dự báo xác suất cho từng bài
        ├── tableau_coefficients.csv    # Hệ số hồi quy (dùng trực quan hóa)
        └── tableau_threshold_validation.csv  # Bảng ngưỡng quyết định
```

---

## ⚡ 3. Các Tệp Dữ liệu Đầu ra (Output Datasets)

> [!IMPORTANT]
> 📂 **Kho Dữ Liệu Đồ Án Đầy Đủ (Google Drive):**  
> Do giới hạn dung lượng 100MB của GitHub, các tệp lớn (`spotify-weekly-charts.csv` ~796 MB, `charts_clean.parquet` ~65 MB, `ml_market_week_forecast.parquet` ~54 MB) **không được lưu trong repo**. Tải toàn bộ dữ liệu thô và dữ liệu đã xử lý tại:  
> 👉 **[TươngTacData - Google Drive](https://drive.google.com/drive/u/0/folders/1TN3uZLE9xYq-DDukDzQRbkzJK8wCtMYi)**  
> ⚠️ **Đặt các file vào đúng thư mục `data/raw/` và `data/processed/` trước khi chạy pipeline.**

| Tên tập dữ liệu | Định dạng | Quy mô (Dòng × Cột) | Đối tượng phục vụ | Mục đích sử dụng |
| :--- | :---: | :---: | :--- | :--- |
| **`charts_clean.parquet`** | Parquet | 1,787,531 × 34 | Toàn nhóm | Fact table trung tâm; phục vụ trích xuất Data Marts, EDA, Story và huấn luyện ML tại `03_model.ipynb`. |
| **`tracks_dimension.csv`** | CSV | 39,190 × 21 | Toàn nhóm | Bảng chiều độc nhất 39,190 bài hát với 12 đặc trưng âm học nội tại và thông tin phát hành. |
| **`ml_tracks.parquet`** | Parquet | 39,190 × 30 | Thành Tài | Tập dữ liệu ML cấp bài hát (song-level), bổ sung `pop_score`, `is_hit`, `is_mega_hit` và các trường thống kê tổng hợp không rò rỉ. |
| **`mart_audio_trend_weekly.parquet`** | Parquet | 5,548 × 29 | Lý Gia Hân | Chuỗi thời gian 290 tuần phân tích xu hướng âm học, tính mùa vụ và tác động đại dịch. |
| **`mart_artist_chart.parquet` & `.csv`** | Parquet / CSV | 15,254 × 7 | Lý Gia Hân | Tổng hợp thành tích nghệ sĩ (lượt stream, số bài, thứ hạng đỉnh cao, thể loại). |
| **`mart_country_year.parquet`** | Parquet | 141 × 42 | Lý Gia Hân | Tích hợp đặc trưng âm học quốc gia theo năm với toàn bộ chỉ số báo cáo hạnh phúc WHS. |
| **`covid_weekly_clean.csv`** | CSV | 12,136 × 5 | Lý Gia Hân | Chuỗi thời gian tử vong COVID-19 theo tuần cho 73 quốc gia và Global. |
| **`country_lookup.csv`** | CSV | 73 × 8 | Toàn nhóm | Bảng cầu nối mã quốc gia ISO-3, phân vùng World Bank và ngôn ngữ bảng xếp hạng. |

---

## 🚀 4. Hướng dẫn Cài đặt & Khởi chạy Dự án

### Bước 1: Clone kho lưu trữ về máy tính
```bash
git clone https://github.com/lyhiahan/Spotify_Audio_Trends_Analytics.git
cd Spotify_Audio_Trends_Analytics
```

### Bước 2: Khởi tạo môi trường ảo & Cài đặt thư viện
```bash
# Tạo môi trường ảo Python:
python -m venv venv

# Kích hoạt môi trường:
# Trên Windows:
venv\Scripts\activate
# Trên macOS / Linux:
source venv/bin/activate

# Cài đặt các gói phụ thuộc:
pip install -r requirements.txt
```

### Bước 3: Tải dữ liệu từ Google Drive
> [!WARNING]
> Trước khi chạy pipeline, hãy tải dữ liệu từ **[Google Drive](https://drive.google.com/drive/u/0/folders/1TN3uZLE9xYq-DDukDzQRbkzJK8wCtMYi)** và đặt vào đúng thư mục:
> - `data/raw/` — chứa: `spotify-weekly-charts.csv`, `country_codes.csv`, `gdp_data.csv`, `global_deaths.csv`, `whs_years_updated.csv`
> - `data/processed/` — chứa các file `.parquet` và `.csv` đã xử lý sẵn (nếu muốn bỏ qua bước tiền xử lý)

### Bước 4: Thực thi Pipeline Tiền xử lý & Xuất dữ liệu
```bash
# Chạy toàn bộ Master Pipeline (tự động nạp thô, làm sạch và xuất hệ thống Data Marts):
python src/data_loader.py
```

### Bước 5: Khởi chạy Ứng dụng Dashboard Story

Người dùng có thể khởi chạy Dashboard theo 2 phương thức:

#### 🌟 Cách 1: Khởi chạy qua Streamlit Web App (Chính thức)
```bash
python -m streamlit run dashboard/story_app.py --server.port 8502
```
Hoặc trên Windows PowerShell:
```powershell
./start_story.ps1
```
👉 Truy cập trực tiếp tại: **`http://localhost:8502`**

#### 🌐 Cách 2: Khởi chạy Độc lập Offline (Không cần cài đặt Python)
Mở trực tiếp tệp [`docs/spotify_data_story.html`](docs/spotify_data_story.html) bằng bất kỳ trình duyệt web hiện đại nào (Google Chrome, Microsoft Edge, Brave). Toàn bộ dữ liệu, biểu đồ Plotly và mã logic tương tác đã được đóng gói độc lập (~15MB), sẵn sàng phục vụ thuyết trình và demo offline ngay lập tức.

---

### 🎮 Hướng dẫn Sử dụng & Trải nghiệm Tương tác (User & Interaction Guide)

Giao diện áp dụng triết lý thiết kế **Fixed-Viewport (Tableau Story Style)** — toàn bộ bảng điều khiển được khóa cố định trong khung nhìn 100vh, **hoàn toàn không cần cuộn chuột** nhằm giảm tải nhận thức và tối ưu hóa trải nghiệm thuyết trình.

#### 1. Mạch dẫn dắt 6 Story Points (Thanh điều hướng trên cùng)
* **Story Point 1 — Cái nhìn về dữ liệu:** Gom trọn **5 biểu đồ phân tích thực chứng** từ `02_eda.ipynb` trên 1 trang 2 hàng (12 cột):
  * *Hàng 1:* Phân phối 5 đặc trưng âm thanh chính & Nửa ma trận tương quan Spearman 10 biến.
  * *Hàng 2:* Xu hướng âm thanh Global Top 200 (2017–2022), Đối chiếu số ca tử vong COVID-19 với âm thanh, và Phân phối nhãn mục tiêu Top 50 trên tập Train.
  * *Tương tác:* Hỗ trợ nút **"Xem lớn"** (mở popup phóng to toàn màn hình xem chi tiết độ nét cao) và nút **"PNG"** (tải ảnh gốc).
* **Story Point 2 — Hồ sơ âm thanh (Hit Formula):** Ma trận nhiệt Z-score đối chiếu 9 đặc trưng âm học giữa các tầng thứ hạng (Top 1–10 vs. Top 101–200) kết hợp biểu đồ hộp (Boxplot) bóc tách cấu trúc âm thanh giữa các thể loại âm nhạc.
* **Story Point 3 — Nghệ sĩ & hợp tác:** Khám phá độ phân tán tương quan giữa điểm nghệ sĩ và lượt nghe 8 tuần, Treemap phân cấp lượt stream của 80 nghệ sĩ dẫn đầu, và kiểm chứng sức mạnh Đơn ca (Solo) vs. Hợp tác (Collab).
* **Story Point 4 — Bản sắc địa lý & ADN âm nhạc:** Bản đồ thế giới Choropleth trực quan hóa các đặc trưng âm học trên 73 quốc gia, đi kèm biểu đồ Radar Chart đối đầu văn hóa 180 độ giữa Việt Nam (Pop Ballad mộc mạc) và Nhật Bản (J-Pop/J-Rock dồn dập).
* **Story Point 5 — Chu kỳ thời gian & đại dịch:** Biểu đồ đối chiếu hiện tượng "TikTok-hóa" sụt giảm thời lượng bài hát, tính mùa vụ âm nhạc tháng 12 (nhạc Giáng sinh), và tác động tâm lý trong đại dịch COVID-19 ("êm hơn nhưng không buồn hơn").
* **Story Point 6 — Mô hình & Ngưỡng dự báo (Machine Learning):** Trực quan hóa không gian quyết định 2D, mô phỏng đánh đổi ngưỡng quyết định $\tau$ thời gian thực trên Ma trận nhầm lẫn (Confusion Matrix) và đường cong Precision – Recall.

#### 2. Các tính năng tương tác đa chiều (Interactive Capabilities)
* **Lọc chéo tức thời (Cross-filtering):** Click trực tiếp vào một thể loại trên Treemap hoặc một nhóm trên biểu đồ Donut để các biểu đồ liên quan tự động lọc và đồng bộ theo đối tượng vừa chọn.
* **Bộ điều khiển chi tiết (Inspector Panel bên phải):** Cho phép người dùng tùy biến khoảng thời gian (2017–2022), thể loại nhạc, nghệ sĩ cụ thể, phân tầng thứ hạng, và phương pháp tính luồng nghe (Weighted vs. Mean).
* **Mô phỏng ngưỡng dự báo động ($\tau$-tuning):** Tại Story Point 6, người dùng có thể kéo thanh trượt ngưỡng $\tau \in [0.0, 1.0]$ hoặc nhấn các nút chọn sẵn (Preset F1 tối ưu `0.79`, Cân bằng `0.50`, Ưu tiên độ chính xác `0.85`) để quan sát sự biến thiên tức thời của Ma trận nhầm lẫn và các chỉ số $F_1$, Precision, Recall.
* **Xuất bản dữ liệu & Hình ảnh:** Mọi biểu đồ trên hệ thống đều tích hợp nút **PNG** (xuất ảnh đồ họa chất lượng cao) và **CSV** (tải bảng dữ liệu đã qua xử lý và lọc).

---

## 👥 5. Phân công Trách nhiệm Nhóm (Theo Barem 10 Điểm)

Chi tiết kế hoạch thực hiện và ma trận đóng góp được lưu tại: [`docs/team_tasks_assignment.md`](docs/team_tasks_assignment.md).

| STT | Họ và tên | MSSV | Vai trò chính | Nhiệm vụ đảm nhiệm theo Barem Đồ án |
| :---: | :--- | :---: | :--- | :--- |
| 1 | **Đinh Quốc Anh** | **24133003** | Data Engineer & Data Analyst | • Xây dựng Kiến trúc Master Pipeline (`src/data_loader.py`).<br>• Làm sạch và kết nối 5 bảng dữ liệu (>1.9M bản ghi).<br>• Xây dựng 9 Calculated Fields và viết `notebooks/01_preprocess.ipynb`.<br>• Thực hiện phân tích EDA tĩnh 8–10 biểu đồ chuyên sâu trong `notebooks/02_eda.ipynb`. |
| 2 | **Lý Gia Hân** | **24133016** | Visualization & Dashboard Dev | • Xây dựng và hoàn thiện hệ thống **9 biểu đồ tương tác chuyên sâu** trong `notebooks/04_story.ipynb` bao phủ 3 trụ cột cốt truyện (Công thức Hit & TikTok-hóa, Bản sắc văn hóa địa lý Việt Nam vs. Nhật Bản, Tính mùa vụ & Khủng hoảng COVID-19).<br>• Thiết kế toàn bộ kiến trúc giao diện bảng điều khiển tương tác đa trang Streamlit (`dashboard/`). |
| 3 | **Đỗ Thanh Thành Tài** | **24133050** | ML Engineer & Demo / Report Lead | • Huấn luyện mô hình Logistic Regression dự báo Top Hit trên tập dữ liệu Song-level không rò rỉ (`notebooks/03_model.ipynb`).<br>• Xây dựng bộ công cụ tương tác dự báo xu hướng thịnh hành trên Dashboard.<br>• Soạn thảo Báo cáo tổng kết đồ án (`reports/Bao_cao_Spotify_Chuong_1_3_4.docx`) và quay Video Demo thuyết trình. |

---

## 📑 6. Tài liệu Tham khảo & Báo cáo Đi kèm
* 📂 **[Kho Dữ liệu Đồ án Đầy đủ (Google Drive)](https://drive.google.com/drive/u/0/folders/1TN3uZLE9xYq-DDukDzQRbkzJK8wCtMYi):** Tải trọn bộ dữ liệu thô và các tệp dữ liệu xử lý lớn.
* 📖 [Từ điển Dữ liệu Toàn diện (Data Dictionary)](docs/data_dictionary.md): Đặc tả chi tiết các bảng thô, Data Marts và công thức tính toán.
* 🔄 [Kiến trúc Luồng Xử lý Dữ liệu (Data Processing Flow)](docs/data_processing_flow.md): Sơ đồ Mermaid, quy trình JOIN và luồng dữ liệu.
* 📋 [Kế hoạch Phân công Công việc (Team Tasks Assignment)](docs/team_tasks_assignment.md): Barem chấm điểm chi tiết và tiến độ phân công nhiệm vụ.
* 🎬 [Kịch bản Thuyết trình Dashboard](docs/KICH_BAN_THUYET_TRINH_DASHBOARD.md): Hướng dẫn demo từng phút, Q&A dự phòng.
* 📊 [Story Studio — Hướng dẫn & Phạm vi Số liệu](docs/story_studio.md): Mô tả 5 story points, tương tác và kiểm tra tính chính xác số liệu.
* 📹 **Link Video Demo:** *(sẽ cập nhật sau khi hoàn thành quay)*
* 🖼️ **Link Slide Thuyết trình:** *(sẽ cập nhật sau khi hoàn thành)*
