"""
Module quản lý nạp dữ liệu, làm sạch và kết nối (JOIN) 5 bảng dữ liệu.
"""
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
SAMPLE_DATA_DIR = os.path.join(BASE_DIR, "data", "sample")

def load_raw_data():
    """Nạp 5 tập dữ liệu gốc từ thư mục data/raw/"""
    artists = pd.read_csv(os.path.join(RAW_DATA_DIR, "best-selling-artists.csv"))
    country_codes = pd.read_csv(os.path.join(RAW_DATA_DIR, "country_codes.csv"))
    gdp = pd.read_csv(os.path.join(RAW_DATA_DIR, "gdp_data.csv"))
    tracks = pd.read_csv(os.path.join(RAW_DATA_DIR, "spotify-tracks-dataset.csv"))
    
    # weekly charts đã được làm sạch và rút gọn
    charts = pd.read_csv(os.path.join(RAW_DATA_DIR, "spotify-weekly-charts.csv"))
    return artists, country_codes, gdp, tracks, charts

def clean_and_join(sample_size=None):
    """
    Thực hiện tiền xử lý, chuẩn hóa các trường khóa và JOIN 5 bảng dữ liệu.
    """
    artists, country_codes, gdp, tracks, charts = load_raw_data()
    
    if sample_size:
        charts = charts.sample(n=min(sample_size, len(charts)), random_state=42)
    
    # 1. Trích xuất năm từ chuỗi ngày tháng bảng xếp hạng
    charts["year"] = pd.to_datetime(charts["week"], errors="coerce").dt.year
    
    # 3. Kết hợp GDP với Country Codes để có Region và Income Group
    gdp_full = pd.merge(gdp, country_codes, on="country_code", how="left")
    
    # 4. Join Bảng xếp hạng tuần với GDP theo quốc gia và năm
    merged_charts = pd.merge(
        charts,
        gdp_full,
        left_on=["country", "year"],
        right_on=["country_name", "year"],
        how="left"
    )
    
    # 5. Join với đặc trưng bài hát (Tracks dataset)
    tracks_sub = tracks[["track_id", "track_genre", "popularity", "duration_ms", "explicit"]].drop_duplicates("track_id")
    final_df = pd.merge(
        merged_charts,
        tracks_sub,
        on="track_id",
        how="left"
    )
    
    return final_df

if __name__ == "__main__":
    print("Generating sample dataset...")
    df_sample = clean_and_join(sample_size=20000)
    out_path = os.path.join(SAMPLE_DATA_DIR, "spotify_sample_merged.csv")
    df_sample.to_csv(out_path, index=False)
    print(f"Sample dataset successfully saved to: {out_path} ({len(df_sample)} rows)")
