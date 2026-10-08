"""Run the Tableau-style Spotify story on a fixed viewport."""
from pathlib import Path
import sys

import streamlit as st
import streamlit.components.v1 as components

sys.path.insert(0, str(Path(__file__).resolve().parent))
import importlib
import story_canvas


st.set_page_config(
    page_title="Spotify · Dashboard Story",
    page_icon="♫",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Streamlit supplies the Python data runtime. The embedded canvas owns the
# viewport and behaves like one fixed Tableau Story sheet.
st.markdown(
    """
    <style>
      html, body, .stApp,
      [data-testid="stAppViewContainer"],
      [data-testid="stMain"],
      .main {height:100vh !important; overflow:hidden !important;}
      header[data-testid="stHeader"], footer, #MainMenu,
      [data-testid="stToolbar"], [data-testid="stDecoration"] {display:none !important;}
      [data-testid="stAppViewBlockContainer"], .block-container {
        padding:0 !important; margin:0 !important; max-width:100vw !important;
        width:100vw !important; height:100vh !important;
      }
      [data-testid="stVerticalBlock"], [data-testid="stElementContainer"] {
        gap:0 !important; margin:0 !important;
      }
      iframe[title="streamlit.components.v1.html"], iframe[title="st.iframe"] {
        display:block !important; width:100vw !important; height:100vh !important;
        border:0 !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner="Đang dựng workbook từ 04_story.ipynb…")
def build_story_canvas(source_stamp):
    return importlib.reload(story_canvas).canvas_html()


try:
    source_stamp = tuple((Path(__file__).parent / name).stat().st_mtime_ns
                         for name in ['story_canvas.py', 'story_canvas.html', 'story_interactions.js', 'story_data.py', '../notebooks/04_story.ipynb', '../data/processed/tracks_dimension.csv', '../data/processed/charts_clean.parquet', '../data/processed/mart_artist_chart.parquet', '../data/processed/mart_country_year.parquet', '../data/processed/mart_audio_trend_weekly.parquet', '../data/processed/covid_weekly_clean.csv'])
    components.html(build_story_canvas(source_stamp), height=1000, scrolling=False)
except Exception as exc:
    st.error(f"Không thể dựng Story: {exc}")
    st.caption("Kiểm tra các tệp trong data/processed và khởi động lại ứng dụng.")
