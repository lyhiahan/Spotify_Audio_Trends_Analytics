"""Run with: streamlit run dashboard/story_app.py"""

import sys
from pathlib import Path

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dashboard.story_dashboards import STORY_PAGES, render_story_dashboard


st.set_page_config(
    page_title="Spotify · Câu chuyện dữ liệu",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    html, body, .stApp {background:#F7F4EF;color:#241F21;}
    [data-testid="stSidebar"] {min-width:225px!important;max-width:225px!important;background:#EEE9E1;}
    [data-testid="stHeader"] {height:2.2rem;background:transparent;}
    #MainMenu, footer, .stDeployButton {display:none!important;}
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### Spotify Audio Trends")
    st.caption("Ba góc nhìn · một màn hình mỗi trang")
    selected = st.radio("Chọn dashboard", STORY_PAGES, label_visibility="collapsed")
    st.caption("Chọn vùng, quốc gia hoặc cột biểu đồ để xem dữ liệu liên quan. Hover để đọc giá trị gốc.")

render_story_dashboard(selected)
