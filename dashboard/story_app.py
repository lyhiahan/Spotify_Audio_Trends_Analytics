"""Run with: streamlit run dashboard/story_app.py"""

import importlib
from pathlib import Path
import sys

import streamlit as st
import streamlit.components.v1 as components

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
dashboard_dir = PROJECT_ROOT / "dashboard"
if str(dashboard_dir) not in sys.path:
    sys.path.insert(0, str(dashboard_dir))

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
    [data-testid="stSidebar"] {min-width:235px!important;max-width:235px!important;background:#EEE9E1;}
    [data-testid="stHeader"] {height:2.2rem;background:transparent;}
    #MainMenu, footer, .stDeployButton {display:none!important;}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner="Đang dựng Tableau Story Canvas từ 04_story.ipynb…")
def build_story_canvas(source_stamp):
    import story_canvas
    return importlib.reload(story_canvas).canvas_html()


OPTIONS = list(STORY_PAGES) + ["Toàn cảnh: Story Studio (Canvas)"]

with st.sidebar:
    st.markdown("### Spotify Audio Trends")
    st.caption("Ba góc nhìn · một màn hình mỗi trang")
    selected = st.radio("Chọn dashboard", OPTIONS, label_visibility="collapsed")
    st.caption("Chọn vùng, quốc gia hoặc cột biểu đồ để xem dữ liệu liên quan. Hover để đọc giá trị gốc.")

if selected in STORY_PAGES:
    render_story_dashboard(selected)
else:
    try:
        source_stamp = tuple(
            (dashboard_dir / name).stat().st_mtime_ns
            for name in [
                "story_canvas.py", "story_canvas.html", "story_interactions.js",
                "story_data.py",
            ] if (dashboard_dir / name).exists()
        )
        components.html(build_story_canvas(source_stamp), height=950, scrolling=True)
    except Exception as exc:
        st.error(f"Không thể dựng Story Canvas: {exc}")
        st.caption("Kiểm tra các tệp trong dashboard/ và data/processed/.")
