"""Main Executive Dashboard for Spotify Audio Trends & Analytics.
Single-page fixed viewport (100vh No-scroll) built for Gia Hân.
Run with: streamlit run dashboard/main_dashboard.py
"""
import json
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
from plotly.offline import get_plotlyjs

ROOT = Path(__file__).resolve().parent

st.set_page_config(
    page_title="Spotify · Executive Main Dashboard",
    page_icon="♫",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Enforce strict 100vh viewport without scrolling
st.markdown(
    """
    <style>
      html, body, .stApp,
      [data-testid="stAppViewContainer"],
      [data-testid="stMain"],
      .main {
        height: 100vh !important;
        max-height: 100vh !important;
        overflow: hidden !important;
        background-color: #0B111E !important;
      }
      header[data-testid="stHeader"], footer, #MainMenu,
      [data-testid="stToolbar"], [data-testid="stDecoration"] {
        display: none !important;
      }
      [data-testid="stAppViewBlockContainer"], .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100vw !important;
        width: 100vw !important;
        height: 100vh !important;
        max-height: 100vh !important;
        overflow: hidden !important;
      }
      [data-testid="stVerticalBlock"], [data-testid="stElementContainer"] {
        gap: 0 !important;
        margin: 0 !important;
      }
      iframe[title="streamlit.components.v1.html"], iframe[title="st.iframe"] {
        display: block !important;
        width: 100vw !important;
        height: 100vh !important;
        max-height: 100vh !important;
        border: 0 !important;
        overflow: hidden !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

@st.cache_data
def load_bundle_html():
    html_file = ROOT / "main_dashboard.html"
    json_file = ROOT / "main_dashboard_data.json"
    
    html_content = html_file.read_text(encoding="utf-8")
    json_content = json_file.read_text(encoding="utf-8")
    
    # Inject offline Plotly.js and embedded JSON bundle directly so it runs seamlessly offline
    plotly_js = get_plotlyjs()
    html_content = html_content.replace(
        '<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>',
        f'<script>{plotly_js}</script>'
    )
    # Replace fetch with direct inline JSON assignment
    fetch_pattern = """    // Load data from JSON file
    fetch('main_dashboard_data.json')
      .then(r => r.json())
      .then(data => {
        DATA_BUNDLE = data;
        initDashboard();
      })
      .catch(err => {
        console.error("Lỗi nạp dữ liệu:", err);
        document.getElementById('live-insight').innerText = "Đang chạy chế độ kiểm thử hoặc dữ liệu cục bộ.";
      });"""
      
    inline_replacement = f"""    DATA_BUNDLE = {json_content};
    initDashboard();"""
    
    if fetch_pattern in html_content:
        html_content = html_content.replace(fetch_pattern, inline_replacement)
    else:
        # Fallback replacement if whitespace differs
        html_content = html_content.replace("let DATA_BUNDLE = null;", f"let DATA_BUNDLE = {json_content};")
        html_content = html_content.replace("fetch('main_dashboard_data.json')", "// fetch bypassed\n      ")

    return html_content

try:
    dashboard_html = load_bundle_html()
    components.html(dashboard_html, height=1000, scrolling=False)
except Exception as e:
    st.error(f"Lỗi khởi chạy Main Dashboard: {e}")
    st.caption("Kiểm tra file dashboard/main_dashboard.html và dashboard/main_dashboard_data.json.")
