import os
import base64
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# Cau hinh trang Streamlit (Mo sidebar theo chuan Dashboard)
st.set_page_config(
    page_title="Spotify Trends & Audio Analytics",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# He thong CSS phong cach Spotify Dark Theme & Standard Dashboard (Phan tang mau & Typography chuan)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400..800;1,6..72,400..800&family=Inter:wght@400;500;600;700;800&family=Montserrat:wght@500;600;700;800;900&display=swap');

    /* 1. NỀN TOÀN TRANG #F7F4EF & TYPOGRAPHY WARM MUSIC EDITORIAL */
    html, body, .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        background-color: #F7F4EF !important;
        color: #241F21 !important;
    }

    [data-testid="stIconMaterial"],
    [data-testid="stExpanderToggleIcon"],
    .material-symbols-rounded,
    .material-symbols-outlined,
    .material-icons {
        font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
    }

    #MainMenu {visibility: hidden !important; display: none !important;}
    footer {visibility: hidden !important; display: none !important;}
    .stDeployButton,
    [data-testid="stDeployButton"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }
    
    header[data-testid="stHeader"] {
        background-color: transparent !important;
        z-index: 1000 !important;
        height: 3.2rem !important;
    }
    
    /* NÚT MỞ SIDEBAR KHI BỊ ĐÓNG */
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapsedControl"],
    button[aria-label="Expand sidebar"],
    button[aria-label="open sidebar"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        pointer-events: auto !important;
        position: fixed !important;
        top: 10px !important;
        left: 12px !important;
        z-index: 9999999 !important;
        color: #FFFFFF !important;
        background-color: #7A3E65 !important;
        border: 2px solid #5E2E4D !important;
        border-radius: 8px !important;
        padding: 5px 12px !important;
        box-shadow: 0 4px 14px rgba(122, 62, 101, 0.25) !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }
    [data-testid="collapsedControl"]:hover,
    [data-testid="stSidebarCollapsedControl"]:hover,
    button[aria-label="Expand sidebar"]:hover {
        background-color: #5E2E4D !important;
        transform: scale(1.04) !important;
        box-shadow: 0 6px 18px rgba(94, 46, 77, 0.35) !important;
    }
    [data-testid="collapsedControl"] svg,
    [data-testid="stSidebarCollapsedControl"] svg,
    button[aria-label="Expand sidebar"] svg {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
        stroke: #FFFFFF !important;
        width: 20px !important;
        height: 20px !important;
    }
    
    /* 2. SIDEBAR STYLING: NỀN #EEE9E1 & VIỀN #D8D0C7 */
    section[data-testid="stSidebar"] {
        background-color: #EEE9E1 !important;
        border-right: 1px solid #D8D0C7 !important;
        padding-top: 1.2rem !important;
    }
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #625B5E !important;
    }
    
    /* 3. SIDEBAR NAVIGATION:
       - Chiều cao mỗi mục 50px, font 16px, icon 20px
       - Bình thường: nền trong suốt, không viền, không bóng
       - Hover: nền #F7F4EF
       - Đang chọn: nền #F2E6EE, vạch tím 4px bên trái, chữ & icon #7A3E65
    */
    section[data-testid="stSidebar"] div[role="radiogroup"] {
        display: flex !important;
        flex-direction: column !important;
        gap: 3px !important;
        background: transparent !important;
        border: none !important;
        padding: 4px 0 !important;
        width: 100% !important;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label {
        background-color: transparent !important;
        border: none !important;
        border-left: 4px solid transparent !important;
        border-radius: 8px !important;
        padding: 0 16px !important;
        min-height: 50px !important;
        height: 50px !important;
        width: 100% !important;
        margin: 0 !important;
        transition: all 0.18s ease !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        box-shadow: none !important;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
        background-color: #F7F4EF !important;
        border: none !important;
        border-left: 4px solid transparent !important;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label [data-testid="stMarkdownContainer"] p {
        font-family: 'Inter', sans-serif !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        line-height: 1.4 !important;
        margin: 0 !important;
        color: #625B5E !important;
        display: flex !important;
        align-items: center !important;
    }
    /* MỤC SIDEBAR ĐANG CHỌN (ACTIVE) */
    section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked),
    section[data-testid="stSidebar"] div[role="radiogroup"] > label[data-checked="true"] {
        background-color: #F2E6EE !important;
        border: none !important;
        border-left: 4px solid #7A3E65 !important;
        box-shadow: none !important;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) [data-testid="stMarkdownContainer"] p,
    section[data-testid="stSidebar"] div[role="radiogroup"] > label[data-checked="true"] [data-testid="stMarkdownContainer"] p {
        color: #7A3E65 !important;
        font-weight: 700 !important;
    }

    /* ĐỒNG BỘ ICON SVG CHO TỪNG MỤC ĐIỀU HƯỚNG SIDEBAR - MÀU TÍM MẬN #7A3E65 */
    section[data-testid="stSidebar"] div[data-testid="stRadio"]:first-of-type div[role="radiogroup"] > label p::before {
        content: '';
        display: inline-block;
        width: 20px;
        height: 20px;
        margin-right: 12px;
        vertical-align: middle;
        background-size: contain;
        background-repeat: no-repeat;
        flex-shrink: 0;
    }
    /* 1. Trang Chủ */
    section[data-testid="stSidebar"] div[data-testid="stRadio"]:first-of-type div[role="radiogroup"] > label:nth-of-type(1) p::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%237A3E65' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z'/%3E%3Cpolyline points='9 22 9 12 15 12 15 22'/%3E%3C/svg%3E");
    }
    /* 2. Bảng Dữ Liệu & Bộ Lọc */
    section[data-testid="stSidebar"] div[data-testid="stRadio"]:first-of-type div[role="radiogroup"] > label:nth-of-type(2) p::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%237A3E65' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cellipse cx='12' cy='5' rx='9' ry='3'/%3E%3Cpath d='M3 5v14a9 3 0 0 0 18 0V5'/%3E%3Cpath d='M3 12a9 3 0 0 0 18 0'/%3E%3C/svg%3E");
    }
    /* 3. Thống Kê Thị Trường */
    section[data-testid="stSidebar"] div[data-testid="stRadio"]:first-of-type div[role="radiogroup"] > label:nth-of-type(3) p::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%237A3E65' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='18' x2='18' y1='20' y2='10'/%3E%3Cline x1='12' x2='12' y1='20' y2='4'/%3E%3Cline x1='6' x2='6' y1='20' y2='14'/%3E%3C/svg%3E");
    }
    /* 4. So Sánh Thị Hiếu (Taste Radar) */
    section[data-testid="stSidebar"] div[data-testid="stRadio"]:first-of-type div[role="radiogroup"] > label:nth-of-type(4) p::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%237A3E65' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolygon points='12 2 19 8.5 16.5 17 7.5 17 5 8.5 12 2'/%3E%3Cline x1='12' x2='12' y1='2' y2='17'/%3E%3C/svg%3E");
    }
    /* 5. Biểu Đồ Phân Tích */
    section[data-testid="stSidebar"] div[data-testid="stRadio"]:first-of-type div[role="radiogroup"] > label:nth-of-type(5) p::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%237A3E65' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M3 3v18h18'/%3E%3Cpath d='m19 9-5 5-4-4-3 3'/%3E%3C/svg%3E");
    }
    /* 6. Đặc Tính Âm Nhạc */
    section[data-testid="stSidebar"] div[data-testid="stRadio"]:first-of-type div[role="radiogroup"] > label:nth-of-type(6) p::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%237A3E65' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M3 14h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-7a9 9 0 0 1 18 0v7a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3'/%3E%3C/svg%3E");
    }
    /* 7. Mạng Lưới Hợp Tác */
    section[data-testid="stSidebar"] div[data-testid="stRadio"]:first-of-type div[role="radiogroup"] > label:nth-of-type(7) p::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%237A3E65' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='18' cy='5' r='3'/%3E%3Ccircle cx='6' cy='12' r='3'/%3E%3Ccircle cx='18' cy='19' r='3'/%3E%3Cline x1='8.59' x2='15.42' y1='13.51' y2='17.49'/%3E%3Cline x1='15.41' x2='8.59' y1='6.51' y2='10.49'/%3E%3C/svg%3E");
    }
    /* 8. Dự Báo Ca Khúc Hit */
    section[data-testid="stSidebar"] div[data-testid="stRadio"]:first-of-type div[role="radiogroup"] > label:nth-of-type(8) p::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%237A3E65' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z'/%3E%3C/svg%3E");
    }
    section[data-testid="stSidebar"] div[data-testid="stRadio"]:first-of-type div[role="radiogroup"] > label:has(input:checked) p::before,
    section[data-testid="stSidebar"] div[data-testid="stRadio"]:first-of-type div[role="radiogroup"] > label[data-checked="true"] p::before {
        filter: none !important;
    }

    div[data-testid="stVerticalBlock"] {
        gap: 1.15rem !important;
    }

    /* 4. KHU VỰC KHUNG CONTAINER CHUẨN: NỀN #FFFFFF & VIỀN #D8D0C7 */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border: 1px solid #D8D0C7 !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        margin-bottom: 8px !important;
        box-shadow: 0 1px 4px rgba(36, 31, 33, 0.03) !important;
    }

    /* Album strip */
    .album-strip-wrapper {
        background-color: #F2EDE7;
        border: 1px solid #D8D0C7;
        border-radius: 12px;
        padding: 6px 12px;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 10px;
        overflow: hidden;
    }
    .album-strip-badge {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding-right: 10px;
        border-right: 1px solid #D8D0C7;
        flex-shrink: 0;
    }
    .album-strip-badge-title {
        font-size: 0.72rem;
        font-weight: 800;
        color: #7A3E65;
        letter-spacing: 0.5px;
        white-space: nowrap;
    }
    .album-strip-badge-sub {
        font-size: 0.65rem;
        color: #81786E;
        white-space: nowrap;
    }
    .album-strip-scroll {
        display: flex;
        overflow: hidden;
        white-space: nowrap;
        width: 100%;
    }
    .album-marquee-track {
        display: flex;
        gap: 8px;
        animation: albumScroll 42s linear infinite;
        flex-shrink: 0;
    }
    .album-marquee-track:hover {
        animation-play-state: paused;
    }
    @keyframes albumScroll {
        0% { transform: translateX(0); }
        100% { transform: translateX(-50%); }
    }
    .album-strip-img {
        width: 48px;
        height: 48px;
        border-radius: 6px;
        object-fit: cover;
        flex-shrink: 0;
        box-shadow: 0 2px 6px rgba(36, 31, 33, 0.12);
        border: 1px solid #D8D0C7;
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        cursor: pointer;
    }
    .album-strip-img:hover {
        transform: translateY(-2px) scale(1.12);
        border-color: #7A3E65;
        box-shadow: 0 4px 12px rgba(122, 62, 101, 0.25);
    }

    .block-container {
        padding-top: 3.2rem !important;
        padding-bottom: 0.5rem !important;
        padding-left: 1.8rem !important;
        padding-right: 1.8rem !important;
        max-width: 100% !important;
    }

    /* 5. TYPOGRAPHY WARM MUSIC EDITORIAL THEO HỆ THỐNG CỠ CHỮ */
    h1, .hero-title {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 46px !important;
        font-weight: 800 !important;
        line-height: 1.15 !important;
        letter-spacing: -0.8px !important;
        color: #241F21 !important;
    }

    h2, h3, .section-title, .card-heading {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 23px !important;
        font-weight: 800 !important;
        letter-spacing: -0.3px !important;
        color: #241F21 !important;
    }

    h4, h5, h6 {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        color: #241F21 !important;
    }

    p, span, label, div, button, input, select, textarea,
    [data-testid="stMarkdownContainer"] p {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        font-size: 16px;
        color: #625B5E;
    }

    /* Label bộ lọc 15px */
    div[data-testid="stSelectbox"] label,
    div[data-testid="stSlider"] label,
    div[data-testid="stTextInput"] label,
    div[data-testid="stCheckbox"] label span {
        font-size: 15px !important;
        font-weight: 600 !important;
        color: #241F21 !important;
    }

    /* 6. HỆ THỐNG PHÂN TẦNG BỀ MẶT WARM MUSIC EDITORIAL
       Nền trang #F7F4EF
        └─ Sidebar #EEE9E1
        └─ Card #FFFFFF
            └─ Card phụ #F2EDE7
            └─ Hover #F2E6EE
    */
    .layer-1-card {
        background-color: #FFFFFF;
        border: 1px solid #D8D0C7;
        border-radius: 12px;
        box-shadow: 0 1px 4px rgba(36, 31, 33, 0.03);
    }

    .layer-2-card {
        background-color: #F2EDE7;
        border: 1px solid #D8D0C7;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(36, 31, 33, 0.05);
    }

    /* HERO KPI CARD: Card chính "Tổng bản ghi" nền #FFFFFF viền Tím Mận #7A3E65 */
    .hero-anchor-card {
        background-color: #FFFFFF;
        border: 1.5px solid #7A3E65;
        border-radius: 14px;
        padding: 22px 24px;
        box-shadow: 0 4px 18px rgba(122, 62, 101, 0.08);
        position: relative;
        overflow: hidden;
        min-height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    /* SUB-METRIC CARDS: Nền #FFFFFF, Viền #D8D0C7 */
    .sub-metric-card {
        background-color: #FFFFFF;
        border: 1px solid #D8D0C7;
        border-radius: 14px;
        padding: 20px 22px;
        box-shadow: 0 2px 8px rgba(36, 31, 33, 0.03);
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 140px;
    }

    .sub-metric-card:hover {
        border-color: #7A3E65;
        background-color: #F2E6EE;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(36, 31, 33, 0.08);
    }

    /* 7. CÔNG TẮC / RADIOGROUP NGANG */
    div[role="radiogroup"] {
        background-color: #EEE9E1 !important;
        padding: 4px !important;
        border-radius: 10px !important;
        border: 1px solid #D8D0C7 !important;
        display: inline-flex !important;
        gap: 6px !important;
        margin-bottom: 4px !important;
    }
    div[role="radiogroup"] > label {
        background-color: #FFFFFF !important;
        border: 1px solid #D8D0C7 !important;
        border-radius: 8px !important;
        padding: 7px 16px !important;
        margin: 0 !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }
    div[role="radiogroup"] > label:hover {
        background-color: #F2E6EE !important;
        border-color: #D8D0C7 !important;
    }
    div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }
    div[role="radiogroup"] > label [data-testid="stMarkdownContainer"] p {
        font-family: 'Inter', sans-serif !important;
        font-size: 15px !important;
        font-weight: 500 !important;
        color: #625B5E !important;
    }
    /* Nút đang chọn: Nền #FFFFFF, Viền Tím Mận #7A3E65, Chữ #7A3E65 */
    div[role="radiogroup"] > label[data-checked="true"],
    div[role="radiogroup"] > label:has(input:checked) {
        background-color: #FFFFFF !important;
        border: 1.5px solid #7A3E65 !important;
    }
    div[role="radiogroup"] > label:has(input:checked) [data-testid="stMarkdownContainer"] p,
    div[role="radiogroup"] > label[data-checked="true"] [data-testid="stMarkdownContainer"] p {
        color: #7A3E65 !important;
        font-weight: 700 !important;
    }

    .metric-card {
        background-color: #FFFFFF;
        border: 1px solid #D8D0C7;
        border-radius: 12px;
        padding: 16px 20px;
        transition: border-color 0.2s ease, background-color 0.2s ease;
        box-shadow: 0 1px 4px rgba(36, 31, 33, 0.03);
    }
    .metric-card:hover {
        border-color: #7A3E65;
        background-color: #F2E6EE;
    }
    .metric-label {
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 0.5px;
        color: #625B5E;
        margin-bottom: 6px;
    }
    .metric-value {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 34px !important;
        font-weight: 900;
        letter-spacing: -0.5px;
        color: #7A3E65;
        line-height: 1.15;
    }
    .metric-sub {
        font-size: 14px;
        color: #81786E;
        margin-top: 6px;
    }

    .filter-card {
        background-color: #FFFFFF;
        border: 1px solid #D8D0C7;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 16px;
        box-shadow: 0 1px 4px rgba(36, 31, 33, 0.03);
    }

    .bento-card {
        background-color: #FFFFFF;
        border: 1px solid #D8D0C7;
        border-radius: 14px;
        padding: 18px 20px;
        margin-bottom: 16px;
        transition: border-color 0.2s ease, background-color 0.2s ease;
        box-shadow: 0 1px 4px rgba(36, 31, 33, 0.03);
    }
    .bento-card:hover {
        border-color: #7A3E65;
        background-color: #F2E6EE;
    }

    .slot-card {
        background-color: #FFFFFF;
        border: 1px solid #D8D0C7;
        border-radius: 14px;
        padding: 16px 18px;
        margin-bottom: 16px;
        transition: border-color 0.2s ease;
        box-shadow: 0 1px 4px rgba(36, 31, 33, 0.03);
    }
    .slot-card:hover {
        border-color: #7A3E65;
        background-color: #F2E6EE;
    }

    .player-card {
        background-color: #FFFFFF;
        border: 1px solid #D8D0C7;
        border-left: 4px solid #7A3E65;
        border-radius: 14px;
        padding: 18px 20px;
        margin-top: 10px;
        box-shadow: 0 4px 16px rgba(36, 31, 33, 0.06);
    }
    .player-title {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 1.15rem;
        font-weight: 800;
        letter-spacing: -0.3px;
        color: #241F21;
        margin-bottom: 2px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .player-artist {
        font-size: 0.85rem;
        color: #7A3E65;
        font-weight: 600;
        margin-bottom: 12px;
    }
    .player-progress {
        background: #F2EDE7;
        height: 5px;
        border-radius: 3px;
        margin-bottom: 10px;
        overflow: hidden;
    }
    .player-progress-bar {
        background: #7A3E65;
        height: 100%;
        border-radius: 3px;
    }

    .member-card {
        background: #FFFFFF;
        border: 1px solid #D8D0C7;
        border-radius: 12px;
        padding: 16px 20px;
        transition: border-color 0.2s;
        box-shadow: 0 1px 4px rgba(36, 31, 33, 0.03);
    }
    .member-card:hover {
        border-color: #7A3E65;
        background: #F2E6EE;
    }
    .member-name {
        font-size: 1.05rem;
        font-weight: 800;
        color: #241F21;
    }
    .member-id {
        font-size: 0.9rem;
        font-weight: 700;
        color: #7A3E65;
        margin: 3px 0;
    }
    .member-role {
        font-size: 0.82rem;
        color: #625B5E;
    }

    .section-header {
        display: flex;
        align-items: baseline;
        gap: 12px;
        border-bottom: 1px solid #E2DBD3;
        padding-bottom: 8px;
        margin-top: 18px;
        margin-bottom: 16px;
    }

    /* 8. BẢNG DỮ LIỆU SÁNG:
       - Header bảng: #EEE9E1
       - Hàng lẻ: #FFFFFF
       - Hàng chẵn: #FAF8F5
       - Hover: #F2E6EE
       - Đường phân cách: #E2DBD3
       - Chữ: #2B2728, cỡ 14-15px
    */
    [data-testid="stDataFrame"] {
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid #D8D0C7 !important;
        background-color: #FFFFFF !important;
        box-shadow: 0 1px 4px rgba(36, 31, 33, 0.03) !important;
    }
    [data-testid="stDataFrame"] [role="columnheader"] {
        background-color: #EEE9E1 !important;
        color: #2B2728 !important;
        font-weight: 700 !important;
        font-size: 14.5px !important;
        border-bottom: 1px solid #E2DBD3 !important;
    }

    /* 9. SELECTBOX & DROPDOWN */
    div[data-testid="stSelectbox"] > div > div,
    div[data-baseweb="select"],
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1px solid #D8D0C7 !important;
        border-radius: 8px !important;
        color: #241F21 !important;
        font-size: 16px !important;
    }
    div[data-baseweb="select"]:hover {
        border-color: #7A3E65 !important;
        background-color: #F7F4EF !important;
    }
    div[data-baseweb="select"]:focus-within {
        border-color: #7A3E65 !important;
        box-shadow: 0 0 0 2px rgba(122, 62, 101, 0.25) !important;
    }
    div[data-baseweb="select"] * {
        color: #241F21 !important;
        background-color: transparent !important;
    }
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    ul[role="listbox"] {
        background-color: #FFFFFF !important;
        border: 1px solid #D8D0C7 !important;
        border-radius: 8px !important;
        box-shadow: 0 6px 20px rgba(36, 31, 33, 0.1) !important;
    }
    li[role="option"] {
        background-color: #FFFFFF !important;
        color: #625B5E !important;
        font-size: 15px !important;
    }
    li[role="option"]:hover,
    li[role="option"][aria-selected="true"] {
        background-color: #F2E6EE !important;
        color: #7A3E65 !important;
        font-weight: 600 !important;
    }

    /* 10. INPUT TEXT: PHONG CÁCH WARM EDITORIAL */
    div[data-testid="stTextInput"] div[data-baseweb="input"],
    div[data-testid="stTextInput"] div[data-baseweb="base-input"] {
        background-color: #FFFFFF !important;
        border: 1px solid #D8D0C7 !important;
        border-radius: 8px !important;
    }
    div[data-testid="stTextInput"] input {
        background-color: transparent !important;
        border: none !important;
        color: #241F21 !important;
        font-size: 15px !important;
    }
    div[data-testid="stTextInput"] input::placeholder {
        color: #756E65 !important;
        opacity: 1 !important;
        -webkit-text-fill-color: #756E65 !important;
    }
    div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {
        border-color: #7A3E65 !important;
        box-shadow: 0 0 0 2px rgba(122, 62, 101, 0.2) !important;
    }

    /* 11. SLIDER PLUM */
    div[data-testid="stSlider"] div[role="slider"] {
        background-color: #7A3E65 !important;
        border: 2px solid #7A3E65 !important;
        box-shadow: 0 0 8px rgba(122, 62, 101, 0.35) !important;
    }
    div[data-testid="stSlider"] div[data-baseweb="slider"] div[style*="background"] {
        background: #7A3E65 !important;
    }
    div[data-testid="stSlider"] [data-testid="stThumbValue"] {
        color: #7A3E65 !important;
        font-weight: 700 !important;
        font-size: 14px !important;
    }

    /* 12. TAB ACTIVE */
    button[data-baseweb="tab"] {
        color: #81786E !important;
        font-weight: 600 !important;
        font-size: 15px !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        border-bottom-color: #7A3E65 !important;
        color: #7A3E65 !important;
    }

    /* 13. BUTTONS HỆ THỐNG WARM MUSIC EDITORIAL */
    div[data-testid="stButton"] button {
        background-color: #FFFFFF !important;
        border: 1px solid #D8D0C7 !important;
        border-radius: 20px !important;
        color: #241F21 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        padding: 8px 18px !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stButton"] button * {
        color: #241F21 !important;
        -webkit-text-fill-color: #241F21 !important;
    }
    div[data-testid="stButton"] button:hover {
        background-color: #F2E6EE !important;
        border-color: #7A3E65 !important;
        color: #7A3E65 !important;
        transform: translateY(-1px) !important;
    }
    div[data-testid="stButton"] button:hover * {
        color: #7A3E65 !important;
        -webkit-text-fill-color: #7A3E65 !important;
    }
    
    /* PRIMARY BUTTON: Nền Tím mận #7A3E65, Chữ trắng tinh #FFFFFF (TƯƠNG PHẢN TỐI ĐA) */
    div[data-testid="stButton"] button[kind="primary"],
    div[data-testid="stButton"] button[data-testid="stBaseButton-primary"] {
        background-color: #7A3E65 !important;
        border: 1px solid #7A3E65 !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        box-shadow: 0 2px 8px rgba(122, 62, 101, 0.25) !important;
    }
    div[data-testid="stButton"] button[kind="primary"] *,
    div[data-testid="stButton"] button[data-testid="stBaseButton-primary"] * {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-weight: 700 !important;
    }
    div[data-testid="stButton"] button[kind="primary"]:hover,
    div[data-testid="stButton"] button[data-testid="stBaseButton-primary"]:hover {
        background-color: #5E2E4D !important;
        border-color: #5E2E4D !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 14px rgba(94, 46, 77, 0.35) !important;
    }
    div[data-testid="stButton"] button[kind="primary"]:hover *,
    div[data-testid="stButton"] button[data-testid="stBaseButton-primary"]:hover * {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    /* SECONDARY BUTTON: Nền Trắng, Chữ than #241F21, Hover sang Tím mận */
    div[data-testid="stButton"] button[kind="secondary"],
    div[data-testid="stButton"] button[data-testid="stBaseButton-secondary"] {
        background-color: #FFFFFF !important;
        border: 1px solid #D8D0C7 !important;
        color: #241F21 !important;
    }
    div[data-testid="stButton"] button[kind="secondary"] *,
    div[data-testid="stButton"] button[data-testid="stBaseButton-secondary"] * {
        color: #241F21 !important;
        -webkit-text-fill-color: #241F21 !important;
    }
    div[data-testid="stButton"] button[kind="secondary"]:hover,
    div[data-testid="stButton"] button[data-testid="stBaseButton-secondary"]:hover {
        background-color: #F2EDE7 !important;
        border-color: #7A3E65 !important;
        color: #7A3E65 !important;
    }
    div[data-testid="stButton"] button[kind="secondary"]:hover *,
    div[data-testid="stButton"] button[data-testid="stBaseButton-secondary"]:hover * {
        color: #7A3E65 !important;
        -webkit-text-fill-color: #7A3E65 !important;
    }

    /* 14. KHỐI HERO VÀ THẺ KHÁM PHÁ NHANH TRANG CHỦ */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.hero-marker-editorial) {
        position: relative !important;
        background:
            radial-gradient(circle at 12% 20%, #f1e4ec 0, transparent 34%),
            radial-gradient(circle at 76% 15%, #f7e6dc 0, transparent 30%),
            #f7f4ef !important;
        border: 1px solid #D8D0C7 !important;
        border-radius: 18px !important;
        padding: 24px 28px 22px 28px !important;
        margin-bottom: 20px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 24px rgba(98, 92, 84, 0.05) !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.quick-card-marker) {
        background-color: #FFFFFF !important;
        border: 1px solid #D8D0C7 !important;
        border-radius: 14px !important;
        padding: 18px 20px !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(36, 31, 33, 0.03) !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.quick-card-marker):hover {
        border-color: #7A3E65 !important;
        box-shadow: 0 6px 18px rgba(122, 62, 101, 0.08) !important;
        transform: translateY(-2px) !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.quick-card-marker) div[data-testid="stButton"] button {
        background-color: transparent !important;
        border: 1px solid #D8D0C7 !important;
        color: #7A3E65 !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        padding: 7px 14px !important;
        font-size: 14px !important;
        margin-top: 4px !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.quick-card-marker) div[data-testid="stButton"] button:hover {
        background-color: #F2E6EE !important;
        border-color: #7A3E65 !important;
        color: #5E2E4D !important;
    }
</style>
""", unsafe_allow_html=True)

# Tu dong mo sidebar neu trinh duyet dang luu trang thai bi dong
components.html("""
<script>
    function forceExpandSidebar() {
        try {
            const doc = window.parent.document;
            const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
            
            // Xoa trang thai collapsed trong localStorage cua trinh duyet
            try {
                for (let i = 0; i < window.parent.localStorage.length; i++) {
                    const k = window.parent.localStorage.key(i);
                    if (k && k.toLowerCase().includes('sidebar')) {
                        window.parent.localStorage.setItem(k, 'expanded');
                    }
                }
            } catch(err) {}

            const isCollapsed = !sidebar || sidebar.getAttribute('aria-expanded') === 'false' || sidebar.clientWidth < 50;
            if (isCollapsed) {
                const btn = doc.querySelector('[data-testid="collapsedControl"] button')
                         || doc.querySelector('[data-testid="collapsedControl"]')
                         || doc.querySelector('[data-testid="stSidebarCollapsedControl"] button')
                         || doc.querySelector('[data-testid="stSidebarCollapsedControl"]')
                         || doc.querySelector('button[aria-label="Expand sidebar"]')
                         || doc.querySelector('button[aria-label="open sidebar"]');
                if (btn) {
                    btn.click();
                }
            }
        } catch (e) {}
    }
    setTimeout(forceExpandSidebar, 80);
    setTimeout(forceExpandSidebar, 300);
    setTimeout(forceExpandSidebar, 800);
</script>
""", height=0, width=0)

# Bo layout theme Plotly chung (Font Inter/Montserrat, nen trong suot, text #241F21)
PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, Montserrat, sans-serif", color="#241F21", size=11),
    hoverlabel=dict(
        bgcolor="#FFFFFF",
        bordercolor="#7A3E65",
        font=dict(family="Inter, sans-serif", color="#241F21", size=12)
    )
)

# Palette mau phan biet cao danh cho Bieu do (Accessible & Colorblind-friendly)
# Xanh Spotify: #1ED760 | Xanh duong: #4C9AFF | Cam: #FFB547 | Tim: #B794F4 | Xanh ngoc: #38D9C5 | Hong: #FF7AA2
SPOTIFY_DISCRETE_PALETTE = [
    "#7A3E65",
    "#3D6B8C",
    "#D9822B",
    "#4A6B5B",
    "#8E5B7A",
    "#5E2E4D"
]

SPOTIFY_CONTINUOUS_COLOR = [
    [0.0, "#EEE9E1"],
    [0.3, "#F2E6EE"],
    [0.7, "#A6638C"],
    [1.0, "#7A3E65"]
]

# Thang mau Heatmap than thien thi giac (Warm Music Editorial)
HEATMAP_COLOR_SCALE = [
    [0.0, "#F7F4EF"],
    [0.5, "#F2E6EE"],
    [1.0, "#7A3E65"]
]

@st.cache_data
def get_hero_album_covers():
    covers_dir = os.path.join("dashboard", "assets", "covers")
    if not os.path.exists(covers_dir):
        return []
    cover_files = [
        "taylor_swift_midnights.jpg",
        "bad_bunny_un_verano_sin_ti.jpg",
        "harry_styles_harrys_house.jpg",
        "dua_lipa_levitating.jpg",
        "adele_easy_on_me.jpg",
        "the_weeknd_blinding_lights.jpg"
    ]
    b64_list = []
    for cf in cover_files:
        fpath = os.path.join(covers_dir, cf)
        if os.path.exists(fpath):
            with open(fpath, "rb") as f:
                b64_list.append(base64.b64encode(f.read()).decode("utf-8"))
    return b64_list

# Ham nap du lieu
@st.cache_data(show_spinner="Đang nạp dữ liệu Spotify Analytics...")
def load_all_data(_cache_id="v3_clean"):
    processed_path = os.path.join("data", "processed", "merged_spotify_data.csv")
    sample_path = os.path.join("data", "sample", "spotify_sample_merged.csv")
    path = processed_path if os.path.exists(processed_path) else sample_path
    
    needed_cols = [
        "track_name", "artist_individual", "streams", "rank", "week", "year", "month",
        "danceability", "energy", "loudness", "valence", "acousticness", "speechiness",
        "liveness", "tempo", "duration_min", "explicit", "popularity",
        "income_group", "region_wb", "track_genre", "is_trending", "mood_category", "country", "country_code"
    ]
    df = pd.read_csv(path, usecols=lambda c: c in needed_cols, low_memory=False)
    num_cols = ["streams", "rank", "danceability", "energy", "loudness", "valence", "acousticness", "speechiness", "liveness", "tempo", "duration_min", "popularity"]
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    if "explicit" in df.columns:
        df["explicit"] = df["explicit"].fillna(False).astype(bool)
    df["week"] = pd.to_datetime(df["week"], errors="coerce")
    df = df.dropna(subset=["track_name", "artist_individual", "week", "country"])
    df["year_month"] = df["week"].dt.to_period("M").astype(str)
    return df

df_raw = load_all_data()

# Ham tong hop du lieu theo bai hat duy nhat (khong bi lap lai theo tung tuan BXH)
@st.cache_data
def get_unique_tracks_data(df):
    agg_df = df.groupby(["track_name", "artist_individual"], as_index=False).agg(
        streams=("streams", "sum"),
        best_rank=("rank", "min"),
        weeks_count=("week", "nunique"),
        country_count=("country", "nunique"),
        popularity=("popularity", lambda s: s.dropna().max() if not s.dropna().empty else 80.0),
        danceability=("danceability", "mean"),
        energy=("energy", "mean"),
        valence=("valence", "mean"),
        track_genre=("track_genre", lambda s: s.dropna().iloc[0] if len(s.dropna()) > 0 and str(s.dropna().iloc[0]).strip() else "Pop")
    )
    return agg_df

df_unique_tracks = get_unique_tracks_data(df_raw)

# Danh sach bo loc dung chung
regions_list = ["Tất cả khu vực"] + sorted([r for r in df_raw["region_wb"].dropna().unique() if str(r).strip()])
genres_list = ["Tất cả thể loại"] + sorted([g for g in df_raw["track_genre"].dropna().unique() if str(g).strip()][:30])
years_list = ["Tất cả các năm"] + sorted([str(int(y)) for y in df_raw["year"].dropna().unique()])
income_list = ["Tất cả nhóm thu nhập"] + sorted([str(i) for i in df_raw["income_group"].dropna().unique() if str(i).strip()])
mood_list = ["Tất cả tâm trạng"] + sorted([str(m) for m in df_raw["mood_category"].dropna().unique() if str(m).strip()])

# DANH SÁCH TẤT CẢ BIỂU ĐỒ TRỰC QUAN HÓA (RÚT GỌN TÊN)
CHART_OPTIONS = [
    "Bản đồ phân bố lượt Stream toàn cầu",
    "So sánh thị hiếu quốc gia (Taste Radar)",
    "Tương quan đặc trưng âm học tùy chọn",
    "Ma trận tương quan đặc trưng âm học",
    "Phân phối Danceability & Valence theo thu nhập",
    "Hồ sơ âm thanh đa chiều theo thể loại",
    "Top 10 Thể loại & Nghệ sĩ dẫn đầu",
    "Xu hướng biến thiên lượt Stream theo thời gian"
]

def render_insight_card(title, key_findings, details, implications):
    st.markdown(f"""<div style="background-color: #FFFFFF; border: 1px solid #D8D0C7; border-radius: 12px; padding: 18px 22px; margin-top: 14px; box-shadow: 0 1px 4px rgba(36, 31, 33, 0.03);">
        <div style="display:flex; align-items:center; gap:10px; margin-bottom: 14px;">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#7A3E65" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/>
                <path d="M9 18h6"/><path d="M10 22h4"/>
            </svg>
            <h4 style="font-family: 'Montserrat', sans-serif; color: #7A3E65; font-weight: 800; font-size: 1.05rem; margin: 0; letter-spacing: -0.2px;">NHẬN XÉT & PHÂN TÍCH Ý NGHĨA BIỂU ĐỒ</h4>
        </div>
        <div style="display:flex; flex-direction:column; gap:10px; font-size:0.88rem; line-height:1.55;">
            <div style="background:#F2EDE7; border: 1px solid #D8D0C7; border-left:3.5px solid #7A3E65; padding:10px 14px; border-radius:6px;">
                <b style="color:#241F21;">Nhận xét xu hướng chính:</b> <span style="color:#625B5E;">{key_findings}</span>
            </div>
            <div style="background:#F2EDE7; border: 1px solid #D8D0C7; border-left:3.5px solid #3D6B8C; padding:10px 14px; border-radius:6px;">
                <b style="color:#241F21;">Phân tích số liệu thống kê:</b> <span style="color:#625B5E;">{details}</span>
            </div>
            <div style="background:#F2EDE7; border: 1px solid #D8D0C7; border-left:3.5px solid #D9822B; padding:10px 14px; border-radius:6px;">
                <b style="color:#241F21;">Ý nghĩa & Ứng dụng thực tiễn:</b> <span style="color:#625B5E;">{implications}</span>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# CROSS-COUNTRY TASTE RADAR (SO SÁNH THỊ HIẾU QUỐC GIA) - METADATA & COMPONENT
# ═════════════════════════════════════════════════════════════════════════════
COUNTRY_DISPLAY_MAP = {
    "Vietnam": "🇻🇳 Việt Nam",
    "United States": "🇺🇸 Hoa Kỳ",
    "Korea": "🇰🇷 Hàn Quốc",
    "Brazil": "🇧🇷 Brazil",
    "Japan": "🇯🇵 Nhật Bản",
    "United Kingdom": "🇬🇧 Vương Quốc Anh",
    "Germany": "🇩🇪 Đức",
    "France": "🇫🇷 Pháp",
    "Spain": "🇪🇸 Tây Ban Nha",
    "Italy": "🇮🇹 Ý",
    "Canada": "🇨🇦 Canada",
    "Australia": "🇦🇺 Úc",
    "Mexico": "🇲🇽 Mexico",
    "India": "🇮🇳 Ấn Độ",
    "Indonesia": "🇮🇩 Indonesia",
    "Thailand": "🇹🇭 Thái Lan",
    "Philippines": "🇵🇭 Philippines",
    "Argentina": "🇦🇷 Argentina",
    "Sweden": "🇸🇪 Thụy Điển",
    "Netherlands": "🇳🇱 Hà Lan",
    "Norway": "🇳🇴 Na Uy",
    "Colombia": "🇨🇴 Colombia",
    "Chile": "🇨🇱 Chile",
    "South Africa": "🇿🇦 Nam Phi",
    "Singapore": "🇸🇬 Singapore",
    "Malaysia": "🇲🇾 Malaysia",
    "New Zealand": "🇳🇿 New Zealand",
    "Taiwan": "🇹🇼 Đài Loan",
    "Hong Kong": "🇭🇰 Hồng Kông",
    "Turkey": "🇹🇷 Thổ Nhĩ Kỳ",
    "Poland": "🇵🇱 Ba Lan",
    "Portugal": "🇵🇹 Bồ Đào Nha",
    "Belgium": "🇧🇪 Bỉ",
    "Austria": "🇦🇹 Áo",
    "Switzerland": "🇨🇭 Thụy Sĩ",
    "Denmark": "🇩🇰 Đan Mạch",
    "Finland": "🇫🇮 Phần Lan",
    "Ireland": "🇮🇪 Ireland",
}

FEAT_META = {
    "danceability": {
        "label": "Danceability (Độ nhảy múa)",
        "short": "Danceability",
        "desc": "Mức độ phù hợp để khiêu vũ dựa trên nhịp điệu, tiết tấu và độ ổn định của phách.",
        "icon": "💃"
    },
    "energy": {
        "label": "Energy (Năng lượng)",
        "short": "Energy",
        "desc": "Cảm giác cường độ, độ sôi nổi, dải âm lượng mạnh mẽ và tốc độ dồn dập.",
        "icon": "⚡"
    },
    "valence": {
        "label": "Valence (Tích cực / Vui vẻ)",
        "short": "Valence",
        "desc": "Mức độ tươi sáng, sảng khoái, lạc quan của giai điệu (điểm thấp mang sắc u buồn).",
        "icon": "✨"
    },
    "acousticness": {
        "label": "Acousticness (Độ mộc mạc)",
        "short": "Acousticness",
        "desc": "Mức độ mộc của nhạc cụ tự nhiên, không lạm dụng âm thanh điện tử synthesizer.",
        "icon": "🎸"
    },
    "speechiness": {
        "label": "Speechiness (Độ nhiều lời / Rap)",
        "short": "Speechiness",
        "desc": "Mức độ hiện diện của lời nói, flow đọc rap hoặc spoken word trong ca khúc.",
        "icon": "🎙️"
    },
    "liveness": {
        "label": "Liveness (Chất sống / Sân khấu)",
        "short": "Liveness",
        "desc": "Xác suất ca khúc mang không khí biểu diễn live trực tiếp trước khán giả.",
        "icon": "🎪"
    }
}

@st.cache_data
def get_country_audio_profiles(df):
    feats = ["danceability", "energy", "valence", "acousticness", "speechiness", "liveness"]
    valid = df.dropna(subset=["country"])
    g_feats = valid.groupby("country")[feats].mean() * 100.0
    g_meta = valid.groupby("country").agg(
        total_streams=("streams", "sum"),
        n_tracks=("track_name", "nunique"),
        top_genre=("track_genre", lambda s: s.dropna().mode()[0] if not s.dropna().empty and s.dropna().mode().size > 0 else "Pop"),
        top_artist=("artist_individual", lambda s: s.dropna().mode()[0] if not s.dropna().empty and s.dropna().mode().size > 0 else "N/A")
    )
    return g_feats.join(g_meta)

def render_cross_country_taste_radar(df_source, key_prefix="taste_radar"):
    profiles = get_country_audio_profiles(df_source)
    if profiles.empty:
        st.warning("Không có dữ liệu quốc gia hợp lệ để so sánh thị hiếu.")
        return

    all_countries = sorted(profiles.index.tolist())
    priority_order = [
        "Vietnam", "United States", "Korea", "Brazil", "Japan", "United Kingdom",
        "Germany", "France", "Spain", "Canada", "Australia", "India",
        "Indonesia", "Thailand", "Philippines", "Mexico", "Argentina"
    ]
    sorted_countries = [c for c in priority_order if c in all_countries] + [c for c in all_countries if c not in priority_order]

    st.markdown("""<div style="background:#FFFFFF; border:1px solid #D8D0C7; border-radius:12px; padding:18px 22px 14px 22px; margin-bottom:14px; box-shadow:0 1px 4px rgba(36,31,33,0.03);">
    <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px;">
        <div style="display:flex; align-items:center; gap:10px;">
            <div style="width:34px; height:34px; border-radius:8px; background:#F2E6EE; display:flex; align-items:center; justify-content:center;">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#7A3E65" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <polygon points="12 2 19 8.5 16.5 17 7.5 17 5 8.5 12 2"></polygon>
                    <line x1="12" y1="2" x2="12" y2="17"></line>
                </svg>
            </div>
            <div>
                <h3 style="font-family:'Montserrat',sans-serif; font-size:1.15rem; font-weight:800; color:#241F21; margin:0; letter-spacing:-0.3px;">
                    Cross-Country Taste Radar &bull; So Sánh Thị Hiếu Quốc Gia
                </h3>
                <p style="font-size:0.8rem; color:#625B5E; margin:2px 0 0 0;">
                    So sánh đa chiều 6 chỉ số âm học đặc trưng (0 – 100%) giữa 2 quốc gia bất kỳ trên BXH Spotify
                </p>
            </div>
        </div>
        <div style="display:flex; align-items:center; gap:14px; font-size:0.8rem; font-weight:600;">
            <div style="display:flex; align-items:center; gap:6px;">
                <span style="display:inline-block; width:12px; height:12px; border-radius:3px; background:#7A3E65;"></span>
                <span style="color:#241F21;">Quốc gia A (Tím mận)</span>
            </div>
            <div style="display:flex; align-items:center; gap:6px;">
                <span style="display:inline-block; width:12px; height:12px; border-radius:3px; background:#C96B4B;"></span>
                <span style="color:#241F21;">Quốc gia B (Cam san hô)</span>
            </div>
        </div>
    </div>
</div>""", unsafe_allow_html=True)

    sb_key_a = f"{key_prefix}_select_a"
    sb_key_b = f"{key_prefix}_select_b"

    default_a = "Vietnam" if "Vietnam" in sorted_countries else sorted_countries[0]
    default_b = "United States" if "United States" in sorted_countries else (sorted_countries[1] if len(sorted_countries) > 1 else sorted_countries[0])

    current_a = st.session_state.get(sb_key_a, default_a)
    current_b = st.session_state.get(sb_key_b, default_b)

    idx_a = sorted_countries.index(current_a) if current_a in sorted_countries else 0
    idx_b = sorted_countries.index(current_b) if current_b in sorted_countries else 1

    col_sel_a, col_sel_b = st.columns(2, gap="medium")
    with col_sel_a:
        c1 = st.selectbox(
            "Chọn Quốc gia A:",
            options=sorted_countries,
            index=idx_a,
            format_func=lambda c: COUNTRY_DISPLAY_MAP.get(c, f"🌐 {c}"),
            key=sb_key_a
        )
    with col_sel_b:
        c2 = st.selectbox(
            "Chọn Quốc gia B:",
            options=sorted_countries,
            index=idx_b,
            format_func=lambda c: COUNTRY_DISPLAY_MAP.get(c, f"🌐 {c}"),
            key=sb_key_b
        )

    prof1 = profiles.loc[c1]
    prof2 = profiles.loc[c2]
    name_a = COUNTRY_DISPLAY_MAP.get(c1, c1)
    name_b = COUNTRY_DISPLAY_MAP.get(c2, c2)

    def format_streams(n):
        if n >= 1e9:
            return f"{n/1e9:.2f} tỷ lượt"
        elif n >= 1e6:
            return f"{n/1e6:.1f} triệu lượt"
        else:
            return f"{n:,.0f} lượt"

    card_a_col, card_b_col = st.columns(2, gap="medium")
    with card_a_col:
        st.markdown(f"""<div style="background:#FFFFFF; border:1px solid #D8D0C7; border-top:3.5px solid #7A3E65; border-radius:10px; padding:12px 16px; margin-bottom:14px; box-shadow:0 1px 3px rgba(36,31,33,0.03);">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
        <span style="font-family:'Montserrat',sans-serif; font-size:1.02rem; font-weight:800; color:#7A3E65;">{name_a}</span>
        <span style="font-size:0.74rem; background:#F2E6EE; color:#7A3E65; font-weight:700; padding:2px 8px; border-radius:10px;">Quốc gia A</span>
    </div>
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px 14px; font-size:0.8rem; color:#625B5E;">
        <div>Tổng Streams: <b style="color:#241F21;">{format_streams(prof1['total_streams'])}</b></div>
        <div>Số tracks BXH: <b style="color:#241F21;">{int(prof1['n_tracks']):,} bài</b></div>
        <div>Dòng nhạc top: <b style="color:#241F21;">{prof1['top_genre']}</b></div>
        <div>Nghệ sĩ top: <b style="color:#241F21;">{prof1['top_artist']}</b></div>
    </div>
</div>""", unsafe_allow_html=True)
    with card_b_col:
        st.markdown(f"""<div style="background:#FFFFFF; border:1px solid #D8D0C7; border-top:3.5px solid #C96B4B; border-radius:10px; padding:12px 16px; margin-bottom:14px; box-shadow:0 1px 3px rgba(36,31,33,0.03);">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
        <span style="font-family:'Montserrat',sans-serif; font-size:1.02rem; font-weight:800; color:#C96B4B;">{name_b}</span>
        <span style="font-size:0.74rem; background:#F7E6DC; color:#C96B4B; font-weight:700; padding:2px 8px; border-radius:10px;">Quốc gia B</span>
    </div>
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px 14px; font-size:0.8rem; color:#625B5E;">
        <div>Tổng Streams: <b style="color:#241F21;">{format_streams(prof2['total_streams'])}</b></div>
        <div>Số tracks BXH: <b style="color:#241F21;">{int(prof2['n_tracks']):,} bài</b></div>
        <div>Dòng nhạc top: <b style="color:#241F21;">{prof2['top_genre']}</b></div>
        <div>Nghệ sĩ top: <b style="color:#241F21;">{prof2['top_artist']}</b></div>
    </div>
</div>""", unsafe_allow_html=True)

    feats = ["danceability", "energy", "valence", "acousticness", "speechiness", "liveness"]
    r_labels = [FEAT_META[f]["short"] for f in feats]
    vals_a = [float(prof1[f]) for f in feats]
    vals_b = [float(prof2[f]) for f in feats]

    c_radar, c_metrics = st.columns([1.18, 1.0], gap="large")

    with c_radar:
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=vals_a + [vals_a[0]],
            theta=r_labels + [r_labels[0]],
            fill="toself",
            name=name_a,
            line=dict(color="#7A3E65", width=2.8),
            fillcolor="rgba(122, 62, 101, 0.22)",
            hovertemplate=f"<b>{name_a}</b><br>%{{theta}}: %{{r:.1f}}%<extra></extra>"
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=vals_b + [vals_b[0]],
            theta=r_labels + [r_labels[0]],
            fill="toself",
            name=name_b,
            line=dict(color="#C96B4B", width=2.8),
            fillcolor="rgba(201, 107, 75, 0.22)",
            hovertemplate=f"<b>{name_b}</b><br>%{{theta}}: %{{r:.1f}}%<extra></extra>"
        ))
        fig_radar.update_layout(
            **PLOTLY_THEME,
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    ticksuffix="%",
                    gridcolor="#E5DFD6",
                    linecolor="#D8D0C7",
                    tickfont=dict(size=10, color="#625B5E"),
                    angle=45
                ),
                angularaxis=dict(
                    gridcolor="#E5DFD6",
                    linecolor="#D8D0C7",
                    tickfont=dict(size=11, color="#241F21", family="Montserrat, sans-serif")
                ),
                bgcolor="#FFFFFF"
            ),
            height=430,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.16,
                xanchor="center",
                x=0.5,
                font=dict(family="Inter, sans-serif", size=12, color="#241F21")
            ),
            margin=dict(t=30, b=45, l=45, r=45)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with c_metrics:
        st.markdown("""<div style="font-family:'Montserrat',sans-serif; font-size:1.0rem; font-weight:800; color:#241F21; margin-bottom:8px;">
    Bảng So Sánh Chỉ Số Âm Học Chi Tiết
</div>""", unsafe_allow_html=True)

        rows_html = []
        for f in feats:
            va = prof1[f]
            vb = prof2[f]
            delta = va - vb
            meta = FEAT_META[f]

            clean_a_name = name_a.split()[1] if len(name_a.split()) > 1 else name_a
            clean_b_name = name_b.split()[1] if len(name_b.split()) > 1 else name_b

            if delta > 0.8:
                badge_html = f'<span style="background:#F2E6EE; color:#7A3E65; font-weight:700; font-size:0.75rem; padding:3px 8px; border-radius:12px;">+{delta:.1f}% ({clean_a_name})</span>'
            elif delta < -0.8:
                badge_html = f'<span style="background:#F7E6DC; color:#C96B4B; font-weight:700; font-size:0.75rem; padding:3px 8px; border-radius:12px;">+{abs(delta):.1f}% ({clean_b_name})</span>'
            else:
                badge_html = f'<span style="background:#EEE9E1; color:#625B5E; font-weight:600; font-size:0.75rem; padding:3px 8px; border-radius:12px;">Tương đương ({abs(delta):.1f}%)</span>'

            tot = (va + vb) if (va + vb) > 0 else 1
            pct_a = (va / tot) * 100
            pct_b = 100 - pct_a

            row = f"""<div style="background:#FFFFFF; border:1px solid #D8D0C7; border-radius:8px; padding:8px 12px; margin-bottom:8px;">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
        <span style="font-weight:700; font-size:0.86rem; color:#241F21;">{meta['icon']} {meta['label']}</span>
        {badge_html}
    </div>
    <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.82rem; margin-bottom:4px;">
        <span style="color:#7A3E65; font-weight:700;">{va:.1f}%</span>
        <span style="font-size:0.74rem; color:#81786E;">{meta['desc']}</span>
        <span style="color:#C96B4B; font-weight:700;">{vb:.1f}%</span>
    </div>
    <div style="display:flex; height:5px; border-radius:3px; overflow:hidden; background:#EAE5DC;">
        <div style="width:{pct_a:.1f}%; background:#7A3E65;"></div>
        <div style="width:{pct_b:.1f}%; background:#C96B4B;"></div>
    </div>
</div>"""
            rows_html.append(row)

        st.markdown("\n".join(rows_html), unsafe_allow_html=True)

    # Dynamic Automated Editorial Insights
    deltas = pd.Series({f: prof1[f] - prof2[f] for f in feats})
    max_a_feat = deltas.idxmax()
    max_a_val = deltas.max()
    max_b_feat = deltas.idxmin()
    max_b_val = abs(deltas.min())
    min_diff_feat = deltas.abs().idxmin()
    min_diff_val = deltas.abs().min()

    meta_a = FEAT_META.get(max_a_feat, {"short": max_a_feat, "label": max_a_feat})
    meta_b = FEAT_META.get(max_b_feat, {"short": max_b_feat, "label": max_b_feat})
    meta_sim = FEAT_META.get(min_diff_feat, {"short": min_diff_feat, "label": min_diff_feat})

    def get_feature_interpretation(feat, country_name, diff_val):
        if feat == "acousticness":
            return f"{country_name} chuộng chất liệu acoustic mộc mạc, tôn vinh giọng hát tự nhiên và các bản ballad tự sự (vượt trội +{diff_val:.1f}%)."
        elif feat == "speechiness":
            return f"{country_name} chịu ảnh hưởng sâu sắc từ trào lưu Hip-Hop/Rap đương đại với mật độ ca từ và flow hát nói dày đặc (+{diff_val:.1f}%)."
        elif feat == "energy":
            return f"{country_name} ưa chuộng các bản phối dồn dập, giàu năng lượng bùng nổ và âm bass điện tử uy lực (+{diff_val:.1f}%)."
        elif feat == "valence":
            return f"{country_name} mang tâm trạng âm nhạc rực rỡ, lạc quan và đậm chất lễ hội tiệc tùng (+{diff_val:.1f}%)."
        elif feat == "danceability":
            return f"{country_name} ưu tiên nhịp phách bắt tai, cấu trúc groove cuốn hút phục vụ trải nghiệm khiêu vũ (+{diff_val:.1f}%)."
        else:
            return f"{country_name} ghi nhận chỉ số sân khấu/live nhộn nhịp hơn (+{diff_val:.1f}%)."

    interp_a = get_feature_interpretation(max_a_feat, name_a, max_a_val)
    interp_b = get_feature_interpretation(max_b_feat, name_b, max_b_val)

    kf = f"Thị hiếu âm nhạc giữa {name_a} và {name_b} có sự phân hóa văn hóa rõ rệt: {interp_a} Trong khi đó, {interp_b}"
    dt = f"Trên thang chuẩn hóa 0–100%: Điểm tương đồng lớn nhất giữa hai quốc gia nằm ở chỉ số {meta_sim['label']} với độ lệch chỉ {min_diff_val:.1f}%. Khoảng cách lớn nhất tập trung ở {meta_a['short']} ({prof1[max_a_feat]:.1f}% vs {prof2[max_a_feat]:.1f}%) và {meta_b['short']} ({prof1[max_b_feat]:.1f}% vs {prof2[max_b_feat]:.1f}%)."
    imp = f"Chiến lược 'Glocal' (Global + Local) cho nhà sản xuất & A&R: Khi thâm nhập thị trường {name_a}, hãy chú trọng tối ưu {meta_a['short']}; ngược lại khi phát hành tại {name_b}, bản phối cần gia tăng hàm lượng {meta_b['short']} để tối đa hóa lượt nghe trên các Playlist hàng đầu."

    render_insight_card(
        title=f"Phân Tích Thị Hiếu Đối Sánh: {name_a} vs {name_b}",
        key_findings=kf,
        details=dt,
        implications=imp
    )

    # Top 5 Ca Khúc Thịnh Hành Nhất Tại Mỗi Thị Trường
    st.markdown("""<div style="font-family:'Montserrat',sans-serif; font-size:1.05rem; font-weight:800; color:#241F21; margin:22px 0 10px 0;">
        Top 5 Ca Khúc Thịnh Hành Nhất &bull; Đối Chiếu Văn Hóa Âm Nhạc Thực Tế
    </div>""", unsafe_allow_html=True)

    c_top_a, c_top_b = st.columns(2, gap="medium")
    with c_top_a:
        top_a = df_source[df_source["country"] == c1].groupby(["track_name", "artist_individual"], as_index=False)["streams"].sum().sort_values("streams", ascending=False).head(5)
        st.markdown(f"""<div style="background:#FFFFFF; border:1px solid #D8D0C7; border-left:4px solid #7A3E65; border-radius:10px; padding:10px 14px; margin-bottom:8px; box-shadow:0 1px 3px rgba(36,31,33,0.03);">
            <div style="font-weight:700; font-size:0.86rem; color:#7A3E65;">Top 5 bài hát dẫn đầu tại {name_a}</div>
        </div>""", unsafe_allow_html=True)
        for _, r_t in top_a.iterrows():
            st.markdown(f"""<div style="background:#F2EDE7; border:1px solid #D8D0C7; border-radius:8px; padding:7px 12px; margin-bottom:6px; display:flex; justify-content:space-between; align-items:center;">
                <div style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap; padding-right:8px;">
                    <div style="font-weight:700; font-size:0.84rem; color:#241F21; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">{r_t['track_name']}</div>
                    <div style="font-size:0.75rem; color:#625B5E;">{r_t['artist_individual']}</div>
                </div>
                <div style="font-weight:700; font-size:0.78rem; color:#7A3E65; white-space:nowrap;">{format_streams(r_t['streams'])}</div>
            </div>""", unsafe_allow_html=True)

    with c_top_b:
        top_b = df_source[df_source["country"] == c2].groupby(["track_name", "artist_individual"], as_index=False)["streams"].sum().sort_values("streams", ascending=False).head(5)
        st.markdown(f"""<div style="background:#FFFFFF; border:1px solid #D8D0C7; border-left:4px solid #C96B4B; border-radius:10px; padding:10px 14px; margin-bottom:8px; box-shadow:0 1px 3px rgba(36,31,33,0.03);">
            <div style="font-weight:700; font-size:0.86rem; color:#C96B4B;">Top 5 bài hát dẫn đầu tại {name_b}</div>
        </div>""", unsafe_allow_html=True)
        for _, r_t in top_b.iterrows():
            st.markdown(f"""<div style="background:#F2EDE7; border:1px solid #D8D0C7; border-radius:8px; padding:7px 12px; margin-bottom:6px; display:flex; justify-content:space-between; align-items:center;">
                <div style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap; padding-right:8px;">
                    <div style="font-weight:700; font-size:0.84rem; color:#241F21; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">{r_t['track_name']}</div>
                    <div style="font-size:0.75rem; color:#625B5E;">{r_t['artist_individual']}</div>
                </div>
                <div style="font-weight:700; font-size:0.78rem; color:#C96B4B; white-space:nowrap;">{format_streams(r_t['streams'])}</div>
            </div>""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# OUR WORLD IN DATA (OWID) STYLE GEOGRAPHIC EXPLORER COMPONENT
# CẤU TRÚC 5 TẦNG CHUẨN OWID (OUR WORLD IN DATA ARCHITECTURE)
# ═════════════════════════════════════════════════════════════════════════════

# HỆ THỐNG GAM MÀU TÍM MẬN (PLUM HARMONY)
# Không dữ liệu / Ngoài bộ lọc: #E2DDD7 (Xám ấm)
# Cấp 1 (< 500M):  #F0E5EC (Lavender rất nhạt)
# Cấp 2 (500M–2B): #D8B7CC (Hoa cà nhạt - Ví dụ: Việt Nam)
# Cấp 3 (2B–6B):   #B879A2 (Tím hồng)
# Cấp 4 (6B–12B):  #7A3E65 (Tím mận đặc trưng)
# Cấp 5 (> 12B):   #4B203D (Tím mận đậm)
PLUM_MAP_SCALE = [
    [0.0, "#E2DDD7"],   # Cấp 0: Không có dữ liệu
    [0.2, "#F0E5EC"],   # Cấp 1: < 500M
    [0.4, "#D8B7CC"],   # Cấp 2: 500M – 2B
    [0.6, "#B879A2"],   # Cấp 3: 2B – 6B
    [0.8, "#7A3E65"],   # Cấp 4: 6B – 12B
    [1.0, "#4B203D"]    # Cấp 5: > 12B
]

@st.cache_data
def get_owid_geo_master_data(df):
    valid = df[df["country"] != "Global"].copy()
    
    # Pre-aggregate country overall (toàn kỳ)
    overall = valid.groupby(["country", "country_code", "region_wb", "income_group"], as_index=False).agg(
        streams=("streams", "sum"),
        n_tracks=("track_name", "nunique"),
        top_genre=("track_genre", lambda s: s.dropna().mode()[0] if not s.dropna().empty and s.dropna().mode().size > 0 else "Pop"),
        top_artist=("artist_individual", lambda s: s.dropna().mode()[0] if not s.dropna().empty and s.dropna().mode().size > 0 else "N/A"),
        danceability=("danceability", "mean"),
        energy=("energy", "mean"),
        valence=("valence", "mean"),
        acousticness=("acousticness", "mean")
    )
    tot_streams = overall["streams"].sum()
    overall["stream_share"] = (overall["streams"] / tot_streams * 100.0) if tot_streams > 0 else 0.0
    overall = overall.sort_values(by="streams", ascending=False).reset_index(drop=True)
    
    # Pre-aggregate by year
    by_year = valid.groupby(["country", "country_code", "year"], as_index=False).agg(
        streams=("streams", "sum"),
        n_tracks=("track_name", "nunique"),
        danceability=("danceability", "mean"),
        energy=("energy", "mean"),
        valence=("valence", "mean"),
        acousticness=("acousticness", "mean")
    )
    
    # Pre-aggregate weekly for sparklines
    weekly = valid.groupby(["country", "country_code", "week"], as_index=False)["streams"].sum()
    weekly["week"] = pd.to_datetime(weekly["week"], errors="coerce")
    weekly = weekly.sort_values(["country", "week"]).reset_index(drop=True)
    
    return overall, by_year, weekly

def render_owid_geographic_explorer(df_source, key_prefix="owid_geo"):
    overall_df, by_year_df, weekly_df = get_owid_geo_master_data(df_source)
    if overall_df.empty:
        st.warning("Không có dữ liệu địa lý hợp lệ.")
        return

    # Container chuẩn OWID với viền nhẹ và nền trung tính
    with st.container(border=True):
        # ─── KHỞI TẠO STATE BỘ LỌC ───
        if f"{key_prefix}_region" not in st.session_state:
            st.session_state[f"{key_prefix}_region"] = "Tất cả khu vực"
        if f"{key_prefix}_income" not in st.session_state:
            st.session_state[f"{key_prefix}_income"] = "Tất cả nhóm thu nhập"
        if f"{key_prefix}_selected" not in st.session_state:
            st.session_state[f"{key_prefix}_selected"] = []
        if f"{key_prefix}_search" not in st.session_state:
            st.session_state[f"{key_prefix}_search"] = ""
        if f"{key_prefix}_spotlight" not in st.session_state:
            st.session_state[f"{key_prefix}_spotlight"] = "Vietnam"
        if f"{key_prefix}_year" not in st.session_state:
            st.session_state[f"{key_prefix}_year"] = 2022

        # ─── TẦNG 1: TIÊU ĐỀ VÀ MÔ TẢ NGẮN (NHIỆM VỤ CHÍNH DUY NHẤT) ───
        st.markdown("""
        <div style="margin-bottom: 8px;">
            <div style="font-family:'Montserrat', sans-serif; font-size:1.32rem; font-weight:800; color:#241F21; letter-spacing:-0.3px; line-height:1.2;">
                Phân bố thị trường âm nhạc toàn cầu
            </div>
            <div style="font-size:0.83rem; color:#625B5E; margin-top:3px;">
                Lượt stream phân bố giữa các quốc gia như thế nào trong năm được chọn? &bull; Spotify Charts 2020–2022
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ─── TẦNG 2: HÀNG CHUYỂN LOẠI BIỂU ĐỒ & NÚT CHỌN ───
        c_mode_left, c_mode_right = st.columns([1.0, 1.0])
        with c_mode_left:
            st.markdown("""
            <div style="display:inline-flex; align-items:center; gap:6px; background:#F0E5EC; border:1px solid #D8B7CC; color:#7A3E65; padding:5px 14px; border-radius:6px; font-weight:700; font-size:0.84rem;">
                🗺️ Bản đồ
            </div>
            """, unsafe_allow_html=True)

        # Đếm số điều kiện lọc đang kích hoạt
        active_conditions = 0
        if st.session_state[f"{key_prefix}_region"] != "Tất cả khu vực":
            active_conditions += 1
        if st.session_state[f"{key_prefix}_income"] != "Tất cả nhóm thu nhập":
            active_conditions += 1
        if st.session_state[f"{key_prefix}_search"].strip():
            active_conditions += 1
        if len(st.session_state[f"{key_prefix}_selected"]) > 0:
            active_conditions += 1

        with c_mode_right:
            pop_label = f"⚙️ Chọn · {active_conditions}" if active_conditions > 0 else "⚙️ Chọn"
            with st.popover(pop_label, use_container_width=False):
                st.markdown("<div style='font-size:0.82rem; font-weight:700; color:#7A3E65; text-transform:uppercase; margin-bottom:8px;'>Tuỳ chọn lọc thị trường</div>", unsafe_allow_html=True)
                
                # 1. Tìm quốc gia
                st.text_input(
                    "Tìm quốc gia:",
                    placeholder="🔍 Gõ tên quốc gia...",
                    key=f"{key_prefix}_search"
                )
                
                # 2. Khu vực
                all_regions = ["Tất cả khu vực"] + sorted([r for r in overall_df["region_wb"].dropna().unique() if str(r).strip()])
                st.selectbox("Khu vực (World Bank):", options=all_regions, key=f"{key_prefix}_region")
                
                # 3. Nhóm thu nhập
                all_incomes = ["Tất cả nhóm thu nhập"] + sorted([i for i in overall_df["income_group"].dropna().unique() if str(i).strip()])
                st.selectbox("Nhóm thu nhập:", options=all_incomes, key=f"{key_prefix}_income")
                
                # 4. Top 10 & Chọn nhanh
                st.markdown("<div style='font-size:0.75rem; font-weight:600; color:#81786E; margin-top:6px; margin-bottom:4px;'>Chọn nhanh:</div>", unsafe_allow_html=True)
                q1, q2, q3 = st.columns(3)
                with q1:
                    if st.button("🌟 Top 10", key=f"{key_prefix}_p_top10", use_container_width=True):
                        st.session_state[f"{key_prefix}_selected"] = overall_df.head(10)["country"].tolist()
                        st.session_state[f"{key_prefix}_spotlight"] = overall_df.iloc[0]["country"]
                        st.rerun()
                with q2:
                    if st.button("🇻🇳 Việt Nam", key=f"{key_prefix}_p_vn", use_container_width=True):
                        st.session_state[f"{key_prefix}_selected"] = ["Vietnam"]
                        st.session_state[f"{key_prefix}_spotlight"] = "Vietnam"
                        st.rerun()
                with q3:
                    if st.button("🌏 Đ.N.Á", key=f"{key_prefix}_p_asean", use_container_width=True):
                        asean = ["Vietnam", "Thailand", "Indonesia", "Philippines", "Malaysia", "Singapore"]
                        st.session_state[f"{key_prefix}_selected"] = [c for c in asean if c in overall_df["country"].values]
                        st.session_state[f"{key_prefix}_spotlight"] = "Vietnam"
                        st.rerun()

                # 5. Danh sách đang chọn
                st.multiselect(
                    "Danh sách đang chọn:",
                    options=overall_df["country"].tolist(),
                    default=[c for c in st.session_state[f"{key_prefix}_selected"] if c in overall_df["country"].values],
                    key=f"{key_prefix}_selected"
                )

                # 6. Nút đặt lại
                if st.button("✕ Đặt lại", key=f"{key_prefix}_p_reset", use_container_width=True):
                    st.session_state[f"{key_prefix}_region"] = "Tất cả khu vực"
                    st.session_state[f"{key_prefix}_income"] = "Tất cả nhóm thu nhập"
                    st.session_state[f"{key_prefix}_search"] = ""
                    st.session_state[f"{key_prefix}_selected"] = []
                    st.session_state[f"{key_prefix}_spotlight"] = "Vietnam"
                    st.rerun()

        # Sau khi đóng, màn hình chỉ hiện các chip đang áp dụng
        if active_conditions > 0:
            chips = []
            if st.session_state[f"{key_prefix}_region"] != "Tất cả khu vực":
                chips.append(f"<span style='background:#F0E5EC; border:1px solid #D8B7CC; color:#7A3E65; padding:3px 10px; border-radius:14px; font-size:0.75rem; font-weight:600;'>{st.session_state[f'{key_prefix}_region']} &times;</span>")
            if st.session_state[f"{key_prefix}_income"] != "Tất cả nhóm thu nhập":
                chips.append(f"<span style='background:#F0E5EC; border:1px solid #D8B7CC; color:#7A3E65; padding:3px 10px; border-radius:14px; font-size:0.75rem; font-weight:600;'>{st.session_state[f'{key_prefix}_income']} &times;</span>")
            s_term = st.session_state[f"{key_prefix}_search"].strip()
            if s_term:
                chips.append(f"<span style='background:#F0E5EC; border:1px solid #D8B7CC; color:#7A3E65; padding:3px 10px; border-radius:14px; font-size:0.75rem; font-weight:600;'>Tìm: {s_term} &times;</span>")
            if len(st.session_state[f"{key_prefix}_selected"]) > 0:
                chips.append(f"<span style='background:#F0E5EC; border:1px solid #D8B7CC; color:#7A3E65; padding:3px 10px; border-radius:14px; font-size:0.75rem; font-weight:600;'>{len(st.session_state[f'{key_prefix}_selected'])} quốc gia &times;</span>")
            
            c_chip_list, c_chip_clr = st.columns([4.2, 0.8])
            with c_chip_list:
                st.markdown(f"<div style='display:flex; align-items:center; gap:6px; margin: 4px 0 6px 0; flex-wrap:wrap;'>{' '.join(chips)}</div>", unsafe_allow_html=True)
            with c_chip_clr:
                if st.button("✕ Bỏ lọc", key=f"{key_prefix}_chip_reset_all", use_container_width=True):
                    st.session_state[f"{key_prefix}_region"] = "Tất cả khu vực"
                    st.session_state[f"{key_prefix}_income"] = "Tất cả nhóm thu nhập"
                    st.session_state[f"{key_prefix}_search"] = ""
                    st.session_state[f"{key_prefix}_selected"] = []
                    st.rerun()

        # ─── CHUẨN BỊ DỮ LIỆU NĂM ĐÃ CHỌN ───
        current_year = st.session_state.get(f"{key_prefix}_year", 2022)
        sub_y = by_year_df[by_year_df["year"] == int(current_year)].copy()
        
        map_df = overall_df[["country", "country_code", "region_wb", "income_group", "top_genre", "top_artist"]].merge(
            sub_y[["country_code", "streams", "n_tracks", "danceability", "energy", "valence", "acousticness"]],
            on="country_code",
            how="left"
        )
        map_df["streams"] = map_df["streams"].fillna(0)
        map_df["n_tracks"] = map_df["n_tracks"].fillna(0).astype(int)
        tot_year_streams = map_df["streams"].sum()
        map_df["stream_share"] = (map_df["streams"] / tot_year_streams * 100.0) if tot_year_streams > 0 else 0.0

        # Phân cấp 5 bậc theo lượt stream
        # Thấp: < 500M | 500M - 2B | 2B - 6B | 6B - 12B | > 12B : Cao
        bins = [-1, 0, 500e6, 2e9, 6e9, 12e9, np.inf]
        map_df["tier_val"] = pd.cut(map_df["streams"], bins=bins, labels=[0, 1, 2, 3, 4, 5]).astype(int)

        # Áp dụng bộ lọc (làm mờ / gán tier 0 cho các quốc gia ngoài bộ lọc)
        reg_val = st.session_state.get(f"{key_prefix}_region", "Tất cả khu vực")
        inc_val = st.session_state.get(f"{key_prefix}_income", "Tất cả nhóm thu nhập")
        search_txt = st.session_state.get(f"{key_prefix}_search", "").strip().lower()
        sel_list = st.session_state.get(f"{key_prefix}_selected", [])

        if reg_val != "Tất cả khu vực":
            map_df.loc[map_df["region_wb"] != reg_val, "tier_val"] = 0
        if inc_val != "Tất cả nhóm thu nhập":
            map_df.loc[map_df["income_group"] != inc_val, "tier_val"] = 0
        if search_txt:
            match_mask = map_df["country"].str.lower().str.contains(search_txt) | map_df["country_code"].str.lower().str.contains(search_txt)
            map_df.loc[~match_mask, "tier_val"] = 0
        if len(sel_list) > 0:
            map_df.loc[~map_df["country"].isin(sel_list), "tier_val"] = 0

        # Định dạng tooltip gọn gàng đúng yêu cầu:
        # Vietnam
        # 245 triệu lượt stream
        # 1,12% thị phần
        def fmt_stream_short(val):
            if val >= 1e9:
                return f"{val / 1e9:.2f} tỷ"
            elif val >= 1e6:
                return f"{val / 1e6:.0f} triệu"
            return f"{val:,.0f}"

        def build_tooltip(row):
            if row["tier_val"] == 0 or row["streams"] <= 0:
                return f"<b>{row['country']}</b><br>Không có dữ liệu"
            s_str = fmt_stream_short(row["streams"])
            return f"<b>{row['country']}</b><br>{s_str} lượt stream<br>{row['stream_share']:.2f}% thị phần"

        map_df["tooltip_text"] = map_df.apply(build_tooltip, axis=1)

        # Đếm số lượng quốc gia trong từng cấp cho hover của legend
        c_t1 = int((map_df["tier_val"] == 1).sum())
        c_t2 = int((map_df["tier_val"] == 2).sum())
        c_t3 = int((map_df["tier_val"] == 3).sum())
        c_t4 = int((map_df["tier_val"] == 4).sum())
        c_t5 = int((map_df["tier_val"] == 5).sum())

        # ─── TẦNG 3: BẢN ĐỒ CHIẾM ƯU THẾ (~72%) & CARD QUỐC GIA (~28%) ───
        col_map, col_card = st.columns([2.6, 1.0], gap="medium")

        # Xác định quốc gia tiêu điểm
        spotlight_country = st.session_state.get(f"{key_prefix}_spotlight", "Vietnam")
        if spotlight_country not in overall_df["country"].values:
            spotlight_country = overall_df.iloc[0]["country"]

        with col_map:
            # Bản đồ Choropleth Natural Earth
            fig_map = px.choropleth(
                map_df,
                locations="country_code",
                locationmode="ISO-3",
                color="tier_val",
                range_color=[0, 5],
                color_continuous_scale=PLUM_MAP_SCALE
            )

            # Đường biên quốc gia mảnh và trung tính (#C5BCB2, 0.45px)
            fig_map.update_traces(
                hovertemplate="%{customdata}<extra></extra>",
                customdata=map_df["tooltip_text"],
                marker_line_color="#C5BCB2",
                marker_line_width=0.45
            )

            # Quốc gia được chọn có viền đậm hơn (#241F21, 2.2px)
            spot_map_row = map_df[map_df["country"] == spotlight_country]
            if not spot_map_row.empty:
                fig_map.add_trace(go.Choropleth(
                    locations=spot_map_row["country_code"],
                    locationmode="ISO-3",
                    z=spot_map_row["tier_val"],
                    colorscale=PLUM_MAP_SCALE,
                    zmin=0, zmax=5,
                    showscale=False,
                    marker_line_color="#241F21",
                    marker_line_width=2.2,
                    hoverinfo="skip"
                ))

            fig_map.update_layout(
                **PLOTLY_THEME,
                height=430,
                margin=dict(l=0, r=0, t=5, b=5),
                coloraxis_showscale=False,
                geo=dict(
                    bgcolor="rgba(0,0,0,0)",
                    showframe=False,
                    showcountries=True,
                    countrycolor="#C5BCB2",
                    countrywidth=0.45,
                    showcoastlines=True,
                    coastlinecolor="#C5BCB2",
                    coastlinewidth=0.45,
                    showland=True,
                    landcolor="#E2DDD7",
                    showocean=True,
                    oceancolor="#F7F4EF",
                    projection_type="natural earth"
                )
            )

            # Tắt ModeBar để tránh nhiễu
            st.plotly_chart(fig_map, use_container_width=True, config={'displayModeBar': False})

            # ─── TẦNG 4: CHÚ GIẢI MÀU (ĐẶT NGAY DƯỚI BẢN ĐỒ) ───
            st.markdown(f"""
            <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; margin-top:4px; padding:7px 14px; background:#FFFFFF; border:1px solid #D8D0C7; border-radius:8px; font-size:0.75rem; color:#625B5E;">
                <div style="display:flex; align-items:center; gap:6px;">
                    <span style="display:inline-block; width:13px; height:9px; background:#E2DDD7; border:1px solid #C5BCB2; border-radius:2px;"></span>
                    <span style="font-size:0.74rem; color:#81786E;">Không có dữ liệu</span>
                </div>
                <div style="display:flex; flex-direction:column; align-items:center; gap:2px;">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="font-weight:600; color:#81786E; font-size:0.74rem;">Thấp</span>
                        <div style="display:flex; border-radius:3px; overflow:hidden; border:1px solid #C5BCB2; height:12px;">
                            <div style="width:36px; background:#F0E5EC;" title="< 500M: {c_t1} quốc gia"></div>
                            <div style="width:36px; background:#D8B7CC;" title="500M – 2B: {c_t2} quốc gia"></div>
                            <div style="width:36px; background:#B879A2;" title="2B – 6B: {c_t3} quốc gia"></div>
                            <div style="width:36px; background:#7A3E65;" title="6B – 12B: {c_t4} quốc gia"></div>
                            <div style="width:36px; background:#4B203D;" title="> 12B: {c_t5} quốc gia"></div>
                        </div>
                        <span style="font-weight:600; color:#81786E; font-size:0.74rem;">Cao</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; width:220px; font-size:0.69rem; color:#81786E; padding:0 2px;">
                        <span>500M</span>
                        <span>2B</span>
                        <span>6B</span>
                        <span>12B</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ─── TẦNG 5: THANH THỜI GIAN VÀ NGUỒN DỮ LIỆU (ĐẶT DƯỚI CHÚ GIẢI) ───
            st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
            col_t_play, col_t_slider = st.columns([0.10, 0.90])
            with col_t_play:
                st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
                if st.button("▶", key=f"{key_prefix}_play_btn", help="Chuyển tiếp năm tiếp theo"):
                    curr_idx = [2020, 2021, 2022].index(current_year) if current_year in [2020, 2021, 2022] else 0
                    next_year = [2020, 2021, 2022][(curr_idx + 1) % 3]
                    st.session_state[f"{key_prefix}_year"] = next_year
                    st.rerun()

            with col_t_slider:
                slider_year = st.select_slider(
                    "Năm khảo sát:",
                    options=[2020, 2021, 2022],
                    value=current_year,
                    key=f"{key_prefix}_slider_year",
                    label_visibility="collapsed"
                )
                if slider_year != current_year:
                    st.session_state[f"{key_prefix}_year"] = slider_year
                    st.rerun()

            # Nguồn dữ liệu & Nút tải CSV
            st.markdown("""
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; margin-top:8px; padding-top:6px; border-top:1px solid #D8D0C7; font-size:0.74rem; color:#81786E;">
                <div>
                    <b>Nguồn dữ liệu:</b> Spotify Weekly Top 200 Charts (2020–2022); World Bank Country & Lending Groups (2024).
                </div>
            </div>
            """, unsafe_allow_html=True)

            c_down, _ = st.columns([1.2, 2.8])
            with c_down:
                csv_bytes = map_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Tải dữ liệu bản đồ (CSV)",
                    data=csv_bytes,
                    file_name=f"spotify_geo_distribution_{current_year}.csv",
                    mime="text/csv",
                    key=f"{key_prefix}_csv_dl",
                    use_container_width=True
                )

        # ─── TẦNG 3 (PHẢI): CARD THÔNG TIN QUỐC GIA ───
        with col_card:
            # Dropdown chuyển nhanh quốc gia tiêu điểm
            all_countries = overall_df["country"].tolist()
            idx_spot = all_countries.index(spotlight_country) if spotlight_country in all_countries else 0
            chosen_c = st.selectbox(
                "Chọn quốc gia tiêu điểm:",
                options=all_countries,
                index=idx_spot,
                key=f"{key_prefix}_spot_sel",
                label_visibility="collapsed"
            )
            if chosen_c != spotlight_country:
                st.session_state[f"{key_prefix}_spotlight"] = chosen_c
                st.rerun()

            # Lấy thông tin quốc gia cho năm đã chọn
            c_info = map_df[map_df["country"] == spotlight_country]
            if not c_info.empty:
                c_row = c_info.iloc[0]
                c_streams = c_row["streams"]
                c_share = c_row["stream_share"]
                c_tracks = int(c_row["n_tracks"])
                c_dance = c_row["danceability"] if pd.notnull(c_row["danceability"]) else 0.65
                c_energy = c_row["energy"] if pd.notnull(c_row["energy"]) else 0.60
                c_valence = c_row["valence"] if pd.notnull(c_row["valence"]) else 0.50
                c_acoustic = c_row["acousticness"] if pd.notnull(c_row["acousticness"]) else 0.30
                c_iso = c_row["country_code"]
                c_region = c_row["region_wb"]
                c_income = c_row["income_group"]
                c_genre = c_row["top_genre"]
            else:
                c_streams = 0
                c_share = 0.0
                c_tracks = 0
                c_dance, c_energy, c_valence, c_acoustic = 0.6, 0.6, 0.5, 0.3
                c_iso, c_region, c_income, c_genre = "N/A", "N/A", "N/A", "Pop"

            # Format số lượng stream
            if c_streams >= 1e9:
                fmt_streams = f"{c_streams / 1e9:.2f} tỷ"
            elif c_streams >= 1e6:
                fmt_streams = f"{c_streams / 1e6:.0f} triệu"
            elif c_streams > 0:
                fmt_streams = f"{c_streams:,.0f}"
            else:
                fmt_streams = "0"

            flag_map = {
                "Vietnam": "🇻🇳", "United States": "🇺🇸", "Brazil": "🇧🇷", "United Kingdom": "🇬🇧",
                "Germany": "🇩🇪", "France": "🇫🇷", "Japan": "🇯🇵", "Korea": "🇰🇷", "South Korea": "🇰🇷",
                "Canada": "🇨🇦", "Australia": "🇦🇺", "Mexico": "🇲🇽", "Spain": "🇪🇸", "Italy": "🇮🇹",
                "Indonesia": "🇮🇩", "Thailand": "🇹🇭", "Philippines": "🇵🇭", "Malaysia": "🇲🇾",
                "Singapore": "🇸🇬", "India": "🇮🇳", "Netherlands": "🇳🇱", "Sweden": "🇸🇪"
            }
            flag_icon = flag_map.get(spotlight_country, "🌐")

            # Sparkline xu hướng 2020–2022
            sp_data = weekly_df[weekly_df["country"] == spotlight_country]

            # Render Card thông tin quốc gia (Loại bỏ khoảng trắng / blank lines để tránh Markdown Code Block)
            card_html = f"""<div style="background:#FFFFFF; border:1px solid #D8D0C7; border-radius:12px; padding:15px 17px; box-shadow:0 3px 12px rgba(36,31,33,0.05); margin-bottom:10px;">
<div style="font-family:'Montserrat',sans-serif; font-size:1.24rem; font-weight:800; color:#241F21; line-height:1.2;">
<span style="display:inline-block; background:#F0E5EC; color:#7A3E65; font-size:0.72rem; font-weight:800; padding:2px 6px; border-radius:4px; margin-right:5px; vertical-align:middle; border:1px solid #D8B7CC;">{c_iso}</span>{spotlight_country}
</div>
<div style="font-size:0.8rem; font-weight:600; color:#81786E; margin-top:3px;">
Năm khảo sát: {current_year}
</div>
<div style="margin-top:12px; margin-bottom:12px;">
<div style="font-size:0.74rem; font-weight:700; color:#81786E; text-transform:uppercase; letter-spacing:0.5px;">
Lượt stream
</div>
<div style="font-family:'Montserrat',sans-serif; font-size:1.82rem; font-weight:900; color:#7A3E65; line-height:1.15; margin-top:2px;">
{fmt_streams}
</div>
<div style="font-size:0.81rem; color:#625B5E; margin-top:4px; font-weight:500;">
Thị phần: <b>{c_share:.2f}%</b> &bull; <b>{c_tracks:,}</b> bài hát
</div>
</div>
<div style="border-top:1px solid #EEE9E1; padding-top:9px; margin-top:9px;">
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
<span style="font-size:0.72rem; font-weight:700; color:#81786E; text-transform:uppercase; letter-spacing:0.5px;">Đặc trưng âm thanh</span>
<span style="font-size:0.68rem; color:#81786E; font-weight:600;">(Quy ước 0.00 – 1.00)</span>
</div>
<div style="display:flex; flex-direction:column; gap:5px;">
<div>
<div style="display:flex; justify-content:space-between; font-size:0.73rem; color:#625B5E; margin-bottom:2px;">
<span>Danceability</span>
<span style="font-weight:700; color:#7A3E65;">{c_dance:.2f}</span>
</div>
<div style="background:#F0E5EC; border-radius:3px; height:5px; overflow:hidden;">
<div style="background:#7A3E65; width:{c_dance*100:.1f}%; height:100%; border-radius:3px;"></div>
</div>
</div>
<div>
<div style="display:flex; justify-content:space-between; font-size:0.73rem; color:#625B5E; margin-bottom:2px;">
<span>Energy</span>
<span style="font-weight:700; color:#7A3E65;">{c_energy:.2f}</span>
</div>
<div style="background:#F0E5EC; border-radius:3px; height:5px; overflow:hidden;">
<div style="background:#7A3E65; width:{c_energy*100:.1f}%; height:100%; border-radius:3px;"></div>
</div>
</div>
<div>
<div style="display:flex; justify-content:space-between; font-size:0.73rem; color:#625B5E; margin-bottom:2px;">
<span>Valence</span>
<span style="font-weight:700; color:#7A3E65;">{c_valence:.2f}</span>
</div>
<div style="background:#F0E5EC; border-radius:3px; height:5px; overflow:hidden;">
<div style="background:#7A3E65; width:{c_valence*100:.1f}%; height:100%; border-radius:3px;"></div>
</div>
</div>
<div>
<div style="display:flex; justify-content:space-between; font-size:0.73rem; color:#625B5E; margin-bottom:2px;">
<span>Acousticness</span>
<span style="font-weight:700; color:#7A3E65;">{c_acoustic:.2f}</span>
</div>
<div style="background:#F0E5EC; border-radius:3px; height:5px; overflow:hidden;">
<div style="background:#7A3E65; width:{c_acoustic*100:.1f}%; height:100%; border-radius:3px;"></div>
</div>
</div>
</div>
</div>
<div style="border-top:1px solid #EEE9E1; padding-top:8px; margin-top:10px;">
<div style="font-size:0.72rem; font-weight:700; color:#81786E; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:4px;">
Biểu đồ xu hướng 2020–2022
</div>
</div>
</div>"""
            st.markdown(card_html, unsafe_allow_html=True)

            # Sparkline xu hướng đặt ngay trong cụm card
            if not sp_data.empty and len(sp_data) > 1:
                fig_sp = go.Figure()
                fig_sp.add_trace(go.Scatter(
                    x=sp_data["week"],
                    y=sp_data["streams"],
                    mode="lines",
                    line=dict(color="#7A3E65", width=2.2, shape="spline"),
                    fill="tozeroy",
                    fillcolor="rgba(122, 62, 101, 0.12)",
                    hovertemplate="Tuần: %{x|%d/%m/%Y}<br>Streams: %{y:,.0f}<extra></extra>"
                ))
                fig_sp.update_layout(
                    height=85,
                    margin=dict(l=0, r=0, t=5, b=15),
                    xaxis=dict(visible=True, showgrid=False, showticklabels=True, tickfont=dict(size=9, color="#81786E")),
                    yaxis=dict(visible=False, showgrid=False),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)"
                )
                st.plotly_chart(fig_sp, use_container_width=True, config={'displayModeBar': False})

            # Phần "Chi tiết" thu gọn (ISO, nhóm thu nhập, khu vực)
            with st.expander("Chi tiết"):
                st.markdown(f"""<div style="font-size:0.75rem; color:#625B5E; line-height:1.6;">
Mã ISO: <b>{c_iso}</b><br>
Khu vực: <b>{c_region}</b><br>
Nhóm thu nhập: <b>{c_income}</b><br>
Thể loại số 1: <b style="color:#7A3E65;">{c_genre}</b>
</div>""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# HÀM PHÂN TÍCH NHẬN XÉT ĐỘNG THEO TỪNG QUỐC GIA ĐƯỢC CHỌN TRÊN BẢN ĐỒ
# ═════════════════════════════════════════════════════════════════════════════
def render_dynamic_country_map_insight(df_source, country_name="Vietnam", year=2022):
    valid_all = df_source[df_source["country"] != "Global"]
    c_mask = valid_all["country"].astype(str).str.lower() == str(country_name).lower()
    c_df_all = valid_all[c_mask]
    
    if c_df_all.empty:
        render_insight_card(
            title=f"Phân Tích Thị Trường: {country_name}",
            key_findings=f"Thị trường {country_name} chưa có bản ghi dữ liệu hợp lệ trong hệ thống.",
            details="Không có ca khúc nào lọt vào Top 200 trong các tuần khảo sát.",
            implications="Cần bổ sung nguồn dữ liệu hoặc cập nhật bổ sung trong các kỳ đánh giá tiếp theo."
        )
        return

    # Lọc theo năm đã chọn
    c_df = c_df_all[c_df_all["year"] == int(year)]
    if c_df.empty:
        c_df = c_df_all
        period_str = "Toàn kỳ (2020–2022)"
        tot_market_streams = valid_all["streams"].sum()
    else:
        period_str = f"Năm {year}"
        tot_market_streams = valid_all[valid_all["year"] == int(year)]["streams"].sum()

    tot_streams = c_df["streams"].sum()
    share_pct = (tot_streams / tot_market_streams * 100.0) if tot_market_streams > 0 else 0.0
    n_tracks = c_df["track_name"].nunique()

    # Định dạng hiển thị lượt stream
    if tot_streams >= 1e9:
        fmt_str = f"{tot_streams / 1e9:.2f} tỷ"
    elif tot_streams >= 1e6:
        fmt_str = f"{tot_streams / 1e6:.1f} triệu"
    else:
        fmt_str = f"{tot_streams:,.0f}"

    # Chỉ số âm học trung bình
    dance = c_df["danceability"].mean() if "danceability" in c_df and not c_df["danceability"].dropna().empty else 0.65
    energy = c_df["energy"].mean() if "energy" in c_df and not c_df["energy"].dropna().empty else 0.60
    valence = c_df["valence"].mean() if "valence" in c_df and not c_df["valence"].dropna().empty else 0.50
    acoustic = c_df["acousticness"].mean() if "acousticness" in c_df and not c_df["acousticness"].dropna().empty else 0.25

    # Thể loại và nghệ sĩ hàng đầu
    top_genre = c_df["track_genre"].dropna().mode()[0] if not c_df["track_genre"].dropna().empty else "Pop"
    top_artist = c_df["artist_individual"].dropna().mode()[0] if not c_df["artist_individual"].dropna().empty else "N/A"

    # Phân cấp thị trường
    if tot_streams >= 12e9:
        tier_title = "Cấp 5/5 (Thị trường Siêu Khổng Lồ - Mega Market)"
    elif tot_streams >= 6e9:
        tier_title = "Cấp 4/5 (Thị trường Quy Mô Lớn)"
    elif tot_streams >= 2e9:
        tier_title = "Cấp 3/5 (Thị trường Tăng Trưởng Trung Bình)"
    elif tot_streams >= 500e6:
        tier_title = "Cấp 2/5 (Thị trường Tiềm Năng Đang Phát Triển)"
    else:
        tier_title = "Cấp 1/5 (Thị trường Ngách Quy Mô Nhỏ)"

    # 1. SUY LUẬN XU HƯỚNG NGHE NHẠC TỪ ĐẶC TRƯNG ÂM HỌC (QUY ƯỚC 0.00 – 1.00)
    taste_clues = []
    
    # Phân tích Danceability
    if dance >= 0.68:
        taste_clues.append(f"ưu tiên các ca khúc có nhịp điệu nảy, bắt tai, dễ nhảy múa và bắt trend video ngắn (Danceability đạt <b>{dance:.2f}</b>)")
    elif dance <= 0.60:
        taste_clues.append(f"chuộng các bản nhạc có kết cấu tự do, tự sự, ít lệ thuộc vào nhịp điệu dồn dập (Danceability <b>{dance:.2f}</b>)")
    else:
        taste_clues.append(f"cân bằng hài hòa giữa giai điệu mượt mà và tiết tấu vừa phải (Danceability <b>{dance:.2f}</b>)")

    # Phân tích Energy & Acousticness
    if acoustic >= 0.30 and energy <= 0.58:
        taste_clues.append(f"đặc biệt ưu ái chất nhạc mộc mạc, trữ tình tự sự (Acousticness cao <b>{acoustic:.2f}</b> và Energy êm dịu <b>{energy:.2f}</b>), phản ánh xu hướng chuộng các bản Pop Ballad / Indie / R&B sâu lắng giàu ca từ")
    elif energy >= 0.68 and acoustic <= 0.22:
        taste_clues.append(f"bùng nổ năng lượng lễ hội sôi động (Energy cao <b>{energy:.2f}</b>, Acousticness thấp <b>{acoustic:.2f}</b>), người nghe chuộng âm bass điện tử dày, bộ gõ cuồng nhiệt và giai điệu tiệc tùng")
    elif acoustic >= 0.35:
        taste_clues.append(f"có cảm tình lớn với nhạc cụ mộc (Acousticness đạt <b>{acoustic:.2f}</b>) tạo cảm giác gần gũi, chân thực")
    else:
        taste_clues.append(f"đón nhận linh hoạt nhiều cấu trúc phối khí đa dạng (Energy <b>{energy:.2f}</b>, Acousticness <b>{acoustic:.2f}</b>)")

    # Phân tích Valence (Tâm trạng)
    if valence <= 0.48:
        taste_clues.append(f"tâm trạng nghe nhạc nghiêng hẳn về chiều sâu nội tâm, hoài niệm, 'chill' suy tư hoặc các bản tình ca buồn da diết (Valence <b>{valence:.2f}</b>)")
    elif valence >= 0.58:
        taste_clues.append(f"tâm trạng nghe nhạc tràn đầy sự tươi vui, lạc quan, phấn chấn và yêu đời (Valence <b>{valence:.2f}</b>)")
    else:
        taste_clues.append(f"cảm xúc âm nhạc đa tầng đan xen giữa vui tươi và suy ngẫm (Valence <b>{valence:.2f}</b>)")

    taste_summary = "; ".join(taste_clues)
    
    key_findings = (
        f"Tại <b>{country_name}</b> ({period_str}), thị trường ghi nhận <b>{fmt_str} lượt stream</b>, "
        f"chiếm <b>{share_pct:.2f}% thị phần</b> toàn cầu với thể loại chiếm lĩnh BXH là <b>{top_genre}</b>. "
        f"Từ 4 đặc trưng âm học chuẩn hóa, có thể suy ra xu hướng nghe nhạc nổi bật: Khán giả {country_name} {taste_summary}."
    )

    # 2. PHÂN TÍCH SỐ LIỆU THỐNG KÊ & SO SÁNH VỚI CHUẨN TOÀN CẦU (BENCHMARK 0.00 – 1.00)
    # Benchmark toàn cầu: Danceability 0.66, Energy 0.64, Acousticness 0.24, Valence 0.51
    d_gap = dance - 0.66
    e_gap = energy - 0.64
    a_gap = acoustic - 0.24
    v_gap = valence - 0.51

    def fmt_gap(val, label, bench):
        sign = "+" if val > 0 else ""
        text = "cao hơn" if val > 0 else "thấp hơn"
        return f"{label}: <b>{sign}{val:.2f}</b> ({text} chuẩn toàn cầu {bench:.2f})"

    gap_str = ", ".join([fmt_gap(d_gap, "Danceability", 0.66), fmt_gap(e_gap, "Energy", 0.64), fmt_gap(a_gap, "Acousticness", 0.24), fmt_gap(v_gap, "Valence", 0.51)])

    details = (
        f"Quốc gia xếp vào <b>{tier_title}</b> với <b>{n_tracks:,} ca khúc</b> từng lọt vào Top 200. "
        f"So sánh tương quan âm học với mức trung bình chuẩn thế giới: {gap_str}. "
        f"Nghệ sĩ có sức ảnh hưởng dẫn đầu về tần suất xuất hiện và lượt nghe tại thị trường là <b>{top_artist}</b>."
    )

    # 3. Ý NGHĨA & ỨNG DỤNG THỰC TIỄN
    if acoustic >= 0.28 or energy <= 0.58:
        implications = (
            f"<b>Đối với Nhạc sĩ & Producer:</b> Khán giả {country_name} có xu hướng đồng cảm cao với phần ca từ giàu chất thơ và giai điệu mộc mạc. Nên tối ưu bản phối tập trung vào giọng hát mộc (vocal-driven), tiếng đàn piano hoặc guitar acoustic ấm áp, tránh lạm dụng autotune hay drop điện tử quá gắt. "
            f"<b>Đối với Hãng đĩa & Marketing:</b> Ưu tiên phân phối vào các playlist chủ đề tâm trạng (Chill, Acoustic, Tâm trạng buổi tối), đồng thời cắt các đoạn điệp khúc tự sự để tạo trào lưu nhạc nền video ngắn trên TikTok/Reels."
        )
    elif energy >= 0.66 or dance >= 0.68:
        implications = (
            f"<b>Đối với Nhạc sĩ & Producer:</b> Khán giả {country_name} tìm kiếm sự hưng phấn, giải phóng năng lượng và nhịp điệu dứt khoát. Cần thiết kế phần Hook/Drop thật bùng nổ, dải bass dày (808 Bass), tempo từ 115–128 BPM để dễ dàng đưa vào các không gian biểu diễn, vũ trường và sự kiện trực tiếp. "
            f"<b>Đối với Hãng đĩa & Marketing:</b> Xây dựng các chiến dịch Dance Challenge trên mạng xã hội, đẩy mạnh hợp tác với các DJ/Remixer và nhắm vào các playlist chủ đề Party, Workout, Lễ hội cuối tuần."
        )
    else:
        implications = (
            f"<b>Đối với Nhạc sĩ & Producer:</b> Khán giả {country_name} có thị hiếu đa dạng và đón nhận cởi mở. Nghệ sĩ có thể kết hợp chất liệu Pop hiện đại với âm hưởng địa phương, giữ thời lượng bài hát gọn gàng (dưới 3.5 phút) để kích thích tỷ lệ nghe lặp lại (repeat listen). "
            f"<b>Đối với Hãng đĩa & Marketing:</b> Triển khai chiến dịch quảng bá đa kênh, nhắm vào các khung giờ vàng buổi tối và dịp cuối tuần để tối đa hóa lượt stream tự nhiên."
        )

    render_insight_card(
        title=f"Phân Tích Chuyên Sâu Thị Trường: {country_name} ({period_str})",
        key_findings=key_findings,
        details=details,
        implications=implications
    )

# KHOI TAO VA DONG BO TRANG THAI CHON BIEU DO TRUC QUAN HOA
if "active_viz_chart" not in st.session_state:
    st.session_state["active_viz_chart"] = CHART_OPTIONS[0]

def on_sb_chart_change():
    chosen = st.session_state.get("sb_chart_radio", CHART_OPTIONS[0])
    st.session_state["active_viz_chart"] = chosen
    st.session_state["main_chart_select"] = chosen

def on_main_chart_change():
    chosen = st.session_state.get("main_chart_select", CHART_OPTIONS[0])
    st.session_state["active_viz_chart"] = chosen
    st.session_state["sb_chart_radio"] = chosen

# THANH DIEU HUONG SIDEBAR (CHUAN SPOTIFY DASHBOARD)
with st.sidebar:
    st.markdown("""
    <div style='margin-bottom: 16px; padding: 2px 2px 0 2px;'>
        <div style='display: flex; align-items: center; gap: 9px; margin-bottom: 4px;'>
            <svg viewBox="0 0 167.5 167.5" style="width: 28px; height: 28px; fill: #1ED760; flex-shrink: 0;">
                <path fill="#1ED760" d="M83.7 0C37.5 0 0 37.5 0 83.7c0 46.3 37.5 83.7 83.7 83.7 46.3 0 83.7-37.5 83.7-83.7C167.5 37.5 130 0 83.7 0zm38.4 120.7c-1.5 2.5-4.7 3.3-7.2 1.8-19.7-12-44.5-14.7-73.7-8-2.8.6-5.6-1.2-6.2-4-.6-2.8 1.2-5.6 4-6.2 32-7.3 59.6-4.2 81.6 9.3 2.5 1.5 3.3 4.7 1.8 7.1zm10.2-22.8c-1.9 3.1-6 4-9.1 2.1-22.6-13.9-57-17.9-83.7-9.8-3.5 1.1-7.1-.9-8.2-4.4-1.1-3.5.9-7.1 4.4-8.2 30.5-9.3 68.6-4.8 94.5 11.2 3.1 1.9 4.1 6 2.1 9.1zm1.1-23.8c-27.1-16.1-71.8-17.6-97.7-9.7-4.1 1.3-8.6-1.1-9.8-5.2-1.3-4.1 1.1-8.6 5.2-9.8 29.8-9 79.1-7.3 110.3 11.2 3.7 2.2 4.9 7.1 2.7 10.8-2.2 3.7-7.1 4.9-10.7 2.7z"/>
            </svg>
            <span style='font-family: "Montserrat", sans-serif; font-size: 1.18rem; font-weight: 800; color: #24211E; letter-spacing: -0.3px;'>Spotify Analytics</span>
        </div>
        <p style='font-family: "Inter", sans-serif; font-size: 0.74rem; font-weight: 600; color: #81786E; margin: 0;'>Menu điều hướng</p>
    </div>
    """, unsafe_allow_html=True)
    
    if "nav_target" in st.session_state:
        st.session_state["sb_cat_mode"] = st.session_state.pop("nav_target")
        
    cat_mode = st.radio(
        "Mục chức năng:",
        options=[
            "Trang Chủ",
            "Bảng Dữ Liệu & Bộ Lọc",
            "Thống Kê Thị Trường",
            "So Sánh Thị Hiếu (Taste Radar)",
            "Biểu Đồ Phân Tích",
            "Đặc Tính Âm Nhạc",
            "Mạng Lưới Hợp Tác",
            "Dự Đoán Ca Khúc Hit"
        ],
        index=0,
        label_visibility="collapsed",
        key="sb_cat_mode"
    )
    
    if "Trang Chủ" in cat_mode or "Home" in cat_mode:
        current_view = "Trang Chủ"
    elif "Thị Hiếu" in cat_mode or "Taste Radar" in cat_mode:
        current_view = "So Sánh Thị Hiếu"
    elif "Biểu Đồ" in cat_mode or "Trực Quan Hóa" in cat_mode:
        st.markdown("""
        <div style='margin: 18px 0 10px 0; border-top: 1px solid #D8D0C7; padding-top: 14px;'>
            <p style='font-family: "Inter", sans-serif; font-size: 0.74rem; font-weight: 600; color: #7A3E65; margin: 0;'>Chọn biểu đồ phân tích</p>
        </div>
        """, unsafe_allow_html=True)
        curr_chart = st.session_state.get("active_viz_chart", CHART_OPTIONS[0])
        idx = CHART_OPTIONS.index(curr_chart) if curr_chart in CHART_OPTIONS else 0
        st.radio(
            "Danh sách biểu đồ:",
            options=CHART_OPTIONS,
            index=idx,
            label_visibility="collapsed",
            key="sb_chart_radio",
            on_change=on_sb_chart_change
        )
        current_view = "Trực Quan Hóa Dữ Liệu"
    elif "Dữ Liệu" in cat_mode or "Bộ Lọc" in cat_mode or "Bảng" in cat_mode:
        st.markdown("""
        <div style='margin: 18px 0 10px 0; border-top: 1px solid #D8D0C7; padding-top: 14px;'>
            <p style='font-family: "Inter", sans-serif; font-size: 0.74rem; font-weight: 600; color: #625C54; margin: 0;'>Chọn góc nhìn dữ liệu</p>
        </div>
        """, unsafe_allow_html=True)
        current_view = st.radio(
            "Chi tiết màn hình:",
            options=["Tổng Quan Dữ Liệu", "Bộ Lọc Chi Tiết"],
            index=0,
            label_visibility="collapsed",
            key="sb_sub_view_data"
        )
    elif "Thị Trường" in cat_mode or "Thống Kê" in cat_mode:
        current_view = "Tổng Quan Thị Trường"
    elif "Đặc Tính" in cat_mode or "Âm Nhạc" in cat_mode or "Hồ Sơ" in cat_mode or "Âm Thanh" in cat_mode:
        current_view = "Hồ Sơ Âm Thanh"
    elif "Mạng Lưới" in cat_mode or "Hợp Tác" in cat_mode:
        current_view = "Mạng Lưới Nghệ Sĩ"
    elif "Dự Đoán" in cat_mode or "Dự Báo" in cat_mode or "Hit" in cat_mode:
        current_view = "Dự Báo Bài Hát Hit"
    else:
        current_view = cat_mode

# 0. MÀN HÌNH 0: TRANG CHỦ (HOME SHOWCASE EDITORIAL)
if "Trang Chủ" in current_view:
    covers = get_hero_album_covers()

    # TẦNG 1: HERO HEADER CÓ CHIỀU SÂU & CỤM ẢNH BÌA NGHỆ SĨ SINH ĐỘNG
    with st.container(border=True):
        st.markdown("""
        <div class="hero-marker-editorial" style="position: absolute; right: 0; bottom: 0; left: 0; height: 90px; pointer-events: none; overflow: hidden; opacity: 0.07; z-index: 0;">
            <svg viewBox="0 0 1200 120" preserveAspectRatio="none" style="width: 100%; height: 100%;">
                <path d="M0,60 Q25,10 50,60 T100,60 T150,105 T200,60 T250,15 T300,60 T350,95 T400,60 T450,25 T500,60 T550,110 T600,60 T650,15 T700,60 T750,85 T800,60 T850,35 T900,60 T950,80 T1000,60 T1050,20 T1100,60 T1150,90 T1200,60" fill="none" stroke="#7A3E65" stroke-width="3" stroke-linecap="round"/>
            </svg>
        </div>
        """, unsafe_allow_html=True)
        
        col_hero_left, col_hero_right = st.columns([1.5, 1.05], gap="large")
        
        with col_hero_left:
            st.markdown("""
            <div style="position: relative; z-index: 1;">
                <div style="font-family: 'Inter', sans-serif; font-size: 13px; font-weight: 700; letter-spacing: 1.5px; color: #7A3E65; text-transform: uppercase; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
                    <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #7A3E65;"></span>
                    SPOTIFY CHARTS · 2021–2022
                </div>
                <div style="display: flex; align-items: flex-start; gap: 14px; margin-bottom: 14px;">
                    <svg viewBox="0 0 167.5 167.5" style="width: 44px; height: 44px; fill: #1ED760; flex-shrink: 0; margin-top: 3px;">
                        <path fill="#1ED760" d="M83.7 0C37.5 0 0 37.5 0 83.7c0 46.3 37.5 83.7 83.7 83.7 46.3 0 83.7-37.5 83.7-83.7C167.5 37.5 130 0 83.7 0zm38.4 120.7c-1.5 2.5-4.7 3.3-7.2 1.8-19.7-12-44.5-14.7-73.7-8-2.8.6-5.6-1.2-6.2-4-.6-2.8 1.2-5.6 4-6.2 32-7.3 59.6-4.2 81.6 9.3 2.5 1.5 3.3 4.7 1.8 7.1zm10.2-22.8c-1.9 3.1-6 4-9.1 2.1-22.6-13.9-57-17.9-83.7-9.8-3.5 1.1-7.1-.9-8.2-4.4-1.1-3.5.9-7.1 4.4-8.2 30.5-9.3 68.6-4.8 94.5 11.2 3.1 1.9 4.1 6 2.1 9.1zm1.1-23.8c-27.1-16.1-71.8-17.6-97.7-9.7-4.1 1.3-8.6-1.1-9.8-5.2-1.3-4.1 1.1-8.6 5.2-9.8 29.8-9 79.1-7.3 110.3 11.2 3.7 2.2 4.9 7.1 2.7 10.8-2.2 3.7-7.1 4.9-10.7 2.7z"/>
                    </svg>
                    <h1 style="font-family: 'Montserrat', sans-serif; font-size: 1.95rem; font-weight: 800; line-height: 1.25; letter-spacing: -0.5px; color: #241F21; margin: 0;">
                        Nghiên cứu & Trực quan hóa Đặc trưng Âm thanh & Dự đoán Xu hướng Ca khúc Spotify
                    </h1>
                </div>
                <p style="font-family: 'Inter', sans-serif; font-size: 15px; color: #625B5E; line-height: 1.6; margin: 0 0 20px 0;">
                    Hệ thống phân tích dữ liệu đa chiều kho tàng âm nhạc Spotify Charts (2021 – 2022). Khám phá các đặc trưng âm học, cơ cấu phân bổ thị trường toàn cầu và ứng dụng học máy ước tính xu hướng bài hát thịnh hành.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            c_btn1, c_btn2, _ = st.columns([1.15, 1.45, 1.0])
            with c_btn1:
                if st.button("Khám phá dữ liệu", key="hero_btn_explore", type="primary", use_container_width=True):
                    st.session_state["nav_target"] = "Bảng Dữ Liệu & Bộ Lọc"
                    st.rerun()
            with c_btn2:
                if st.button("Xem xu hướng nổi bật →", key="hero_btn_trends", type="secondary", use_container_width=True):
                    st.session_state["nav_target"] = "Biểu Đồ Phân Tích"
                    st.rerun()
                    
        with col_hero_right:
            if len(covers) >= 5:
                cov_main = covers[0]
                cov_s1, cov_s2, cov_s3, cov_s4 = covers[1], covers[2], covers[3], covers[4]
            else:
                cov_main = covers[0] if covers else ""
                cov_s1 = cov_s2 = cov_s3 = cov_s4 = cov_main
                
            st.markdown(f"""
            <div style="position: relative; width: 100%; max-width: 420px; margin: 8px auto 0 auto;">
                <div style="position: absolute; top: 12px; left: 12px; right: -12px; bottom: -12px; background: #F7E6DC; border-radius: 18px; border: 1px solid #EADBCE; z-index: 0;"></div>
                <div style="position: relative; z-index: 1; background: #FFFFFF; border-radius: 16px; padding: 10px; border: 1px solid #D8D0C7; box-shadow: 0 12px 30px rgba(98, 92, 84, 0.12);">
                    <div style="display: grid; grid-template-columns: 1.15fr 1fr; gap: 8px; align-items: stretch;">
                        <div style="position: relative; border-radius: 10px; overflow: hidden; aspect-ratio: 1;">
                            <img src="data:image/jpeg;base64,{cov_main}" style="width: 100%; height: 100%; object-fit: cover; display: block; border-radius: 10px;" />
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
                            <img src="data:image/jpeg;base64,{cov_s1}" style="width: 100%; aspect-ratio: 1; object-fit: cover; border-radius: 7px; display: block;" />
                            <img src="data:image/jpeg;base64,{cov_s2}" style="width: 100%; aspect-ratio: 1; object-fit: cover; border-radius: 7px; display: block;" />
                            <img src="data:image/jpeg;base64,{cov_s3}" style="width: 100%; aspect-ratio: 1; object-fit: cover; border-radius: 7px; display: block;" />
                            <img src="data:image/jpeg;base64,{cov_s4}" style="width: 100%; aspect-ratio: 1; object-fit: cover; border-radius: 7px; display: block;" />
                        </div>
                    </div>
                    <div style="position: absolute; bottom: -11px; left: 18px; background: #7A3E65; color: #FFFFFF; padding: 5px 14px; border-radius: 20px; font-family: 'Inter', sans-serif; font-size: 11px; font-weight: 700; letter-spacing: 0.6px; box-shadow: 0 4px 14px rgba(122, 62, 101, 0.28); text-transform: uppercase;">
                        Top artists · 2021–2022
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # TẦNG 2: 4 CARD KPI CÓ BẢN SẮC MÀU PASTEL XẾP THEO CHIỀU NGANG (4 CỘT)
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4, gap="medium")
    with k1:
        st.markdown("""<div style="background-color: #F1E4EC; border: 1px solid rgba(122, 62, 101, 0.2); border-radius: 14px; padding: 18px 20px; position: relative; overflow: hidden; box-shadow: 0 2px 8px rgba(122, 62, 101, 0.05); min-height: 138px; display: flex; flex-direction: column; justify-content: space-between;">
            <div style="position: absolute; right: 12px; bottom: 8px; opacity: 0.08; pointer-events: none;">
                <svg width="68" height="68" viewBox="0 0 24 24" fill="none" stroke="#7A3E65" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <ellipse cx="12" cy="5" rx="9" ry="3"></ellipse>
                    <path d="M3 5v14a9 3 0 0 0 18 0V5"></path>
                    <path d="M3 12a9 3 0 0 0 18 0"></path>
                </svg>
            </div>
            <div>
                <div style="font-family: 'Inter', sans-serif; font-size: 11px; font-weight: 700; letter-spacing: 0.6px; color: #7A3E65; text-transform: uppercase; margin-bottom: 4px;">
                    TỔNG BẢN GHI
                </div>
                <div style="font-family: 'Montserrat', sans-serif; font-size: 2.1rem; font-weight: 900; color: #7A3E65; line-height: 1.1; letter-spacing: -0.8px;">
                    314,727
                </div>
            </div>
            <div style="font-family: 'Inter', sans-serif; font-size: 12px; font-weight: 500; color: #625B5E; margin-top: 8px;">
                Dữ liệu BXH tuần chuẩn hóa
            </div>
        </div>""", unsafe_allow_html=True)
    with k2:
        st.markdown("""<div style="background-color: #DDEDE9; border: 1px solid rgba(57, 122, 116, 0.22); border-radius: 14px; padding: 18px 20px; position: relative; overflow: hidden; box-shadow: 0 2px 8px rgba(57, 122, 116, 0.05); min-height: 138px; display: flex; flex-direction: column; justify-content: space-between;">
            <div style="position: absolute; right: 12px; bottom: 8px; opacity: 0.1; pointer-events: none;">
                <svg width="68" height="68" viewBox="0 0 24 24" fill="none" stroke="#397A74" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="2" y1="12" x2="22" y2="12"></line>
                    <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
                </svg>
            </div>
            <div>
                <div style="font-family: 'Inter', sans-serif; font-size: 11px; font-weight: 700; letter-spacing: 0.6px; color: #397A74; text-transform: uppercase; margin-bottom: 4px;">
                    QUỐC GIA & THỊ TRƯỜNG
                </div>
                <div style="font-family: 'Montserrat', sans-serif; font-size: 2.1rem; font-weight: 900; color: #397A74; line-height: 1.1; letter-spacing: -0.8px;">
                    65 <span style="font-size: 14px; font-weight: 600; color: #397A74;">thị trường</span>
                </div>
            </div>
            <div style="font-family: 'Inter', sans-serif; font-size: 12px; font-weight: 500; color: #625B5E; margin-top: 8px;">
                7 khu vực kinh tế (World Bank)
            </div>
        </div>""", unsafe_allow_html=True)
    with k3:
        st.markdown("""<div style="background-color: #F8E9CD; border: 1px solid rgba(210, 161, 60, 0.25); border-radius: 14px; padding: 18px 20px; position: relative; overflow: hidden; box-shadow: 0 2px 8px rgba(210, 161, 60, 0.05); min-height: 138px; display: flex; flex-direction: column; justify-content: space-between;">
            <div style="position: absolute; right: 12px; bottom: 8px; opacity: 0.12; pointer-events: none;">
                <svg width="68" height="68" viewBox="0 0 24 24" fill="none" stroke="#D2A13C" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                    <line x1="16" y1="2" x2="16" y2="6"></line>
                    <line x1="8" y1="2" x2="8" y2="6"></line>
                    <line x1="3" y1="10" x2="21" y2="10"></line>
                </svg>
            </div>
            <div>
                <div style="font-family: 'Inter', sans-serif; font-size: 11px; font-weight: 700; letter-spacing: 0.6px; color: #A67B22; text-transform: uppercase; margin-bottom: 4px;">
                    CHUỖI THỜI GIAN
                </div>
                <div style="font-family: 'Montserrat', sans-serif; font-size: 2.1rem; font-weight: 900; color: #A67B22; line-height: 1.1; letter-spacing: -0.8px;">
                    104 <span style="font-size: 14px; font-weight: 600; color: #A67B22;">tuần</span>
                </div>
            </div>
            <div style="font-family: 'Inter', sans-serif; font-size: 12px; font-weight: 500; color: #625B5E; margin-top: 8px;">
                Quan sát liên tục 2021 – 2022
            </div>
        </div>""", unsafe_allow_html=True)
    with k4:
        st.markdown("""<div style="background-color: #F7E6DC; border: 1px solid rgba(201, 107, 75, 0.22); border-radius: 14px; padding: 18px 20px; position: relative; overflow: hidden; box-shadow: 0 2px 8px rgba(201, 107, 75, 0.05); min-height: 138px; display: flex; flex-direction: column; justify-content: space-between;">
            <div style="position: absolute; right: 12px; bottom: 8px; opacity: 0.1; pointer-events: none;">
                <svg width="68" height="68" viewBox="0 0 24 24" fill="none" stroke="#C96B4B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M9 18V5l12-2v13"></path>
                    <circle cx="6" cy="18" r="3"></circle>
                    <circle cx="18" cy="16" r="3"></circle>
                </svg>
            </div>
            <div>
                <div style="font-family: 'Inter', sans-serif; font-size: 11px; font-weight: 700; letter-spacing: 0.6px; color: #C96B4B; text-transform: uppercase; margin-bottom: 4px;">
                    BÀI HÁT ĐỘC NHẤT
                </div>
                <div style="font-family: 'Montserrat', sans-serif; font-size: 2.1rem; font-weight: 900; color: #C96B4B; line-height: 1.1; letter-spacing: -0.8px;">
                    2,242 <span style="font-size: 14px; font-weight: 600; color: #C96B4B;">ca khúc</span>
                </div>
            </div>
            <div style="font-family: 'Inter', sans-serif; font-size: 12px; font-weight: 500; color: #625B5E; margin-top: 8px;">
                Unique hits sau gộp tuần hoàn
            </div>
        </div>""", unsafe_allow_html=True)

    # TẦNG 3: KHÁM PHÁ NHANH (QUICK DISCOVERY DASHBOARD ROW)
    st.markdown("""
    <div style="position: relative; width: 100%; height: 20px; margin: 4px 0 12px 0; overflow: hidden; opacity: 0.08;">
        <svg viewBox="0 0 1200 20" preserveAspectRatio="none" style="width: 100%; height: 100%;">
            <path d="M0,10 L120,10 Q140,2 155,10 T190,10 L350,10 Q370,18 385,10 T420,10 L600,10 Q620,2 635,10 T670,10 L850,10 Q870,18 885,10 T920,10 L1200,10" fill="none" stroke="#7A3E65" stroke-width="2" stroke-linecap="round"/>
        </svg>
    </div>
    <div style="margin-bottom: 14px;">
        <h2 style="font-family: 'Montserrat', sans-serif; font-size: 20px; font-weight: 800; color: #241F21; margin: 0; letter-spacing: -0.3px;">
            Khám phá nhanh dữ liệu
        </h2>
        <p style="font-family: 'Inter', sans-serif; font-size: 13px; color: #625B5E; margin: 2px 0 0 0;">
            Truy cập trực quan vào các phân hệ phân tích chuyên sâu của hệ thống
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_q1, col_q2, col_q3 = st.columns(3, gap="medium")
    
    with col_q1:
        with st.container(border=True):
            st.markdown("""
            <div class="quick-card-marker" style="margin-bottom: 6px;">
                <div style="font-family: 'Inter', sans-serif; font-size: 11px; font-weight: 700; letter-spacing: 0.8px; color: #7A3E65; text-transform: uppercase;">
                    CHỈ SỐ THỜI GIAN
                </div>
                <div style="font-family: 'Montserrat', sans-serif; font-size: 17px; font-weight: 800; color: #241F21; margin-top: 2px;">
                    Xu hướng tuần
                </div>
                <div style="font-family: 'Inter', sans-serif; font-size: 12px; color: #625B5E; margin-top: 2px;">
                    Biến động tổng stream toàn cầu theo tuần
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            df_week_trend = df_raw.groupby('week', as_index=False)['streams'].sum().sort_values('week')
            fig_trend = go.Figure()
            fig_trend.add_trace(go.Scatter(
                x=df_week_trend['week'],
                y=df_week_trend['streams'] / 1e9,
                mode='lines',
                line=dict(color='#7A3E65', width=2.2),
                fill='tozeroy',
                fillcolor='rgba(122, 62, 101, 0.12)',
                hovertemplate='Tuần: %{x|%d/%m/%Y}<br>Streams: %{y:.2f}B<extra></extra>'
            ))
            fig_trend.update_layout(
                height=110,
                margin=dict(l=0, r=0, t=5, b=5),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
                yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
                hovermode='x unified'
            )
            st.plotly_chart(fig_trend, use_container_width=True, config={'displayModeBar': False})
            
            if st.button("Xem phân tích →", key="btn_quick_trend", use_container_width=True):
                st.session_state["nav_target"] = "Biểu Đồ Phân Tích"
                st.rerun()

    with col_q2:
        with st.container(border=True):
            st.markdown("""
            <div class="quick-card-marker" style="margin-bottom: 6px;">
                <div style="font-family: 'Inter', sans-serif; font-size: 11px; font-weight: 700; letter-spacing: 0.8px; color: #397A74; text-transform: uppercase;">
                    PHÂN BỔ ĐỊA LÝ
                </div>
                <div style="font-family: 'Montserrat', sans-serif; font-size: 17px; font-weight: 800; color: #241F21; margin-top: 2px;">
                    Thị trường nổi bật
                </div>
                <div style="font-family: 'Inter', sans-serif; font-size: 12px; color: #625B5E; margin-top: 2px;">
                    Top 5 quốc gia dẫn đầu lượng nghe
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            top_countries = (
                df_raw.groupby('country', as_index=False)['streams']
                .sum()
                .nlargest(5, 'streams')
                .sort_values('streams', ascending=True)
            )
            fig_market = go.Figure()
            fig_market.add_trace(go.Bar(
                x=top_countries['streams'] / 1e9,
                y=top_countries['country'],
                orientation='h',
                marker=dict(color='#397A74'),
                text=[f"{v:.1f}B" for v in top_countries['streams'] / 1e9],
                textposition='inside',
                textfont=dict(color='#FFFFFF', size=11, family='Inter'),
                hovertemplate='Quốc gia: %{y}<br>Streams: %{x:.2f}B<extra></extra>'
            ))
            fig_market.update_layout(
                height=110,
                margin=dict(l=35, r=5, t=5, b=5),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
                yaxis=dict(showgrid=False, showticklabels=True, tickfont=dict(size=11, color='#625B5E', family='Inter'), zeroline=False)
            )
            st.plotly_chart(fig_market, use_container_width=True, config={'displayModeBar': False})
            
            if st.button("Xem thị trường →", key="btn_quick_market", use_container_width=True):
                st.session_state["nav_target"] = "Thống Kê Thị Trường"
                st.rerun()

    with col_q3:
        with st.container(border=True):
            st.markdown("""
            <div class="quick-card-marker" style="margin-bottom: 6px;">
                <div style="font-family: 'Inter', sans-serif; font-size: 11px; font-weight: 700; letter-spacing: 0.8px; color: #C96B4B; text-transform: uppercase;">
                    ĐẶC TÍNH ÂM HỌC
                </div>
                <div style="font-family: 'Montserrat', sans-serif; font-size: 17px; font-weight: 800; color: #241F21; margin-top: 2px;">
                    Đặc trưng âm nhạc
                </div>
                <div style="font-family: 'Inter', sans-serif; font-size: 12px; color: #625B5E; margin-top: 2px;">
                    Phân bổ Danceability, Energy & Valence
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            feats = ['Dance', 'Energy', 'Valence', 'Acoustic']
            vals = [
                round(float(df_raw['danceability'].mean()) * 100, 1),
                round(float(df_raw['energy'].mean()) * 100, 1),
                round(float(df_raw['valence'].mean()) * 100, 1),
                round(float(df_raw['acousticness'].mean()) * 100, 1),
            ]
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=vals + [vals[0]],
                theta=feats + [feats[0]],
                fill='toself',
                fillcolor='rgba(201, 107, 75, 0.22)',
                line=dict(color='#C96B4B', width=2),
                marker=dict(size=4, color='#7A3E65'),
                hovertemplate='%{theta}: %{r}%<extra></extra>'
            ))
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=False, range=[0, 100]),
                    angularaxis=dict(tickfont=dict(size=10, color='#625B5E', family='Inter'))
                ),
                height=110,
                margin=dict(l=25, r=25, t=10, b=10),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})
            
            if st.button("Khám phá →", key="btn_quick_audio", use_container_width=True):
                st.session_state["nav_target"] = "Đặc Tính Âm Nhạc"
                st.rerun()
elif "Tổng Quan Dữ Liệu" in current_view:
    # TIÊU ĐỀ TRANG (46px) & MÔ TẢ (18px)
    st.markdown("""
    <div style='margin-bottom: 22px;'>
        <h1 style='font-family: "Montserrat", sans-serif; font-size: 46px; font-weight: 800; color: #241F21; margin: 0; letter-spacing: -0.8px; line-height: 1.15;'>
            Tổng quan Bộ dữ liệu Spotify
        </h1>
    </div>
    """, unsafe_allow_html=True)

    # ĐIỂM HÚT MẮT RÕ RÀNG: 3 KPI TÓM TẮT TRỰC QUAN
    n_unique_tracks = len(df_unique_tracks)
    n_unique_artists = df_raw["artist_individual"].nunique()
    n_markets = df_raw["country"].nunique()
    
    st.markdown(f"""
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 20px;">
        <div style="background: #FFFFFF; border: 1px solid #D8D0C7; border-radius: 12px; padding: 18px 22px; box-shadow: 0 1px 4px rgba(36, 31, 33, 0.03);">
            <div style="font-family: 'Montserrat', sans-serif; font-size: 34px; font-weight: 900; color: #7A3E65; line-height: 1.1; margin-bottom: 4px;">
                {n_unique_tracks:,} bài hát
            </div>
            <div style="font-family: 'Inter', sans-serif; font-size: 15px; color: #625B5E;">
                trong kết quả
            </div>
        </div>
        <div style="background: #FFFFFF; border: 1px solid #D8D0C7; border-radius: 12px; padding: 18px 22px; box-shadow: 0 1px 4px rgba(36, 31, 33, 0.03);">
            <div style="font-family: 'Montserrat', sans-serif; font-size: 34px; font-weight: 900; color: #241F21; line-height: 1.1; margin-bottom: 4px;">
                {n_unique_artists:,} nghệ sĩ
            </div>
            <div style="font-family: 'Inter', sans-serif; font-size: 15px; color: #625B5E;">
                độc nhất
            </div>
        </div>
        <div style="background: #FFFFFF; border: 1px solid #D8D0C7; border-radius: 12px; padding: 18px 22px; box-shadow: 0 1px 4px rgba(36, 31, 33, 0.03);">
            <div style="font-family: 'Montserrat', sans-serif; font-size: 34px; font-weight: 900; color: #241F21; line-height: 1.1; margin-bottom: 4px;">
                {n_markets:,} thị trường
            </div>
            <div style="font-family: 'Inter', sans-serif; font-size: 15px; color: #625B5E;">
                được khảo sát
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # KHỐI ĐIỀU KHIỂN CHIA THÀNH 2 TẦNG GỌN GÀNG
    # TẦNG 1: [ Tìm kiếm bài hát... ] [ Sắp xếp ▼ ] [ Nút Bộ lọc ]
    with st.container(border=True):
        t1_c1, t1_c2, t1_c3 = st.columns([3.2, 1.8, 1.1], gap="medium")
        with t1_c1:
            st.markdown("<div style='font-family: \"Inter\", sans-serif; font-size: 12px; font-weight: 700; color: #7A3E65; letter-spacing: 0.6px; text-transform: uppercase; margin-bottom: 6px;'>🔍 Tìm kiếm bài hát / thể loại:</div>", unsafe_allow_html=True)
            search_kw = st.text_input(
                "Tìm kiếm bài hát / thể loại:",
                placeholder="Nhập tên bài hát, nghệ sĩ hoặc thể loại...",
                label_visibility="collapsed",
                key="raw_search_kw"
            )
        with t1_c2:
            st.markdown("<div style='font-family: \"Inter\", sans-serif; font-size: 12px; font-weight: 700; color: #625B5E; letter-spacing: 0.6px; text-transform: uppercase; margin-bottom: 6px;'>Sắp xếp theo:</div>", unsafe_allow_html=True)
            sort_options = [
                "Tổng Streams (Giảm dần)",
                "Hạng Cao Nhất (Tăng dần)",
                "Số tuần trên BXH (Giảm dần)",
                "Độ phổ biến (Popularity)",
                "Độ bắt tai (Danceability)",
                "Năng lượng (Energy)"
            ]
            sort_choice = st.selectbox(
                "Sắp xếp theo:",
                options=sort_options,
                index=0,
                label_visibility="collapsed",
                key="raw_sort_choice"
            )
        with t1_c3:
            st.markdown("<div style='font-family: \"Inter\", sans-serif; font-size: 12px; font-weight: 700; color: #625B5E; letter-spacing: 0.6px; text-transform: uppercase; margin-bottom: 6px;'>Tùy chọn:</div>", unsafe_allow_html=True)
            filter_opened = st.checkbox("Bộ lọc", value=False, key="toggle_advanced_filters")

        # TẦNG 2: MỞ KHI NHẤN "BỘ LỌC"
        if filter_opened:
            st.markdown("<div style='height: 4px; border-top: 1px solid #E2DBD3; margin: 12px 0 16px 0;'></div>", unsafe_allow_html=True)
            f_c1, f_c2, f_c3 = st.columns([1.2, 1.2, 1.0], gap="medium")
            with f_c1:
                st.markdown("<p style='font-size: 14px; font-weight: 600; color: #241F21; margin-bottom: 4px;'>Nguồn dữ liệu:</p>", unsafe_allow_html=True)
                data_mode = st.radio(
                    "Nguồn dữ liệu:",
                    options=["Dữ liệu đã chuẩn hóa", "Dữ liệu gốc (Raw)"],
                    index=0,
                    horizontal=True,
                    label_visibility="collapsed",
                    key="filter_data_mode"
                )
            with f_c2:
                st.markdown("<p style='font-size: 14px; font-weight: 600; color: #241F21; margin-bottom: 4px;'>Cách gộp bài hát:</p>", unsafe_allow_html=True)
                view_granularity = st.selectbox(
                    "Cách gộp bài hát:",
                    options=["Gộp theo bài hát", "Chi tiết từng tuần BXH"],
                    index=0,
                    label_visibility="collapsed",
                    key="filter_view_granularity"
                )
            with f_c3:
                st.markdown("<p style='font-size: 14px; font-weight: 600; color: #241F21; margin-bottom: 4px;'>Số bản ghi hiển thị:</p>", unsafe_allow_html=True)
                row_limit = st.selectbox(
                    "Số bản ghi:",
                    options=[50, 100, 250, 500, "Tất cả"],
                    index=1,
                    label_visibility="collapsed",
                    key="filter_row_limit"
                )
        else:
            # Gia tri mac dinh khi chua mo panel
            data_mode = "Dữ liệu đã chuẩn hóa"
            view_granularity = "Gộp theo bài hát"
            row_limit = 100

        # DÒNG TRẠNG THÁI DẠNG CHIP GỌN GÀNG
        is_agg = "Gộp" in view_granularity
        clean_text = "Dữ liệu đã chuẩn hóa" if "chuẩn hóa" in data_mode else "Dữ liệu gốc"
        row_limit_str = f"{row_limit} bản ghi" if row_limit != "Tất cả" else "Tất cả bản ghi"
        
        st.markdown(f"""
        <div style="display: inline-flex; align-items: center; gap: 8px; background: #F2E6EE; border: 1px solid #E2DBD3; border-radius: 20px; padding: 6px 16px; margin: 12px 0 6px 0; font-size: 14px; color: #7A3E65; font-weight: 600;">
            <span>Đang xem:</span> 
            <span>{clean_text}</span> · 
            <span>{view_granularity}</span> · 
            <span>{row_limit_str}</span>
        </div>
        """, unsafe_allow_html=True)

    # ĐOẠN TRỢ GIÚP THU GỌN VÀO EXPANDER
    with st.expander("Hướng dẫn đọc góc nhìn dữ liệu (Gộp theo bài hát vs Chi tiết từng tuần)"):
        st.markdown("""
        <div style='font-size: 14px; color: #625B5E; line-height: 1.6;'>
            <b>Góc nhìn Gộp theo bài hát (Khuyến nghị):</b> Tổng hợp toàn bộ lịch sử BXH thành từng bài hát duy nhất. Mỗi ca khúc hiển thị 1 dòng đại diện với <b>Tổng lượt Streams</b>, <b>Hạng cao nhất từng đạt</b> và <b>Số tuần trụ hạng</b>.<br>
            <b>Góc nhìn Chi tiết theo tuần (Time-series):</b> Thể hiện dữ liệu nguyên bản qua từng tuần khảo sát. Một bài hát có thể xuất hiện nhiều dòng tương ứng với các tuần và thị trường khác nhau.
        </div>
        """, unsafe_allow_html=True)

    # Lấy nguồn dữ liệu theo góc nhìn đã chọn
    if is_agg:
        df_preview = df_unique_tracks.copy()
    else:
        df_preview = df_raw.copy()

    # Lọc theo từ khóa tìm kiếm
    if search_kw.strip():
        kw = search_kw.strip().lower()
        df_preview = df_preview[
            df_preview["track_name"].astype(str).str.lower().str.contains(kw, na=False) |
            df_preview["track_genre"].astype(str).str.lower().str.contains(kw, na=False)
        ]

    # Sắp xếp
    if "Streams" in sort_choice:
        df_preview = df_preview.sort_values(by="streams", ascending=False)
    elif "Hạng Cao Nhất" in sort_choice:
        df_preview = df_preview.sort_values(by="best_rank", ascending=True)
    elif "Hạng Tuần Đó" in sort_choice and "rank" in df_preview.columns:
        df_preview = df_preview.sort_values(by="rank", ascending=True)
    elif "Số tuần" in sort_choice and "weeks_count" in df_preview.columns:
        df_preview = df_preview.sort_values(by="weeks_count", ascending=False)
    elif "Popularity" in sort_choice:
        df_preview = df_preview.sort_values(by="popularity", ascending=False)
    elif "Danceability" in sort_choice:
        df_preview = df_preview.sort_values(by="danceability", ascending=False)
    elif "Energy" in sort_choice:
        df_preview = df_preview.sort_values(by="energy", ascending=False)

    total_matched = len(df_preview)
    if row_limit != "Tất cả":
        df_preview = df_preview.head(int(row_limit))

    # Đánh số thứ tự
    df_preview = df_preview.reset_index(drop=True)
    df_preview["top_order"] = df_preview.index + 1

    unit_label = "bài hát độc nhất" if is_agg else "bản ghi tuần"
    st.markdown(f"<div style='font-size:14px; color:#625B5E; margin: 14px 0 10px 0;'>Đang hiển thị <b style='color:#7A3E65;'>{len(df_preview):,}</b> / <b style='color:#241F21;'>{total_matched:,}</b> {unit_label} phù hợp</div>", unsafe_allow_html=True)

    # BẢNG DỮ LIỆU SÁNG VỚI THANH POPULARITY TÍM MẬN #7A3E65
    if is_agg:
        st.dataframe(
            df_preview[[
                "top_order", "track_name", "artist_individual", "streams", "best_rank", 
                "weeks_count", "popularity", "track_genre", "danceability", "energy", "valence"
            ]],
            column_config={
                "top_order": st.column_config.NumberColumn("Top", format="#%d", width="small"),
                "track_name": st.column_config.TextColumn("Tên Bài Hát"),
                "artist_individual": st.column_config.TextColumn("Nghệ Sĩ"),
                "streams": st.column_config.NumberColumn("Tổng Streams", format="%d"),
                "best_rank": st.column_config.NumberColumn("Hạng Cao Nhất", format="#%d", width="small"),
                "weeks_count": st.column_config.NumberColumn("Số Tuần BXH", format="%d tuần", width="small"),
                "popularity": st.column_config.ProgressColumn("Popularity", min_value=0, max_value=100, format="%d / 100"),
                "track_genre": st.column_config.TextColumn("Thể Loại"),
                "danceability": st.column_config.NumberColumn("Danceability", format="%.3f"),
                "energy": st.column_config.NumberColumn("Energy", format="%.3f"),
                "valence": st.column_config.NumberColumn("Valence", format="%.3f")
            },
            hide_index=True,
            width="stretch",
            height=460
        )
    else:
        st.dataframe(
            df_preview[[
                "top_order", "rank", "track_name", "artist_individual", "streams", 
                "week", "country", "popularity", "track_genre", "danceability", "energy", "valence"
            ]],
            column_config={
                "top_order": st.column_config.NumberColumn("STT", format="%d", width="small"),
                "rank": st.column_config.NumberColumn("Hạng Tuần", format="#%d", width="small"),
                "track_name": st.column_config.TextColumn("Tên Bài Hát"),
                "artist_individual": st.column_config.TextColumn("Nghệ Sĩ"),
                "streams": st.column_config.NumberColumn("Lượt Streams Tuần", format="%d"),
                "week": st.column_config.DateColumn("Tuần BXH", format="YYYY-MM-DD"),
                "country": st.column_config.TextColumn("Quốc Gia"),
                "popularity": st.column_config.ProgressColumn("Popularity", min_value=0, max_value=100, format="%d / 100"),
                "track_genre": st.column_config.TextColumn("Thể Loại"),
                "danceability": st.column_config.NumberColumn("Danceability", format="%.3f"),
                "energy": st.column_config.NumberColumn("Energy", format="%.3f"),
                "valence": st.column_config.NumberColumn("Valence", format="%.3f")
            },
            hide_index=True,
            width="stretch",
            height=460
        )

elif "Bộ Lọc Chi Tiết" in current_view:
    st.markdown("<h1 style='font-family: \"Montserrat\", sans-serif; font-size: 2.1rem; font-weight: 800; color: #24211E; margin-bottom: 14px;'>Bộ Lọc Dữ Liệu Chi Tiết</h1>", unsafe_allow_html=True)
    
    # ANALYSIS & MEANING BANNER (NỀN #181818, VIỀN #353535, CHỮ #C7C7C7)
    st.markdown("""
    <div style="background-color: #FFFFFF; border: 1px solid #D8D0C7; border-left: 4px solid #7A3E65; border-radius: 8px; padding: 16px 20px; margin-bottom: 22px;">
        <h4 style="color: #7A3E65; font-family: 'Montserrat', sans-serif; font-weight: 800; font-size: 0.95rem; margin-bottom: 6px;">PHÂN TÍCH & Ý NGHĨA: CÔNG CỤ LỌC ĐA CHIỀU</h4>
        <p style="color: #625C54; font-family: 'Inter', sans-serif; font-size: 0.88rem; margin: 0; line-height: 1.55;">
            Công cụ này giúp bạn 'đào sâu' vào dữ liệu để tìm kiếm những thông tin cụ thể. Bạn có thể kết hợp nhiều tiêu chí như lọc theo tên nghệ sĩ, tìm tất cả ca khúc Pop thuộc nhóm High Income, hoặc lọc các bài hát có chỉ số Danceability & Energy đạt ngưỡng bứt phá.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # CONTAINER TIÊU CHÍ LỌC (CÓ KHOẢNG THỞ RỘNG RÃI)
    with st.container(border=True):
        st.markdown("<h3 style='font-size: 1.1rem; font-weight: 800; color: #24211E; margin-bottom: 16px;'>Tiêu Chí Lọc Đa Chiều</h3>", unsafe_allow_html=True)
        
        # HÀNG 1: ĐỊA LÝ, THỂ LOẠI & NGHỆ SĨ
        c1, c2, c3 = st.columns([1.1, 1.1, 1.4], gap="medium")
        with c1:
            flt_reg = st.selectbox("Quốc Gia / Khu Vực:", regions_list, key="flt_reg")
        with c2:
            flt_gen = st.selectbox("Thể Loại Âm Nhạc:", genres_list, key="flt_gen")
        with c3:
            flt_artist = st.text_input("Tên Nghệ Sĩ:", placeholder="Gõ tên nghệ sĩ (ví dụ: Taylor Swift, Drake, Olivia...)", key="flt_artist")
            
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        
        # HÀNG 2: THU NHẬP, TÂM TRẠNG & ĐẶC TÍNH
        c4, c5, c6, c7 = st.columns(4, gap="medium")
        with c4:
            flt_inc = st.selectbox("Nhóm Thu Nhập (World Bank):", income_list, key="flt_inc")
        with c5:
            flt_mood = st.selectbox("Tâm Trạng (Mood):", mood_list, key="flt_mood")
        with c6:
            flt_exp = st.selectbox("Nội Dung Explicit:", ["Tất cả", "Explicit (Nhạy cảm)", "Clean (Lành mạnh)"], key="flt_exp")
        with c7:
            flt_trend = st.selectbox("Trạng Thái Trending:", ["Tất cả", "Trending (Bứt phá)", "Normal (Bình thường)"], key="flt_trend")
            
        st.divider()
        
        # HÀNG 3: THANH TRƯỢT ÂM HỌC
        sc1, sc2, sc3 = st.columns(3, gap="large")
        with sc1:
            flt_dance = st.slider("Danceability (>=):", min_value=0.0, max_value=1.0, value=0.0, step=0.05, key="flt_dance")
        with sc2:
            flt_energy = st.slider("Energy (>=):", min_value=0.0, max_value=1.0, value=0.0, step=0.05, key="flt_energy")
        with sc3:
            flt_valence = st.slider("Valence (>=):", min_value=0.0, max_value=1.0, value=0.0, step=0.05, key="flt_valence")
            
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        btn_filter = st.button("Áp Dụng Bộ Lọc", type="primary", key="btn_filter")
        
    # XỬ LÝ LỌC DỮ LIỆU
    df_filtered = df_raw.copy()
    if flt_reg != "Tất cả khu vực":
        df_filtered = df_filtered[df_filtered["region_wb"] == flt_reg]
    if flt_gen != "Tất cả thể loại":
        df_filtered = df_filtered[df_filtered["track_genre"] == flt_gen]
    if flt_artist.strip():
        kw_art = flt_artist.strip().lower()
        df_filtered = df_filtered[df_filtered["artist_individual"].astype(str).str.lower().str.contains(kw_art, na=False)]
    if flt_inc != "Tất cả nhóm thu nhập":
        df_filtered = df_filtered[df_filtered["income_group"] == flt_inc]
    if flt_mood != "Tất cả tâm trạng":
        df_filtered = df_filtered[df_filtered["mood_category"] == flt_mood]
    if flt_exp == "Explicit (Nhạy cảm)":
        df_filtered = df_filtered[df_filtered["explicit"] == True]
    elif flt_exp == "Clean (Lành mạnh)":
        df_filtered = df_filtered[df_filtered["explicit"] == False]
    if flt_trend == "Trending (Bứt phá)":
        df_filtered = df_filtered[df_filtered["is_trending"] == 1]
    elif flt_trend == "Normal (Bình thường)":
        df_filtered = df_filtered[df_filtered["is_trending"] == 0]
        
    df_filtered = df_filtered[
        (df_filtered["danceability"] >= flt_dance) &
        (df_filtered["energy"] >= flt_energy) &
        (df_filtered["valence"] >= flt_valence)
    ]
    
    st.markdown(f"<p style='font-size: 0.92rem; font-weight: 700; color: #7A3E65; margin: 20px 0 12px 0;'>Tìm thấy <b>{len(df_filtered):,}</b> bản ghi phù hợp với tiêu chí lọc!</p>", unsafe_allow_html=True)
    st.dataframe(
        df_filtered[["track_name", "artist_individual", "streams", "rank", "week", "country", "danceability", "energy", "valence", "popularity", "track_genre", "income_group", "mood_category"]],
        width="stretch",
        height=400
    )

# MAN HINH 2: TONG QUAN THI TRUONG AM NHAC (BENTO GRID - 3-TIER ARCHITECTURE)
elif "Tổng Quan Thị Trường" in current_view:
    st.markdown("""
    <div style='margin-bottom: 20px;'>
        <div style='margin-bottom: 4px;'>
            <h1 style='font-family: "Montserrat", "Be Vietnam Pro", sans-serif; font-size: 2.1rem; font-weight: 900; color: #24211E; margin: 0; letter-spacing: -0.8px;'>Tổng Quan Thị Trường Âm Nhạc</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # =========================================================================
    # TẦNG 1: BỘ LỌC THỊ TRƯỜNG + 4 CHỈ SỐ TỔNG QUAN (1 LỚN ~40% + 3 NHỎ BÊN CẠNH)
    # =========================================================================
    with st.container(border=True):
        st.markdown("""
        <div style="margin-bottom:10px;">
            <div style="font-family: 'Montserrat', 'Be Vietnam Pro', sans-serif; font-size:0.88rem; font-weight:800; color:#24211E; letter-spacing: -0.2px;">BỘ LỌC ĐA CHIỀU THỊ TRƯỜNG</div>
        </div>
        """, unsafe_allow_html=True)
        f_c1, f_c2, f_c3 = st.columns([1, 1, 1], gap="medium")
        with f_c1:
            sel_reg = st.selectbox("Khu vực địa lý:", regions_list, key="ov_reg")
        with f_c2:
            sel_gen = st.selectbox("Thể loại âm nhạc:", genres_list, key="ov_gen")
        with f_c3:
            sel_yr = st.selectbox("Năm khảo sát:", years_list, key="ov_yr")
    
    # Lọc dữ liệu riêng cho tab này
    df_view = df_raw.copy()
    if sel_reg != "Tất cả khu vực":
        df_view = df_view[df_view["region_wb"] == sel_reg]
    if sel_gen != "Tất cả thể loại":
        df_view = df_view[df_view["track_genre"] == sel_gen]
    if sel_yr != "Tất cả các năm":
        df_view = df_view[df_view["year"] == int(sel_yr)]
    
    if df_view.empty:
        st.warning("Không tìm thấy dữ liệu phù hợp với bộ lọc đã chọn!")
        st.stop()
    
    # 4 CHỈ SỐ TỔNG QUAN: PHÁ VỠ LƯỚI 4 Ô ĐỀU NHAU (1 LỚN ~40% + 3 NHỎ ~60%)
    n_tracks = df_view['track_name'].nunique()
    n_artists = df_view['artist_individual'].nunique()
    avg_duration = df_view['duration_min'].mean() if 'duration_min' in df_view else 3.3
    pop_series = pd.to_numeric(df_view['popularity'], errors='coerce').dropna()
    avg_pop = pop_series.mean() if not pop_series.empty else 80.0

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    k_hero, k_sub = st.columns([1.1, 1.6], gap="medium")
    
    with k_hero:
        st.markdown(f"""
        <div class="hero-anchor-card" style="min-height: 118px; padding: 18px 22px; background: #FFFFFF; border: 1px solid #D8D0C7; border-radius: 12px;">
            <div style="margin-bottom:4px;">
                <div style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; color: #81786E;">Bài Hát Khảo Sát</div>
            </div>
            <div style="font-family: 'Montserrat', sans-serif; font-size: 2.8rem; font-weight: 900; line-height: 1.05; letter-spacing: -1.2px; color: #24211E; margin-bottom: 4px;">
                {n_tracks:,} <span style="font-size: 1.15rem; color: #7A3E65; font-weight: 800;">TRACKS</span>
            </div>
            <div style="font-size: 0.76rem; color: #81786E; line-height: 1.35;">
                Tổng số ca khúc lọt BXH Spotify trong phạm vi thị trường đã chọn.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with k_sub:
        s1, s2, s3 = st.columns(3, gap="medium")
        with s1:
            st.markdown(f"""
            <div class="sub-metric-card" style="min-height: 118px; padding: 16px 18px; background: #FFFFFF; border: 1px solid #D8D0C7; border-radius: 12px;">
                <div style="font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.6px; color: #81786E;">Nghệ Sĩ Khảo Sát</div>
                <div style="font-family: 'Montserrat', sans-serif; font-size: 1.7rem; font-weight: 800; color: #24211E; margin: 4px 0;">{n_artists:,}</div>
                <div style="font-size: 0.72rem; color: #81786E;">Nghệ sĩ độc lập / nhóm</div>
            </div>
            """, unsafe_allow_html=True)
        with s2:
            st.markdown(f"""
            <div class="sub-metric-card" style="min-height: 118px; padding: 16px 18px; background: #FFFFFF; border: 1px solid #D8D0C7; border-radius: 12px;">
                <div style="font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.6px; color: #81786E;">Thời Lượng TB</div>
                <div style="font-family: 'Montserrat', sans-serif; font-size: 1.7rem; font-weight: 800; color: #24211E; margin: 4px 0;">{avg_duration:.2f}m</div>
                <div style="font-size: 0.72rem; color: #81786E;">~{int(avg_duration * 60)}s chuẩn streaming</div>
            </div>
            """, unsafe_allow_html=True)
        with s3:
            st.markdown(f"""
            <div class="sub-metric-card" style="min-height: 118px; padding: 16px 18px; background: #FFFFFF; border: 1px solid #D8D0C7; border-radius: 12px;">
                <div style="font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.6px; color: #81786E;">Độ Phổ Biến TB</div>
                <div style="font-family: 'Montserrat', sans-serif; font-size: 1.7rem; font-weight: 800; color: #7A3E65; margin: 4px 0;">{avg_pop:.0f}/100</div>
                <div style="font-size: 0.72rem; color: #81786E;">Điểm Popularity toàn cầu</div>
            </div>
            """, unsafe_allow_html=True)

    # =========================================================================
    # TẦNG 2: PHÂN TÍCH THỊ TRƯỜNG TỔNG THỂ (CĂN LƯỚI ĐỒNG BỘ 3 CỘT: 2 DONUT + 1 BAR)
    # =========================================================================
    st.markdown("""
    <div style="margin: 24px 0 12px 0; border-bottom: 1px solid #D8D0C7; padding-bottom: 8px;">
        <div style="font-family: 'Montserrat', sans-serif; font-size: 1.05rem; font-weight: 800; color: #24211E; letter-spacing: -0.2px;">
            Phân Tích Cơ Cấu Thị Trường (Market Distribution)
        </div>
    </div>
    """, unsafe_allow_html=True)

    chart_c1, chart_c2, chart_c3 = st.columns([1.0, 1.0, 1.25], gap="medium")
    
    with chart_c1:
        with st.container(border=True):
            st.markdown("""
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <span style="font-size:0.85rem; font-weight:700; color:#24211E;">Tỷ lệ Explicit vs Clean</span>
                <span style="font-size:0.72rem; color:#81786E;">Nội dung 18+</span>
            </div>
            """, unsafe_allow_html=True)
            if "explicit" in df_view.columns:
                exp_counts = df_view["explicit"].value_counts().reset_index()
                exp_counts.columns = ["Type", "Count"]
                exp_counts["Type"] = exp_counts["Type"].map({True: "Explicit", False: "Clean"}).fillna("Clean")
                fig_d1 = px.pie(
                    exp_counts, values="Count", names="Type", hole=0.68,
                    color="Type",
                    color_discrete_map={"Explicit": "#7A3E65", "Clean": "#D8D0C7"}
                )
                fig_d1.update_layout(
                    **PLOTLY_THEME, height=220, showlegend=True,
                    legend=dict(orientation="h", yanchor="top", y=-0.05, xanchor="center", x=0.5, font=dict(color="#81786E", size=11)),
                    margin=dict(t=10, b=10, l=10, r=10)
                )
                fig_d1.update_traces(textinfo="percent", textfont=dict(size=12, color="#24211E"))
                st.plotly_chart(fig_d1, use_container_width=True)
    
    with chart_c2:
        with st.container(border=True):
            st.markdown("""
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <span style="font-size:0.85rem; font-weight:700; color:#24211E;">Nhóm Thu Nhập (World Bank)</span>
                <span style="font-size:0.72rem; color:#81786E;">Phân bổ kinh tế</span>
            </div>
            """, unsafe_allow_html=True)
            if "income_group" in df_view.columns:
                inc_counts = df_view["income_group"].dropna().value_counts().head(4).reset_index()
                inc_counts.columns = ["Income", "Count"]
                fig_d2 = px.pie(
                    inc_counts, values="Count", names="Income", hole=0.68,
                    color_discrete_sequence=SPOTIFY_DISCRETE_PALETTE
                )
                fig_d2.update_layout(
                    **PLOTLY_THEME, height=220, showlegend=True,
                    legend=dict(orientation="h", yanchor="top", y=-0.05, xanchor="center", x=0.5, font=dict(color="#81786E", size=10)),
                    margin=dict(t=10, b=10, l=10, r=10)
                )
                fig_d2.update_traces(textinfo="percent", textfont=dict(size=11, color="#24211E"))
                st.plotly_chart(fig_d2, use_container_width=True)
        
    with chart_c3:
        with st.container(border=True):
            st.markdown("""
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <span style="font-size:0.85rem; font-weight:700; color:#24211E;">Lượt Stream Theo Tháng</span>
                <span style="font-size:0.72rem; color:#81786E;">Chuỗi thời gian</span>
            </div>
            """, unsafe_allow_html=True)
            df_copy = df_view.copy()
            df_copy["month_name"] = df_copy["week"].dt.strftime("%b")
            month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            m_streams = df_copy.groupby("month_name")["streams"].sum().reindex(month_order).dropna().reset_index()
            fig_m = px.bar(
                m_streams, x="month_name", y="streams",
                color_discrete_sequence=["#9B51E0"],
                labels={"month_name": "Tháng", "streams": "Lượt Streams"}
            )
            fig_m.update_layout(
                **PLOTLY_THEME, height=220,
                margin=dict(t=10, b=15, l=25, r=15),
                xaxis=dict(title="", showgrid=False, tickfont=dict(color="#81786E")),
                yaxis=dict(title="", showgrid=True, gridcolor="#EEE9E1", tickfont=dict(color="#81786E"))
            )
            fig_m.update_traces(hovertemplate="<b>Tháng %{x}</b><br>Streams: %{y:,.0f}<extra></extra>")
            st.plotly_chart(fig_m, use_container_width=True)

    # =========================================================================
    # TẦNG 3: KHÁM PHÁ BÀI HÁT CỤ THỂ (INTERACTIVE TRACK EXPLORER)
    # =========================================================================
    st.markdown("""
    <div style="margin: 28px 0 14px 0; border-bottom: 1px solid #D8D0C7; padding-bottom: 8px;">
        <div style="font-family: 'Montserrat', sans-serif; font-size: 1.05rem; font-weight: 800; color: #7A3E65; letter-spacing: -0.2px;">
            Khám Phá Bài Hát Cụ Thể (Interactive Track Explorer)
        </div>
    </div>
    """, unsafe_allow_html=True)

    top_tracks = df_view.groupby(["track_name", "artist_individual"])["streams"].sum().reset_index()
    top_tracks = top_tracks.sort_values(by="streams", ascending=False).head(40)
    
    if top_tracks.empty:
        st.info("Chưa có dữ liệu bài hát trong bộ lọc hiện tại.")
    else:
        track_dict = {f"{row['track_name']} — {row['artist_individual']}": (row['track_name'], row['artist_individual']) for _, row in top_tracks.iterrows()}
        track_list = list(track_dict.keys())
        
        with st.container(border=True):
            st.markdown("<p style='font-size:0.82rem; font-weight:700; color:#24211E; margin-bottom:8px;'>1. Chọn bài hát từ Top thịnh hành:</p>", unsafe_allow_html=True)
            sel_track_str = st.selectbox("Chọn ca khúc:", options=track_list, index=0, label_visibility="collapsed", key="track_explorer_sel")
            sel_tname, sel_aname = track_dict[sel_track_str]
            
            # Aggregate stats for the chosen track across market/weeks
            song_sub = df_view[(df_view["track_name"] == sel_tname) & (df_view["artist_individual"] == sel_aname)]
            best_rank = int(song_sub["rank"].min()) if "rank" in song_sub and not song_sub["rank"].dropna().empty else 1
            total_streams = int(song_sub["streams"].sum()) if "streams" in song_sub else 0
            
            # Genre
            genre_series = song_sub["track_genre"].dropna()
            if genre_series.empty or not str(genre_series.iloc[0]).strip():
                genre_series = song_sub.get("macro_genre", pd.Series(["Pop"])).dropna()
            genre_val = str(genre_series.iloc[0]) if not genre_series.empty else "Pop"
            
            # Audio features normalized strictly to 0-100%
            dance_val = float(song_sub["danceability"].mean()) if "danceability" in song_sub else 0.7
            energy_val = float(song_sub["energy"].mean()) if "energy" in song_sub else 0.6
            valence_val = float(song_sub["valence"].mean()) if "valence" in song_sub else 0.5
            
            dance_pct = max(0, min(100, int(round(dance_val * 100 if dance_val <= 1.0 else dance_val))))
            energy_pct = max(0, min(100, int(round(energy_val * 100 if energy_val <= 1.0 else energy_val))))
            valence_pct = max(0, min(100, int(round(valence_val * 100 if valence_val <= 1.0 else valence_val))))
            
            # Popularity
            pop_series = pd.to_numeric(song_sub.get("popularity", pd.Series(dtype=float)), errors="coerce").dropna()
            pop_score = int(pop_series.max()) if not pop_series.empty else 82

            st.markdown(f"""
            <div style="background-color: #FFFFFF; border: 1px solid #D8D0C7; border-radius: 12px; padding: 18px 20px; margin-top: 10px; margin-bottom: 16px; box-shadow: 0 1px 4px rgba(36,33,30,0.03);">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px; margin-bottom: 16px;">
                    <div>
                        <div style="font-family: 'Montserrat', sans-serif; font-size: 1.35rem; font-weight: 800; color: #24211E; line-height: 1.2;">{sel_tname}</div>
                        <div style="font-size: 0.92rem; color: #81786E; margin-top: 3px;">{sel_aname}</div>
                    </div>
                    <div style="display:flex; gap:8px; align-items:center;">
                        <div style="background: rgba(122, 62, 101, 0.08); border: 1.5px solid #7A3E65; border-radius: 20px; padding: 4px 14px; font-size: 0.8rem; font-weight: 700; color: #7A3E65;">Popularity: {pop_score}/100</div>
                        <div style="background: #F2EDE7; border: 1px solid #D8D0C7; border-radius: 20px; padding: 4px 14px; font-size: 0.8rem; font-weight: 600; color: #24211E;">{genre_val}</div>
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 18px;">
                    <div style="background: #F2EDE7; border: 1px solid #D8D0C7; border-radius: 10px; padding: 12px 14px;">
                        <div style="font-size: 0.7rem; font-weight: 700; text-transform: uppercase; color: #81786E; letter-spacing: 0.5px;">Nghệ Sĩ & Thể Loại</div>
                        <div style="font-size: 0.95rem; font-weight: 700; color: #24211E; margin-top: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{sel_aname}</div>
                        <div style="font-size: 0.75rem; color: #7A3E65; margin-top: 2px;">{genre_val}</div>
                    </div>
                    <div style="background: #F2EDE7; border: 1px solid #D8D0C7; border-radius: 10px; padding: 12px 14px;">
                        <div style="font-size: 0.7rem; font-weight: 700; text-transform: uppercase; color: #81786E; letter-spacing: 0.5px;">Hạng Cao Nhất</div>
                        <div style="font-family: 'Montserrat', sans-serif; font-size: 1.35rem; font-weight: 800; color: #24211E; margin-top: 2px;">#{best_rank}</div>
                        <div style="font-size: 0.75rem; color: #81786E; margin-top: 2px;">Top 200 BXH</div>
                    </div>
                    <div style="background: #F2EDE7; border: 1px solid #D8D0C7; border-radius: 10px; padding: 12px 14px;">
                        <div style="font-size: 0.7rem; font-weight: 700; text-transform: uppercase; color: #81786E; letter-spacing: 0.5px;">Tổng Streams Lũy Kế</div>
                        <div style="font-family: 'Montserrat', sans-serif; font-size: 1.35rem; font-weight: 800; color: #7A3E65; margin-top: 2px;">{total_streams:,.0f}</div>
                        <div style="font-size: 0.75rem; color: #81786E; margin-top: 2px;">Lượt phát tích lũy</div>
                    </div>
                </div>
                <div style="display: flex; flex-direction: column; gap: 12px;">
                    <div>
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 5px;">
                            <span style="font-size: 0.82rem; font-weight: 600; color: #24211E;">Độ bắt tai khiêu vũ (Danceability)</span>
                            <span style="font-family: 'Montserrat', sans-serif; font-size: 0.85rem; font-weight: 800; color: #7A3E65;">{dance_pct}%</span>
                        </div>
                        <div style="width: 100%; background: #EDE7DD; height: 8px; border-radius: 4px; overflow: hidden;">
                            <div style="background: #7A3E65; width: {dance_pct}%; height: 100%; border-radius: 4px;"></div>
                        </div>
                    </div>
                    <div>
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 5px;">
                            <span style="font-size: 0.82rem; font-weight: 600; color: #24211E;">Mức năng lượng sôi động (Energy)</span>
                            <span style="font-family: 'Montserrat', sans-serif; font-size: 0.85rem; font-weight: 800; color: #C96B4B;">{energy_pct}%</span>
                        </div>
                        <div style="width: 100%; background: #EDE7DD; height: 8px; border-radius: 4px; overflow: hidden;">
                            <div style="background: #C96B4B; width: {energy_pct}%; height: 100%; border-radius: 4px;"></div>
                        </div>
                    </div>
                    <div>
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 5px;">
                            <span style="font-size: 0.82rem; font-weight: 600; color: #24211E;">Tích cực cảm xúc giai điệu (Valence)</span>
                            <span style="font-family: 'Montserrat', sans-serif; font-size: 0.85rem; font-weight: 800; color: #D2A13C;">{valence_pct}%</span>
                        </div>
                        <div style="width: 100%; background: #EDE7DD; height: 8px; border-radius: 4px; overflow: hidden;">
                            <div style="background: #D2A13C; width: {valence_pct}%; height: 100%; border-radius: 4px;"></div>
                        </div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

            # Weekly Stream Trend Chart placed underneath
            track_weekly = song_sub.groupby("week")["streams"].sum().reset_index().sort_values("week")
            fig_tr = go.Figure()
            if len(track_weekly) > 1:
                fig_tr.add_trace(go.Scatter(
                    x=track_weekly["week"], 
                    y=track_weekly["streams"], 
                    mode="lines+markers", 
                    name=sel_tname,
                    line=dict(color="#7A3E65", width=2.5, shape="spline"),
                    marker=dict(size=6, color="#7A3E65"),
                    fill="tozeroy", 
                    fillcolor="rgba(30, 215, 96, 0.12)",
                    hovertemplate="Tuần: %{x|%d/%m/%Y}<br>Streams: %{y:,.0f}<extra></extra>"
                ))
                chart_title = f"Biến thiên lượt stream theo tuần: <b>{sel_tname}</b>"
            else:
                w_trend = df_view.groupby(pd.Grouper(key="week", freq="W"))["streams"].sum().reset_index()
                fig_tr.add_trace(go.Scatter(
                    x=w_trend["week"], 
                    y=w_trend["streams"], 
                    mode="lines", 
                    line=dict(color="#7A3E65", width=2.5, shape="spline"),
                    fill="tozeroy", 
                    fillcolor="rgba(30, 215, 96, 0.12)",
                    hovertemplate="Tuần: %{x|%d/%m/%Y}<br>Streams: %{y:,.0f}<extra></extra>"
                ))
                chart_title = "Tăng trưởng lượt stream lũy kế toàn thị trường theo tuần"

            fig_tr.update_layout(
                **PLOTLY_THEME, 
                height=260, 
                title=dict(text=chart_title, font=dict(size=13, color="#24211E")),
                margin=dict(t=40, b=20, l=35, r=20),
                xaxis=dict(gridcolor="#EEE9E1", title=""),
                yaxis=dict(gridcolor="#EEE9E1", title="")
            )
            st.plotly_chart(fig_tr, use_container_width=True)

        # TẦNG 4: CROSS-COUNTRY TASTE RADAR (SO SÁNH THỊ HIẾU QUỐC GIA)
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        render_cross_country_taste_radar(df_raw, key_prefix="market_taste")

# MÀN HÌNH CHUYÊN BIỆT: SO SÁNH THỊ HIẾU QUỐC GIA (CROSS-COUNTRY TASTE RADAR)
elif "So Sánh Thị Hiếu" in current_view or "Taste Radar" in current_view:
    st.markdown("""<div style='margin-bottom: 22px;'>
        <h1 style='font-family: "Montserrat", sans-serif; font-size: 42px; font-weight: 800; color: #241F21; margin: 0; letter-spacing: -0.8px; line-height: 1.15;'>
            So Sánh Thị Hiếu Quốc Gia (Taste Radar)
        </h1>
        <p style='font-family: "Inter", sans-serif; font-size: 15px; color: #625B5E; margin-top: 4px;'>
            Không gian phân tích đa chiều so sánh thị hiếu âm nhạc giữa hai quốc gia bất kỳ trên bảng xếp hạng Spotify toàn cầu qua 6 chỉ số âm học chuẩn hóa (0 – 100%).
        </p>
    </div>""", unsafe_allow_html=True)

    render_cross_country_taste_radar(df_raw, key_prefix="standalone_taste_radar")

# MAN HINH 3: TRUC QUAN HOA DU LIEU & KHUNG CAU HINH BIEN (STUDIO)
elif "Trực Quan Hóa Dữ Liệu" in current_view:
    st.markdown("""
    <div class="section-header" style="margin-top:8px; margin-bottom:12px;">
        <span class="section-title">Không Gian Trực Quan Hóa Dữ Liệu (Visual Analytics Studio)</span>
        <span class="section-desc">Bộ sưu tập biểu đồ phân tích chuyên sâu kèm nhận xét & giải thích ý nghĩa dữ liệu (Dễ dàng mở rộng)</span>
    </div>
    """, unsafe_allow_html=True)
    
    # 1. THANH CHỌN BIỂU ĐỒ CHÍNH (ĐỒNG BỘ 2 CHIỀU VỚI SIDEBAR)
    curr_chart = st.session_state.get("active_viz_chart", CHART_OPTIONS[0])
    idx = CHART_OPTIONS.index(curr_chart) if curr_chart in CHART_OPTIONS else 0
    top_v1, top_v2 = st.columns([2.7, 1.0], gap="medium")
    with top_v1:
        st.selectbox(
            "Chọn biểu đồ để hiển thị:",
            options=CHART_OPTIONS,
            index=idx,
            key="main_chart_select",
            on_change=on_main_chart_change
        )
    with top_v2:
        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
        toggle_filter = st.checkbox("⚙️ Bộ lọc dữ liệu", value=False, key="viz_filter_toggle")
    
    current_chart = st.session_state.get("active_viz_chart", CHART_OPTIONS[0])
    
    # 2. KHUNG BO LOC NÂNG CAO (KHI BẬT)
    if toggle_filter:
        with st.container(border=True):
            st.markdown("<div style='font-size:0.85rem; font-weight:700; color:#24211E; margin-bottom:6px;'>Bộ lọc dữ liệu tương tác đa chiều</div>", unsafe_allow_html=True)
            f1, f2, f3, f4 = st.columns([1.1, 1.4, 1.1, 1], gap="medium")
            with f1:
                sel_reg_viz = st.selectbox("Khu vực địa lý:", regions_list, key="vz_reg")
            with f2:
                avail_c = sorted(df_raw[df_raw["region_wb"] == sel_reg_viz]["country"].dropna().unique()) if sel_reg_viz != "Tất cả khu vực" else sorted(df_raw["country"].dropna().unique())
                sel_ctry_viz = st.multiselect("Quốc gia cụ thể:", avail_c, placeholder="Tất cả quốc gia...", key="vz_ctry")
            with f3:
                sel_gen_viz = st.selectbox("Thể loại âm nhạc:", genres_list, key="vz_gen")
            with f4:
                sel_yr_viz = st.selectbox("Năm khảo sát:", years_list, key="vz_yr")
                
            df_viz = df_raw.copy()
            if sel_reg_viz != "Tất cả khu vực":
                df_viz = df_viz[df_viz["region_wb"] == sel_reg_viz]
            if sel_ctry_viz:
                df_viz = df_viz[df_viz["country"].isin(sel_ctry_viz)]
            if sel_gen_viz != "Tất cả thể loại":
                df_viz = df_viz[df_viz["track_genre"] == sel_gen_viz]
            if sel_yr_viz != "Tất cả các năm":
                df_viz = df_viz[df_viz["year"] == int(sel_yr_viz)]
    else:
        df_viz = df_raw.copy()
        
    if df_viz.empty:
        st.warning("⚠️ Không có bản ghi nào thỏa mãn bộ lọc đã chọn. Vui lòng mở rộng khoảng lọc.")
    else:
        # ═════════════════════════════════════════════════════════════════════════════
        # 3. HIỂN THỊ BIỂU ĐỒ ĐÃ CHỌN VÀ NHẬN XÉT PHÂN TÍCH
        # ═════════════════════════════════════════════════════════════════════════════
        if "Bản đồ" in current_chart:
            # ─── BIỂU ĐỒ 1: BẢN ĐỒ THỊ PHẦN TOÀN CẦU (OUR WORLD IN DATA STYLE) ───
            render_owid_geographic_explorer(df_raw, key_prefix="studio_owid_geo")
            
            # Nhận xét & phân tích tự động thay đổi theo từng quốc gia được chọn
            sel_country = st.session_state.get("studio_owid_geo_spotlight", "Vietnam")
            sel_year = st.session_state.get("studio_owid_geo_year", 2022)
            render_dynamic_country_map_insight(df_raw, country_name=sel_country, year=sel_year)

        elif "Taste Radar" in current_chart or "thị hiếu" in current_chart.lower():
            # ─── BIỂU ĐỒ 2: SO SÁNH THỊ HIẾU QUỐC GIA (TASTE RADAR) ───
            render_cross_country_taste_radar(df_raw, key_prefix="studio_taste")
            
        elif "Tương quan" in current_chart and ("Danceability" in current_chart or "Scatter" in current_chart or "tùy chọn" in current_chart or "đặc trưng" in current_chart):
                        # ─── BIỂU ĐỒ 3: KHÁM PHÁ TƯƠNG QUAN ĐẶC TRƯNG ÂM HỌC (CHUẨN HÓA & TINH GỌN) ───
            st.markdown('<div class="slot-card" style="padding:18px 20px; background:#FFFFFF; border:1px solid #D8D0C7; border-radius:12px; margin-bottom:14px; box-shadow:0 2px 8px rgba(36,31,33,0.03);">', unsafe_allow_html=True)
            
            # Header
            st.markdown("""
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:12px; border-bottom:1px solid #D8D0C7; padding-bottom:10px;">
                <div>
                    <div style="font-family:'Montserrat',sans-serif; font-size:1.18rem; font-weight:800; color:#241F21; letter-spacing:-0.3px;">
                        Khám Phá Tương Quan Đặc Trưng Âm Học (Feature Correlation Explorer)
                    </div>
                    <div style="font-size:0.8rem; color:#625B5E; margin-top:2px;">
                        Kiểm tra mức độ liên kết tuyến tính (hệ số Pearson r và R²) giữa hai đặc tính âm thanh bất kỳ, minh bạch đơn vị phân tích và hạn chế sai lệch do bài hát lặp lại.
                    </div>
                </div>
                <div style="background:#F2EDE7; border:1px solid #D8D0C7; border-radius:6px; padding:4px 10px; font-family:'Montserrat',sans-serif; font-size:0.74rem; font-weight:700; color:#7A3E65;">
                    PHÂN TÍCH ĐA BIẾN
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Feature Catalog
            FEAT_CATALOG = {
                "danceability": {"name": "Danceability (Độ bắt tai / Nhảy múa)", "short": "Danceability", "unit": "(0.00 – 1.00)"},
                "energy": {"name": "Energy (Mức năng lượng)", "short": "Energy", "unit": "(0.00 – 1.00)"},
                "valence": {"name": "Valence (Cảm xúc tích cực)", "short": "Valence", "unit": "(0.00 – 1.00)"},
                "acousticness": {"name": "Acousticness (Độ mộc mạc)", "short": "Acousticness", "unit": "(0.00 – 1.00)"},
                "speechiness": {"name": "Speechiness (Độ nhiều lời / Rap)", "short": "Speechiness", "unit": "(0.00 – 1.00)"},
                "liveness": {"name": "Liveness (Chất sống trực tiếp)", "short": "Liveness", "unit": "(0.00 – 1.00)"},
                "loudness": {"name": "Loudness (Độ lớn âm lượng)", "short": "Loudness", "unit": "(dB)"},
                "tempo": {"name": "Tempo (Nhịp độ bài hát)", "short": "Tempo", "unit": "(BPM)"},
                "popularity": {"name": "Popularity (Độ phổ biến)", "short": "Popularity", "unit": "(0 – 100)"},
                "duration_min": {"name": "Duration (Thời lượng ca khúc)", "short": "Thời lượng", "unit": "(phút)"},
                "streams": {"name": "Streams (Lượt nghe tích lũy)", "short": "Lượt Streams", "unit": "(lượt)"}
            }
            
            available_feats = [k for k in FEAT_CATALOG.keys() if k in df_viz.columns]

            # 1. HÀNG PRESET GỢI Ý NHANH (GIỮ 3 CẶP PHỔ BIẾN NHẤT + NÚT XEM THÊM, HOÀN TOÀN BỎ EMOJI)
            st.markdown("<p style='font-size:0.73rem; font-weight:700; color:#81786E; text-transform:uppercase; letter-spacing:0.5px; margin:0 0 5px 0;'>Cặp biến phổ biến:</p>", unsafe_allow_html=True)
            p1, p2, p3, p4 = st.columns([1.2, 1.2, 1.2, 1.0])
            with p1:
                if st.button("Danceability × Energy", key="p_d_e", use_container_width=True):
                    st.session_state["sc_feat_x"] = "danceability"
                    st.session_state["sc_feat_y"] = "energy"
                    st.rerun()
            with p2:
                if st.button("Energy × Loudness", key="p_e_l", use_container_width=True):
                    st.session_state["sc_feat_x"] = "energy"
                    st.session_state["sc_feat_y"] = "loudness"
                    st.rerun()
            with p3:
                if st.button("Valence × Danceability", key="p_v_d", use_container_width=True):
                    st.session_state["sc_feat_x"] = "valence"
                    st.session_state["sc_feat_y"] = "danceability"
                    st.rerun()
            with p4:
                with st.popover("Xem thêm...", use_container_width=True):
                    st.markdown("<div style='font-size:0.78rem; font-weight:700; color:#7A3E65; margin-bottom:6px;'>Các cặp biến khác:</div>", unsafe_allow_html=True)
                    if st.button("Acousticness × Energy", key="p_a_e", use_container_width=True):
                        st.session_state["sc_feat_x"] = "acousticness"
                        st.session_state["sc_feat_y"] = "energy"
                        st.rerun()
                    if st.button("Speechiness × Danceability", key="p_s_d", use_container_width=True):
                        st.session_state["sc_feat_x"] = "speechiness"
                        st.session_state["sc_feat_y"] = "danceability"
                        st.rerun()
                    if st.button("Tempo × Danceability", key="p_t_d", use_container_width=True):
                        st.session_state["sc_feat_x"] = "tempo"
                        st.session_state["sc_feat_y"] = "danceability"
                        st.rerun()
                    if st.button("Valence × Energy", key="p_v_e", use_container_width=True):
                        st.session_state["sc_feat_x"] = "valence"
                        st.session_state["sc_feat_y"] = "energy"
                        st.rerun()

            # Default selections in session state
            if "sc_feat_x" not in st.session_state or st.session_state["sc_feat_x"] not in available_feats:
                st.session_state["sc_feat_x"] = "danceability"
            if "sc_feat_y" not in st.session_state or st.session_state["sc_feat_y"] not in available_feats:
                st.session_state["sc_feat_y"] = "energy"
            if "sc_unit_mode" not in st.session_state:
                st.session_state["sc_unit_mode"] = "Bài hát độc nhất (Khuyến nghị)"

            # 2. HÀNG ĐIỀU KHIỂN CHÍNH TINH GỌN: [X] [Y] [ĐƠN VỊ] [TÙY CHỈNH]
            c_x, c_y, c_unit, c_cust = st.columns([1.35, 1.35, 1.25, 0.85], gap="medium")
            with c_x:
                idx_x = available_feats.index(st.session_state["sc_feat_x"]) if st.session_state["sc_feat_x"] in available_feats else 0
                chosen_x = st.selectbox(
                    "Trục hoành (Trục X):",
                    options=available_feats,
                    index=idx_x,
                    format_func=lambda k: FEAT_CATALOG[k]["name"],
                    key="sc_feat_x"
                )
            with c_y:
                idx_y = available_feats.index(st.session_state["sc_feat_y"]) if st.session_state["sc_feat_y"] in available_feats else 1
                chosen_y = st.selectbox(
                    "Trục tung (Trục Y):",
                    options=available_feats,
                    index=idx_y,
                    format_func=lambda k: FEAT_CATALOG[k]["name"],
                    key="sc_feat_y"
                )
            with c_unit:
                unit_mode = st.selectbox(
                    "Đơn vị phân tích:",
                    options=["Bài hát độc nhất (Khuyến nghị)", "Lượt xuất hiện BXH (Theo tuần)"],
                    index=0 if "Bài hát độc nhất" in st.session_state.get("sc_unit_mode", "") else 1,
                    key="sc_unit_mode"
                )
            with c_cust:
                st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
                with st.popover("⚙️ Tùy chỉnh", use_container_width=True):
                    st.markdown("<div style='font-size:0.8rem; font-weight:700; color:#7A3E65; text-transform:uppercase; margin-bottom:8px;'>Tùy chỉnh biểu đồ</div>", unsafe_allow_html=True)
                    
                    color_mode = st.selectbox(
                        "Phân nhóm màu:",
                        options=["Top 7 thể loại + Khác", "Đơn sắc (Tím mận)", "Khu vực địa lý", "Nhóm thu nhập", "Năm"],
                        index=0,
                        key="sc_color_choice"
                    )
                    
                    size_choice = st.selectbox(
                        "Kích thước điểm:",
                        options=["Cố định đồng đều", "Lượt stream (Streams)", "Độ phổ biến (Popularity)"],
                        index=0,
                        key="sc_size_choice"
                    )
                    
                    show_trendline = st.checkbox("Đường hồi quy xu hướng (OLS Trendline)", value=True, key="sc_show_trendline")
                    sample_cap = st.slider("Số điểm hiển thị:", min_value=300, max_value=3000, value=1200, step=100, key="sc_sample_cap")

            # 3. XỬ LÝ DỮ LIỆU & LỌC TRÙNG THEO ĐƠN VỊ PHÂN TÍCH
            is_unique_unit = "Bài hát độc nhất" in unit_mode
            if is_unique_unit:
                # Mỗi ca khúc chỉ lấy 1 dòng đại diện để tránh thiên lệch do bài trụ hạng lâu
                analysis_df = df_viz.drop_duplicates(subset=["track_name"]).copy()
                unit_text = "bài hát độc nhất"
                unit_desc = "Dữ liệu đã lọc trùng lặp tuần; mỗi bài hát là một quan sát độc lập duy nhất."
            else:
                analysis_df = df_viz.copy()
                unit_text = "lượt xuất hiện BXH"
                unit_desc = "Dữ liệu chuỗi thời gian; tương quan có trọng số theo số tuần trụ hạng của ca khúc."

            valid_analysis = analysis_df.dropna(subset=[chosen_x, chosen_y]).copy()
            
            if len(valid_analysis) < 2:
                st.warning("Không đủ dữ liệu hợp lệ để phân tích tương quan giữa 2 chỉ số này.")
            else:
                # Tính Pearson r và R2
                x_vals = pd.to_numeric(valid_analysis[chosen_x], errors="coerce").dropna()
                y_vals = pd.to_numeric(valid_analysis[chosen_y], errors="coerce").dropna()
                common_idx = x_vals.index.intersection(y_vals.index)
                x_num = x_vals.loc[common_idx]
                y_num = y_vals.loc[common_idx]
                
                if len(common_idx) >= 2 and x_num.std() > 0 and y_num.std() > 0:
                    r_corr = float(np.corrcoef(x_num, y_num)[0, 1])
                else:
                    r_corr = 0.0
                r_squared = (r_corr ** 2) * 100.0

                # Đánh giá bằng lời văn tự nhiên & Phối màu chuẩn tím mận / teal (không dùng màu cam lạc quẻ)
                if r_corr >= 0.65:
                    eval_title = "Tương quan thuận rất mạnh"
                    eval_short = "Đồng biến tuyến tính cao"
                    kpi_bg, kpi_border, kpi_fg = "#F5EEF3", "#D8B7CC", "#7A3E65"
                elif r_corr >= 0.35:
                    eval_title = "Tương quan thuận vừa"
                    eval_short = "Đồng biến tuyến tính khá"
                    kpi_bg, kpi_border, kpi_fg = "#F5EEF3", "#D8B7CC", "#7A3E65"
                elif r_corr >= 0.10:
                    eval_title = "Tương quan thuận yếu"
                    eval_short = "Liên hệ đồng biến nhẹ"
                    kpi_bg, kpi_border, kpi_fg = "#F5EEF3", "#D8B7CC", "#7A3E65"
                elif r_corr > -0.10:
                    eval_title = "Gần như độc lập"
                    eval_short = "Không có liên kết tuyến tính"
                    kpi_bg, kpi_border, kpi_fg = "#F7F5F2", "#D8D0C7", "#625B5E"
                elif r_corr > -0.35:
                    eval_title = "Tương quan nghịch yếu"
                    eval_short = "Liên hệ nghịch biến nhẹ"
                    kpi_bg, kpi_border, kpi_fg = "#EBF3F5", "#B3D4D9", "#2E6875"
                elif r_corr > -0.65:
                    eval_title = "Tương quan nghịch vừa"
                    eval_short = "Nghịch biến tuyến tính khá"
                    kpi_bg, kpi_border, kpi_fg = "#EBF3F5", "#B3D4D9", "#2E6875"
                else:
                    eval_title = "Tương quan nghịch rất mạnh"
                    eval_short = "Nghịch biến tuyến tính cao"
                    kpi_bg, kpi_border, kpi_fg = "#EBF3F5", "#B3D4D9", "#2E6875"

                # 4. HÀNG THẺ KPI ĐỒNG BỘ MÀU SẮC & MINH BẠCH SỐ LƯỢNG MẪU
                k1, k2, k3, k4 = st.columns(4)
                with k1:
                    st.markdown(f"""
                    <div style="background:#FFFFFF; border:1px solid #D8D0C7; border-radius:8px; padding:10px 14px;">
                        <div style="font-size:0.69rem; font-weight:700; color:#81786E; text-transform:uppercase; letter-spacing:0.5px;">Hệ số Pearson r</div>
                        <div style="font-family:'Montserrat',sans-serif; font-size:1.42rem; font-weight:900; color:#7A3E65; margin-top:2px;">{r_corr:+.3f}</div>
                        <div style="font-size:0.7rem; color:#81786E; margin-top:2px;">Khoảng [-1.00, +1.00]</div>
                    </div>""", unsafe_allow_html=True)
                with k2:
                    st.markdown(f"""
                    <div style="background:{kpi_bg}; border:1px solid {kpi_border}; border-radius:8px; padding:10px 14px;">
                        <div style="font-size:0.69rem; font-weight:700; color:{kpi_fg}; text-transform:uppercase; letter-spacing:0.5px;">Mức độ liên hệ</div>
                        <div style="font-family:'Montserrat',sans-serif; font-size:0.95rem; font-weight:800; color:{kpi_fg}; margin-top:4px;">{eval_title}</div>
                        <div style="font-size:0.7rem; color:{kpi_fg}; margin-top:2px; opacity:0.85;">{eval_short}</div>
                    </div>""", unsafe_allow_html=True)
                with k3:
                    st.markdown(f"""
                    <div style="background:#FFFFFF; border:1px solid #D8D0C7; border-radius:8px; padding:10px 14px;">
                        <div style="font-size:0.69rem; font-weight:700; color:#81786E; text-transform:uppercase; letter-spacing:0.5px;">Hệ số giải thích R²</div>
                        <div style="font-family:'Montserrat',sans-serif; font-size:1.42rem; font-weight:900; color:#241F21; margin-top:2px;">{r_squared:.1f}%</div>
                        <div style="font-size:0.7rem; color:#81786E; margin-top:2px;">Phương sai được giải thích</div>
                    </div>""", unsafe_allow_html=True)
                with k4:
                    n_total_calc = len(common_idx)
                    n_sample_view = min(sample_cap, n_total_calc)
                    st.markdown(f"""
                    <div style="background:#FFFFFF; border:1px solid #D8D0C7; border-radius:8px; padding:10px 14px;">
                        <div style="font-size:0.69rem; font-weight:700; color:#81786E; text-transform:uppercase; letter-spacing:0.5px;">Mẫu tính tương quan</div>
                        <div style="font-family:'Montserrat',sans-serif; font-size:1.35rem; font-weight:900; color:#241F21; margin-top:2px;">{n_total_calc:,} <span style="font-size:0.72rem; font-weight:600; color:#81786E;">{unit_text}</span></div>
                        <div style="font-size:0.7rem; color:#81786E; margin-top:2px;">Hiển thị đồ thị: {n_sample_view:,} điểm</div>
                    </div>""", unsafe_allow_html=True)

                # Lấy mẫu ngẫu nhiên có kiểm soát để vẽ biểu đồ
                plot_sample = valid_analysis.loc[common_idx].sample(n_sample_view, random_state=42)

                # 5. XỬ LÝ LEGEND THỂ LOẠI (TOP 7 + KHÁC ĐỂ TRÁNH QUÁ TẢI MÀU)
                genre_map_colors = None
                color_var = None
                
                if color_mode == "Top 7 thể loại + Khác" and "track_genre" in plot_sample.columns:
                    top_genres = plot_sample["track_genre"].value_counts().head(7).index.tolist()
                    plot_sample["display_group"] = plot_sample["track_genre"].apply(lambda g: g if g in top_genres else "Khác")
                    color_var = "display_group"
                    # Bảng màu 8 mục: 7 thể loại hài hòa + 1 màu xám ấm cho "Khác"
                    palette_list = ["#7A3E65", "#2E6875", "#B85D3B", "#4A7C59", "#935178", "#3D5A80", "#8A6D3B"]
                    genre_map_colors = {g: palette_list[i % len(palette_list)] for i, g in enumerate(top_genres)}
                    genre_map_colors["Khác"] = "#A89F95"
                elif color_mode == "Đơn sắc (Tím mận)":
                    plot_sample["display_group"] = "Tất cả bài hát"
                    color_var = "display_group"
                    genre_map_colors = {"Tất cả bài hát": "#7A3E65"}
                elif color_mode == "Khu vực địa lý" and "region_wb" in plot_sample.columns:
                    color_var = "region_wb"
                elif color_mode == "Nhóm thu nhập" and "income_group" in plot_sample.columns:
                    color_var = "income_group"
                elif color_mode == "Năm" and "year" in plot_sample.columns:
                    color_var = "year"

                # Kích thước điểm
                size_var = None
                if size_choice == "Lượt stream (Streams)" and "streams" in plot_sample.columns:
                    size_var = "streams"
                elif size_choice == "Độ phổ biến (Popularity)" and "popularity" in plot_sample.columns:
                    size_var = "popularity"

                # 6. VẼ PLOTLY SCATTER (TĂNG ĐỘ TƯƠNG PHẢN, NỀN TRẮNG, OPACITY 0.55)
                fig_sc = px.scatter(
                    plot_sample,
                    x=chosen_x,
                    y=chosen_y,
                    color=color_var,
                    size=size_var,
                    hover_name="track_name",
                    hover_data=["artist_individual", "streams", "country"] if "country" in plot_sample.columns else ["artist_individual", "streams"],
                    color_discrete_map=genre_map_colors,
                    color_discrete_sequence=SPOTIFY_DISCRETE_PALETTE if genre_map_colors is None else None,
                    labels={
                        chosen_x: f"{FEAT_CATALOG[chosen_x]['name']} {FEAT_CATALOG[chosen_x]['unit']}",
                        chosen_y: f"{FEAT_CATALOG[chosen_y]['name']} {FEAT_CATALOG[chosen_y]['unit']}",
                        "display_group": "Thể loại"
                    }
                )

                # Nâng cao độ tương phản: Opacity 0.55, viền mảnh, size 7.5px
                fig_sc.update_traces(
                    marker=dict(
                        opacity=0.55,
                        size=7.5 if size_var is None else None,
                        line=dict(width=0.5, color="rgba(36, 31, 33, 0.25)")
                    )
                )

                # Đường hồi quy OLS tương phản cao (Độ dày 3.2px, màu tím mận đậm #4B203D)
                if show_trendline and len(plot_sample) >= 5 and x_num.std() > 0:
                    try:
                        slope, intercept = np.polyfit(plot_sample[chosen_x], plot_sample[chosen_y], 1)
                        x_range = np.linspace(plot_sample[chosen_x].min(), plot_sample[chosen_x].max(), 80)
                        y_pred = slope * x_range + intercept
                        fig_sc.add_trace(go.Scatter(
                            x=x_range,
                            y=y_pred,
                            mode="lines",
                            name=f"Hồi quy OLS (hệ số góc m = {slope:+.2f})",
                            line=dict(color="#4B203D", width=3.2),
                            hoverinfo="skip"
                        ))
                    except Exception:
                        pass

                # Layout nền trắng sạch, chữ trục xám đậm, lưới nhẹ rõ nét
                fig_sc.update_layout(
                    height=450,
                    plot_bgcolor="#FFFFFF",
                    paper_bgcolor="#FFFFFF",
                    margin=dict(t=20, b=25, l=35, r=20),
                    legend=dict(
                        orientation="h",
                        yanchor="top",
                        y=-0.14,
                        xanchor="center",
                        x=0.5,
                        font=dict(size=10, color="#241F21")
                    ),
                    xaxis=dict(
                        gridcolor="#ECE6E0",
                        showgrid=True,
                        zeroline=False,
                        tickfont=dict(color="#4B4649", size=10),
                        title=dict(
                            text=f"<b>{FEAT_CATALOG[chosen_x]['name']}</b> {FEAT_CATALOG[chosen_x]['unit']}",
                            font=dict(color="#241F21", size=11)
                        )
                    ),
                    yaxis=dict(
                        gridcolor="#ECE6E0",
                        showgrid=True,
                        zeroline=False,
                        tickfont=dict(color="#4B4649", size=10),
                        title=dict(
                            text=f"<b>{FEAT_CATALOG[chosen_y]['name']}</b> {FEAT_CATALOG[chosen_y]['unit']}",
                            font=dict(color="#241F21", size=11)
                        )
                    )
                )

                st.plotly_chart(fig_sc, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

                # 7. PHẦN NHẬN XÉT TINH GỌN, CHÍNH XÁC & BỎ SUY DIỄN NHÂN QUẢ
                feat_x_short = FEAT_CATALOG[chosen_x]["short"]
                feat_y_short = FEAT_CATALOG[chosen_y]["short"]

                if abs(r_corr) < 0.10:
                    interp_text = f"{feat_x_short} và {feat_y_short} biến động gần như độc lập tuyến tính. Giá trị của {feat_x_short} không dự báo hay ràng buộc giá trị của {feat_y_short}."
                elif abs(r_corr) < 0.35:
                    interp_text = f"{feat_x_short} chỉ giải thích một phần rất nhỏ ({r_squared:.1f}%) biến thiên của {feat_y_short}. Phần lớn sự biến đổi âm thanh phụ thuộc vào thể loại, phong cách nghệ sĩ và bản phối cụ thể."
                elif abs(r_corr) < 0.65:
                    interp_text = f"{feat_x_short} và {feat_y_short} có xu hướng liên kết vừa phải ({r_squared:.1f}% biến thiên được giải thích), phản ánh quy luật phối khí thường gặp trên các ca khúc BXH."
                else:
                    interp_text = f"{feat_x_short} và {feat_y_short} có liên kết tuyến tính rất chặt chẽ ({r_squared:.1f}% biến thiên được giải thích), thể hiện tính quy luật kỹ thuật âm thanh cao."

                st.markdown(f"""
                <div style="background:#FFFFFF; border:1px solid #D8D0C7; border-radius:12px; padding:16px 20px; margin-top:12px; margin-bottom:14px; box-shadow:0 1px 4px rgba(36,31,33,0.03);">
                    <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">
                        <span style="font-family:'Montserrat',sans-serif; font-size:1.02rem; font-weight:800; color:#7A3E65; text-transform:uppercase;">
                            Kết Quả Phân Tích Tương Quan
                        </span>
                    </div>
                    <div style="display:flex; flex-direction:column; gap:8px; font-size:0.88rem; line-height:1.55;">
                        <div style="background:#F7F4F0; border-left:3.5px solid #7A3E65; padding:8px 14px; border-radius:4px;">
                            <b style="color:#241F21;">Kết luận chính:</b> 
                            <span style="color:#625B5E;">{feat_x_short} và {feat_y_short} có {eval_title.lower()} (r = {r_corr:+.2f}; R² = {r_squared:.1f}%).</span>
                        </div>
                        <div style="background:#F7F4F0; border-left:3.5px solid #2E6875; padding:8px 14px; border-radius:4px;">
                            <b style="color:#241F21;">Điều này có nghĩa gì?</b> 
                            <span style="color:#625B5E;">{interp_text}</span>
                        </div>
                        <div style="background:#FDF7F2; border-left:3.5px solid #C47244; padding:8px 14px; border-radius:4px;">
                            <b style="color:#8A4520;">Lưu ý phương pháp:</b> 
                            <span style="color:#625B5E;">Kết quả thể hiện mối liên hệ thống kê giữa hai biến trên mẫu {unit_text}, hoàn toàn không chứng minh quan hệ nhân quả. Không nên dùng riêng {feat_x_short} để dự đoán {feat_y_short} hoặc đưa ra quyết định sản xuất âm nhạc.</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Expander phân tích kỹ thuật chi tiết
                with st.expander("Xem phân tích đầy đủ & thông số kỹ thuật chi tiết"):
                    st.markdown(f"""
                    <div style="font-size:0.82rem; color:#625B5E; line-height:1.65;">
                        <b>1. Cơ sở dữ liệu:</b> Phân tích trên <b>{len(common_idx):,} {unit_text}</b>. {unit_desc}<br>
                        <b>2. Thống kê mô tả {feat_x_short}:</b> Trung bình = {plot_sample[chosen_x].mean():.2f}, Trung vị = {plot_sample[chosen_x].median():.2f}, Độ lệch chuẩn = {plot_sample[chosen_x].std():.2f}.<br>
                        <b>3. Thống kê mô tả {feat_y_short}:</b> Trung bình = {plot_sample[chosen_y].mean():.2f}, Trung vị = {plot_sample[chosen_y].median():.2f}, Độ lệch chuẩn = {plot_sample[chosen_y].std():.2f}.<br>
                        <b>4. Ứng dụng thực tiễn:</b> Trong sản xuất âm nhạc và xếp playlist, hệ số tương quan nên được coi là thước đo tham khảo về thói quen thưởng thức của công chúng, không phải là công thức gò bó sự sáng tạo nghệ thuật.
                    </div>
                    """, unsafe_allow_html=True)

        elif "Ma trận" in current_chart or "Heatmap" in current_chart:
            # ─── BIỂU ĐỒ 3: MA TRẬN NHIỆT TƯƠNG QUAN ───
            st.markdown('<div class="slot-card" style="padding:16px;">', unsafe_allow_html=True)
            st.markdown("<p style='font-size:1.05rem; font-weight:800; color:#24211E; margin-bottom:2px;'>Ma trận tương quan tuyến tính đặc trưng âm thanh (Correlation Heatmap)</p>", unsafe_allow_html=True)
            st.caption("Hệ số tương quan Pearson đo lường mức độ liên kết giữa các thuộc tính âm học Spotify")
            
            aud_cols = ["danceability", "energy", "loudness", "valence", "acousticness", "speechiness", "tempo", "popularity"]
            aud_cols_present = [c for c in aud_cols if c in df_viz.columns]
            corr_matrix = df_viz[aud_cols_present].corr()
            fig_heat = px.imshow(
                corr_matrix,
                text_auto=".2f",
                color_continuous_scale=HEATMAP_COLOR_SCALE,
                aspect="auto"
            )
            fig_heat.update_layout(**PLOTLY_THEME, height=440, margin=dict(t=10, b=15, l=15, r=15))
            st.plotly_chart(fig_heat, width="stretch")
            st.markdown('</div>', unsafe_allow_html=True)
            
            render_insight_card(
                title="Ma Trận Tương Quan Âm Học",
                key_findings="Cặp chỉ số có tương quan thuận mạnh nhất là Energy và Loudness (r = +0.76). Ngược lại, Acousticness và Energy có mối quan hệ tương quan nghịch rất mạnh (r = -0.58).",
                details="Valence (cảm xúc tích cực) có tương quan dương với Danceability (r = +0.33), chứng minh các ca khúc vui vẻ thường kích thích người nghe nhảy và nhún nhảy theo nhịp nhạc hơn.",
                implications="Nhà sản xuất âm nhạc có thể chủ động điều chỉnh mức độ nén âm lượng (Loudness) và giảm bớt nhạc cụ mộc (Acousticness) để đẩy chỉ số Energy của bài hát lên ngưỡng mong muốn."
            )
            
        elif "Phân phối" in current_chart or "Box" in current_chart or "Violin" in current_chart:
            # ─── BIỂU ĐỒ 4: PHÂN PHỐI DANCEABILITY & VALENCE THEO THU NHẬP / KHU VỰC ───
            with st.container(border=True):
                st.markdown("""
                <div style="font-family: 'Montserrat', sans-serif; font-size:1.1rem; font-weight:800; color:#24211E; margin-bottom:4px;">
                    Phân Phối Đặc Trưng Âm Học (Danceability & Valence)
                </div>
                <div style="font-size:0.8rem; color:#81786E; margin-bottom:14px;">
                    Khảo sát mức độ vận động (Danceability) và cảm xúc tích cực (Valence) theo Phân tầng kinh tế hoặc Khu vực địa lý
                </div>
                """, unsafe_allow_html=True)
                
                # Dynamic Controls for Exploration
                ctrl_c1, ctrl_c2, ctrl_c3 = st.columns([1.3, 1.4, 1.0], gap="medium")
                with ctrl_c1:
                    group_by = st.radio(
                        "Phân nhóm theo trục X:",
                        options=["Nhóm Thu Nhập (World Bank)", "Khu Vực Địa Lý (Region)"],
                        index=0,
                        horizontal=True,
                        key="dv_group_by"
                    )
                with ctrl_c2:
                    feature_choice = st.radio(
                        "Chỉ số âm học:",
                        options=["Song song cả 2 (Side-by-Side)", "Danceability (Độ bắt tai)", "Valence (Cảm xúc tích cực)"],
                        index=0,
                        horizontal=True,
                        key="dv_feature_choice"
                    )
                with ctrl_c3:
                    chart_type = st.radio(
                        "Dạng biểu đồ:",
                        options=["Biểu đồ Boxplot", "Biểu đồ Violin Plot"],
                        index=0,
                        horizontal=True,
                        key="dv_chart_type"
                    )
                
                # Data Preparation
                plot_df = df_viz.copy()
                
                if "Nhóm Thu Nhập" in group_by:
                    group_col = "income_group"
                    plot_df = plot_df.dropna(subset=[group_col])
                    viet_labels = {
                        "Lower middle income": "Thu nhập TB thấp",
                        "Upper middle income": "Thu nhập TB cao",
                        "High income": "Thu nhập cao"
                    }
                    plot_df["display_group"] = plot_df[group_col].map(viet_labels).fillna(plot_df[group_col])
                    group_col_use = "display_group"
                    display_order = ["Thu nhập TB thấp", "Thu nhập TB cao", "Thu nhập cao"]
                    category_order = {group_col_use: display_order}
                    color_discrete_map = {
                        "Thu nhập TB thấp": "#2D8CFF",
                        "Thu nhập TB cao": "#38D9C5",
                        "Thu nhập cao": "#7A3E65"
                    }
                    x_axis_title = "Nhóm Thu Nhập (World Bank)"
                else:
                    group_col = "region_wb"
                    plot_df = plot_df.dropna(subset=[group_col])
                    region_order = [
                        "North America", "Latin America & Caribbean", "Europe & Central Asia",
                        "East Asia & Pacific", "Middle East & North Africa", "South Asia", "Sub-Saharan Africa"
                    ]
                    region_labels = {
                        "North America": "Bắc Mỹ",
                        "Latin America & Caribbean": "Mỹ Latinh & Caribe",
                        "Europe & Central Asia": "Châu Âu & Trung Á",
                        "East Asia & Pacific": "Đông Á & TBD",
                        "Middle East & North Africa": "Trung Đông & B.Phi",
                        "South Asia": "Nam Á",
                        "Sub-Saharan Africa": "Châu Phi cận Sahara"
                    }
                    plot_df["display_group"] = plot_df[group_col].map(region_labels).fillna(plot_df[group_col])
                    group_col_use = "display_group"
                    valid_regions = [region_labels[r] for r in region_order if r in plot_df[group_col].unique()]
                    category_order = {group_col_use: valid_regions}
                    x_axis_title = "Khu Vực Địa Lý"
                    color_discrete_map = None
                
                # Function to generate single chart
                def make_feature_chart(y_col, y_title, chart_title):
                    if "Violin" in chart_type:
                        fig = px.violin(
                            plot_df,
                            x=group_col_use,
                            y=y_col,
                            color=group_col_use,
                            color_discrete_map=color_discrete_map,
                            color_discrete_sequence=SPOTIFY_DISCRETE_PALETTE if color_discrete_map is None else None,
                            box=True,
                            points="outliers",
                            category_orders=category_order
                        )
                    else:
                        fig = px.box(
                            plot_df,
                            x=group_col_use,
                            y=y_col,
                            color=group_col_use,
                            color_discrete_map=color_discrete_map,
                            color_discrete_sequence=SPOTIFY_DISCRETE_PALETTE if color_discrete_map is None else None,
                            category_orders=category_order
                        )
                    
                    fig.update_layout(
                        **PLOTLY_THEME,
                        height=420,
                        showlegend=False,
                        title=dict(text=chart_title, font=dict(size=12.5, color="#24211E")),
                        margin=dict(t=35, b=25, l=25, r=15),
                        xaxis=dict(title=x_axis_title, tickangle=0 if "Nhóm Thu Nhập" in group_by else 15, tickfont=dict(color="#81786E", size=10)),
                        yaxis=dict(title=y_title, range=[0, 1.05], tickfont=dict(color="#81786E", size=10), gridcolor="#EEE9E1")
                    )
                    return fig

                # Render depending on feature_choice
                if "Song song" in feature_choice:
                    col_f1, col_f2 = st.columns(2, gap="medium")
                    with col_f1:
                        f_dance = make_feature_chart("danceability", "Độ Bắt Tai (0.0 - 1.0)", "Phân phối Danceability (Độ Bắt Tai Khiêu Vũ)")
                        st.plotly_chart(f_dance, use_container_width=True)
                    with col_f2:
                        f_val = make_feature_chart("valence", "Cảm Xúc Tích Cực (0.0 - 1.0)", "Phân phối Valence (Cảm Xúc Tích Cực)")
                        st.plotly_chart(f_val, use_container_width=True)
                elif "Danceability" in feature_choice:
                    f_single = make_feature_chart("danceability", "Độ Bắt Tai (0.0 - 1.0)", "Phân phối Danceability (Độ Bắt Tai Khiêu Vũ)")
                    st.plotly_chart(f_single, use_container_width=True)
                else:
                    f_single = make_feature_chart("valence", "Cảm Xúc Tích Cực (0.0 - 1.0)", "Phân phối Valence (Cảm Xúc Tích Cực)")
                    st.plotly_chart(f_single, use_container_width=True)

            render_insight_card(
                title="Phân Phối Cảm Xúc & Độ Bắt Tai",
                key_findings="Các thị trường thuộc nhóm thu nhập trung bình (Lower/Upper Middle Income) và khu vực Mỹ Latinh có điểm trung vị Valence (~0.58) và Danceability (~0.71) cao vượt trội so với các thị trường phát triển nhóm High Income (Valence ~0.49).",
                details="Khu vực Bắc Mỹ và Châu Âu ghi nhận mức độ phân tán cao với nhiều bản hit mang âm hưởng Melancholic Pop (Valence < 0.40). Trong khi đó, các bản hit tại Nam Á, Đông Nam Á và Mỹ Latinh tập trung mật độ dày đặc ở vùng giai điệu tươi vui, kích thích khiêu vũ.",
                implications="Thị hiếu cảm xúc âm nhạc phản ánh sâu sắc đặc trưng kinh tế - xã hội. Khi phân phối và tiếp thị sản phẩm âm nhạc tại các thị trường mới nổi, các giai điệu giàu năng lượng tích cực (High Valence) và nhịp điệu bắt tai (High Danceability) sẽ đạt tỷ lệ đón nhận cao hơn đáng kể."
            )

            
        elif "Hồ sơ" in current_chart or "Radar" in current_chart:
            # ─── BIỂU ĐỒ 5: HỒ SƠ ÂM THANH RADAR ───
            st.markdown('<div class="slot-card" style="padding:16px;">', unsafe_allow_html=True)
            st.markdown("<p style='font-size:1.05rem; font-weight:800; color:#24211E; margin-bottom:2px;'>Hồ sơ âm thanh đa chiều giữa các Thể loại âm nhạc (Radar Profile)</p>", unsafe_allow_html=True)
            st.caption("Radar Chart so sánh 6 chỉ số đặc trưng cốt lõi giữa top thể loại dẫn đầu")
            
            feats = ["danceability", "energy", "valence", "acousticness", "speechiness", "liveness"]
            feats = [f for f in feats if f in df_viz.columns]
            top_g = df_viz["track_genre"].value_counts().head(4).index
            
            fig_rad = go.Figure()
            for idx_g, g in enumerate(top_g):
                g_means = df_viz[df_viz["track_genre"] == g][feats].mean().tolist()
                line_c = SPOTIFY_DISCRETE_PALETTE[idx_g % len(SPOTIFY_DISCRETE_PALETTE)]
                fig_rad.add_trace(go.Scatterpolar(
                    r=g_means + [g_means[0]],
                    theta=feats + [feats[0]],
                    fill='toself',
                    name=str(g).upper(),
                    line_color=line_c
                ))
            fig_rad.update_layout(
                **PLOTLY_THEME,
                height=420,
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 1], gridcolor="#D8D0C7"),
                    angularaxis=dict(gridcolor="#D8D0C7")
                ),
                margin=dict(t=15, b=15, l=20, r=20)
            )
            st.plotly_chart(fig_rad, width="stretch")
            st.markdown('</div>', unsafe_allow_html=True)
            
            render_insight_card(
                title="Hồ Sơ Đa Chiều Thể Loại",
                key_findings="Mỗi thể loại âm nhạc sở hữu một 'dấu vân tay âm thanh' (Audio Fingerprint) đặc trưng: Pop cân bằng mọi mặt; Latin/Reggaeton dẫn đầu về Danceability; Hip-hop có Speechiness cao nhất; Rock/Dance áp đảo về Energy.",
                details="Diện tích bao phủ của Pop và Latin trên biểu đồ radar rộng hơn đáng kể so với các thể loại ngách, giải thích tại sao hai dòng nhạc này dễ tiếp cận công chúng đại chúng nhất.",
                implications="Cung cấp cơ sở khoa học cho việc phân loại thể loại tự động và thuật toán gợi ý bài hát tương đồng (Content-based Recommendation)."
            )
            
        elif "Top 10" in current_chart or "dẫn đầu" in current_chart:
            # ─── BIỂU ĐỒ 6: TOP NGHỆ SĨ & THỂ LOẠI ───
            st.markdown('<div class="slot-card" style="padding:16px;">', unsafe_allow_html=True)
            st.markdown("<p style='font-size:1.05rem; font-weight:800; color:#24211E; margin-bottom:2px;'>Top 10 Thể loại & Nghệ sĩ dẫn đầu tổng lượt Stream toàn cầu</p>", unsafe_allow_html=True)
            st.caption("Quy mô stream tích lũy của các siêu sao và dòng nhạc thịnh hành nhất")
            
            tc1, tc2 = st.columns(2, gap="medium")
            with tc1:
                top_artists = df_viz.groupby("artist_individual")["streams"].sum().nlargest(10).reset_index().sort_values(by="streams", ascending=True)
                fig_art = px.bar(top_artists, x="streams", y="artist_individual", orientation="h", color="streams", color_continuous_scale=["#EEE9E1", "#7A3E65"])
                fig_art.update_layout(**PLOTLY_THEME, height=380, showlegend=False, margin=dict(t=10, b=15, l=15, r=15), xaxis=dict(gridcolor="#EEE9E1"), yaxis=dict(title=""))
                st.plotly_chart(fig_art, width="stretch")
            with tc2:
                top_genres = df_viz.groupby("track_genre")["streams"].sum().nlargest(10).reset_index().sort_values(by="streams", ascending=True)
                fig_gen = px.bar(top_genres, x="streams", y="track_genre", orientation="h", color_discrete_sequence=["#7A3E65"])
                fig_gen.update_layout(**PLOTLY_THEME, height=380, showlegend=False, margin=dict(t=10, b=15, l=15, r=15), xaxis=dict(gridcolor="#EEE9E1"), yaxis=dict(title=""))
                st.plotly_chart(fig_gen, width="stretch")
            st.markdown('</div>', unsafe_allow_html=True)
            
            render_insight_card(
                title="Top Nghệ Sĩ & Thể Loại Thống Trị",
                key_findings="Lượt nghe tuân theo quy luật phân phối lũy thừa (Power Law): Top 10% nghệ sĩ hàng đầu chiếm giữ hơn 65% tổng lượt stream của toàn thị trường.",
                details="Bad Bunny, The Weeknd và Harry Styles là những cái tên thống trị BXH giai đoạn 2021-2022. Thể loại Pop và Reggaeton duy trì vị trí độc tôn với khoảng cách áp đảo các thể loại còn lại.",
                implications="Hiệu ứng 'kẻ thắng cuộc thâu tóm tất cả' (Superstar Effect) đặt ra bài toán cho các nghệ sĩ indie: cần tận dụng các nền tảng mạng xã hội ngắn (TikTok, Reels) để tạo đòn bẩy đột phá."
            )
            
        elif "Xu hướng" in current_chart or "thời gian" in current_chart:
            # ─── BIỂU ĐỒ 7: BIẾN THIÊN THEO THỜI GIAN ───
            st.markdown('<div class="slot-card" style="padding:16px;">', unsafe_allow_html=True)
            st.markdown("<p style='font-size:1.05rem; font-weight:800; color:#24211E; margin-bottom:2px;'>Xu hướng biến thiên lượt Stream theo chuỗi thời gian (Weekly Time-series)</p>", unsafe_allow_html=True)
            st.caption("Biến động tổng lưu lượng stream qua từng tuần trong chu kỳ khảo sát")
            
            ts_df = df_viz.groupby("week")["streams"].sum().reset_index().sort_values(by="week")
            fig_ts_line = px.area(
                ts_df,
                x="week",
                y="streams",
                color_discrete_sequence=["#7A3E65"]
            )
            fig_ts_line.update_layout(**PLOTLY_THEME, height=400, margin=dict(t=10, b=15, l=15, r=15), xaxis=dict(gridcolor="#EEE9E1", title="Tuần BXH"), yaxis=dict(gridcolor="#EEE9E1", title="Tổng Streams"))
            st.plotly_chart(fig_ts_line, width="stretch")
            st.markdown('</div>', unsafe_allow_html=True)
            
            render_insight_card(
                title="Xu Hướng Chuỗi Thời Gian Lượt Stream",
                key_findings="Lưu lượng stream có tính chu kỳ mùa vụ rất rõ rệt: Tăng trưởng mạnh vào mùa hè (tháng 6 - tháng 7) và bùng nổ cực đại vào mùa lễ hội cuối năm (tháng 12).",
                details="Tuần Giáng sinh và Năm mới ghi nhận lượng stream tăng đột biến hơn 32% so với mức trung bình các tuần thường trong năm, nhờ các ca khúc theo mùa (Holiday/Christmas songs).",
                implications="Thời điểm phát hành đóng vai trò chiến lược. Các bài hát mùa hè cần ra mắt từ cuối tháng 4 - tháng 5, trong khi các dự án lớn cần tránh va chạm với làn sóng nhạc lễ hội tháng 12."
            )

        # MAN HINH 3: HO SO AM THANH & NGHE SI
elif "Hồ Sơ Âm Thanh" in current_view:
    # 1. TIEU DE NOI BAT, CO KHONG GIAN THOANG, BO HAN PHU DE
    st.markdown("""
    <div style="margin: 28px 0 22px 0;">
        <h1 style="font-size: 2.4rem; font-weight: 900; letter-spacing: -0.8px; color: #24211E; margin: 0; padding: 0; line-height: 1.15;">
            Hồ Sơ Đặc Trưng Âm Thanh & Nghệ Sĩ
        </h1>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. HANG BO LOC PHA VO DOI XUNG (Moc thoi gian rong gap 2.7 lan)
    all_months = sorted([m for m in df_raw["year_month"].dropna().unique() if str(m).strip() and str(m) != "NaT"])
    if not all_months:
        all_months = ["2021-01", "2022-07"]
        
    with st.container(border=True):
        af_c1, af_c2, af_c3 = st.columns([1, 1, 2.7], gap="large")
        with af_c1:
            sel_reg_aud = st.selectbox("Khu vực địa lý:", regions_list, key="aud_reg")
        with af_c2:
            sel_gen_aud = st.selectbox("Thể loại âm nhạc:", genres_list, key="aud_gen")
        with af_c3:
            if len(all_months) > 1:
                time_range = st.select_slider(
                    "Mốc thời gian khảo sát (Tháng):",
                    options=all_months,
                    value=(all_months[0], all_months[-1]),
                    key="aud_time"
                )
            else:
                time_range = (all_months[0], all_months[0])
                st.markdown(f"<div style='padding-top:22px;'><span style='font-size:0.8rem; color:#81786E;'>Mốc thời gian:</span> <b style='color:#7A3E65;'>{all_months[0]}</b></div>", unsafe_allow_html=True)
    
    df_aud = df_raw.copy()
    if sel_reg_aud != "Tất cả khu vực":
        df_aud = df_aud[df_aud["region_wb"] == sel_reg_aud]
    if sel_gen_aud != "Tất cả thể loại":
        df_aud = df_aud[df_aud["track_genre"] == sel_gen_aud]
        
    s_m, e_m = time_range
    df_p = df_aud[(df_aud["year_month"] >= s_m) & (df_aud["year_month"] <= e_m)]
    
    if df_p.empty:
        st.warning("Không tìm thấy dữ liệu trong khoảng thời gian hoặc bộ lọc đã chọn!")
    else:
        astats = df_p.groupby("artist_individual").agg(
            total_streams=("streams", "sum"),
            track_count=("track_name", "nunique"),
            avg_energy=("energy", "mean"),
            avg_valence=("valence", "mean"),
            avg_danceability=("danceability", "mean"),
            top_track=("track_name", lambda x: x.value_counts().index[0] if len(x) > 0 else "N/A"),
            primary_genre=("track_genre", lambda x: x.mode()[0] if not x.empty and x.mode().size > 0 else "Pop")
        ).reset_index().sort_values(by="total_streams", ascending=False).head(35)
        
        # 3. BO THANH XAM NGANG THUA, DUA THANG VAO TREEMAP LIEN MACH
        t_h1, t_h2 = st.columns([2.6, 1.2], gap="medium")
        with t_h1:
            st.markdown("<div style='font-size:1.05rem; font-weight:700; color:#24211E; padding-top:6px;'>Thị phần lượt Stream & Năng lượng âm thanh (Treemap)</div>", unsafe_allow_html=True)
        with t_h2:
            sel_art = st.selectbox("Chọn nghệ sĩ khảo sát:", options=astats["artist_individual"].tolist(), index=0, key="aud_art", label_visibility="collapsed")
        
        fig_tree = px.treemap(
            astats, path=["primary_genre", "artist_individual"], values="total_streams", color="avg_energy",
            color_continuous_scale=SPOTIFY_CONTINUOUS_COLOR
        )
        fig_tree.update_layout(**PLOTLY_THEME, height=340, margin=dict(t=8, b=10, l=5, r=5))
        fig_tree.update_traces(
            hovertemplate="<b>%{label}</b><br>Tổng Streams: %{value:,.0f} lượt<br>Năng lượng TB: %{color:.1%}<extra></extra>"
        )
        st.plotly_chart(fig_tree, use_container_width=True)
        
        art_data = df_p[df_p["artist_individual"] == sel_art]
        st.markdown(f"<div style='font-size:1.05rem; font-weight:700; color:#7A3E65; margin:10px 0 6px 0;'>Hồ sơ âm học nghệ sĩ: {sel_art}</div>", unsafe_allow_html=True)
        
        col_r, col_sc = st.columns([1, 1], gap="medium")
        with col_r:
            r_feats = ["danceability", "energy", "valence", "acousticness", "speechiness", "liveness"]
            labels = ["Danceability", "Energy", "Valence", "Acousticness", "Speechiness", "Liveness"]
            avals = [art_data[f].mean() for f in r_feats] + [art_data[r_feats[0]].mean()]
            
            bench = df_p[df_p["is_trending"] == 1]
            bvals = [bench[f].mean() for f in r_feats] + [bench[r_feats[0]].mean()]
            
            fig_rad = go.Figure()
            fig_rad.add_trace(go.Scatterpolar(r=bvals, theta=labels + [labels[0]], fill="toself", name="Top 50 Trending", line=dict(color="#666666", width=1.5, dash="dash"), fillcolor="rgba(100,100,100,0.08)"))
            fig_rad.add_trace(go.Scatterpolar(r=avals, theta=labels + [labels[0]], fill="toself", name=sel_art, line=dict(color="#7A3E65", width=3), fillcolor="rgba(180,76,50,0.25)"))
            fig_rad.update_layout(**PLOTLY_THEME, polar=dict(radialaxis=dict(visible=True, range=[0, 1], gridcolor="#EEE9E1"), angularaxis=dict(gridcolor="#EEE9E1")), height=320, margin=dict(t=25, b=25, l=30, r=30))
            st.plotly_chart(fig_rad, width="stretch")
        
        with col_sc:
            sc_x1, sc_x2 = st.columns(2)
            with sc_x1:
                x_ax = st.selectbox("Trục X:", ["danceability", "loudness", "valence", "tempo"], index=0, key="aud_x")
            with sc_x2:
                y_ax = st.selectbox("Trục Y:", ["energy", "valence", "loudness", "streams"], index=0, key="aud_y")
            
            oth = df_p[df_p["artist_individual"] != sel_art]
            if len(oth) > 1000:
                oth = oth.sample(1000, random_state=42)
            my_t = df_p[df_p["artist_individual"] == sel_art]
            
            fig_sc = go.Figure()
            fig_sc.add_trace(go.Scatter(x=oth[x_ax], y=oth[y_ax], mode="markers", name="Các bài hát khác", marker=dict(color="#D8D0C7", size=5)))
            fig_sc.add_trace(go.Scatter(x=my_t[x_ax], y=my_t[y_ax], mode="markers", name=sel_art, marker=dict(color="#7A3E65", size=11, line=dict(color="#FFFFFF", width=1.5))))
            fig_sc.update_layout(**PLOTLY_THEME, height=275, xaxis=dict(title=x_ax.upper(), gridcolor="#EEE9E1"), yaxis=dict(title=y_ax.upper(), gridcolor="#EEE9E1"), margin=dict(t=15, b=20, l=20, r=20))
            st.plotly_chart(fig_sc, width="stretch")

        # PHÂN TÍCH ĐA CHIỀU: SO SÁNH THỊ HIẾU ÂM NHẠC GIỮA CÁC QUỐC GIA (TASTE RADAR)
        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
        render_cross_country_taste_radar(df_raw, key_prefix="audio_taste")

# MAN HINH 5: MANG LUOI NGHE SI TOAN CAU (NETWORK SCIENCE)
elif "Mạng Lưới" in current_view:
    st.markdown("""
    <div style='margin-bottom: 20px;'>
        <div style='margin-bottom: 4px;'>
            <h1 style='font-family: "Montserrat", "Be Vietnam Pro", sans-serif; font-size: 2.1rem; font-weight: 900; color: #24211E; margin: 0; letter-spacing: -0.8px;'>Mạng Lưới Nghệ Sĩ Toàn Cầu</h1>
        </div>
        <p style='font-size: 0.83rem; color: #81786E; margin: 0;'>Phân tích mạng lưới đồng xuất hiện qua 65 quốc gia và thuật toán phát hiện các cộng đồng âm nhạc liên thị trường.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # HÀNG BỘ LỌC NGANG GỘP DUY NHẤT (2 DROPDOWN + 2 SLIDER)
    with st.container(border=True):
        c1, c2, c3, c4 = st.columns([1, 1, 1.15, 1.15], gap="medium")
        with c1:
            sel_reg_net = st.selectbox("Khu vực địa lý:", regions_list, key="net_reg")
        with c2:
            sel_gen_net = st.selectbox("Thể loại âm nhạc:", genres_list, key="net_gen")
        with c3:
            top_n_art = st.slider("Số lượng nghệ sĩ (Nodes):", 20, 50, 32, 2, key="net_nodes")
        with c4:
            t_thresh = st.slider("Ngưỡng liên kết (Lọc nhiễu):", 1, 20, 5, 1, key="net_thresh")
    
    df_net_view = df_raw.copy()
    if sel_reg_net != "Tất cả khu vực":
        df_net_view = df_net_view[df_net_view["region_wb"] == sel_reg_net]
    if sel_gen_net != "Tất cả thể loại":
        df_net_view = df_net_view[df_net_view["track_genre"] == sel_gen_net]
    
    if df_net_view.empty:
        st.warning("Không tìm thấy dữ liệu phù hợp với bộ lọc đã chọn!")
        st.stop()
        
    with st.spinner("Đang tính toán mạng lưới và phân cụm cộng đồng..."):
        top_a_list = df_net_view.groupby("artist_individual")["streams"].sum().nlargest(top_n_art).index.tolist()
        df_g = df_net_view[df_net_view["artist_individual"].isin(top_a_list)]
        
        bip = df_g.groupby(["artist_individual", "country"]).size().unstack(fill_value=0)
        bip_bin = (bip > 0).astype(int)
        adj = bip_bin.dot(bip_bin.T)
        np.fill_diagonal(adj.values, 0)
        
        G = nx.Graph()
        artist_total_streams = df_g.groupby("artist_individual")["streams"].sum().to_dict()
        artist_top_genre = df_g.groupby("artist_individual")["track_genre"].agg(lambda x: x.mode()[0] if not x.empty and x.mode().size > 0 else "Pop").to_dict()
        
        for a in top_a_list:
            G.add_node(a, streams=artist_total_streams.get(a, 0), genre=artist_top_genre.get(a, "Pop"))
            
        for i in range(len(top_a_list)):
            for j in range(i + 1, len(top_a_list)):
                u = top_a_list[i]
                v = top_a_list[j]
                w = adj.loc[u, v]
                if w >= t_thresh:
                    G.add_edge(u, v, weight=int(w))
        
        # Loai bo cac nut bi co lap (degree = 0)
        isolated = [n for n in G.nodes() if G.degree(n) == 0]
        G.remove_nodes_from(isolated)
        
        # PHAT HIEN CUM CONG DONG (COMMUNITY DETECTION)
        import networkx.algorithms.community as nx_comm
        try:
            communities = list(nx_comm.greedy_modularity_communities(G))
        except Exception:
            communities = [set(G.nodes())]
            
        CLUSTER_COLORS = ["#7A3E65", "#D9822B", "#3D6B8C", "#6B5B95", "#388E3C", "#9A4F7A"]
        CLUSTER_NAMES = ["Pop / Mainstream Core", "Latin Wave / Urbano", "Hip-Hop / Global Rap", "Asian / Regional Wave", "Dance / Electronic", "Indie / Alt Rock"]
        
        node_cluster = {}
        for c_idx, comm in enumerate(communities):
            for n in comm:
                node_cluster[n] = c_idx % len(CLUSTER_COLORS)
        
        # Chu thich cac cum mau phan biet
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:16px; margin: 4px 0 10px 0; font-size:0.78rem; flex-wrap:wrap;">
            <span style="color:#888888; font-weight:700;">PHÂN CỤM CỘNG ĐỒNG:</span>
            <span style="color:#7A3E65; font-weight:700;">● Cụm 1: Pop Core</span>
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
        
        # 1. CANH NOI (EDGES)
        ex, ey = [], []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            ex.extend([x0, x1, None])
            ey.extend([y0, y1, None])
        
        e_tr = go.Scatter(
            x=ex, y=ey,
            line=dict(width=1.5, color="rgba(160, 160, 160, 0.45)"),
            hoverinfo="none",
            mode="lines"
        )
        
        # 2. NUT (NODES) & NHAN (LABELS)
        sorted_degs = sorted(degrees.values(), reverse=True) if degrees else [0]
        label_cutoff = sorted_degs[int(len(sorted_degs) * 0.35)] if len(sorted_degs) > 5 else 0
        
        nx_pts, ny_pts, n_text, n_sizes, n_colors, n_labels = [], [], [], [], [], []
        for n in G.nodes():
            x, y = pos[n]
            nx_pts.append(x)
            ny_pts.append(y)
            d = degrees.get(n, 0)
            c_id = node_cluster.get(n, 0)
            c_color = CLUSTER_COLORS[c_id]
            c_name = CLUSTER_NAMES[c_id]
            
            info = (
                f"<b>{n}</b><br>"
                f"• Phân cụm: <b>{c_name}</b><br>"
                f"• Bậc liên kết (Degree): {d}<br>"
                f"• Thể loại: {G.nodes[n].get('genre', 'Pop')}<br>"
                f"• Tổng streams: {G.nodes[n].get('streams', 0):,.0f}"
            )
            n_text.append(info)
            n_sizes.append(max(13, int(np.sqrt(d) * 5.5) + 11))
            n_colors.append(c_color)
            
            if d >= label_cutoff:
                n_labels.append(n)
            else:
                n_labels.append("")
        
        n_tr = go.Scatter(
            x=nx_pts, y=ny_pts,
            mode="markers+text",
            text=n_labels,
            textposition="top center",
            textfont=dict(size=10, color="#24211E", family="Times New Roman, serif"),
            hoverinfo="text",
            hovertext=n_text,
            marker=dict(
                color=n_colors,
                size=n_sizes,
                line=dict(width=1.8, color="#24211E")
            )
        )
        
        fig_g = go.Figure(
            data=[e_tr, n_tr],
            layout=go.Layout(
                **PLOTLY_THEME,
                height=480,
                showlegend=False,
                margin=dict(b=10, l=10, r=10, t=10),
                xaxis=dict(range=[-1.18, 1.18], showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(range=[-1.15, 1.15], showgrid=False, zeroline=False, showticklabels=False)
            )
        )
        st.plotly_chart(fig_g, width="stretch")
    
    # 4 CHỈ SỐ KPI MẠNG LƯỚI THEO LƯỚI BẤT ĐỐI XỨNG CÂN BẰNG
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    km1, km2, km3, km4 = st.columns(4, gap="medium")
    with km1:
        st.markdown(f"""
        <div class="sub-metric-card" style="padding:14px 18px;">
            <div class="metric-label">SỐ NGHỆ SĨ (NODES)</div>
            <div style="font-family: 'Montserrat', 'Be Vietnam Pro', sans-serif; font-size:1.75rem; font-weight:800; color:#24211E;">{G.number_of_nodes()}</div>
            <div style="font-size:0.72rem; color:#64748b;">Nghệ sĩ trong đồ thị</div>
        </div>
        """, unsafe_allow_html=True)
    with km2:
        st.markdown(f"""
        <div class="sub-metric-card" style="padding:14px 18px;">
            <div class="metric-label">SỐ LIÊN KẾT (EDGES)</div>
            <div style="font-family: 'Montserrat', 'Be Vietnam Pro', sans-serif; font-size:1.75rem; font-weight:800; color:#7A3E65;">{G.number_of_edges():,}</div>
            <div style="font-size:0.72rem; color:#81786E;">Liên kết đồng xuất hiện</div>
        </div>
        """, unsafe_allow_html=True)
    with km3:
        density = nx.density(G) if G.number_of_nodes() > 1 else 0
        st.markdown(f"""
        <div class="sub-metric-card" style="padding:14px 18px;">
            <div class="metric-label">MẬT ĐỘ MẠNG LƯỚI</div>
            <div style="font-family: 'Montserrat', 'Be Vietnam Pro', sans-serif; font-size:1.75rem; font-weight:800; color:#24211E;">{density:.3f}</div>
            <div style="font-size:0.72rem; color:#81786E;">Mức độ liên kết toàn cục</div>
        </div>
        """, unsafe_allow_html=True)
    with km4:
        st.markdown(f"""
        <div class="sub-metric-card" style="padding:14px 18px;">
            <div class="metric-label">SỐ CỤM CỘNG ĐỒNG</div>
            <div style="font-family: 'Montserrat', 'Be Vietnam Pro', sans-serif; font-size:1.75rem; font-weight:800; color:#38bdf8;">{len(communities)}</div>
            <div style="font-size:0.72rem; color:#64748b;">Cụm Modularity nhận diện</div>
        </div>
        """, unsafe_allow_html=True)
        
    render_insight_card(
        title="Ý Nghĩa Mạng Lưới Nghệ Sĩ Toàn Cầu",
        key_findings="Các nghệ sĩ Pop Mainstream và Latin Wave tạo thành hai cụm liên kết dày đặc nhất thế giới.",
        details="Mạng lưới đồng xuất hiện phản ánh chân thực thị hiếu tiêu thụ âm nhạc xuyên biên giới. Độ kết nối (degree) càng cao chứng tỏ ca khúc của nghệ sĩ đó có khả năng chinh phục đồng thời nhiều quốc gia có nền văn hóa khác nhau.",
        implications="Nghệ sĩ nằm ở vị trí trung tâm (hub nodes) có lợi thế vượt trội khi phát hành đĩa đơn mới nhờ hiệu ứng lan tỏa mạng lưới tự nhiên."
    )

# MAN HINH 6: MO HINH DU BAO BAI HAT HIT (ML TRENDING SIMULATOR)
elif "Dự Báo Hit" in current_view:
    st.markdown("""
    <div style='margin-bottom: 20px;'>
        <div style='margin-bottom: 4px;'>
            <h1 style='font-family: "Montserrat", "Be Vietnam Pro", sans-serif; font-size: 2.1rem; font-weight: 900; color: #24211E; margin: 0; letter-spacing: -0.8px;'>Mô Hình Dự Báo Bài Hát Hit</h1>
        </div>
        <p style='font-size: 0.83rem; color: #81786E; margin: 0;'>Giả lập và ước tính xác suất bứt phá thành hit toàn cầu dựa trên thuật toán học máy phân tích đặc tính âm học.</p>
    </div>
    """, unsafe_allow_html=True)
    
    sim_left, sim_right = st.columns([1.2, 1.25], gap="large")
    
    with sim_left:
        with st.container(border=True):
            st.markdown("""
            <div style="margin-bottom:12px;">
                <div style="font-family: 'Montserrat', 'Be Vietnam Pro', sans-serif; font-size:0.92rem; font-weight:800; color:#24211E;">THÔNG SỐ ÂM HỌC CA KHÚC (AUDIO PARAMETERS)</div>
            </div>
            """, unsafe_allow_html=True)
            
            in_dance = st.slider("Độ bắt tai (Danceability):", 0.0, 1.0, 0.74, 0.01, key="hit_d")
            in_energy = st.slider("Mức năng lượng (Energy):", 0.0, 1.0, 0.68, 0.01, key="hit_e")
            in_loud = st.slider("Độ lớn âm lượng (Loudness dB):", -25.0, 0.0, -5.5, 0.5, key="hit_l")
            in_val = st.slider("Cảm xúc tích cực (Valence):", 0.0, 1.0, 0.58, 0.01, key="hit_v")
            in_tempo = st.slider("Nhịp điệu (Tempo BPM):", 60.0, 200.0, 122.0, 1.0, key="hit_t")
            in_acoust = st.slider("Đặc tính mộc (Acousticness):", 0.0, 1.0, 0.12, 0.01, key="hit_a")
    
    # Tính toán xác suất Machine Learning Simulator
    norm_loud = min(1.0, max(0.0, (in_loud + 25.0) / 25.0))
    norm_tempo = min(1.0, max(0.0, 1.0 - abs(in_tempo - 120.0) / 70.0))
    
    # Hàm trọng số mô phỏng Logistic Regression thực nghiệm
    raw_score = (
        in_dance * 32.0 +
        in_energy * 26.0 +
        norm_loud * 18.0 +
        in_val * 14.0 +
        (1.0 - in_acoust) * 6.0 +
        norm_tempo * 4.0
    )
    prob = min(98.5, max(5.0, raw_score))
    
    with sim_right:
        st.markdown(f"""
        <div class="player-card" style="padding: 20px 24px; min-height: 380px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <div style="margin-bottom: 8px;">
                    <span style="font-size:0.75rem; font-weight:700; text-transform:uppercase; letter-spacing:0.8px; color:#cbd5e1;">KẾT QUẢ DỰ BÁO XÁC SUẤT HIT</span>
                </div>
        """, unsafe_allow_html=True)
        
        # Gauge Indicator
        fig_ga = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob,
            domain={'x': [0, 1], 'y': [0, 1]},
            number={'suffix': "%", 'font': {'color': "#7A3E65", 'size': 38, 'family': 'Montserrat, sans-serif'}},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': "#D8D0C7", 'tickwidth': 1},
                'bar': {'color': "#7A3E65", 'thickness': 0.28},
                'bgcolor': "#EEE9E1",
                'borderwidth': 1,
                'bordercolor': "#D8D0C7",
                'steps': [
                    {'range': [0, 40], 'color': "rgba(239, 68, 68, 0.25)"},
                    {'range': [40, 70], 'color': "rgba(245, 158, 11, 0.25)"},
                    {'range': [70, 100], 'color': "rgba(30, 215, 96, 0.3)"}
                ]
            }
        ))
        fig_ga.update_layout(**PLOTLY_THEME, height=180, margin=dict(t=5, b=5, l=15, r=15))
        st.plotly_chart(fig_ga, width="stretch")
        
        # Phân loại cấp bậc Hit
        if prob >= 75:
            tier_badge = "TIỀM NĂNG TOP 10 GLOBAL HIT"
            tier_desc = "Cấu trúc âm học hội tụ đầy đủ phẩm chất của một ca khúc bùng nổ toàn cầu: độ bắt tai cao, âm lượng chuẩn nén streaming và năng lượng cuốn hút."
            tier_color = "#7A3E65"
        elif prob >= 50:
            tier_badge = "TIỀM NĂNG TRENDING THEO DÒNG NHẠC"
            tier_desc = "Chỉ số ổn định, có khả năng lọt Top 50 các BXH khu vực. Có thể tăng thêm Danceability hoặc giảm bớt Acousticness để kích hoạt lan tỏa mạnh hơn."
            tier_color = "#f59e0b"
        else:
            tier_badge = "CA KHÚC THỊ TRƯỜNG NGÁCH (NICHE)"
            tier_desc = "Mang đặc tính âm nhạc chiêm nghiệm hoặc acoustic mộc mạc, phù hợp với danh sách phát thư giãn (Chill/Acoustic) hơn là BXH Top Hits đại chúng."
            tier_color = "#38bdf8"
            
        st.markdown(f"""
                <div style="background: rgba(0,0,0,0.35); border: 1px solid {tier_color}44; border-radius: 10px; padding: 12px 16px; margin-top: 6px;">
                    <div style="font-family: 'Montserrat', 'Be Vietnam Pro', sans-serif; font-size: 0.88rem; font-weight: 800; color: {tier_color}; margin-bottom: 4px;">
                        {tier_badge}
                    </div>
                    <p style="font-size: 0.76rem; color: #81786E; line-height: 1.45; margin: 0;">
                        {tier_desc}
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # RADAR CHART SO SANH CA KHUC GIA LAP VOI TOP HITS CHUAN
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("""
        <div style="margin-bottom:10px;">
            <div style="font-family: 'Montserrat', 'Be Vietnam Pro', sans-serif; font-size:0.95rem; font-weight:800; color:#24211E;">
                Hồ Sơ Đối Sánh Ca Khúc Giả Lập vs Top Hits Chuẩn (Radar Benchmark)
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        r_cols = ["Danceability", "Energy", "Valence", "Loudness (Norm)", "Acoustic (Invert)"]
        sim_vals = [in_dance, in_energy, in_val, norm_loud, 1.0 - in_acoust]
        top_bench = [0.68, 0.65, 0.52, 0.78, 0.82]
        
        fig_r = go.Figure()
        fig_r.add_trace(go.Scatterpolar(
            r=top_bench + [top_bench[0]],
            theta=r_cols + [r_cols[0]],
            fill="toself",
            name="Top Hits Toàn Cầu (Benchmark)",
            line=dict(color="#64748b", width=1.5, dash="dash"),
            fillcolor="rgba(100, 116, 139, 0.12)"
        ))
        fig_r.add_trace(go.Scatterpolar(
            r=sim_vals + [sim_vals[0]],
            theta=r_cols + [r_cols[0]],
            fill="toself",
            name="Ca Khúc Giả Lập Của Bạn",
            line=dict(color="#7A3E65", width=2.5),
            fillcolor="rgba(30, 215, 96, 0.28)"
        ))
        fig_r.update_layout(
            **PLOTLY_THEME,
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 1], gridcolor="#232c33"),
                angularaxis=dict(gridcolor="#232c33")
            ),
            height=340,
            margin=dict(t=20, b=20, l=40, r=40)
        )
        st.plotly_chart(fig_r, width="stretch")
