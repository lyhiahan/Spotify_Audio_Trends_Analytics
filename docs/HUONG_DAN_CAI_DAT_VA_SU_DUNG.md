# Hướng dẫn Cài đặt và Sử dụng Dashboard (Spotify Audio Trends & Analytics)

Tài liệu này cung cấp hướng dẫn chi tiết từ việc thiết lập môi trường, cài đặt các thư viện cần thiết cho đến quy trình vận hành và khai thác các tính năng phân tích trực quan trên **Spotify Audio Trends Dashboard** (`dashboard/story_app.py`).

---

## 1. Giới thiệu tổng quan

Hệ thống dashboard được phát triển dưới dạng **Tableau Story Canvas** tương tác cao, kết hợp giữa nền tảng dữ liệu **Python/Streamlit** và khung trực quan hóa **Plotly.js / HTML5 Canvas**. 

Ứng dụng cho phép khám phá xu hướng âm học toàn diện từ hơn 39.000 bài hát và dữ liệu bảng xếp hạng Spotify Weekly Charts (2017 – 2022) qua **6 phân hệ (Story Points)**:
1. **Main Dashboard:** Toàn cảnh 6 trụ cột âm học cốt lõi.
2. **Hồ sơ âm thanh:** Heatmap Z-score theo tầng thứ hạng và Boxplot 5 thể loại nhạc.
3. **Nghệ sĩ & Hợp tác:** Đòn bẩy hợp tác (Collab vs Solo) và cơ cấu 80 nghệ sĩ dẫn đầu.
4. **Bản sắc địa lý:** Bản đồ thế giới 73 quốc gia và Radar đối đầu ADN âm nhạc.
5. **Dòng chảy thời gian & Xã hội:** Xu hướng rút ngắn thời lượng, tính mùa vụ và tác động đại dịch COVID-19.
6. **Mô hình hóa dự báo:** Không gian phân loại bài Hit Top 50, ma trận nhầm lẫn và hệ số Odds Ratio.

---

## 2. Yêu cầu hệ thống & Môi trường

- **Hệ điều hành:** Windows 10/11, macOS, hoặc Linux.
- **Python:** Phiên bản Python 3.9 trở lên (đã kiểm thử tương thích tốt với Python 3.10 – 3.14).
- **Trình duyệt web:** Google Chrome, Microsoft Edge, Brave hoặc Firefox phiên bản mới nhất.
- **Dữ liệu chuẩn bị:** Thư mục `data/processed/` cần chứa đầy đủ các tệp dữ liệu đã làm sạch:
  - `tracks_dimension.csv`
  - `charts_clean.parquet`
  - `mart_artist_chart.parquet` (hoặc `.csv`)
  - `mart_country_year.parquet` (hoặc `.csv`)
  - `mart_audio_trend_weekly.parquet` (hoặc `.csv`)
  - `covid_weekly_clean.csv`

---

## 3. Hướng dẫn cài đặt từng bước

### Bước 1: Mở thư mục dự án
Mở terminal (PowerShell, Bash hoặc Command Prompt) và điều hướng đến thư mục gốc của dự án:
```powershell
cd d:\LAPTRINH\TUONGTACDATA\DoAn\Spotify_Audio_Trends_Analytics
```

### Bước 2: Tạo và kích hoạt môi trường ảo (Khuyến nghị)
Khởi tạo môi trường ảo Python độc lập để tránh xung đột thư viện:
- **Trên Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```
- **Trên macOS / Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### Bước 3: Cài đặt các thư viện phụ thuộc
Cài đặt toàn bộ các gói thư viện được chỉ định trong `requirements.txt`:
```powershell
pip install -r requirements.txt
```
*Các thư viện chính bao gồm: `streamlit`, `pandas`, `numpy`, `plotly`, `pyarrow`, `fastparquet`, `scikit-learn`.*

---

## 4. Hướng dẫn khởi chạy ứng dụng

Thực thi lệnh Streamlit trực tiếp từ terminal / PowerShell:
```powershell
streamlit run dashboard/story_app.py
```
Màn hình console sẽ xuất hiện địa chỉ truy cập:
```text
  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```
Truy cập đường dẫn trên bằng trình duyệt web để bắt đầu sử dụng. Ngoài ra, bạn cũng có thể mở tệp `docs/spotify_data_story.html` để xem bản story tương tác độc lập mà không cần môi trường Python.

---

## 5. Cấu trúc thư mục nguồn của Dashboard

```text
dashboard/
├── story_app.py            # Entrypoint chính khởi chạy ứng dụng Streamlit
├── story_canvas.py         # Trình dựng Workbook, cấu hình tabs và nhúng dữ liệu
├── story_canvas.html       # Bộ khung HTML5, layout CSS và typography
├── story_interactions.js   # Động cơ tương tác Plotly, liên kết bộ lọc và cross-filtering
├── story_data.py           # Module trích xuất và tiền xử lý dữ liệu từ data mart
├── story_charts.py         # Khởi tạo các biểu đồ phân tích thành phần
├── story_analysis.py       # Phân tích slot xếp hạng và thuật toán xếp hạng nghệ sĩ
└── eda_data.py             # Đọc dữ liệu EDA tổng quan ban đầu
```

---

## 6. Hướng dẫn sử dụng & Khai thác các tính năng

### Bố cục giao diện tổng thể
Giao diện được thiết kế theo chuẩn Tableau Storyboard cố định khung nhìn (viewport), bao gồm:
1. **Thanh điều hướng Story Points (Phía trên):** Các thẻ điều hướng chuyển đổi linh hoạt giữa 6 màn hình phân tích.
2. **Khu vực hiển thị biểu đồ chính (Trung tâm):** Nơi hiển thị các biểu đồ trực quan hóa Plotly tương tác.
3. **Bảng điều khiển & Diễn giải phân tích (Cột bên phải):**
   - **Bộ lọc động:** Cho phép chọn năm, vùng địa lý, thể loại, tình trạng đơn ca/hợp tác.
   - **Thẻ KPI định lượng:** Tự động tính toán lại giá trị trung bình/trung vị theo dữ liệu đang lọc.
   - **Ghi chú học thuật:** Cung cấp giải thích nguyên nhân và kết luận khoa học dựa trên dữ liệu.

---

### Hướng dẫn tương tác trên từng Story Point

#### 1. Main Dashboard (Toàn cảnh xu hướng âm thanh & Công thức Hit)
- **Mục tiêu:** Cung cấp cái nhìn bao quát về 6 trụ cột âm nhạc chỉ trên một màn hình duy nhất.
- **Tương tác liên kết (Cross-filtering):**
  - **Click vào một quốc gia trên bản đồ:** Tự động gán quốc gia đó vào trục đối đầu trên biểu đồ Radar kế bên.
  - **Click vào một ô trên Heatmap:** Khóa chọn đặc trưng âm học tương ứng để kiểm tra phân vị.
  - **Click vào một mốc thời gian trên chuỗi thời lượng:** Lọc phạm vi năm tương ứng cho toàn bảng.

#### 2. Hồ sơ âm thanh (Hits Profile)
- **Heatmap Z-score 9 đặc trưng theo 4 tầng thứ hạng:**
  - Nhấp chuột vào các ô đỏ (+SD) hoặc xanh (-SD) để xem chi tiết mức độ phân hóa âm học giữa Top 1–10 và Hạng 101–200.
- **Boxplot phân phối 5 thể loại nhạc:**
  - Sử dụng menu thả xuống (Dropdown) để chuyển đổi tức thì giữa 4 thuộc tính: `Energy`, `Danceability`, `Valence`, và `Tempo`.
  - Rê chuột (Hover) lên các hộp để đọc chính xác giá trị trung vị (median), tứ phân vị (Q1, Q3) và giá trị trung bình (mean).

#### 3. Nghệ sĩ & Hợp tác (Artists & Collaboration)
- **Scatter plot tên tuổi vs Lượt stream 8 tuần:** Quan sát tương quan giữa thâm niên/quy mô bài hát với khả năng tích lũy stream.
- **Treemap 80 nghệ sĩ dẫn đầu:** Click vào tên nghệ sĩ để lọc dữ liệu stream và theo dõi tỷ trọng đóng góp.
- **Biểu đồ Solo vs Collab:** Đối chiếu sự khác biệt giữa hình thức biểu diễn đơn ca và hợp tác về tổng lượt nghe và số lượng bài hát.

#### 4. Bản sắc địa lý & ADN âm nhạc (Geography & Radar)
- **Bản đồ thế giới Choropleth (73 quốc gia):**
  - Chuyển đổi giữa các chỉ số âm thanh để quan sát sự phân bố địa lý (ví dụ: Valence cực đại tại khu vực Mỹ Latinh).
- **Radar đối đầu 9 đặc trưng:**
  - Chọn Quốc gia A và Quốc gia B từ bộ lọc để so sánh trực quan "dấu vân tay âm học" đa chiều giữa hai thị trường.

#### 5. Dòng chảy thời gian & Xã hội (Temporal & COVID-19)
- **Chuỗi thời lượng bài hát (2017 – 2022):** Quan sát xu hướng co cụm thời lượng bài hát từ mức ~218 giây xuống dải 198 – 206 giây.
- **Tính mùa vụ 12 tháng:** Phân tích sự tăng vọt mang tính chu kỳ của Acousticness vào tháng 12 hàng năm.
- **Tương quan COVID-19:** Đối chiếu từng đặc trưng âm thanh với chuỗi số ca tử vong theo tuần để nhận diện tác động của các đợt giãn cách xã hội.

#### 6. Mô hình hóa dự báo (Predictive Modeling)
- **Ranh giới phân loại 2D (Decision Boundary):** Trực quan hóa khả năng phân tách bài hát lọt Top 50 dựa trên các đặc trưng âm học.
- **Ma trận nhầm lẫn (Confusion Matrix):** Đánh giá độ chính xác thực tế, tỷ lệ True Positive và False Positive của mô hình.
- **Đường cong đánh đổi Precision – Recall:** Kéo thanh trượt ngưỡng phân loại (threshold $\tau$) để quan sát sự đánh đổi giữa độ chính xác và độ bao phủ.

---

## 7. Các tính năng xuất báo cáo & Lưu cấu hình

Ở góc trên bảng điều khiển, bạn có thể sử dụng các công cụ tiện ích:
- **Tải ảnh biểu đồ (PNG):** Nhấp vào biểu tượng máy ảnh trên thanh công cụ Plotly của từng biểu đồ để lưu hình ảnh chất lượng cao.
- **Khôi phục mặc định (Reset):** Nhấn nút khôi phục để đưa tất cả các bộ lọc và góc nhìn về trạng thái ban đầu của Story Point.
- **Chế độ trình chiếu toàn màn hình:** Nhấn phím `F11` trên trình duyệt để chuyển sang chế độ thuyết trình chuyên nghiệp.

---

## 8. Xử lý sự cố thường gặp (Troubleshooting)

| Tình huống / Lỗi | Nguyên nhân | Cách khắc phục |
| :--- | :--- | :--- |
| **Báo lỗi `FileNotFoundError` khi khởi động** | Thiếu tệp dữ liệu đã làm sạch trong thư mục `data/processed/`. | Đảm bảo các tệp `charts_clean.parquet`, `tracks_dimension.csv`,... đã nằm đúng trong thư mục `data/processed/`. |
| **Cổng 8501 hoặc 8502 đã bị chiếm dụng** | Một tiến trình Streamlit khác đang chạy ngầm. | Chạy lệnh `streamlit run dashboard/story_app.py --server.port 8505` để đổi sang cổng trống khác. |
| **Giao diện không cập nhật sau khi sửa code** | Trình duyệt hoặc Streamlit lưu bộ nhớ đệm cũ. | Nhấn tổ hợp phím `Ctrl + F5` trên trình duyệt, hoặc nhấn phím `C` trong Streamlit để xóa cache dữ liệu. |
| **Bản đồ thế giới không tải được ranh giới** | Mất kết nối Internet khi tải dữ liệu bản đồ nền Plotly. | Kiểm tra lại kết nối mạng Internet của thiết bị để Plotly tải dữ liệu địa giới quốc gia. |
