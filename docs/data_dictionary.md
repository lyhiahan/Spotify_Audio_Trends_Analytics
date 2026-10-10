# Từ điển dữ liệu Spotify Audio Trends Analytics

Cập nhật ngày **09/10/2026**. Nội dung được đối chiếu trực tiếp với năm file trong `data/raw/`, tám file trong `data/processed/` và mã hiện tại của các notebook. Số dòng không bao gồm dòng tên cột CSV; kiểu CSV là kiểu pandas suy ra khi đọc, không phải schema cố định.

Notebook chuẩn: [01_preprocess](../notebooks/01_preprocess.ipynb), [02_eda](../notebooks/02_eda.ipynb), [03_model](../notebooks/03_model.ipynb), [04_story](../notebooks/04_story.ipynb).

## 1. Phạm vi và quy tắc đọc dữ liệu

- Dữ liệu âm thanh đã nằm trong file chart; pipeline hiện không dùng `songs.csv` để tạo popularity.
- ML hiện dự báo **Global Top 50 trong tám tuần sau tuần đầu quan sát**, không dùng `pop_score` hoặc `is_hit`.
- `ml_tracks`, `ml_market_week_forecast` và `whs_clean.csv` không còn là đầu ra đang dùng trong `data/processed/`. WHR sạch được giữ trong bộ nhớ rồi ghép vào mart quốc gia–năm.
- Chỉ có bài từng xuất hiện trên chart; dữ liệu không đại diện toàn bộ danh mục Spotify.
- Một dòng chart là một credit nghệ sĩ của bài–thị trường–tuần. Trước khi tổng hợp lượt nghe hoặc audio, cần loại lặp về slot.
- Nguồn gốc được notebook/module ghi nhận là Spotify charts, World Bank, Johns Hopkins và World Happiness Report. Repo chưa có manifest xác thực URL tải, ngày tải, phiên bản và giấy phép của từng file; không suy diễn giấy phép bản tải.

## 2. Dữ liệu thô

| File | Dòng | Cột | Thời gian/cấu trúc | Grain |
| --- | --- | --- | --- | --- |
| spotify-weekly-charts.csv | 1,787,999 | 36 | 2016-12-29 đến 2022-07-14 | Credit nghệ sĩ trên chart |
| global_deaths.csv | 1,143 | 290 | 1.142 dòng ngày: 2020-01-23 đến 2023-03-09 | Một dòng metadata tỉnh/bang + các dòng ngày |
| gdp_data.csv | 13,365 | 4 | 1960–2022 | Thực thể–năm |
| country_codes.csv | 217 | 3 | Snapshot metadata; không có cột năm | Mã thực thể |
| whs_years_updated.csv | 1,510 | 46 | 2015–2024 | Quốc gia–ấn bản; khóa thô có trùng |

### 2.1. `spotify-weekly-charts.csv`

File có 73 dòng header lặp trong dữ liệu. Một bài hợp tác có thể có nhiều dòng cùng streams; không cộng các dòng này như các lượt nghe riêng. Kiểu rank/streams/ngày ở file thô cần được chuẩn hóa trước sử dụng.

| Cột thô | Đơn vị/dạng | Ý nghĩa |
| --- | --- | --- |
| `Unnamed: 0` | index | Index xuất CSV; loại khỏi bảng sạch. |
| `uri` | URI | Spotify URI của bài; tách phần cuối thành track_id. |
| `rank` | vị trí | Thứ hạng ở thị trường và tuần tương ứng, 1–200; số nhỏ hơn là hạng cao hơn. |
| `artist_names` | chuỗi | Tên các nghệ sĩ tham gia bài hát theo nguồn. |
| `artists_num` | nghệ sĩ | Số nghệ sĩ được nguồn ghi nhận; không dùng để nhân lượt nghe. |
| `artist_individual` | chuỗi | Tên nghệ sĩ tương ứng artist_id của dòng. |
| `artist_id` | URI | Spotify URI của nghệ sĩ; tách phần cuối thành artist_id sạch. |
| `artist_genre` | nhãn | Thể loại gắn với nghệ sĩ trong nguồn, đã chuẩn hóa; unknown không phải giá trị thiếu pandas. |
| `artist_img` | URL | Ảnh nghệ sĩ; không giữ trong charts_clean. |
| `collab` | cờ nguồn | Thông tin hợp tác của nguồn; không giữ trong charts_clean hiện tại. |
| `track_name` | chuỗi | Tên bài hát; không dùng làm khóa. |
| `release_date` | chuỗi | Ngày phát hành gốc, có thể là YYYY, YYYY-MM hoặc YYYY-MM-DD. |
| `album_num_tracks` | bài | Số bài trong album theo nguồn; không giữ trong charts_clean. |
| `album_cover` | URL | Ảnh bìa; không giữ trong charts_clean. |
| `source` | chuỗi | Metadata nguồn/nhà phát hành trong file; không đủ để xác thực provenance bản tải. |
| `peak_rank` | vị trí | Hạng tốt nhất nguồn ghi nhận tính đến dòng hiện tại; không dùng làm X tuần đầu mặc định. |
| `previous_rank` | vị trí/thiếu | Hạng tuần trước; −1 và giá trị thiếu nguồn được chuyển thành NA. |
| `weeks_on_chart` | tuần | Số tuần trên chart do nguồn ghi nhận đến dòng hiện tại. |
| `streams` | lượt nghe | Streams được ghi nhận trên chart của bài ở đúng thị trường–tuần; lặp trên các dòng credit nghệ sĩ. |
| `week` | ngày | Mốc tuần trong nguồn; chart hiện đều là thứ Năm. Pipeline coi đây là ngày kết thúc tuần khi ghép COVID, chưa xác minh lịch công bố nguồn. |
| `danceability` | 0–1 | Mức độ phù hợp để nhảy theo nhịp của bản thu. |
| `energy` | 0–1 | Cường độ và mức hoạt động cảm nhận của âm thanh. |
| `key` | mã tông 0–11 | Pitch class của tông nhạc; 0=C, 1=C♯, …, 11=B. Đây là biến phân loại. |
| `mode` | 0/1 | 0: giọng thứ; 1: giọng trưởng. |
| `loudness` | dB | Mức loudness của bản thu; snapshot hiện có giá trị từ −41,41 đến +1,906 dB. |
| `speechiness` | 0–1 | Mức hiện diện của lời nói trong âm thanh; không tự xác định thể loại Rap. |
| `acousticness` | 0–1 | Chỉ số ước lượng tính acoustic của bản thu; không phải tỷ lệ nhạc cụ mộc. |
| `instrumentalness` | 0–1 | Chỉ số ước lượng mức không có giọng hát. |
| `liveness` | 0–1 | Chỉ số ước lượng dấu hiệu khán giả/biểu diễn trực tiếp. |
| `valence` | 0–1 | Sắc thái tích cực cảm nhận của âm thanh; không đo hạnh phúc của người nghe. |
| `tempo` | BPM | Nhịp độ ước lượng, tính bằng nhịp/phút. |
| `duration` | ms | Thời lượng bản thu; đổi sang phút bằng duration/60000. |
| `country` | thị trường | Tên thị trường chart; Global là thị trường riêng, không phải quốc gia. |
| `region` | nhãn | Metadata vùng từ nguồn chart, khác wb_region. |
| `language` | nhãn | Metadata ngôn ngữ từ nguồn chart; không xác nhận ngôn ngữ của từng bài. |
| `pivot` | trường kỹ thuật | Trường của nguồn, không giữ trong bảng sạch. |

### 2.2. `global_deaths.csv`

File trong repo đã được chuyển vị và chứa **số tử vong phát sinh theo ngày**. Không phải bảng gốc có ngày ở các cột, và không lấy sai phân thêm lần nữa.

| Trường/cấu trúc | Ý nghĩa |
| --- | --- |
| `Country/Region` | Dòng đầu có chữ Province/State; các dòng sau là ngày dạng M/D/YY. |
| Các cột thực thể như `Afghanistan`, `Australia.1`, `China.12` | Cột quốc gia hoặc tỉnh/bang; hậu tố .1, .2 do tên lặp khi đọc CSV, không phải mã địa lý. |
| Dòng metadata đầu tiên | Chứa tên tỉnh/bang tương ứng từng cột; không phải một ngày quan sát. |
| Giá trị từ dòng ngày | Số tử vong mới báo cáo; số âm là điều chỉnh nguồn và được giữ trong tổng. |

Pipeline hiện ánh xạ Hong Kong bằng tên cột `China.12`, gộp các tỉnh về quốc gia rồi cộng tuần. Giá trị không chuyển được sang số được điền 0 trong notebook hiện tại; đây là quy tắc xử lý đang có, không chứng minh nguồn không thiếu.

### 2.3. `gdp_data.csv`

| Cột | Ý nghĩa |
| --- | --- |
| `country_name` | Tên quốc gia hoặc nhóm tổng hợp kinh tế. |
| `country_code` | Mã thực thể; gồm cả mã nhóm như thế giới/khu vực. |
| `year` | Năm ghi nhận. |
| `value` | Giá trị GDP nguồn. Notebook đặt tên làm việc gdp_usd, nhưng file không kèm mã chỉ tiêu/đơn vị để xác thực snapshot. |

GDP hiện phục vụ kiểm tra join trong 01_preprocess; không có cột GDP tổng trong mart_country_year được lưu. `gdp_factor` trong WHR là biến khác.

### 2.4. `country_codes.csv`

| Cột | Ý nghĩa |
| --- | --- |
| `country_code` | Mã ba ký tự làm khóa metadata. |
| `region` | Vùng World Bank, chuyển thành wb_region trong bảng sạch. |
| `income_group` | Nhóm thu nhập, chuyển thành wb_income_group trong bảng sạch. |

### 2.5. `whs_years_updated.csv`

File hợp nhất nhiều ấn bản nên có nhiều tên cột cho cùng nhóm chỉ tiêu; một số cột chỉ có dữ liệu ở một số năm. Các giá trị thiếu do khác schema năm không được coi ngay là lỗi.

| Cột/nhóm cột | Ý nghĩa |
| --- | --- |
| `Country`, `Year`, `Score` | Tên quốc gia, năm ấn bản và điểm hạnh phúc được dùng làm trường chuẩn. |
| `Happiness Rank`, `Happiness.Rank`, `Overall rank`, `RANK` | Các cột thứ hạng từ các ấn bản. |
| `Region`, `Regional indicator` | Metadata khu vực theo báo cáo. |
| Các cột Economy/GDP/Explained by… | Thông tin kinh tế hoặc thành phần giải thích điểm; thang đo tùy ấn bản. |
| Family/Social support; Health/Healthy life; Freedom; Generosity; Trust/Perceptions of corruption | Các nhóm nhân tố được hợp nhất thành sáu cột trong mart. |
| Standard Error/Confidence Interval/Whisker | Thông tin độ bất định của nguồn; không giữ trong mart hiện tại. |
| Dystopia/Residual | Thành phần nền/phần dư của báo cáo; không giữ trong mart hiện tại. |

Notebook đổi dòng Cyprus 2022 có Score < 6 thành North Cyprus để giải quyết khóa trùng. Đây là quy tắc của code hiện tại, không phải xác nhận tên gốc từ tài liệu nguồn.

## 3. Các file xử lý hiện có

| File | Dòng | Cột | Grain/khóa | Sử dụng |
| --- | --- | --- | --- | --- |
| charts_clean.parquet | 1,787,531 | 35 | track_id, artist_id, chart_country, week | Nguồn chart sạch cho EDA/model/story |
| tracks_dimension.csv | 39,190 | 21 | track_id | Phân phối audio cấp bài |
| country_lookup.csv | 73 | 8 | chart_country | Ánh xạ quốc gia |
| covid_weekly_clean.csv | 12,136 | 4 | country, week | Đối chiếu dịch tễ |
| mart_audio_trend_weekly.parquet | 5,548 | 29 | chart_country, week | Xu hướng và mùa vụ |
| mart_artist_chart.parquet | 15,254 | 10 | artist_id | Nghệ sĩ trong dashboard |
| mart_country_year.parquet | 141 | 42 | chart_country, year | Hồ sơ quốc gia và WHR |
| mart_artist_chart.csv | 15,254 | 16 | artist_id | Bản mở rộng cũ, không tương đương schema Parquet |

Kiểu `str`/`object` và độ phân giải datetime có thể khác theo phiên bản pandas. Kiểu trong bảng dưới là kết quả đọc tại lần đối chiếu này.

### 3.1. Quy ước audio và tổng hợp

| Đặc trưng | Đơn vị | Ý nghĩa |
| --- | --- | --- |
| `danceability` | 0–1 | Mức độ phù hợp để nhảy theo nhịp của bản thu. |
| `energy` | 0–1 | Cường độ và mức hoạt động cảm nhận của âm thanh. |
| `key` | mã tông 0–11 | Pitch class của tông nhạc; 0=C, 1=C♯, …, 11=B. Đây là biến phân loại. |
| `mode` | 0/1 | 0: giọng thứ; 1: giọng trưởng. |
| `loudness` | dB | Mức loudness của bản thu; snapshot hiện có giá trị từ −41,41 đến +1,906 dB. |
| `speechiness` | 0–1 | Mức hiện diện của lời nói trong âm thanh; không tự xác định thể loại Rap. |
| `acousticness` | 0–1 | Chỉ số ước lượng tính acoustic của bản thu; không phải tỷ lệ nhạc cụ mộc. |
| `instrumentalness` | 0–1 | Chỉ số ước lượng mức không có giọng hát. |
| `liveness` | 0–1 | Chỉ số ước lượng dấu hiệu khán giả/biểu diễn trực tiếp. |
| `valence` | 0–1 | Sắc thái tích cực cảm nhận của âm thanh; không đo hạnh phúc của người nghe. |
| `tempo` | BPM | Nhịp độ ước lượng, tính bằng nhịp/phút. |
| `duration` | ms | Thời lượng bản thu; đổi sang phút bằng duration/60000. |

Với một nhóm G gồm các slot đã loại lặp nghệ sĩ:

- `{feature}_mean = mean(feature)` trên các slot của nhóm.
- `{feature}_weighted = sum(feature × streams) / sum(streams)`; nếu tổng streams bằng 0, dùng mean.
- Mart năm tính trực tiếp từ toàn bộ slot trong quốc gia–năm, không phải trung bình đơn giản của các mart tuần.
- `mode_mean` là tỷ trọng slot giọng trưởng; `mode_weighted` là tỷ trọng theo streams.
- `key_mean` và `key_weighted` đang tồn tại trong file, nhưng không có diễn giải trung bình tông nhạc đáng tin cậy. Không dùng hai cột này để kết luận âm nhạc; nên dùng phân phối/tỷ trọng tông.

### 3.2. `charts_clean.parquet`

Khóa: `track_id`, `artist_id`, `chart_country`, `week`.


| Cột | Kiểu đọc | Đơn vị | Thiếu | Ý nghĩa |
| --- | --- | --- | --- | --- |
| `track_id` | str | ID | 0 | ID bài Spotify sau khi bỏ tiền tố URI. |
| `track_name` | str | chuỗi | 0 | Tên bài hát; không dùng làm khóa. |
| `artist_id` | str | ID | 0 | ID nghệ sĩ của dòng credit. Trong tracks_dimension là dòng đầu được giữ, không xác nhận nghệ sĩ chính. |
| `artist_names` | str | chuỗi | 0 | Tên các nghệ sĩ tham gia bài hát theo nguồn. |
| `artist_individual` | str | chuỗi | 0 | Tên nghệ sĩ tương ứng artist_id của dòng. |
| `artists_num` | int16 | nghệ sĩ | 0 | Số nghệ sĩ được nguồn ghi nhận; không dùng để nhân lượt nghe. |
| `artist_genre` | category | nhãn | 0 | Thể loại gắn với nghệ sĩ trong nguồn, đã chuẩn hóa; unknown không phải giá trị thiếu pandas. |
| `week` | datetime64[us] | ngày | 0 | Mốc tuần trong nguồn; chart hiện đều là thứ Năm. Pipeline coi đây là ngày kết thúc tuần khi ghép COVID, chưa xác minh lịch công bố nguồn. |
| `year` | int32 | năm | 0 | Năm của week trong chart/mart; năm ấn bản khi đi cùng dữ liệu WHR. |
| `month` | int32 | tháng | 0 | Tháng của week, 1–12. |
| `chart_country` | category | thị trường | 0 | Tên thị trường chart; Global là thị trường riêng, không phải quốc gia. |
| `chart_region` | category | nhãn | 0 | Metadata vùng từ nguồn chart, khác wb_region. |
| `chart_language` | category | nhãn | 0 | Metadata ngôn ngữ từ nguồn chart; không xác nhận ngôn ngữ của từng bài. |
| `rank` | int32 | vị trí | 0 | Thứ hạng ở thị trường và tuần tương ứng, 1–200; số nhỏ hơn là hạng cao hơn. |
| `previous_rank` | Int16 | vị trí/thiếu | 167,519 | Hạng tuần trước; −1 và giá trị thiếu nguồn được chuyển thành NA. |
| `is_new_entry` | bool | bool | 0 | True nếu previous_rank nguồn là −1 hoặc thiếu; không xác nhận lần xuất hiện đầu trong toàn bộ lịch sử. |
| `peak_rank` | int32 | vị trí | 0 | Hạng tốt nhất nguồn ghi nhận tính đến dòng hiện tại; không dùng làm X tuần đầu mặc định. |
| `weeks_on_chart` | int32 | tuần | 0 | Số tuần trên chart do nguồn ghi nhận đến dòng hiện tại. |
| `streams` | int64 | lượt nghe | 0 | Streams được ghi nhận trên chart của bài ở đúng thị trường–tuần; lặp trên các dòng credit nghệ sĩ. |
| `release_date` | str | chuỗi | 0 | Ngày phát hành gốc, có thể là YYYY, YYYY-MM hoặc YYYY-MM-DD. |
| `release_date_clean` | datetime64[us] | ngày | 0 | Ngày phát hành sau parse; độ chính xác có thể bị giảm vì chuỗi gốc chỉ có năm/tháng. |
| `release_year` | Int64 | năm | 0 | Năm lấy từ release_date_clean. |
| `days_to_chart` | int64 | ngày | 0 | (week − release_date_clean).days của dòng hiện tại; có giá trị âm và có thể dựa trên ngày suy ra từ chuỗi thiếu độ chính xác. |
| `danceability` | float32 | 0–1 | 0 | Mức độ phù hợp để nhảy theo nhịp của bản thu. |
| `energy` | float32 | 0–1 | 0 | Cường độ và mức hoạt động cảm nhận của âm thanh. |
| `key` | Int8 | mã tông 0–11 | 0 | Pitch class của tông nhạc; 0=C, 1=C♯, …, 11=B. Đây là biến phân loại. |
| `mode` | Int8 | 0/1 | 0 | 0: giọng thứ; 1: giọng trưởng. |
| `loudness` | float32 | dB | 0 | Mức loudness của bản thu; snapshot hiện có giá trị từ −41,41 đến +1,906 dB. |
| `speechiness` | float32 | 0–1 | 0 | Mức hiện diện của lời nói trong âm thanh; không tự xác định thể loại Rap. |
| `acousticness` | float32 | 0–1 | 0 | Chỉ số ước lượng tính acoustic của bản thu; không phải tỷ lệ nhạc cụ mộc. |
| `instrumentalness` | float32 | 0–1 | 0 | Chỉ số ước lượng mức không có giọng hát. |
| `liveness` | float32 | 0–1 | 0 | Chỉ số ước lượng dấu hiệu khán giả/biểu diễn trực tiếp. |
| `valence` | float32 | 0–1 | 0 | Sắc thái tích cực cảm nhận của âm thanh; không đo hạnh phúc của người nghe. |
| `tempo` | float32 | BPM | 0 | Nhịp độ ước lượng, tính bằng nhịp/phút. |
| `duration` | float32 | ms | 0 | Thời lượng bản thu; đổi sang phút bằng duration/60000. |

### 3.3. `tracks_dimension.csv`

Khóa: `track_id`.


| Cột | Kiểu đọc | Đơn vị | Thiếu | Ý nghĩa |
| --- | --- | --- | --- | --- |
| `track_id` | str | ID | 0 | ID bài Spotify sau khi bỏ tiền tố URI. |
| `track_name` | str | chuỗi | 0 | Tên bài hát; không dùng làm khóa. |
| `artist_id` | str | ID | 0 | ID nghệ sĩ của dòng credit. Trong tracks_dimension là dòng đầu được giữ, không xác nhận nghệ sĩ chính. |
| `artist_names` | str | chuỗi | 0 | Tên các nghệ sĩ tham gia bài hát theo nguồn. |
| `artists_num` | int64 | nghệ sĩ | 0 | Số nghệ sĩ được nguồn ghi nhận; không dùng để nhân lượt nghe. |
| `artist_genre` | str | nhãn | 0 | Thể loại gắn với nghệ sĩ trong nguồn, đã chuẩn hóa; unknown không phải giá trị thiếu pandas. |
| `release_date` | str | chuỗi | 0 | Ngày phát hành gốc, có thể là YYYY, YYYY-MM hoặc YYYY-MM-DD. |
| `release_date_clean` | str | ngày | 0 | Ngày phát hành sau parse; độ chính xác có thể bị giảm vì chuỗi gốc chỉ có năm/tháng. |
| `release_year` | int64 | năm | 0 | Năm lấy từ release_date_clean. |
| `danceability` | float64 | 0–1 | 0 | Mức độ phù hợp để nhảy theo nhịp của bản thu. |
| `energy` | float64 | 0–1 | 0 | Cường độ và mức hoạt động cảm nhận của âm thanh. |
| `key` | int64 | mã tông 0–11 | 0 | Pitch class của tông nhạc; 0=C, 1=C♯, …, 11=B. Đây là biến phân loại. |
| `mode` | int64 | 0/1 | 0 | 0: giọng thứ; 1: giọng trưởng. |
| `loudness` | float64 | dB | 0 | Mức loudness của bản thu; snapshot hiện có giá trị từ −41,41 đến +1,906 dB. |
| `speechiness` | float64 | 0–1 | 0 | Mức hiện diện của lời nói trong âm thanh; không tự xác định thể loại Rap. |
| `acousticness` | float64 | 0–1 | 0 | Chỉ số ước lượng tính acoustic của bản thu; không phải tỷ lệ nhạc cụ mộc. |
| `instrumentalness` | float64 | 0–1 | 0 | Chỉ số ước lượng mức không có giọng hát. |
| `liveness` | float64 | 0–1 | 0 | Chỉ số ước lượng dấu hiệu khán giả/biểu diễn trực tiếp. |
| `valence` | float64 | 0–1 | 0 | Sắc thái tích cực cảm nhận của âm thanh; không đo hạnh phúc của người nghe. |
| `tempo` | float64 | BPM | 0 | Nhịp độ ước lượng, tính bằng nhịp/phút. |
| `duration` | float64 | ms | 0 | Thời lượng bản thu; đổi sang phút bằng duration/60000. |

### 3.4. `country_lookup.csv`

Khóa: `chart_country`.


| Cột | Kiểu đọc | Đơn vị | Thiếu | Ý nghĩa |
| --- | --- | --- | --- | --- |
| `chart_country` | str | thị trường | 0 | Tên thị trường chart; Global là thị trường riêng, không phải quốc gia. |
| `country_code` | str | mã | 0 | Mã ba ký tự trong dữ liệu World Bank; nguồn GDP còn có mã nhóm tổng hợp, không phải tất cả đều là quốc gia ISO. |
| `wb_country_name` | str | chuỗi | 0 | Tên được lookup ánh xạ theo metadata World Bank; Taiwan được bổ sung thủ công trong notebook. |
| `wb_region` | str | nhãn | 0 | Nhóm vùng World Bank dùng để phân nhóm trong phân tích. |
| `wb_income_group` | str | nhãn | 0 | Nhóm thu nhập theo snapshot metadata, không có phiên bản theo từng năm. |
| `chart_region` | str | nhãn | 0 | Metadata vùng từ nguồn chart, khác wb_region. |
| `chart_language` | str | nhãn | 0 | Metadata ngôn ngữ từ nguồn chart; không xác nhận ngôn ngữ của từng bài. |
| `n_weeks` | int64 | tuần | 0 | Số tuần quan sát của bảng tương ứng; ở lookup là toàn nguồn, ở mart quốc gia-năm là trong năm. |

### 3.5. `covid_weekly_clean.csv`

Khóa: `country`, `week`.


| Cột | Kiểu đọc | Đơn vị | Thiếu | Ý nghĩa |
| --- | --- | --- | --- | --- |
| `country` | str | thực thể | 0 | Tên quốc gia/thực thể COVID đã ánh xạ; có Global. |
| `week` | str | ngày | 0 | Mốc tuần trong nguồn; chart hiện đều là thứ Năm. Pipeline coi đây là ngày kết thúc tuần khi ghép COVID, chưa xác minh lịch công bố nguồn. |
| `weekly_deaths` | int64 | ca/tuần | 0 | Tổng số tử vong báo cáo theo ngày từ thứ Sáu đến thứ Năm; có thể âm do điều chỉnh nguồn. |
| `cumulative_deaths` | int64 | ca | 0 | Tổng lũy kế weekly_deaths theo thực thể từ đầu chuỗi đang có. |

### 3.6. `mart_audio_trend_weekly.parquet`

Khóa: `chart_country`, `week`.


| Cột | Kiểu đọc | Đơn vị | Thiếu | Ý nghĩa |
| --- | --- | --- | --- | --- |
| `chart_country` | category | thị trường | 0 | Tên thị trường chart; Global là thị trường riêng, không phải quốc gia. |
| `week` | datetime64[us] | ngày | 0 | Mốc tuần trong nguồn; chart hiện đều là thứ Năm. Pipeline coi đây là ngày kết thúc tuần khi ghép COVID, chưa xác minh lịch công bố nguồn. |
| `total_streams` | float64 | lượt nghe | 0 | Tổng streams các slot trong thị trường–tuần; không cộng Global với các quốc gia để diễn giải tổng Spotify. |
| `track_count` | float64 | slot | 0 | len(g) sau loại lặp nghệ sĩ trong mart tuần; bằng số vị trí được giữ, không phải số bài mới. |
| `new_entries` | float64 | slot | 0 | Tổng is_new_entry sau loại lặp nghệ sĩ của nhóm tuần. |
| `danceability_mean` | float64 | 0–1 | 0 | Trung bình danceability trên slot của nhóm; xem quy tắc tại mục 3.1. |
| `danceability_weighted` | float64 | 0–1 | 0 | Trung bình danceability có trọng số streams; xem quy tắc tại mục 3.1. |
| `energy_mean` | float64 | 0–1 | 0 | Trung bình energy trên slot của nhóm; xem quy tắc tại mục 3.1. |
| `energy_weighted` | float64 | 0–1 | 0 | Trung bình energy có trọng số streams; xem quy tắc tại mục 3.1. |
| `key_mean` | float64 | mã tông 0–11 | 0 | Trung bình key trên slot của nhóm; xem quy tắc tại mục 3.1. |
| `key_weighted` | float64 | mã tông 0–11 | 0 | Trung bình key có trọng số streams; xem quy tắc tại mục 3.1. |
| `mode_mean` | float64 | 0/1 | 0 | Trung bình mode trên slot của nhóm; xem quy tắc tại mục 3.1. |
| `mode_weighted` | float64 | 0/1 | 0 | Trung bình mode có trọng số streams; xem quy tắc tại mục 3.1. |
| `loudness_mean` | float64 | dB | 0 | Trung bình loudness trên slot của nhóm; xem quy tắc tại mục 3.1. |
| `loudness_weighted` | float64 | dB | 0 | Trung bình loudness có trọng số streams; xem quy tắc tại mục 3.1. |
| `speechiness_mean` | float64 | 0–1 | 0 | Trung bình speechiness trên slot của nhóm; xem quy tắc tại mục 3.1. |
| `speechiness_weighted` | float64 | 0–1 | 0 | Trung bình speechiness có trọng số streams; xem quy tắc tại mục 3.1. |
| `acousticness_mean` | float64 | 0–1 | 0 | Trung bình acousticness trên slot của nhóm; xem quy tắc tại mục 3.1. |
| `acousticness_weighted` | float64 | 0–1 | 0 | Trung bình acousticness có trọng số streams; xem quy tắc tại mục 3.1. |
| `instrumentalness_mean` | float64 | 0–1 | 0 | Trung bình instrumentalness trên slot của nhóm; xem quy tắc tại mục 3.1. |
| `instrumentalness_weighted` | float64 | 0–1 | 0 | Trung bình instrumentalness có trọng số streams; xem quy tắc tại mục 3.1. |
| `liveness_mean` | float64 | 0–1 | 0 | Trung bình liveness trên slot của nhóm; xem quy tắc tại mục 3.1. |
| `liveness_weighted` | float64 | 0–1 | 0 | Trung bình liveness có trọng số streams; xem quy tắc tại mục 3.1. |
| `valence_mean` | float64 | 0–1 | 0 | Trung bình valence trên slot của nhóm; xem quy tắc tại mục 3.1. |
| `valence_weighted` | float64 | 0–1 | 0 | Trung bình valence có trọng số streams; xem quy tắc tại mục 3.1. |
| `tempo_mean` | float64 | BPM | 0 | Trung bình tempo trên slot của nhóm; xem quy tắc tại mục 3.1. |
| `tempo_weighted` | float64 | BPM | 0 | Trung bình tempo có trọng số streams; xem quy tắc tại mục 3.1. |
| `duration_mean` | float64 | ms | 0 | Trung bình duration trên slot của nhóm; xem quy tắc tại mục 3.1. |
| `duration_weighted` | float64 | ms | 0 | Trung bình duration có trọng số streams; xem quy tắc tại mục 3.1. |

### 3.7. `mart_artist_chart.parquet`

Khóa: `artist_id`.


| Cột | Kiểu đọc | Đơn vị | Thiếu | Ý nghĩa |
| --- | --- | --- | --- | --- |
| `artist_id` | str | ID | 0 | ID nghệ sĩ của dòng credit. Trong tracks_dimension là dòng đầu được giữ, không xác nhận nghệ sĩ chính. |
| `artist_name` | str | chuỗi | 0 | Tên artist_individual đầu tiên của artist_id trong dữ liệu sạch. |
| `artist_genre` | category | nhãn | 0 | Thể loại gắn với nghệ sĩ trong nguồn, đã chuẩn hóa; unknown không phải giá trị thiếu pandas. |
| `n_chart_tracks` | int64 | bài | 0 | Số track_id khác nhau của nghệ sĩ trong mọi thị trường đang có. |
| `global_streams` | int64 | lượt nghe credit | 0 | Streams các dòng credit của nghệ sĩ ở Global; full credit cho từng nghệ sĩ hợp tác. |
| `global_peak_rank` | int64 | vị trí | 0 | Hạng thấp nhất theo số ở Global; −1 nếu nghệ sĩ không có dòng Global. |
| `global_weeks_on_chart` | int64 | tuần | 0 | Số ngày week khác nhau nghệ sĩ xuất hiện ở Global; 0 nếu không có. |
| `country_streams` | int64 | lượt nghe credit | 0 | Streams các dòng credit của nghệ sĩ ở các quốc gia; tách khỏi Global. |
| `country_peak_rank` | int64 | vị trí | 0 | Hạng thấp nhất theo số ở các quốc gia; −1 nếu không có dòng quốc gia. |
| `country_weeks_on_chart` | int64 | tuần | 0 | Số ngày week khác nhau nghệ sĩ xuất hiện ở ít nhất một quốc gia; không phải số cặp quốc gia–tuần. |

### 3.8. `mart_country_year.parquet`

Khóa: `chart_country`, `year`.


| Cột | Kiểu đọc | Đơn vị | Thiếu | Ý nghĩa |
| --- | --- | --- | --- | --- |
| `chart_country` | str | thị trường | 0 | Tên thị trường chart; Global là thị trường riêng, không phải quốc gia. |
| `year` | int32 | năm | 0 | Năm của week trong chart/mart; năm ấn bản khi đi cùng dữ liệu WHR. |
| `yearly_streams` | float64 | lượt nghe | 0 | Tổng streams các slot trong đúng quốc gia–năm. |
| `slot_count` | float64 | slot | 0 | Số slot chart được giữ trong quốc gia–năm; một bài nhiều tuần đóng góp nhiều slot. |
| `n_weeks` | float64 | tuần | 0 | Số tuần quan sát của bảng tương ứng; ở lookup là toàn nguồn, ở mart quốc gia-năm là trong năm. |
| `danceability_mean` | float64 | 0–1 | 0 | Trung bình danceability trên slot của nhóm; xem quy tắc tại mục 3.1. |
| `danceability_weighted` | float64 | 0–1 | 0 | Trung bình danceability có trọng số streams; xem quy tắc tại mục 3.1. |
| `energy_mean` | float64 | 0–1 | 0 | Trung bình energy trên slot của nhóm; xem quy tắc tại mục 3.1. |
| `energy_weighted` | float64 | 0–1 | 0 | Trung bình energy có trọng số streams; xem quy tắc tại mục 3.1. |
| `key_mean` | float64 | mã tông 0–11 | 0 | Trung bình key trên slot của nhóm; xem quy tắc tại mục 3.1. |
| `key_weighted` | float64 | mã tông 0–11 | 0 | Trung bình key có trọng số streams; xem quy tắc tại mục 3.1. |
| `mode_mean` | float64 | 0/1 | 0 | Trung bình mode trên slot của nhóm; xem quy tắc tại mục 3.1. |
| `mode_weighted` | float64 | 0/1 | 0 | Trung bình mode có trọng số streams; xem quy tắc tại mục 3.1. |
| `loudness_mean` | float64 | dB | 0 | Trung bình loudness trên slot của nhóm; xem quy tắc tại mục 3.1. |
| `loudness_weighted` | float64 | dB | 0 | Trung bình loudness có trọng số streams; xem quy tắc tại mục 3.1. |
| `speechiness_mean` | float64 | 0–1 | 0 | Trung bình speechiness trên slot của nhóm; xem quy tắc tại mục 3.1. |
| `speechiness_weighted` | float64 | 0–1 | 0 | Trung bình speechiness có trọng số streams; xem quy tắc tại mục 3.1. |
| `acousticness_mean` | float64 | 0–1 | 0 | Trung bình acousticness trên slot của nhóm; xem quy tắc tại mục 3.1. |
| `acousticness_weighted` | float64 | 0–1 | 0 | Trung bình acousticness có trọng số streams; xem quy tắc tại mục 3.1. |
| `instrumentalness_mean` | float64 | 0–1 | 0 | Trung bình instrumentalness trên slot của nhóm; xem quy tắc tại mục 3.1. |
| `instrumentalness_weighted` | float64 | 0–1 | 0 | Trung bình instrumentalness có trọng số streams; xem quy tắc tại mục 3.1. |
| `liveness_mean` | float64 | 0–1 | 0 | Trung bình liveness trên slot của nhóm; xem quy tắc tại mục 3.1. |
| `liveness_weighted` | float64 | 0–1 | 0 | Trung bình liveness có trọng số streams; xem quy tắc tại mục 3.1. |
| `valence_mean` | float64 | 0–1 | 0 | Trung bình valence trên slot của nhóm; xem quy tắc tại mục 3.1. |
| `valence_weighted` | float64 | 0–1 | 0 | Trung bình valence có trọng số streams; xem quy tắc tại mục 3.1. |
| `tempo_mean` | float64 | BPM | 0 | Trung bình tempo trên slot của nhóm; xem quy tắc tại mục 3.1. |
| `tempo_weighted` | float64 | BPM | 0 | Trung bình tempo có trọng số streams; xem quy tắc tại mục 3.1. |
| `duration_mean` | float64 | ms | 0 | Trung bình duration trên slot của nhóm; xem quy tắc tại mục 3.1. |
| `duration_weighted` | float64 | ms | 0 | Trung bình duration có trọng số streams; xem quy tắc tại mục 3.1. |
| `country_code` | str | mã | 0 | Mã ba ký tự trong dữ liệu World Bank; nguồn GDP còn có mã nhóm tổng hợp, không phải tất cả đều là quốc gia ISO. |
| `wb_region` | str | nhãn | 0 | Nhóm vùng World Bank dùng để phân nhóm trong phân tích. |
| `wb_income_group` | str | nhãn | 0 | Nhóm thu nhập theo snapshot metadata, không có phiên bản theo từng năm. |
| `chart_region` | category | nhãn | 0 | Metadata vùng từ nguồn chart, khác wb_region. |
| `chart_language` | category | nhãn | 0 | Metadata ngôn ngữ từ nguồn chart; không xác nhận ngôn ngữ của từng bài. |
| `happiness_rank` | int64 | hạng | 0 | Hạng hạnh phúc được hợp nhất từ các cột thứ hạng của các ấn bản WHR. |
| `happiness_score` | float64 | 0–10 | 0 | Điểm đánh giá cuộc sống trong ấn bản WHR; không phải cảm xúc âm nhạc. |
| `gdp_factor` | float64 | thang nguồn WHR | 0 | Thành phần kinh tế trong WHR, không phải GDP tổng USD; các năm có thể dùng cột/thang khác nhau. |
| `social_support` | float64 | thang nguồn WHR | 0 | Thành phần hỗ trợ xã hội đã hợp nhất từ các ấn bản; cần đối chiếu thang trước khi so sánh năm. |
| `healthy_life` | float64 | thang nguồn WHR | 0 | Thành phần sức khỏe/tuổi thọ trong WHR; không mặc định là số năm sống. |
| `freedom` | float64 | thang nguồn WHR | 0 | Thành phần tự do lựa chọn trong WHR. |
| `generosity` | float64 | thang nguồn WHR | 0 | Thành phần lòng rộng lượng trong WHR. |
| `corruption` | float64 | thang nguồn WHR | 0 | Thành phần nhận thức về tham nhũng trong WHR. |

### 3.9. `mart_artist_chart.csv`: bản mở rộng cũ

File hiện có 15.254 dòng và **16 cột**, trong khi Parquet có 10 cột. Dashboard hiện đọc Parquet. Sáu cột bổ sung là `n_global_tracks`, `stream_points`, `track_points`, `week_points`, `rank_points`, `artist_popularity`. Các cột điểm là chỉ số tự tính của nhánh cũ, không phải popularity Spotify; notebook 01 hiện không tái tạo chúng. Không coi hai file là hai định dạng tương đương và không dùng các điểm này làm nhãn ML hiện tại.

## 4. Cohort và nhãn dự báo trong `03_model.ipynb`

Cohort được tạo trong bộ nhớ từ chart Global. Không có file ml_tracks mới trong data/processed. Một mẫu là **một track_id tại tuần đầu quan sát trong nguồn Global**.


### 4.1. Công thức nhãn

`hit_next_8_weeks = 1` nếu tồn tại k thuộc {1,…,8} sao cho bài có rank 1–50 ở Global tại `first_chart_week + 7k ngày`; bằng 0 nếu không có sự kiện đó và cửa sổ đủ điều kiện. Tuần đầu t0 không tính vào nhãn.

Chỉ có nhãn khi cả tám tuần tương lai đều đủ 50 hạng Top 50. Bài ở tuần đầu toàn nguồn bị loại khỏi mẫu học; cửa sổ ra ngoài biên cuối hoặc thiếu Top 50 không được coi là nhãn âm. Nếu bài đã ở Top 50 tại t0, Y=1 vẫn cần xuất hiện lại ở một tuần sau. Nhãn đo cả duy trì và bứt phá, không chỉ bứt phá từ hạng >50.


### 4.2. Các trường tạo thêm

| Cột | Kiểu | Đơn vị | Vai trò | Ý nghĩa |
| --- | --- | --- | --- | --- |
| `first_chart_week` | datetime64[us] | ngày | id/time | Tuần đầu quan sát trong nguồn, không xác nhận lần đầu toàn lịch sử. |
| `rank_first_week` | int32 | 1–200 | feature | rank tại t0. |
| `streams_first_week` | int64 | lượt nghe | feature/provenance | streams Global tại t0; giá trị gốc dùng tạo log. |
| `log_streams_first_week` | float64 | log tự nhiên | feature | ln(1 + streams_first_week). |
| `duration_min` | float32 | phút | feature | duration/60000. |
| `label_window_end` | datetime64[us] | ngày | outcome_audit | first_chart_week + 56 ngày. |
| `has_valid_label` | bool | bool | outcome_audit | Đủ tám tuần Top 50 để quan sát nhãn. |
| `hit_next_8_weeks` | Int8 | 0/1/NA | outcome | Nhãn theo mục 4.1. |
| `is_left_censored` | bool | bool | provenance | t0 trùng tuần đầu nguồn; không vào mẫu học. |
| `is_right_censored` | bool | bool | outcome_audit | Cửa sổ kết thúc sau tuần cuối nguồn. |
| `label_status` | str | nhãn | outcome_audit | valid, right_censored hoặc incomplete_future_top50; xét riêng cờ biên trái. |
| `eligible_for_model` | bool | bool | outcome_audit | has_valid_label và không ở biên trái. |
| `split_group` | str | nhãn | split_audit | train/validation/test, nhóm purge, unlabeled hoặc excluded_left_boundary. |

### 4.3. Tập đầu vào và chia thời gian

X gồm 10 audio liên tục (`danceability`, `energy`, `loudness`, `speechiness`, `acousticness`, `instrumentalness`, `liveness`, `valence`, `tempo`, `duration_min`) cùng `rank_first_week`, `log_streams_first_week`. Không có key/mode, popularity, tổng streams cả lịch sử, WHR hay COVID trong X hiện tại.

Các cột rank, streams, week, tên bài của dòng đầu có thể còn nằm trong cohort để truy vết; không mặc định mọi cột của cohort là feature. Imputer và scaler được fit trên Train.


| Tập | Bài | Y=1 | Tỷ lệ Y=1 | t0 đầu | t0 cuối |
| --- | --- | --- | --- | --- | --- |
| train | 2,625 | 622 | 23.70% | 2017-01-05 | 2020-01-02 |
| validation | 840 | 181 | 21.55% | 2020-03-05 | 2021-01-07 |
| test | 941 | 214 | 22.74% | 2021-03-11 | 2022-05-19 |


Toàn nguồn Global có **5,347 bài**, **4,665 bài** đủ điều kiện trước purge. Mốc Validation là **2020-03-05**, Test là **2021-03-11**; **259 bài** bị purge ở hai biên. Mốc chia theo phân vị 60%/80% của tuần đầu trên nhóm đủ điều kiện. Cửa sổ nhãn của Train phải kết thúc trước Validation; Validation phải kết thúc trước Test.

ID bài tách biệt giữa các tập, nhưng không có đảm bảo nghệ sĩ hoặc bản thu khác ID tách biệt. Timestamp công bố chart và thời điểm có sẵn của audio chưa được xác minh. `02_eda` tạo lại cohort tương đương nhưng biểu diễn nhãn chưa biết bằng −1; `03_model` dùng NA nullable. Không coi −1 là lớp thứ ba.

## 5. Khóa join và quy tắc tổng hợp

| Ghép/tổng hợp | Khóa | Quy tắc |
| --- | --- | --- |
| Chart → tracks_dimension | track_id | many-to-one; mỗi bài một dòng audio. |
| Chart/mart → country_lookup | chart_country | many-to-one; Global không có trong lookup quốc gia. |
| Mart quốc gia → WHR | chart_country, year ↔ country, year | 01 hiện inner join sau chuẩn hóa; 141 cặp trong snapshot khớp. |
| Mart tuần → COVID | chart_country, week ↔ country, week | Nên validate one-to-one khi đã tổng hợp; các tuần trước nguồn COVID không có dữ liệu. |
| Lookup → GDP kiểm tra | country_code, year | many-to-one; GDP không được lưu trong mart quốc gia hiện tại. |
| Chart credit → slot | chart_country, week, rank | Loại lặp nghệ sĩ trước tổng hợp audio/streams. |
| Global → cohort | track_id, week | Loại lặp bài–tuần, lấy tuần đầu và quan sát tám tuần sau. |

Tổng credit nghệ sĩ không bằng tổng lượt nghe độc lập: bài hợp tác được ghi đầy đủ streams cho từng nghệ sĩ. Global và country_streams phải được trình bày riêng. Mart năm dựa trên phạm vi năm có sẵn; 2022 chỉ đến 14/07, và một số quốc gia có ít tuần hơn các quốc gia khác.

## 6. Giới hạn cần giữ trong báo cáo

- Các file hiện tại là snapshot địa phương, không có bằng chứng về ngày tải hoặc giấy phép từng bản phân phối.
- Chart Global trải từ 2016-12-29 đến 2022-07-14; chart quốc gia bắt đầu muộn và không đồng đều. Không so sánh tổng năm khi phạm vi tuần khác nhau mà không giải thích.
- Ngày release_date_clean có thể suy ra từ chuỗi chỉ có năm/tháng. days_to_chart không luôn là độ trễ chính xác đến ngày; dữ liệu hiện có giá trị âm.
- `week` là mốc thứ Năm trong dữ liệu; việc coi đó là kết thúc tuần khi ghép COVID là quy ước code hiện tại.
- WHR hợp nhất cột khác nhau giữa các ấn bản. Không gán sáu factor cùng đơn vị hoặc so sánh xuyên năm mà không kiểm tra.
- WHO/JHU tử vong báo cáo, valence và happiness_score đo các khái niệm khác nhau; tương quan không đủ để suy ra nguyên nhân hoặc tâm lý người nghe.
- Nhãn chỉ quan sát trong chart được giữ sau lọc audio. Mô hình không áp dụng mặc định cho bài chưa từng vào Top 200.
- Schema bảng xử lý và bảng ML trong bộ nhớ được phân biệt rõ; đọc X theo danh sách FEATURES của notebook 03, không theo toàn bộ cột.

## 7. Tài liệu đang dùng

- [Luồng xử lý](data_processing_flow.md): sơ đồ và quy trình.
- [Hướng dẫn dashboard](HUONG_DAN_CAI_DAT_VA_SU_DUNG.md): chạy và thao tác.
- [Phân công nhóm](team_tasks_assignment.md): nhiệm vụ theo barem.
- [HTML story](spotify_data_story.html): bản demo độc lập.
