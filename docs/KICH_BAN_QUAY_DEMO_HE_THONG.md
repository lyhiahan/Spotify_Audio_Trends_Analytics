# KỊCH BẢN QUAY VIDEO DEMO HỆ THỐNG
# SPOTIFY AUDIO ATLAS & TRENDS ANALYTICS
## Hệ thống Phân tích Đặc trưng Âm thanh, Network Science & Storytelling Trực quan Tương tác

---

* **Học phần:** Tương tác Dữ liệu Trực quan (Interactive Data Visualization / Visual Analytics)
* **Nhóm thực hiện:** Nhóm 04 (Lý Gia Hân, Đinh Quốc Anh, Đỗ Thanh Thành Tài)
* **Thời lượng video dự kiến:** **8 – 10 phút**
* **Trọng tâm video:** 
  1. **Dashboard chính:** Story Studio (`dashboard/story_app.py` chạy cổng 8502) — Visual Storytelling 5 Story Points.
  2. **Biểu đồ EDA chuyên sâu & Network Science (Đinh Quốc Anh):** Trang `dashboard/pages/2_🎵_Dac_Trung_Am_Thanh.py` & notebook `02_eda.ipynb` (Treemap, Radar Profile, Mạng lưới quan hệ quốc gia, Hit Simulator).
  3. **Giao diện Bento Grid thị trường (Lý Gia Hân):** Trang `dashboard/pages/1_📊_Tong_Quan_Du_Lieu.py` (Player Card, Track Drawer, 4 Thẻ KPI).
  4. **Mô hình hóa dự báo Hit (Đỗ Thanh Thành Tài):** Logistic Regression kháng rò rỉ dữ liệu (AUC = 0.811, ngưỡng tối ưu F1 $\tau = 0.79$).

---

## 🛠️ CHECKLIST KỸ THUẬT TRƯỚC KHI BẤM QUAY (PRE-RECORDING)

1. **Chuẩn bị môi trường phần mềm:**
   - Mở sẵn 2 Terminal:
     - **Terminal 1:** Chạy Story Studio chính: `streamlit run dashboard/story_app.py --server.port 8502`
     - **Terminal 2:** Chạy các trang phân tích chi tiết: `streamlit run dashboard/pages/2_🎵_Dac_Trung_Am_Thanh.py --server.port 8501`
   - Mở sẵn trình duyệt (Chrome/Edge) với 2 tab:
     - **Tab 1:** `http://localhost:8502` (Story Studio chính)
     - **Tab 2:** `http://localhost:8501` (Trang Đặc trưng Âm thanh & Network Science của Quốc Anh)
     - *(Tùy chọn) Tab 3:* Trang `1_📊_Tong_Quan_Du_Lieu.py`
2. **Cài đặt hiển thị & Âm thanh:**
   - Đưa trình duyệt về chế độ **F11 (Toàn màn hình)** để ẩn thanh URL, tối ưu tỷ lệ khung hình 16:9.
   - Ẩn con trỏ chuột khi không chuyển động hoặc bật hiệu ứng vòng sáng chuột (Mouse Highlight) trong phần mềm quay để người xem dễ theo dõi.
   - Kiểm tra Micro: Thu âm rõ ràng, bật chống ồn (Noise Suppression).
3. **Quy tắc di chuyển chuột khi quay:**
   - **Không lia chuột loạn xạ:** Di chuột từ từ, dứt khoát đến đúng nút/biểu đồ cần giải thích.
   - **Nguyên tắc "Dừng 2 giây":** Khi rê chuột (hover) vào tooltip hoặc click vào một điểm, dừng chuột lại 2 giây để người xem đọc được dữ liệu tooltip trước khi nói tiếp.

---

## ⏱️ TỔNG QUAN TIMELINE VIDEO DEMO (8 – 10 PHÚT)

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ [00:00 - 01:00]  PHẦN 0: Mở đầu, Bối cảnh nghiên cứu & Quy mô bộ dữ liệu Big Data     │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ [01:00 - 03:30]  PHẦN 1: EDA Chuyên sâu, Network Science & Hit Simulator (QUỐC ANH)   │
│                  • Treemap thị phần & Năng lượng âm học Top 40 nghệ sĩ                │
│                  • Linked Views: Radar Profile nghệ sĩ vs Top 50 Trending & Scatter    │
│                  • Đồ thị mạng lưới đồng xuất hiện quốc gia (NetworkX Modularity)     │
│                  • Bộ giả lập dự báo Hit thời gian thực (Logistic Regression)         │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ [03:30 - 04:30]  PHẦN 2: Bento Grid Tổng quan Thị trường Âm nhạc (GIA HÂN)            │
│                  • Track Drawer & Now Playing Card tương tác phong cách Spotify        │
│                  • 4 Thẻ KPI động theo vùng địa lý và thể loại                         │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ [04:30 - 08:15]  PHẦN 3: STORY STUDIO — DASHBOARD CHÍNH (STORYTELLING 5 TRỤ CỘT)      │
│                  • Point 1: Công thức tạo Hit (Heatmap z-score, Boxplot, Solo/Collab) │
│                  • Point 2: Tên tuổi nghệ sĩ & Tương quan Spearman lượt nghe 8 tuần   │
│                  • Point 3: Bản sắc địa lý (Choropleth Map, Radar Việt Nam vs Nhật)   │
│                  • Point 4: Mùa vụ Giáng sinh & Biến động đại dịch COVID-19           │
│                  • Point 5: Không gian quyết định Machine Learning & Ngưỡng tau       │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ [08:15 - 09:30]  PHẦN 4: Ý nghĩa thực tiễn, Khuyến nghị ngành nhạc & Lời kết          │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🎬 KỊCH BẢN CHI TIẾT TỪNG PHÂN ĐOẠN

---

### PHẦN 0: MỞ ĐẦU, BỐI CẢNH & NỀN TẢNG DỮ LIỆU (00:00 – 01:00)

* **Màn hình hiển thị:** Tab 1 — `http://localhost:8502` (Giao diện Story Studio mở ở Story Point 1, chế độ Fullscreen F11).

| Mốc thời gian | Thao tác trên màn hình | Lời thoại thuyết minh (Voiceover Script) | Thông điệp dữ liệu cốt lõi |
| :--- | :--- | :--- | :--- |
| **00:00 – 00:30** | • Giữ chuột ở góc màn hình, để khán giả chiêm ngưỡng bố cục thiết kế Story Studio.<br>• Rê nhẹ chuột qua logo và thanh tiêu đề `Spotify Audio Trends & Analytics`. | *"Xin chào Thầy Cô và các bạn! Chào mừng mọi người đến với video demo hệ thống **Spotify Audio Atlas & Trends Analytics** do nhóm 04 thực hiện.<br><br>Trong kỷ nguyên streaming, mỗi tuần có hàng chục nghìn bài hát ra mắt. Bài toán sống còn của nghệ sĩ và nhà sản xuất là: **Đặc trưng âm thanh nào thực sự quyết định một bài hát trở thành Hit? Văn hóa âm nhạc giữa các quốc gia khác nhau ra sao? Và làm thế nào để dự báo cơ hội lọt bảng xếp hạng ngay từ tuần đầu phát hành?**"* | Nêu bật bài toán kinh doanh và lý do nghiên cứu. |
| **00:30 – 01:00** | • Bật slide mở đầu hoặc chuyển lướt tab sang file README/kiến trúc dữ liệu.<br>• Sau đó chuyển ngay sang Tab 2 (`localhost:8501`) để bắt đầu phần EDA chuyên sâu. | *"Để trả lời câu hỏi đó, nhóm em đã thu thập và xử lý toàn diện hơn **1,9 triệu bản ghi bảng xếp hạng tuần toàn cầu**, kết hợp với kho dữ liệu âm học chuyên sâu của Spotify và chuỗi thời gian tử vong COVID-19.<br><br>Hệ thống được phát triển theo luồng hoàn chỉnh: Từ **EDA khám phá đặc trưng âm thanh & Network Science**, đến **Dashboard Bento Grid**, và đỉnh cao là **Story Studio tương tác 5 trụ cột**. Sau đây, em xin mời mọi người cùng bắt đầu từ tầng phân tích khám phá dữ liệu."* | Khẳng định quy mô Big Data (>1.9M records) và tính hoàn chỉnh của đề tài. |

---

### PHẦN 1: EDA ĐẶC TRƯNG ÂM THANH, NETWORK SCIENCE & HIT SIMULATOR (01:00 – 03:30)
> *Phụ trách bởi: **Đinh Quốc Anh** (Đóng góp chính trong `notebooks/02_eda.ipynb` & `dashboard/pages/2_🎵_Dac_Trung_Am_Thanh.py`)*

* **Màn hình hiển thị:** Tab 2 — `http://localhost:8501` (Trang Đặc trưng Âm thanh & Nghệ sĩ).

| Mốc thời gian | Thao tác trên màn hình | Lời thoại thuyết minh (Voiceover Script) | Thông điệp dữ liệu cốt lõi |
| :--- | :--- | :--- | :--- |
| **01:00 – 01:40** | **Góc nhìn 1: Hồ sơ âm thanh & Nghệ sĩ**<br>• Rê chuột vào **Treemap thị phần stream & Năng lượng âm học**.<br>• Hover vào một số ô lớn (ví dụ: Bad Bunny, The Weeknd, BTS).<br>• Bấm chọn nghệ sĩ **The Weeknd** hoặc **Bad Bunny** trực tiếp trên Treemap. | *"Đầu tiên là phân hệ Khám phá Đặc trưng Âm thanh do bạn **Đinh Quốc Anh** xây dựng.<br><br>Quan sát biểu đồ Treemap, diện tích thể hiện thị phần lượt stream, trong khi màu sắc thể hiện năng lượng (Energy) trung bình. Chúng ta thấy sự áp đảo của các siêu sao dòng nhạc Pop và Latin.<br><br>Khi em click chọn một nghệ sĩ cụ thể — ví dụ **Bad Bunny** — toàn bộ hệ thống Linked Views bên dưới sẽ lập tức được đồng bộ theo thời gian thực."* | Thao tác click trên Treemap kích hoạt Linked Views cập nhật đồng thời 3 thành phần bên dưới. |
| **01:40 – 02:15** | **Linked Views: Radar Profile & Scatter Highlight**<br>• Chỉ chuột vào biểu đồ Radar (Radar Profile).<br>• Rê chuột so sánh đường màu mận của nghệ sĩ với **đường nét đứt chuẩn Top 50 Trending**.<br>• Nhìn sang biểu đồ tán xạ (Scatter Highlight), chỉ vào các chấm nổi bật màu mận giữa nền xám. | *"Nhìn vào Biểu đồ Radar, chúng ta có thể so sánh 'dấu vân tay âm học' của nghệ sĩ với đường nét đứt — đại diện cho chuẩn Top 50 Trending toàn cầu. Ta thấy rõ Bad Bunny vượt trội hoàn toàn về độ dễ nhảy (Danceability) và năng lượng (Energy), nhưng tính mộc (Acousticness) lại ở mức rất thấp.<br><br>Bên cạnh đó, biểu đồ tán xạ Scatter Highlight làm sáng rõ các ca khúc của nghệ sĩ trên nền 1.200 bài hát đối chứng, cho thấy các bài hát của anh tập trung dày đặc ở góc phần tư có độ nhảy và năng lượng cao nhất."* | Chuẩn hóa đối chiếu (Benchmarking) hồ sơ âm học nghệ sĩ với chuẩn mực BXH thế giới. |
| **02:15 – 02:50** | **Góc nhìn 2: Mạng lưới đồng xuất hiện quốc gia**<br>• Bấm chuyển radio sang tab **'🌐 Mạng Lưới Đồng Xuất Hiện & Dự Báo Hit'**.<br>• Rê chuột qua các cụm màu trên đồ thị mạng lưới.<br>• Kéo slider 'Ngưỡng liên kết' từ 5 lên 8 để thấy mạng lưới lọc bớt cạnh nhiễu. | *"Chuyển sang góc nhìn thứ hai: **Mạng lưới khoa học (Network Science)**. Đây là một điểm đột phá trong phân tích EDA của nhóm.<br><br>Nhóm em sử dụng thuật toán Bipartite Graph để ánh xạ sự đồng xuất hiện của các nghệ sĩ trên các bảng xếp hạng quốc gia. Sử dụng thuật toán phân cụm Modularity, mạng lưới tự động bóc tách thành 5 cộng đồng âm nhạc rõ rệt: Cụm Pop Core toàn cầu, Cụm Latin Wave, Cụm Hip-Hop, và Cụm Asian Wave.<br><br>Khi tăng ngưỡng liên kết lên 8 quốc gia, ta thấy những nghệ sĩ như Drake, Ed Sheeran hay Dua Lipa đóng vai trò là các nút trung tâm (Hub Nodes) kết nối toàn bộ thị trường âm nhạc quốc tế."* | Ứng dụng Network Science & Community Detection để tìm ra các Hub nghệ sĩ thống trị toàn cầu. |
| **02:50 – 03:30** | **Bộ giả lập Machine Learning Hit Simulator**<br>• Cuộn nhẹ xuống mục **'2. Công Cụ Giả Lập Dự Báo Thịnh Hành'**.<br>• Kéo slider: Tăng *Danceability* lên 0.85, tăng *Energy* lên 0.75, giảm *Acousticness* về 0.10.<br>• Chỉ vào **Đồng hồ Gauge Chart** đang nhảy lên >75%.<br>• Rê chuột xuống biểu đồ thanh ngang **Feature Importance**. | *"Dưới đây là công cụ giả lập **Hit Simulator** dựa trên mô hình Logistic Regression.<br><br>Nhà sản xuất có thể điều chỉnh 7 thuộc tính âm thanh của một bản demo. Khi em tăng độ dễ nhảy lên 0.85 và giảm tính mộc xuống 0.10, đồng hồ đo xác suất lập tức tăng vọt lên mức hơn 75% khả năng lọt Top 50 Trending.<br><br>Biểu đồ thanh ngang hệ số hồi quy bên dưới giải thích rõ nguyên nhân: Danceability và Loudness đóng góp hệ số dương lớn nhất thúc đẩy bài hát thành hit, trong khi Acousticness mang hệ số âm kìm hãm cơ hội lọt BXH. Điều này hoàn toàn khớp với ma trận tương quan Spearman mà nhóm đã chứng minh trong notebook `02_eda.ipynb`."* | Cầu nối giữa phân tích tương quan EDA và công cụ hỗ trợ ra quyết định sản xuất âm nhạc. |

---

### PHẦN 2: BENTO GRID TỔNG QUAN THỊ TRƯỜNG ÂM NHẠC (03:30 – 04:30)
> *Phụ trách bởi: **Lý Gia Hân** (Đóng góp trong `dashboard/pages/1_📊_Tong_Quan_Du_Lieu.py`)*

* **Màn hình hiển thị:** Tab 3 hoặc chuyển URL sang trang `1_📊_Tong_Quan_Du_Lieu.py`.

| Mốc thời gian | Thao tác trên màn hình | Lời thoại thuyết minh (Voiceover Script) | Thông điệp dữ liệu cốt lõi |
| :--- | :--- | :--- | :--- |
| **03:30 – 04:00** | • Giới thiệu layout Bento Grid hiện đại.<br>• Bấm chọn dropdown 'Khu vực địa lý' chọn **Latin America & Caribbean**.<br>• Quan sát 4 thẻ KPI cập nhật tức thì. | *"Tiếp theo là Bảng điều khiển Tổng quan Thị trường do bạn **Lý Gia Hân** thiết kế theo ngôn ngữ **Bento Grid** hiện đại của Spotify Web Player.<br><br>Tại đây, người dùng có thể lọc toàn diện theo khu vực, thể loại và năm. Bốn thẻ KPI cung cấp ngay bức tranh tổng thể: số lượng bài hát, nghệ sĩ, thời lượng trung bình và độ phổ biến trung bình của từng thị trường."* | Thiết kế Bento Grid trực quan, trải nghiệm mượt mà, thông số KPI bao quát. |
| **04:00 – 04:30** | • Chỉ chuột vào **Track Drawer** bên trái.<br>• Chọn một bài hát thịnh hành trong danh sách dropdown (ví dụ: *Blinding Lights* hoặc *Despacito*).<br>• Chỉ vào **Player Card 'Now Playing'** ở giữa màn hình: quan sát 3 thanh progress bar (Danceability, Energy, Valence). | *"Một điểm nhấn trải nghiệm người dùng ở đây là **Widget Now Playing**. Khi chọn một bài hát từ danh sách Top ca khúc bên trái, thanh trình phát nhạc ảo sẽ lập tức phân tích và hiển thị trực quan cấu trúc âm thanh: tỷ lệ nhảy múa, năng lượng bùng nổ và cảm xúc tươi vui.<br><br>Đây là công cụ tuyệt vời giúp người quản lý âm nhạc có cái nhìn nhanh (quick glance) về bất kỳ bài hát nào trong kho dữ liệu."* | Tương tác dạng Widget nghe nhạc thực tế, tăng độ sinh động cho bài thuyết trình. |

---

### PHẦN 3: STORY STUDIO — DASHBOARD CHÍNH TƯƠNG TÁC 5 TRỤ CỘT (04:30 – 08:15)
> *Dashboard trung tâm của đề tài: `dashboard/story_app.py` (Cổng 8502)*

* **Màn hình hiển thị:** Chuyển về Tab 1 — `http://localhost:8502`, bấm **F11** toàn màn hình.

| Mốc thời gian | Thao tác trên màn hình | Lời thoại thuyết minh (Voiceover Script) | Thông điệp dữ liệu cốt lõi |
| :--- | :--- | :--- | :--- |
| **04:30 – 04:55** | • Giới thiệu thanh điều hướng Story Studio gồm 5 nút bấm chuẩn Tableau Story.<br>• Đang ở **Story Point 1: Hồ sơ âm thanh & Công thức tạo hit**. | *"Và bây giờ, chúng ta bước vào trung tâm của đề tài: **Story Studio** — Hệ thống Kể chuyện Dữ liệu Trực quan tương tác hoàn toàn trên một màn hình duy nhất (No-scroll canvas), được thiết kế chuẩn mực theo triết lý Data Storytelling của Tableau.<br><br>Câu chuyện được cấu trúc qua 5 chương logic chặt chẽ."* | Khung nhìn cố định (Fixed viewport), tính thẩm mỹ cao, liền mạch. |
| **04:55 – 05:40** | **Story 1: Công thức tạo Hit & Xu hướng Thời đại**<br>• Rê chuột vào hàng **Top 1–10** trên Heatmap z-score, chỉ vào ô màu đỏ dương (*Tempo, Danceability, Valence*).<br>• Đổi dropdown Boxplot từ *Energy* sang *Valence*.<br>• Bấm vào phần **Collab** trên biểu đồ Donut.<br>• Chỉ chuột xuống biểu đồ đường thời lượng bài hát. | *"**Chương 1: Công thức tạo Hit.**<br><br>Nhìn vào Biểu đồ nhiệt chuẩn hóa z-score: Nhóm **Top 1–10** nổi bật hoàn toàn với sắc đỏ: nhịp độ Tempo cao hơn 0,16 độ lệch chuẩn (+5,5 BPM), Danceability và Valence đều vượt trội. Ngược lại, Acousticness và Instrumentalness âm sâu. Đáng chú ý, Loudness gần như bằng 0 — chứng minh cố gắng đẩy âm lượng to không giúp bài hát thăng hạng!<br><br>Khi bấm chọn nhóm **Collab** trên biểu đồ tròn: Mặc dù đơn ca chiếm 60% số lượng, nhưng ca khúc hợp tác (Collab) lại có trung vị lượt stream cao hơn hẳn — là đòn bẩy cộng hưởng khán giả.<br><br>Và ở biểu đồ dưới cùng: Thời lượng bài hát đã giảm từ **218 giây (2017) xuống 198 giây (2020)** — giảm 20 giây để thích ứng với chu kỳ chú ý ngắn của TikTok và cơ chế tính stream sau 30 giây của Spotify."* | • Z-score làm nổi bật đặc trưng Top 1-10.<br>• Collab có trung vị stream cao hơn Solo.<br>• Bài hát ngắn đi 20 giây thích ứng TikTok. |
| **05:40 – 06:20** | **Story 2: Nghệ sĩ & Hợp tác**<br>• Bấm nút chuyển sang **Point 2: Nghệ sĩ & hợp tác**.<br>• Rê chuột qua biểu đồ tán xạ phân tích tương quan Spearman (trục hoành: Điểm nghệ sĩ quá khứ, trục tung: Stream 8 tuần).<br>• Hover vào Treemap 80 nghệ sĩ dẫn đầu. | *"**Chương 2: Tên tuổi Nghệ sĩ và Lượt nghe.**<br><br>Ở biểu đồ phân tán bên trái, nhóm em sử dụng hệ số tương quan hạng Spearman để đo mối liên hệ giữa thành tích quá khứ của nghệ sĩ với lượt stream 8 tuần đầu khi bài hát lọt bảng xếp hạng Global.<br><br>Tương quan đạt mức dương đáng kể: một nghệ sĩ đã có thương hiệu lớn sẽ có xác suất bùng nổ lượt nghe ngay trong những tuần đầu cao hơn rõ rệt. Tuy nhiên, vẫn xuất hiện những điểm ngoại lệ (Outliers) phía trên — những ca khúc 'one-hit wonder' của nghệ sĩ mới nổi nhờ hiệu ứng mạng xã hội."* | Tương quan Spearman kháng rò rỉ; nhận diện các hiện tượng One-hit wonder. |
| **06:20 – 07:05** | **Story 3: Bản sắc Địa lý & ADN Âm nhạc Toàn cầu**<br>• Bấm chuyển sang **Point 3: Bản sắc địa lý**.<br>• Chọn dropdown chỉ số trên Bản đồ Choropleth là *Valence*.<br>• Bấm chọn **Việt Nam** (đường xanh) và so sánh với **Nhật Bản** (đường tím) trên Radar Chart. | *"**Chương 3: Bản sắc Địa lý.** Khi đưa âm nhạc ra thế giới, liệu một bài hát có chinh phục được mọi quốc gia?<br><br>Bản đồ thế giới cho thấy khu vực Mỹ Latinh rực sáng sắc đỏ với chỉ số cảm xúc tích cực (Valence) cao nhất toàn cầu.<br><br>Đặc biệt, nhìn vào màn đối đầu trên Radar Chart giữa **Việt Nam và Nhật Bản**: Hai quốc gia thể hiện hai bản sắc âm học đối lập 180 độ! Khán giả Việt Nam chuộng Pop Ballad mộc mạc (Acousticness đạt 0,47, Energy chỉ 0,53). Ngược lại, Nhật Bản dẫn đầu về J-Pop và Anime sôi động (Energy lên tới 0,73, nhịp độ rất nhanh, Acousticness chỉ 0,17).<br><br>Insight chiến lược: Mang một bài Ballad dịu êm của Việt Nam sang Nhật Bản mà không remix lại theo phong cách dồn dập thì sẽ rất khó để cạnh tranh!"* | Đối đầu trực tiếp Việt Nam vs Nhật Bản chứng minh sự phân hóa sâu sắc của văn hóa nghe nhạc. |
| **07:05 – 07:45** | **Story 4: Chu kỳ Thời gian & Biến động Đại dịch COVID-19**<br>• Bấm chuyển sang **Point 4: Chu kỳ thời gian**.<br>• Chỉ vào cột **Tháng 12** trên biểu đồ 12 tháng: Acousticness tăng vọt.<br>• Rê chuột qua biểu đồ kết hợp chuỗi thời gian tử vong COVID-19 và đường âm thanh. | *"**Chương 4: Chu kỳ Thời gian & Đại dịch.**<br><br>Nhìn vào chu kỳ 12 tháng, độ nhảy duy trì quanh mức 0,70 nhưng đến tháng 12 thì giảm sâu, nhường chỗ cho Acousticness tăng vọt. Lý do là bảng xếp hạng tháng 12 bị chiếm trọn bởi các ca khúc Giáng sinh kinh điển như của Mariah Carey hay Wham!.<br><br>Đối chiếu với các làn sóng tử vong COVID-19 từ 2020 đến 2022: Khi đại dịch lập đỉnh, Acousticness tăng cao, Energy giảm sâu, nhưng Valence vẫn kiên định đi ngang trên mốc 0,50. Âm nhạc trong đại dịch **trở nên êm dịu hơn để chữa lành, nhưng không hề bi quan**."* | • Tháng 12 là mùa nhạc Giáng sinh hoài niệm.<br>• COVID-19: Âm nhạc êm hơn nhưng không buồn hơn (hiệu ứng chữa lành). |
| **07:45 – 08:15** | **Story 5: Mô hình Hóa & Ngưỡng Dự Báo (Machine Learning)**<br>• Bấm chuyển sang **Point 5: Mô hình & Ngưỡng dự báo**.<br>• Kéo thanh trượt ngưỡng phân loại $\tau$ từ 0.50 lên **0.79**.<br>• Quan sát Ma trận nhầm lẫn (Confusion Matrix) và đường Precision-Recall thay đổi ngay lập tức. | *"**Chương 5: Chuyển hóa Dự báo thành Hành động.**<br><br>Đây là mô hình Logistic Regression do bạn **Đỗ Thanh Thành Tài** huấn luyện, đạt **AUC ấn tượng 0,811** trên tập kiểm thử độc lập 2021–2022.<br><br>Mô hình được thiết kế **kháng rò rỉ dữ liệu (anti-leakage)**: chỉ dùng đặc trưng âm học và thành tích tuần đầu để dự báo khả năng bài hát trụ vững trong Top 50 suốt 8 tuần tiếp theo.<br><br>Đặc biệt, hệ thống cho phép nhà quản lý kéo thanh trượt ngưỡng $\tau$. Tại ngưỡng tối ưu $\tau = 0,79$, F1-score đạt cực đại, cân bằng hoàn hảo giữa việc bắt trúng bài Hit (Precision) mà không bỏ sót tiềm năng (Recall)."* | • AUC = 0.811, Test set độc lập 2021-2022.<br>• Kháng rò rỉ dữ liệu.<br>• Tương tác ngưỡng $\tau = 0.79$ tối ưu quyết định. |

---

### PHẦN 4: TỔNG KẾT, GIÁ TRỊ ỨNG DỤNG & LỜI KẾT (08:15 – 09:15)

* **Màn hình hiển thị:** Quay lại màn hình tổng quan Story Studio hoặc trang thông tin nhóm.

| Mốc thời gian | Thao tác trên màn hình | Lời thoại thuyết minh (Voiceover Script) | Thông điệp dữ liệu cốt lõi |
| :--- | :--- | :--- | :--- |
| **08:15 – 09:15** | • Mở rộng góc nhìn toàn màn hình, rê chuột qua các tab lần cuối.<br>• Kết thúc video với giọng nói tự tin, trang trọng. | *"Kính thưa Thầy Cô và các bạn! Thông qua hệ sinh thái phân tích toàn diện từ **EDA Chuyên sâu, Bento Grid, đến Story Studio 5 trụ cột**, đề tài của nhóm 04 đã giải quyết trọn vẹn vòng đời của dữ liệu âm nhạc:<br><br>1. **Hiểu quá khứ:** Nhận diện công thức tạo hit, văn hóa vùng miền và tính mùa vụ.<br>2. **Mô phỏng hiện tại:** Khám phá mạng lưới liên kết nghệ sĩ toàn cầu.<br>3. **Dự báo tương lai:** Cung cấp công cụ phân loại Hit chuẩn xác phục vụ trực tiếp cho các hãng đĩa và nghệ sĩ.<br><br>Chúng em xin chân thành cảm ơn Thầy Cô và các bạn đã theo dõi video demo đồ án! Rất mong nhận được những góp ý quý báu từ Hội đồng."* | Tóm lược 3 giá trị: Hiểu quá khứ — Mô phỏng hiện tại — Dự báo tương lai. |

---

## 🎯 BẢNG TỔNG HỢP PHÂN CÔNG THUYẾT MINH TRONG VIDEO

Nếu nhóm muốn **quay video có sự tham gia thuyết minh của cả 3 thành viên** (hoặc 1 người nói đại diện nhưng nêu rõ tên đóng góp), phân bổ như sau:

| Thành viên | MSSV | Phần thuyết minh trong video | Mốc thời lượng |
| :--- | :--- | :--- | :--- |
| **Lý Gia Hân** | 24133021 | • Giới thiệu đề tài & Kiến trúc Story Studio<br>• Trình diễn Story Studio (Point 1, 3, 4)<br>• Trình diễn Bento Grid thị trường | Phút 00:00 – 01:00<br>Phút 03:30 – 04:30<br>Phút 04:30 – 07:45 |
| **Đinh Quốc Anh** | 24133003 | • Phân tích EDA đặc trưng âm thanh & Treemap<br>• Đồ thị mạng lưới đồng xuất hiện (Network Science)<br>• Công cụ giả lập Hit Simulator | Phút 01:00 – 03:30 |
| **Đỗ Thanh Thành Tài** | 24133083 | • Trình bày Story Point 5: Machine Learning Decision Boundary, ngưỡng $\tau$, Ma trận nhầm lẫn & Kết luận ứng dụng | Phút 07:45 – 09:15 |

---

## 💡 MẸO & KỸ THUẬT QUAY ĐỂ VIDEO ĐẠT ĐIỂM TỐI ĐA (PRO TIPS)

1. **Độ phân giải màn hình:** Đặt màn hình ở độ phân giải **1920 × 1080** hoặc **1440 × 900**. Tránh dùng màn hình 4K hoặc 2K siêu rộng (Ultrawide) vì khi nén video chữ sẽ bị bé khó đọc trên máy chấm của Thầy Cô.
2. **Âm thanh nền (BGM):** Có thể chèn một đoạn nhạc nền nhẹ không lời (Lo-fi acoustic / ambient chill) với âm lượng cực nhỏ (**5% – 8%**) để tạo không khí âm nhạc Spotify chuyên nghiệp, nhưng **tuyệt đối không để lấn át giọng nói**.
3. **Hiệu ứng thu phóng (Zoom-in) khi biên tập:** Nếu sử dụng CapCut/Premiere/Camtasia để cắt ghép:
   - Khi nói về *Heatmap z-score Top 1-10*, zoom nhẹ vào 150% khu vực ô z-score.
   - Khi nói về *Radar Việt Nam vs Nhật Bản*, zoom vào biểu đồ Radar.
   - Khi nói về *Hit Simulator / Gauge chart*, zoom vào đồng hồ đo %.
4. **Chuẩn bị kịch bản giấy trước mặt:** In hoặc mở kịch bản này trên điện thoại/màn hình phụ để nói liền mạch, không bị ậm ừ ("ờ, à"), giữ nhịp điệu hào hứng, tự tin.
