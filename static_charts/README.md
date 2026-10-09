# Thư mục biểu đồ tĩnh phân tích khám phá dữ liệu (EDA Static Charts)

Thư mục lưu trữ toàn bộ sáu biểu đồ tĩnh được tạo lập và đối soát từ notebook [`notebooks/02_eda.ipynb`](../notebooks/02_eda.ipynb) phục vụ báo cáo đồ án và lưu trữ độc lập.

## Danh mục biểu đồ:

| STT | Tên tập tin | Nội dung biểu đồ | Nguồn dữ liệu |
|---|---|---|---|
| 1 | `01_audio_distributions.png` | Phân phối 5 đặc trưng âm thanh chính (Loudness, Energy, Speechiness, Valence, Duration) | `tracks_dimension.csv` (39,190 bài hát) |
| 2 | `02_spearman_correlation.png` | Ma trận tương quan Spearman của 10 đặc trưng âm học liên tục | `tracks_dimension.csv` (39,190 bài hát) |
| 3 | `03_global_audio_trends.png` | Xu hướng 4 đặc trưng âm thanh theo tuần trên Global Top 200 (2017–2022, Rolling 4 tuần) | `mart_audio_trend_weekly.parquet` (Global, 289 tuần) |
| 4 | `04_happiness_vs_valence.png` | Tương quan điểm hạnh phúc WHR và điểm Valence âm nhạc năm 2021 và 2022 | `mart_country_year.parquet` (68–73 quốc gia) |
| 5 | `05_covid_deaths_vs_audio.png` | Biến động số ca tử vong COVID-19 và đặc trưng âm thanh tuần (Global 2020–2022) | `covid_weekly_clean.csv` & `mart_audio_trend_weekly.parquet` (130 tuần) |
| 6 | `06_target_label_distribution.png` | Phân phối nhãn dự báo Global Top 50 trong 8 tuần trên tập huấn luyện Train | Cohort từ `charts_clean.parquet` (Train: 2,625 bài) |

*Ghi chú: Toàn bộ ảnh được xuất ở định dạng PNG độ nét cao, đồng bộ chính xác 100% với các bảng thống kê định lượng trong báo cáo.*
