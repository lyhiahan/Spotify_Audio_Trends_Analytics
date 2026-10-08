# Spotify Audio Atlas — 3 dashboard / 9 biểu đồ

Story cho dự án Gia Hân cập nhật theo `notebooks/04_story.ipynb` mới nhất. Mỗi story point chứa một dashboard; toàn bộ biểu đồ xuất hiện đồng thời trong canvas theo chiều cao màn hình. Bố cục desktop được kiểm tra ở 1440 × 900, không cuộn trang. Màn hình hẹp có nút Bộ lọc mở cột điều khiển.

## Chạy

```powershell
./start_story.ps1
```

Mở http://localhost:8502/. Bản độc lập: `docs/spotify_data_story.html`. Bản đồ cần mạng để tải địa giới Plotly; dữ liệu và thư viện vẽ đã nhúng trong HTML.

## Câu chuyện

| Dashboard | Biểu đồ cùng hiển thị | Câu hỏi |
|---|---|---|
| 1 · Công thức tạo hit & xu hướng | Heatmap 9 đặc trưng × 4 tầng hạng; boxplot 4 chỉ số × 5 thể loại; treemap thể loại → Top 80 nghệ sĩ; donut & bar Solo/Collab; thời lượng tuần & đường trung bình 4 tuần | Các bản hit khác nhau như thế nào về âm học, thể loại, nghệ sĩ và thời lượng? |
| 2 · Bản sắc địa lý & ADN âm nhạc | Bản đồ chuyển 4 chỉ số; radar 6 trục của 2 quốc gia | Khác biệt quốc gia có còn rõ khi dùng cùng năm và cách tính? |
| 3 · Mùa vụ & COVID-19 | Cột nhóm 12 tháng; tử vong tuần và đường âm thanh chuyển đủ 9 đặc trưng | Đâu là mùa vụ cuối năm, đâu là đồng biến động trong đại dịch? |

Navy cho cấu trúc, xanh lam/xanh ngọc cho đối chiếu, tím cho quốc gia B và màu ấm cho các nhóm phụ. Luận điểm tự tính theo bộ lọc; lời giải thích nguyên nhân được ghi là giả thuyết.

## Tương tác

- Dashboard 1: năm → thể loại → nghệ sĩ, tầng hạng và Solo/Collab. Bấm heatmap chọn đặc trưng/tầng hạng; bấm boxplot chọn thể loại; bấm nhánh treemap rồi nghệ sĩ để lọc chéo. Nút ↑ Gốc trở về toàn bộ thể loại. Bấm donut/bar chọn Solo hoặc Collab. Boxplot có dropdown riêng cho Energy, Danceability, Valence, Tempo.
- Thời lượng mặc định giữ bối cảnh 2017–2022, tô khoảng năm BXH chọn. Lọc thể loại/nghệ sĩ/tầng hạng/biểu diễn chuyển sang trung bình tháng theo stream và đường trung bình 4 tháng; bấm điểm thời gian để chọn năm BXH.
- Dashboard 2: năm → vùng → quốc gia A, chọn quốc gia B và phương pháp trung bình. Bấm quốc gia trên bản đồ cập nhật A trong radar. Bản đồ có Valence, Danceability, Acousticness, Energy; bảng chi tiết đối chiếu đủ 9 chỉ số.
- Dashboard 3: năm → tháng → tuần. Bấm tháng lọc chuỗi COVID và mở Top bài của tháng. Bấm tuần mở chi tiết 9 đặc trưng. Các đoạn giữa tháng không liên tục được ngắt đường, tránh nối qua thời gian không có dữ liệu.
- Hover hiển thị thông số, đơn vị và ngữ cảnh; zoom/pan, legend theo hỗ trợ của Plotly. Bỏ lựa chọn/Khôi phục point trở về trạng thái đã chụp của point.

## Biên tập và xuất

Biên tập caption, lời dẫn, ghi chú và thứ tự story point. Áp dụng chụp bộ lọc hiện tại; chuyển point khôi phục bộ lọc đã lưu. Nút Lưu giữ workbook v4 trong trình duyệt; JSON dùng để mở lại cấu hình. Phiên bản v4 có cấu trúc 3 dashboard nên không nhập workbook v2/v3.

HTML xuất story tương tác có dữ liệu và cấu hình; PNG xuất từng biểu đồ; CSV xuất giá trị đang được vẽ. PDF mở hộp thoại in dashboard hiện tại; nếu trình duyệt không hỗ trợ in iframe, mở HTML độc lập để in. Không xuất TWBX.

## Phạm vi và kiểm tra số liệu

Nguồn là 6 bảng Parquet đã xử lý, tương ứng các bảng CSV mà notebook tham chiếu. Notebook và quy trình tiền xử lý không bị sửa.

- Các dòng nghệ sĩ cùng bài/tuần/thị trường/hạng được bỏ đếm lặp khi tính stream bài hát: 1.787.531 dòng ghi công tương ứng 1.109.375 lần xuất hiện BXH.
- Heatmap là độ lệch trung bình nhóm chia độ lệch chuẩn toàn BXH Global (z-score), không phải ma trận tương quan. Mẫu mặc định 2020–2022; baseline giữ đủ bốn tầng hạng trong cùng bộ lọc.
- Boxplot và donut dùng danh mục bài hát, mỗi bài một lần. Bar chỉ tính bài có stream trong năm chọn. Trên toàn bộ mẫu, Collab khoảng 21,8 triệu/bài, Solo 17,7 triệu/bài; không xác nhận con số gấp ba. Treemap dùng stream ghi công cho nghệ sĩ, nên không phải thị phần độc quyền.
- Trung bình thời lượng tuần theo năm: 2017 khoảng 218,0 giây; 2020 khoảng 198,5; 2022 khoảng 205,7. Có giảm rồi tăng lại; không kết luận giảm liên tục hay TikTok là nguyên nhân.
- Địa lý có 68 quốc gia năm 2021 và 73 năm 2022. Radar và bản đồ dùng cùng phương pháp: trung bình thường hoặc theo stream. Đặc trưng âm học không tự chứng minh loại nhạc hay tâm lý người nghe.
- Có 289 tuần Global trong 2017–2022, trong đó 130 tuần ghép được với COVID từ 2020 đến 07/2022. Năm 2022 chỉ có 28 tuần. Nhóm tuần tử vong cao/thấp chia theo trung vị trong phạm vi lọc, chỉ là mô tả đồng biến động.
- Bấm tháng 12 hiện các bài Giáng sinh nổi bật: đây là bằng chứng trực tiếp trong danh sách bài để giải thích mùa vụ. Giả thuyết giãn cách, nghe tại nhà, thuật toán hay chữa lành cần dữ liệu bổ sung để kiểm chứng.

## Mã nguồn và xác minh

`story_data.py` đọc và bỏ đếm lặp dữ liệu; `story_canvas.py` dựng workbook/payload; `story_canvas.html` bố cục; `story_interactions.js` tổng hợp, vẽ và liên kết biểu đồ. Streamlit cache theo thời gian sửa nguồn, notebook và dữ liệu.

```powershell
node --check dashboard/story_interactions.js
node tests/test_story_figures.cjs
python -m compileall -q dashboard/story_app.py dashboard/story_canvas.py dashboard/story_data.py
python -c "import sys; sys.path.insert(0,'dashboard'); import story_canvas; from pathlib import Path; Path('docs/spotify_data_story.html').write_text(story_canvas.canvas_html(),encoding='utf-8')"
```

Kiểm tra hồi quy bao gồm stream Collab bỏ đếm lặp, 9 z-score, bộ lọc phân cấp, drill-down thời lượng, cách tính radar thống nhất, lọc tháng và nhóm dữ liệu rỗng. Giao diện kiểm tra trực tiếp gồm chuyển point, boxplot, thể loại/nghệ sĩ, cách tính quốc gia, tháng → COVID → chi tiết tuần.
