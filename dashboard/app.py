import streamlit as st

st.set_page_config(
    page_title="Spotify Trends & Audio Analytics",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎵 Khám Phá Đặc Trưng Âm Thanh & Dự Đoán Xu Hướng Spotify")
st.markdown("### Đồ án môn học: Tương tác Dữ liệu (Interactive Data Visualization)")

st.markdown("""
Chào mừng bạn đến với hệ thống **Dashboard Phân tích & Tương tác Dữ liệu Âm nhạc Toàn cầu**!
Ứng dụng này khai phá sự kết hợp giữa **hành vi nghe nhạc trực tuyến**, **đặc tính âm học (Audio Features)** và **yếu tố kinh tế - xã hội (GDP, thu nhập)** của từng quốc gia.

---
""")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Bài hát phân tích", "114,000+", "Audio features")
with col2:
    st.metric("Bản ghi tuần Charts", "314,000+", "Toàn cầu (Đã lọc)")
with col3:
    st.metric("Quốc gia khảo sát", "70+", "Kèm số liệu GDP")
with col4:
    st.metric("Mô hình dự báo", "Linear & Logistic", "Trending Predictor")

st.markdown("""
---
### 🧭 Hướng Dẫn Điều Hướng (Navigation):
Vui lòng sử dụng **Thanh điều hướng (Sidebar)** bên trái để truy cập các trang chuyên biệt:

1. **📊 1. Tổng quan Dữ liệu:** Khám phá cấu trúc 5 bảng dữ liệu, Data Dictionary và phân phối chung.
2. **🎵 2. Đặc trưng Âm thanh:** Phân tích tương quan giữa các Audio Features (*Danceability*, *Energy*, *Valence*...).
3. **🌍 3. Kinh tế & Âm nhạc:** Khám phá sự tương quan giữa GDP, mức thu nhập quốc gia và sở thích nghe nhạc.
4. **🤖 4. Dự báo Thịnh hành:** Công cụ tương tác dự đoán khả năng lọt Top Trending của bài hát dựa trên mô hình Machine Learning.
5. **📖 5. Câu chuyện Dữ liệu (Storytelling):** Những phát hiện và câu chuyện đằng sau dữ liệu lớn.
""")

st.sidebar.success("Chọn trang phân tích từ danh sách phía trên.")
