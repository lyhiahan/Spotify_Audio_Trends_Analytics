import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Cau hinh trang Streamlit
st.set_page_config(
    page_title="Tổng Quan Dữ Liệu | Spotify Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# He thong CSS phong cach Spotify Bento Grid
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,500;0,600;0,700;0,800;0,900;1,700&family=Be+Vietnam+Pro:ital,wght@0,500;0,600;0,700;0,800;0,900;1,700&display=swap');

    html, body, .stApp {
        font-family: 'Times New Roman', Times, Georgia, serif !important;
        background-color: #0d0d0d !important;
        color: #ffffff !important;
    }

    [data-testid="stIconMaterial"],
    [data-testid="stExpanderToggleIcon"],
    .material-symbols-rounded,
    .material-symbols-outlined,
    .material-icons {
        font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
    }

    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    .stDeployButton {display: none !important;}
    [data-testid="stSidebar"],
    [data-testid="stSidebarCollapsedControl"],
    section[data-testid="stSidebar"],
    div[data-testid="collapsedControl"],
    div[data-testid="stSidebarNav"],
    div[data-testid="stSidebarNavSeparator"],
    div[data-testid="stSidebarNavItems"] {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
        position: absolute !important;
        left: -9999px !important;
        pointer-events: none !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #141414 !important;
        border: 1px solid #282828 !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        margin-bottom: 20px !important;
    }

    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2.2rem !important;
        padding-right: 2.2rem !important;
        max-width: 100% !important;
    }

    h1, h2, h3 {
        font-family: 'Montserrat', 'Be Vietnam Pro', sans-serif !important;
        font-weight: 800 !important;
        letter-spacing: -0.6px !important;
        color: #ffffff !important;
    }

    p, span, label {
        font-family: 'Times New Roman', Times, serif !important;
        color: #b3b3b3;
    }

    .bento-card {
        background-color: #161616;
        border: 1px solid #242424;
        border-radius: 14px;
        padding: 18px 20px;
        margin-bottom: 16px;
        transition: all 0.2s ease;
    }
    .bento-card:hover {
        border-color: #333333;
    }

    .slot-card {
        background-color: #161616;
        border: 1px dashed #2f2f2f;
        border-radius: 14px;
        padding: 16px 18px;
        margin-bottom: 16px;
        transition: border-color 0.2s;
    }
    .slot-card:hover {
        border-color: #1DB954;
    }

    .metric-item {
        background-color: #1a1a1a;
        border: 1px solid #262626;
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 10px;
        transition: transform 0.15s, border-color 0.15s;
    }
    .metric-item:hover {
        border-color: #1DB954;
        transform: translateX(3px);
    }
    .metric-num {
        font-size: 1.45rem;
        font-weight: 800;
        color: #1DB954;
        line-height: 1.2;
    }
    .metric-label {
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.7px;
        color: #888888;
    }

    .player-card {
        background: linear-gradient(135deg, #0e2a18 0%, #161616 100%);
        border: 1px solid #1DB954;
        border-radius: 14px;
        padding: 20px;
        position: relative;
        overflow: hidden;
    }
    .player-title {
        font-size: 1.15rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 2px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .player-artist {
        font-size: 0.85rem;
        color: #1DB954;
        font-weight: 600;
        margin-bottom: 14px;
    }
    .player-progress {
        background: #282828;
        height: 5px;
        border-radius: 3px;
        margin-bottom: 12px;
        overflow: hidden;
    }
    .player-progress-bar {
        background: #1DB954;
        height: 100%;
        border-radius: 3px;
    }
    .player-controls {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 18px;
        font-size: 1.25rem;
        color: #ffffff;
    }

    .member-card {
        background: #181818;
        border: 1px solid #242424;
        border-radius: 10px;
        padding: 10px 14px;
        margin-bottom: 8px;
    }
    .member-name {
        font-size: 0.88rem;
        font-weight: 700;
        color: #ffffff;
    }
    .member-id {
        font-size: 0.78rem;
        font-weight: 600;
        color: #1DB954;
    }
    .member-role {
        font-size: 0.72rem;
        color: #777777;
    }
</style>
""", unsafe_allow_html=True)

# Bo layout theme chung cho Plotly Charts
PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#b3b3b3", size=11),
    hoverlabel=dict(
        bgcolor="#181818",
        bordercolor="#1DB954",
        font=dict(family="Inter, sans-serif", color="#ffffff", size=12)
    )
)

# Ham nap du lieu
@st.cache_data(show_spinner="Đang nạp dữ liệu tổng quan...")
def load_data():
    processed_path = os.path.join("data", "processed", "merged_spotify_data.csv")
    sample_path = os.path.join("data", "sample", "spotify_sample_merged.csv")
    path = processed_path if os.path.exists(processed_path) else sample_path
    
    needed_cols = [
        "track_name", "artist_individual", "streams", "rank", "week", "year", "month",
        "danceability", "energy", "valence", "duration_min", "explicit",
        "popularity", "income_group", "region_wb", "track_genre"
    ]
    df = pd.read_csv(path, usecols=lambda c: c in needed_cols, low_memory=False)
    df["week"] = pd.to_datetime(df["week"], errors="coerce")
    df = df.dropna(subset=["track_name", "artist_individual", "week"])
    return df

df = load_data()

# Header tieu de
st.title("Tổng Quan Dữ Liệu Thị Trường Âm Nhạc")
st.markdown("<p style='font-size:0.95rem; color:#888888; margin-top:-6px; margin-bottom:20px;'>Bảng điều khiển trực quan tương tác chuẩn Bento Grid phong cách Spotify Web Player</p>", unsafe_allow_html=True)

# Bo loc toan he thong ngay dau trang
with st.container(border=True):
    st.markdown("""
    <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:8px;">
        <div style="font-size:0.85rem; font-weight:700; color:#ffffff;">Bộ lọc dữ liệu thị trường</div>
        <span style="font-size:0.75rem; color:#777777;">Tự động cập nhật các biểu đồ và danh sách bài hát bên dưới</span>
    </div>
    """, unsafe_allow_html=True)
    f_c1, f_c2, f_c3 = st.columns([1, 1, 1], gap="medium")
    with f_c1:
        regions = ["Tất cả khu vực"] + sorted([r for r in df["region_wb"].dropna().unique() if str(r).strip()])
        sel_region = st.selectbox("Khu vực địa lý:", regions)
    with f_c2:
        genres = ["Tất cả thể loại"] + sorted([g for g in df["track_genre"].dropna().unique() if str(g).strip()][:30])
        sel_genre = st.selectbox("Thể loại âm nhạc:", genres)
    with f_c3:
        years = ["Tất cả các năm"] + sorted([str(int(y)) for y in df["year"].dropna().unique()])
        sel_year = st.selectbox("Năm khảo sát:", years)

# Loc du lieu
df_view = df.copy()
if sel_region != "Tất cả khu vực":
    df_view = df_view[df_view["region_wb"] == sel_region]
if sel_genre != "Tất cả thể loại":
    df_view = df_view[df_view["track_genre"] == sel_genre]
if sel_year != "Tất cả các năm":
    df_view = df_view[df_view["year"] == int(sel_year)]

# KHU VUC BENTO GRID CHINH (3 COT)
col_left, col_mid, col_right = st.columns([1.1, 1.2, 1.7], gap="medium")

# COT 1: TRACK DRAWER (DANH SACH CA KHUC THINH HANH BEN TRAI)
with col_left:
    st.markdown("""
    <div class="bento-card">
        <p style='font-size:0.8rem; font-weight:700; color:#888888; text-transform:uppercase; margin-bottom:6px;'>DANH SÁCH BÀI HÁT</p>
        <p style='font-size:0.75rem; color:#666666; margin-bottom:12px;'>Chọn bài hát để đồng bộ Widget nghe nhạc</p>
    """, unsafe_allow_html=True)
    
    top_tracks = df_view.groupby(["track_name", "artist_individual"])["streams"].sum().reset_index()
    top_tracks = top_tracks.sort_values(by="streams", ascending=False).head(30)
    
    track_options = [f"{row['track_name']} — {row['artist_individual']}" for _, row in top_tracks.iterrows()]
    selected_track_str = st.selectbox(
        "Chọn bài hát:",
        options=track_options,
        index=0,
        label_visibility="collapsed"
    )
    
    sel_track_name = selected_track_str.split(" — ")[0]
    sel_artist_name = selected_track_str.split(" — ")[1]
    
    # Lay thong tin chi tiet ca khuc dang chon
    sel_track_data = df_view[(df_view["track_name"] == sel_track_name) & (df_view["artist_individual"] == sel_artist_name)].iloc[0]
    
    st.markdown(f"""
        <hr style='border-color:#242424; margin:12px 0;'>
        <p style='font-size:0.75rem; color:#888888;'>Thể loại: <b style='color:#ffffff;'>{sel_track_data.get('track_genre', 'Pop')}</b></p>
        <p style='font-size:0.75rem; color:#888888;'>Tổng stream: <b style='color:#1DB954;'>{sel_track_data['streams']:,.0f}</b></p>
        <p style='font-size:0.75rem; color:#888888;'>Thứ hạng đỉnh cao: <b style='color:#ffffff;'>#{sel_track_data['rank']}</b></p>
    </div>
    """, unsafe_allow_html=True)

# COT 2: 4 THE KPIS DOC + WIDGET SPOTIFY NOW PLAYING
with col_mid:
    # 4 The KPI xep doc
    kpi_col1, kpi_col2 = st.columns(2)
    with kpi_col1:
        st.markdown(f"""
        <div class="metric-item">
            <div class="metric-label">BÀI HÁT KHẢO SÁT</div>
            <div class="metric-num">{df_view['track_name'].nunique():,}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="metric-item">
            <div class="metric-label">THỜI LƯỢNG TRUNG BÌNH</div>
            <div class="metric-num">{df_view['duration_min'].mean():.2f}m</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi_col2:
        st.markdown(f"""
        <div class="metric-item">
            <div class="metric-label">NGHỆ SĨ GHI NHẬN</div>
            <div class="metric-num">{df_view['artist_individual'].nunique():,}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="metric-item">
            <div class="metric-label">ĐỘ PHỔ BIẾN TB</div>
            <div class="metric-num">{df_view['popularity'].mean():.0f}/100</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Widget Now Playing Card
    dance_pct = int(sel_track_data.get('danceability', 0.7) * 100)
    energy_pct = int(sel_track_data.get('energy', 0.6) * 100)
    valence_pct = int(sel_track_data.get('valence', 0.5) * 100)
    
    st.markdown(f"""
    <div class="player-card">
        <p style='font-size:0.7rem; color:#1DB954; font-weight:700; text-transform:uppercase; margin-bottom:6px;'>ĐANG KHẢO SÁT (NOW PLAYING)</p>
        <div class="player-title">{sel_track_name}</div>
        <div class="player-artist">{sel_artist_name}</div>
        
        <div class="player-progress">
            <div class="player-progress-bar" style="width: {dance_pct}%;"></div>
        </div>
        
        <div style="font-size:0.75rem; color:#888888; display:flex; justify-content:space-between; margin-bottom:12px;">
            <span>Dance: {dance_pct}%</span>
            <span>Energy: {energy_pct}%</span>
            <span>Valence: {valence_pct}%</span>
        </div>
        
        <div class="player-controls">
            <span>⏮</span>
            <span style="font-size:1.6rem; color:#1DB954;">▶</span>
            <span>⏭</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# COT 3: BO DONUT CHARTS & MONTHLY BREAKDOWN
with col_right:
    donut_c1, donut_c2 = st.columns(2)
    
    with donut_c1:
        st.markdown('<div class="slot-card">', unsafe_allow_html=True)
        st.markdown("<p style='font-size:0.8rem; font-weight:700; color:#ffffff; margin-bottom:0;'>SLOT 1: TỶ LỆ EXPLICIT (18+)</p>", unsafe_allow_html=True)
        st.caption("Chỗ này dành cho Gia Hân vẽ Donut Chart Explicit")
        
        # CODE MAU DONUT CHART (Gia Han co the tuy bien lai)
        if "explicit" in df_view.columns:
            explicit_counts = df_view["explicit"].value_counts().reset_index()
            explicit_counts.columns = ["Type", "Count"]
            explicit_counts["Type"] = explicit_counts["Type"].map({True: "Explicit", False: "Clean"})
            
            fig_donut1 = px.pie(
                explicit_counts, values="Count", names="Type",
                hole=0.68,
                color="Type",
                color_discrete_map={"Explicit": "#1DB954", "Clean": "#2a2a2a"}
            )
            fig_donut1.update_layout(
                **PLOTLY_THEME,
                height=170,
                showlegend=False,
                margin=dict(t=10, b=10, l=10, r=10)
            )
            fig_donut1.update_traces(textinfo="label+percent", textfont=dict(size=10, color="#ffffff"))
            st.plotly_chart(fig_donut1, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with donut_c2:
        st.markdown('<div class="slot-card">', unsafe_allow_html=True)
        st.markdown("<p style='font-size:0.8rem; font-weight:700; color:#ffffff; margin-bottom:0;'>SLOT 2: PHÂN BỔ NHÓM THU NHẬP</p>", unsafe_allow_html=True)
        st.caption("Chỗ này dành cho Gia Hân vẽ Donut Income")
        
        # CODE MAU DONUT CHART 2 (Gia Han co the tuy bien lai)
        if "income_group" in df_view.columns:
            income_counts = df_view["income_group"].value_counts().head(3).reset_index()
            income_counts.columns = ["Income", "Count"]
            
            fig_donut2 = px.pie(
                income_counts, values="Count", names="Income",
                hole=0.68,
                color_discrete_sequence=["#1DB954", "#8e44ad", "#34495e"]
            )
            fig_donut2.update_layout(
                **PLOTLY_THEME,
                height=170,
                showlegend=False,
                margin=dict(t=10, b=10, l=10, r=10)
            )
            fig_donut2.update_traces(textinfo="percent", textfont=dict(size=10, color="#ffffff"))
            st.plotly_chart(fig_donut2, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # SLOT 3: MONTHLY BREAKDOWN BAR CHART (Giong hinh 1 ban gui)
    st.markdown('<div class="slot-card">', unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.82rem; font-weight:700; color:#ffffff; margin-bottom:0;'>SLOT 3: STREAMS BY MONTH (PHÂN BỔ LƯỢT NGHE THEO THÁNG)</p>", unsafe_allow_html=True)
    st.caption("Chỗ này dành cho Gia Hân vẽ Bar Chart màu tím giống Ảnh 1 tham khảo")
    
    # CODE MAU BAR CHART PURPLE (Gia Han co the thay the hoac tuy bien)
    df_view["month_name"] = df_view["week"].dt.strftime("%b")
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_streams = df_view.groupby("month_name")["streams"].sum().reindex(month_order).dropna().reset_index()
    
    fig_month = px.bar(
        monthly_streams, x="month_name", y="streams",
        color_discrete_sequence=["#9b51e0"]
    )
    fig_month.update_layout(
        **PLOTLY_THEME,
        height=180,
        margin=dict(t=15, b=20, l=20, r=20),
        xaxis=dict(title="", showgrid=False),
        yaxis=dict(title="", showgrid=True, gridcolor="#222222")
    )
    fig_month.update_traces(marker=dict(line=dict(width=0), opacity=0.9))
    st.plotly_chart(fig_month, width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<hr style='border-color:#222222; margin:22px 0;'>", unsafe_allow_html=True)

# HANG DUOI CUNG: 2 BIỂU ĐỒ DIỆN RỘNG (SLOT 4 & SLOT 5)
col_b1, col_b2 = st.columns([1.2, 1], gap="medium")

with col_b1:
    st.markdown('<div class="slot-card">', unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.88rem; font-weight:700; color:#ffffff; margin-bottom:2px;'>SLOT 4: CUMULATIVE & YEARLY GROWTH (TĂNG TRƯỞNG LƯỢT NGHE)</p>", unsafe_allow_html=True)
    st.caption("Chỗ này dành cho Gia Hân vẽ Area Spline Chart mượt mà giống Ảnh 2 tham khảo")
    
    # CODE MAU AREA SPLINE (Gia Han co the tuy bien)
    weekly_trend = df_view.groupby(pd.Grouper(key="week", freq="W"))["streams"].sum().reset_index()
    
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=weekly_trend["week"], y=weekly_trend["streams"],
        mode="lines",
        name="Lượt nghe hàng tuần",
        line=dict(color="#f39c12", width=2.5, shape="spline"),
        fill="tozeroy",
        fillcolor="rgba(243, 156, 18, 0.12)"
    ))
    fig_trend.update_layout(
        **PLOTLY_THEME,
        height=280,
        margin=dict(t=20, b=20, l=30, r=20),
        xaxis=dict(gridcolor="#1f1f1f"),
        yaxis=dict(gridcolor="#1f1f1f")
    )
    st.plotly_chart(fig_trend, width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)

with col_b2:
    st.markdown('<div class="slot-card">', unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.88rem; font-weight:700; color:#ffffff; margin-bottom:2px;'>SLOT 5: TOP CA KHÚC DẪN ĐẦU THỊ PHẦN (HORIZONTAL BARS)</p>", unsafe_allow_html=True)
    st.caption("Chỗ này dành cho Gia Hân vẽ Horizontal Bar Chart xếp hạng bài hát")
    
    # CODE MAU HORIZONTAL BAR CHART (Gia Han co the tuy bien)
    top_songs = df_view.groupby("track_name")["streams"].sum().nlargest(8).reset_index().sort_values(by="streams", ascending=True)
    
    fig_top = go.Figure(go.Bar(
        x=top_songs["streams"],
        y=top_songs["track_name"],
        orientation="h",
        marker=dict(color="#1DB954", line=dict(width=0))
    ))
    fig_top.update_layout(
        **PLOTLY_THEME,
        height=280,
        margin=dict(t=20, b=20, l=10, r=20),
        xaxis=dict(gridcolor="#1f1f1f"),
        yaxis=dict(gridcolor="rgba(0,0,0,0)")
    )
    st.plotly_chart(fig_top, width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)
