# BẢNG PHÂN CHIA NHIỆM VỤ THÀNH VIÊN (PROJECT CUỐI KỲ)
**Môn học:** Tương tác Dữ liệu (Data Interaction / Interactive Visualization)  
**Đề tài:** Nghiên cứu và trực quan hóa các đặc trưng âm thanh và dự đoán xu hướng bài hát thịnh hành trên Spotify

---

## I. Ma trận Ánh xạ Nhiệm vụ theo Barem Chấm điểm (10 Điểm)

| Mục theo Barem | Trọng số & Yêu cầu | Nhiệm vụ kỹ thuật cần hoàn thành | Phân công vai trò |
| :--- | :--- | :--- | :--- |
| **1. Giới thiệu đề tài & Mô tả dữ liệu** | 0.5 - 1.0 điểm | Viết bối cảnh, lý do chọn đề tài, mục tiêu phân tích.<br>Lập Data Dictionary đầy đủ 5 bảng (`docs/data_dictionary.md`). | Leader / Data Analyst |
| **2. Tiền xử lý & Khám phá dữ liệu (EDA)** | 2.0 - 2.5 điểm | • Viết code làm sạch, xử lý Missing/Outlier, trích xuất ID.<br>• Viết thuật toán JOIN 5 bảng dữ liệu.<br>• Phân tích EDA phân phối đơn biến, đa biến, ma trận tương quan các chỉ số âm học (`valence`, `danceability`, `energy`...). | Data Engineer / Data Analyst |
| **3. Thiết kế Dashboard Tương tác** | 2.5 - 3.0 điểm | • Xây dựng Web App tương tác (Streamlit / Plotly Dash).<br>• Thiết kế luồng tương tác đa chiều (Dropdown bộ lọc theo Quốc gia/Năm, Slider độ dài, Checkbox thể loại, Hover tooltip).<br>• Phân trang logic (Tổng quan $\rightarrow$ Âm học $\rightarrow$ Kinh tế $\rightarrow$ Dự báo). | Frontend / Visualization Specialist |
| **4. Khai phá Insight & Storytelling** | 1.5 - 2.0 điểm | • Đúc kết ít nhất 3-5 insight sâu sắc (ví dụ: Sự chuyển dịch xu hướng âm nhạc trong mùa dịch 2021-2022; Tương quan GDP và dòng nhạc thịnh hành; Nghệ sĩ huyền thoại vs hiện đại).<br>• Xây dựng kịch bản "Kể chuyện bằng dữ liệu" (Storytelling). | Business Analyst / Data Storyteller |
| **5. Mô hình dự báo (ML Modeling)** | 1.5 điểm | • Xây dựng mô hình Hồi quy tuyến tính (Dự đoán `streams` / `popularity`) hoặc Hồi quy Logistic (Dự đoán xác suất lọt Top Trend 1/0).<br>• Đánh giá mô hình ($R^2$, RMSE, Accuracy, ROC-AUC, Confusion Matrix).<br>• Tích hợp form dự báo tương tác vào Dashboard. | ML Engineer / Data Scientist |
| **6. Cài đặt & Video Demo** | 0.5 điểm | • Đóng gói mã nguồn, viết `README.md`, `requirements.txt`.<br>• Quay video demo luồng tương tác (kèm link backup YouTube/Google Drive). | All / Technical Lead |
| **7. Báo cáo & Tài liệu tham khảo** | 0.5 điểm | Soạn báo cáo Word/PDF hoàn chỉnh theo cấu trúc 7 mục, chuẩn bị Slide thuyết trình. | Leader & Thư ký nhóm |

---

## II. Gợi ý Phân công theo Quy mô Nhóm

### Phương án A: Nhóm 4 thành viên (Khuyên dùng)
* **Thành viên 1 (Trưởng nhóm - Data Pipeline & Project Manager):**
  * Quản lý tiến độ Git, cấu trúc repo.
  * Phụ trách Mục 1 (Mô tả bài toán, Data Dictionary) & Mục 2 (Làm sạch, chuẩn hóa, Join 5 bảng dữ liệu).
  * Viết notebook `01_preprocess.ipynb`.

* **Thành viên 2 (Data Analyst & EDA Specialist):**
  * Phụ trách Mục 2 (EDA chuyên sâu) & Mục 4 (Khai phá Insight & Storytelling).
  * Vẽ biểu đồ tương quan nhiệt (Correlation Matrix), phân tích xu hướng âm thanh theo thời gian và quốc gia.
  * Viết notebook `02_eda.ipynb` và nội dung trang Kể chuyện dữ liệu.

* **Thành viên 3 (Visualization & Dashboard Developer):**
  * Phụ trách Mục 3 (Thiết kế Dashboard tương tác bằng Streamlit/Plotly).
  * Xây dựng giao diện đa trang (`dashboard/app.py`, các trang phân tích âm thanh, bản đồ thế giới choropleth map).
  * Đảm bảo tính tương tác cao: filter thời gian, cross-filtering, tooltip, responsive layout.

* **Thành viên 4 (Machine Learning & Documentation/Demo):**
  * Phụ trách Mục 5 (Huấn luyện mô hình Linear/Logistic Regression, đánh giá metrics trong notebook `03_model.ipynb`).
  * Tích hợp model vào Dashboard (tab Dự báo tương tác) và tổng hợp kịch bản trong `04_story.ipynb`.
  * Phụ trách Mục 6 & 7: Viết tài liệu hướng dẫn cài đặt, quay video demo, tổng hợp slide thuyết trình.

---

### Phương án B: Nhóm 3 thành viên
* **Thành viên 1:** Mục 1, Mục 2 (Data Preprocessing, Join & Pipeline).
* **Thành viên 2:** Mục 3 (Dashboard Tương tác) & Mục 5 (Tích hợp Model ML).
* **Thành viên 3:** Mục 2 (EDA), Mục 4 (Insight & Storytelling), Mục 6 & 7 (Video demo, Báo cáo & Slide).

---

### Phương án C: Nhóm 5 thành viên
* **Thành viên 1 (Leader):** Kiến trúc hệ thống, Mục 1, Pipeline Join & Chuẩn hóa dữ liệu.
* **Thành viên 2:** Phân tích EDA, Trực quan hóa đặc trưng âm học & thị trường.
* **Thành viên 3:** Lập trình Dashboard Streamlit (Giao diện chính, Bộ lọc động, Biểu đồ Plotly).
* **Thành viên 4:** Huấn luyện mô hình ML (Linear/Logistic Regression), Feature Importance.
* **Thành viên 5:** Viết nội dung Storytelling (Mục 4), Video Demo & Báo cáo tổng kết (Mục 6, 7).
