# Spotify Audio Atlas — 5 story point / 14 hình và biểu đồ

Điểm mở đầu dựa trên `notebooks/02_eda.ipynb`; các phần tiếp theo dùng các mart và nội dung trong `notebooks/04_story.ipynb`. Mỗi story point chứa một dashboard; Phần EDA dùng bố cục bốn hình trên một màn hình, không có khung diễn giải bên phải; các điểm phân tích phía sau hiển thị trong canvas theo chiều cao màn hình. Bố cục desktop được kiểm tra ở 1440 × 900, không cuộn trang. Màn hình hẹp có nút Bộ lọc mở cột điều khiển.

## Chạy

```powershell
./start_story.ps1
```

Mở http://localhost:8502/. Bản độc lập: `docs/spotify_data_story.html`. Bản đồ cần mạng để tải địa giới Plotly; dữ liệu và thư viện vẽ đã nhúng trong HTML.

## Câu chuyện

| Story point | Biểu đồ cùng hiển thị | Câu hỏi |
|---|---|---|
| 1 · Cái nhìn về dữ liệu | Bốn hình tĩnh từ Matplotlib/Seaborn: năm histogram audio; Spearman; phân phối nhãn Train; xu hướng bốn đặc trưng | Mẫu dữ liệu có hình dạng gì, các đặc trưng liên hệ ra sao và thứ hạng ban đầu mang tín hiệu gì? |
| 2 · Hồ sơ âm thanh | Heatmap z-score; boxplot theo thể loại | Hồ sơ âm thanh khác nhau thế nào giữa nhóm hạng và thể loại? |
| 3 · Nghệ sĩ & hợp tác | Tương quan tên tuổi với stream 8 tuần; treemap nghệ sĩ; donut và bar Solo/Collab | Tên tuổi và hợp tác đi cùng thành tích như thế nào? |
| 4 · Bản sắc địa lý và ADN âm nhạc | Bản đồ; radar hai quốc gia | Khác biệt quốc gia có còn rõ khi dùng cùng năm và cách tính? |
| 5 · Chu kỳ thời gian và đại dịch | Thời lượng; cột nhóm 12 tháng; COVID và âm thanh theo tuần | Đâu là xu hướng dài hạn, mùa vụ và đồng biến động trong đại dịch? |

Navy cho cấu trúc, xanh lam/xanh ngọc cho đối chiếu, tím cho quốc gia B và màu ấm cho các nhóm phụ. Luận điểm tự tính theo bộ lọc; lời giải thích nguyên nhân được ghi là giả thuyết.

## Tương tác

- Cái nhìn về dữ liệu: bốn hình cùng xuất hiện trên một màn hình, bấm hình hoặc “Xem lớn” để mở hình đầy đủ, “PNG” tải đúng hình gốc. Hình được nhúng từ output đã lưu trong `02_eda.ipynb`, giữ nguyên màu, trục, KDE và chú giải. Mỗi lần chạy lại EDA cần lưu notebook rồi tải lại dashboard. Phần EDA là hình tĩnh, các điểm phía sau tiếp tục dùng tương tác Plotly.
- Hồ sơ âm thanh và Nghệ sĩ & hợp tác: năm → thể loại → nghệ sĩ, tầng hạng và Solo/Collab. Bấm heatmap chọn đặc trưng/tầng hạng; bấm boxplot chọn thể loại; bấm nhánh treemap rồi nghệ sĩ để lọc chéo. Nút ↑ Gốc trở về toàn bộ thể loại. Bấm donut/bar chọn Solo hoặc Collab. Boxplot có dropdown riêng cho Energy, Danceability, Valence, Tempo.
- Thời lượng mặc định giữ bối cảnh 2017–2022, tô khoảng năm BXH chọn. Lọc thể loại/nghệ sĩ/tầng hạng/biểu diễn chuyển sang trung bình tháng theo stream và đường trung bình 4 tháng; bấm điểm thời gian để chọn năm BXH.
- Bản sắc địa lý: năm → vùng → quốc gia A, chọn quốc gia B và phương pháp trung bình. Bấm quốc gia trên bản đồ cập nhật A trong radar. Bản đồ có Valence, Danceability, Acousticness, Energy; bảng chi tiết đối chiếu đủ 9 chỉ số.
- Chu kỳ thời gian: năm → tháng → tuần. Bấm tháng lọc chuỗi COVID và mở Top bài của tháng. Bấm tuần mở chi tiết 9 đặc trưng. Các đoạn giữa tháng không liên tục được ngắt đường, tránh nối qua thời gian không có dữ liệu.
- Hover hiển thị thông số, đơn vị và ngữ cảnh; zoom/pan, legend theo hỗ trợ của Plotly. Bỏ lựa chọn/Khôi phục point trở về trạng thái đã chụp của point.

## Biên tập và xuất

Biên tập caption, lời dẫn, ghi chú và thứ tự story point. Áp dụng chụp bộ lọc hiện tại; chuyển point khôi phục bộ lọc đã lưu. Nút Lưu giữ workbook v6 trong trình duyệt; JSON dùng để mở lại cấu hình. Workbook v5 được nâng cấp bằng cách thêm điểm mở đầu và giữ nội dung đã biên tập. Các phiên bản cũ hơn chưa hỗ trợ nhập.

HTML xuất story tương tác có dữ liệu và cấu hình; PNG xuất từng biểu đồ; CSV xuất giá trị đang được vẽ. PDF mở hộp thoại in dashboard hiện tại; nếu trình duyệt không hỗ trợ in iframe, mở HTML độc lập để in. Không xuất TWBX.

## Phạm vi và kiểm tra số liệu

Nguồn là các bảng hiện có trong `data/processed`: chart, track dimension, country lookup, COVID và các mart. Notebook và quy trình tiền xử lý không bị sửa.

- Điểm mở đầu dùng 39.190 bài duy nhất, 74 thị trường gồm Global và 290 tuần Global. Spearman Energy–Loudness khoảng 0,690. Đây là mẫu bài từng vào bảng xếp hạng, không đại diện toàn bộ Spotify.
- Cột hạng tuần đầu dùng 2.625 bài Train Global, gồm 622 bài Y=1 (23,70%). Y=1 khi có hạng 1–50 trong tám tuần sau tuần đầu; không tính tuần đầu và chỉ giữ cửa sổ có đủ tám tuần Top 50. Tỷ lệ theo nhóm 1–50, 51–100, 101–150, 151–200 lần lượt là 64,48%, 17,11%, 12,13%, 5,48%. Đây là mô tả trên Train, không phải kết quả mô hình hoặc bằng chứng nhân quả.
- Các dòng nghệ sĩ cùng bài/tuần/thị trường/hạng được bỏ đếm lặp khi tính stream bài hát: 1.787.531 dòng ghi công tương ứng 1.109.375 lần xuất hiện BXH.
- Heatmap là độ lệch trung bình nhóm chia độ lệch chuẩn toàn BXH Global (z-score), không phải ma trận tương quan. Mẫu mặc định 2020–2022; baseline giữ đủ bốn tầng hạng trong cùng bộ lọc.
- Boxplot và donut dùng các bài từng vào BXH Global trong khoảng năm chọn, mỗi bài một lần. Cột Solo/Collab là trung vị tổng stream Global theo bài, chỉ tính các tuần thuộc bộ lọc; hover hiển thị thêm trung bình. Với mặc định 2020–2022, Solo chiếm 58,9% bài trong mẫu; Collab có trung vị khoảng 28,52 triệu/bài, Solo 23,47 triệu/bài, nhưng trung bình lần lượt là 91,23 và 96,18 triệu/bài. Lợi thế ở trung vị gợi ý hợp tác có thể là đòn bẩy chiến lược đáng xem xét, không xác nhận con số gấp ba hoặc khẳng định đây là cách tối ưu nhất để tạo siêu hit. Treemap dùng stream ghi công cho nghệ sĩ, nên không phải thị phần độc quyền.
- Trung bình thời lượng tuần theo năm: 2017 khoảng 218,0 giây; 2020 khoảng 198,5; 2022 khoảng 205,7. Có giảm rồi tăng lại; không kết luận giảm liên tục hay TikTok là nguyên nhân.
- Địa lý có 68 quốc gia năm 2021 và 73 năm 2022. Radar và bản đồ dùng cùng phương pháp: trung bình thường hoặc theo stream. Đặc trưng âm học không tự chứng minh loại nhạc hay tâm lý người nghe.
- Có 289 tuần Global trong 2017–2022, trong đó 130 tuần ghép được với COVID từ 2020 đến 07/2022. Năm 2022 chỉ có 28 tuần. Nhóm tuần tử vong cao/thấp chia theo trung vị trong phạm vi lọc, chỉ là mô tả đồng biến động.
- Bấm tháng 12 hiện các bài Giáng sinh nổi bật: đây là bằng chứng trực tiếp trong danh sách bài để giải thích mùa vụ. Giả thuyết giãn cách, nghe tại nhà, thuật toán hay chữa lành cần dữ liệu bổ sung để kiểm chứng.

## Mã nguồn và xác minh

`eda_data.py` đọc bốn output PNG từ notebook và tính các tóm tắt theo mẫu EDA; `story_data.py` đọc và bỏ đếm lặp dữ liệu; `story_canvas.py` dựng workbook/payload; `story_canvas.html` bố cục; `story_interactions.js` tổng hợp, vẽ và liên kết biểu đồ. Streamlit cache theo thời gian sửa nguồn, notebook và dữ liệu.

```powershell
node --check dashboard/story_interactions.js
node tests/test_story_figures.cjs
python -m compileall -q dashboard/story_app.py dashboard/story_canvas.py dashboard/story_data.py dashboard/eda_data.py
python -c "import sys; sys.path.insert(0,'dashboard'); import story_canvas; from pathlib import Path; Path('docs/spotify_data_story.html').write_text(story_canvas.canvas_html(),encoding='utf-8')"
```

Kiểm tra hình tĩnh đối chiếu từng byte PNG, kích thước và SHA256 với notebook. Kiểm tra các tóm tắt EDA gồm tổng histogram, trung bình/trung vị, 45 cặp tương quan, mẫu Train, lọc chéo và nâng cấp workbook v5. Kiểm tra hồi quy bao gồm stream Collab bỏ đếm lặp, 9 z-score, bộ lọc phân cấp, drill-down thời lượng, cách tính radar thống nhất, lọc tháng và nhóm dữ liệu rỗng. Giao diện kiểm tra trực tiếp gồm chuyển point, boxplot, thể loại/nghệ sĩ, cách tính quốc gia, tháng → COVID → chi tiết tuần.
