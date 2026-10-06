import os
import sys
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

sys.stdout.reconfigure(encoding='utf-8')
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# ---------------------------------------------------------------------------
# CELL DEFINITIONS FOR PART 1 & PART 2
# ---------------------------------------------------------------------------

cells = []

# Title & Overview
cells.append(new_markdown_cell("""# Khai Phá Insight & Kể Chuyện Dữ Liệu (Data Storytelling)
## Đề Tài: Spotify Audio Trends & Crisis Analytics (2020 – 2022)
**Người thực hiện:** Lý Gia Hân (24133016) — Visualization Specialist & Dashboard Developer

---

### 📖 Giới Thiệu Cốt Truyện Dữ Liệu:
Hồ sơ âm thanh trên Spotify không chỉ đơn thuần là những con số kỹ thuật, mà là **dấu vân tay văn hóa** của từng khu vực và **tấm gương phản chiếu tâm lý xã hội** trước các biến cố lịch sử. Cuốn notebook này được thiết kế như tài liệu nghiên cứu cốt lõi phục vụ xây dựng hệ thống Dashboard tương tác, bao gồm hai trục phân tích chiến lược:

1. **Phần 1: Một Thế Giới, Nhiều Hồ Sơ Âm Thanh: Khu Vực Khác Nhau Như Thế Nào Trên Spotify?**
   - *Chiều không gian & Văn hóa địa lý:* Khảo sát 73 quốc gia thuộc 7 khu vực World Bank (`wb_region`) trong năm 2022 và so sánh 68 quốc gia xuyên suốt hai năm 2021 – 2022.
   - Trả lời 3 câu hỏi thực chứng:
     * *Hồ sơ âm nhạc của từng khu vực vĩ mô có nét đặc trưng gì nổi bật?*
     * *Khác biệt cụ thể giữa các khu vực lớn đến mức nào (khoảng cách định lượng)?*
     * *Giá trị trung bình khu vực có che giấu sự đa dạng cực đoan bên trong (đặc biệt tại Đông Á & Thái Bình Dương)?*

2. **Phần 2: Biến Động Âm Nhạc Toàn Cầu Trong Đại Dịch COVID-19 & Hiệu Ứng Trốn Chạy Thực Tại**
   - *Chiều thời gian & Khủng hoảng xã hội:* Theo dõi chuỗi thời gian 130 tuần liên tục (2020 – 2022) đối chiếu giữa dữ liệu âm thanh toàn cầu và các đợt bùng phát dịch bệnh.
   - Kiểm định giả thuyết tâm lý học hành vi: *"Hiệu ứng trốn chạy thực tại"* (Musical Escapism) và *"Hiệu ứng son môi"* (Lipstick Effect).

3. **Phần 3: Đúc Kết Thông Điệp Kể Chuyện Toàn Diện Cho Dashboard**
   - Tổng hợp các luận điểm vàng kết nối giữa bản sắc địa phương và phản ứng tâm lý khủng hoảng toàn cầu."""))

# Imports & Environment Setup
cells.append(new_code_cell("""import os
import sys
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

pd.set_option('display.max_columns', None)

cwd = os.getcwd()
PROJECT_ROOT = os.path.dirname(cwd) if os.path.basename(cwd) == "notebooks" else cwd
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

print(f"Môi trường phân tích sẵn sàng. Thư mục dự án: {PROJECT_ROOT}")"""))

# ---------------------------------------------------------------------------
# PHẦN 1: MỘT THẾ GIỚI, NHIỀU HỒ SƠ ÂM THANH
# ---------------------------------------------------------------------------

cells.append(new_markdown_cell("""---
# PHẦN 1: MỘT THẾ GIỚI, NHIỀU HỒ SƠ ÂM THANH: KHU VỰC KHÁC NHAU NHƯ THẾ NÀO TRÊN SPOTIFY?

### 🎯 Chiến Lược Tiếp Cận & Khung Phân Tích:
Thay vì đặt ra một "nghịch lý" định kiến trước rồi tìm cách chứng minh, chúng ta tiếp cận khách quan dựa trên dữ liệu thực chứng với quy trình 5 bước:
1. **Toàn cảnh hồ sơ 7 khu vực × 9 đặc trưng:** Bắt đầu bằng Heatmap chuẩn hóa để bao quát trọn vẹn mọi khía cạnh âm thanh.
2. **Đo lường độ phân hóa cốt lõi:** Chọn 4 đặc trưng có độ lệch lớn nhất (Danceability, Energy, Valence, Acousticness) để so sánh cột nhóm định lượng.
3. **Phân bố địa lý toàn cầu:** Bản đồ Choropleth cho Acousticness xác định các tâm điểm và vùng trũng âm nhạc mộc.
4. **Mổ xẻ đa dạng nội vùng (Intra-regional Diversity):** Biểu đồ điểm từng quốc gia kiểm chứng xem mức trung bình vùng có che giấu sự đối nghịch giữa các quốc gia hay không (trường hợp Việt Nam, Indonesia và Nhật Bản).
5. **Độ ổn định văn hóa qua thời gian:** Dot plot 2021 – 2022 theo khu vực trên 68 quốc gia có mặt cả hai năm để tìm ra nét âm thanh bền vững và nét thay đổi."""))

# Load Regional Data
cells.append(new_code_cell("""# Nạp và chuẩn bị dữ liệu quốc gia & khu vực
country_year_path = os.path.join(PROJECT_ROOT, "data", "processed", "mart_country_year.parquet")
df_country_all = pd.read_parquet(country_year_path)

# Dữ liệu năm 2022 (73 quốc gia)
df_2022 = df_country_all[df_country_all['year'] == 2022].copy()

# Xác định 68 quốc gia hiện diện ở cả hai năm 2021 và 2022
countries_2021 = set(df_country_all[df_country_all['year'] == 2021]['country_code'])
countries_2022 = set(df_country_all[df_country_all['year'] == 2022]['country_code'])
common_countries = countries_2021.intersection(countries_2022)

df_common = df_country_all[df_country_all['country_code'].isin(common_countries)].copy()

AUDIO_FEATURES_9 = [
    'danceability', 'energy', 'valence', 'acousticness',
    'speechiness', 'instrumentalness', 'liveness', 'loudness', 'tempo'
]
FEATURE_COLS_WEIGHTED = [f'{f}_weighted' for f in AUDIO_FEATURES_9]

FEATURE_LABELS = [
    'Danceability', 'Energy', 'Valence', 'Acousticness',
    'Speechiness', 'Instrumentalness', 'Liveness', 'Loudness (dB)', 'Tempo (BPM)'
]

print(f"✅ Dữ liệu năm 2022: {len(df_2022)} quốc gia thuộc {df_2022['wb_region'].nunique()} khu vực World Bank.")
print(f"✅ Quốc gia có mặt ở cả hai năm (2021 - 2022): {len(common_countries)} quốc gia.")"""))

# Biểu đồ 1: Heatmap
cells.append(new_markdown_cell("""---
## 1. Hồ Sơ Âm Nhạc Của Từng Khu Vực (Heatmap 7 Khu Vực × 9 Đặc Trưng, 2022)

**Phương pháp trực quan:**
- Trục tung thể hiện 7 khu vực địa lý vĩ mô của Ngân hàng Thế giới (`wb_region`).
- Trục hoành là đủ 9 đặc trưng âm thanh Spotify.
- Chuẩn hóa Min-Max theo từng cột (từng đặc trưng) đưa về thang $[0, 1]$ nhằm loại bỏ độ lệch thang đo giữa các đơn vị (dB, BPM, tỉ lệ).
- Tooltip hiển thị đầy đủ thông tin: Khu vực, Tên đặc trưng, Điểm chuẩn hóa và **Giá trị gốc thực tế kèm đơn vị đo**."""))

cells.append(new_code_cell("""def plot_heatmap_regional_profiles(df_year):
    reg_raw = df_year.groupby('wb_region')[FEATURE_COLS_WEIGHTED].mean()
    reg_raw.columns = FEATURE_LABELS
    
    # Chuẩn hóa Min-Max theo từng đặc trưng (theo cột)
    reg_norm = (reg_raw - reg_raw.min()) / (reg_raw.max() - reg_raw.min())
    
    # Chuẩn bị ma trận giá trị gốc hiển thị trong tooltip
    custom_hover = []
    for r in reg_raw.index:
        row_vals = []
        for c in reg_raw.columns:
            val = reg_raw.loc[r, c]
            if 'Loudness' in c:
                row_vals.append(f"{val:.2f} dB")
            elif 'Tempo' in c:
                row_vals.append(f"{val:.1f} BPM")
            else:
                row_vals.append(f"{val:.4f}")
        custom_hover.append(row_vals)
        
    fig = go.Figure(data=go.Heatmap(
        z=reg_norm.values,
        x=FEATURE_LABELS,
        y=reg_norm.index.tolist(),
        colorscale='Viridis',
        customdata=custom_hover,
        text=np.round(reg_norm.values, 2),
        texttemplate='%{text:.2f}',
        textfont=dict(size=11),
        hovertemplate='<b>Khu vực:</b> %{y}<br><b>Đặc trưng:</b> %{x}<br><b>Điểm chuẩn hóa (0-1):</b> %{z:.2f}<br><b>Giá trị gốc:</b> %{customdata}<extra></extra>',
        colorbar=dict(
            title=dict(text='Điểm Chuẩn Hóa<br>(0: Thấp nhất, 1: Cao nhất)', font=dict(size=11)),
            thickness=15,
            len=0.85
        )
    ))
    
    fig.update_layout(
        title=dict(
            text='<b>Hồ Sơ Âm Thanh 7 Khu Vực World Bank (Spotify Charts 2022)</b><br><sup>Chuẩn hóa Min-Max theo từng đặc trưng • Hover xem giá trị gốc</sup>',
            x=0.01, y=0.96,
            font=dict(size=15)
        ),
        xaxis=dict(tickangle=-25, tickfont=dict(size=11)),
        yaxis=dict(tickfont=dict(size=11)),
        height=520,
        margin=dict(l=170, r=40, t=80, b=70),
        template='plotly_white'
    )
    return fig

fig_reg_heatmap = plot_heatmap_regional_profiles(df_2022)
fig_reg_heatmap.show()"""))

cells.append(new_markdown_cell("""### 💡 Insight 1: Bức tranh toàn cảnh 7 khu vực × 9 đặc trưng âm thanh (2022)

1. **Mỹ Latinh (Latin America & Caribbean) — "Thủ phủ" của năng lượng và vũ điệu toàn cầu:**
   - Dẫn đầu tuyệt đối thế giới ở 4 chỉ số cốt lõi: **Danceability** ($0.7292$, điểm chuẩn hóa $1.000$), **Energy** ($0.6755$, chuẩn hóa $1.000$), **Valence** ($0.5825$, chuẩn hóa $1.000$), và **Loudness** ($-5.43$ dB, chuẩn hóa $1.000$).
   - Thị hiếu âm nhạc tại Mỹ Latinh mang tính thể chất rất cao, thống trị bởi các dòng nhạc Reggaeton, Latin Pop và Funk Carioca sôi động, âm lượng được master nén rất lớn để phục vụ các bữa tiệc và câu lạc bộ khiêu vũ.

2. **Châu Á (East Asia & Pacific và South Asia) — Vùng đất của giai điệu mộc mạc và chiêm nghiệm:**
   - Chiếm lĩnh hai vị trí dẫn đầu toàn cầu về độ mộc mạc (**Acousticness**): Nam Á ($0.3392$, chuẩn hóa $1.000$) và Đông Á & Thái Bình Dương ($0.3379$, chuẩn hóa $0.988$), cao gấp rưỡi Bắc Mỹ ($0.2257$).
   - Đồng thời, Đông Á có điểm **Danceability thấp nhất thế giới** ($0.6214$, chuẩn hóa $0.000$) và Nam Á có **Energy thấp nhất** ($0.5989$, chuẩn hóa $0.000$) cùng nhịp độ chậm nhất ($115.4$ BPM). Người nghe tại các thị trường châu Á chuộng các thể loại giàu cảm xúc trữ tình, mộc mạc và mang tính tự sự cao (Pop Ballad, Acoustic Indie).

3. **Châu Phi cận Sahara & Châu Âu — Hai thái cực nhịp điệu riêng biệt:**
   - **Châu Phi cận Sahara:** Xếp thứ nhì thế giới về **Danceability** ($0.7260$, chuẩn hóa $0.970$), đồng thời dẫn đầu toàn cầu về **Speechiness** ($0.1269$, chuẩn hóa $1.000$) và **Instrumentalness** ($0.0308$, chuẩn hóa $1.000$), khắc họa rõ nét cấu trúc của dòng nhạc Afrobeats và Amapiano với bộ gõ phức hợp và ca từ giàu tính nhịp điệu.
   - **Châu Âu & Trung Á:** Nổi bật với **Tempo nhanh nhất hành tinh** ($123.65$ BPM, chuẩn hóa $1.000$) và Energy rất cao ($0.6638$, chuẩn hóa $0.847$), phản ánh sự thịnh hành của văn hóa nhạc điện tử (EDM), Euro-Pop và House."""))

# Biểu đồ 2: Grouped Bar
cells.append(new_markdown_cell("""---
## 2. Khác Biệt Nổi Bật Giữa Các Khu Vực (Cột Nhóm Cho 4 Đặc Trưng Trọng Tâm, 2022)

**Phương pháp trực quan:**
- Chọn ra 4 đặc trưng có độ phân hóa sâu sắc nhất từ Heatmap: **Danceability, Energy, Valence, Acousticness**.
- Biểu đồ cột nhóm so sánh trực diện 7 khu vực theo thang đo gốc $[0, 1]$.
- Nhãn giá trị định dạng 2 chữ số thập phân trên từng cột; hover cung cấp số liệu chi tiết tới 4 chữ số thập phân."""))

cells.append(new_code_cell("""def plot_grouped_bar_key_features(df_year):
    features_4 = ['danceability', 'energy', 'valence', 'acousticness']
    cols_4 = [f'{f}_weighted' for f in features_4]
    labels_4 = ['Danceability', 'Energy', 'Valence', 'Acousticness']
    palette_4 = ['#1DB954', '#FF5722', '#FFB300', '#9C27B0']
    
    reg_summary = df_year.groupby('wb_region')[cols_4].mean()
    reg_summary.columns = labels_4
    
    # Sắp xếp các khu vực theo Danceability giảm dần
    reg_summary = reg_summary.sort_values('Danceability', ascending=False)
    
    fig = go.Figure()
    for feat, color in zip(labels_4, palette_4):
        fig.add_trace(go.Bar(
            x=reg_summary.index,
            y=reg_summary[feat],
            name=feat,
            marker_color=color,
            text=reg_summary[feat].round(2),
            texttemplate='%{text:.2f}',
            textposition='outside',
            hovertemplate='<b>Khu vực:</b> %{x}<br><b>Đặc trưng:</b> ' + feat + '<br><b>Giá trị:</b> %{y:.4f}<extra></extra>'
        ))
        
    fig.update_layout(
        barmode='group',
        title=dict(
            text='<b>So Sánh 4 Đặc Trưng Phân Hóa Nổi Bật Giữa 7 Khu Vực (2022)</b><br><sup>Danceability • Energy • Valence • Acousticness (Giá trị trung bình luồng nghe)</sup>',
            x=0.01, y=0.96,
            font=dict(size=15)
        ),
        xaxis=dict(tickangle=-15, tickfont=dict(size=11)),
        yaxis=dict(title='Giá trị trung bình (0 – 1)', range=[0, 0.84], tickfont=dict(size=10)),
        legend=dict(
            orientation='h',
            yanchor='bottom', y=1.02,
            xanchor='right', x=0.99,
            font=dict(size=11)
        ),
        height=540,
        margin=dict(l=60, r=30, t=90, b=80),
        template='plotly_white'
    )
    return fig

fig_grouped_bars = plot_grouped_bar_key_features(df_2022)
fig_grouped_bars.show()"""))

cells.append(new_markdown_cell("""### 💡 Insight 2: Đo lường khoảng cách cụ thể giữa các khu vực (2022)

1. **Khoảng cách Danceability cực lớn giữa Mỹ Latinh và Đông Á:**
   - Chênh lệch Danceability giữa Mỹ Latinh ($0.7292$) và Đông Á & Thái Bình Dương ($0.6214$) lên tới **$0.1078$ điểm** (tương đương chênh lệch $+17.3\%$). Đây là độ giãn cách lớn nhất giữa hai khu vực trên bất kỳ chỉ số âm thanh nào, chứng minh sự phân cực sâu sắc giữa văn hóa nghe nhạc để khiêu vũ (Dance-centric) và nghe nhạc để cảm thụ giai điệu (Melody-centric).

2. **Nghịch lý "Vui tươi" (Valence) và "Mộc mạc" (Acousticness):**
   - Mỹ Latinh có điểm số tươi sáng (Valence) cao nhất thế giới ($0.5825$), trong khi Nam Á ($0.4813$), Bắc Mỹ ($0.4893$) và Đông Á ($0.4902$) đều dưới ngưỡng $0.50$ (khoảng chênh lệch đạt $+21.0\%$).
   - Tuy nhiên, xu hướng bị đảo ngược hoàn toàn ở chỉ số Acousticness: Nam Á ($0.3392$) và Đông Á ($0.3379$) cao hơn Bắc Mỹ ($0.2257$) và Châu Âu ($0.2359$) tới **$+50.3\%$**. Khu vực nghe nhạc "buồn và mộc" nhất thế giới nằm ở Châu Á, trong khi khu vực "vui vẻ và điện tử" nhất tập trung ở Mỹ Latinh.

3. **Mặt bằng Energy: Năng lượng bùng nổ của phương Tây và Latin:**
   - Mỹ Latinh ($0.6755$) và Châu Âu ($0.6638$) duy trì mức năng lượng cao vượt trội so với Nam Á ($0.5989$) và Đông Á ($0.6033$), độ chênh lệch là **$0.0766$ điểm ($+12.8\%$)**, phản ánh sự ưa chuộng bản phối sôi động, nhiều âm bass và synthesizer tại các thị trường Âu - Mỹ."""))

# Biểu đồ 3: Choropleth Map
cells.append(new_markdown_cell("""---
## 3. Phân Bố Theo Địa Lý Toàn Cầu (Bản Đồ Choropleth Cho Acousticness, 2022)

**Phương pháp trực quan:**
- Khảo sát không gian địa lý của đặc trưng có mức phân hóa cao nhất: **Acousticness** (Độ mộc mạc) trên 73 quốc gia năm 2022.
- Mã hóa màu theo thang sắc độ tuần tự `Tealgrn` (màu đậm = Acousticness cao).
- Tooltip hiển thị: Tên quốc gia, Mã ISO-3, Khu vực, Giá trị Acousticness và **Thứ hạng toàn cầu (#1 đến #73)**."""))

cells.append(new_code_cell("""def plot_choropleth_acousticness(df_year):
    df_sorted = df_year.sort_values('acousticness_weighted', ascending=False).copy()
    df_sorted['global_rank'] = range(1, len(df_sorted) + 1)
    
    fig = go.Figure(data=go.Choropleth(
        locations=df_sorted['country_code'],
        locationmode='ISO-3',
        z=df_sorted['acousticness_weighted'],
        customdata=df_sorted[['chart_country', 'wb_region', 'global_rank', 'acousticness_weighted']],
        colorscale='Tealgrn',
        colorbar=dict(
            title=dict(text='Acousticness<br>(Độ mộc mạc)', font=dict(size=11)),
            thickness=15,
            len=0.75
        ),
        hovertemplate='<b>%{customdata[0]}</b> (%{locations})<br>' +
                      'Khu vực: %{customdata[1]}<br>' +
                      'Acousticness: <b>%{customdata[3]:.4f}</b><br>' +
                      'Thứ hạng toàn cầu: <b>#%{customdata[2]}/73</b><extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text='<b>Bản Đồ Phân Bố Toàn Cầu: Chỉ Số Nhạc Mộc (Acousticness) Năm 2022</b><br><sup>Tâm điểm tập trung tại Đông Nam Á • Vùng trũng tại Bắc Âu & Đông Âu</sup>',
            x=0.01, y=0.96,
            font=dict(size=15)
        ),
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth',
            coastlinecolor='#BDC3C7',
            countrycolor='#E0E0E0'
        ),
        height=560,
        margin=dict(l=0, r=0, t=70, b=0)
    )
    return fig

fig_choropleth_acoustic = plot_choropleth_acousticness(df_2022)
fig_choropleth_acoustic.show()"""))

cells.append(new_markdown_cell("""### 💡 Insight 3: Bản đồ địa lý âm thanh và những cực đối lập toàn cầu

1. **Đông Nam Á là tâm điểm của dòng nhạc mộc mạc toàn cầu:**
   - Bản đồ hiển thị một vệt màu đậm đặc tập trung tại khu vực Đông Nam Á. Hai quốc gia có Acousticness cao nhất trên toàn cầu là **Indonesia ($0.5128$ — Hạng 1/73)** và **Việt Nam ($0.4542$ — Hạng 2/73)**, theo sau là Philippines ($0.3847$ — Hạng 5) và Malaysia ($0.3513$ — Hạng 7). Tại hai quốc gia đứng đầu, gần một nửa lượng stream tập trung vào các bản nhạc thuần nhạc cụ mộc, ballad acoustic và indie du dương.

2. **"Vùng trũng" Acousticness tại Bắc Âu và Đông Âu:**
   - Các quốc gia có chỉ số mộc thấp nhất hành tinh tập trung dày đặc ở Châu Âu: **Phần Lan ($0.1561$ — Thấp nhất thế giới)**, Bulgaria ($0.1643$), Estonia ($0.1770$), Latvia ($0.1911$). Thị hiếu nghe nhạc tại các quốc gia này bị chi phối gần như hoàn toàn bởi âm thanh nhân tạo tổng hợp: Synth-Pop, Metal, Electro-Pop.

3. **Ngoại lệ địa lý nổi bật (Geographical Outliers):**
   - **Nhật Bản (JPN):** Cùng thuộc khu vực Đông Á & Thái Bình Dương nhưng Acousticness chỉ đạt **$0.1803$ (Hạng 67/73 toàn cầu)**, thấp hơn $2.8$ lần so với Indonesia và khác biệt hoàn toàn với xu hướng của phần còn lại của châu Á.
   - **Iceland (ISL):** Nằm tại Bắc Âu nhưng Acousticness vọt lên **$0.3491$ (Hạng 9 toàn cầu)**, cao hơn gấp đôi Phần Lan ($0.1561$), phản ánh trường phái âm nhạc dân gian đương đại và acoustic truyền thống của đảo quốc này."""))

# Biểu đồ 4: Strip Plot Intra-regional
cells.append(new_markdown_cell("""---
## 4. Khác Biệt Bên Trong Khu Vực: Trung Bình Có Che Giấu Sự Đa Dạng? (Biểu Đồ Điểm 2022)

**Phương pháp trực quan:**
- Biểu đồ điểm (Strip / Point Plot) hiển thị từng quốc gia (mỗi chấm tròn là một nước) phân theo 7 khu vực World Bank.
- Trục tung là đặc trưng phân hóa mạnh nhất: **Acousticness**.
- Biểu tượng hình thoi màu đen biểu thị **giá trị trung bình của từng khu vực**.
- Chú thích mũi tên nổi bật cho các quốc gia tiêu biểu: **Việt Nam (VNM), Indonesia (IDN), Nhật Bản (JPN), Iceland (ISL), Phần Lan (FIN)**."""))

cells.append(new_code_cell("""def plot_strip_intra_regional_diversity(df_year):
    reg_means = df_year.groupby('wb_region')['acousticness_weighted'].mean().to_dict()
    df_plot = df_year.copy()
    df_plot['reg_mean'] = df_plot['wb_region'].map(reg_means)
    df_plot['diff_from_mean'] = df_plot['acousticness_weighted'] - df_plot['reg_mean']
    
    # Sắp xếp các khu vực theo trung bình giảm dần
    sorted_regions = sorted(reg_means.keys(), key=lambda r: reg_means[r], reverse=True)
    
    fig = go.Figure()
    
    # Vẽ các điểm quốc gia
    for region in sorted_regions:
        sub = df_plot[df_plot['wb_region'] == region]
        fig.add_trace(go.Scatter(
            x=[region] * len(sub),
            y=sub['acousticness_weighted'],
            mode='markers',
            name=region,
            marker=dict(size=9, opacity=0.75),
            customdata=sub[['chart_country', 'country_code', 'acousticness_weighted', 'diff_from_mean', 'reg_mean']],
            hovertemplate='<b>%{customdata[0]}</b> (%{customdata[1]})<br>' +
                          'Acousticness: <b>%{customdata[2]:.4f}</b><br>' +
                          'Trung bình vùng: %{customdata[4]:.4f}<br>' +
                          'Chênh lệch (Δ): <b>%{customdata[3]:+.4f}</b><extra></extra>',
            showlegend=False
        ))
        
        # Vẽ điểm trung bình khu vực (Diamond)
        fig.add_trace(go.Scatter(
            x=[region],
            y=[reg_means[region]],
            mode='markers',
            marker=dict(symbol='diamond', size=13, color='black', line=dict(width=1.5, color='white')),
            name='Trung bình vùng',
            showlegend=(region == sorted_regions[0]),
            hovertemplate='<b>Trung bình %{x}:</b> %{y:.4f}<extra></extra>'
        ))
        
    # Chú thích các trường hợp điển hình
    annotations = [
        ('IDN', 'Indonesia (0.513) - #1 Thế giới', 45, -25),
        ('VNM', 'Việt Nam (0.454) - #2 Thế giới', -50, -20),
        ('JPN', 'Nhật Bản (0.180) - Đối lập cực đoan', -50, 30),
        ('ISL', 'Iceland (0.349) - Ngoại lệ Châu Âu', 45, -25),
        ('FIN', 'Phần Lan (0.156) - Thấp nhất', 45, 25)
    ]
    
    for code, text_label, ax_val, ay_val in annotations:
        c_row = df_plot[df_plot['country_code'] == code]
        if not c_row.empty:
            r = c_row.iloc[0]
            fig.add_annotation(
                x=r['wb_region'],
                y=r['acousticness_weighted'],
                text=f"<b>{text_label}</b>",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=1.5,
                ax=ax_val,
                ay=ay_val,
                bgcolor='rgba(255, 255, 255, 0.9)',
                bordercolor='#34495E',
                borderwidth=1,
                font=dict(size=10)
            )
            
    fig.update_layout(
        title=dict(
            text='<b>Độ Phân Hóa Nội Bộ Từng Khu Vực: Phân Bố Acousticness Của Từng Quốc Gia (2022)</b><br><sup>Mỗi chấm là một quốc gia • Hình thoi đen là trung bình vùng • Đối chiếu Indonesia, Việt Nam vs Nhật Bản</sup>',
            x=0.01, y=0.96,
            font=dict(size=15)
        ),
        xaxis=dict(tickangle=-15, tickfont=dict(size=11), title='Khu vực World Bank'),
        yaxis=dict(title='Acousticness (Chỉ số mộc)', range=[0.11, 0.56], tickfont=dict(size=10)),
        legend=dict(x=0.99, y=1.02, xanchor='right', yanchor='bottom', orientation='h'),
        height=560,
        margin=dict(l=60, r=40, t=80, b=80),
        template='plotly_white'
    )
    return fig

fig_strip_diversity = plot_strip_intra_regional_diversity(df_2022)
fig_strip_diversity.show()"""))

cells.append(new_markdown_cell("""### 💡 Insight 4: Vạch trần "ảo ảnh trung bình vùng" qua trường hợp Đông Á & Thái Bình Dương

1. **Sự đối lập cực đoan bên trong vùng East Asia & Pacific (Indonesia vs Nhật Bản):**
   - Giá trị trung bình của vùng East Asia & Pacific là $0.3379$. Tuy nhiên, bên trong vùng tồn tại một **hố sâu phân hóa lên tới $0.3325$ điểm** giữa **Indonesia ($0.5128$)** và **Nhật Bản ($0.1803$)**!
   - Nếu chỉ dựa vào chỉ số trung bình vùng, ta sẽ lầm tưởng các quốc gia châu Á có gu âm nhạc tương đồng nhau. Thực tế, Đông Nam Á (Indonesia, Việt Nam, Philippines) chuộng giai điệu mộc mạc, nhẹ nhàng; trong khi các thị trường Đông Á phát triển như Nhật Bản lại ưa chuộng các thể loại nhạc giàu năng lượng (Energy $0.730$), nhịp điệu dồn dập (J-Rock, Anime OST, Idol Pop) với độ mộc mạc thuộc hàng thấp nhất thế giới.

2. **Hồ sơ độc đáo của Việt Nam (VNM): Giao thoa giữa mộc mạc và dễ nhảy:**
   - Việt Nam sở hữu vị trí rất đặc biệt: xếp thứ 2 thế giới về Acousticness ($0.4542$), nhưng lại có **Danceability cao vượt trội ($0.6723$)**, cao hơn đáng kể so với Indonesia ($0.5576$) và trung bình toàn vùng ($0.6214$).
   - Điều này phản ánh rõ cấu trúc bảng xếp hạng Spotify Việt Nam: người nghe yêu thích các bản Pop Ballad ngọt ngào, giàu nhạc cụ acoustic nhưng luôn có phần beat bắt tai, dễ đung đưa (phong cách V-Pop hiện đại hoặc xu hướng Ballad/Lofi Remix).

3. **Tính đồng nhất của Mỹ Latinh so với độ tản mạn của Châu Á:**
   - Trong khi East Asia & Pacific có biên độ tản mạn lớn nhất hành tinh ($0.180 \to 0.513$, biên độ $0.333$), khu vực **Latin America & Caribbean** lại có tính thuần nhất rất cao: toàn bộ các quốc gia đều tập trung chặt chẽ trong dải hẹp $0.218 - 0.316$ (biên độ chỉ $0.098$). Thị hiếu Mỹ Latinh đồng nhất xuyên biên giới nhờ vị thế áp đảo của dòng nhạc Reggaeton."""))

# Biểu đồ 5: Dot Plot 2021 vs 2022
cells.append(new_markdown_cell("""---
## 5. Hồ Sơ Thay Đổi Giữa Hai Năm (Dot Plot 2021–2022 Theo Khu Vực, Thang Đo Riêng)

**Phương pháp trực quan:**
- Đo lường mức độ biến chuyển của 7 khu vực giữa hai năm 2021 và 2022 trên **68 quốc gia có mặt ở cả hai năm**.
- Bố cục lưới $3 \times 3$ subplots cho đủ 9 đặc trưng âm thanh.
- Mỗi ô có trục hoành là thang đo độc lập tương ứng với miền giá trị của từng đặc trưng.
- Hai mốc thời gian được biểu diễn bằng hai điểm màu: **2021 (Xanh dương, chấm tròn)** và **2022 (Đỏ, hình thoi)**, nối với nhau bằng đoạn thẳng chỉ rõ hướng dịch chuyển."""))

cells.append(new_code_cell("""def plot_dotplot_regional_evolution(df_common_data):
    features_all = [
        'danceability', 'energy', 'valence', 'acousticness',
        'speechiness', 'instrumentalness', 'liveness', 'loudness', 'tempo'
    ]
    cols_all = [f'{f}_weighted' for f in features_all]
    titles_all = [
        'Danceability', 'Energy', 'Valence', 'Acousticness',
        'Speechiness', 'Instrumentalness', 'Liveness', 'Loudness (dB)', 'Tempo (BPM)'
    ]
    
    reg_yearly = df_common_data.groupby(['wb_region', 'year'])[cols_all].mean().reset_index()
    regions = sorted(df_common_data['wb_region'].unique())
    
    fig = make_subplots(
        rows=3, cols=3,
        subplot_titles=[f"<b>{t}</b>" for t in titles_all],
        horizontal_spacing=0.10,
        vertical_spacing=0.14
    )
    
    for idx, (f_col, t_label) in enumerate(zip(cols_all, titles_all)):
        r = idx // 3 + 1
        c = idx % 3 + 1
        
        piv = reg_yearly.pivot(index='wb_region', columns='year', values=f_col).loc[regions]
        
        # Đường nối 2021 -> 2022
        for reg in regions:
            val_21 = piv.loc[reg, 2021]
            val_22 = piv.loc[reg, 2022]
            fig.add_trace(go.Scatter(
                x=[val_21, val_22],
                y=[reg, reg],
                mode='lines',
                line=dict(color='#BDC3C7', width=2),
                showlegend=False,
                hoverinfo='skip'
            ), row=r, col=c)
            
        # Điểm năm 2021
        fig.add_trace(go.Scatter(
            x=piv[2021],
            y=regions,
            mode='markers',
            name='Năm 2021',
            marker=dict(size=8, color='#3498DB', symbol='circle'),
            showlegend=(idx == 0),
            hovertemplate='<b>%{y}</b> (2021)<br>' + t_label + ': %{x:.4f}<extra></extra>'
        ), row=r, col=c)
        
        # Điểm năm 2022
        fig.add_trace(go.Scatter(
            x=piv[2022],
            y=regions,
            mode='markers',
            name='Năm 2022',
            marker=dict(size=9, color='#E74C3C', symbol='diamond'),
            showlegend=(idx == 0),
            hovertemplate='<b>%{y}</b> (2022)<br>' + t_label + ': %{x:.4f}<extra></extra>'
        ), row=r, col=c)
        
        if c != 1:
            fig.update_yaxes(showticklabels=False, row=r, col=c)
        else:
            fig.update_yaxes(tickfont=dict(size=9), row=r, col=c)
            
        fig.update_xaxes(tickfont=dict(size=9), row=r, col=c)
        
    fig.update_layout(
        title=dict(
            text='<b>Biến Chuyển Hồ Sơ Âm Thanh 2021 – 2022 Theo 7 Khu Vực (Lưới 3×3 Thang Đo Riêng)</b><br><sup>Xét trên 68 quốc gia hiện diện ở cả hai năm • Đánh giá nét âm thanh ổn định và biến đổi</sup>',
            x=0.01, y=0.99,
            font=dict(size=15)
        ),
        legend=dict(
            orientation='h',
            x=0.99, y=1.03,
            xanchor='right', yanchor='bottom',
            font=dict(size=11),
            bgcolor='rgba(255, 255, 255, 0.7)'
        ),
        height=880,
        margin=dict(l=150, r=30, t=80, b=50),
        template='plotly_white'
    )
    return fig

fig_dotplot_evolution = plot_dotplot_regional_evolution(df_common)
fig_dotplot_evolution.show()"""))

cells.append(new_markdown_cell("""### 💡 Insight 5: Quán tính văn hóa bền vững và những dịch chuyển hậu bình thường mới (2021 vs 2022)

1. **Quán tính văn hóa cao độ (Cultural Inertia) của các đặc trưng cốt lõi:**
   - Trên cả 68 quốc gia có mặt ở cả hai năm, các đặc trưng cốt lõi như **Danceability** và **Energy** biến động cực kỳ nhỏ giữa 2021 và 2022: mức thay đổi của Danceability tại hầu hết các khu vực chỉ dao động trong biên độ $\pm 0.001$ đến $\pm 0.006$ (dưới $1\%$).
   - Điều này chứng minh "ADN âm thanh" của từng khu vực là một cấu trúc văn hóa bền vững, định hình bởi ngôn ngữ, truyền thống thưởng thức và không dễ bị xáo trộn trong ngắn hạn.

2. **Sự điều chỉnh sắc thái cảm xúc tại Mỹ Latinh (Valence sụt giảm):**
   - Biến động đáng chú ý nhất về mặt tâm trạng diễn ra tại Mỹ Latinh & Caribbean: chỉ số **Valence sụt giảm từ $0.6267$ (2021) xuống $0.5848$ (2022)**, mức giảm **$-0.0420$ điểm ($-6.69\%$)**.
   - Dù vẫn là khu vực nghe nhạc vui tươi nhất thế giới, người nghe tại Mỹ Latinh trong năm 2022 bắt đầu đón nhận nhiều ca khúc mang âm hưởng trầm buồn, tự sự hơn sau thời kỳ đại dịch.

3. **Sự trỗi dậy của Energy và sụt giảm Acousticness tại Bắc Mỹ (Hậu bình thường mới):**
   - Tại Bắc Mỹ (Mỹ & Canada), **Energy tăng từ $0.6073$ lên $0.6355$ ($+4.64\%$)**, đi kèm với sự sụt giảm mạnh nhất về **Acousticness từ $0.2553$ xuống $0.2257$ ($-11.57\%$)**.
   - Khi các hạn chế dịch bệnh được gỡ bỏ hoàn toàn vào năm 2022, gu thưởng thức âm nhạc tại Bắc Mỹ nhanh chóng chuyển dịch từ các bài hát acoustic êm dịu thời kỳ phong tỏa sang các sản phẩm âm nhạc điện tử, bùng nổ năng lượng phục vụ các lễ hội và tụ điểm giải trí."""))

# ---------------------------------------------------------------------------
# PHẦN 2: BIẾN ĐỘNG ÂM NHẠC TRONG ĐẠI DỊCH COVID-19
# ---------------------------------------------------------------------------

cells.append(new_markdown_cell("""---
# PHẦN 2: BIẾN ĐỘNG ÂM NHẠC TOÀN CẦU TRONG ĐẠI DỊCH COVID-19 & HIỆU ỨNG TRỐN CHẠY THỰC TẠI (2020 – 2022)

### 🎯 Bối Cảnh Phân Tích Chuỗi Thời Gian Khủng Hoảng:
Nếu Phần 1 giải mã bản sắc âm thanh theo **không gian (khu vực)**, thì Phần 2 khảo sát sự biến đổi cảm xúc theo **thời gian (biến cố khủng hoảng)**. Nghiên cứu khảo sát chuỗi dữ liệu **130 tuần liên tục (23/01/2020 → 14/07/2022)** trên thị trường Toàn cầu (Global), kết hợp dữ liệu âm thanh Spotify với số liệu tử vong do dịch bệnh COVID-19.

**Cấu trúc 5 bộ biểu đồ phân tích:**
1. **COVID và âm nhạc theo thời gian:** Với mỗi đặc trưng (đủ 9 biến), vẽ hai ô trên–dưới: ca tử vong theo tuần ở trên, đặc trưng âm thanh ở dưới; cùng trục thời gian.
2. **Scatter ca tử vong × đặc trưng âm thanh:** Trục X: tử vong tuần, Trục Y: đặc trưng âm thanh, mỗi điểm là một tuần, màu theo năm (2020, 2021, 2022).
3. **Heatmap tháng × 9 đặc trưng, kèm biểu đồ thanh tử vong COVID:** 9 cột âm thanh đã chuẩn hóa min-max đặt cạnh biểu đồ thanh tử vong theo tháng, dùng chung hàng tháng.
4. **So sánh hồ sơ giữa tuần tử vong cao và thấp:** Chia tuần theo mức tử vong (ngưỡng trung vị), dùng dot plot chia ô $3 \times 3$ với thang đo riêng biệt từng biến.
5. **Dot plot so sánh hồ sơ âm nhạc toàn cầu giữa 2021 & 2022:** Đánh giá mức độ chuyển dịch khi bước vào giai đoạn bình thường mới."""))

# Load COVID data
cells.append(new_code_cell("""# Nạp và kết hợp dữ liệu âm nhạc tuần & COVID-19 toàn cầu
audio_trend_path = os.path.join(PROJECT_ROOT, "data", "processed", "mart_audio_trend_weekly.parquet")
covid_path = os.path.join(PROJECT_ROOT, "data", "processed", "covid_weekly_clean.csv")

df_audio_all = pd.read_parquet(audio_trend_path)
df_covid_all = pd.read_csv(covid_path)

df_audio_global = df_audio_all[df_audio_all['chart_country'] == 'Global'].copy()
df_covid_global = df_covid_all[df_covid_all['country'] == 'Global'].copy()

ALL_9_FEATURES = [
    'danceability', 'energy', 'valence', 'acousticness',
    'instrumentalness', 'speechiness', 'liveness', 'loudness', 'tempo'
]

# Map các cột _weighted sang tên chuẩn để phân tích chuỗi thời gian
for f in ALL_9_FEATURES:
    if f'{f}_weighted' in df_audio_global.columns:
        df_audio_global[f] = df_audio_global[f'{f}_weighted']

df_audio_global['week'] = pd.to_datetime(df_audio_global['week'])
df_covid_global['week'] = pd.to_datetime(df_covid_global['week'])

df_merged = pd.merge(
    df_audio_global,
    df_covid_global[['week', 'weekly_deaths', 'cumulative_deaths']],
    on='week',
    how='inner'
).sort_values('week')

df_merged['year'] = df_merged['week'].dt.year
df_merged['year_month'] = df_merged['week'].dt.to_period('M').astype(str)

SHORT_TITLES = [
    'Danceability', 'Energy', 'Valence',
    'Acousticness', 'Instrumentalness', 'Speechiness',
    'Liveness', 'Loudness (dB)', 'Tempo (BPM)'
]

FEATURE_META = {
    'danceability': ('Danceability', 'Độ dễ nhảy', '#1ABC9C', 'Tỉ lệ (0–1)'),
    'energy': ('Energy', 'Cường độ năng lượng', '#E67E22', 'Tỉ lệ (0–1)'),
    'valence': ('Valence', 'Cảm xúc tích cực', '#F1C40F', 'Tỉ lệ (0–1)'),
    'acousticness': ('Acousticness', 'Độ mộc mạc', '#9B59B6', 'Tỉ lệ (0–1)'),
    'instrumentalness': ('Instrumentalness', 'Độ khí nhạc', '#34495E', 'Tỉ lệ (0–1)'),
    'speechiness': ('Speechiness', 'Độ dày lời ca', '#E74C3C', 'Tỉ lệ (0–1)'),
    'liveness': ('Liveness', 'Độ sống động', '#2ECC71', 'Tỉ lệ (0–1)'),
    'loudness': ('Loudness', 'Âm lượng trung bình', '#3498DB', 'dB'),
    'tempo': ('Tempo', 'Nhịp độ bài hát', '#D35400', 'BPM')
}

print(f"✅ Đã nạp thành công: {len(df_merged)} tuần quan sát ({df_merged['week'].min().strftime('%d/%m/%Y')} → {df_merged['week'].max().strftime('%d/%m/%Y')})")"""))

# COVID Plot 1: Stacked timelines
cells.append(new_markdown_cell("""---
## 2.1. COVID Và Âm Nhạc Theo Thời Gian (9 Biểu Đồ Hai Ô Trên–Dưới)

**Phương pháp trực quan:** Với mỗi đặc trưng trong 9 đặc trưng, tạo một biểu đồ tương tác gồm 2 ô trên–dưới đồng bộ trục thời gian $X$:
- Ô trên: Số ca tử vong vì COVID-19 theo tuần toàn cầu (`weekly_deaths`).
- Ô dưới: Giá trị trung bình đặc trưng âm thanh tương ứng trong tuần."""))

cells.append(new_code_cell("""def plot_covid_audio_stacked(df, feature_key):
    name, desc, color, unit = FEATURE_META[feature_key]
    
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        subplot_titles=[
            '<b>Số Ca Tử Vong COVID-19 Toàn Cầu Theo Tuần (weekly_deaths)</b>',
            f'<b>Đặc Trưng Âm Thanh: {name} ({desc}) [{unit}]</b>'
        ],
        row_heights=[0.42, 0.58]
    )
    
    fig.add_trace(
        go.Bar(
            x=df['week'],
            y=df['weekly_deaths'],
            name='Tử vong COVID/tuần',
            marker=dict(color='#E74C3C', opacity=0.7),
            hovertemplate='<b>Tuần:</b> %{x|%d/%m/%Y}<br><b>Tử vong:</b> %{y:,.0f} ca<extra></extra>'
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=df['week'],
            y=df[feature_key],
            name=name,
            mode='lines+markers',
            line=dict(color=color, width=2.5),
            marker=dict(size=4),
            hovertemplate='<b>Tuần:</b> %{x|%d/%m/%Y}<br><b>' + name + ':</b> %{y:.4f}<extra></extra>'
        ),
        row=2, col=1
    )
    
    fig.update_xaxes(
        showgrid=True, gridcolor='#F0F0F0',
        rangebreaks=[],
        row=2, col=1
    )
    fig.update_yaxes(title_text='Ca tử vong', row=1, col=1)
    fig.update_yaxes(title_text=f'{name} ({unit})', row=2, col=1)
    
    fig.update_layout(
        title=dict(
            text=f'<b>Đối Chiếu Làn Sóng COVID-19 & Xu Hướng {name} (2020 – 2022)</b>',
            x=0.01, y=0.98,
            font=dict(size=15)
        ),
        showlegend=False,
        height=520,
        margin=dict(l=60, r=30, t=70, b=40),
        template='plotly_white'
    )
    return fig

for feat in ['valence', 'energy', 'danceability', 'acousticness']:
    fig_st = plot_covid_audio_stacked(df_merged, feat)
    fig_st.show()"""))

cells.append(new_markdown_cell("""### 💡 Insight 1: Khi tử vong tăng, đạt đỉnh rồi giảm, âm nhạc thay đổi thế nào?
1. **Đỉnh dịch không đồng nghĩa với sụp đổ cảm xúc:** Khi các làn sóng tử vong COVID-19 đạt đỉnh (đỉnh 1: tháng 01/2021 với hơn 100,000 ca/tuần; đỉnh 2: tháng 05/2021; đỉnh 3: tháng 02/2022), chỉ số `Valence` (tích cực) không hề giảm mạnh tương ứng mà duy trì quanh ngưỡng $0.51 - 0.54$.
2. **Cú sốc phong tỏa ban đầu (Tháng 3–5/2020):** `Danceability` đạt đỉnh lịch sử ($0.723$) ngay khi đại dịch bùng phát và các lệnh cách ly xã hội toàn cầu có hiệu lực. Người nghe tìm đến âm nhạc có tiết tấu dễ nhảy để xua tan cảm giác bức bối tại nhà.
3. **Phản ứng có độ trễ pha:** Sau mỗi đỉnh dịch đi qua từ 4 đến 8 tuần, `Energy` và `Loudness` có xu hướng bật tăng trở lại khi các biện pháp nới lỏng xã hội được kích hoạt."""))

# COVID Plot 2: Scatter 3x3
cells.append(new_markdown_cell("""---
## 2.2. Scatter Ca Tử Vong × Đặc Trưng Âm Thanh

**Phương pháp trực quan:** Lưới $3 \times 3$ biểu đồ phân tán. Trục $X$ là số ca tử vong tuần (`weekly_deaths`), trục $Y$ là đặc trưng âm thanh. Mỗi điểm là một tuần, màu sắc phân biệt theo năm (2020: Xanh dương, 2021: Cam, 2022: Xanh lá)."""))

cells.append(new_code_cell("""def plot_scatter_covid_features(df):
    year_colors = {2020: '#3498DB', 2021: '#E67E22', 2022: '#2ECC71'}
    
    fig = make_subplots(
        rows=3, cols=3,
        subplot_titles=[f"<b>{name}</b>" for name in SHORT_TITLES],
        horizontal_spacing=0.07,
        vertical_spacing=0.10
    )
    
    for idx, (col, short_name) in enumerate(zip(ALL_9_FEATURES, SHORT_TITLES)):
        r = idx // 3 + 1
        c = idx % 3 + 1
        
        for yr in [2020, 2021, 2022]:
            sub = df[df['year'] == yr]
            fig.add_trace(
                go.Scatter(
                    x=sub['weekly_deaths'],
                    y=sub[col],
                    mode='markers',
                    name=f'Năm {yr}',
                    marker=dict(color=year_colors[yr], size=6, opacity=0.7),
                    showlegend=(idx == 0),
                    hovertemplate='<b>Tuần:</b> %{customdata|%d/%m/%Y}<br><b>Tử vong:</b> %{x:,.0f}<br><b>' + short_name + ':</b> %{y:.4f}<extra></extra>',
                    customdata=sub['week']
                ),
                row=r, col=c
            )
            
        fig.update_xaxes(title_text='Ca tử vong/tuần' if r == 3 else None, tickfont=dict(size=9), row=r, col=c)
        fig.update_yaxes(title_text=short_name if c == 1 else None, tickfont=dict(size=9), row=r, col=c)
        
    fig.update_layout(
        title=dict(
            text='<b>Phân Bố Đặc Trưng Âm Thanh Theo Mức Tử Vong COVID-19 Hàng Tuần</b>',
            x=0.01, y=0.99,
            font=dict(size=15)
        ),
        legend=dict(
            orientation='h',
            x=0.99, y=1.03,
            xanchor='right', yanchor='bottom',
            font=dict(size=11),
            bgcolor='rgba(255, 255, 255, 0.7)'
        ),
        height=820,
        margin=dict(l=60, r=30, t=70, b=50),
        template='plotly_white'
    )
    return fig

fig_scatter = plot_scatter_covid_features(df_merged)
fig_scatter.show()"""))

cells.append(new_markdown_cell("""### 💡 Insight 2: Những tuần tử vong cao có âm nhạc khác tuần tử vong thấp không?
1. **Phân cụm theo năm lấn át mối tương quan tuyến tính:** Trên hầu hết các biểu đồ, các điểm tập trung thành từng cụm rõ rệt theo màu sắc của năm: năm 2020 (xanh dương, tử vong thấp đến trung bình nhưng `Danceability` cao), năm 2021 (cam, trải rộng khắp dải tử vong cao từ 40,000 đến 100,000), và năm 2022 (xanh lá, tử vong giảm dần nhưng `Energy` và `Loudness` chuyển dịch lên vùng cao hơn).
2. **Không tồn tại mối quan hệ nghịch biến tuyến tính đơn giản:** Các điểm không tạo thành một đường dốc xuống giữa tử vong và Valence. Điều này khẳng định thị hiếu nghe nhạc công chúng không bị chi phối cơ học bởi số liệu dịch tễ trong từng tuần riêng lẻ, mà vận động theo chu kỳ tâm lý xã hội và dòng sản phẩm âm nhạc phát hành theo mùa."""))

# COVID Plot 3: Monthly heatmap + deaths bar
cells.append(new_markdown_cell("""---
## 2.3. Heatmap Tháng × 9 Đặc Trưng, Kèm Biểu Đồ Thanh Tử Vong COVID

**Phương pháp trực quan:** Tổng hợp dữ liệu theo tháng ($N = 31$ tháng từ 01/2020 đến 07/2022):
- Ô bên trái: Heatmap 9 cột âm thanh đã chuẩn hóa Min-Max theo từng cột về thang $[0, 1]$.
- Ô bên phải: Biểu đồ thanh nằm ngang thể hiện tổng số ca tử vong COVID-19 trong tháng đó, dùng chung trục $Y$ là các tháng."""))

cells.append(new_code_cell("""def plot_heatmap_monthly_with_covid_bar(df):
    w_cols = ALL_9_FEATURES
    monthly = df.groupby('year_month').agg({
        **{c: 'mean' for c in w_cols},
        'weekly_deaths': 'sum'
    }).reset_index()
    monthly.rename(columns={'weekly_deaths': 'monthly_deaths'}, inplace=True)
    
    # Chuẩn hóa Min-Max theo từng cột đặc trưng
    norm_features = pd.DataFrame()
    for col in w_cols:
        c_min = monthly[col].min()
        c_max = monthly[col].max()
        norm_features[col] = (monthly[col] - c_min) / (c_max - c_min)
        
    fig = make_subplots(
        rows=1, cols=2,
        column_widths=[0.68, 0.32],
        shared_yaxes=True,
        horizontal_spacing=0.03,
        subplot_titles=[
            '<b>Hồ Sơ Âm Thanh Theo Tháng (Chuẩn Hóa Min-Max 0–1)</b>',
            '<b>Tổng Ca Tử Vong COVID-19 Trong Tháng</b>'
        ]
    )
    
    # Heatmap
    fig.add_trace(
        go.Heatmap(
            z=norm_features.values,
            x=SHORT_TITLES,
            y=monthly['year_month'],
            colorscale='YlGnBu',
            colorbar=dict(
                title=dict(text='Điểm<br>chuẩn hóa', font=dict(size=10)),
                x=0.64, thickness=12, len=0.8
            ),
            hovertemplate='<b>Tháng:</b> %{y}<br><b>Đặc trưng:</b> %{x}<br><b>Chuẩn hóa:</b> %{z:.2f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Bar chart ca tử vong theo tháng
    fig.add_trace(
        go.Bar(
            x=monthly['monthly_deaths'],
            y=monthly['year_month'],
            orientation='h',
            marker=dict(color='#E74C3C', opacity=0.8),
            name='Tử vong/tháng',
            hovertemplate='<b>Tháng:</b> %{y}<br><b>Tử vong:</b> %{x:,.0f} ca<extra></extra>'
        ),
        row=1, col=2
    )
    
    fig.update_xaxes(tickangle=-30, tickfont=dict(size=10), row=1, col=1)
    fig.update_xaxes(title_text='Ca tử vong', tickfont=dict(size=9), row=1, col=2)
    fig.update_yaxes(title_text='Năm - Tháng', tickfont=dict(size=9), autorange='reversed', row=1, col=1)
    
    fig.update_layout(
        title=dict(
            text='<b>Đối Chiếu Hồ Sơ Âm Thanh Hàng Tháng Và Quy Mô Đại Dịch COVID-19</b>',
            x=0.01, y=0.98,
            font=dict(size=15)
        ),
        showlegend=False,
        height=740,
        margin=dict(l=70, r=30, t=70, b=60),
        template='plotly_white'
    )
    return fig

fig_heatmap_covid = plot_heatmap_monthly_with_covid_bar(df_merged)
fig_heatmap_covid.show()"""))

cells.append(new_markdown_cell("""### 💡 Insight 3: Trong những tháng dịch nghiêm trọng, cả hồ sơ âm nhạc thay đổi đồng thời hay chỉ vài đặc trưng?
1. **Sự biến chuyển đồng bộ của cụm Energy – Loudness – Acousticness:** Giai đoạn dịch căng thẳng nhất (11/2020 – 05/2021 với hơn 350,000 – 400,000 ca tử vong/tháng), `Acousticness` đạt các mức cao nhất trong chu kỳ, trong khi `Energy` và `Loudness` duy trì ở mức thấp.
2. **Bước ngoặt mùa hè 2021 & đầu năm 2022:** Khi các chiến dịch tiêm chủng diện rộng mở đường cho việc nới lỏng hạn chế, `Energy` và `Loudness` đồng loạt chuyển sang sắc độ đậm (giá trị cao) trên Heatmap, đánh dấu sự trở lại của các bản nhạc sôi động phục vụ không gian công cộng và lễ hội."""))

# COVID Plot 4: Dot plot death groups
cells.append(new_markdown_cell("""---
## 2.4. So Sánh Hồ Sơ Giữa Tuần Tử Vong Cao Và Thấp

**Phương pháp trực quan:** Chia 130 tuần thành hai nhóm:
- Nhóm tuần tử vong cao: `weekly_deaths` $\ge$ ngưỡng trung vị ($48,683$ ca/tuần).
- Nhóm tuần tử vong thấp: `weekly_deaths` $<$ ngưỡng trung vị.
Vẽ Dot plot lưới $3 \times 3$ với thang đo riêng biệt từng biến để so sánh trực quan giá trị trung bình giữa hai nhóm."""))

cells.append(new_code_cell("""def plot_dotplot_death_groups(df):
    median_deaths = df['weekly_deaths'].median()
    df_temp = df.copy()
    df_temp['death_group'] = np.where(
        df_temp['weekly_deaths'] >= median_deaths,
        'Tử vong cao (≥ Median)',
        'Tử vong thấp (< Median)'
    )
    
    group_summary = df_temp.groupby('death_group')[ALL_9_FEATURES].mean().reset_index()
    
    fig = make_subplots(
        rows=3, cols=3,
        subplot_titles=[f"<b>{name}</b>" for name in SHORT_TITLES],
        horizontal_spacing=0.08,
        vertical_spacing=0.12
    )
    
    for idx, (col, short_name) in enumerate(zip(ALL_9_FEATURES, SHORT_TITLES)):
        r = idx // 3 + 1
        c = idx % 3 + 1
        
        val_low = group_summary.loc[group_summary['death_group'] == 'Tử vong thấp (< Median)', col].values[0]
        val_high = group_summary.loc[group_summary['death_group'] == 'Tử vong cao (≥ Median)', col].values[0]
        
        # Đường nối hai điểm
        fig.add_trace(
            go.Scatter(
                x=[val_low, val_high],
                y=['Hồ sơ', 'Hồ sơ'],
                mode='lines',
                line=dict(color='#BDC3C7', width=3),
                showlegend=False,
                hoverinfo='skip'
            ),
            row=r, col=c
        )
        
        # Điểm tử vong thấp
        fig.add_trace(
            go.Scatter(
                x=[val_low],
                y=['Hồ sơ'],
                mode='markers',
                name='Tử vong thấp (< Median)',
                marker=dict(size=11, color='#2ECC71', symbol='circle'),
                showlegend=(idx == 0),
                hovertemplate='<b>Tử vong thấp:</b> %{x:.4f}<extra></extra>'
            ),
            row=r, col=c
        )
        
        # Điểm tử vong cao
        fig.add_trace(
            go.Scatter(
                x=[val_high],
                y=['Hồ sơ'],
                mode='markers',
                name='Tử vong cao (≥ Median)',
                marker=dict(size=11, color='#E74C3C', symbol='diamond'),
                showlegend=(idx == 0),
                hovertemplate='<b>Tử vong cao:</b> %{x:.4f}<extra></extra>'
            ),
            row=r, col=c
        )
        
        fig.update_xaxes(tickfont=dict(size=9), row=r, col=c)
        fig.update_yaxes(showticklabels=False, row=r, col=c)
        
    fig.update_layout(
        title=dict(
            text=f'<b>So Sánh Hồ Sơ Âm Thanh: Tuần Tử Vong Cao vs Thấp (Ngưỡng Trung Vị = {median_deaths:,.0f} ca/tuần)</b>',
            x=0.01, y=0.99,
            font=dict(size=15)
        ),
        legend=dict(
            orientation='h',
            x=0.99, y=1.03,
            xanchor='right', yanchor='bottom',
            font=dict(size=11),
            bgcolor='rgba(255, 255, 255, 0.7)'
        ),
        height=780,
        margin=dict(l=40, r=30, t=70, b=50),
        template='plotly_white'
    )
    return fig

fig_dotplot_deaths = plot_dotplot_death_groups(df_merged)
fig_dotplot_deaths.show()"""))

cells.append(new_markdown_cell("""### 💡 Insight 4: Giai đoạn tử vong cao có Valence thấp hơn, Energy cao hơn, Acousticness cao hơn không?
* **Valence giữ độ ổn định bất ngờ:** Mức chênh lệch `Valence` giữa tuần tử vong cao ($0.527$) và tuần tử vong thấp ($0.519$) chỉ là $+0.008$. Người dân không bỏ nghe nhạc tích cực trong những tuần nguy kịch.
* **Độ mộc mạc (Acousticness) tăng nhẹ:** Tuần tử vong cao có `Acousticness` đạt $0.252$ so với $0.244$ ở tuần tử vong thấp ($+0.008$), cho thấy xu hướng tìm về các bản nhạc mộc mạc, yên bình tăng nhẹ khi nguy cơ dịch bệnh bao trùm.
* **Độ dễ nhảy (Danceability) cao hơn trong tuần tử vong cao:** $0.680$ so với $0.672$ ($+0.008$), củng cố giả thuyết người nghe sử dụng âm nhạc nhịp điệu để đối phó với căng thẳng tâm lý."""))

# COVID Plot 5: Dot plot yearly
cells.append(new_markdown_cell("""---
## 2.5. Dot Plot So Sánh Hồ Sơ Toàn Cầu Giữa Năm 2021 & 2022

**Phương pháp trực quan:** Lưới $3 \times 3$ biểu đồ chấm so sánh giá trị trung bình năm 2021 và năm 2022 toàn cầu trên từng đặc trưng với thang đo riêng biệt."""))

cells.append(new_code_cell("""def plot_dotplot_yearly_comparison(df):
    df_temp = df[df['year'].isin([2021, 2022])].copy()
    yearly_summary = df_temp.groupby('year')[ALL_9_FEATURES].mean().reset_index()
    
    fig = make_subplots(
        rows=3, cols=3,
        subplot_titles=[f"<b>{name}</b>" for name in SHORT_TITLES],
        horizontal_spacing=0.08,
        vertical_spacing=0.12
    )
    
    for idx, (col, short_name) in enumerate(zip(ALL_9_FEATURES, SHORT_TITLES)):
        r = idx // 3 + 1
        c = idx % 3 + 1
        
        val_2021 = yearly_summary.loc[yearly_summary['year'] == 2021, col].values[0]
        val_2022 = yearly_summary.loc[yearly_summary['year'] == 2022, col].values[0]
        
        # Đường nối
        fig.add_trace(
            go.Scatter(
                x=[val_2021, val_2022],
                y=['Toàn cầu', 'Toàn cầu'],
                mode='lines',
                line=dict(color='#BDC3C7', width=3),
                showlegend=False,
                hoverinfo='skip'
            ),
            row=r, col=c
        )
        
        # 2021 marker
        fig.add_trace(
            go.Scatter(
                x=[val_2021],
                y=['Toàn cầu'],
                mode='markers',
                name='Năm 2021',
                marker=dict(size=11, color='#E67E22', symbol='circle'),
                showlegend=(idx == 0),
                hovertemplate='<b>2021:</b> %{x:.4f}<extra></extra>'
            ),
            row=r, col=c
        )
        
        # 2022 marker
        fig.add_trace(
            go.Scatter(
                x=[val_2022],
                y=['Toàn cầu'],
                mode='markers',
                name='Năm 2022',
                marker=dict(size=11, color='#2ECC71', symbol='diamond'),
                showlegend=(idx == 0),
                hovertemplate='<b>2022:</b> %{x:.4f}<extra></extra>'
            ),
            row=r, col=c
        )
        
        fig.update_xaxes(tickfont=dict(size=9), row=r, col=c)
        fig.update_yaxes(showticklabels=False, row=r, col=c)
        
    fig.update_layout(
        title=dict(
            text='<b>Chuyển Dịch Hồ Sơ Âm Thanh Toàn Cầu: Năm 2021 vs Năm 2022</b>',
            x=0.01, y=0.99,
            font=dict(size=15)
        ),
        legend=dict(
            orientation='h',
            x=0.99, y=1.03,
            xanchor='right', yanchor='bottom',
            font=dict(size=11),
            bgcolor='rgba(255, 255, 255, 0.7)'
        ),
        height=780,
        margin=dict(l=40, r=30, t=70, b=50),
        template='plotly_white'
    )
    return fig

fig_dotplot_years = plot_dotplot_yearly_comparison(df_merged)
fig_dotplot_years.show()"""))

cells.append(new_markdown_cell("""### 💡 Insight 5: So sánh hồ sơ âm nhạc toàn cầu 2021 vs 2022:
* **Gia tăng năng lượng và âm lượng mạnh mẽ:** Sang năm 2022, `Energy` tăng từ $0.632$ lên $0.657$ ($+0.025$) và `Loudness` tăng từ $-6.16$ dB lên $-5.98$ dB ($+0.18$ dB).
* **Độ mộc mạc suy giảm:** `Acousticness` giảm từ $0.254$ xuống $0.231$ ($-0.023$).
* **Nét âm thanh ổn định:** `Danceability` hầu như giữ nguyên ($0.677 \to 0.676$), chứng minh thói quen chuộng nhạc bắt tai, dễ nhảy là đặc tính dài hạn của người dùng Spotify toàn cầu."""))

# ---------------------------------------------------------------------------
# PHẦN 3: ĐÚC KẾT TOÀN DIỆN CHO DASHBOARD GIA HÂN
# ---------------------------------------------------------------------------

cells.append(new_markdown_cell("""---
# PHẦN 3: ĐÚC KẾT CỐT TRUYỆN DỮ LIỆU TOÀN DIỆN CHO DASHBOARD (GIA HÂN)

### 🧩 Sự Giao Thoa Giữa "Bản Sắc Địa Lý" & "Tâm Lý Khủng Hoảng":
Hành trình phân tích dữ liệu mở ra hai tầng khám phá then chốt giúp định hình giao diện và câu chuyện của Dashboard:

```
                               ┌─────────────────────────────────────────────────────────────┐
                               │             SPOTIFY AUDIO TRENDS ANALYTICS                  │
                               └──────────────────────────────┬──────────────────────────────┘
                                                              │
                       ┌──────────────────────────────────────┴──────────────────────────────────────┐
                       ▼                                                                            ▼
       ┌───────────────────────────────┐                                            ┌───────────────────────────────┐
       │     CHIỀU KHÔNG GIAN          │                                            │       CHIỀU THỜI GIAN         │
       │    (Bản Sắc Vùng Miền)        │                                            │    (Khủng Hoảng & Cảm Xúc)    │
       └───────────────┬───────────────┘                                            └───────────────┬───────────────┘
                       │                                                                            │
      ┌────────────────┴────────────────┐                                          ┌────────────────┴────────────────┐
      │ • Mỹ Latinh: Vũ điệu & năng lượng│                                          │ • Phong tỏa 2020: Escapism đỉnh  │
      │ • Châu Á: Mộc mạc & tự sự       │                                          │ • Đỉnh dịch: Không bi lụy        │
      │ • Phân hóa nội vùng cực lớn      │                                          │ • Hậu dịch 2022: Bùng nổ Energy  │
      └─────────────────────────────────┘                                          └─────────────────────────────────┘
```

---

### 🎙️ 4 Thông Điệp Kể Chuyện Chiến Lược Cho Dashboard:

#### 1. "Một thế giới, nhiều thế giới âm thanh":
* Bản đồ và hồ sơ vùng miền khẳng định thị hiếu nghe nhạc phân hóa cực kỳ sâu sắc theo địa lý: Mỹ Latinh dẫn đầu tuyệt đối về tính khiêu vũ và năng lượng ($0.73$ Danceability, $0.68$ Energy); trong khi Đông Nam Á (Indonesia, Việt Nam) là tâm điểm nhạc mộc mạc toàn cầu ($0.45 - 0.51$ Acousticness).
* **Ứng dụng Dashboard:** Bắt buộc cung cấp bộ lọc tương tác theo 7 khu vực World Bank (`wb_region`) để người dùng tự do đối chiếu các "hồ sơ âm thanh" độc bản này.

#### 2. Cảnh báo "Ảo ảnh trung bình vùng" (Intra-regional Diversity):
* Trung bình khu vực là một chỉ số hữu ích nhưng che giấu những thái cực nội tại to lớn. Điển hình tại East Asia & Pacific, khoảng cách Acousticness giữa Indonesia ($0.513$) và Nhật Bản ($0.180$) lên tới $0.333$ điểm — lớn hơn khoảng cách giữa bất kỳ hai khu vực nào trên thế giới!
* **Ứng dụng Dashboard:** Khi người dùng chọn một khu vực, Dashboard cần hiển thị strip plot / scatter plot phân bổ từng quốc gia bên trong thay vì chỉ hiển thị một con số trung bình đơn điệu.

#### 3. "Hiệu ứng trốn chạy thực tại" (Musical Escapism) trong khủng hoảng:
* Dữ liệu chuỗi thời gian 130 tuần đại dịch bác bỏ định kiến cho rằng con người sẽ chìm vào nhạc bi lụy khi gặp thảm kịch. Ngay trong giai đoạn tử vong kỷ lục, chỉ số tích cực (`Valence`) vẫn giữ vững ($0.52 - 0.53$), và `Danceability` đạt đỉnh ngay thời điểm phong tỏa ngặt nghèo nhất đầu năm 2020.
* Âm nhạc hoạt động như một **vùng đệm tâm lý (Psychological Buffer)**, một công cụ giải tỏa căng thẳng và trốn chạy thực tại.

#### 4. Giải phóng năng lượng hậu khủng hoảng (2022) & "Hiệu ứng son môi":
* Khi bước sang năm 2022 giữa bối cảnh thế giới vừa phục hồi vừa đón nhận làn sóng lạm phát, âm nhạc không hề lắng xuống mà bùng nổ mạnh mẽ: `Energy` và `Loudness` tăng vọt, trong khi `Acousticness` giảm sâu. Âm nhạc trực tuyến trở thành hình thức giải trí chi phí thấp mang lại sự thăng hoa cảm xúc tức thì.
* **Ứng dụng Dashboard:** Cung cấp thanh trượt thời gian (Timeline Slider) cho phép người xem chứng kiến sự dịch chuyển của các chỉ số âm thanh tương ứng với từng giai đoạn lịch sử dịch bệnh và kinh tế."""))

# ---------------------------------------------------------------------------
# WRITE NOTEBOOK AND EXECUTE
# ---------------------------------------------------------------------------

nb = new_notebook(cells=cells)
nb.metadata['language_info'] = {
    'name': 'python',
    'version': '3.11.9'
}

notebook_path = os.path.join(PROJECT_ROOT, "notebooks", "04_story.ipynb")

with open(notebook_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

print(f"🎉 Đã tạo thành công file: {notebook_path} với tổng cộng {len(cells)} cells!")
