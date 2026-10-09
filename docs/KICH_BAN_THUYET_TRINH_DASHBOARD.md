# KỊCH BẢN THUYẾT TRÌNH CHI TIẾT: SPOTIFY AUDIO ATLAS
## HỆ THỐNG TRỰC QUAN HÓA VÀ KỂ CHUYỆN DỮ LIỆU TƯƠNG TÁC (INTERACTIVE DATA STORYTELLING)

* **Học phần:** Tương tác Dữ liệu Trực quan (Interactive Data Visualization / Visual Analytics)
* **Người thực hiện & Thuyết trình:** **Lý Gia Hân** (Vai trò: *Visualization Specialist & Lead Data Analyst*)
* **Đối tượng tiếp nhận:** Hội đồng Giám khảo / Ban Giám đốc & Đối tác Sản xuất Âm nhạc
* **Thời lượng dự kiến:** 7 – 8 phút (bao gồm chuyển giao cho phần Machine Learning)
* **Ứng dụng trình diễn:** Story Studio (`dashboard/story_app.py` hoặc `./start_story.ps1` chạy cổng `8502`)

---

## 📌 PHẦN CHUẨN BỊ TRƯỚC KHI BẮT ĐẦU (CHECKLIST KỸ THUẬT)

1. **Khởi chạy ứng dụng:** Mở terminal chạy lệnh `./start_story.ps1` (hoặc `streamlit run dashboard/story_app.py`).
2. **Thiết lập hiển thị:** Truy cập `http://localhost:8502/`, bấm phím **F11** trên trình duyệt để đưa về chế độ toàn màn hình (Full Screen).
3. **Độ phân giải tối ưu:** Giao diện được tối ưu chuẩn màn hình 1440 × 900 không cần cuộn trang (No-scroll canvas).
4. **Kiểm tra trạng thái ban đầu:** Đảm bảo ứng dụng đang dừng ở **Story Point 1 (Công thức tạo hit & xu hướng)**, các bộ lọc ở trạng thái mặc định (Tất cả năm, Tất cả thể loại).

---

## 🕒 TỔNG QUAN PHÂN BỔ THỜI GIAN THUYẾT TRÌNH

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ [00:00 - 01:00]  PHẦN 1: Mở đầu, Bối cảnh kinh doanh & Giới thiệu Nền tảng   │
├──────────────────────────────────────────────────────────────────────────────┤
│ [01:00 - 03:00]  PHẦN 2: Story 1 - Công thức tạo Hit & Xu hướng Thời đại     │
├──────────────────────────────────────────────────────────────────────────────┤
│ [03:00 - 04:30]  PHẦN 3: Story 2 - Bản sắc Địa lý & ADN Âm nhạc Toàn cầu     │
├──────────────────────────────────────────────────────────────────────────────┤
│ [04:30 - 06:00]  PHẦN 4: Story 3 - Tính Mùa vụ 12 Tháng & Ứng phó Đại dịch   │
├──────────────────────────────────────────────────────────────────────────────┤
│ [06:00 - 07:00]  PHẦN 5: Tổng kết, Khuyến nghị & Bàn giao phần Machine Learning│
├──────────────────────────────────────────────────────────────────────────────┤
│ [07:00+]         PHẦN 6: Chuẩn bị câu hỏi phản biện (Q&A)                    │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 🎬 KỊCH BẢN CHI TIẾT TỪNG PHÚT

---

### PHẦN 1: MỞ ĐẦU, BỐI CẢNH VÀ NỀN TẢNG CÔNG NGHỆ (00:00 – 01:00)

| Thao tác trên màn hình (Hành động) | Lời thoại thuyết trình (Gia Hân) |
| :--- | :--- |
| • Đứng trước màn hình, giữ giao diện Story Point 1 ở trạng thái tổng quan.<br><br>• Chưa bấm vội vào các biểu đồ con, giữ ánh mắt bao quát hội đồng/sếp. | *"Kính thưa Thầy Cô trong Hội đồng và các bạn! Em là **Lý Gia Hân**, đảm nhiệm vai trò Visualization Specialist và Data Analyst của đề tài.<br><br>Trong thời đại mà mỗi tuần có hàng chục nghìn ca khúc mới được phát hành lên các nền tảng phát trực tuyến, câu hỏi lớn nhất mà các nghệ sĩ và hãng đĩa đặt ra là: **Làm thế nào để một tác phẩm nổi bật và trụ vững trên bảng xếp hạng?**<br><br>Để trả lời bài toán này, em đã xây dựng hệ thống **Spotify Audio Atlas** dựa trên hơn 1,78 triệu bản ghi bảng xếp hạng tuần toàn cầu. Hệ thống được phát triển hoàn toàn trên nền tảng **Streamlit kết hợp Plotly**, mang lại trải nghiệm khám phá dữ liệu tương tác đa chiều thời gian thực trên một màn hình duy nhất mà không cần cuộn trang.<br><br>Sau đây, em xin mời Hội đồng cùng bước vào hành trình kể chuyện dữ liệu qua 3 trụ cột phân tích chuyên sâu."* |

---

### PHẦN 2: STORY 1 — CÔNG THỨC TẠO HIT & XU HƯỚNG THỜI ĐẠI (01:00 – 03:00)

| Thao tác trên màn hình (Hành động) | Lời thoại thuyết trình (Gia Hân) |
| :--- | :--- |
| **Bước 1: Giới thiệu Biểu đồ nhiệt (Heatmap z-score)**<br>• Rê chuột vào hàng **Top 1–10**, chỉ vào các ô màu đỏ dương tính (*Tempo, Danceability, Valence*). | *"Trụ cột đầu tiên: **Công thức tạo Hit**. Nhìn vào Biểu đồ nhiệt ở góc trên bên trái, nhóm em sử dụng chỉ số chuẩn hóa z-score để đo mức độ khác biệt của từng nhóm thứ hạng so với trung bình toàn bảng xếp hạng.<br><br>Nhóm **Top 1–10** nổi bật hoàn toàn với sắc đỏ dương tính: nhịp độ Tempo cao hơn 0,16 độ lệch chuẩn (nhanh hơn trung bình 5,5 nhịp BPM), độ dễ nhảy Danceability và năng lượng Energy đều vượt trội. Ngược lại, tính mộc (Acousticness) và tính không lời (Instrumentalness) giảm sâu xuống sắc xanh âm tính.<br><br>Đặc biệt, chỉ số âm lượng (Loudness) gần như bằng 0 trên mọi phân tầng — chứng minh rằng việc cố gắng đẩy âm lượng to hơn không giúp bài hát thăng hạng, mà chìa khóa nằm ở nhịp điệu bắt tai và phần lời hát điệp khúc ấn tượng."* |
| **Bước 2: Chuyển đổi Boxplot thể loại**<br>• Bấm chọn dropdown trên biểu đồ hộp từ *Energy* sang *Valence*. | *"Khi nhìn vào phân bố thể loại qua biểu đồ hộp, chúng ta thấy rõ bản sắc riêng biệt: dòng nhạc Latin áp đảo về độ tươi vui (Valence đạt trung vị 0,67, vượt xa các dòng nhạc khác), trong khi Rap và Pop lại mang phổ cảm xúc trầm và tự sự hơn. Điều này khẳng định không có một dòng nhạc nào vượt trội trên mọi chỉ số, mà mỗi thể loại đều có thế mạnh cảm xúc riêng."* |
| **Bước 3: Lọc chéo Solo vs. Collab**<br>• Bấm vào phần **Collab** trên biểu đồ Donut.<br>• Quan sát toàn bộ canvas tự động lọc theo nhóm hợp tác. | *"Về chiến lược phát hành: **Nên hát đơn hay kết hợp nhiều nghệ sĩ?**<br><br>Khi em bấm chọn nhóm Collab, biểu đồ cho thấy một phát hiện rất giá trị: Mặc dù các ca khúc đơn ca chiếm gần 60% số lượng phát hành, nhưng các sản phẩm hợp tác (Collab) lại đạt mức trung vị lượt stream cao hơn hẳn so với đơn ca. Sự kết hợp giữa các nghệ sĩ chính là đòn bẩy hiệu quả nhất để cộng hưởng tệp khán giả của nhau."* |
| **Bước 4: Xu hướng thời lượng bài hát**<br>• Chỉ chuột xuống biểu đồ đường thời lượng ở dưới cùng. | *"Và ở biểu đồ thời lượng dưới cùng, chúng ta thấy rõ xu hướng rút ngắn độ dài bài hát: từ mức trung bình 218 giây vào năm 2017 xuống còn 198 giây vào năm 2020 — giảm mất 20 giây chỉ sau 3 năm. Đây là sự thích ứng trực tiếp của âm nhạc trước làn sóng video ngắn TikTok và cơ chế tính lượt stream sau 30 giây của Spotify."* |

---

### PHẦN 3: STORY 2 — BẢN SẮC ĐỊA LÝ & ADN ÂM NHẠC TOÀN CẦU (03:00 – 04:30)

| Thao tác trên màn hình (Hành động) | Lời thoại thuyết trình (Gia Hân) |
| :--- | :--- |
| **Bước 1: Chuyển sang Story Point 2**<br>• Bấm nút chuyển sang **Point 2: Bản sắc địa lý** trên thanh điều khiển.<br>• Chuyển dropdown chỉ số trên Bản đồ thế giới sang *Valence*. | *"Bước sang trụ cột thứ hai: **Bản sắc Địa lý và Văn hóa âm nhạc**. Khi một nghệ sĩ muốn đưa tác phẩm ra quốc tế, liệu một giai điệu có thể chinh phục được mọi quốc gia hay không?<br><br>Quan sát Bản đồ thế giới Choropleth, khi chọn chỉ số cảm xúc tích cực (Valence), khu vực Mỹ Latinh rực sáng với sắc đỏ vượt trội. Đây là khu vực tiêu thụ âm nhạc có giai điệu tươi vui, tiệc tùng và giàu sức sống nhất toàn cầu."* |
| **Bước 2: Đối đầu trực tiếp trên Radar Chart**<br>• Bấm vào **Việt Nam** trên bản đồ (tự động cập nhật vào Radar Chart màu xanh lam).<br>• Chọn quốc gia so sánh là **Nhật Bản** (đường màu tím). | *"Để thấy rõ sự khác biệt văn hóa, em xin mời Thầy Cô nhìn vào màn đối đầu trực tiếp giữa hai thị trường lớn tại Châu Á: **Việt Nam** và **Nhật Bản**.<br><br>Hai quốc gia thể hiện hai dấu vân tay âm nhạc đối lập 180 độ:
- Khán giả Việt Nam dành sự ưu tiên vượt bậc cho các ca khúc Pop Ballad mộc mạc, nhẹ nhàng, thể hiện qua tính mộc Acousticness đạt 0,47 và năng lượng Energy chỉ ở mức 0,53.
- Ngược lại, Nhật Bản dẫn đầu thế giới về J-Pop, J-Rock và nhạc hoạt hình Anime với năng lượng dồn dập lên tới 0,73, nhịp độ rất nhanh và âm thanh mộc chỉ chiếm 0,17.<br><br>Insight mang tính ứng dụng ở đây là: Nếu mang một bài hát ballad êm dịu đang thịnh hành tại Việt Nam sang phát hành tại Nhật Bản mà không phối khí lại theo hướng dồn dập, bài hát đó rất khó để cạnh tranh trên bảng xếp hạng nước bạn."* |

---

### PHẦN 4: STORY 3 — TÍNH MÙA VỤ 12 THÁNG & ỨNG PHÓ ĐẠI DỊCH (04:30 – 06:00)

| Thao tác trên màn hình (Hành động) | Lời thoại thuyết trình (Gia Hân) |
| :--- | :--- |
| **Bước 1: Chuyển sang Story Point 3**<br>• Bấm chuyển sang **Point 3: Mùa vụ & COVID-19**.<br>• Chỉ vào Biểu đồ cột nhóm 12 tháng. | *"Trụ cột thứ ba giải quyết bài toán: **Nên phát hành bài hát vào thời điểm nào trong năm?**<br><br>Nhìn vào chu kỳ 12 tháng, độ dễ khiêu vũ (Danceability) duy trì rất ổn định từ tháng 1 đến tháng 11 quanh mức 0,70. Tuy nhiên, sang đến tháng 12, chỉ số này giảm mạnh nhường chỗ cho tính mộc (Acousticness) tăng vọt lên đỉnh điểm."* |
| **Bước 2: Drill-down danh sách bài hát**<br>• Bấm trực tiếp vào cột **Tháng 12**.<br>• Xem bảng Top ca khúc tháng 12 vừa hiển thị bên dưới. | *"Khi em bấm vào tháng 12 để xem chi tiết danh sách bài hát, nguyên nhân lập tức được chứng minh bằng dữ liệu: Bảng xếp hạng tháng 12 bị thống trị hoàn toàn bởi các ca khúc Giáng sinh và kỳ nghỉ kinh điển như của Mariah Carey hay Wham!.<br><br>Khuyến nghị thực tế cho các nghệ sĩ trẻ: Tránh phát hành các bài hát Dance Pop sôi động vào tháng 12 vì sẽ phải đối đầu trực tiếp với thói quen hoài niệm lễ hội của công chúng."* |
| **Bước 3: Tương quan chuỗi thời gian COVID-19**<br>• Rê chuột qua biểu đồ kết hợp chuỗi thời gian tử vong dịch bệnh và đường âm thanh. | *"Đặc biệt, khi đối chiếu dữ liệu âm nhạc với chuỗi tử vong đại dịch COVID-19 từ năm 2020 đến 2022, chúng em phát hiện một quy luật tâm lý rất thú vị: **Âm nhạc trở nên êm hơn nhưng không buồn hơn**.<br><br>Khi các đợt tử vong do dịch bệnh lập đỉnh, tính mộc (Acousticness) tăng cao, năng lượng (Energy) giảm sâu, nhưng chỉ số cảm xúc (Valence) vẫn kiên định đi ngang trên mốc 0,50. Điều này cho thấy trong nghịch cảnh, âm nhạc đóng vai trò như một liều thuốc chữa lành: người nghe tìm kiếm sự mộc mạc, yên bình để xoa dịu tinh thần chứ không đắm chìm vào những giai điệu bi quan."* |

---

### PHẦN 5: TỔNG KẾT, ĐÓNG GÓI & KẾT NỐI SANG MACHINE LEARNING (06:00 – 07:00)

| Thao tác trên màn hình (Hành động) | Lời thoại thuyết trình (Gia Hân) |
| :--- | :--- |
| • Chuyển giao diện về trang tổng kết hoặc mở trang dự báo Machine Learning.<br><br>• Quay sang bạn Thành Tài để sẵn sàng chuyển giao lượt thuyết trình. | *"Kính thưa Thầy Cô và các bạn, thông qua 3 Dashboard với 9 biểu đồ tương tác cao, hệ thống **Spotify Audio Atlas** đã làm sáng tỏ trọn vẹn bức tranh âm nhạc từ cấp độ bài hát, nghệ sĩ, vùng miền cho đến các biến động lịch sử.<br><br>Tuy nhiên, mục tiêu cuối cùng của Data Science không chỉ dừng lại ở việc mô tả quá khứ, mà còn là **dự báo tương lai**. Để giúp các nhà sản xuất có thể kiểm tra xem một bài hát mới toanh trước khi ra mắt có cơ hội trở thành Hit hay không, nhóm em đã xây dựng mô hình Machine Learning phân loại Hit kháng rò rỉ dữ liệu.<br><br>Sau đây, em xin trân trọng nhường lại phần trình bày cho bạn **Đỗ Thanh Thành Tài** để đi sâu vào thuật toán và mô hình dự báo. Em xin chân thành cảm ơn!"* |

---

## 💡 BỘ CÂU HỎI VẤN ĐÁP DỰ PHÒNG (Q&A) DÀNH CHO GIA HÂN

Dưới đây là các câu hỏi Thầy Cô hoặc Giám khảo rất hay hỏi về phần Trực quan hóa, cùng câu trả lời mẫu chuẩn xác nhất:

### Câu hỏi 1: Tại sao em lại chọn Streamlit và Plotly mà không dùng PowerBI hay Tableau?
* **Trả lời của Gia Hân:**  
  *"Dạ thưa Thầy/Cô, PowerBI và Tableau là những công cụ Business Intelligence rất mạnh, nhưng trong khuôn khổ một đồ án Khoa học Dữ liệu toàn diện, việc chọn **Streamlit kết hợp Plotly** mang lại 3 ưu thế vượt trội:  
  1. **Tính linh hoạt:** Cho phép em tự lập trình các logic xử lý dữ liệu phức tạp (như tính toán z-score theo nhóm, chuẩn hóa dữ liệu ghép nối với COVID-19) mà không bị giới hạn bởi các hàm dựng sẵn của phần mềm thương mại.  
  2. **Tích hợp liền mạch với Machine Learning:** Streamlit cho phép kết nối trực tiếp với mô hình Scikit-learn của bạn Tài trên cùng một mã nguồn Python. Khi người dùng thay đổi thông số bài hát trên giao diện, mô hình có thể dự báo ngay lập tức.  
  3. **Khả năng đóng gói độc lập:** Em có thể xuất ra file HTML tương tác độc lập (`spotify_data_story.html`) hoặc chạy web app cục bộ mà người dùng không cần mua bản quyền phần mềm."*

### Câu hỏi 2: Tại sao biểu đồ nhiệt ở Dashboard 1 lại dùng z-score thay vì hiển thị giá trị trung bình thật?
* **Trả lời của Gia Hân:**  
  *"Dạ, các đặc trưng âm thanh của Spotify có đơn vị đo lường hoàn toàn khác nhau: Tempo đo bằng BPM (khoảng 120), Loudness đo bằng Decibel âm (-6 dB), trong khi Danceability và Valence lại nằm trên thang đo từ 0 đến 1. Nếu đưa trực tiếp giá trị thật lên một biểu đồ nhiệt thì các biến có số lớn sẽ lấn át hoàn toàn các biến còn lại. Việc chuẩn hóa về **z-score** đưa tất cả các biến về cùng một thước đo độ lệch chuẩn, giúp chúng ta nhìn thấy ngay thuộc tính nào thực sự tạo nên sự khác biệt giữa các nhóm thứ hạng."*

### Câu hỏi 3: Biểu đồ thời lượng cho thấy bài hát giảm từ 218s xuống 198s, có chắc chắn là do TikTok không?
* **Trả lời của Gia Hân:**  
  *"Dạ thưa Thầy/Cô, như em đã nêu trong phần nguyên tắc diễn giải ở Chương 1, dữ liệu ghi nhận đây là **sự đồng biến động theo thời gian** giữa giai đoạn TikTok bùng nổ và sự suy giảm độ dài bài hát. Chúng em không khẳng định TikTok là nguyên nhân duy nhất, mà đây là sự cộng hưởng giữa hai yếu tố: sự thay đổi trong chu kỳ chú ý của người nghe trên mạng xã hội, kết hợp với cơ chế trả phí bản quyền của Spotify (chỉ cần nghe đủ 30 giây là tính một lượt stream), tạo động lực kinh tế cho các nhà sản xuất làm bài hát ngắn hơn để tối ưu lượt nghe lặp lại."*

### Câu hỏi 4: Thao tác "lọc chéo" (Cross-filtering) trong Dashboard của em hoạt động như thế nào?
* **Trả lời của Gia Hân:**  
  *"Dạ, trong file `story_interactions.js` và `story_canvas.py`, em đã thiết lập cơ chế lắng nghe sự kiện click của Plotly. Khi người dùng bấm vào một phần tử (ví dụ: bấm vào nhãn Collab trên biểu đồ Donut hoặc bấm vào nhánh Pop trên Treemap), hệ thống sẽ bắt lấy giá trị thuộc tính đó, tự động lọc lại bảng dữ liệu tương ứng trong bộ nhớ và cập nhật lại đồng thời tất cả các biểu đồ còn lại trên màn hình mà không cần phải tải lại trang."*
