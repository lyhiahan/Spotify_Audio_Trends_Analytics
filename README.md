# 🎵 SPOTIFY AUDIO TRENDS & ANALYTICS
## Nghiên cứu và Trực quan hóa các Đặc trưng Âm thanh & Dự đoán Xu hướng Bài hát Thịnh hành trên Spotify

> **Đồ án môn học:** Tương tác Dữ liệu (Interactive Data Visualization / Visual Analytics)  
> **Nền tảng phát triển:** Python 3.10+, Streamlit, Plotly Interactive, Scikit-learn, Pandas, Seaborn.  
> **Kiến trúc dữ liệu:** Phân nhánh tối ưu (Early Branching Pipeline Architecture — Version 3.0).

---

## 📌 1. Giới thiệu Đề tài & Mục tiêu Nghiên cứu

Trong kỷ nguyên số hóa âm nhạc trực tuyến, sự thành công của một bản thu không chỉ phụ thuộc vào độ nhận diện của nghệ sĩ mà còn gắn liền mật thiết với **các đặc trưng âm thanh (Audio Features)** nội tại (như *danceability*, *energy*, *valence*, *tempo*, *acousticness*), cũng như **môi trường kinh tế - xã hội (quy mô GDP, cơ cấu dân số, phân tầng thu nhập World Bank)** của từng quốc gia.

Đề tài giải quyết trọn vẹn 4 mục tiêu học thuật và ứng dụng thực tiễn:
1. **Kiến trúc Pipeline Phân nhánh Tối ưu (Branching Pipeline):** Tích hợp 5 tập dữ liệu đa nguồn (>1.9 triệu dòng thô), phân bổ làm sạch và sinh ra **3 tập dữ liệu đầu ra chuyên biệt** phục vụ độc lập cho Phân tích Kinh tế - Xã hội, Dòng thời gian Đại dịch COVID-19 và Huấn luyện Machine Learning.
2. **Khám phá Insight & Kể chuyện bằng Dữ liệu (Data Storytelling):** 
   * *Nghịch lý Cảm xúc (GDP vs Valence Paradox):* Liệu các nước đang phát triển (GDP trung bình/thấp) có chuộng âm nhạc sôi động và giàu năng lượng hơn để giải tỏa áp lực so với các nước phát triển?
   * *3 Giai đoạn Đại dịch COVID-19 (Timeline Waves 2020 – 2022):* Đo lường sự chuyển biến tâm lý người nghe toàn cầu từ *Phong tỏa (Lockdown & Shock)* sang *Giải tỏa (Vaccine & Escapism)* và *Bình thường mới (Reopening & New Normal)*.
   * *Làn sóng Dịch chuyển Âm nhạc Toàn cầu:* Sự bùng nổ của âm nhạc bản địa Latin (Bad Bunny) và K-Pop (BTS) từ các nước đang phát triển ra toàn thế giới.
3. **Mô hình Học máy Dự báo Xu hướng (Machine Learning):** Áp dụng thuật toán **Hồi quy Logistic (Logistic Regression)** trên tập dữ liệu cấp độ bài hát (Song-level) độc nhất, **triệt tiêu 100% rủi ro rò rỉ dữ liệu (Data Leakage)** để dự báo xác suất một bài hát trở thành Top Hit (`is_trending`).
4. **Hệ thống Dashboard Tương tác Đa chiều (Interactive Visual Analytics):** Xây dựng bảng điều khiển Streamlit gồm 5 trang chuyên sâu với các biểu đồ tương tác thời gian thực (Plotly Choropleth, Radar Chart, Russell Mood Map, Dynamic Scatter Plot).

---

## 🗂️ 2. Cấu trúc Thư mục Dự án

```text
PROJECT/
├── .gitignore                          # Cấu hình bỏ qua file >100MB, theo dõi file ML & COVID
├── requirements.txt                    # Danh sách thư viện Python cần cài đặt
├── README.md                           # Giới thiệu đồ án, hướng dẫn cài đặt và tổng kết
│
├── data/                               # Quản trị dữ liệu đa nguồn
│   ├── raw/                            # 5 tập dữ liệu CSV gốc ban đầu (>1.9M dòng)
│   │   ├── best-selling-artists.csv    # 121 dòng × 7 cột (Nghệ sĩ bán đĩa chạy nhất lịch sử)
│   │   ├── country_codes.csv           # 217 dòng × 3 cột (Mã ISO-3, vùng địa lý, nhóm thu nhập)
│   │   ├── gdp_data.csv                # 13,365 dòng × 4 cột (Chuỗi thời gian GDP World Bank)
│   │   ├── spotify-tracks-dataset.csv  # 114,000 dòng × 22 cột (Đặc trưng âm thanh & thể loại)
│   │   └── spotify-weekly-charts.csv   # 1,788,000 dòng × 36 cột (Top 200 Weekly Charts 796.6 MB)
│   │
│   ├── processed/                      # 3 tập dữ liệu chuyên biệt sau Branching Pipeline
│   │   ├── spotify_socioeconomic_2021_2022.csv # Dữ liệu 74 quốc gia (1,051,527 dòng × 40 cột, 378.4 MB)
│   │   ├── spotify_covid_timeline_2020_2022.csv # Dữ liệu Global 3 pha đại dịch (26,598 dòng × 32 cột, 7.6 MB)
│   │   └── tracks_ml_dataset.csv               # Dữ liệu Song-level cho ML (39,202 bài × 18 cột, 6.1 MB)
│   │
│   └── sample/                         # Dữ liệu mẫu rút gọn phục vụ kiểm thử nhanh
│       └── spotify_sample_merged.csv   # Sample 20,000 dòng chuẩn hóa (7.2 MB)
│
├── notebooks/                          # Jupyter Notebooks nghiên cứu theo Barem đồ án
│   ├── 01_preprocess.ipynb             # Minh họa tiền xử lý, Branching Pipeline, 13 biến & EDA tĩnh
│   ├── 02_eda.ipynb                    # Phân tích khám phá dữ liệu (EDA) đa biến chuyên sâu
│   ├── 03_model.ipynb                  # Huấn luyện mô hình Logistic Regression & trực quan hóa ML
│   └── 04_story.ipynb                  # Khai thác Insight chuyên sâu & cốt truyện dữ liệu
│
├── src/                                # Module mã nguồn dùng chung
│   ├── __init__.py
│   ├── data_loader.py                  # Pipeline ETL phân nhánh 3 nhánh & 4 hàm nạp dữ liệu
│   └── models.py                       # Xây dựng và kiểm định mô hình Machine Learning
│
├── dashboard/                          # Ứng dụng Dashboard Tương tác (Streamlit & Plotly)
│   ├── app.py                          # Trang chủ (Homepage) của Dashboard
│   ├── pages/
│   │   ├── 1_📊_Tong_Quan_Du_Lieu.py   # Tổng quan số liệu, Data Quality & Từ điển dữ liệu
│   │   ├── 2_🎵_Dac_Trung_Am_Thanh.py # Phân tích tương quan các Audio Features (Heatmap, Radar)
│   │   ├── 3_🌍_Kinh_Te_va_Am_Nhac.py  # Bản đồ thế giới Choropleth, GDP vs Lượng Stream, Latin/K-Pop
│   │   ├── 4_🤖_Du_Bao_Thinh_Hanh.py  # Công cụ tương tác nhập đặc trưng dự báo Top Trending
│   │   └── 5_📖_Cau_Chuyen_Du_Lieu.py # Data Storytelling: Nghịch lý GDP, 3 Pha COVID Timeline
│   └── assets/                         # Hình ảnh minh họa và assets
│
├── docs/                               # Tài liệu học thuật & Báo cáo kỹ thuật
│   ├── data_dictionary.md              # Từ điển dữ liệu toàn diện (5 bảng thô & 3 bảng processed)
│   ├── data_processing_flow.md         # Tài liệu kiến trúc luồng dữ liệu phân nhánh v3.0
│   ├── team_tasks_assignment.md        # Bảng phân công trách nhiệm nhóm theo barem 10 điểm
│   └── final_report.docx               # Báo cáo tổng kết đồ án theo cấu trúc chuẩn IEEE
│
└── models/                             # Lưu trữ mô hình Machine Learning đã huấn luyện
    └── trend_predictor.pkl
```

---

## ⚡ 3. Ba Nhánh Dữ liệu Mục tiêu (Specialized Datasets)

| Tên tập dữ liệu | Quy mô (Dòng × Cột) | Dung lượng | Thành viên sử dụng | Mục đích phân tích & Trực quan hóa |
| :--- | :---: | :---: | :--- | :--- |
| **`spotify_socioeconomic_2021_2022.csv`** | 1,051,527 × 40 | ~378.4 MB | **Lý Gia Hân** | • Bản đồ Choropleth 74 quốc gia.<br>• Nghịch lý GDP vs Valence.<br>• Phân tầng thu nhập World Bank.<br>• Đo lường thị phần làn sóng Latin & K-Pop. |
| **`spotify_covid_timeline_2020_2022.csv`** | 26,598 × 32 | ~7.6 MB | **Lý Gia Hân** | • Phân tích chuỗi thời gian 3 pha đại dịch toàn cầu (`Lockdown & Shock`, `Vaccine & Escapism`, `Reopening & New Normal`). |
| **`tracks_ml_dataset.csv`** | 39,202 × 18 | ~6.1 MB | **Đỗ Thanh Thành Tài** | • Cấp độ bài hát độc nhất (Song-level).<br>• Chống 100% Data Leakage cho mô hình Logistic Regression.<br>• Nhãn `is_trending` đạt tỷ lệ Hit 35.9%. |
| **`spotify_sample_merged.csv`** | 20,000 × 40 | ~7.2 MB | **Nhóm phát triển** | • Bản mẫu rút gọn để dựng UI Dashboard và kiểm thử biểu đồ siêu tốc trong 0.2 giây. |

---

## 🚀 4. Hướng dẫn Cài đặt & Khởi chạy Dự án

### Bước 1: Clone kho lưu trữ về máy tính
```bash
git clone <URL_REPO_GITHUB_CỦA_NHÓM>
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
# Chạy toàn bộ Branching Pipeline (tự động nạp, làm sạch và xuất cả 3 file processed):
python src/data_loader.py

# (Tùy chọn) Chạy chế độ mẫu thử nhanh với 20,000 dòng:
python src/data_loader.py --sample 20000
```

### Bước 4: Khởi chạy Ứng dụng Dashboard Streamlit
```bash
streamlit run dashboard/app.py
```
Sau khi khởi chạy thành công, truy cập giao diện dashboard tại địa chỉ: `http://localhost:8501`.

---

## 💻 5. Sử dụng Module Nạp Dữ liệu trong Code Python

Các thành viên có thể nạp trực tiếp dữ liệu vào Jupyter Notebooks hoặc Dashboard pages mà không cần viết lại mã nạp CSV:

```python
# 1. Nạp dữ liệu Kinh tế - Xã hội 74 quốc gia:
from src.data_loader import load_socioeconomic_data
df_socio = load_socioeconomic_data()

# 2. Nạp dữ liệu Dòng thời gian 3 pha COVID-19:
from src.data_loader import load_covid_data
df_covid = load_covid_data()

# 3. Nạp dữ liệu Song-level cho Machine Learning:
from src.data_loader import load_ml_data
df_ml = load_ml_data()

# 4. Nạp bản mẫu Sample 20,000 dòng:
from src.data_loader import load_sample_data
df_sample = load_sample_data()
```

---

## 👥 6. Phân công Trách nhiệm Nhóm (Theo Barem 10 Điểm)

Chi tiết kế hoạch thực hiện và ma trận đóng góp được lưu tại: [`docs/team_tasks_assignment.md`](docs/team_tasks_assignment.md).

| STT | Họ và tên | MSSV | Vai trò chính | Nhiệm vụ đảm nhiệm theo Barem Đồ án |
| :---: | :--- | :---: | :--- | :--- |
| 1 | **Đinh Quốc Anh** | **24133003** | Data Engineer & Data Analyst | • Xây dựng Kiến trúc Branching Pipeline (`src/data_loader.py`).<br>• Làm sạch và kết nối 5 bảng dữ liệu (>1.9M bản ghi).<br>• Xây dựng 13 Calculated Fields và viết `notebooks/01_preprocess.ipynb`.<br>• Thực hiện phân tích EDA tĩnh 8–10 biểu đồ chuyên sâu trong `notebooks/02_eda.ipynb`. |
| 2 | **Lý Gia Hân** | **24133016** | Visualization & Dashboard Dev | • Thiết kế toàn bộ giao diện tương tác Streamlit đa trang (`dashboard/`).<br>• Xây dựng Bản đồ tương tác thế giới Choropleth, Radar Chart và Russell Mood Map.<br>• Phân tích cốt truyện dữ liệu: Nghịch lý GDP vs Valence và 3 Pha COVID-19 trong `notebooks/04_story.ipynb`. |
| 3 | **Đỗ Thanh Thành Tài** | **24133050** | ML Engineer & Demo / Report Lead | • Huấn luyện mô hình Logistic Regression dự báo Top Hit trên tập dữ liệu Song-level không rò rỉ (`notebooks/03_model.ipynb`).<br>• Xây dựng bộ công cụ tương tác dự báo trên Dashboard Trang 4.<br>• Soạn thảo Báo cáo tổng kết đồ án chuẩn IEEE (`docs/final_report.docx`) và quay Video Demo thuyết trình. |

---

## 📑 7. Tài liệu Tham khảo & Báo cáo Đi kèm
* 📖 [Từ điển Dữ liệu Toàn diện (Data Dictionary)](docs/data_dictionary.md): Đặc tả chi tiết 5 bảng thô, 3 bảng processed và công thức toán học của 13 Calculated Fields.
* 🔄 [Kiến trúc Luồng Xử lý Dữ liệu (Data Processing Flow)](docs/data_processing_flow.md): Sơ đồ Mermaid, lý do chuyển đổi phân nhánh và báo cáo hiệu năng.
* 📋 [Kế hoạch Phân công Công việc (Team Tasks Assignment)](docs/team_tasks_assignment.md): Barem chấm điểm chi tiết và tiến độ phân công nhiệm vụ.
* 📹 **Link Video Demo (YouTube / Google Drive):** `[CẬP NHẬT LINK VIDEO TẠI ĐÂY]`
* 📊 **Link Slide Thuyết trình:** `[CẬP NHẬT LINK CANVA/GOOGLE SLIDES TẠI ĐÂY]`
