# 🎵 NGHIÊN CỨU VÀ TRỰC QUAN HÓA CÁC ĐẶC TRƯNG ÂM THANH & DỰ ĐOÁN XU HƯỚNG BÀI HÁT THỊNH HÀNH TRÊN SPOTIFY
> **Đồ án môn học:** Tương tác Dữ liệu (Interactive Data Visualization / Visual Analytics)  
> **Nền tảng phát triển:** Python, Streamlit, Plotly, Scikit-learn, Pandas.

---

## 📌 1. Giới thiệu Đề tài & Mục tiêu Nghiên cứu
Trong kỷ nguyên số hóa âm nhạc, sự thành công của một bài hát không chỉ đến từ danh tiếng của nghệ sĩ mà còn gắn liền mật thiết với các **đặc trưng âm thanh (Audio Features)** như độ bắt tai (*danceability*), năng lượng (*energy*), cảm xúc (*valence*), tiết tấu (*tempo*), cũng như **môi trường kinh tế - xã hội (GDP, khu vực địa lý)** của từng thị trường.

Dự án này thực hiện:
1. **Khai phá & Tiền xử lý dữ liệu đa nguồn:** Kết nối 5 bảng dữ liệu lớn (Lịch sử nghệ sĩ bán đĩa chạy nhất, Bảng xếp hạng tuần Spotify, Đặc trưng âm thanh 114,000 bài hát, Dữ liệu mã quốc gia & GDP thế giới).
2. **Thiết kế Dashboard tương tác trực quan:** Cho phép người dùng tùy biến khám phá xu hướng âm nhạc toàn cầu và từng quốc gia thông qua các biểu đồ tương tác thời gian thực (Plotly & Streamlit).
3. **Khai phá Insight & Kể chuyện bằng dữ liệu (Storytelling):** Làm rõ sự chuyển dịch gu âm nhạc và tương quan giữa tiềm lực kinh tế quốc gia với thói quen nghe nhạc.
4. **Mô hình học máy dự báo xu hướng:** Áp dụng thuật toán **Hồi quy Tuyến tính (Linear Regression)** để dự đoán độ phổ biến / lượt stream và **Hồi quy Logistic (Logistic Regression)** để phân loại khả năng bài hát lọt vào Top Trending.

---

## 🗂️ 2. Cấu trúc Thư mục Dự án

```text
PROJECT/
├── .gitignore                          # Ngăn chặn push các file CSV nặng >100MB lên GitHub
├── requirements.txt                    # Danh sách thư viện Python cần cài đặt
├── README.md                           # Giới thiệu đồ án, hướng dẫn chạy và tổng kết
│
├── data/                               # Quản trị dữ liệu đa nguồn
│   ├── raw/                            # 5 tập dữ liệu CSV gốc ban đầu
│   ├── processed/                      # Dữ liệu sau khi làm sạch, chuẩn hóa và JOIN
│   └── sample/                         # Dữ liệu mẫu thu nhỏ (sample) để test và push GitHub
│
├── notebooks/                          # Jupyter Notebooks nghiên cứu & phân tích theo giai đoạn
│   ├── 01_preprocess.ipynb             # Tiền xử lý, chuẩn hóa ID, JOIN 5 bảng
│   ├── 02_eda.ipynb                    # Phân tích khám phá dữ liệu (EDA) đa biến
│   ├── 03_model.ipynb                  # Huấn luyện mô hình Linear/Logistic Regression
│   └── 04_story.ipynb                  # Khai thác Insight chuyên sâu & cốt truyện dữ liệu
│
├── src/                                # Module mã nguồn dùng chung
│   ├── __init__.py
│   ├── data_loader.py                  # Pipeline nạp và tiền xử lý dữ liệu tự động
│   └── models.py                       # Code huấn luyện và suy luận mô hình ML
│
├── dashboard/                          # Ứng dụng Dashboard Tương tác (Streamlit)
│   ├── app.py                          # Trang chủ (Homepage) của Dashboard
│   ├── pages/
│   │   ├── 1_📊_Tong_Quan_Du_Lieu.py   # Tổng quan số liệu, Metrics & Data Dictionary
│   │   ├── 2_🎵_Dac_Trung_Am_Thanh.py # Phân tích tương quan các Audio Features
│   │   ├── 3_🌍_Kinh_Te_va_Am_Nhac.py  # Bản đồ thế giới, phân tích GDP vs Lượng Stream
│   │   ├── 4_🤖_Du_Bao_Thinh_Hanh.py  # Công cụ tương tác nhập đặc trưng dự báo Trending
│   │   └── 5_📖_Cau_Chuyen_Du_Lieu.py # Data Storytelling & Báo cáo Insight
│   └── assets/                         # Hình ảnh, icon minh họa
│
├── docs/                               # Tài liệu học thuật & Báo cáo
│   ├── data_dictionary.md              # Từ điển dữ liệu chi tiết cho toàn bộ 5 bảng
│   ├── team_tasks_assignment.md        # Bảng phân chia công việc chi tiết cho các thành viên
│   └── final_report.docx               # Báo cáo tổng kết 7 mục theo yêu cầu đồ án
│
└── models/                             # Lưu trữ mô hình Machine Learning (.pkl)
    └── trend_predictor.pkl
```

---

## 🚀 3. Hướng dẫn Cài đặt & Chạy ứng dụng

### Bước 1: Clone kho lưu trữ về máy
```bash
git clone <URL_REPO_GITHUB_CỦA_NHÓM>
cd PROJECT
```

### Bước 2: Tạo môi trường ảo & Cài đặt thư viện
```bash
# Tạo môi trường ảo (Khuyến nghị)
python -m venv venv

# Kích hoạt môi trường:
# Trên Windows:
venv\Scripts\activate
# Trên macOS / Linux:
source venv/bin/activate

# Cài đặt các gói phụ thuộc
pip install -r requirements.txt
```

### Bước 3: Khởi chạy Dashboard Tương tác (Streamlit)
```bash
streamlit run dashboard/app.py
```
Sau khi chạy, mở trình duyệt tại địa chỉ: `http://localhost:8501`.

---

## 👥 4. Phân công Nhiệm vụ Thành viên (Theo Barem 10 điểm)

Chi tiết bảng phân công và ma trận trách nhiệm được lưu tại: [`docs/team_tasks_assignment.md`](docs/team_tasks_assignment.md).

| STT | Họ và tên | MSSV | Vai trò chính | Nhiệm vụ đảm nhiệm |
| :---: | :--- | :---: | :--- | :--- |
| 1 | *Nguyễn Văn A* | *XXXXXXXX* | Leader / Data Engineer | Tiền xử lý dữ liệu, Join 5 bảng, Quản lý Repo Git |
| 2 | *Trần Thị B* | *XXXXXXXX* | Data Analyst | Phân tích EDA, Trực quan hóa đặc trưng âm học |
| 3 | *Lê Văn C* | *XXXXXXXX* | Frontend / Dashboard Dev | Xây dựng Dashboard tương tác Streamlit/Plotly |
| 4 | *Phạm Thị D* | *XXXXXXXX* | ML & Documentation | Mô hình Hồi quy dự báo, Storytelling, Video Demo |

---

## 📹 5. Video Demo & Báo cáo
* **Link Video Demo (YouTube / Google Drive):** `[CẬP NHẬT LINK VIDEO TẠI ĐÂY]` *(Bắt buộc theo barem)*
* **Link Slide Thuyết trình:** `[CẬP NHẬT LINK CANVA/GOOGLE SLIDE TẠI ĐÂY]`
* **Từ điển dữ liệu chi tiết:** Xem tại [`docs/data_dictionary.md`](docs/data_dictionary.md).
