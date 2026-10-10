# 🎵 SPOTIFY AUDIO TRENDS & ANALYTICS
## Nghiên cứu, Trực quan hóa Đặc trưng Âm thanh và Dự đoán Xu hướng Bài hát Thịnh hành trên Spotify

> **Đồ án môn học:** Tương tác Dữ liệu (Interactive Data Visualization / Visual Analytics)  
> **Giảng viên hướng dẫn:** Bộ môn Khoa học Dữ liệu & Trực quan hóa  
> **Nền tảng công nghệ:** Python 3.10+, Streamlit, Plotly.js, Scikit-learn, Pandas, NumPy, HTML5 Canvas.  
> **Kiến trúc dữ liệu:** Data Marts chuyên biệt — `charts_clean`, `tracks_dimension`, `mart_audio_trend_weekly`, `mart_country_year`, `mart_artist_chart` (Parquet + CSV).

---

## 📌 1. Giới thiệu đề tài & Mục tiêu nghiên cứu

Trong kỷ nguyên âm nhạc số, sự thành công của một bản thu không chỉ phụ thuộc vào danh tiếng của nghệ sĩ mà còn gắn liền mật thiết với **các đặc trưng âm thanh nội tại (Audio Features)** như *Danceability*, *Energy*, *Valence*, *Tempo*, *Acousticness*, **chiến lược phát hành** (đơn ca vs. hợp tác biểu diễn), cũng như **bản sắc văn hóa - địa lý** và **các biến cố xã hội vĩ mô** (tính chu kỳ mùa vụ, đại dịch toàn cầu).

Đề tài giải quyết trọn vẹn 4 mục tiêu cốt lõi:

1. **Kiến trúc Master Pipeline & Data Marts:** Tích hợp 5 tập dữ liệu đa nguồn (>1.9 triệu dòng thô), làm sạch và xuất ra hệ thống Data Marts định dạng Parquet/CSV tối ưu, phục vụ song song cho phân tích trực quan hóa quy mô lớn và mô hình học máy cấp bài hát (song-level) triệt tiêu hoàn toàn rủi ro rò rỉ dữ liệu (Data Leakage).
2. **Kể chuyện dữ liệu đa chiều (Data Storytelling) qua 3 Trụ cột nghiên cứu:**
   * **Trụ cột 1 — Công thức tạo Hit & Xu hướng Thời đại (Hit Formula & Dynamics):**
     * *Phân tầng thứ hạng:* Ma trận Z-score định lượng độ lệch âm học giữa Top 1–10 và Hạng 101–200; nhóm dẫn đầu vượt trội ở Tempo (+0.16 SD), Liveness (+0.14 SD), Danceability (+0.13 SD), Valence (+0.12 SD), Energy (+0.11 SD), đồng thời giảm thiểu tối đa Instrumentalness (-0.12 SD) và Acousticness (-0.11 SD).
     * *Sức mạnh Hợp tác (Collab vs. Solo):* Đơn ca chiếm ưu thế về số lượng phát hành (~59%), nhưng các dự án Hợp tác (Collab) có **trung vị lượt stream/bài cao hơn** (28,52 triệu so với 23,47 triệu), gợi ý hợp tác là đòn bẩy chiến lược đáng xem xét.
     * *Xu hướng rút ngắn thời lượng (2017 – 2022):* Thời lượng trung bình bài hát co cụm từ mức đỉnh **217,96 giây (~3 phút 38 giây)** năm 2017 xuống đáy **198,50 giây (~3 phút 18 giây)** năm 2020 (rút ngắn gần 20 giây), sau đó ổn định trong dải chuẩn **198 – 206 giây (~3 phút 20 giây)** dưới tác động của cơ chế chi trả bản quyền 30 giây và văn hóa video ngắn.
   * **Trụ cột 2 — Bản sắc Địa lý & ADN Âm nhạc (Cultural & Geographic Audio DNA):**
     * *Bản đồ thế giới Choropleth (73 quốc gia):* Bóc tách sự phân hóa cảm xúc (*Valence* cực đại tại Mỹ Latinh) và mức độ bắt nhịp (*Danceability*).
     * *Dấu vân tay ADN âm nhạc (Việt Nam vs. Nhật Bản):* Radar Chart đối đầu chứng minh sự đối lập văn hóa rõ rệt ngay trong Châu Á: Việt Nam chuộng Pop Ballad mộc mạc và trầm buồn (*Acousticness* 0.47, *Energy* 0.53, *Valence* 0.46); trong khi Nhật Bản dẫn đầu về J-Pop/J-Rock và Anime OST dồn dập (*Energy* 0.73, *Acousticness* 0.17).
   * **Trụ cột 3 — Chu kỳ Thời gian & Biến cố Xã hội (Seasonality & Crisis Dynamics):**
     * *Tính mùa vụ 12 tháng:* Danceability ổn định quanh mức 0.70 từ tháng 1 đến 11, nhưng giảm sâu vào tháng 12 nhường chỗ cho Acousticness tăng vọt do sự trỗi dậy của nhạc Giáng sinh và lễ hội cuối năm.
     * *Tác động kép của đại dịch COVID-19 (2020 – 2022):* Đánh giá khách quan sự dịch chuyển ngữ cảnh từ không gian công cộng về tư gia trong các đợt giãn cách. Kiểm định thống kê trên 130 tuần cho thấy tương quan giữa số ca tử vong và Acousticness đạt $r = 0.345$, và sau khi khử nhiễu tháng lịch vẫn đạt $r = 0.315$, chứng minh áp lực dịch bệnh tạo tác động độc lập thực chất lên hành vi tiêu thụ âm nhạc.
3. **Mô hình Học máy Dự báo Xu hướng (Machine Learning):** Huấn luyện mô hình **Hồi quy Logistic (Logistic Regression)** trên tập dữ liệu cấp bài hát không rò rỉ, dự báo xác suất một bài hát mới lọt vào Top 50 Global trong 8 tuần đầu với diện tích dưới đường cong ROC đạt $AUC = 0.811$.
4. **Hệ thống Dashboard Tương tác Toàn diện:** Xây dựng bảng điều khiển Tableau Story Canvas duy nhất (`dashboard/story_app.py`) tích hợp 6 Story Points, hỗ trợ lọc chéo thời gian thực (cross-filtering), cố định khung nhìn không cuộn chuột (100vh) và tối ưu hóa cho thuyết trình.

---

## 🗂️ 2. Cấu trúc Thư mục Dự án

```text
Spotify_Audio_Trends_Analytics/
├── .gitignore                          # Cấu hình loại trừ file rác, file tạm và dữ liệu >100MB
├── requirements.txt                    # Danh sách thư viện Python cần thiết
├── README.md                           # Giới thiệu tổng quan, hướng dẫn cài đặt và kết quả đề tài
│
├── data/                               # Quản trị dữ liệu đa nguồn
│   ├── raw/                            # Dữ liệu nguồn bổ trợ
│   │   ├── country_codes.csv           # 217 dòng (Mã ISO-3, phân vùng World Bank, nhóm thu nhập)
│   │   ├── gdp_data.csv                # Chuỗi thời gian GDP theo quốc gia (World Bank)
│   │   ├── global_deaths.csv           # Chuỗi số ca tử vong COVID-19 toàn cầu theo ngày
│   │   └── whs_years_updated.csv       # Dữ liệu World Happiness Report (2015 – 2024)
│   │
│   └── processed/                      # Hệ sinh thái dữ liệu sạch & Data Marts tối ưu Parquet
│       ├── charts_clean.parquet        # Bảng sự kiện Top 200 làm sạch (1.787M dòng × 34 cột)
│       ├── tracks_dimension.csv        # 39,190 bài hát (12 đặc trưng âm học & metadata phát hành)
│       ├── mart_audio_trend_weekly.parquet  # Chuỗi thời gian 290 tuần xu hướng âm học toàn cầu
│       ├── mart_artist_chart.parquet   # Thống kê thành tích và lượt stream theo nghệ sĩ
│       ├── mart_country_year.parquet   # Dữ liệu âm học quốc gia theo năm tích hợp báo cáo WHS
│       ├── covid_weekly_clean.csv      # Chuỗi thời gian số ca tử vong COVID-19 theo tuần
│       └── country_lookup.csv          # Bảng ánh xạ mã quốc gia ISO-3 và phân vùng địa lý
│
├── notebooks/                          # Jupyter Notebooks nghiên cứu & trực quan hóa
│   ├── 01_preprocess.ipynb             # Master Pipeline ETL, kiểm tra chất lượng & làm sạch
│   ├── 02_eda.ipynb                    # Phân tích khám phá dữ liệu (EDA) đa biến chuyên sâu
│   ├── 03_model.ipynb                  # Huấn luyện mô hình Logistic Regression & trực quan hóa ML
│   └── 04_story.ipynb                  # Khai thác Insight và xây dựng các biểu đồ câu chuyện dữ liệu
│
├── src/                                # Module xử lý mã nguồn dùng chung
│   ├── __init__.py
│   └── data_loader.py                  # Pipeline ETL Master Dataset & các hàm nạp dữ liệu tiện ích
│
├── dashboard/                          # Ứng dụng Story Dashboard duy nhất (chạy qua story_app.py)
│   ├── story_app.py                    # Entry point chính chạy Streamlit (story_app.py)
│   ├── story_canvas.py                 # Module dựng Workbook, điều phối 6 story points và payload
│   ├── story_canvas.html               # Bộ khung HTML5, layout CSS no-scroll và typography
│   ├── story_interactions.js           # Logic vẽ biểu đồ Plotly, xử lý sự kiện click & lọc chéo
│   ├── story_data.py                   # Tiền xử lý dữ liệu và cấu trúc payload từ data mart
│   ├── story_charts.py                 # Khởi tạo các thành phần biểu đồ Plotly
│   ├── story_analysis.py               # Phân tích slot thứ hạng & thuật toán điểm tên tuổi nghệ sĩ
│   └── eda_data.py                     # Trích xuất dữ liệu tổng quan ban đầu
│
├── docs/                               # Tài liệu học thuật & Báo cáo kỹ thuật
│   ├── HUONG_DAN_CAI_DAT_VA_SU_DUNG.md # Hướng dẫn chi tiết cài đặt và sử dụng Dashboard
│   ├── data_dictionary.md              # Từ điển dữ liệu toàn diện (bảng thô, Data Marts & ML Dataset)
│   ├── data_processing_flow.md         # Sơ đồ kiến trúc luồng dữ liệu hợp nhất (Mermaid)
│   ├── team_tasks_assignment.md        # Bảng phân công trách nhiệm nhóm theo barem 10 điểm
│   └── spotify_data_story.html         # Bản story tương tác độc lập (chạy offline trên trình duyệt)
│
├── models/                             # Metrics & kết quả mô hình Machine Learning
│   └── model_metrics.json              # Chỉ số đánh giá mô hình Logistic Regression
│
├── reports/                            # Báo cáo kết quả & mô hình đã huấn luyện
│   ├── Bao_cao_Spotify_Chuong_1_3_4.docx   # Báo cáo Word đồ án môn học
│   └── global_top50_first_week/        # Mô hình dự báo Global Top 50 tuần đầu
│       ├── selected_logistic.joblib    # Mô hình Logistic Regression đã huấn luyện
│       ├── model_metrics.json          # AUC=0.811, Accuracy=83.7% trên tập kiểm thử
│       ├── first_week_forecast.parquet # Bảng dự báo xác suất cho từng bài hát
│       ├── tableau_coefficients.csv    # Hệ số hồi quy dùng trực quan hóa
│       └── tableau_threshold_validation.csv  # Bảng đánh đổi ngưỡng quyết định
│
└── tests/                              # Bộ kiểm thử tự động
    ├── run_story_notebook.py           # Kiểm tra thực thi notebook story
    ├── test_story_analysis.py          # Kiểm tra logic phân tích và xếp hạng nghệ sĩ
    └── test_story_figures.cjs          # Kiểm tra tính toàn vẹn của các biểu đồ story
```

---

## ⚡ 3. Các Tệp Dữ liệu Đầu ra (Output Data Marts)

> [!IMPORTANT]
> 📂 **Kho Dữ Liệu Đồ Án Đầy Đủ (Google Drive):**  
> Do giới hạn dung lượng 100MB của GitHub, tệp thô ban đầu (`spotify-weekly-charts.csv` ~796 MB) được lưu trữ trên cloud. Bạn có thể tải toàn bộ dữ liệu tại:  
> 👉 **[TươngTacData - Google Drive](https://drive.google.com/drive/u/0/folders/1TN3uZLE9xYq-DDukDzQRbkzJK8wCtMYi)**  
> ⚠️ Hãy đặt các tệp vào thư mục `data/raw/` hoặc `data/processed/` trước khi chạy pipeline tiền xử lý.

| Tên tập dữ liệu | Định dạng | Quy mô (Dòng × Cột) | Mục đích sử dụng |
| :--- | :---: | :---: | :--- |
| **`charts_clean.parquet`** | Parquet | 1,787,531 × 34 | Bảng sự kiện (Fact table) trung tâm; phục vụ trích xuất Data Marts, EDA, Story Dashboard và huấn luyện mô hình ML. |
| **`tracks_dimension.csv`** | CSV | 39,190 × 21 | Bảng chiều độc nhất 39,190 bài hát với 12 đặc trưng âm học nội tại và metadata phát hành. |
| **`mart_audio_trend_weekly.parquet`** | Parquet | 5,548 × 29 | Chuỗi thời gian 290 tuần xu hướng âm học, tính mùa vụ và tác động đại dịch COVID-19. |
| **`mart_artist_chart.parquet`** | Parquet | 15,254 × 7 | Tổng hợp thành tích nghệ sĩ (lượt stream, số bài, thứ hạng đỉnh cao, thể loại). |
| **`mart_country_year.parquet`** | Parquet | 141 × 42 | Tích hợp đặc trưng âm học quốc gia theo năm với toàn bộ chỉ số báo cáo hạnh phúc WHS (73 quốc gia). |
| **`covid_weekly_clean.csv`** | CSV | 12,136 × 5 | Chuỗi thời gian số ca tử vong COVID-19 theo tuần cho 73 quốc gia và toàn cầu (Global). |
| **`country_lookup.csv`** | CSV | 73 × 8 | Bảng cầu nối mã quốc gia ISO-3, phân vùng World Bank và ngôn ngữ bảng xếp hạng. |

---

## 🚀 4. Hướng dẫn Cài đặt & Khởi chạy Dashboard

### Bước 1: Clone kho lưu trữ về máy tính
```bash
git clone https://github.com/lyhiahan/Spotify_Audio_Trends_Analytics.git
cd Spotify_Audio_Trends_Analytics
```

### Bước 2: Thiết lập môi trường ảo & Cài đặt thư viện
```powershell
# Tạo môi trường ảo:
python -m venv .venv

# Kích hoạt môi trường (Windows PowerShell):
.\.venv\Scripts\Activate.ps1

# (Trên macOS / Linux):
# source .venv/bin/activate

# Cài đặt toàn bộ thư viện phụ thuộc:
pip install -r requirements.txt
```

### Bước 3: Khởi chạy Ứng dụng Dashboard

Người dùng có thể khởi chạy ứng dụng theo 2 phương thức:

#### 🌟 Cách 1: Khởi chạy qua Streamlit Web App (Chính thức)
Thực thi lệnh Streamlit tiêu chuẩn:
```powershell
streamlit run dashboard/story_app.py
```
👉 Truy cập trực tiếp tại: **`http://localhost:8501`** (hoặc cổng được cấp phát trên terminal).

#### 🌐 Cách 2: Khởi chạy Độc lập Offline (Không cần môi trường Python)
Mở trực tiếp tệp [`docs/spotify_data_story.html`](docs/spotify_data_story.html) bằng bất kỳ trình duyệt web hiện đại nào (Google Chrome, Microsoft Edge, Brave). Toàn bộ dữ liệu, thư viện Plotly.js và mã logic tương tác đã được nhúng độc lập, sẵn sàng phục vụ trình chiếu offline.

---

## 🎮 5. Kiến trúc Giao diện & Hướng dẫn Sử dụng Dashboard

Bảng điều khiển áp dụng triết lý thiết kế **Fixed-Viewport (Tableau Story Style)** — toàn bộ giao diện được khóa cố định trong khung nhìn 100vh, **hoàn toàn không cần cuộn chuột**, tối ưu hóa tối đa cho việc trình chiếu và thuyết trình khoa học.

### Mạch dẫn dắt qua 6 Story Points cốt lõi:

| Story Point | Tên màn hình | Biểu đồ trực quan hóa trung tâm | Nội dung phân tích & Tương tác chính |
| :---: | :--- | :--- | :--- |
| **1** | **MAIN DASHBOARD** | 6 biểu đồ trụ cột: Bản đồ thế giới, Radar ADN, Heatmap thứ hạng, Chuỗi thời lượng, Solo vs Collab, Treemap 80 nghệ sĩ | Bảng điều khiển tinh hoa bao quát toàn bộ đề tài trên 1 màn hình. Hỗ trợ **lọc chéo đa chiều (cross-filtering)**: click quốc gia trên bản đồ cập nhật Radar, click ô heatmap khóa đặc trưng, click mốc thời gian lọc năm. |
| **2** | **HỒ SƠ ÂM THANH** | Heatmap Z-score 9 đặc trưng theo 4 tầng thứ hạng & Boxplot 5 thể loại nhạc | Phân tích dấu vân tay âm học của Top 1–10 so với Hạng 101–200. Menu dropdown trên Boxplot cho phép chuyển đổi tức thì giữa Energy, Danceability, Valence, Tempo của 5 dòng nhạc (Pop, Latin, K-Pop, Rap, Dance Pop). |
| **3** | **NGHỆ SĨ & HỢP TÁC** | Scatter plot tên tuổi vs Lượt stream 8 tuần, Treemap 80 nghệ sĩ, Donut & Bar Solo/Collab | Đánh giá đòn bẩy hợp tác: Collab có trung vị stream cao hơn Solo (28.52M vs 23.47M). Treemap phân bổ thị phần stream có thể click chọn từng nghệ sĩ. |
| **4** | **BẢN SẮC ĐỊA LÝ** | Bản đồ thế giới Choropleth (73 quốc gia) & Radar Chart đối đầu ADN âm nhạc | Nhận diện sự phân cực địa lý (Valence cực đại tại Mỹ Latinh). Trực quan hóa đối kháng 180 độ giữa thị hiếu Pop Ballad mộc mạc của Việt Nam và J-Pop/Rock dồn dập của Nhật Bản. |
| **5** | **DÒNG CHẢY THỜI GIAN** | Chuỗi thời lượng 2017–2022, Biểu đồ mùa vụ 12 tháng, Tương quan COVID-19 theo tuần | Chứng minh xu hướng rút ngắn thời lượng bài hát từ ~218s xuống dải 198–206s. Phân tích hiện tượng tăng vọt Acousticness vào tháng 12 (nhạc Giáng sinh) và kiểm định khử mùa vụ đại dịch ($r = 0.315$). |
| **6** | **MÔ HÌNH HÓA** | Không gian quyết định 2D, Confusion Matrix, Đánh đổi Precision – Recall, Bảng Odds Ratio | Trực quan hóa kết quả mô hình Logistic Regression dự báo Top 50. Cho phép kéo thanh trượt ngưỡng phân loại $\tau \in [0.0, 1.0]$ để mô phỏng đánh đổi thời gian thực giữa Precision và Recall. |

---

## 👥 6. Phân công Trách nhiệm Nhóm (Theo Barem 10 Điểm)

Chi tiết bảng kế hoạch thực hiện và ma trận đóng góp được lưu tại: [`docs/team_tasks_assignment.md`](docs/team_tasks_assignment.md).

| STT | Họ và tên | MSSV | Vai trò chính | Nhiệm vụ đảm nhiệm theo Barem Đồ án |
| :---: | :--- | :---: | :--- | :--- |
| 1 | **Đinh Quốc Anh** | **24133003** | Data Engineer & Data Analyst | • Xây dựng Kiến trúc Master Pipeline (`src/data_loader.py`).<br>• Làm sạch và tích hợp 5 bảng dữ liệu (>1.9 triệu bản ghi).<br>• Xây dựng 9 Calculated Fields và soạn thảo `notebooks/01_preprocess.ipynb`.<br>• Thực hiện phân tích EDA tĩnh chuyên sâu đa biến trong `notebooks/02_eda.ipynb`. |
| 2 | **Lý Gia Hân** | **24133016** | Visualization & Dashboard Lead | • Xây dựng và hoàn thiện hệ thống **biểu đồ phân tích chuyên sâu** trong `notebooks/04_story.ipynb` bao phủ toàn diện 3 trụ cột cốt truyện.<br>• Thiết kế toàn bộ kiến trúc giao diện tương tác Tableau Story Canvas (`dashboard/story_app.py`, `story_canvas.py`, `story_interactions.js`).<br>• Xây dựng cơ chế lọc chéo (cross-filtering) và chuẩn hóa thiết kế no-scroll fixed-viewport. |
| 3 | **Đỗ Thanh Thành Tài** | **24133050** | ML Engineer & Report Lead | • Huấn luyện mô hình Logistic Regression dự báo Top Hit trên tập dữ liệu cấp bài hát không rò rỉ (`notebooks/03_model.ipynb`).<br>• Tích hợp trực quan hóa mô hình (Boundary, Confusion Matrix, Precision-Recall) lên Dashboard.<br>• Soạn thảo Báo cáo tổng kết đồ án (`reports/Bao_cao_Spotify_Chuong_1_3_4.docx`) và phụ trách Video Demo thuyết trình. |

---

## 📑 7. Tài liệu Tham khảo & Báo cáo Kèm theo

* 📂 **[Kho Dữ liệu Đồ án Đầy đủ (Google Drive)](https://drive.google.com/drive/u/0/folders/1TN3uZLE9xYq-DDukDzQRbkzJK8wCtMYi):** Tải trọn bộ dữ liệu thô và các tệp dữ liệu xử lý lớn.
* 📖 [Hướng dẫn Cài đặt & Sử dụng Dashboard](docs/HUONG_DAN_CAI_DAT_VA_SU_DUNG.md): Cẩm nang hướng dẫn thao tác chi tiết từng tính năng và xử lý lỗi.
* 📚 [Từ điển Dữ liệu Toàn diện (Data Dictionary)](docs/data_dictionary.md): Đặc tả chi tiết các bảng thô, Data Marts và công thức tính toán.
* 🔄 [Kiến trúc Luồng Xử lý Dữ liệu (Data Processing Flow)](docs/data_processing_flow.md): Sơ đồ Mermaid, quy trình ETL và luồng dữ liệu hợp nhất.
* 📋 [Kế hoạch Phân công Công việc (Team Tasks Assignment)](docs/team_tasks_assignment.md): Barem chấm điểm chi tiết và tiến độ phân công nhiệm vụ.
* 📹 **Link Video Demo:** *(Cập nhật tại buổi báo cáo)*
* 🖼️ **Link Slide Thuyết trình:** *(Cập nhật tại buổi báo cáo)*
