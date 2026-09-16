# BẢNG PHÂN CHIA NHIỆM VỤ THÀNH VIÊN (PROJECT CUỐI KỲ)
**Môn học:** Tương tác Dữ liệu (Interactive Data Visualization / Visual Analytics)  
**Đề tài:** Nghiên cứu và trực quan hóa các đặc trưng âm thanh & dự đoán xu hướng bài hát thịnh hành trên Spotify  
**Quy mô nhóm:** 03 thành viên

---

## I. THÔNG TIN THÀNH VIÊN VÀ VAI TRÒ CHÍNH

| STT | Họ và tên | MSSV | Vai trò chính | Trọng tâm phụ trách |
| :---: | :--- | :---: | :--- | :--- |
| **1** | **Đinh Quốc Anh** | **24133003** | **Data Engineer & Data Analyst** | Xử lý số liệu, Tiền xử lý đa nguồn (Join 5 bảng), Calculated fields & Phân tích EDA tĩnh |
| **2** | **Lý Gia Hân** | **24133016** | **Visualization Specialist & Dashboard Dev** | Trực quan hóa dữ liệu, Thiết kế Dashboard tương tác (Streamlit/Plotly), Bản đồ địa lý & Storytelling |
| **3** | **Đỗ Thanh Thành Tài** | **24133050** | **ML Engineer & Demo / Reporting Lead** | Huấn luyện mô hình dự báo (Linear/Logistic), Trực quan hóa ML trên Dashboard, Quay Video Demo & Báo cáo |

---

## II. MA TRẬN ÁNH XẠ NHIỆM VỤ THEO BAREM CHẤM ĐIỂM (10 ĐIỂM)

Bảng phân công bám sát chính xác từng tiêu chí trong **Rubric đánh giá Đồ án Cuối kỳ**:

| Phần theo Rubric | Điểm | Tiêu chí chi tiết theo Barem | Thành viên phụ trách | Nhiệm vụ cụ thể cần hoàn thành |
| :--- | :---: | :--- | :---: | :--- |
| **1. Thu thập & Tiền xử lý dữ liệu** | **2.5đ** | • **Xác định bài toán & Dataset (0.5đ):** Mục tiêu rõ ràng, dữ liệu $\ge$ 5,000 dòng, $\ge$ 3 bảng, nêu rõ nguồn & Data Dictionary.<br>• **Làm sạch dữ liệu (0.5đ):** Code Python xử lý triệt để Missing values, Outliers, chuẩn hóa ngày tháng/chuỗi.<br>• **Biến đổi dữ liệu (0.75đ):** Join/Merge các bảng chính xác, tạo trường tính toán mới (**Calculated fields**).<br>• **Khám phá dữ liệu EDA (0.75đ):** Dùng Matplotlib/Seaborn vẽ ít nhất 3 - 5 biểu đồ tĩnh phân tích phân phối trước khi đưa lên Dashboard. | **Đinh Quốc Anh** | • Xác định mục tiêu bài toán, xây dựng từ điển dữ liệu (`docs/data_dictionary.md`).<br>• Làm sạch triệt để 5 tập dữ liệu (>300,000 dòng, đạt chuẩn $\ge 5,000$ dòng và $\ge 3$ bảng).<br>• Tạo các cột mới: `is_trending` (0/1), `mood_category`, `stream_share_country`,...<br>• Xây dựng pipeline JOIN 5 bảng trong `src/data_loader.py` và `01_preprocess.ipynb`.<br>• Vẽ $\ge 5$ biểu đồ EDA tĩnh (Heatmap, Distribution, Boxplot) trong `02_eda.ipynb`. |
| **2. Thiết kế Dashboard (Trọng tâm)** | **3.5đ** | • **Giao diện & UI/UX (0.5đ):** Layout hợp lý, màu sắc hài hòa, Legend rõ ràng.<br>• **Đa dạng biểu đồ (1.0đ):** Sử dụng $\ge 8$ loại biểu đồ khác nhau (Bar, Line, Pie, Scatter, Heatmap, Treemap, Radar, Boxplot...).<br>• **Bản đồ không gian (0.5đ):** Ít nhất 1 biểu đồ dạng Geographic Map.<br>• **Tính tương tác (1.5đ):** Bộ lọc đa cấp (Filters), Drill-down, Tooltip khi hover, Cross-filtering. | **Lý Gia Hân** | • Thiết kế giao diện Dashboard Streamlit nhiều trang khoa học, thẩm mỹ.<br>• Xây dựng đầy đủ 8 loại biểu đồ Plotly tương tác chuẩn xác theo loại biến.<br>• Tích hợp **Choropleth Map** thế giới thể hiện phân bổ streams và chỉ số âm thanh (sử dụng mã ISO-3 từ `country_codes.csv`).<br>• Thiết lập bộ lọc liên hoàn nhiều cấp (Vùng $\rightarrow$ Quốc gia $\rightarrow$ Thể loại $\rightarrow$ Thời gian), hover tooltip hiển thị thông tin sâu. |
| **3. Phân tích Insight & Dự báo** | **2.0đ** | • **Khai phá Insight (1.0đ):** Rút ra câu chuyện dữ liệu (Storytelling), phân tích nguyên nhân và xu hướng.<br>• **Mô hình Dự báo (0.5đ):** Áp dụng đúng thuật toán Hồi quy tuyến tính hoặc Logistic.<br>• **Trực quan Dự báo (0.5đ):** Tích hợp kết quả dự báo lên biểu đồ trực quan trong Dashboard. | **Lý Gia Hân** *(Insight & Story)*<br>+<br>**Đỗ Thanh Thành Tài** *(Mô hình & Trực quan ML)* | • **Lý Gia Hân:** Xây dựng trang Data Storytelling khai thác các insight sâu (Nghịch lý cảm xúc theo GDP, sự chuyển biến gu âm nhạc 2021-2022).<br>• **Đỗ Thanh Thành Tài:**<br>  - Xây dựng mô hình Logistic Regression dự báo xác suất bài hát lọt Top Trending trong `03_model.ipynb` và đóng gói model.<br>  - Tích hợp công cụ tương tác dự báo (Interactive Simulator) kèm biểu đồ đo xác suất (Gauge chart / Trendline) trực tiếp trên Dashboard. |
| **4. Báo cáo & Demo ứng dụng** | **2.0đ** | • **Báo cáo khoa học (1.0đ):** Cấu trúc chuẩn, sơ đồ Pipeline hệ thống, trích dẫn IEEE, giải thích logic chọn biểu đồ, minh họa code.<br>• **Ứng dụng Demo (1.0đ):** Dashboard chạy mượt mà, kịch bản lôi cuốn, đóng vai Data Analyst thuyết trình với sếp/khách hàng. | **Đỗ Thanh Thành Tài** *(Lead)*<br>+<br>**Cả nhóm cùng hỗ trợ** | • **Đỗ Thanh Thành Tài:**<br>  - Viết kịch bản và thực hiện quay **Video Demo** chất lượng cao (đóng vai Data Analyst trình bày báo cáo chuyên nghiệp).<br>  - Tổng hợp báo cáo nghiên cứu hoàn chỉnh, bổ sung trích dẫn chuẩn IEEE và giải thích logic trực quan.<br>• **Đinh Quốc Anh & Lý Gia Hân:** Cung cấp sơ đồ pipeline, hình ảnh biểu đồ và giải thích kỹ thuật tương ứng. |

---

## III. CHECKLIST CÔNG VIỆC CHI TIẾT THEO TỪNG THÀNH VIÊN

### 1. Đinh Quốc Anh (Phụ trách: Xử lý số liệu & EDA)
- [ ] Kiểm tra, rà soát missing value và kiểu dữ liệu của cả 5 file dữ liệu trong thư mục `data/raw/`.
- [ ] Chuẩn hóa `track_id`, liên kết mã quốc gia ISO-3 và nạp dữ liệu GDP theo từng năm.
- [ ] Tạo các trường tính toán mới (**Calculated fields**):
  - `is_trending`: Đánh dấu bài hát thuộc nhóm hit bảng xếp hạng (1) hay nhóm nhạc thông thường (0).
  - `mood_category`: Phân loại nhóm cảm xúc bài hát dựa trên ngưỡng `energy` và `valence`.
  - `stream_share_country`: Tỷ trọng đóng góp lượt nghe theo từng quốc gia.
- [ ] Hoàn thiện Notebook `notebooks/01_preprocess.ipynb` và module `src/data_loader.py`.
- [ ] Hoàn thiện Notebook `notebooks/02_eda.ipynb` với ít nhất **5 biểu đồ tĩnh** chuẩn mực (Matplotlib/Seaborn):
  - Biểu đồ phân phối đa biến các Audio Features.
  - Biểu đồ nhiệt (Heatmap) ma trận tương quan giữa âm học và lượt nghe.
  - Boxplot so sánh đặc trưng âm thanh giữa các thể loại/nhóm thu nhập.
- [ ] Vẽ sơ đồ luồng dữ liệu (Data Pipeline Architecture) phục vụ Báo cáo cuối kỳ.

### 2. Lý Gia Hân (Phụ trách: Trực quan hóa & Dashboard Tương tác)
- [ ] Thiết kế cấu trúc giao diện Dashboard đa trang trên Streamlit (`dashboard/app.py` và các trang trong `dashboard/pages/`).
- [ ] Đảm bảo tiêu chuẩn UI/UX: Giao diện hiện đại, tone màu đồng bộ, bố cục chia cột khoa học, nhãn/chú thích (Legend) rõ ràng.
- [ ] Xây dựng đủ **8 loại biểu đồ Plotly tương tác khác nhau**:
  1. *Choropleth Map:* Bản đồ nhiệt toàn cầu thể hiện lượt stream/đặc trưng âm học theo quốc gia.
  2. *Scatter Plot:* Tương quan giữa GDP và Lượt stream/Năng lượng âm thanh (kèm đường xu hướng).
  3. *Bar Chart (Đứng/Ngang):* Top bài hát, Top nghệ sĩ trụ hạng lâu nhất.
  4. *Line Chart:* Biến động đặc trưng âm nhạc theo chuỗi thời gian các tuần (2021 - 2022).
  5. *Heatmap:* Bản đồ nhiệt tương quan tương tác giữa các thuộc tính âm thanh.
  6. *Pie / Donut Chart:* Tỷ lệ thị phần nghe nhạc theo Nhóm thu nhập (`income_group`).
  7. *Box Plot / Violin Plot:* So sánh phân phối độ vui vẻ (`valence`) giữa các khu vực địa lý.
  8. *Radar Chart:* Biểu đồ mạng nhện so sánh Audio Profile của bài hát với chuẩn Top Trending.
- [ ] Xây dựng tính năng tương tác chuyên sâu: Bộ lọc phân cấp liên hoàn (Cascading filter), Hover Tooltip chi tiết, tùy chọn nhóm chỉ số.
- [ ] Xây dựng trang **Storytelling (Câu chuyện dữ liệu)**: Khắc họa góc nhìn sâu sắc về thói quen nghe nhạc và mối tương quan kinh tế - xã hội.

### 3. Đỗ Thanh Thành Tài (Phụ trách: Mô hình dự báo, Video Demo & Báo cáo)
- [ ] Chuẩn bị tập dữ liệu huấn luyện (Train/Test split 80/20, chuẩn hóa StandardScaler).
- [ ] Huấn luyện mô hình **Hồi quy Logistic (Logistic Regression)** dự đoán khả năng bài hát lọt Top Trending (`is_trending`).
- [ ] Đánh giá toàn diện mô hình: Accuracy, Precision, Recall, F1-score, ROC-AUC curve và ma trận nhầm lẫn (Confusion Matrix).
- [ ] Trích xuất hệ số tác động (Feature Importance) xem đặc trưng âm học nào quyết định hit âm nhạc.
- [ ] Đóng gói mô hình (`models/trend_predictor.pkl`) và xây dựng module `src/models.py`.
- [ ] Lập trình trang **"Dự báo thịnh hành"** trên Dashboard: Tích hợp bảng điều khiển tương tác (nhập thông số âm thanh $\rightarrow$ hiển thị xác suất lọt Top Hit dạng Gauge Chart/Phân lớp rủi ro).
- [ ] Soạn thảo Báo cáo khoa học hoàn chỉnh (`docs/final_report.docx`):
  - Định dạng chuẩn bài báo khoa học, trích dẫn tài liệu chuẩn IEEE.
  - Viết phần giải thích cơ sở logic lựa chọn biểu đồ và đoạn mã giả (pseudo-code) của pipeline.
- [ ] Xây dựng kịch bản thuyết trình và quay **Video Demo hoàn chỉnh**:
  - Đóng vai Data Analyst trình bày báo cáo trực quan trước ban lãnh đạo/khách hàng.
  - Trình diễn mượt mà các thao tác lọc dữ liệu, drill-down và chạy thử nghiệm mô hình dự báo.

---

## IV. CẤU TRÚC BÁO CÁO CUỐI KỲ BẮT BUỘC (7 MỤC CHUẨN KHOA HỌC)

Theo yêu cầu chuẩn học thuật trong Rubric, tài liệu báo cáo của nhóm (`docs/final_report.docx`) bắt buộc tuân theo cấu trúc 7 phần sau:

1. **Mục 1: Xác định bài toán & Dataset**
   - Trình bày rõ bối cảnh, lý do chọn đề tài và mục tiêu phân tích.
   - Giới thiệu các tập dữ liệu sử dụng ($\ge 5,000$ dòng, $\ge 3$ bảng - đồ án dùng 5 bảng với $>300,000$ dòng).
   - Đính kèm đường dẫn và trích lục Từ điển dữ liệu chi tiết (`docs/data_dictionary.md`).
2. **Mục 2: Làm sạch dữ liệu (Data Cleaning & Code)**
   - Mô tả thuật toán và minh họa code Python xử lý triệt để Missing values, Outliers.
   - Chuẩn hóa định dạng ngày tháng (`week`), chuỗi ký tự (`track_name`, `country`).
3. **Mục 3: Biến đổi dữ liệu (Feature Engineering & Join Code)**
   - Sơ đồ hệ thống và giải thích thuật toán Join/Merge 5 bảng dữ liệu chính xác.
   - Định nghĩa và công thức của các trường dữ liệu tính toán mới có ý nghĩa (**Calculated fields**): `is_trending`, `mood_category`, `stream_share_country`,...
4. **Mục 4: Khám phá dữ liệu (EDA - Exploratory Data Analysis)**
   - Trình bày ít nhất 3 - 5 biểu đồ tĩnh (Seaborn/Matplotlib) phân tích phân phối dữ liệu trước khi đưa lên Dashboard.
   - Rút ra nhận định thống kê ban đầu về các đặc trưng âm học và xu hướng nghe nhạc.
5. **Mục 5: Mô hình dự báo (Predictive Modeling)**
   - Mô tả thuật toán Hồi quy tuyến tính (Linear) hoặc Hồi quy Logistic (Logistic Regression).
   - Diễn giải kết quả đánh giá mô hình: Accuracy, Precision, Recall, ROC-AUC, Feature Coefficients.
   - Giải thích cách tích hợp kết quả mô hình thành công cụ trực quan hóa tương tác trên Dashboard.
6. **Mục 6: Hướng dẫn cài đặt / sử dụng & Link Video Demo**
   - Hướng dẫn các bước cài đặt môi trường (`requirements.txt`) và lệnh chạy Dashboard (`streamlit run dashboard/app.py`).
   - **Bắt buộc có Link Video Demo tóm tắt (YouTube / Google Drive)** ghi lại quá trình vận hành trực tiếp.
7. **Mục 7: Kết luận & Tài liệu tham khảo**
   - Đúc kết các insight cốt lõi và giá trị ứng dụng thực tiễn của đề tài.
   - Danh mục tài liệu tham khảo được trích dẫn theo đúng chuẩn **IEEE**.
