# 🎵 SPOTIFY AUDIO TRENDS & ANALYTICS
## Nghiên cứu và trực quan hóa các đặc trưng âm thanh và dự đoán xu hướng bài hát thịnh hành trên Spotify

> **Đồ án môn học:** Tương tác Dữ liệu (Interactive Data Visualization / Visual Analytics)  
> **Nền tảng phát triển:** Python 3.10+, Streamlit, Plotly Interactive, Scikit-learn, Pandas, Seaborn.  
> **Kiến trúc dữ liệu:** Master Dataset Hợp nhất 38 Cột & Tập Dữ liệu ML Cấp Bài Hát 19 Cột (Version 3.4).

---

## 📌 1. Giới thiệu đề tài và mục tiêu nghiên cứu

Trong kỷ nguyên số hóa âm nhạc trực tuyến, sự thành công của một bản thu không chỉ phụ thuộc vào độ nhận diện của nghệ sĩ mà còn gắn liền mật thiết với **các đặc trưng âm thanh (Audio Features)** nội tại (như *danceability*, *energy*, *valence*, *tempo*, *acousticness*), cũng như **môi trường kinh tế - xã hội (quy mô GDP, phân tầng thu nhập World Bank)** của từng quốc gia.

Đề tài giải quyết trọn vẹn 4 mục tiêu học thuật và ứng dụng thực tiễn:
1. **Kiến trúc Master Pipeline Hợp nhất:** Tích hợp 5 tập dữ liệu đa nguồn (>1.9 triệu dòng thô), làm sạch và xuất ra **1 tệp dữ liệu lớn duy nhất (Master Dataset)** tích hợp cả Kinh tế - Xã hội và COVID Timeline với đúng **38 cột cốt lõi phục vụ Insight**, đồng thời trích xuất tập dữ liệu cấp bài hát không rò rỉ cho mô hình học máy.
2. **Khám phá insight và kể chuyện bằng dữ liệu (Data Storytelling):**
   * *Nghịch lý Cảm xúc (GDP vs Valence Paradox):* Liệu các nước đang phát triển (GDP trung bình/thấp) có chuộng âm nhạc sôi động và giàu năng lượng hơn để giải tỏa áp lực so với các nước phát triển?
   * *3 Giai đoạn Đại dịch COVID-19 (Timeline Waves 2020 – 2022):* Đo lường sự chuyển biến tâm lý người nghe toàn cầu qua các cột mốc: *Phong tỏa (Lockdown & Shock)*, *Giải tỏa (Vaccine & Escapism)* và *Bình thường mới (Reopening & New Normal)*.
   * *Làn sóng Dịch chuyển Âm nhạc Toàn cầu:* Sự bùng nổ của âm nhạc bản địa Latin (Bad Bunny) và K-Pop (BTS) từ các nước đang phát triển ra toàn thế giới.
3. **Mô hình Học máy Dự báo Xu hướng (Machine Learning):** Áp dụng thuật toán **Hồi quy Logistic (Logistic Regression)** trên tập dữ liệu cấp độ bài hát (Song-level) độc nhất, **triệt tiêu 100% rủi ro rò rỉ dữ liệu (Data Leakage)** để dự báo xác suất một bài hát trở thành Top Hit (`is_trending`).
4. **Hệ thống Dashboard Tương tác Đa chiều (Interactive Visual Analytics):** Xây dựng bảng điều khiển Streamlit gồm 5 trang chuyên sâu với các biểu đồ tương tác thời gian thực (Plotly Choropleth, Radar Chart, Russell Mood Map, Dynamic Scatter Plot).

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
│   └── processed/                      # Tệp dữ liệu sau khi xử lý & kết nối 5 bảng
│       ├── merged_spotify_data.csv     # Master Dataset (1,078,125 dòng × 38 cột, ~308 MB)
│       └── tracks_ml_data.csv          # Song-level ML Dataset (36,699 bài × 19 cột, ~5.5 MB) cho Thành Tài
│
├── notebooks/                          # Jupyter Notebooks nghiên cứu theo Barem đồ án
│   ├── 01_preprocess.ipynb             # Minh họa tiền xử lý, Master Pipeline, 9 biến & EDA tĩnh
│   ├── 02_eda.ipynb                    # Phân tích khám phá dữ liệu (EDA) đa biến chuyên sâu
│   ├── 03_model.ipynb                  # Huấn luyện mô hình Logistic Regression & trực quan hóa ML
│   └── 04_story.ipynb                  # Khai thác Insight chuyên sâu & cốt truyện dữ liệu
│
├── src/                                # Module mã nguồn dùng chung
│   ├── __init__.py
│   └── data_loader.py                  # Pipeline ETL Master Dataset & các hàm nạp dữ liệu tiện ích
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
│   ├── data_dictionary.md              # Từ điển dữ liệu toàn diện (5 bảng thô, Master Dataset 38 cột & ML 19 cột)
│   ├── data_processing_flow.md         # Tài liệu kiến trúc luồng dữ liệu hợp nhất v3.4
│   ├── team_tasks_assignment.md        # Bảng phân công trách nhiệm nhóm theo barem 10 điểm
│   └── final_report.docx               # Báo cáo tổng kết đồ án theo cấu trúc chuẩn IEEE
│
└── models/                             # Lưu trữ mô hình Machine Learning đã huấn luyện
    └── trend_predictor.pkl
```

---

## ⚡ 3. Các Tệp Dữ liệu Đầu ra (Output Datasets)

> [!IMPORTANT]
> 📂 **Kho Dữ Liệu Đồ Án Đầy Đủ (Google Drive):**  
> Do giới hạn dung lượng 100MB của GitHub đối với các tệp dữ liệu lớn (`songs.csv` ~856 MB, `spotify-weekly-charts.csv` ~796 MB, `spotify.csv` ~390 MB), toàn bộ dữ liệu thô và dữ liệu đã xử lý được lưu trữ công khai tại:  
> 👉 **[TươngTacData - Google Drive](https://drive.google.com/drive/u/0/folders/1TN3uZLE9xYq-DDukDzQRbkzJK8wCtMYi)**

| Tên tập dữ liệu | Quy mô (Dòng × Cột) | Dung lượng | Đối tượng phục vụ | Mục đích sử dụng |
| :--- | :---: | :---: | :--- | :--- |
| **`merged_spotify_data.csv`** | 1,078,125 × 38 | ~308 MB | **Toàn nhóm** | • File lớn duy nhất chứa trọn vẹn Insight đồ án: Kinh tế 73 nước + Global, phân loại dòng nhạc vĩ mô (`macro_genre`). |
| **`tracks_ml_data.csv`** | 36,699 × 19 | ~5.5 MB | **Đỗ Thanh Thành Tài** | • Cấp độ bài hát (Song-level) độc nhất, chống rò rỉ dữ liệu cho mô hình hồi quy (Tỷ lệ Hit: 35.9%). |

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
# Chạy toàn bộ Master Pipeline (tự động nạp thô, làm sạch và xuất Master Dataset + ML Dataset):
python src/data_loader.py
```

### Bước 4: Khởi chạy Ứng dụng Dashboard Streamlit
```bash
streamlit run dashboard/app.py
```
Sau khi khởi chạy thành công, truy cập giao diện dashboard tại địa chỉ: `http://localhost:8501`.

---

## 💻 5. Sử dụng Module Nạp Dữ liệu trong Code Python

Các thành viên có thể nạp trực tiếp dữ liệu vào Jupyter Notebooks hoặc Dashboard pages bằng các hàm tiện ích:

```python
# 1. Nạp file Master lớn duy nhất (merged_spotify_data.csv):
from src.data_loader import load_master_data
df_master = load_master_data()  # hoặc load_master_data(nrows=50000)

# 2. Nạp tập dữ liệu Song-level cho Thành Tài huấn luyện Machine Learning:
from src.data_loader import load_ml_data
df_ml = load_ml_data()
```

---

## 👥 6. Phân công Trách nhiệm Nhóm (Theo Barem 10 Điểm)

Chi tiết kế hoạch thực hiện và ma trận đóng góp được lưu tại: [`docs/team_tasks_assignment.md`](docs/team_tasks_assignment.md).

| STT | Họ và tên | MSSV | Vai trò chính | Nhiệm vụ đảm nhiệm theo Barem Đồ án |
| :---: | :--- | :---: | :--- | :--- |
| 1 | **Đinh Quốc Anh** | **24133003** | Data Engineer & Data Analyst | • Xây dựng Kiến trúc Master Pipeline (`src/data_loader.py`).<br>• Làm sạch và kết nối 5 bảng dữ liệu (>1.9M bản ghi).<br>• Xây dựng 9 Calculated Fields và viết `notebooks/01_preprocess.ipynb`.<br>• Thực hiện phân tích EDA tĩnh 8–10 biểu đồ chuyên sâu trong `notebooks/02_eda.ipynb`. |
| 2 | **Lý Gia Hân** | **24133016** | Visualization & Dashboard Dev | • Thiết kế toàn bộ giao diện tương tác Streamlit đa trang (`dashboard/`).<br>• Xây dựng Bản đồ tương tác thế giới Choropleth, Radar Chart và Russell Mood Map.<br>• Phân tích cốt truyện dữ liệu: Nghịch lý GDP vs Valence và 3 Pha COVID-19 trong `notebooks/04_story.ipynb`. |
| 3 | **Đỗ Thanh Thành Tài** | **24133050** | ML Engineer & Demo / Report Lead | • Huấn luyện mô hình Logistic Regression dự báo Top Hit trên tập dữ liệu Song-level không rò rỉ (`notebooks/03_model.ipynb`).<br>• Xây dựng bộ công cụ tương tác dự báo trên Dashboard Trang 4.<br>• Soạn thảo Báo cáo tổng kết đồ án chuẩn IEEE (`docs/final_report.docx`) và quay Video Demo thuyết trình. |

---

## 📑 7. Tài liệu Tham khảo & Báo cáo Đi kèm
* 📂 **[Kho Dữ liệu Đồ án Đầy đủ (Google Drive)](https://drive.google.com/drive/u/0/folders/1TN3uZLE9xYq-DDukDzQRbkzJK8wCtMYi):** Tải trọn bộ dữ liệu thô (`songs.csv`, `spotify-weekly-charts.csv`) và dữ liệu gộp (`spotify.csv`).
* 📖 [Từ điển Dữ liệu Toàn diện (Data Dictionary)](docs/data_dictionary.md): Đặc tả chi tiết các bảng thô, Master Dataset và công thức tính toán.
* 🔄 [Kiến trúc Luồng Xử lý Dữ liệu (Data Processing Flow)](docs/data_processing_flow.md): Sơ đồ Mermaid, quy trình JOIN và luồng dữ liệu.
* 📋 [Kế hoạch Phân công Công việc (Team Tasks Assignment)](docs/team_tasks_assignment.md): Barem chấm điểm chi tiết và tiến độ phân công nhiệm vụ.
* 📹 **Link Video Demo (YouTube / Google Drive):** `[CẬP NHẬT LINK VIDEO TẠI ĐÂY]`
* 📊 **Link Slide Thuyết trình:** `[CẬP NHẬT LINK CANVA/GOOGLE SLIDES TẠI ĐÂY]`
