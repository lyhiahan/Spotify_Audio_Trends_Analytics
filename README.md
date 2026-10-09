# 🎵 SPOTIFY AUDIO TRENDS & ANALYTICS
## Nghiên cứu - trực quan hóa các đặc trưng âm thanh và dự đoán xu hướng bài hát thịnh hành trên Spotify.

> **Đồ án môn học:** Tương tác Dữ liệu (Interactive Data Visualization / Visual Analytics)  
> **Nền tảng phát triển:** Python 3.10+, Streamlit, Plotly Interactive, Scikit-learn, Pandas, Seaborn.  
> **Kiến trúc dữ liệu:** Master Dataset Hợp nhất 38 Cột & Hệ thống Data Marts Chuyên biệt (Version 3.5).

---

## 📌 1. Giới thiệu đề tài và mục tiêu nghiên cứu

Trong kỷ nguyên số hóa âm nhạc trực tuyến, sự thành công của một bản thu không chỉ phụ thuộc vào độ nhận diện của nghệ sĩ mà còn gắn liền mật thiết với **các đặc trưng âm thanh (Audio Features)** nội tại (như *danceability*, *energy*, *valence*, *tempo*, *acousticness*), **chiến lược phát hành** (đơn ca vs. hợp tác biểu diễn), cũng như **bản sắc văn hóa - xã hội** và **các biến cố thời gian** (tính mùa vụ, đại dịch toàn cầu).

Đề tài giải quyết trọn vẹn 4 mục tiêu học thuật và ứng dụng thực tiễn:
1. **Kiến trúc Master Pipeline & Data Marts:** Tích hợp 5 tập dữ liệu đa nguồn (>1.9 triệu dòng thô), làm sạch và xuất ra hệ thống Data Marts tối ưu hóa định dạng Parquet/CSV, phục vụ song song cho phân tích trực quan hóa quy mô lớn và mô hình học máy cấp bài hát không rò rỉ dữ liệu.
2. **Khám phá insight và kể chuyện bằng dữ liệu (Data Storytelling) qua 3 Trụ cột cốt truyện:**
   * **Trụ cột 1 — Công thức tạo Hit & Xu hướng Thời đại (Hit Formula & Dynamics):**
     * *Phân tầng thứ hạng:* Ma trận z-score bóc tách sự khác biệt âm học giữa nhóm dẫn đầu (Top 1–10) và nhóm bám đuổi (Top 101–200).
     * *Sức mạnh Hợp tác (Collab vs. Solo):* Đơn ca chiếm tới 60.8% số lượng phát hành, nhưng các dự án Hợp tác (Collab) đạt trung bình **53.7 triệu lượt stream/bài** (gấp hơn 3 lần so với 17.7 triệu của Đơn ca).
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
│   ├── raw/                            # 5 tập dữ liệu CSV gốc ban đầu (>1.9M dòng)
│   │   ├── best-selling-artists.csv    # 121 dòng × 7 cột (Nghệ sĩ bán đĩa chạy nhất lịch sử)
│   │   ├── country_codes.csv           # 217 dòng × 3 cột (Mã ISO-3, vùng địa lý, nhóm thu nhập)
│   │   ├── gdp_data.csv                # 13,365 dòng × 4 cột (Chuỗi thời gian GDP World Bank)
│   │   ├── spotify-tracks-dataset.csv  # 114,000 dòng × 22 cột (Đặc trưng âm thanh & thể loại)
│   │   └── spotify-weekly-charts.csv   # 1,787,999 dòng × 36 cột (Top 200 Weekly Charts 796.6 MB)
│   │
│   └── processed/                      # Hệ sinh thái dữ liệu sạch và Data Marts chuẩn mực
│       ├── charts_clean.parquet        # Bảng sự kiện Top 200 làm sạch (1.78M dòng × 34 cột)
│       ├── tracks_dimension.csv        # 39,190 bài hát (12 đặc trưng âm thanh & metadata)
│       ├── mart_audio_trend_weekly.parquet # Chuỗi thời gian 290 tuần xu hướng âm học
│       ├── mart_artist_chart.parquet   # Thống kê thành tích & lượt stream theo nghệ sĩ
│       ├── mart_artist_chart.csv       # Bản CSV tương thích của mart_artist_chart
│       ├── mart_country_year.parquet   # Dữ liệu âm học & báo cáo hạnh phúc WHS (73 quốc gia)
│       ├── covid_weekly_clean.csv      # Chuỗi thời gian số ca tử vong COVID-19 theo tuần
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
├── dashboard/                          # Ứng dụng Dashboard Story tương tác (Streamlit & Plotly)
│   ├── story_app.py                    # Ứng dụng dashboard chính
│   ├── story_canvas.py                 # Bộ khung dựng story canvas
│   ├── story_charts.py                 # Các thành phần biểu đồ tương tác
│   └── story_data.py                   # Xử lý và nạp dữ liệu cho story
│
├── docs/                               # Tài liệu học thuật & Báo cáo kỹ thuật
│   ├── data_dictionary.md              # Từ điển dữ liệu toàn diện (bảng thô, Data Marts & ML Dataset)
│   ├── data_processing_flow.md         # Tài liệu kiến trúc luồng dữ liệu hợp nhất v3.5
│   ├── team_tasks_assignment.md        # Bảng phân công trách nhiệm nhóm theo barem 10 điểm
│   ├── story_studio.md                 # Hướng dẫn dashboard và phạm vi dữ liệu
│   └── spotify_data_story.html         # Bản story tương tác độc lập
│
└── models/                             # Lưu trữ mô hình Machine Learning đã huấn luyện
    └── trend_predictor.pkl
```

---

## ⚡ 3. Các Tệp Dữ liệu Đầu ra (Output Datasets)

> [!IMPORTANT]
> 📂 **Kho Dữ Liệu Đồ Án Đầy Đủ (Google Drive):**  
> Do giới hạn dung lượng 100MB của GitHub đối với các tệp dữ liệu lớn (`spotify-weekly-charts.csv` ~796 MB, `merged_spotify_data.csv` ~308 MB), toàn bộ dữ liệu thô và dữ liệu đã xử lý được lưu trữ công khai tại:  
> 👉 **[TươngTacData - Google Drive](https://drive.google.com/drive/u/0/folders/1TN3uZLE9xYq-DDukDzQRbkzJK8wCtMYi)**

| Tên tập dữ liệu | Định dạng | Quy mô (Dòng × Cột) | Đối tượng phục vụ | Mục đích sử dụng |
| :--- | :---: | :---: | :--- | :--- |
| **`charts_clean.parquet`** | Parquet | 1,787,531 × 34 | Toàn nhóm | Fact table trung tâm; phục vụ trích xuất Data Marts, EDA, Story và huấn luyện ML tại `03_model.ipynb`. |
| **`tracks_dimension.csv`** | CSV | 39,190 × 21 | Toàn nhóm | Bảng chiều độc nhất 39,190 bài hát với 12 đặc trưng âm học nội tại và thông tin phát hành. |
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

### Bước 3: Thực thi Pipeline Tiền xử lý & Xuất dữ liệu
```bash
# Chạy toàn bộ Master Pipeline (tự động nạp thô, làm sạch và xuất hệ thống Data Marts):
python src/data_loader.py
```

### Bước 4: Khởi chạy Ứng dụng Dashboard Streamlit
```bash
python -m streamlit run dashboard/story_app.py
```
Sau khi khởi chạy thành công, truy cập giao diện dashboard tại địa chỉ: `http://localhost:8501`.

Hoặc khởi chạy cổng riêng bằng lệnh:
```powershell
./start_story.ps1
```
(Mở tại `http://localhost:8502`).

Dashboard mở đầu bằng điểm “Cái nhìn về dữ liệu”, gồm bốn hình Matplotlib/Seaborn lấy trực tiếp từ `02_eda.ipynb`: phân phối audio, tương quan Spearman, phân phối nhãn Train và xu hướng âm thanh theo tuần. Bốn hình nằm trên cùng một màn hình; có thể xem lớn và tải hình gốc. Sau đó là bốn điểm về hồ sơ âm thanh, nghệ sĩ, địa lý và thời gian. Mỗi story point hiển thị một dashboard gồm các biểu đồ cùng chủ đề trên một màn hình, có bộ lọc đa cấp, drill-down, tooltip và lọc chéo. Xem thêm [hướng dẫn và phạm vi dữ liệu](docs/story_studio.md), hoặc tải [bản HTML tương tác độc lập](docs/spotify_data_story.html). (Lưu ý: Bản đồ cần kết nối mạng để tải địa giới quốc gia).

---

## 👥 5. Phân công Trách nhiệm Nhóm (Theo Barem 10 Điểm)

Chi tiết kế hoạch thực hiện và ma trận đóng góp được lưu tại: [`docs/team_tasks_assignment.md`](docs/team_tasks_assignment.md).

| STT | Họ và tên | MSSV | Vai trò chính | Nhiệm vụ đảm nhiệm theo Barem Đồ án |
| :---: | :--- | :---: | :--- | :--- |
| 1 | **Đinh Quốc Anh** | **24133003** | Data Engineer & Data Analyst | • Xây dựng Kiến trúc Master Pipeline (`src/data_loader.py`).<br>• Làm sạch và kết nối 5 bảng dữ liệu (>1.9M bản ghi).<br>• Xây dựng 9 Calculated Fields và viết `notebooks/01_preprocess.ipynb`.<br>• Thực hiện phân tích EDA tĩnh 8–10 biểu đồ chuyên sâu trong `notebooks/02_eda.ipynb`. |
| 2 | **Lý Gia Hân** | **24133016** | Visualization & Dashboard Dev | • Xây dựng và hoàn thiện hệ thống **9 biểu đồ tương tác chuyên sâu** trong `notebooks/04_story.ipynb` bao phủ 3 trụ cột cốt truyện (Công thức Hit & TikTok-hóa, Bản sắc văn hóa địa lý Việt Nam vs. Nhật Bản, Tính mùa vụ & Khủng hoảng COVID-19).<br>• Thiết kế toàn bộ kiến trúc giao diện bảng điều khiển tương tác đa trang Streamlit (`dashboard/`). |
| 3 | **Đỗ Thanh Thành Tài** | **24133050** | ML Engineer & Demo / Report Lead | • Huấn luyện mô hình Logistic Regression dự báo Top Hit trên tập dữ liệu Song-level không rò rỉ (`notebooks/03_model.ipynb`).<br>• Xây dựng bộ công cụ tương tác dự báo xu hướng thịnh hành trên Dashboard.<br>• Soạn thảo Báo cáo tổng kết đồ án chuẩn IEEE (`docs/final_report.docx`) và quay Video Demo thuyết trình. |

---

## 📑 6. Tài liệu Tham khảo & Báo cáo Đi kèm
* 📂 **[Kho Dữ liệu Đồ án Đầy đủ (Google Drive)](https://drive.google.com/drive/u/0/folders/1TN3uZLE9xYq-DDukDzQRbkzJK8wCtMYi):** Tải trọn bộ dữ liệu thô và các tệp dữ liệu xử lý lớn.
* 📖 [Từ điển Dữ liệu Toàn diện (Data Dictionary)](docs/data_dictionary.md): Đặc tả chi tiết các bảng thô, Data Marts và công thức tính toán.
* 🔄 [Kiến trúc Luồng Xử lý Dữ liệu (Data Processing Flow)](docs/data_processing_flow.md): Sơ đồ Mermaid, quy trình JOIN và luồng dữ liệu.
* 📋 [Kế hoạch Phân công Công việc (Team Tasks Assignment)](docs/team_tasks_assignment.md): Barem chấm điểm chi tiết và tiến độ phân công nhiệm vụ.
* 📹 **Link Video Demo (YouTube / Google Drive):** `[CẬP NHẬT LINK VIDEO TẠI ĐÂY]`
* 📊 **Link Slide Thuyết trình:** `[CẬP NHẬT LINK CANVA/GOOGLE SLIDES TẠI ĐÂY]`
