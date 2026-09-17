import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# Cấu hình trang với layout rộng
st.set_page_config(
    page_title="Đặc Trưng Âm Thanh & Dự Báo Thịnh Hành | Spotify Analytics",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hệ thống Design System cao cấp phong cách Spotify Dark Theme
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
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
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
        font-weight: 400 !important;
        color: #b3b3b3;
    }

    .section-header {
        display: flex;
        align-items: baseline;
        gap: 12px;
        border-bottom: 1px solid #222222;
        padding-bottom: 8px;
        margin-top: 18px;
        margin-bottom: 16px;
    }
    .section-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.3px;
        margin: 0;
    }
    .section-desc {
        font-size: 0.85rem;
        color: #777777;
        margin: 0;
    }

    .metric-card {
        background-color: #181818;
        border: 1px solid #282828;
        border-radius: 12px;
        padding: 16px 20px;
        transition: all 0.2s ease-in-out;
    }
    .metric-card:hover {
        border-color: #1DB954;
        background-color: #1e1e1e;
        transform: translateY(-2px);
    }
    .metric-label {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #888888;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 1.65rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #1DB954;
        line-height: 1.2;
    }
    .metric-sub {
        font-size: 0.75rem;
        color: #666666;
        margin-top: 4px;
    }

    .surface-card {
        background-color: #161616;
        border: 1px solid #262626;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 20px;
    }

    .member-card {
        background: #181818;
        border: 1px solid #242424;
        border-radius: 10px;
        padding: 10px 14px;
        margin-bottom: 8px;
        transition: border-color 0.2s;
    }
    .member-card:hover {
        border-color: #1DB954;
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

    div[role="radiogroup"] {
        background-color: #161616;
        padding: 4px;
        border-radius: 30px;
        border: 1px solid #282828;
        display: inline-flex !important;
        gap: 6px;
    }
    div[role="radiogroup"] > label {
        background-color: transparent;
        padding: 8px 22px !important;
        border-radius: 24px !important;
        margin: 0 !important;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    div[role="radiogroup"] > label:hover {
        background-color: #222222;
    }
    div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }
    div[role="radiogroup"] > label [data-testid="stMarkdownContainer"] p {
        font-size: 0.88rem !important;
        font-weight: 500 !important;
        color: #b3b3b3 !important;
    }
    div[role="radiogroup"] > label[data-checked="true"],
    div[role="radiogroup"] > label:has(input:checked) {
        background-color: #1DB954 !important;
    }
    div[role="radiogroup"] > label:has(input:checked) [data-testid="stMarkdownContainer"] p {
        color: #000000 !important;
        font-weight: 700 !important;
    }

    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #242424;
    }

    /* DARK THEME SELECTBOX (Bo hoan toan mau trang mac dinh) */
    div[data-testid="stSelectbox"] > div,
    div[data-testid="stSelectbox"] > div > div,
    div[data-baseweb="select"],
    div[data-baseweb="select"] > div,
    div[data-baseweb="select"] div,
    div[data-baseweb="select"] input {
        background-color: #161616 !important;
        background: #161616 !important;
        border: 1px solid #2e2e2e !important;
        border-radius: 8px !important;
        color: #ffffff !important;
    }
    div[data-baseweb="select"]:hover,
    div[data-baseweb="select"]:focus-within {
        border-color: #1DB954 !important;
    }
    div[data-baseweb="select"] * {
        color: #ffffff !important;
        background-color: transparent !important;
    }
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    div[data-baseweb="popover"] div,
    ul[role="listbox"],
    li[role="option"] {
        background-color: #161616 !important;
        background: #161616 !important;
        border: 1px solid #333333 !important;
        border-radius: 8px !important;
        color: #cccccc !important;
    }
    li[role="option"]:hover,
    li[role="option"][aria-selected="true"] {
        background-color: #242424 !important;
        background: #242424 !important;
        color: #1DB954 !important;
    }
    div[data-baseweb="select"] svg {
        fill: #1DB954 !important;
    }

    /* DONG NHAT MAU NHAN SPOTIFY GREEN CHO SLIDER (Khong dung do/hong) */
    div[data-testid="stSlider"] div[role="slider"] {
        background-color: #1DB954 !important;
        border: 2px solid #1DB954 !important;
        box-shadow: 0 0 10px rgba(29, 185, 84, 0.5) !important;
    }
    div[data-testid="stSlider"] div[data-baseweb="slider"] div[style*="background"] {
        background: #1DB954 !important;
    }
    div[data-testid="stSlider"] div[data-baseweb="slider"] > div > div:first-child {
        background: #1DB954 !important;
    }
    div[data-testid="stSlider"] [data-testid="stThumbValue"] {
        color: #1DB954 !important;
        font-weight: 700 !important;
    }
    div[data-baseweb="slider"] div {
        background-color: #1DB954 !important;
    }

    /* DONG NHAT TAB ACTIVE SANG SPOTIFY GREEN */
    button[data-baseweb="tab"] {
        color: #888888 !important;
        font-weight: 600 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        border-bottom-color: #1DB954 !important;
        color: #1DB954 !important;
    }
</style>
""", unsafe_allow_html=True)

# Bộ Layout chuẩn hóa cho toàn bộ Plotly Charts
PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#141414",
    font=dict(family="Inter, -apple-system, sans-serif", color="#b3b3b3", size=11),
    hoverlabel=dict(
        bgcolor="#181818",
        bordercolor="#1DB954",
        font=dict(family="Inter, sans-serif", color="#ffffff", size=12)
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5,
        font=dict(color="#b3b3b3", size=11),
        bgcolor="rgba(0,0,0,0)"
    )
)

SPOTIFY_CONTINUOUS_COLOR = [
    [0.0, "#101010"],
    [0.25, "#0b3318"],
    [0.65, "#14833b"],
    [1.0, "#1DB954"]
]

# Hàm nạp dữ liệu cache
@st.cache_data(show_spinner="Đang nạp dữ liệu phân tích...")
def load_dataset():
    processed_path = os.path.join("data", "processed", "merged_spotify_data.csv")
    sample_path = os.path.join("data", "sample", "spotify_sample_merged.csv")
    path = processed_path if os.path.exists(processed_path) else sample_path
    
    needed_cols = [
        "track_name", "artist_individual", "streams", "rank", "week", "year",
        "danceability", "energy", "loudness", "valence", "acousticness",
        "speechiness", "liveness", "tempo", "track_genre", "country",
        "region_wb", "is_trending", "mood_category"
    ]
    df = pd.read_csv(path, usecols=lambda c: c in needed_cols, low_memory=False)
    df["week"] = pd.to_datetime(df["week"], errors="coerce")
    df = df.dropna(subset=["week", "artist_individual", "country"])
    df["year_month"] = df["week"].dt.to_period("M").astype(str)
    return df

df_full = load_dataset()

# 1. TIEU DE NOI BAT, CO KHONG GIAN THOANG, BO HAN PHU DE
st.markdown("""
<div style="margin: 28px 0 22px 0;">
    <h1 style="font-size: 2.4rem; font-weight: 900; letter-spacing: -0.8px; color: #ffffff; margin: 0; padding: 0; line-height: 1.15;">
        Hồ Sơ Đặc Trưng Âm Thanh & Nghệ Sĩ
    </h1>
</div>
""", unsafe_allow_html=True)

# Bộ chuyển đổi góc nhìn phân tích dạng tab gạch chân hiện đại
view_mode = st.radio(
    "Góc nhìn phân tích:",
    options=[
        "🎧 Hồ Sơ Âm Thanh & Nghệ Sĩ",
        "🌐 Mạng Lưới Đồng Xuất Hiện & Dự Báo Hit"
    ],
    index=0,
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# GÓC NHÌN 1: HỒ SƠ ÂM THANH & NGHỆ SĨ
if view_mode == "🎧 Hồ Sơ Âm Thanh & Nghệ Sĩ":
    all_months = sorted(df_full["year_month"].unique())
    
    # 2. HANG BO LOC PHA VO DOI XUNG (Moc thoi gian rong gap 2.7 lan hai o kia)
    with st.container(border=True):
        af_c1, af_c2, af_c3 = st.columns([1, 1, 2.7], gap="large")
        with af_c1:
            regions = ["Tất cả khu vực"] + sorted([r for r in df_full["region_wb"].dropna().unique() if str(r).strip()])
            selected_region = st.selectbox("Khu vực địa lý:", regions)
        with af_c2:
            genres = ["Tất cả thể loại"] + sorted([g for g in df_full["track_genre"].dropna().unique() if str(g).strip()][:30])
            selected_genre = st.selectbox("Thể loại âm nhạc:", genres)
        with af_c3:
            time_range = st.select_slider(
                "Mốc thời gian khảo sát (Tháng):",
                options=all_months,
                value=(all_months[0], all_months[-1])
            )
            
    df_filtered = df_full.copy()
    if selected_region != "Tất cả khu vực":
        df_filtered = df_filtered[df_filtered["region_wb"] == selected_region]
    if selected_genre != "Tất cả thể loại":
        df_filtered = df_filtered[df_filtered["track_genre"] == selected_genre]

    start_m, end_m = time_range
    df_period = df_filtered[(df_filtered["year_month"] >= start_m) & (df_filtered["year_month"] <= end_m)]
    
    if df_period.empty:
        st.warning("Không tìm thấy dữ liệu trong khoảng thời gian hoặc bộ lọc đã chọn. Vui lòng nới rộng bộ lọc!")
        st.stop()
    
    artist_stats = df_period.groupby("artist_individual").agg(
        total_streams=("streams", "sum"),
        track_count=("track_name", "nunique"),
        avg_energy=("energy", "mean"),
        avg_valence=("valence", "mean"),
        avg_danceability=("danceability", "mean"),
        top_track=("track_name", lambda x: x.value_counts().index[0] if len(x) > 0 else "N/A"),
        primary_genre=("track_genre", lambda x: x.mode()[0] if not x.empty and x.mode().size > 0 else "Pop")
    ).reset_index()
    
    top_artists_df = artist_stats.sort_values(by="total_streams", ascending=False).head(40)
    
    # 3. BO THANH XAM NGANG THUA, DUA THANG VAO TREEMAP LIEN MACH
    t_h1, t_h2 = st.columns([2.6, 1.2], gap="medium")
    with t_h1:
        st.markdown("<div style='font-size:1.05rem; font-weight:700; color:#ffffff; padding-top:6px;'>Thị phần lượt Stream & Năng lượng âm thanh (Treemap)</div>", unsafe_allow_html=True)
    with t_h2:
        selected_artist = st.selectbox(
            "Tìm nhanh nghệ sĩ:",
            options=top_artists_df["artist_individual"].tolist(),
            index=0,
            label_visibility="collapsed"
        )
    
    fig_treemap = px.treemap(
        top_artists_df,
        path=["primary_genre", "artist_individual"],
        values="total_streams",
        color="avg_energy",
        color_continuous_scale=SPOTIFY_CONTINUOUS_COLOR,
        hover_data={
            "total_streams": ":,.0f",
            "top_track": True,
            "avg_energy": ":.2f",
            "avg_valence": ":.2f",
            "primary_genre": False,
            "artist_individual": False
        }
    )
    fig_treemap.update_traces(
        textinfo="label+value",
        hovertemplate="<b>%{label}</b><br>Thể loại: %{parent}<br>Tổng Streams: %{value:,.0f}<br>Energy: %{color:.2f}<extra></extra>"
    )
    fig_treemap.update_layout(
        **PLOTLY_THEME,
        margin=dict(t=10, l=5, r=5, b=10),
        height=420,
        coloraxis_colorbar=dict(
            title=dict(text="Energy", font=dict(color="#b3b3b3", size=10)),
            thickness=12,
            len=0.85,
            tickfont=dict(color="#888888", size=9)
        )
    )
    
    treemap_event = st.plotly_chart(fig_treemap, width="stretch", on_select="rerun", selection_mode="points")
    
    if treemap_event and "selection" in treemap_event and treemap_event["selection"]["points"]:
        clicked_pt = treemap_event["selection"]["points"][0]
        clicked_name = clicked_pt.get("label")
        if clicked_name and clicked_name in top_artists_df["artist_individual"].values:
            selected_artist = clicked_name
    
    st.markdown(f"""
    <div class="section-header" style="margin-top:28px;">
        <span class="section-title">3. Hồ Sơ Âm Thanh Liên Kết (Linked Views): <span style="color:#1DB954;">{selected_artist}</span></span>
        <span class="section-desc">Đối chiếu hồ sơ âm học của nghệ sĩ với chuẩn Top 50 Trending toàn cầu</span>
    </div>
    """, unsafe_allow_html=True)
    
    artist_data = df_period[df_period["artist_individual"] == selected_artist]
    artist_summary = top_artists_df[top_artists_df["artist_individual"] == selected_artist].iloc[0]
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">TỔNG LƯỢT STREAMS</div>
            <div class="metric-value">{artist_summary['total_streams']:,.0f}</div>
            <div class="metric-sub">Trong giai đoạn {start_m} – {end_m}</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">BÀI HÁT THỊNH HÀNH NHẤT</div>
            <div class="metric-value" style="font-size:1.15rem; color:#ffffff;">{artist_summary['top_track']}</div>
            <div class="metric-sub">Đạt thứ hạng cao nhất</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">THỂ LOẠI CHÍNH</div>
            <div class="metric-value" style="font-size:1.25rem;">{artist_summary['primary_genre']}</div>
            <div class="metric-sub">{artist_summary['track_count']} bài hát lọt BXH</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">ENERGY / VALENCE</div>
            <div class="metric-value">{artist_summary['avg_energy']:.2f} / {artist_summary['avg_valence']:.2f}</div>
            <div class="metric-sub">Thang đo cảm xúc (0.0 – 1.0)</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    
    st.markdown('<div class="surface-card">', unsafe_allow_html=True)
    col_radar, col_scatter = st.columns([1, 1], gap="medium")
    
    with col_radar:
        st.markdown("<p style='font-size:0.92rem; font-weight:700; color:#ffffff; margin-bottom:4px;'>Biểu Đồ Mạng Nhện (Radar Profile)</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:0.78rem; color:#777777; margin-bottom:12px;'>Đường nét đứt mảnh thể hiện chuẩn Top 50 Trending thế giới</p>", unsafe_allow_html=True)
        
        radar_features = ["danceability", "energy", "valence", "acousticness", "speechiness", "liveness"]
        feature_labels = ["Danceability", "Energy", "Valence", "Acousticness", "Speechiness", "Liveness"]
        
        artist_vals = [artist_data[feat].mean() for feat in radar_features]
        artist_vals.append(artist_vals[0])
        
        benchmark_data = df_period[df_period["is_trending"] == 1]
        bench_vals = [benchmark_data[feat].mean() for feat in radar_features]
        bench_vals.append(bench_vals[0])
        
        categories = feature_labels + [feature_labels[0]]
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=bench_vals,
            theta=categories,
            fill="toself",
            name="Chuẩn Top 50 Trending",
            line=dict(color="#777777", width=1.5, dash="dash"),
            fillcolor="rgba(100, 100, 100, 0.08)"
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=artist_vals,
            theta=categories,
            fill="toself",
            name=selected_artist,
            line=dict(color="#1DB954", width=3),
            fillcolor="rgba(29, 185, 84, 0.35)"
        ))
        fig_radar.update_layout(
            **PLOTLY_THEME,
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 1], tickfont=dict(color="#666666", size=8), gridcolor="#222222"),
                angularaxis=dict(tickfont=dict(color="#b3b3b3", size=10), gridcolor="#222222")
            ),
            height=370,
            margin=dict(t=35, b=25, l=35, r=35)
        )
        st.plotly_chart(fig_radar, width="stretch")
    
    with col_scatter:
        st.markdown("<p style='font-size:0.92rem; font-weight:700; color:#ffffff; margin-bottom:4px;'>Không Gian Phân Tán (Scatter Highlight)</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:0.78rem; color:#777777; margin-bottom:12px;'>Bài hát của nghệ sĩ được làm sáng nổi bật giữa nền xám đặc</p>", unsafe_allow_html=True)
        
        ax_col1, ax_col2 = st.columns(2)
        with ax_col1:
            x_axis = st.selectbox("Trục X:", ["danceability", "loudness", "valence", "tempo"], index=0, label_visibility="collapsed")
        with ax_col2:
            y_axis = st.selectbox("Trục Y:", ["energy", "valence", "loudness", "streams"], index=0, label_visibility="collapsed")
        
        other_tracks = df_period[df_period["artist_individual"] != selected_artist]
        this_artist_tracks = df_period[df_period["artist_individual"] == selected_artist]
        
        if len(other_tracks) > 1200:
            other_tracks = other_tracks.sample(1200, random_state=42)
        
        fig_scatter = go.Figure()
        fig_scatter.add_trace(go.Scatter(
            x=other_tracks[x_axis],
            y=other_tracks[y_axis],
            mode="markers",
            name="Các nghệ sĩ khác",
            marker=dict(color="#282828", size=5, opacity=0.9),
            text=other_tracks["track_name"],
            hovertemplate="<b>%{text}</b><br>" + f"{x_axis}: %{{x:.2f}}<br>{y_axis}: %{{y:.2f}}<extra></extra>"
        ))
        fig_scatter.add_trace(go.Scatter(
            x=this_artist_tracks[x_axis],
            y=this_artist_tracks[y_axis],
            mode="markers",
            name=selected_artist,
            marker=dict(color="#1DB954", size=11, line=dict(color="#ffffff", width=1.5)),
            text=this_artist_tracks["track_name"],
            hovertemplate=f"<b>%{{text}}</b><br>Nghệ sĩ: {selected_artist}<br>" + f"{x_axis}: %{{x:.2f}}<br>{y_axis}: %{{y:.2f}}<extra></extra>"
        ))
        fig_scatter.update_layout(
            **PLOTLY_THEME,
            height=370,
            xaxis=dict(title=x_axis.upper(), gridcolor="#202020"),
            yaxis=dict(title=y_axis.upper(), gridcolor="#202020"),
            margin=dict(t=35, b=25, l=20, r=20)
        )
        st.plotly_chart(fig_scatter, width="stretch")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section-header" style="margin-top:20px;">
        <span class="section-title">4. Danh Mục Bài Hát Của Nghệ Sĩ</span>
        <span class="section-desc">Thống kê chi tiết thứ hạng cao nhất và nhóm tâm trạng theo công thức âm học</span>
    </div>
    """, unsafe_allow_html=True)
    
    track_table = artist_data.groupby("track_name").agg(
        total_streams=("streams", "sum"),
        best_rank=("rank", "min"),
        avg_danceability=("danceability", "mean"),
        avg_energy=("energy", "mean"),
        avg_valence=("valence", "mean"),
        mood=("mood_category", lambda x: x.mode()[0] if not x.empty and x.mode().size > 0 else "N/A")
    ).reset_index().sort_values(by="total_streams", ascending=False)
    
    st.dataframe(
        track_table.style.format({
            "total_streams": "{:,.0f}",
            "best_rank": "#{:.0f}",
            "avg_danceability": "{:.3f}",
            "avg_energy": "{:.3f}",
            "avg_valence": "{:.3f}"
        }),
        width="stretch",
        hide_index=True
    )

# GÓC NHÌN 2: MẠNG LƯỚI ĐỒNG XUẤT HIỆN & DỰ BÁO HIT
else:
    # 1. TIEU DE NOI BAT, BO PHU DE, CO KHOANG TRONG THOANG
    st.markdown("""
    <div style="margin: 28px 0 20px 0;">
        <h1 style="font-size: 2.35rem; font-weight: 900; letter-spacing: -0.8px; color: #ffffff; margin: 0; padding: 0; line-height: 1.15;">
            Mạng Lưới Đồng Xuất Hiện Qua Thị Trường Quốc Gia (Network Science)
        </h1>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. HANG BO LOC NGANG GOP DUY NHAT (2 DROPDOWN + 2 SLIDER)
    with st.container(border=True):
        c1, c2, c3, c4 = st.columns([1, 1, 1.15, 1.15], gap="medium")
        with c1:
            sel_reg_net = st.selectbox("Khu vực địa lý:", regions, key="net_reg_p2")
        with c2:
            sel_gen_net = st.selectbox("Thể loại âm nhạc:", genres, key="net_gen_p2")
        with c3:
            top_n = st.slider("Số lượng nghệ sĩ (Nodes):", 20, 50, 32, 2, key="net_n_p2")
        with c4:
            threshold = st.slider("Ngưỡng liên kết (Lọc nhiễu):", 1, 20, 5, 1, key="net_t_p2")
    
    df_net_data = df_full.copy()
    if sel_reg_net != "Tất cả khu vực":
        df_net_data = df_net_data[df_net_data["region_wb"] == sel_reg_net]
    if sel_gen_net != "Tất cả thể loại":
        df_net_data = df_net_data[df_net_data["track_genre"] == sel_gen_net]
        
    if df_net_data.empty:
        st.warning("Không tìm thấy dữ liệu phù hợp với bộ lọc đã chọn!")
        st.stop()
    
    with st.spinner("Đang tính toán mạng lưới và phân cụm cộng đồng..."):
        top_artists = df_net_data.groupby("artist_individual")["streams"].sum().nlargest(top_n).index.tolist()
        df_net = df_net_data[df_net_data["artist_individual"].isin(top_artists)]
        
        bipartite = df_net.groupby(["artist_individual", "country"]).size().unstack(fill_value=0)
        bipartite_binary = (bipartite > 0).astype(int)
        
        adj_matrix = bipartite_binary.dot(bipartite_binary.T)
        np.fill_diagonal(adj_matrix.values, 0)
        
        G = nx.Graph()
        artist_total_streams = df_net.groupby("artist_individual")["streams"].sum().to_dict()
        artist_top_genre = df_net.groupby("artist_individual")["track_genre"].agg(lambda x: x.mode()[0] if not x.empty and x.mode().size > 0 else "Pop").to_dict()
        
        for artist in top_artists:
            G.add_node(
                artist,
                streams=artist_total_streams.get(artist, 1000),
                genre=artist_top_genre.get(artist, "Pop")
            )
        
        for i in range(len(top_artists)):
            for j in range(i + 1, len(top_artists)):
                u = top_artists[i]
                v = top_artists[j]
                weight = adj_matrix.loc[u, v]
                if weight >= threshold:
                    G.add_edge(u, v, weight=int(weight))
        
        # Loai bo cac nut co lap (degree = 0) de khong bi roi rac/tran ra goc (nhu loi YOASOBI)
        isolated = [n for n in G.nodes() if G.degree(n) == 0]
        G.remove_nodes_from(isolated)
        
        # PHAT HIEN CUM CONG DONG (COMMUNITY DETECTION)
        import networkx.algorithms.community as nx_comm
        try:
            communities = list(nx_comm.greedy_modularity_communities(G))
        except Exception:
            communities = [set(G.nodes())]
            
        CLUSTER_COLORS = ["#1DB954", "#ff793f", "#a29bfe", "#00cec9", "#f1c40f", "#fd79a8"]
        CLUSTER_NAMES = ["Pop Core / Mainstream", "Latin Wave / Urbano", "Hip-Hop / Global Rap", "Asian / Regional Wave", "Dance / Electro", "Indie / Alt"]
        
        node_cluster = {}
        for c_idx, comm in enumerate(communities):
            for n in comm:
                node_cluster[n] = c_idx % len(CLUSTER_COLORS)
                
        st.markdown("""
        <div style="display:flex; align-items:center; gap:16px; margin: 4px 0 8px 0; font-size:0.78rem; flex-wrap:wrap;">
            <span style="color:#888888; font-weight:700;">PHÂN CỤM CỘNG ĐỒNG:</span>
            <span style="color:#1DB954; font-weight:700;">● Cụm 1: Pop Core</span>
            <span style="color:#ff793f; font-weight:700;">● Cụm 2: Latin Wave</span>
            <span style="color:#a29bfe; font-weight:700;">● Cụm 3: Hip-Hop / Rap</span>
            <span style="color:#00cec9; font-weight:700;">● Cụm 4: Asian / Regional</span>
            <span style="color:#f1c40f; font-weight:700;">● Cụm 5: Dance / Electro</span>
        </div>
        """, unsafe_allow_html=True)
        
        degrees = dict(G.degree())
        pos = nx.spring_layout(G, k=1.1, iterations=60, seed=42)
        
        if len(G.nodes()) > 1:
            xs = [pos[n][0] for n in G.nodes()]
            ys = [pos[n][1] for n in G.nodes()]
            dx = (max(xs) - min(xs)) or 1
            dy = (max(ys) - min(ys)) or 1
            for n in G.nodes():
                pos[n] = np.array([
                    (pos[n][0] - min(xs)) / dx * 2 - 1,
                    (pos[n][1] - min(ys)) / dy * 2 - 1
                ])
        
        # 1. CANH NOI (EDGES) - VE RO NET
        edge_x = []
        edge_y = []
        for edge in G.edges(data=True):
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1.5, color="rgba(160, 160, 160, 0.45)"),
            hoverinfo="none",
            mode="lines"
        )
        
        # 2. NUT (NODES) & NHAN (LABELS) - TRÁNH CHỒNG CHÉO CHỮ
        sorted_degs = sorted(degrees.values(), reverse=True) if degrees else [0]
        label_cutoff = sorted_degs[int(len(sorted_degs) * 0.35)] if len(sorted_degs) > 5 else 0
        
        node_x = []
        node_y = []
        node_text = []
        node_size = []
        node_color = []
        node_labels = []
        
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            deg = degrees.get(node, 0)
            strm = artist_total_streams.get(node, 0)
            gnr = artist_top_genre.get(node, "Pop")
            c_id = node_cluster.get(node, 0)
            c_color = CLUSTER_COLORS[c_id]
            c_name = CLUSTER_NAMES[c_id]
            
            info = (
                f"<b>{node}</b> ({gnr})<br>"
                f"• Phân cụm: <b>{c_name}</b><br>"
                f"• Bậc liên kết (Degree): {deg}<br>"
                f"• Tổng streams: {strm:,.0f}<br>"
                f"• Quốc gia cùng lọt top: {bipartite_binary.loc[node].sum()}"
            )
            node_text.append(info)
            node_size.append(max(13, int(np.sqrt(deg) * 5.5) + 11))
            node_color.append(c_color)
            
            if deg >= label_cutoff:
                node_labels.append(node)
            else:
                node_labels.append("")  # Nut nho chi hien tren hover
        
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode="markers+text",
            hoverinfo="text",
            text=node_labels,
            textposition="top center",
            textfont=dict(size=10, color="#ffffff", family="Inter, sans-serif"),
            marker=dict(
                color=node_color,
                size=node_size,
                line=dict(width=1.8, color="#ffffff")
            )
        )
        node_trace.hovertext = node_text
        
        fig_net = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                **PLOTLY_THEME,
                height=450,
                showlegend=False,
                margin=dict(b=10, l=10, r=10, t=10),
                xaxis=dict(range=[-1.18, 1.18], showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(range=[-1.15, 1.15], showgrid=False, zeroline=False, showticklabels=False)
            )
        )
        st.plotly_chart(fig_net, width="stretch")
    
    nm1, nm2, nm3, nm4 = st.columns(4)
    with nm1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">SỐ NGHỆ SĨ (NODES)</div>
            <div class="metric-value">{G.number_of_nodes()}</div>
            <div class="metric-sub">Trong không gian mạng lưới</div>
        </div>
        """, unsafe_allow_html=True)
    with nm2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">SỐ LIÊN KẾT (EDGES)</div>
            <div class="metric-value">{G.number_of_edges():,}</div>
            <div class="metric-sub">Độ mạnh ≥ {threshold} quốc gia</div>
        </div>
        """, unsafe_allow_html=True)
    with nm3:
        density = nx.density(G) if G.number_of_nodes() > 1 else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">MẬT ĐỘ MẠNG LƯỚI</div>
            <div class="metric-value">{density:.3f}</div>
            <div class="metric-sub">Network Density (0.0 – 1.0)</div>
        </div>
        """, unsafe_allow_html=True)
    with nm4:
        components = nx.number_connected_components(G) if G.number_of_nodes() > 0 else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">SỐ CỤM ĐỘC LẬP</div>
            <div class="metric-value">{components}</div>
            <div class="metric-sub">Connected Clusters</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section-header" style="margin-top:30px;">
        <span class="section-title">2. Công Cụ Giả Lập Dự Báo Thịnh Hành (Machine Learning Simulator)</span>
        <span class="section-desc">Mô hình Hồi quy Logistic phân lớp xác suất bài hát lọt Top 50 Trending</span>
    </div>
    """, unsafe_allow_html=True)
    
    features = ["danceability", "energy", "loudness", "valence", "acousticness", "speechiness", "tempo"]
    train_df = df_full.dropna(subset=features + ["is_trending"])
    if len(train_df) > 15000:
        train_df = train_df.sample(15000, random_state=42)
    
    X = train_df[features]
    y = train_df["is_trending"]
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    clf = LogisticRegression(class_weight="balanced", random_state=42)
    clf.fit(X_scaled, y)
    
    st.markdown('<div class="surface-card">', unsafe_allow_html=True)
    col_s1, col_s2, col_s3 = st.columns([1, 1, 1.2], gap="large")
    
    with col_s1:
        st.markdown("<p style='font-size:0.85rem; font-weight:700; color:#ffffff;'>Nhóm Tiết Tấu & Âm Lượng</p>", unsafe_allow_html=True)
        sim_dance = st.slider("Độ bắt tai (Danceability):", 0.0, 1.0, 0.72, 0.02)
        sim_energy = st.slider("Năng lượng âm thanh (Energy):", 0.0, 1.0, 0.68, 0.02)
        sim_loudness = st.slider("Âm lượng trung bình (Loudness dB):", -25.0, 0.0, -5.5, 0.5)
    
    with col_s2:
        st.markdown("<p style='font-size:0.85rem; font-weight:700; color:#ffffff;'>Nhóm Cảm Xúc & Lời Hát</p>", unsafe_allow_html=True)
        sim_valence = st.slider("Cảm xúc tích cực (Valence):", 0.0, 1.0, 0.55, 0.02)
        sim_acoustic = st.slider("Tính mộc mạc (Acousticness):", 0.0, 1.0, 0.18, 0.02)
        sim_speech = st.slider("Tỷ lệ lời hát (Speechiness):", 0.0, 1.0, 0.08, 0.01)
    
    with col_s3:
        st.markdown("<p style='font-size:0.85rem; font-weight:700; color:#ffffff;'>Xác Suất Lọt Top Trending</p>", unsafe_allow_html=True)
        sim_tempo = st.slider("Nhịp điệu (Tempo BPM):", 60.0, 200.0, 120.0, 1.0)
        
        input_data = np.array([[sim_dance, sim_energy, sim_loudness, sim_valence, sim_acoustic, sim_speech, sim_tempo]])
        input_scaled = scaler.transform(input_data)
        prob_trending = clf.predict_proba(input_scaled)[0][1] * 100
        
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob_trending,
            domain={'x': [0, 1], 'y': [0, 1]},
            number={'suffix': "%", 'font': {'color': "#1DB954", 'size': 36, 'family': "Inter"}},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': "#444444", 'tickwidth': 1},
                'bar': {'color': "#1DB954", 'thickness': 0.3},
                'bgcolor': "#1c1c1c",
                'borderwidth': 0,
                'steps': [
                    {'range': [0, 40], 'color': "rgba(255, 75, 75, 0.2)"},
                    {'range': [40, 70], 'color': "rgba(255, 170, 0, 0.2)"},
                    {'range': [70, 100], 'color': "rgba(29, 185, 84, 0.25)"}
                ],
                'threshold': {
                    'line': {'color': "#ffffff", 'width': 2},
                    'thickness': 0.75,
                    'value': 70
                }
            }
        ))
        fig_gauge.update_layout(
            **PLOTLY_THEME,
            height=220,
            margin=dict(t=20, b=10, l=15, r=15)
        )
        st.plotly_chart(fig_gauge, width="stretch")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section-header" style="margin-top:20px;">
        <span class="section-title">3. Hệ Số Tác Động Của Các Yếu Tố Âm Học (Feature Importance)</span>
        <span class="section-desc">Hệ số dương thúc đẩy khả năng thành Hit • Hệ số âm kìm hãm cơ hội lọt bảng xếp hạng</span>
    </div>
    """, unsafe_allow_html=True)
    
    coef_df = pd.DataFrame({
        "Đặc trưng âm học": ["Danceability", "Energy", "Loudness", "Valence", "Acousticness", "Speechiness", "Tempo"],
        "Hệ số (Coefficient)": clf.coef_[0]
    }).sort_values(by="Hệ số (Coefficient)", ascending=True)
    
    colors = ["#1DB954" if c >= 0 else "#e91e63" for c in coef_df["Hệ số (Coefficient)"]]
    
    fig_coef = go.Figure(go.Bar(
        x=coef_df["Hệ số (Coefficient)"],
        y=coef_df["Đặc trưng âm học"],
        orientation="h",
        marker=dict(color=colors, line=dict(width=0))
    ))
    fig_coef.update_layout(
        **PLOTLY_THEME,
        height=280,
        margin=dict(t=15, b=20, l=10, r=10),
        xaxis=dict(gridcolor="#222222", zerolinecolor="#444444"),
        yaxis=dict(gridcolor="rgba(0,0,0,0)")
    )
    st.plotly_chart(fig_coef, width="stretch")
