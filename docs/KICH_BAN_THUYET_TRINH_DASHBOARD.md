# KỊCH BẢN THUYẾT TRÌNH CHI TIẾT: SPOTIFY AUDIO ATLAS
## HỆ THỐNG TRỰC QUAN HÓA VÀ KỂ CHUYỆN DỮ LIỆU TƯƠNG TÁC (INTERACTIVE DATA STORYTELLING)

* **Học phần:** Tương tác Dữ liệu Trực quan (Interactive Data Visualization / Visual Analytics)
* **Người thực hiện & Thuyết trình:** 
  * **Lý Gia Hân** (Lead Visualization Specialist & Data Analyst — Trình bày Story Point 1 đến 5)
  * **Đỗ Thanh Thành Tài** (Machine Learning Engineer & Modeler — Trình bày Story Point 6)
* **Đối tượng tiếp nhận:** Hội đồng Giám khảo / Ban Giám đốc & Đối tác Sản xuất Âm nhạc
* **Thời lượng dự kiến:** 8 – 10 phút (cho toàn bộ 6 Story Points tương tác)
* **Ứng dụng trình diễn:** Spotify Story Studio (`dashboard/story_app.py` chạy trên Streamlit cổng `8502` hoặc file độc lập `docs/spotify_data_story.html`)

---

## 📌 PHẦN CHUẨN BỊ TRƯỚC KHI BẮT ĐẦU (CHECKLIST KỸ THUẬT)

1. **Khởi chạy ứng dụng:** Mở terminal chạy lệnh `.\start_story.ps1` (hoặc `python -m streamlit run dashboard/story_app.py --server.port 8502`).
2. **Thiết lập hiển thị:** Truy cập `http://localhost:8502/`, bấm phím **F11** trên trình duyệt (hoặc nút **Toàn màn hình ⛶** trên thanh công cụ) để đưa về chế độ toàn màn hình không viền.
3. **Độ phân giải chuẩn:** Thiết kế tối ưu cho tỷ lệ 16:9 (1440 × 900 trở lên), bố cục chia lưới thích ứng, không cần cuộn trang (Fixed single-screen viewport).
4. **Kiểm tra trạng thái ban đầu:** 
   * Thanh điều hướng trên cùng hiển thị đủ **6 Story Points**.
   * Bắt đầu tại **Story Point 1: Cái nhìn về dữ liệu** (Dashboard tổng hợp 4 hình ảnh tĩnh từ EDA).
   * Phím tắt điều hướng nhanh: Dùng phím mũi tên `←` và `→` trên bàn phím để chuyển đổi giữa các Story Points mượt mà.

---

## 🕒 TỔNG QUAN PHÂN BỔ THỜI GIAN THUYẾT TRÌNH

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ [00:00 - 01:00]  PHẦN 1: Mở đầu, Bối cảnh Bài toán & Nền tảng Công nghệ                │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ [01:00 - 02:15]  PHẦN 2: Story 1 — Cái nhìn về Dữ liệu (Dẫn nhập EDA & Phân phối Nền) │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ [02:15 - 03:45]  PHẦN 3: Story 2 — Hồ sơ Âm thanh & Công thức Tạo Hit                  │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ [03:45 - 05:00]  PHẦN 4: Story 3 — Nghệ sĩ, Thể loại & Sức mạnh Hợp tác (Collab)       │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ [05:00 - 06:15]  PHẦN 5: Story 4 — Bản sắc Địa lý & ADN Âm nhạc Toàn cầu               │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ [06:15 - 07:30]  PHẦN 6: Story 5 — Chu kỳ Thời gian, Mùa vụ & Biến động Đại dịch       │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ [07:30 - 09:00]  PHẦN 7: Story 6 — Mô hình Máy học & Ngưỡng Quyết định Dự báo (τ)      │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ [09:00 - 10:00]  PHẦN 8: Tổng kết Khuyến nghị Chiến lược & Giải đáp Phản biện (Q&A)   │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🎬 KỊCH BẢN CHI TIẾT TỪNG STORY POINT

---

### PHẦN 1: MỞ ĐẦU, BỐI CẢNH VÀ NỀN TẢNG CÔNG NGHỆ (00:00 – 01:00)

| Thao tác trên màn hình (Hành động) | Lời thoại thuyết trình (Gia Hân) |
| :--- | :--- |
| • Đứng trước màn hình, giữ giao diện Story Point 1 ở trạng thái tổng quan.<br><br>• Ánh mắt bao quát hội đồng/khán giả, phong thái tự tin. | *"Kính thưa Quý Thầy Cô trong Hội đồng và các bạn! Em là **Lý Gia Hân**, đại diện nhóm thực hiện đề tài **Spotify Audio Trends & Predictive Analytics**.<br><br>Trong kỷ nguyên streaming số hóa, mỗi tuần có hơn 100.000 ca khúc mới đổ về Spotify. Đối với các nghệ sĩ và hãng thu âm (Record Labels), câu hỏi sống còn là: **Yếu tố nào thực sự định hình một ca khúc Hit, và làm sao để đưa ra quyết định đầu tư chính xác trước khi ra mắt sản phẩm?**<br><br>Để giải quyết trọn vẹn bài toán này, nhóm em đã xây dựng hệ thống **Spotify Audio Atlas** xử lý hơn 1,78 triệu lượt quan sát bảng xếp hạng tuần trên toàn cầu. Ứng dụng được thiết kế theo tư duy **Tableau Storytelling** trên nền tảng **Streamlit kết hợp Plotly**, với 6 chặng câu chuyện liên kết chặt chẽ từ khám phá dữ liệu mộc, phân tích hành vi người nghe, cho đến mô hình máy học dự báo tương lai. Em xin kính mời Hội đồng cùng bước vào câu chuyện dữ liệu!"* |

---

### PHẦN 2: STORY POINT 1 — CÁI NHÌN VỀ DỮ LIỆU (DẪN NHẬP EDA) (01:00 – 02:15)

| Thao tác trên màn hình (Hành động) | Lời thoại thuyết trình (Gia Hân) |
| :--- | :--- |
| **Bước 1: Giới thiệu 4 góc nhìn EDA mộc**<br>• Trỏ chuột lướt qua 4 góc màn hình: Phân phối âm thanh (trên trái), Ma trận tương quan (trên phải), Xu hướng Global (dưới trái), Phân phối nhãn Train (dưới phải). | *"Chặng đầu tiên: **Cái nhìn về Dữ liệu**. Trước khi bước vào các bảng tương tác phức tạp, nguyên tắc cốt lõi của Visual Analytics là phải thấu hiểu bản chất phân phối của dữ liệu mộc.<br><br>Trên một màn hình duy nhất, nhóm em đồng bộ 4 biểu đồ nền tảng trích xuất trực tiếp từ quá trình EDA thực chứng trên 39.190 ca khúc độc nhất."* |
| **Bước 2: Phóng to hình phân phối âm thanh**<br>• Bấm nút **'Xem lớn'** ở ô trên bên trái.<br>• Chỉ vào phân phối của *Speechiness* và *Duration*.<br>• Bấm nút **'Đóng'** modal. | *"Khi bấm **Xem lớn** biểu đồ phân phối âm thanh, chúng ta nhận diện ngay hiện tượng lệch phải nghiêm trọng: Độ dài bài hát có đuôi kéo dài tới hơn 30 phút (các bản ghi podcast hoặc nhạc thiền), và tính hiện diện lời nói Speechiness phần lớn tập trung dưới 0,1. Do đó, việc sử dụng giá trị trung vị (Median) thay vì trung bình cộng là yêu cầu bắt buộc để không bị bóp méo bởi các giá trị ngoại lai."* |
| **Bước 3: Chỉ vào Ma trận tương quan & Nhãn Train**<br>• Chỉ vào ô tương quan $\rho = 0,763$ giữa Energy và Loudness.<br>• Chỉ sang biểu đồ phân phối nhãn Train ở góc dưới bên phải. | *"Ở biểu đồ tương quan góc trên bên phải, cặp biến **Energy và Loudness** có hệ số Spearman đạt tới **0,763** — phản ánh sự chồng lấn thông tin rất lớn: nhạc càng to thì cảm giác năng lượng càng mạnh.<br><br>Đặc biệt, nhìn vào góc dưới bên phải: **Tỷ lệ bài hát đạt Global Top 50 trong 8 tuần chỉ chiếm 22,8%** trên tập Train. Sự mất cân bằng nhãn này đòi hỏi bài toán dự báo ở các chặng sau không thể dùng thước đo Accuracy thông thường mà phải dựa trên F1-Score và Precision–Recall."* |

---

### PHẦN 3: STORY POINT 2 — HỒ SƠ ÂM THANH & CÔNG THỨC TẠO HIT (02:15 – 03:45)

| Thao tác trên màn hình (Hành động) | Lời thoại thuyết trình (Gia Hân) |
| :--- | :--- |
| **Bước 1: Chuyển sang Story Point 2**<br>• Bấm phím `→` hoặc click vào tab **'Hồ sơ âm thanh'**.<br>• Rê chuột vào hàng **Top 1–10** trên Heatmap Z-Score. | *"Chuyển sang chặng thứ hai: **Giải mã Công thức tạo Hit**. Nhìn vào Biểu đồ nhiệt ở bên trái, nhóm em sử dụng kỹ thuật chuẩn hóa z-score để đo mức độ lệch chuẩn của từng nhóm thứ hạng so với mức trung bình của toàn bảng xếp hạng.<br><br>Nhóm **Top 1–10** rực sáng với sắc đỏ dương tính ở các đặc trưng: Độ dễ nhảy (Danceability z = +0,13), Cường độ năng lượng (Energy z = +0,10) và Nhịp độ (Tempo). Ngược lại, tính mộc (Acousticness) và tính khí nhạc không lời (Instrumentalness) lao dốc xuống sắc xanh âm tính sâu.<br><br>Đặc biệt, chỉ số âm lượng (Loudness) tiệm cận mức 0 trên mọi phân tầng — đập tan quan niệm sai lầm rằng 'phải nén âm thanh thật to mới lên top'. Người nghe chọn bài vì giai điệu dễ bắt nhịp chứ không phải vì âm lượng lớn."* |
| **Bước 2: Chuyển đổi Boxplot thể loại**<br>• Bấm chọn dropdown trên biểu đồ hộp từ *Energy* sang *Valence* (Sắc thái tích cực).<br>• Chỉ vào vị trí phân vị của Latin vs. Pop/Rap. | *"Khi khảo sát sự phân hóa thể loại qua biểu đồ hộp bên phải: Thể loại **Latin** áp đảo tuyệt đối về độ tươi vui, sắc thái tích cực với trung vị Valence đạt tới 0,67 — vượt xa Pop (0,51) và Rap (0,46).<br><br>Điều này mang lại khuyến nghị định vị sản phẩm rất rõ nét: Các tác phẩm Pop hay Rap thành công nhờ chiều sâu cảm xúc tự sự và nhịp điệu bắt tai, trong khi dòng nhạc Latin là 'vua' của sự hưng phấn và tiệc tùng."* |

---

### PHẦN 4: STORY POINT 3 — NGHỆ SĨ, THỂ LOẠI & SỨC MẠNH HỢP TÁC (03:45 – 05:00)

| Thao tác trên màn hình (Hành động) | Lời thoại thuyết trình (Gia Hân) |
| :--- | :--- |
| **Bước 1: Chuyển sang Story Point 3**<br>• Bấm tab **'Nghệ sĩ & hợp tác'**.<br>• Chỉ vào Treemap 80 nghệ sĩ dẫn đầu ở góc trên bên phải. | *"Chặng thứ ba đưa chúng ta đến câu hỏi chiến lược: **Tên tuổi nghệ sĩ và việc hợp tác (Collab) đóng vai trò như thế nào trong thành công thương mại?**<br><br>Quan sát Treemap ở góc phải, diện tích ô tỷ lệ thuận với số lượt stream ghi nhận. Chúng ta thấy rõ sự thống trị áp đảo của các 'siêu sao' dòng Pop và Latin như Bad Bunny, Drake, Taylor Swift và The Weeknd."* |
| **Bước 2: Khám phá Ma trận tương quan nghệ sĩ**<br>• Rê chuột vào ô tương quan giữa *Tên tuổi nghệ sĩ (Prior Streams/Hits)* và *Lượt nghe 8 tuần đầu* trên biểu đồ bên trái. | *"Biểu đồ ma trận bên trái chỉ ra mối tương quan Spearman đạt tới **$\rho = 0,58$** giữa thành tích tích lũy trong quá khứ của nghệ sĩ và lượt stream 8 tuần đầu của bài hát mới. Điều này chứng minh 'hiệu ứng hào quang' (Halo Effect): Tên tuổi nghệ sĩ chính là chiếc vé bảo chứng mạnh mẽ nhất giúp bài hát có đà bật ban đầu."* |
| **Bước 3: Đối chiếu Solo vs. Collab**<br>• Bấm vào biểu đồ Donut & Bar chart ở góc dưới bên phải.<br>• Đổi dropdown sang 'Phân phối chi tiết' để xem boxplot. | *"Vậy với các nghệ sĩ mới chưa có tên tuổi lớn, đâu là giải pháp?<br><br>Câu trả lời nằm ở biểu đồ **Solo vs. Collab**: Mặc dù các ca khúc đơn ca (Solo) chiếm tới gần 60% số lượng phát hành, nhưng các sản phẩm **hợp tác (Collab) lại đạt mức trung vị lượt stream cao hơn hẳn**. Hợp tác âm nhạc chính là chiếc đòn bẩy thông minh nhất giúp cộng hưởng tệp người hâm mộ chéo giữa các nghệ sĩ."* |

---

### PHẦN 5: STORY POINT 4 — BẢN SẮC ĐỊA LÝ & ADN ÂM NHẠC TOÀN CẦU (05:00 – 06:15)

| Thao tác trên màn hình (Hành động) | Lời thoại thuyết trình (Gia Hân) |
| :--- | :--- |
| **Bước 1: Chuyển sang Story Point 4**<br>• Bấm tab **'Bản sắc địa lý và ADN âm nhạc'**.<br>• Chọn dropdown chỉ số bản đồ là *Valence*. | *"Chặng thứ tư: **Bản sắc Địa lý**. Khi một nghệ sĩ muốn đưa tác phẩm vươn ra thị trường quốc tế, liệu một công thức âm thanh duy nhất có thể chinh phục mọi quốc gia hay không?<br><br>Quan sát Bản đồ thế giới Choropleth bên trái: Khu vực Mỹ Latinh và Caribe rực sáng với sắc đỏ rực rỡ — minh chứng cho thị trường tiêu thụ âm nhạc sôi động, giàu năng lượng và tích cực nhất hành tinh."* |
| **Bước 2: Trực quan hóa đối kháng trên Radar Chart**<br>• Bấm chọn **Việt Nam (VNM)** trên bản đồ (hiển thị đường màu xanh).<br>• Chọn so sánh với **Nhật Bản (JPN)** (hiển thị đường màu hồng). | *"Để thấy sự khác biệt văn hóa, em xin mời Hội đồng nhìn vào màn so sánh trực diện giữa hai thị trường lớn của Châu Á: **Việt Nam** và **Nhật Bản** trên biểu đồ Radar 6 trục bên phải.<br><br>Hai quốc gia đại diện cho hai bản sắc âm học đối lập nhau 180 độ:
- Khán giả **Việt Nam** ưu tiên tuyệt đối các giai điệu nhẹ nhàng, trữ tình (V-Pop Ballad): tính mộc Acousticness đạt tới 0,47 và năng lượng Energy chỉ ở mức 0,53.
- Ngược lại, **Nhật Bản** là đế chế của J-Pop, J-Rock và Anime Music: năng lượng Energy vọt lên tới 0,73, nhịp độ rất nhanh nhưng tính mộc chỉ chiếm 0,17.<br><br>Ý nghĩa ứng dụng: Một bản ballad êm dịu thành công tại Việt Nam nếu mang nguyên bản sang Nhật Bản sẽ rất khó cạnh tranh nếu không được phối khí lại để gia tăng tiết tấu và năng lượng."* |

---

### PHẦN 6: STORY POINT 5 — CHU KỲ THỜI GIAN, MÙA VỤ & ĐẠI DỊCH (06:15 – 07:30)

| Thao tác trên màn hình (Hành động) | Lời thoại thuyết trình (Gia Hân) |
| :--- | :--- |
| **Bước 1: Chuyển sang Story Point 5**<br>• Bấm tab **'Chu kỳ thời gian và đại dịch'**.<br>• Chỉ vào biểu đồ đường thời lượng ở trên cùng. | *"Chặng thứ năm phân tích yếu tố thời gian: **Nên phát hành bài hát vào thời điểm nào, và biến cố lịch sử tác động ra sao đến thói quen nghe nhạc?**<br><br>Nhìn vào biểu đồ đường trên cùng: Thời lượng trung bình của bài hát trên Global Top 200 đã **rút ngắn từ 218 giây (năm 2017) xuống còn 198 giây (năm 2022)** — giảm tới 20 giây. Đây là phản ứng thích nghi trực tiếp trước làn sóng video ngắn TikTok và thuật toán chi trả bản quyền sau 30 giây nghe của Spotify."* |
| **Bước 2: Khám phá Mùa vụ tháng 12**<br>• Chỉ vào cột tháng 12 trên biểu đồ chu kỳ tháng.<br>• Bấm vào thanh tháng 12 để lọc dữ liệu. | *"Về tính mùa vụ: Nhạc nhảy Danceability duy trì ổn định từ tháng 1 đến tháng 11 quanh mức 0,70. Nhưng cứ đến **tháng 12 hàng năm**, tính mộc Acousticness lại tăng vọt lên đỉnh điểm.<br><br>Lý do là bảng xếp hạng tháng 12 bị độc chiếm bởi làn sóng ca khúc Giáng sinh kinh điển (như của Mariah Carey hay Wham!). Bài học rút ra: Các nghệ sĩ trẻ nên tránh phát hành bài hát mới vào tháng 12 để không phải cạnh tranh với thói quen hoài niệm lễ hội."* |
| **Bước 3: Phân tích đồng biến động COVID-19**<br>• Rê chuột qua biểu đồ kết hợp chuỗi tử vong COVID-19 và đường âm thanh bên dưới. | *"Đặc biệt, khi đối chiếu âm nhạc với làn sóng tử vong đại dịch COVID-19 (2020–2022), dữ liệu cho thấy một nghịch lý tâm lý học sâu sắc: **Âm nhạc trở nên êm dịu hơn nhưng không bi quan hơn**.<br><br>Trong các đỉnh dịch, Acousticness tăng cao, Energy giảm sâu, nhưng chỉ số cảm xúc Valence vẫn kiên định đi ngang trên mốc 0,50. Âm nhạc đóng vai trò như một liều thuốc chữa lành: người nghe tìm đến sự mộc mạc để vỗ về tâm hồn chứ không muốn chìm vào u uất."* |

---

### PHẦN 7: STORY POINT 6 — MÔ HÌNH MÁY HỌC & NGƯỠNG QUYẾT ĐỊNH DỰ BÁO (07:30 – 09:00)

| Thao tác trên màn hình (Hành động) | Lời thoại thuyết trình (Thành Tài) |
| :--- | :--- |
| **Bước 1: Chuyển sang Story Point 6**<br>• Bấm phím `→` hoặc tab **'Mô hình & Ngưỡng dự báo'**.<br>• Nhường mic cho bạn **Đỗ Thanh Thành Tài**. | *(Gia Hân chuyển giao)*: *"Và sau khi đã thấu hiểu quá khứ, câu hỏi cuối cùng của nhà sản xuất là: **Liệu bài hát của tôi có thể trở thành Hit trong tương lai?** Em xin nhường phần trình bày Story Point 6 cho bạn **Đỗ Thanh Thành Tài**!"*<br><br>*(Thành Tài tiếp nhận)*: *"Kính thưa Hội đồng, tại Story Point 6, chúng em đưa mô hình Machine Learning trực tiếp lên Dashboard để hỗ trợ ra quyết định kinh doanh theo thời gian thực.<br><br>Mô hình Hồi quy Logistic được huấn luyện trên 12 biến đo lường ở tuần đầu phát hành (10 biến âm học + thứ hạng + log stream) để dự báo khả năng bài hát lọt vào **Global Top 50 trong vòng 8 tuần tiếp theo**."* |
| **Bước 2: Phân tích Hệ số Hồi quy (Odds Ratio)**<br>• Chỉ vào biểu đồ thanh Odds Ratio ở góc dưới bên phải.<br>• Rê chuột vào biến *Log streams* và *Danceability*. | *"Nhìn vào biểu đồ Hệ số Hồi quy ở góc dưới bên phải: Hai biến có trọng số chi phối mạnh nhất chính là **Log streams tuần đầu (Odds Ratio = 1,84)** và **Thứ hạng tuần đầu**.<br><br>Trong các biến âm học, **Danceability (Độ dễ nhảy)** là yếu tố thúc đẩy tích cực mạnh nhất với Odds Ratio = 1,18 (mỗi độ lệch chuẩn tăng thêm giúp cơ hội thành hit tăng 18%), tiếp theo là Valence và Loudness. Ngược lại, Energy và Acousticness có hệ số âm nhẹ, phản ánh xu hướng chuộng nhạc êm và bắt tai hơn là quá dồn dập."* |
| **Bước 3: Tương tác kéo thanh trượt Ngưỡng Quyết định $\tau$**<br>• Kéo thanh trượt **$\tau$** từ `0.79` xuống `0.50`, rồi nâng lên `0.85`.<br>• Quan sát Ma trận nhầm lẫn (Confusion Matrix) và Không gian quyết định 2D cập nhật tức thì. | *"Điểm đột phá của Dashboard này là **sự tương tác với Ngưỡng quyết định $\tau$**:<br><br>
1. Tại ngưỡng tối ưu **$\tau = 0,79$** (chọn trên Validation để tối đa hóa F1-Score), trên tập Test độc lập (941 bài năm 2021–2022), mô hình đạt **Precision = 65,6%**, **Recall = 59,8%** và **F1 = 62,6%** (với ROC-AUC đạt 0,811).<br>
2. Nếu hãng đĩa muốn **chiến lược an toàn (tránh đầu tư lãng phí)**: Họ tăng $\tau$ lên 0,85, Precision tăng vọt lên trên 75% — chỉ rót vốn cho những bài có độ chắc chắn cao nhất.<br>
3. Nếu muốn **săn tìm tài năng (không bỏ sót bất kỳ viên ngọc thô nào)**: Họ hạ $\tau$ xuống 0,50, Recall tăng mạnh giúp bắt trọn hầu hết các ca khúc có tiềm năng hit."* |
| **Bước 4: Cảnh báo học thuật và tính minh bạch**<br>• Chỉ vào khung lưu ý bên thanh Inspector. | *"Đặc biệt, nhóm em giữ thái độ trung thực học thuật tuyệt đối: Đối với các bài khởi đầu ngoài Top 50 (hạng 51–200), tỷ lệ vươn lên Top 50 thực tế chỉ có 1,5%. Mô hình thẳng thắn cảnh báo nguy cơ Dương tính giả (False Positive) nếu điểm xuất phát ban đầu quá thấp, giúp các nhà đầu tư không ảo tưởng vào các chỉ số âm thanh đơn thuần mà bỏ qua đòn bẩy truyền thông."* |

---

### PHẦN 8: TỔNG KẾT, KHUYẾN NGHỊ & KẾT THÚC (09:00 – 10:00)

| Thao tác trên màn hình (Hành động) | Lời thoại thuyết trình (Gia Hân & Thành Tài) |
| :--- | :--- |
| • Hai bạn đứng cạnh nhau trước màn hình.<br><br>• Đưa giao diện về trạng thái tổng kết, sẵn sàng cho phiên vấn đáp Q&A. | *(Gia Hân tổng kết)*: *"Kính thưa Thầy Cô, qua 6 Story Points liên hoàn, hệ thống **Spotify Audio Atlas** đã hiện thực hóa trọn vẹn mục tiêu của học phần Trực quan hóa Dữ liệu Tương tác:
1. **Mô tả tường minh:** Làm sáng tỏ cấu trúc phân phối và tương quan của dữ liệu âm nhạc toàn cầu.
2. **Kể chuyện hấp dẫn:** Đưa người xem đi qua hành trình từ bài hát, nghệ sĩ, biên giới địa lý đến biến cố lịch sử.
3. **Dự báo hành động:** Tích hợp mô hình máy học với khả năng tùy biến ngưỡng quyết định theo khẩu vị rủi ro kinh doanh.<br><br>Chúng em xin chân thành cảm ơn Quý Thầy Cô trong Hội đồng đã chú ý lắng nghe, và nhóm em rất mong nhận được những góp ý quý báu!"* |

---

## 💡 BỘ CÂU HỎI VẤN ĐÁP DỰ PHÒNG (Q&A) CHUYÊN SÂU

### Câu hỏi 1: Tại sao hệ thống lại dùng giao diện Fixed-Viewport (không cuộn trang) kiểu Tableau Story thay vì giao diện cuộn dài (Scrollable Dashboard)?
* **Trả lời (Gia Hân):**  
  *"Dạ thưa Thầy Cô, giao diện cuộn dài (Vertical Scrolling) thường khiến người xem bị quá tải thông tin (Cognitive Overload) và dễ mất ngữ cảnh khi cuộn qua lại giữa các biểu đồ. Nhóm em áp dụng triết lý **Visual Information-Seeking Mantra** của Ben Shneiderman: 'Overview first, zoom and filter, then details-on-demand'. Thiết kế 1 màn hình cố định kết hợp phân chia 6 Story Point giúp người dùng tập trung 100% vào một chủ đề duy nhất tại mỗi thời điểm, các biểu đồ tự động tương tác và lọc chéo với nhau mà không làm phân tán sự chú ý."*

### Câu hỏi 2: Tại sao ở Story 1 lại sử dụng cả hình ảnh tĩnh từ EDA thay vì vẽ lại hoàn toàn bằng Plotly tương tác?
* **Trả lời (Gia Hân):**  
  *"Dạ, việc đưa 4 biểu đồ tĩnh Matplotlib/Seaborn gốc từ notebook vào Story Point 1 mang 2 mục đích học thuật quan trọng:  
  1. **Tính trung thực và nguyên bản:** Giữ nguyên các đường tham chiếu thống kê phức tạp (đường phân vị, đường mật độ KDE và chú thích chuyên sâu) đã được kiểm định chặt chẽ trong notebook phân tích EDA.  
  2. **Hiệu năng hệ thống:** Việc render biểu đồ tĩnh dạng PNG nhúng trực tiếp giúp trang mở đầu tải ngay lập tức trong 0,1 giây, đồng thời cung cấp tính năng 'Xem lớn' và tải file PNG gốc phục vụ cho việc trích xuất báo cáo."*

### Câu hỏi 3: Ngưỡng tối ưu $\tau = 0,79$ ở Story 6 được xác định như thế nào, và tại sao không dùng ngưỡng mặc định 0,5?
* **Trả lời (Thành Tài):**  
  *"Dạ thưa Thầy Cô, bài toán dự đoán Hit có tỷ lệ nhãn dương nền chỉ khoảng 22,8% (mất cân bằng nhãn). Nếu dùng ngưỡng mặc định 0,5, mô hình sẽ gặp rất nhiều Dương tính giả (False Positives), dẫn đến việc đầu tư sai lầm cho các bài hát không có tiềm năng.  
  Nhóm em đã quét đường cong ngưỡng trên tập **Validation độc lập** (giai đoạn 2020–2021) với bước nhảy 0,01 và xác định ngưỡng $\tau = 0,79$ là điểm cân bằng tối ưu hóa chỉ số F1-Score ($F_1 = 66,2\%$ trên Validation). Sau đó, ngưỡng này được khóa cố định và đem kiểm định độc lập trên tập **Test** (2021–2022) đạt F1 = 62,6%, khẳng định mô hình không bị quá khớp (overfitting)."*

### Câu hỏi 4: Có hiện tượng rò rỉ dữ liệu (Data Leakage) khi tính toán các biến âm thanh và lượt nghe không?
* **Trả lời (Thành Tài):**  
  *"Dạ hoàn toàn không có rò rỉ dữ liệu. Nhóm em đã áp dụng quy tắc phòng chống rò rỉ nghiêm ngặt:  
  1. **Tách biệt thời gian (Temporal Split):** Chia dữ liệu Train (2017–2020), Validation (2020–2021) và Test (2021–2022) theo dòng thời gian thực tế, kèm vùng đệm an toàn 8 tuần giữa các tập để loại trừ việc một bài hát vắt qua hai giai đoạn.  
  2. **Chỉ dùng thông tin tuần đầu:** Toàn bộ 12 biến dự báo chỉ được trích xuất tại đúng tuần đầu tiên bài hát xuất hiện ($t_0$), tuyệt đối không sử dụng bất kỳ dữ liệu tích lũy nào trong tương lai của 8 tuần tiếp theo."*
