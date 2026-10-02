# BẢNG PHÂN CHIA NHIỆM VỤ THEO BAREM (PROJECT CUỐI KỲ)

**Môn học:** Tương tác dữ liệu trực quan (Interactive Data Visualization / Visual Analytics)
**Đề tài:** Nghiên cứu và trực quan hóa các đặc trưng âm thanh và tương quan với các vấn đề xã hội. Phân tích dự đoán xu hướng bài hát thịnh hành trên Spotify
**Quy mô nhóm:** 03 thành viên

> Bảng dưới đây liệt kê đầy đủ các tiêu chí chấm điểm theo Rubric (barem 10 điểm) của đồ án.

---

## I. THÔNG TIN THÀNH VIÊN

| STT | Họ và tên | MSSV | Vai trò chính |
| :---: | :--- | :---: | :--- |
| 1 | Đinh Quốc Anh | 24133003 | Data Engineer & Data Analyst |
| 2 | Lý Gia Hân | 24133016 | Visualization Specialist & Dashboard Dev |
| 3 | Đỗ Thanh Thành Tài | 24133050 | ML Engineer & Demo/Reporting Lead |

---

## II. MA TRẬN PHÂN CÔNG THEO BAREM (10 ĐIỂM)

| Phần theo Rubric | Điểm | Tiêu chí chi tiết theo Barem |
| :--- | :---: | :--- |
| **1. Thu thập & Tiền xử lý dữ liệu** | **2.5đ** | • **Xác định bài toán & Dataset (0.5đ):** Mục tiêu rõ ràng, dữ liệu ≥ 5,000 dòng, ≥ 3 bảng, nêu rõ nguồn & Data Dictionary.<br>• **Làm sạch dữ liệu (0.5đ):** Code Python xử lý triệt để Missing values, Outliers, chuẩn hóa ngày tháng/chuỗi.<br>• **Biến đổi dữ liệu (0.75đ):** Join/Merge các bảng chính xác, tạo trường tính toán mới (Calculated fields).<br>• **Khám phá dữ liệu EDA (0.75đ):** Dùng Matplotlib/Seaborn vẽ ít nhất 3 - 5 biểu đồ tĩnh phân tích phân phối trước khi đưa lên Dashboard. |
| **2. Thiết kế Dashboard (Trọng tâm)** | **3.5đ** | • **Giao diện & UI/UX (0.5đ):** Layout hợp lý, màu sắc hài hòa, Legend rõ ràng.<br>• **Đa dạng biểu đồ (1.0đ):** Sử dụng ≥ 8 loại biểu đồ khác nhau (Bar, Line, Pie, Scatter, Heatmap, Treemap, Radar, Boxplot...).<br>• **Bản đồ không gian (0.5đ):** Ít nhất 1 biểu đồ dạng Geographic Map.<br>• **Tính tương tác (1.5đ):** Bộ lọc đa cấp (Filters), Drill-down, Tooltip khi hover, Cross-filtering. |
| **3. Phân tích Insight & Dự báo** | **2.0đ** | • **Khai phá Insight (1.0đ):** Rút ra câu chuyện dữ liệu (Storytelling), phân tích nguyên nhân và xu hướng.<br>• **Mô hình Dự báo (0.5đ):** Áp dụng đúng thuật toán Hồi quy tuyến tính hoặc Logistic.<br>• **Trực quan Dự báo (0.5đ):** Tích hợp kết quả dự báo lên biểu đồ trực quan trong Dashboard. |
| **4. Báo cáo & Demo ứng dụng** | **2.0đ** | • **Báo cáo khoa học (1.0đ):** Cấu trúc chuẩn, sơ đồ Pipeline hệ thống, trích dẫn IEEE, giải thích logic chọn biểu đồ, minh họa code.<br>• **Ứng dụng Demo (1.0đ):** Dashboard chạy mượt mà, kịch bản lôi cuốn, đóng vai Data Analyst thuyết trình với sếp/khách hàng. |
| **Tổng cộng** | **10.0đ** | Toàn bộ 4 phần theo Rubric |

---

## III. NGUYÊN TẮC PHỐI HỢP

- Mỗi thành viên chịu trách nhiệm **kết quả cuối cùng** của phần barem được giao, không bị ràng buộc cách làm cụ thể.
- Phần 3 và Phần 4 có tính liên đới giữa các thành viên — cần thống nhất giao diện dữ liệu đầu vào/đầu ra (VD: định dạng file model, tên cột) trước khi từng người triển khai độc lập.
- Deadline nội bộ và cách chia nhỏ công việc trong phạm vi mỗi phần do người phụ trách phần đó tự sắp xếp.
- Nếu phát sinh thay đổi phạm vi dữ liệu/hướng đề tài ảnh hưởng đến phần của người khác (VD: đổi định nghĩa `is_hit`, đổi cấu trúc bảng `tracks_master`), cần thông báo trong nhóm trước khi triển khai.
