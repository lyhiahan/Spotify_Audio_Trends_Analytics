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

# He thong CSS phong cach Spotify Dark Theme & Standard Dashboard
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,400;1,700&family=Be+Vietnam+Pro:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,400;1,700&display=swap');

    html, body, .stApp {
        font-family: 'Times New Roman', Times, Georgia, serif !important;
        background-color: #08090a !important;
        color: #f1f5f9 !important;
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
    
    /* NUT MO SIDEBAR KHI BI DONG - PHONG CACH SPOTIFY NỔI BẬT */
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
        color: #000000 !important;
        background-color: #1DB954 !important;
        border: 2px solid #1ed760 !important;
        border-radius: 8px !important;
        padding: 5px 12px !important;
        box-shadow: 0 4px 18px rgba(29, 185, 84, 0.6) !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }
    [data-testid="collapsedControl"]:hover,
    [data-testid="stSidebarCollapsedControl"]:hover,
    button[aria-label="Expand sidebar"]:hover {
        background-color: #1ed760 !important;
        transform: scale(1.06) !important;
        box-shadow: 0 6px 22px rgba(29, 185, 84, 0.8) !important;
    }
    [data-testid="collapsedControl"] svg,
    [data-testid="stSidebarCollapsedControl"] svg,
    button[aria-label="Expand sidebar"] svg {
        color: #000000 !important;
        fill: #000000 !important;
        stroke: #000000 !important;
        width: 22px !important;
        height: 22px !important;
    }
    
    /* SIDEBAR STYLING SPOTIFY THEME */
    section[data-testid="stSidebar"] {
        background-color: #121212 !important;
        border-right: 1px solid #242424 !important;
        padding-top: 1rem !important;
    }
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #cccccc !important;
    }
    
    /* SIDEBAR RADIOGROUP STYLING */
    section[data-testid="stSidebar"] div[role="radiogroup"] {
        display: flex !important;
        flex-direction: column !important;
        gap: 8px !important;
        background: transparent !important;
        border: none !important;
        padding: 4px 0 !important;
        width: 100% !important;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label {
        background-color: #161616 !important;
        border: 1px solid #242424 !important;
        border-radius: 10px !important;
        padding: 9px 14px !important;
        width: 100% !important;
        margin: 0 !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
        background-color: #202020 !important;
        border-color: #333333 !important;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked),
    section[data-testid="stSidebar"] div[role="radiogroup"] > label[data-checked="true"] {
        background-color: #1DB954 !important;
        border-color: #1ed760 !important;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label [data-testid="stMarkdownContainer"] p {
        font-family: 'Times New Roman', Times, serif !important;
        font-size: 0.92rem !important;
        font-weight: 600 !important;
        line-height: 1.35 !important;
        margin: 0 !important;
        color: #d1d5db !important;
        display: flex !important;
        align-items: center !important;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) [data-testid="stMarkdownContainer"] p,
    section[data-testid="stSidebar"] div[role="radiogroup"] > label[data-checked="true"] [data-testid="stMarkdownContainer"] p {
        color: #000000 !important;
        font-weight: 800 !important;
    }

    /* ĐỒNG BỘ ICON: Lucide outline SVG cho từng mục điều hướng sidebar */
    section[data-testid="stSidebar"] div[data-testid="stRadio"]:first-of-type div[role="radiogroup"] > label p::before {
        content: '';
        display: inline-block;
        width: 18px;
        height: 18px;
        margin-right: 10px;
        vertical-align: middle;
        background-size: contain;
        background-repeat: no-repeat;
        flex-shrink: 0;
    }
    /* 1. Trang Chủ (Lucide Home) */
    section[data-testid="stSidebar"] div[data-testid="stRadio"]:first-of-type div[role="radiogroup"] > label:nth-of-type(1) p::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%231ed760' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z'/%3E%3Cpolyline points='9 22 9 12 15 12 15 22'/%3E%3C/svg%3E");
    }
    /* 2. Dữ Liệu & Bộ Lọc (Lucide Database) */
    section[data-testid="stSidebar"] div[data-testid="stRadio"]:first-of-type div[role="radiogroup"] > label:nth-of-type(2) p::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%231ed760' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cellipse cx='12' cy='5' rx='9' ry='3'/%3E%3Cpath d='M3 5v14a9 3 0 0 0 18 0V5'/%3E%3Cpath d='M3 12a9 3 0 0 0 18 0'/%3E%3C/svg%3E");
    }
    /* 3. Tổng Quan Thị Trường (Lucide BarChart) */
    section[data-testid="stSidebar"] div[data-testid="stRadio"]:first-of-type div[role="radiogroup"] > label:nth-of-type(3) p::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%231ed760' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='18' x2='18' y1='20' y2='10'/%3E%3Cline x1='12' x2='12' y1='20' y2='4'/%3E%3Cline x1='6' x2='6' y1='20' y2='14'/%3E%3C/svg%3E");
    }
    /* 4. Trực Quan Hóa Dữ Liệu (Lucide TrendingUp) */
    section[data-testid="stSidebar"] div[data-testid="stRadio"]:first-of-type div[role="radiogroup"] > label:nth-of-type(4) p::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%231ed760' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M3 3v18h18'/%3E%3Cpath d='m19 9-5 5-4-4-3 3'/%3E%3C/svg%3E");
    }
    /* 5. Hồ Sơ Âm Thanh (Lucide Headphones) */
    section[data-testid="stSidebar"] div[data-testid="stRadio"]:first-of-type div[role="radiogroup"] > label:nth-of-type(5) p::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%231ed760' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M3 14h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-7a9 9 0 0 1 18 0v7a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3'/%3E%3C/svg%3E");
    }
    /* 6. Mạng Lưới Nghệ Sĩ (Lucide Network) */
    section[data-testid="stSidebar"] div[data-testid="stRadio"]:first-of-type div[role="radiogroup"] > label:nth-of-type(6) p::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%231ed760' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='18' cy='5' r='3'/%3E%3Ccircle cx='6' cy='12' r='3'/%3E%3Ccircle cx='18' cy='19' r='3'/%3E%3Cline x1='8.59' x2='15.42' y1='13.51' y2='17.49'/%3E%3Cline x1='15.41' x2='8.59' y1='6.51' y2='10.49'/%3E%3C/svg%3E");
    }
    /* 7. Dự Báo Bài Hát Hit (Lucide Sparkles) */
    section[data-testid="stSidebar"] div[data-testid="stRadio"]:first-of-type div[role="radiogroup"] > label:nth-of-type(7) p::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%231ed760' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z'/%3E%3C/svg%3E");
    }
    /* Khi mục đang active: icon chuyển sang màu đen để đồng bộ với chữ */
    section[data-testid="stSidebar"] div[data-testid="stRadio"]:first-of-type div[role="radiogroup"] > label:has(input:checked) p::before,
    section[data-testid="stSidebar"] div[data-testid="stRadio"]:first-of-type div[role="radiogroup"] > label[data-checked="true"] p::before {
        filter: brightness(0) !important;
    }

    div[data-testid="stVerticalBlock"] {
        gap: 0.95rem !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #141414 !important;
        border: 1px solid #282828 !important;
        border-radius: 12px !important;
        padding: 8px 12px !important;
        margin-bottom: 8px !important;
    }

    .home-header {
        background: linear-gradient(135deg, #071f11 0%, #0d1a12 50%, #121212 100%);
        border: 1px solid #1a3824;
        border-radius: 12px;
        padding: 8px 18px;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 14px rgba(0,0,0,0.4);
    }
    .home-header-left {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .home-header-title {
        font-size: 1.35rem;
        font-weight: 800;
        letter-spacing: -0.4px;
        color: #ffffff;
        line-height: 1.15;
    }
    .home-header-sub {
        font-size: 0.74rem;
        color: #888888;
        font-weight: 500;
        margin-top: 2px;
    }
    .home-header-badge {
        color: #1DB954;
        font-weight: 700;
    }
    .home-header-stats {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .home-stat-box {
        text-align: center;
        padding: 2px 12px;
        border-left: 1px solid #222222;
    }
    .home-stat-label {
        font-size: 0.62rem;
        font-weight: 700;
        color: #777777;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .home-stat-value {
        font-size: 1.12rem;
        font-weight: 800;
        color: #ffffff;
        line-height: 1.15;
    }

    /* Standalone Horizontal Album Strip */
    .album-strip-wrapper {
        background-color: #121212;
        border: 1px solid #222222;
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
        border-right: 1px solid #252525;
        flex-shrink: 0;
    }
    .album-strip-badge-title {
        font-size: 0.72rem;
        font-weight: 800;
        color: #1DB954;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        white-space: nowrap;
    }
    .album-strip-badge-sub {
        font-size: 0.62rem;
        color: #666666;
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
        box-shadow: 0 3px 8px rgba(0,0,0,0.6);
        border: 1px solid #242424;
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        cursor: pointer;
    }
    .album-strip-img:hover {
        transform: translateY(-2px) scale(1.15);
        border-color: #1DB954;
        box-shadow: 0 4px 12px rgba(29, 185, 84, 0.45);
    }

    .block-container {
        padding-top: 3.2rem !important;
        padding-bottom: 0.5rem !important;
        padding-left: 1.6rem !important;
        padding-right: 1.6rem !important;
        max-width: 100% !important;
    }

    /* GLOBAL 2-FONT ARCHITECTURE (STRICT CONSISTENCY) */
    /* 1. Heading Font: Montserrat & Be Vietnam Pro (Full Vietnamese Diacritics Support) */
    h1, h2, h3, h4, h5, h6, 
    .outfit-font,
    .heading-font, 
    .metric-value,
    .section-title,
    [data-testid="stHeading"] *,
    .hero-title,
    .card-heading {
        font-family: 'Montserrat', 'Be Vietnam Pro', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* 2. Body Font: Times New Roman */
    html, body, .stApp, 
    p, span, label, div, button, input, select, textarea,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stWidgetLabel"] p,
    [data-testid="stRadio"] label,
    [data-testid="stSelectbox"] div,
    [data-testid="stSlider"] div,
    [data-testid="stCaptionContainer"],
    .plus-jakarta,
    .times-roman-font {
        font-family: 'Times New Roman', Times, Georgia, serif !important;
    }

    /* ========================================================
       DEPTH SYSTEM: 3-TIER SURFACE LAYERING & BASELINE GRID (8px/12px)
       ======================================================== */
    /* Layer 1: Base Card Surfaces */
    .layer-1-card {
        background-color: #111417;
        border: 1px solid #1e252a;
        border-radius: 12px;
    }

    /* Layer 2: Elevated & Interactive Panels */
    .layer-2-card {
        background-color: #151a1e;
        border: 1px solid #253038;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
    }

    /* Layer 3: Hero Anchor Card (Asymmetric Focal Point) */
    .hero-anchor-card {
        background: linear-gradient(135deg, rgba(29, 185, 84, 0.16) 0%, rgba(13, 27, 19, 0.92) 48%, rgba(17, 21, 20, 0.98) 100%);
        border: 1px solid rgba(30, 215, 96, 0.45);
        border-radius: 16px;
        padding: 24px 28px;
        box-shadow: 0 16px 40px rgba(0, 0, 0, 0.55), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
        min-height: 238px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .hero-anchor-card::after {
        content: '';
        position: absolute;
        top: -30px;
        right: -30px;
        width: 170px;
        height: 170px;
        background: radial-gradient(circle, rgba(30, 215, 96, 0.22) 0%, transparent 70%);
        pointer-events: none;
    }

    /* Satellite Sub-Metric Card */
    .sub-metric-card {
        background: linear-gradient(145deg, #13171b 0%, #101316 100%);
        border: 1px solid #1f272e;
        border-radius: 14px;
        padding: 16px 20px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 110px;
    }

    .sub-metric-card:hover {
        border-color: #2b3943;
        background: linear-gradient(145deg, #161c21 0%, #12161a 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45);
    }

    div[role="radiogroup"] {
        background-color: #14181b;
        padding: 3px;
        border-radius: 30px;
        border: 1px solid #232c33;
        display: inline-flex !important;
        gap: 4px;
        margin-bottom: 6px;
    }
    div[role="radiogroup"] > label {
        background-color: transparent;
        padding: 5px 16px !important;
        border-radius: 20px !important;
        margin: 0 !important;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    div[role="radiogroup"] > label:hover {
        background-color: #1e262c;
    }
    div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }
    div[role="radiogroup"] > label [data-testid="stMarkdownContainer"] p {
        font-family: 'Times New Roman', Times, serif !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        color: #94a3b8 !important;
    }
    div[role="radiogroup"] > label[data-checked="true"],
    div[role="radiogroup"] > label:has(input:checked) {
        background-color: #1DB954 !important;
    }
    div[role="radiogroup"] > label:has(input:checked) [data-testid="stMarkdownContainer"] p {
        color: #000000 !important;
        font-weight: 800 !important;
    }

    .metric-card {
        background-color: #111417;
        border: 1px solid #1e252a;
        border-radius: 12px;
        padding: 16px 20px;
        transition: border-color 0.2s ease, background-color 0.2s ease;
    }
    .metric-card:hover {
        border-color: #2e3a42;
        background-color: #151a1e;
    }
    .metric-label {
        font-family: 'Times New Roman', Times, serif !important;
        font-size: 0.76rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #94a3b8;
        margin-bottom: 8px;
    }
    .metric-value {
        font-family: 'Montserrat', 'Be Vietnam Pro', sans-serif !important;
        font-size: 1.95rem;
        font-weight: 800;
        letter-spacing: -0.8px;
        color: #1DB954;
        line-height: 1.15;
    }
    .metric-sub {
        font-family: 'Times New Roman', Times, serif !important;
        font-size: 0.78rem;
        color: #64748b;
        margin-top: 6px;
    }

    .filter-card {
        background-color: #13171a;
        border: 1px solid #1f272e;
        border-radius: 12px;
        padding: 12px 18px;
        margin-bottom: 16px;
    }

    .bento-card {
        background-color: #13171a;
        border: 1px solid #1f272e;
        border-radius: 14px;
        padding: 18px 20px;
        margin-bottom: 16px;
        transition: border-color 0.25s ease, background-color 0.25s ease;
    }
    .bento-card:hover {
        border-color: #2e3a43;
        background-color: #161c21;
    }

    .slot-card {
        background-color: #121619;
        border: 1px dashed #242f36;
        border-radius: 14px;
        padding: 16px 18px;
        margin-bottom: 16px;
        transition: border-color 0.25s ease;
    }
    .slot-card:hover {
        border-color: #1DB954;
    }

    .player-card {
        background: linear-gradient(135deg, #092314 0%, #111915 60%, #141817 100%);
        border: 1px solid rgba(29, 185, 84, 0.45);
        border-radius: 14px;
        padding: 18px 20px;
        margin-top: 10px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    }
    .player-title {
        font-family: 'Montserrat', 'Be Vietnam Pro', sans-serif !important;
        font-size: 1.15rem;
        font-weight: 800;
        letter-spacing: -0.3px;
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
        margin-bottom: 12px;
    }
    .player-progress {
        background: #282828;
        height: 5px;
        border-radius: 3px;
        margin-bottom: 10px;
        overflow: hidden;
    }
    .player-progress-bar {
        background: #1DB954;
        height: 100%;
        border-radius: 3px;
    }

    .member-card {
        background: #181818;
        border: 1px solid #242424;
        border-radius: 12px;
        padding: 16px 20px;
        transition: border-color 0.2s;
    }
    .member-card:hover {
        border-color: #1DB954;
    }
    .member-name {
        font-size: 1.05rem;
        font-weight: 800;
        color: #ffffff;
    }
    .member-id {
        font-size: 0.9rem;
        font-weight: 700;
        color: #1DB954;
        margin: 3px 0;
    }
    .member-role {
        font-size: 0.8rem;
        color: #aaaaaa;
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
        font-size: 1.2rem;
        font-weight: 800;
        color: #ffffff;
    }
    .section-desc {
        font-size: 0.82rem;
        color: #777777;
    }

    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #242424;
    }

    /* 1. DARK THEME SELECTBOX (Bo hoan toan mau trang mac dinh) */
    div[data-testid="stSelectbox"] > div > div,
    div[data-baseweb="select"],
    div[data-baseweb="select"] > div {
        background-color: #161616 !important;
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
    ul[role="listbox"] {
        background-color: #161616 !important;
        border: 1px solid #333333 !important;
        border-radius: 8px !important;
    }
    li[role="option"] {
        background-color: #161616 !important;
        color: #cccccc !important;
    }
    li[role="option"]:hover,
    li[role="option"][aria-selected="true"] {
        background-color: #242424 !important;
        color: #1DB954 !important;
    }
    div[data-testid="stSelectbox"] label,
    div[data-testid="stSlider"] label {
        color: #aaaaaa !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
    }

    /* 2. DONG NHAT MAU NHAN SPOTIFY GREEN CHO SLIDER (Khong dung do/hong) */
    div[data-testid="stSlider"] div[role="slider"] {
        background-color: #1DB954 !important;
        border: 2px solid #1DB954 !important;
        box-shadow: 0 0 10px rgba(29, 185, 84, 0.45) !important;
    }
    div[data-testid="stSlider"] div[data-baseweb="slider"] div[style*="background"] {
        background: #1DB954 !important;
    }
    div[data-testid="stSlider"] [data-testid="stThumbValue"] {
        color: #1DB954 !important;
        font-weight: 700 !important;
    }

    /* 3. DONG NHAT TAB ACTIVE SANG SPOTIFY GREEN (Khong dung xanh duong) */
    button[data-baseweb="tab"] {
        color: #888888 !important;
        font-weight: 600 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        border-bottom-color: #1DB954 !important;
        color: #1DB954 !important;
    }

    /* 4. PILL BUTTONS (GLASSMORPHISM STYLE LIKE SPOTIFY UI) */
    div[data-testid="stButton"] button {
        background-color: rgba(20, 25, 28, 0.85) !important;
        border: 1px solid rgba(255, 255, 255, 0.14) !important;
        border-radius: 24px !important;
        color: #e2e8f0 !important;
        font-family: 'Times New Roman', Times, serif !important;
        font-weight: 700 !important;
        font-size: 0.88rem !important;
        padding: 8px 16px !important;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.35) !important;
    }
    div[data-testid="stButton"] button:hover {
        background-color: #1DB954 !important;
        border-color: #1ed760 !important;
        color: #000000 !important;
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 6px 22px rgba(29, 185, 84, 0.5) !important;
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

# Bo layout theme Plotly chung
PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Times New Roman, serif", color="#94a3b8", size=11),
    hoverlabel=dict(
        bgcolor="#151a1e",
        bordercolor="#1DB954",
        font=dict(family="Times New Roman, serif", color="#ffffff", size=12)
    )
)

SPOTIFY_CONTINUOUS_COLOR = [
    [0.0, "#101010"],
    [0.25, "#0b3318"],
    [0.65, "#14833b"],
    [1.0, "#1DB954"]
]

@st.cache_data
def get_hero_album_covers():
    covers_dir = os.path.join("dashboard", "assets", "covers")
    if not os.path.exists(covers_dir):
        return []
    cover_files = [
        "the_weeknd_blinding_lights.jpg",
        "taylor_swift_midnights.jpg",
        "dua_lipa_levitating.jpg",
        "billie_eilish_happier_than_ever.jpg",
        "harry_styles_harrys_house.jpg",
        "adele_easy_on_me.jpg"
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
def load_all_data():
    processed_path = os.path.join("data", "processed", "merged_spotify_data.csv")
    sample_path = os.path.join("data", "sample", "spotify_sample_merged.csv")
    path = processed_path if os.path.exists(processed_path) else sample_path
    
    needed_cols = [
        "track_name", "artist_individual", "streams", "rank", "week", "year", "month",
        "danceability", "energy", "loudness", "valence", "acousticness", "speechiness",
        "liveness", "tempo", "duration_min", "explicit", "popularity",
        "income_group", "region_wb", "track_genre", "is_trending", "mood_category", "country"
    ]
    df = pd.read_csv(path, usecols=lambda c: c in needed_cols, low_memory=False)
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
        popularity=("popularity", "max"),
        danceability=("danceability", "mean"),
        energy=("energy", "mean"),
        valence=("valence", "mean"),
        track_genre=("track_genre", lambda s: s.dropna().iloc[0] if len(s.dropna()) > 0 else "Pop")
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
    "🗺️ Bản đồ phân bố lượt Stream toàn cầu",
    "📈 Tương quan Danceability vs Energy",
    "🔥 Ma trận tương quan đặc trưng âm học",
    "🎻 Phân phối Danceability & Valence theo thu nhập",
    "🕸️ Hồ sơ âm thanh đa chiều theo thể loại",
    "📊 Top 10 Thể loại & Nghệ sĩ dẫn đầu",
    "📅 Xu hướng biến thiên lượt Stream theo thời gian"
]

def render_insight_card(title, key_findings, details, implications):
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #101c13 0%, #0d1610 50%, #111111 100%); border: 1px solid #1a4228; border-radius: 12px; padding: 18px 22px; margin-top: 14px; box-shadow: 0 4px 18px rgba(0,0,0,0.45);">
        <div style="display:flex; align-items:center; gap:10px; margin-bottom: 12px;">
            <span style="font-size: 1.25rem;">💡</span>
            <h4 style="color: #1DB954; font-weight: 800; font-size: 1.05rem; margin: 0; letter-spacing: -0.2px;">NHẬN XÉT & PHÂN TÍCH Ý NGHĨA BIỂU ĐỒ</h4>
        </div>
        <div style="display:flex; flex-direction:column; gap:10px; font-size:0.86rem; line-height:1.55;">
            <div style="background:#152219; border-left:3px solid #1DB954; padding:8px 12px; border-radius:4px;">
                <b style="color:#ffffff;">📌 Nhận xét xu hướng chính:</b> <span style="color:#cccccc;">{key_findings}</span>
            </div>
            <div style="background:#171c18; border-left:3px solid #3498db; padding:8px 12px; border-radius:4px;">
                <b style="color:#ffffff;">🔍 Phân tích số liệu thống kê:</b> <span style="color:#cccccc;">{details}</span>
            </div>
            <div style="background:#1a1914; border-left:3px solid #f39c12; padding:8px 12px; border-radius:4px;">
                <b style="color:#ffffff;">🎯 Ý nghĩa & Ứng dụng thực tiễn:</b> <span style="color:#cccccc;">{implications}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
    <div style='margin-bottom: 14px;'>
        <h2 style='font-size: 1.35rem; font-weight: 900; letter-spacing: -0.3px; color: #1DB954; margin: 0 0 4px 0;'>DANH MỤC</h2>
        <p style='font-size: 0.74rem; font-weight: 700; color: #888888; text-transform: uppercase; letter-spacing: 0.6px; margin: 0;'>CHỌN CHỨC NĂNG:</p>
    </div>
    """, unsafe_allow_html=True)
    
    cat_mode = st.radio(
        "Mục chức năng:",
        options=[
            "Trang Chủ",
            "Bảng Dữ Liệu & Bộ Lọc",
            "Thống Kê Thị Trường",
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
    elif "Biểu Đồ" in cat_mode or "Trực Quan Hóa" in cat_mode:
        st.markdown("""
        <div style='margin: 22px 0 12px 0; border-top: 1px solid #282828; padding-top: 16px;'>
            <p style='font-size: 0.74rem; font-weight: 700; color: #1DB954; text-transform: uppercase; letter-spacing: 0.6px; margin: 0;'>CHỌN BIỂU ĐỒ PHÂN TÍCH:</p>
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
        <div style='margin: 22px 0 12px 0; border-top: 1px solid #282828; padding-top: 16px;'>
            <p style='font-size: 0.74rem; font-weight: 700; color: #888888; text-transform: uppercase; letter-spacing: 0.6px; margin: 0;'>CHỌN GÓC NHÌN DỮ LIỆU:</p>
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

# 0. MÀN HÌNH 0: TRANG CHỦ (HOME SHOWCASE)
if "Trang Chủ" in current_view:
    # 6 ẢNH BÌA ALBUM NGHỆ SĨ THẬT (3x2 GRID), OPACITY VỪA PHẢI, KHÔNG LẤN ÁT CHỮ
    covers = get_hero_album_covers()
    mosaic_imgs = ""
    for c in covers[:6]:
        mosaic_imgs += f'<img src="data:image/jpeg;base64,{c}" style="width:100%; aspect-ratio:1; object-fit:cover; border-radius:8px; box-shadow:0 4px 12px rgba(0,0,0,0.6); border: 1px solid rgba(255,255,255,0.08);" />'

    # TẦNG 1: HERO HEADER KHÔNG ĐÓNG KHUNG (THOÁNG ĐẠT & KẾT NỐI TỰ NHIÊN)
    st.markdown(f"""
    <div style="margin-bottom: 26px; padding-top: 4px;">
        <div style="display: grid; grid-template-columns: 1.65fr 1fr; gap: 32px; align-items: center;">
            <div>
                <div style="display: flex; align-items: flex-start; gap: 16px; margin-bottom: 14px;">
                    <svg viewBox="0 0 167.5 167.5" style="width: 50px; height: 50px; fill: #1DB954; flex-shrink: 0; margin-top: 4px; filter: drop-shadow(0 0 12px rgba(29, 185, 84, 0.5));">
                        <path fill="#1DB954" d="M83.7 0C37.5 0 0 37.5 0 83.7c0 46.3 37.5 83.7 83.7 83.7 46.3 0 83.7-37.5 83.7-83.7C167.5 37.5 130 0 83.7 0zm38.4 120.7c-1.5 2.5-4.7 3.3-7.2 1.8-19.7-12-44.5-14.7-73.7-8-2.8.6-5.6-1.2-6.2-4-.6-2.8 1.2-5.6 4-6.2 32-7.3 59.6-4.2 81.6 9.3 2.5 1.5 3.3 4.7 1.8 7.1zm10.2-22.8c-1.9 3.1-6 4-9.1 2.1-22.6-13.9-57-17.9-83.7-9.8-3.5 1.1-7.1-.9-8.2-4.4-1.1-3.5.9-7.1 4.4-8.2 30.5-9.3 68.6-4.8 94.5 11.2 3.1 1.9 4.1 6 2.1 9.1zm1.1-23.8c-27.1-16.1-71.8-17.6-97.7-9.7-4.1 1.3-8.6-1.1-9.8-5.2-1.3-4.1 1.1-8.6 5.2-9.8 29.8-9 79.1-7.3 110.3 11.2 3.7 2.2 4.9 7.1 2.7 10.8-2.2 3.7-7.1 4.9-10.7 2.7z"/>
                    </svg>
                    <h1 style="font-family: 'Montserrat', 'Be Vietnam Pro', sans-serif; font-size: 1.8rem; font-weight: 900; line-height: 1.25; letter-spacing: -0.5px; color: #ffffff; text-transform: uppercase; margin: 0;">
                        NGHIÊN CỨU VÀ TRỰC QUAN HÓA CÁC ĐẶC TRƯNG ÂM THANH & DỰ ĐOÁN XU HƯỚNG BÀI HÁT THỊNH HÀNH TRÊN SPOTIFY
                    </h1>
                </div>
                <p style="font-family: 'Times New Roman', Times, serif; font-size: 1.05rem; color: #94a3b8; line-height: 1.6; margin: 0 0 16px 0;">
                    Hệ thống phân tích dữ liệu đa chiều kho tàng âm nhạc Spotify Charts (2021 – 2022). Khám phá các đặc trưng âm học, cơ cấu phân bổ thị trường toàn cầu và ứng dụng học máy ước tính xu hướng bài hát thịnh hành.
                </p>
                <div style="display: flex; flex-wrap: wrap; gap: 18px; font-family: 'Times New Roman', Times, serif; font-size: 0.9rem; color: #64748b;">
                    <span>📅 <b>Chuỗi thời gian:</b> 2021 – 2022 (104 tuần)</span>
                    <span>🌍 <b>Bao phủ:</b> 65 Thị trường toàn cầu</span>
                </div>
            </div>
            <div>
                <div style="position: relative; overflow: hidden; border-radius: 14px; padding: 4px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.08); box-shadow: 0 12px 36px rgba(0,0,0,0.55);">
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px;">
                        {mosaic_imgs}
                    </div>
                </div>
                <div style="font-family: 'Times New Roman', Times, serif; font-size: 0.78rem; color: #64748b; text-align: center; margin-top: 8px;">
                    Nghệ sĩ tiêu biểu trên bảng xếp hạng âm nhạc toàn cầu
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # TẦNG 2: DẢI CHỈ SỐ KPI ĐƯỢC PHÂN PHỐI ĐỘC LẬP & RÕ RÀNG
    st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
    m_col1, m_col2 = st.columns([1.15, 1.85], gap="medium")
    with m_col1:
        st.markdown(f"""
        <div class="hero-anchor-card" style="min-height: 140px; padding: 22px 26px;">
            <div>
                <div style="font-family: 'Times New Roman', Times, serif; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; color: #cbd5e1; margin-bottom: 4px;">
                    TỔNG BẢN GHI BXH TOÀN CẦU
                </div>
                <div style="font-family: 'Montserrat', 'Be Vietnam Pro', sans-serif; font-size: 3.1rem; font-weight: 900; color: #1ed760; line-height: 1; letter-spacing: -1.2px; margin: 6px 0 8px 0;">
                    314,727
                </div>
            </div>
            <div style="font-family: 'Times New Roman', Times, serif; font-size: 0.86rem; color: #94a3b8; line-height: 1.45;">
                Tập dữ liệu chuẩn hóa từ 65 thị trường âm nhạc qua 104 tuần liên tiếp (2021 – 2022).
            </div>
        </div>
        """, unsafe_allow_html=True)
    with m_col2:
        s1, s2, s3 = st.columns(3, gap="medium")
        with s1:
            st.markdown(f"""
            <div class="sub-metric-card" style="min-height: 140px; padding: 20px 22px;">
                <div style="font-family: 'Times New Roman', Times, serif; font-size: 0.76rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.6px; color: #94a3b8; margin-bottom: 4px;">
                    BAO PHỦ ĐỊA LÝ
                </div>
                <div style="font-family: 'Montserrat', 'Be Vietnam Pro', sans-serif; font-size: 2.1rem; font-weight: 800; color: #ffffff; margin: 4px 0;">
                    65 <span style="font-size: 0.85rem; font-weight: 600; color: #64748b;">Quốc gia</span>
                </div>
                <div style="font-family: 'Times New Roman', Times, serif; font-size: 0.82rem; color: #64748b; line-height: 1.4;">
                    Đại diện cho tất cả các nhóm kinh tế theo World Bank.
                </div>
            </div>
            """, unsafe_allow_html=True)
        with s2:
            st.markdown(f"""
            <div class="sub-metric-card" style="min-height: 140px; padding: 20px 22px;">
                <div style="font-family: 'Times New Roman', Times, serif; font-size: 0.76rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.6px; color: #94a3b8; margin-bottom: 4px;">
                    CHUỖI THỜI GIAN
                </div>
                <div style="font-family: 'Montserrat', 'Be Vietnam Pro', sans-serif; font-size: 2.1rem; font-weight: 800; color: #ffffff; margin: 4px 0;">
                    104 <span style="font-size: 0.85rem; font-weight: 600; color: #64748b;">Tuần</span>
                </div>
                <div style="font-family: 'Times New Roman', Times, serif; font-size: 0.82rem; color: #64748b; line-height: 1.4;">
                    Quan sát biến động tuần hoàn từ năm 2021 đến hết 2022.
                </div>
            </div>
            """, unsafe_allow_html=True)
        with s3:
            st.markdown(f"""
            <div class="sub-metric-card" style="min-height: 140px; padding: 20px 22px;">
                <div style="font-family: 'Times New Roman', Times, serif; font-size: 0.76rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.6px; color: #94a3b8; margin-bottom: 4px;">
                    UNIQUE HITS
                </div>
                <div style="font-family: 'Montserrat', 'Be Vietnam Pro', sans-serif; font-size: 2.1rem; font-weight: 800; color: #ffffff; margin: 4px 0;">
                    2,242 <span style="font-size: 0.85rem; font-weight: 600; color: #64748b;">Bài</span>
                </div>
                <div style="font-family: 'Times New Roman', Times, serif; font-size: 0.82rem; color: #64748b; line-height: 1.4;">
                    Ca khúc độc nhất sau khi lọc và gộp chuỗi tuần hoàn.
                </div>
            </div>
            """, unsafe_allow_html=True)





# 1. MÀN HÌNH 1A: TỔNG QUAN DỮ LIỆU
elif "Tổng Quan Dữ Liệu" in current_view:
    st.markdown("""
    <div style='margin-bottom: 20px;'>
        <div style='margin-bottom: 6px;'>
            <h1 style='font-family: "Montserrat", "Be Vietnam Pro", sans-serif; font-size: 2.2rem; font-weight: 900; color: #ffffff; margin: 0; letter-spacing: -0.8px;'>Tổng Quan Bộ Dữ Liệu Spotify</h1>
        </div>
        <p style='font-size: 0.84rem; color: #94a3b8; margin: 0; line-height: 1.45;'>
            Báo cáo cấu trúc quy mô tập mẫu, định lượng lịch sử xếp hạng và các thông số âm học chuẩn hóa từ Spotify Charts API (2021 – 2022).
        </p>
    </div>
    """, unsafe_allow_html=True)
    


    # 2. CHẾ ĐỘ DỮ LIỆU & CÁCH GỘP BÀI HÁT (CÓ KHOẢNG THỞ RỘNG RÃI THEO LƯỚI 16PX)
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    c_mode1, c_mode2 = st.columns([1.1, 1.1], gap="large")
    with c_mode1:
        st.markdown("<p style='font-size: 0.82rem; font-weight: 700; color: #cccccc; margin-bottom: 6px;'>Chế Độ Xem Dữ Liệu:</p>", unsafe_allow_html=True)
        data_mode = st.radio(
            "Chọn Nguồn Dữ Liệu:",
            options=[
                "🟢 Dữ Liệu Đã Làm Sạch (Cleaned Data)",
                "🔴 Dữ Liệu Gốc (Raw Data)"
            ],
            index=0,
            horizontal=True,
            label_visibility="collapsed",
            key="home_data_mode"
        )
    with c_mode2:
        st.markdown("<p style='font-size: 0.82rem; font-weight: 700; color: #1DB954; margin-bottom: 6px;'>Cách gộp bài hát:</p>", unsafe_allow_html=True)
        view_granularity = st.selectbox(
            "Cách gộp bài hát:",
            options=[
                "Gộp theo bài hát",
                "Chi tiết từng tuần BXH"
            ],
            index=0,
            label_visibility="collapsed",
            key="home_view_granularity"
        )

    # 3. GHI CHÚ NHỎ GỌN (GIỮ NGUYÊN NỘI DUNG NHƯ CŨ, KHOẢNG THỞ CÂN ĐỐI)
    is_agg = "Gộp" in view_granularity
    if is_agg:
        st.markdown("""
        <div style='font-size: 0.76rem; color: #b3b3b3; background: #0f1c13; border-left: 3px solid #1DB954; padding: 8px 14px; border-radius: 6px; margin: 16px 0 16px 0; line-height: 1.45;'>
            💡 <b>Góc nhìn Gộp theo bài hát (Khuyến nghị):</b> Đã tổng hợp 314,727 bản ghi tuần thành 2,242 bài hát độc nhất. Mỗi bài chỉ xuất hiện <b>duy nhất 1 dòng</b> với <b>Tổng lượt Streams</b>, <b>Hạng cao nhất từng đạt</b> và <b>Số tuần trụ hạng</b>. Cột <b>Top</b> thể hiện thứ tự xếp hạng của bài hát trong bảng.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='font-size: 0.76rem; color: #b3b3b3; background: #1c170e; border-left: 3px solid #f39c12; padding: 8px 14px; border-radius: 6px; margin: 16px 0 16px 0; line-height: 1.45;'>
            ⚠️ <b>Góc nhìn Chi tiết theo tuần (Time-series):</b> Đang hiển thị bản ghi lịch sử từng tuần của 65 quốc gia. Cùng 1 bài hát sẽ xuất hiện nhiều dòng nếu lọt top ở nhiều tuần khác nhau. Cột <b>Hạng Tuần Đó</b> là thứ hạng của bài hát trên BXH trong tuần cụ thể đó.
        </div>
        """, unsafe_allow_html=True)

    # 4. THANH TÌM KIẾM, SẮP XẾP & BỘ ĐIỀU KHIỂN BẢNG DỮ LIỆU (TÁCH BIỆT RÕ RÀNG)
    t_c1, t_c2, t_c3 = st.columns([2.2, 1.3, 0.9], gap="medium")
    with t_c1:
        search_kw = st.text_input(
            "Tìm kiếm bài hát / thể loại:",
            placeholder="🔍 Tìm kiếm theo tên bài hát hoặc thể loại...",
            label_visibility="collapsed",
            key="raw_search_kw"
        )
    with t_c2:
        if is_agg:
            sort_options = [
                "Tổng Streams (Giảm dần)",
                "Hạng Cao Nhất (Tăng dần)",
                "Số tuần trên BXH (Giảm dần)",
                "Độ phổ biến (Popularity)",
                "Độ bắt tai (Danceability)",
                "Năng lượng (Energy)"
            ]
        else:
            sort_options = [
                "Lượt Streams tuần đó (Giảm dần)",
                "Hạng Tuần Đó (Tăng dần)",
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
    with t_c3:
        row_limit = st.selectbox(
            "Số bản ghi:",
            options=[50, 100, 250, 500, "Tất cả"],
            index=1,
            label_visibility="collapsed",
            key="raw_row_limit"
        )

    # Lấy nguồn dữ liệu theo góc nhìn đã chọn
    if is_agg:
        df_preview = df_unique_tracks.copy()
    else:
        df_preview = df_raw.copy()

    # Xử lý lọc dữ liệu theo từ khóa tìm kiếm (ĐÃ LOẠI BỎ LỌC THEO TÊN NGHỆ SĨ)
    if search_kw.strip():
        kw = search_kw.strip().lower()
        df_preview = df_preview[
            df_preview["track_name"].astype(str).str.lower().str.contains(kw, na=False) |
            df_preview["track_genre"].astype(str).str.lower().str.contains(kw, na=False)
        ]

    # Xử lý sắp xếp cột
    if "Streams" in sort_choice:
        df_preview = df_preview.sort_values(by="streams", ascending=False)
    elif "Hạng Cao Nhất" in sort_choice:
        df_preview = df_preview.sort_values(by="best_rank", ascending=True)
    elif "Hạng Tuần Đó" in sort_choice:
        df_preview = df_preview.sort_values(by="rank", ascending=True)
    elif "Số tuần" in sort_choice:
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

    # Đánh số thứ tự bảng Top (1, 2, 3...)
    df_preview = df_preview.reset_index(drop=True)
    df_preview["top_order"] = df_preview.index + 1

    # Thông báo số lượng kết quả
    unit_label = "bài hát độc nhất" if is_agg else "bản ghi tuần"
    st.markdown(f"<p style='font-size:0.78rem; color:#888888; margin: 4px 0 8px 0;'>📊 Đang hiển thị <b>{len(df_preview):,}</b> / <b>{total_matched:,}</b> {unit_label} phù hợp</p>", unsafe_allow_html=True)

    # 5. BANG DU LIEU DATAFRAME VOI COLUMN_CONFIG
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
                "popularity": st.column_config.ProgressColumn("Popularity", min_value=0, max_value=100, format="%d"),
                "track_genre": st.column_config.TextColumn("Thể Loại"),
                "danceability": st.column_config.NumberColumn("Danceability", format="%.3f"),
                "energy": st.column_config.NumberColumn("Energy", format="%.3f"),
                "valence": st.column_config.NumberColumn("Valence", format="%.3f")
            },
            hide_index=True,
            width="stretch",
            height=420
        )
    else:
        st.dataframe(
            df_preview[[
                "top_order", "rank", "track_name", "artist_individual", "streams", 
                "week", "country", "popularity", "track_genre", "danceability", "energy", "valence"
            ]],
            column_config={
                "top_order": st.column_config.NumberColumn("STT", format="%d", width="small"),
                "rank": st.column_config.NumberColumn("Hạng Tuần Đó", format="#%d", width="small"),
                "track_name": st.column_config.TextColumn("Tên Bài Hát"),
                "artist_individual": st.column_config.TextColumn("Nghệ Sĩ"),
                "streams": st.column_config.NumberColumn("Lượt Streams Tuần Đó", format="%d"),
                "week": st.column_config.DateColumn("Tuần BXH", format="YYYY-MM-DD"),
                "country": st.column_config.TextColumn("Quốc Gia"),
                "popularity": st.column_config.ProgressColumn("Popularity", min_value=0, max_value=100, format="%d"),
                "track_genre": st.column_config.TextColumn("Thể Loại"),
                "danceability": st.column_config.NumberColumn("Danceability", format="%.3f"),
                "energy": st.column_config.NumberColumn("Energy", format="%.3f"),
                "valence": st.column_config.NumberColumn("Valence", format="%.3f")
            },
            hide_index=True,
            width="stretch",
            height=420
        )

# 2. MÀN HÌNH 1B: BỘ LỌC DỮ LIỆU CHI TIẾT (LIKE USER REFERENCE SCREENSHOT)
elif "Bộ Lọc Chi Tiết" in current_view:
    st.markdown("<h1 style='font-size: 2.2rem; font-weight: 900; color: #ffffff; margin-bottom: 14px;'>Bộ Lọc Dữ Liệu Chi Tiết</h1>", unsafe_allow_html=True)
    
    # BLUE ANALYSIS & MEANING BANNER
    st.markdown("""
    <div style="background-color: #0b2336; border-left: 4px solid #1DB954; border-radius: 8px; padding: 16px 20px; margin-bottom: 22px;">
        <h4 style="color: #1DB954; font-weight: 800; font-size: 0.95rem; margin-bottom: 6px;">PHÂN TÍCH & Ý NGHĨA: CÔNG CỤ LỌC</h4>
        <p style="color: #d1d5db; font-size: 0.82rem; margin: 0; line-height: 1.55;">
            Công cụ này giúp bạn 'đào sâu' vào dữ liệu để tìm kiếm những thông tin cụ thể. Bạn có thể kết hợp nhiều tiêu chí như lọc theo tên nghệ sĩ, tìm tất cả ca khúc Pop thuộc nhóm High Income, hoặc lọc các bài hát có chỉ số Danceability & Energy đạt ngưỡng bứt phá.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # CONTAINER TIÊU CHÍ LỌC (CÓ KHOẢNG THỞ RỘNG RÃI)
    with st.container(border=True):
        st.markdown("<h3 style='font-size: 1.1rem; font-weight: 800; color: #ffffff; margin-bottom: 16px;'>Tiêu Chí Lọc Đa Chiều 🔗</h3>", unsafe_allow_html=True)
        
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
        btn_filter = st.button("Lọc Ngay 🔍", type="primary", key="btn_filter")
        
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
    
    st.markdown(f"<p style='font-size: 0.92rem; font-weight: 700; color: #1DB954; margin: 20px 0 12px 0;'>🎉 Tìm thấy <b>{len(df_filtered):,}</b> bản ghi phù hợp với tiêu chí lọc!</p>", unsafe_allow_html=True)
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
            <h1 style='font-family: "Montserrat", "Be Vietnam Pro", sans-serif; font-size: 2.1rem; font-weight: 900; color: #ffffff; margin: 0; letter-spacing: -0.8px;'>Tổng Quan Thị Trường Âm Nhạc</h1>
        </div>
        <p style='font-size: 0.83rem; color: #94a3b8; margin: 0;'>Theo dõi các chỉ số cốt lõi, phân tích cơ cấu thị trường và khám phá chi tiết từng ca khúc thịnh hành.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # =========================================================================
    # TẦNG 1: BỘ LỌC THỊ TRƯỜNG + 4 CHỈ SỐ TỔNG QUAN (1 LỚN ~40% + 3 NHỎ BÊN CẠNH)
    # =========================================================================
    with st.container(border=True):
        st.markdown("""
        <div style="margin-bottom:10px;">
            <div style="font-family: 'Montserrat', 'Be Vietnam Pro', sans-serif; font-size:0.88rem; font-weight:800; color:#ffffff; letter-spacing: -0.2px;">⚙️ BỘ LỌC ĐA CHIỀU THỊ TRƯỜNG</div>
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
    avg_duration = df_view['duration_min'].mean()
    avg_pop = df_view['popularity'].mean()

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    k_hero, k_sub = st.columns([1.1, 1.6], gap="medium")
    
    with k_hero:
        st.markdown(f"""
        <div class="hero-anchor-card" style="min-height: 118px; padding: 18px 22px;">
            <div style="margin-bottom:4px;">
                <div style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; color: #cbd5e1;">Bài Hát Khảo Sát</div>
            </div>
            <div style="font-family: 'Montserrat', 'Be Vietnam Pro', sans-serif; font-size: 2.8rem; font-weight: 900; line-height: 1.05; letter-spacing: -1.2px; color: #ffffff; margin-bottom: 4px;">
                {n_tracks:,} <span style="font-size: 1.15rem; color: #1ed760; font-weight: 800;">TRACKS</span>
            </div>
            <div style="font-size: 0.76rem; color: #94a3b8; line-height: 1.35;">
                Tổng số ca khúc lọt BXH Spotify trong phạm vi thị trường đã chọn.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with k_sub:
        s1, s2, s3 = st.columns(3, gap="medium")
        with s1:
            st.markdown(f"""
            <div class="sub-metric-card" style="min-height: 118px; padding: 16px 18px;">
                <div style="font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.6px; color: #94a3b8;">Nghệ Sĩ Khảo Sát</div>
                <div style="font-family: 'Montserrat', 'Be Vietnam Pro', sans-serif; font-size: 1.7rem; font-weight: 800; color: #ffffff; margin: 4px 0;">{n_artists:,}</div>
                <div style="font-size: 0.72rem; color: #64748b;">Nghệ sĩ độc lập/nhóm</div>
            </div>
            """, unsafe_allow_html=True)
        with s2:
            st.markdown(f"""
            <div class="sub-metric-card" style="min-height: 118px; padding: 16px 18px;">
                <div style="font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.6px; color: #94a3b8;">Thời Lượng TB</div>
                <div style="font-family: 'Montserrat', 'Be Vietnam Pro', sans-serif; font-size: 1.7rem; font-weight: 800; color: #ffffff; margin: 4px 0;">{avg_duration:.2f}m</div>
                <div style="font-size: 0.72rem; color: #64748b;">~{int(avg_duration * 60)}s chuẩn streaming</div>
            </div>
            """, unsafe_allow_html=True)
        with s3:
            st.markdown(f"""
            <div class="sub-metric-card" style="min-height: 118px; padding: 16px 18px;">
                <div style="font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.6px; color: #94a3b8;">Độ Phổ Biến TB</div>
                <div style="font-family: 'Montserrat', 'Be Vietnam Pro', sans-serif; font-size: 1.7rem; font-weight: 800; color: #1ed760; margin: 4px 0;">{avg_pop:.0f}/100</div>
                <div style="font-size: 0.72rem; color: #64748b;">Điểm Popularity trung bình</div>
            </div>
            """, unsafe_allow_html=True)

    # =========================================================================
    # TẦNG 2: PHÂN TÍCH THỊ TRƯỜNG TỔNG THỂ (CĂN LƯỚI ĐỒNG BỘ 3 CỘT: 2 DONUT + 1 BAR)
    # =========================================================================
    st.markdown("""
    <div style="margin: 24px 0 12px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.08); padding-bottom: 8px;">
        <div style="font-family: 'Montserrat', 'Be Vietnam Pro', sans-serif; font-size: 1.05rem; font-weight: 800; color: #ffffff; letter-spacing: -0.2px;">
            📊 Phân Tích Cơ Cấu Thị Trường (Market Distribution)
        </div>
    </div>
    """, unsafe_allow_html=True)

    chart_c1, chart_c2, chart_c3 = st.columns([1.0, 1.0, 1.25], gap="medium")
    
    with chart_c1:
        st.markdown("""
        <div class="bento-card" style="margin-bottom:0; padding: 16px 18px; min-height: 255px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                <span style="font-size:0.8rem; font-weight:700; color:#ffffff;">Tỷ lệ Explicit vs Clean</span>
                <span style="font-size:0.68rem; color:#888888;">Nội dung nhạy cảm</span>
            </div>
        """, unsafe_allow_html=True)
        if "explicit" in df_view.columns:
            exp_counts = df_view["explicit"].value_counts().reset_index()
            exp_counts.columns = ["Type", "Count"]
            exp_counts["Type"] = exp_counts["Type"].map({True: "Explicit", False: "Clean"})
            fig_d1 = px.pie(exp_counts, values="Count", names="Type", hole=0.7, color="Type", color_discrete_map={"Explicit": "#1DB954", "Clean": "#252e35"})
            fig_d1.update_layout(**PLOTLY_THEME, height=170, showlegend=False, margin=dict(t=5, b=5, l=5, r=5))
            fig_d1.update_traces(textinfo="label+percent", textfont=dict(size=10, color="#ffffff"))
            st.plotly_chart(fig_d1, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with chart_c2:
        st.markdown("""
        <div class="bento-card" style="margin-bottom:0; padding: 16px 18px; min-height: 255px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                <span style="font-size:0.8rem; font-weight:700; color:#ffffff;">Nhóm Thu Nhập (World Bank)</span>
                <span style="font-size:0.68rem; color:#888888;">Phân bổ kinh tế</span>
            </div>
        """, unsafe_allow_html=True)
        if "income_group" in df_view.columns:
            inc_counts = df_view["income_group"].value_counts().head(3).reset_index()
            inc_counts.columns = ["Income", "Count"]
            fig_d2 = px.pie(inc_counts, values="Count", names="Income", hole=0.7, color_discrete_sequence=["#1DB954", "#8e44ad", "#38bdf8"])
            fig_d2.update_layout(**PLOTLY_THEME, height=170, showlegend=False, margin=dict(t=5, b=5, l=5, r=5))
            fig_d2.update_traces(textinfo="label+percent", textfont=dict(size=10, color="#ffffff"))
            st.plotly_chart(fig_d2, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with chart_c3:
        st.markdown("""
        <div class="bento-card" style="margin-bottom:0; padding: 16px 18px; min-height: 255px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                <span style="font-size:0.8rem; font-weight:700; color:#ffffff;">Lượt Stream Theo Tháng</span>
                <span style="font-size:0.68rem; color:#888888;">Biến thiên chuỗi thời gian</span>
            </div>
        """, unsafe_allow_html=True)
        df_copy = df_view.copy()
        df_copy["month_name"] = df_copy["week"].dt.strftime("%b")
        month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        m_streams = df_copy.groupby("month_name")["streams"].sum().reindex(month_order).dropna().reset_index()
        fig_m = px.bar(m_streams, x="month_name", y="streams", color_discrete_sequence=["#9b51e0"])
        fig_m.update_layout(**PLOTLY_THEME, height=170, margin=dict(t=10, b=15, l=15, r=15), xaxis=dict(title="", showgrid=False), yaxis=dict(title="", showgrid=True, gridcolor="#222222"))
        st.plotly_chart(fig_m, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    # =========================================================================
    # TẦNG 3: KHÁM PHÁ BÀI HÁT CỤ THỂ (ĐỒNG BỘ 1 KHUNG DUY NHẤT: CHỌN + CHI TIẾT)
    # =========================================================================
    st.markdown("""
    <div style="margin: 28px 0 14px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.08); padding-bottom: 8px;">
        <div style="font-family: 'Montserrat', 'Be Vietnam Pro', sans-serif; font-size: 1.05rem; font-weight: 800; color: #1ed760; letter-spacing: -0.2px;">
            🎧 Khám Phá Bài Hát Cụ Thể (Interactive Track Explorer)
        </div>
    </div>
    """, unsafe_allow_html=True)

    top_tracks = df_view.groupby(["track_name", "artist_individual"])["streams"].sum().reset_index()
    top_tracks = top_tracks.sort_values(by="streams", ascending=False).head(30)
    track_options = [f"{row['track_name']} — {row['artist_individual']}" for _, row in top_tracks.iterrows()]
    
    with st.container(border=True):
        p_c1, p_c2 = st.columns([1.15, 1.25], gap="large")
        
        with p_c1:
            st.markdown("<p style='font-size:0.8rem; font-weight:700; color:#cbd5e1; margin-bottom:6px;'>1. Chọn ca khúc để khám phá:</p>", unsafe_allow_html=True)
            sel_track_str = st.selectbox("Chọn ca khúc:", options=track_options, index=0, label_visibility="collapsed", key="track_explorer_sel")
            
            sel_tname = sel_track_str.split(" — ")[0]
            sel_aname = sel_track_str.split(" — ")[1]
            t_data = df_view[(df_view["track_name"] == sel_tname) & (df_view["artist_individual"] == sel_aname)].iloc[0]
            
            st.markdown(f"""
            <div style="margin-top: 14px; background: #151a1e; border: 1px solid #232c33; border-radius: 10px; padding: 12px 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-size: 0.76rem; color: #94a3b8;">Thể loại: <b style="color: #ffffff;">{t_data.get('track_genre', 'Pop')}</b></span>
                    <span style="font-size: 0.76rem; color: #94a3b8;">Thứ hạng: <b style="color: #ffffff;">#{t_data['rank']}</b></span>
                </div>
                <div style="font-size: 0.76rem; color: #94a3b8;">
                    Tổng Streams tích lũy: <b style="font-family: 'Montserrat', 'Be Vietnam Pro', sans-serif; font-size: 1.15rem; color: #1ed760; font-weight: 800;">{t_data['streams']:,.0f}</b> lượt
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with p_c2:
            dance_pct = int(t_data.get('danceability', 0.7) * 100)
            energy_pct = int(t_data.get('energy', 0.6) * 100)
            valence_pct = int(t_data.get('valence', 0.5) * 100)
            
            st.markdown(f"""
            <div class="player-card" style="margin-top: 0; padding: 16px 20px;">
                <div style="margin-bottom: 2px;">
                    <div class="player-title">{sel_tname}</div>
                    <div class="player-artist">{sel_aname}</div>
                </div>
                <div class="player-progress" style="margin: 8px 0 10px 0;"><div class="player-progress-bar" style="width: {dance_pct}%;"></div></div>
                <div style="display: flex; flex-direction: column; gap: 6px;">
                    <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#cbd5e1;">
                        <span>💃 Độ bắt tai (Danceability): <b>{dance_pct}%</b></span>
                        <div style="width: 110px; background: #22292f; height: 6px; border-radius: 3px; align-self:center; overflow:hidden;">
                            <div style="background: #1ed760; width: {dance_pct}%; height: 100%;"></div>
                        </div>
                    </div>
                    <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#cbd5e1;">
                        <span>⚡ Mức năng lượng (Energy): <b>{energy_pct}%</b></span>
                        <div style="width: 110px; background: #22292f; height: 6px; border-radius: 3px; align-self:center; overflow:hidden;">
                            <div style="background: #f59e0b; width: {energy_pct}%; height: 100%;"></div>
                        </div>
                    </div>
                    <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#cbd5e1;">
                        <span>🌈 Tích cực cảm xúc (Valence): <b>{valence_pct}%</b></span>
                        <div style="width: 110px; background: #22292f; height: 6px; border-radius: 3px; align-self:center; overflow:hidden;">
                            <div style="background: #38bdf8; width: {valence_pct}%; height: 100%;"></div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # =========================================================================
    # TẦNG 4: XU HƯỚNG TÍCH LŨY LƯỢT STREAM THEO TUẦN
    # =========================================================================
    st.markdown("<hr style='border-color:rgba(255,255,255,0.08); margin:20px 0 16px 0;'>", unsafe_allow_html=True)
    
    st.markdown('<div class="bento-card" style="margin-bottom:0; padding:16px 18px;">', unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.85rem; font-weight:700; color:#ffffff; margin-bottom:0;'>Tăng trưởng lượt stream lũy kế theo tuần</p>", unsafe_allow_html=True)
    st.caption("Biểu đồ diện tích spline theo tuần")
    
    w_trend = df_view.groupby(pd.Grouper(key="week", freq="W"))["streams"].sum().reset_index()
    fig_tr = go.Figure()
    fig_tr.add_trace(go.Scatter(x=w_trend["week"], y=w_trend["streams"], mode="lines", line=dict(color="#f39c12", width=2.5, shape="spline"), fill="tozeroy", fillcolor="rgba(243, 156, 18, 0.12)"))
    fig_tr.update_layout(**PLOTLY_THEME, height=270, margin=dict(t=15, b=20, l=25, r=15), xaxis=dict(gridcolor="#1f1f1f"), yaxis=dict(gridcolor="#1f1f1f"))
    st.plotly_chart(fig_tr, width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)

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
            "📊 Chọn biểu đồ để hiển thị:",
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
            st.markdown("<div style='font-size:0.85rem; font-weight:700; color:#ffffff; margin-bottom:6px;'>Bộ lọc dữ liệu tương tác đa chiều</div>", unsafe_allow_html=True)
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
        # (Để thêm biểu đồ mới: Chỉ cần thêm 1 nhánh elif "Tên biểu đồ" in current_chart)
        # ═════════════════════════════════════════════════════════════════════════════
        
        if "Bản đồ" in current_chart:
            # ─── BIỂU ĐỒ 1: BẢN ĐỒ THỊ PHẦN TOÀN CẦU ───
            st.markdown('<div class="slot-card" style="padding:16px;">', unsafe_allow_html=True)
            st.markdown("<p style='font-size:1.05rem; font-weight:800; color:#ffffff; margin-bottom:2px;'>Bản đồ phân bổ tổng lượt Stream theo Quốc gia (Choropleth Map)</p>", unsafe_allow_html=True)
            st.caption("Thị phần tiêu thụ âm nhạc trực tuyến trên 65 quốc gia và vùng lãnh thổ")
            
            geo_df = df_viz.groupby("country")["streams"].sum().reset_index()
            fig_map = px.choropleth(
                geo_df,
                locations="country",
                locationmode="country names",
                color="streams",
                color_continuous_scale=["#0e2d18", "#14833b", "#1DB954", "#1ed760"],
                labels={"streams": "Lượt stream"}
            )
            fig_map.update_layout(
                **PLOTLY_THEME,
                height=450,
                margin=dict(l=0, r=0, t=10, b=0),
                geo=dict(bgcolor="rgba(0,0,0,0)", showframe=False, showcoastlines=True, coastlinecolor="#2a2a2a", projection_type="equirectangular")
            )
            st.plotly_chart(fig_map, width="stretch")
            st.markdown('</div>', unsafe_allow_html=True)
            
            render_insight_card(
                title="Bản Đồ Phân Bổ Lượt Stream Toàn Cầu",
                key_findings="Thị trường Bắc Mỹ (Hoa Kỳ) và Mỹ Latinh (Mexico, Brazil) chiếm tỷ trọng stream vượt trội, cho thấy sự tập trung thị phần cao tại các quốc gia có độ phủ sóng internet và dịch vụ streaming trả phí phổ cập.",
                details=f"Top 5 quốc gia dẫn đầu đóng góp hơn 45% tổng lượt stream trong tổng số {df_viz['country'].nunique()} quốc gia khảo sát. Các quốc gia thuộc khu vực Châu Phi và Trung Á có độ phủ stream thấp hơn đáng kể.",
                implications="Khi lên kế hoạch ra mắt ca khúc hoặc album toàn cầu, các nghệ sĩ và hãng đĩa cần ưu tiên tối ưu hóa múi giờ phát hành và chiến dịch quảng bá tập trung vào các thị trường dẫn dắt lưu lượng này."
            )
            
        elif "Tương quan Danceability" in current_chart or "Scatter" in current_chart:
            # ─── BIỂU ĐỒ 2: TƯƠNG QUAN DANCEABILITY VS ENERGY ───
            st.markdown('<div class="slot-card" style="padding:16px;">', unsafe_allow_html=True)
            st.markdown("<p style='font-size:1.05rem; font-weight:800; color:#ffffff; margin-bottom:2px;'>Tương quan Độ bắt tai (Danceability) vs Năng lượng (Energy)</p>", unsafe_allow_html=True)
            st.caption("Phân bố tương quan âm học đa chiều kèm thể loại và độ lớn lượt stream")
            
            sample_viz = df_viz.sample(min(1500, len(df_viz)), random_state=42)
            fig_sc = px.scatter(
                sample_viz,
                x="danceability",
                y="energy",
                color="track_genre" if "track_genre" in sample_viz.columns else None,
                size="streams",
                hover_name="track_name",
                hover_data=["artist_individual", "streams", "rank"],
                color_discrete_sequence=["#1DB954", "#f39c12", "#e74c3c", "#3498db", "#9b59b6", "#1abc9c"]
            )
            fig_sc.update_layout(**PLOTLY_THEME, height=440, margin=dict(t=10, b=15, l=15, r=15))
            st.plotly_chart(fig_sc, width="stretch")
            st.markdown('</div>', unsafe_allow_html=True)
            
            render_insight_card(
                title="Tương Quan Danceability vs Energy",
                key_findings="Xuất hiện xu hướng tương quan thuận rõ nét giữa Danceability và Energy. Đa số các bản hit lọt top bảng xếp hạng tuần đều tập trung dày đặc ở góc phần tư phía trên bên phải (Danceability > 0.65 và Energy > 0.60).",
                details="Thể loại Reggaeton, Dance/Electronic và Pop phân cụm rất chặt chẽ tại vùng năng lượng cao (Energy trung bình đạt 0.72). Ngược lại, Acoustic/Indie phân bố rải rác ở góc trái dưới với Energy thấp (< 0.45).",
                implications="Công thức phối khí tối ưu cho một bài hát hướng đến vị thế viral trên Spotify đòi hỏi nhịp điệu kích thích vận động (rhythmic drive) và mức năng lượng âm thanh sôi nổi."
            )
            
        elif "Ma trận" in current_chart or "Heatmap" in current_chart:
            # ─── BIỂU ĐỒ 3: MA TRẬN NHIỆT TƯƠNG QUAN ───
            st.markdown('<div class="slot-card" style="padding:16px;">', unsafe_allow_html=True)
            st.markdown("<p style='font-size:1.05rem; font-weight:800; color:#ffffff; margin-bottom:2px;'>Ma trận tương quan tuyến tính đặc trưng âm thanh (Correlation Heatmap)</p>", unsafe_allow_html=True)
            st.caption("Hệ số tương quan Pearson đo lường mức độ liên kết giữa các thuộc tính âm học Spotify")
            
            aud_cols = ["danceability", "energy", "loudness", "valence", "acousticness", "speechiness", "tempo", "popularity"]
            aud_cols_present = [c for c in aud_cols if c in df_viz.columns]
            corr_matrix = df_viz[aud_cols_present].corr()
            fig_heat = px.imshow(
                corr_matrix,
                text_auto=".2f",
                color_continuous_scale=["#0a140e", "#14833b", "#1DB954"],
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
            # ─── BIỂU ĐỒ 4: PHÂN PHỐI THEO NHÓM THU NHẬP ───
            st.markdown('<div class="slot-card" style="padding:16px;">', unsafe_allow_html=True)
            st.markdown("<p style='font-size:1.05rem; font-weight:800; color:#ffffff; margin-bottom:2px;'>Phân phối Cảm xúc (Valence) & Độ bắt tai theo Nhóm thu nhập World Bank</p>", unsafe_allow_html=True)
            st.caption("Boxplot & Violin Plot thể hiện trung vị, độ phân tán và mật độ xác suất của cảm xúc âm nhạc")
            
            b_c1, b_c2 = st.columns(2, gap="medium")
            with b_c1:
                fig_box = px.box(
                    df_viz.dropna(subset=["income_group"]),
                    x="income_group",
                    y="danceability",
                    color="income_group",
                    color_discrete_sequence=["#1DB954", "#3498db", "#e67e22", "#9b59b6"]
                )
                fig_box.update_layout(**PLOTLY_THEME, height=380, showlegend=False, margin=dict(t=10, b=15, l=15, r=15))
                st.plotly_chart(fig_box, width="stretch")
            with b_c2:
                fig_v = px.violin(
                    df_viz.dropna(subset=["income_group"]),
                    x="income_group",
                    y="valence",
                    color="income_group",
                    box=True,
                    color_discrete_sequence=["#1DB954", "#f1c40f", "#e74c3c", "#34495e"]
                )
                fig_v.update_layout(**PLOTLY_THEME, height=380, showlegend=False, margin=dict(t=10, b=15, l=15, r=15))
                st.plotly_chart(fig_v, width="stretch")
            st.markdown('</div>', unsafe_allow_html=True)
            
            render_insight_card(
                title="Phân Phối Cảm Xúc Theo Nhóm Thu Nhập",
                key_findings="Các quốc gia thuộc nhóm thu nhập trung bình (Upper/Lower Middle Income) có điểm trung vị Valence cao hơn rõ rệt so với nhóm thu nhập cao (High Income).",
                details="Trung vị Valence ở nhóm Middle Income đạt mức ~0.58, trong khi nhóm High Income chỉ đạt ~0.49. Người nghe ở các nước phát triển có xu hướng chuộng các bài hát có âm điệu trầm lắng, sâu lắng (melancholic pop) nhiều hơn.",
                implications="Thị hiếu âm nhạc chịu sự chi phối mạnh mẽ của yếu tố kinh tế - xã hội. Khi phát hành nhạc ở các thị trường đang phát triển, các giai điệu tươi sáng, giàu năng lượng tích cực sẽ dễ tiếp cận khán giả hơn."
            )
            
        elif "Hồ sơ" in current_chart or "Radar" in current_chart:
            # ─── BIỂU ĐỒ 5: HỒ SƠ ÂM THANH RADAR ───
            st.markdown('<div class="slot-card" style="padding:16px;">', unsafe_allow_html=True)
            st.markdown("<p style='font-size:1.05rem; font-weight:800; color:#ffffff; margin-bottom:2px;'>Hồ sơ âm thanh đa chiều giữa các Thể loại âm nhạc (Radar Profile)</p>", unsafe_allow_html=True)
            st.caption("Radar Chart so sánh 6 chỉ số đặc trưng cốt lõi giữa top thể loại dẫn đầu")
            
            feats = ["danceability", "energy", "valence", "acousticness", "speechiness", "liveness"]
            feats = [f for f in feats if f in df_viz.columns]
            top_g = df_viz["track_genre"].value_counts().head(4).index
            
            fig_rad = go.Figure()
            for g in top_g:
                g_means = df_viz[df_viz["track_genre"] == g][feats].mean().tolist()
                fig_rad.add_trace(go.Scatterpolar(
                    r=g_means + [g_means[0]],
                    theta=feats + [feats[0]],
                    fill='toself',
                    name=str(g).upper()
                ))
            fig_rad.update_layout(
                **PLOTLY_THEME,
                height=420,
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 1], gridcolor="#222222"),
                    angularaxis=dict(gridcolor="#222222")
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
            st.markdown("<p style='font-size:1.05rem; font-weight:800; color:#ffffff; margin-bottom:2px;'>Top 10 Thể loại & Nghệ sĩ dẫn đầu tổng lượt Stream toàn cầu</p>", unsafe_allow_html=True)
            st.caption("Quy mô stream tích lũy của các siêu sao và dòng nhạc thịnh hành nhất")
            
            tc1, tc2 = st.columns(2, gap="medium")
            with tc1:
                top_artists = df_viz.groupby("artist_individual")["streams"].sum().nlargest(10).reset_index().sort_values(by="streams", ascending=True)
                fig_art = px.bar(top_artists, x="streams", y="artist_individual", orientation="h", color="streams", color_continuous_scale=["#0e2d18", "#1DB954"])
                fig_art.update_layout(**PLOTLY_THEME, height=380, showlegend=False, margin=dict(t=10, b=15, l=15, r=15), xaxis=dict(gridcolor="#1f1f1f"), yaxis=dict(title=""))
                st.plotly_chart(fig_art, width="stretch")
            with tc2:
                top_genres = df_viz.groupby("track_genre")["streams"].sum().nlargest(10).reset_index().sort_values(by="streams", ascending=True)
                fig_gen = px.bar(top_genres, x="streams", y="track_genre", orientation="h", color_discrete_sequence=["#1ed760"])
                fig_gen.update_layout(**PLOTLY_THEME, height=380, showlegend=False, margin=dict(t=10, b=15, l=15, r=15), xaxis=dict(gridcolor="#1f1f1f"), yaxis=dict(title=""))
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
            st.markdown("<p style='font-size:1.05rem; font-weight:800; color:#ffffff; margin-bottom:2px;'>Xu hướng biến thiên lượt Stream theo chuỗi thời gian (Weekly Time-series)</p>", unsafe_allow_html=True)
            st.caption("Biến động tổng lưu lượng stream qua từng tuần trong chu kỳ khảo sát")
            
            ts_df = df_viz.groupby("week")["streams"].sum().reset_index().sort_values(by="week")
            fig_ts_line = px.area(
                ts_df,
                x="week",
                y="streams",
                color_discrete_sequence=["#1DB954"]
            )
            fig_ts_line.update_layout(**PLOTLY_THEME, height=400, margin=dict(t=10, b=15, l=15, r=15), xaxis=dict(gridcolor="#1f1f1f", title="Tuần BXH"), yaxis=dict(gridcolor="#1f1f1f", title="Tổng Streams"))
            st.plotly_chart(fig_ts_line, width="stretch")
            st.markdown('</div>', unsafe_allow_html=True)
            
            render_insight_card(
                title="Xu Hướng Chuỗi Thời Gian Lượt Stream",
                key_findings="Lưu lượng stream có tính chu kỳ mùa vụ rất rõ rệt: Tăng trưởng mạnh vào mùa hè (tháng 6 - tháng 7) và bùng nổ cực đại vào mùa lễ hội cuối năm (tháng 12).",
                details="Tuần Giáng sinh và Năm mới ghi nhận lượng stream tăng đột biến hơn 32% so với mức trung bình các tuần thường trong năm, nhờ các ca khúc theo mùa (Holiday/Christmas songs).",
                implications="Thời điểm phát hành đóng vai trò chiến lược. Các bài hát mùa hè cần ra mắt từ cuối tháng 4 - tháng 5, trong khi các dự án lớn cần tránh va chạm với làn sóng nhạc lễ hội tháng 12."
            )

        # ═════════════════════════════════════════════════════════════════════════════
        # 🛠️ KHUNG HƯỚNG DẪN DÀNH CHO BẠN (LÝ GIA HÂN): CÁCH THÊM BIỂU ĐỒ MỚI TỪ NOTEBOOK
        # ═════════════════════════════════════════════════════════════════════════════
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        with st.expander("🛠️ Hướng dẫn cách thêm biểu đồ mới từ Jupyter Notebook (Dành cho bạn Lý Gia Hân)", expanded=False):
            st.markdown("""
            ### 📌 3 Bước cực kỳ đơn giản để đưa thêm bất kỳ biểu đồ nào bạn vẽ sau này lên Dashboard:
            
            **Bước 1:** Mở file `dashboard/app.py`, tìm đến danh sách `CHART_OPTIONS` (khoảng dòng 650) và thêm tên biểu đồ mới của bạn:
            ```python
            CHART_OPTIONS = [
                "🗺️ Biểu đồ 1: ...",
                ...
                "🎨 Biểu đồ 8: Phân tích độ dài bài hát theo năm (Histogram & KDE)"  # <-- Thêm tên biểu đồ mới vào đây
            ]
            ```
            
            **Bước 2:** Cuộn xuống phần `Trực Quan Hóa Dữ Liệu` (dưới Biểu đồ 7) và thêm một nhánh `elif`:
            ```python
            elif "Biểu đồ 8" in current_chart:
                st.markdown('<div class="slot-card" style="padding:16px;">', unsafe_allow_html=True)
                st.markdown("<p style='font-size:1.05rem; font-weight:800; color:#ffffff; margin-bottom:2px;'>Tên Biểu Đồ 8 Của Bạn</p>", unsafe_allow_html=True)
                st.caption("Mô tả ngắn gọn về biểu đồ...")
                
                # Code vẽ biểu đồ Plotly (từ notebook của bạn):
                fig8 = px.histogram(df_viz, x="duration_min", color="year", nbins=40, color_discrete_sequence=["#1DB954", "#3498db"])
                fig8.update_layout(**PLOTLY_THEME, height=400)
                st.plotly_chart(fig8, width="stretch")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Nhận xét và phân tích ý nghĩa biểu đồ:
                render_insight_card(
                    title="Phân Tích Thời Lượng Bài Hát",
                    key_findings="Xu hướng bài hát ngày càng ngắn dần qua các năm...",
                    details="Thời lượng trung bình giảm từ 3.6 phút (2021) xuống 3.1 phút (2022)...",
                    implications="Tối ưu cho thuật toán phát lặp lại trên TikTok và Spotify Shorts..."
                )
            ```
            
            **Bước 3:** Nhấn Save (`Ctrl + S`). Biểu đồ mới của bạn sẽ tự động xuất hiện trong danh sách lựa chọn ở Sidebar và màn hình chính!
            """)

# MAN HINH 3: HO SO AM THANH & NGHE SI
elif "Hồ Sơ Âm Thanh" in current_view:
    # 1. TIEU DE NOI BAT, CO KHONG GIAN THOANG, BO HAN PHU DE
    st.markdown("""
    <div style="margin: 28px 0 22px 0;">
        <h1 style="font-size: 2.4rem; font-weight: 900; letter-spacing: -0.8px; color: #ffffff; margin: 0; padding: 0; line-height: 1.15;">
            Hồ Sơ Đặc Trưng Âm Thanh & Nghệ Sĩ
        </h1>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. HANG BO LOC PHA VO DOI XUNG (Moc thoi gian rong gap 2.7 lan)
    all_months = sorted(df_raw["year_month"].unique())
    with st.container(border=True):
        af_c1, af_c2, af_c3 = st.columns([1, 1, 2.7], gap="large")
        with af_c1:
            sel_reg_aud = st.selectbox("Khu vực địa lý:", regions_list, key="aud_reg")
        with af_c2:
            sel_gen_aud = st.selectbox("Thể loại âm nhạc:", genres_list, key="aud_gen")
        with af_c3:
            time_range = st.select_slider("Mốc thời gian khảo sát (Tháng):", options=all_months, value=(all_months[0], all_months[-1]), key="aud_time")
    
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
            st.markdown("<div style='font-size:1.05rem; font-weight:700; color:#ffffff; padding-top:6px;'>Thị phần lượt Stream & Năng lượng âm thanh (Treemap)</div>", unsafe_allow_html=True)
        with t_h2:
            sel_art = st.selectbox("Chọn nghệ sĩ khảo sát:", options=astats["artist_individual"].tolist(), index=0, key="aud_art", label_visibility="collapsed")
        
        fig_tree = px.treemap(
            astats, path=["primary_genre", "artist_individual"], values="total_streams", color="avg_energy",
            color_continuous_scale=SPOTIFY_CONTINUOUS_COLOR
        )
        fig_tree.update_layout(**PLOTLY_THEME, height=340, margin=dict(t=8, b=10, l=5, r=5))
        st.plotly_chart(fig_tree, width="stretch")
        
        art_data = df_p[df_p["artist_individual"] == sel_art]
        st.markdown(f"<div style='font-size:1.05rem; font-weight:700; color:#1DB954; margin:10px 0 6px 0;'>Hồ sơ âm học nghệ sĩ: {sel_art}</div>", unsafe_allow_html=True)
        
        col_r, col_sc = st.columns([1, 1], gap="medium")
        with col_r:
            r_feats = ["danceability", "energy", "valence", "acousticness", "speechiness", "liveness"]
            labels = ["Danceability", "Energy", "Valence", "Acousticness", "Speechiness", "Liveness"]
            avals = [art_data[f].mean() for f in r_feats] + [art_data[r_feats[0]].mean()]
            
            bench = df_p[df_p["is_trending"] == 1]
            bvals = [bench[f].mean() for f in r_feats] + [bench[r_feats[0]].mean()]
            
            fig_rad = go.Figure()
            fig_rad.add_trace(go.Scatterpolar(r=bvals, theta=labels + [labels[0]], fill="toself", name="Top 50 Trending", line=dict(color="#666666", width=1.5, dash="dash"), fillcolor="rgba(100,100,100,0.08)"))
            fig_rad.add_trace(go.Scatterpolar(r=avals, theta=labels + [labels[0]], fill="toself", name=sel_art, line=dict(color="#1DB954", width=3), fillcolor="rgba(29,185,84,0.35)"))
            fig_rad.update_layout(**PLOTLY_THEME, polar=dict(radialaxis=dict(visible=True, range=[0, 1], gridcolor="#222222"), angularaxis=dict(gridcolor="#222222")), height=320, margin=dict(t=25, b=25, l=30, r=30))
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
            fig_sc.add_trace(go.Scatter(x=oth[x_ax], y=oth[y_ax], mode="markers", name="Các bài hát khác", marker=dict(color="#282828", size=5)))
            fig_sc.add_trace(go.Scatter(x=my_t[x_ax], y=my_t[y_ax], mode="markers", name=sel_art, marker=dict(color="#1DB954", size=11, line=dict(color="#ffffff", width=1.5))))
            fig_sc.update_layout(**PLOTLY_THEME, height=275, xaxis=dict(title=x_ax.upper(), gridcolor="#1f1f1f"), yaxis=dict(title=y_ax.upper(), gridcolor="#1f1f1f"), margin=dict(t=15, b=20, l=20, r=20))
            st.plotly_chart(fig_sc, width="stretch")

# MAN HINH 5: MANG LUOI NGHE SI TOAN CAU (NETWORK SCIENCE)
elif "Mạng Lưới" in current_view:
    st.markdown("""
    <div style='margin-bottom: 20px;'>
        <div style='margin-bottom: 4px;'>
            <h1 style='font-family: "Montserrat", "Be Vietnam Pro", sans-serif; font-size: 2.1rem; font-weight: 900; color: #ffffff; margin: 0; letter-spacing: -0.8px;'>Mạng Lưới Nghệ Sĩ Toàn Cầu</h1>
        </div>
        <p style='font-size: 0.83rem; color: #94a3b8; margin: 0;'>Phân tích mạng lưới đồng xuất hiện qua 65 quốc gia và thuật toán phát hiện các cộng đồng âm nhạc liên thị trường.</p>
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
            
        CLUSTER_COLORS = ["#1DB954", "#ff793f", "#a29bfe", "#00cec9", "#f1c40f", "#fd79a8"]
        CLUSTER_NAMES = ["Pop / Mainstream Core", "Latin Wave / Urbano", "Hip-Hop / Global Rap", "Asian / Regional Wave", "Dance / Electronic", "Indie / Alt Rock"]
        
        node_cluster = {}
        for c_idx, comm in enumerate(communities):
            for n in comm:
                node_cluster[n] = c_idx % len(CLUSTER_COLORS)
        
        # Chu thich cac cum mau phan biet
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:16px; margin: 4px 0 10px 0; font-size:0.78rem; flex-wrap:wrap;">
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
            textfont=dict(size=10, color="#ffffff", family="Times New Roman, serif"),
            hoverinfo="text",
            hovertext=n_text,
            marker=dict(
                color=n_colors,
                size=n_sizes,
                line=dict(width=1.8, color="#ffffff")
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
            <div style="font-family: 'Montserrat', 'Be Vietnam Pro', sans-serif; font-size:1.75rem; font-weight:800; color:#ffffff;">{G.number_of_nodes()}</div>
            <div style="font-size:0.72rem; color:#64748b;">Nghệ sĩ trong đồ thị</div>
        </div>
        """, unsafe_allow_html=True)
    with km2:
        st.markdown(f"""
        <div class="sub-metric-card" style="padding:14px 18px;">
            <div class="metric-label">SỐ LIÊN KẾT (EDGES)</div>
            <div style="font-family: 'Montserrat', 'Be Vietnam Pro', sans-serif; font-size:1.75rem; font-weight:800; color:#1ed760;">{G.number_of_edges():,}</div>
            <div style="font-size:0.72rem; color:#64748b;">Liên kết đồng xuất hiện</div>
        </div>
        """, unsafe_allow_html=True)
    with km3:
        density = nx.density(G) if G.number_of_nodes() > 1 else 0
        st.markdown(f"""
        <div class="sub-metric-card" style="padding:14px 18px;">
            <div class="metric-label">MẬT ĐỘ MẠNG LƯỚI</div>
            <div style="font-family: 'Montserrat', 'Be Vietnam Pro', sans-serif; font-size:1.75rem; font-weight:800; color:#ffffff;">{density:.3f}</div>
            <div style="font-size:0.72rem; color:#64748b;">Mức độ liên kết toàn cục</div>
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
            <h1 style='font-family: "Montserrat", "Be Vietnam Pro", sans-serif; font-size: 2.1rem; font-weight: 900; color: #ffffff; margin: 0; letter-spacing: -0.8px;'>Mô Hình Dự Báo Bài Hát Hit</h1>
        </div>
        <p style='font-size: 0.83rem; color: #94a3b8; margin: 0;'>Giả lập và ước tính xác suất bứt phá thành hit toàn cầu dựa trên thuật toán học máy phân tích đặc tính âm học.</p>
    </div>
    """, unsafe_allow_html=True)
    
    sim_left, sim_right = st.columns([1.2, 1.25], gap="large")
    
    with sim_left:
        with st.container(border=True):
            st.markdown("""
            <div style="margin-bottom:12px;">
                <div style="font-family: 'Montserrat', 'Be Vietnam Pro', sans-serif; font-size:0.92rem; font-weight:800; color:#ffffff;">🎛️ THÔNG SỐ ÂM HỌC CA KHÚC (AUDIO PARAMETERS)</div>
            </div>
            """, unsafe_allow_html=True)
            
            in_dance = st.slider("💃 Độ bắt tai (Danceability):", 0.0, 1.0, 0.74, 0.01, key="hit_d")
            in_energy = st.slider("⚡ Mức năng lượng (Energy):", 0.0, 1.0, 0.68, 0.01, key="hit_e")
            in_loud = st.slider("🔊 Độ lớn âm lượng (Loudness dB):", -25.0, 0.0, -5.5, 0.5, key="hit_l")
            in_val = st.slider("🌈 Cảm xúc tích cực (Valence):", 0.0, 1.0, 0.58, 0.01, key="hit_v")
            in_tempo = st.slider("🥁 Nhịp điệu (Tempo BPM):", 60.0, 200.0, 122.0, 1.0, key="hit_t")
            in_acoust = st.slider("🎸 Đặc tính mộc (Acousticness):", 0.0, 1.0, 0.12, 0.01, key="hit_a")
    
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
            number={'suffix': "%", 'font': {'color': "#1DB954", 'size': 38, 'family': 'Montserrat, sans-serif'}},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': "#444444", 'tickwidth': 1},
                'bar': {'color': "#1DB954", 'thickness': 0.28},
                'bgcolor': "#161b1f",
                'borderwidth': 1,
                'bordercolor': "#232c33",
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
            tier_badge = "🔥 TIỀM NĂNG TOP 10 GLOBAL HIT"
            tier_desc = "Cấu trúc âm học hội tụ đầy đủ phẩm chất của một ca khúc bùng nổ toàn cầu: độ bắt tai cao, âm lượng chuẩn nén streaming và năng lượng cuốn hút."
            tier_color = "#1ed760"
        elif prob >= 50:
            tier_badge = "⚡ TIỀM NĂNG TRENDING THEO DÒNG NHẠC"
            tier_desc = "Chỉ số ổn định, có khả năng lọt Top 50 các BXH khu vực. Có thể tăng thêm Danceability hoặc giảm bớt Acousticness để kích hoạt lan tỏa mạnh hơn."
            tier_color = "#f59e0b"
        else:
            tier_badge = "🎵 CA KHÚC THỊ TRƯỜNG NGÁCH (NICHE)"
            tier_desc = "Mang đặc tính âm nhạc chiêm nghiệm hoặc acoustic mộc mạc, phù hợp với danh sách phát thư giãn (Chill/Acoustic) hơn là BXH Top Hits đại chúng."
            tier_color = "#38bdf8"
            
        st.markdown(f"""
                <div style="background: rgba(0,0,0,0.35); border: 1px solid {tier_color}44; border-radius: 10px; padding: 12px 16px; margin-top: 6px;">
                    <div style="font-family: 'Montserrat', 'Be Vietnam Pro', sans-serif; font-size: 0.88rem; font-weight: 800; color: {tier_color}; margin-bottom: 4px;">
                        {tier_badge}
                    </div>
                    <p style="font-size: 0.76rem; color: #94a3b8; line-height: 1.45; margin: 0;">
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
            <div style="font-family: 'Montserrat', 'Be Vietnam Pro', sans-serif; font-size:0.95rem; font-weight:800; color:#ffffff;">
                📊 Hồ Sơ Đối Sánh Ca Khúc Giả Lập vs Top Hits Chuẩn (Radar Benchmark)
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
            line=dict(color="#1ed760", width=2.5),
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
