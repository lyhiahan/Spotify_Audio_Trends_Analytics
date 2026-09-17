"""
src/data_loader.py
==================
Pipeline ETL nạp, làm sạch và kết nối 5 bảng dữ liệu thành 1 tệp Master duy nhất phục vụ Insight
và xuất các tệp mẫu rút gọn (Sample) cho nhóm phát triển & Machine Learning.

Kiến trúc tệp đầu ra:
    1. Tệp Master lớn duy nhất (Toàn bộ dữ liệu phục vụ Insight: Kinh tế 74 nước & COVID Timeline):
       -> data/processed/merged_spotify_data.csv (41 cột cốt lõi phục vụ Insight)
    2. Tệp Sample rút gọn phục vụ phát triển Dashboard:
       -> data/sample/spotify_sample_merged.csv (20,000 dòng × 41 cột)
    3. Tệp Sample cấp độ bài hát chuyên dụng cho Machine Learning (Thành Tài):
       -> data/sample/tracks_sample_ml.csv (Song-level, chống 100% Data Leakage)

Author: Đinh Quốc Anh (Data Engineer & Data Analyst)
"""

import os
import re
import sys
import io
import warnings
from datetime import datetime
import numpy as np
import pandas as pd

# Đảm bảo in tiếng Việt & emoji trên mọi hệ điều hành (kể cả Windows cp1252)
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

warnings.filterwarnings("ignore")

# Cấu hình đường dẫn
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
SAMPLE_DIR = os.path.join(BASE_DIR, "data", "sample")

# Cấu hình phân tích
AUDIO_FEATURES = [
    "danceability", "energy", "loudness", "speechiness",
    "acousticness", "instrumentalness", "liveness", "valence", "tempo"
]
AUDIO_0_1 = [
    "danceability", "energy", "speechiness", "acousticness",
    "instrumentalness", "liveness", "valence"
]
TRENDING_THRESHOLD = 50   # rank <= 50 -> is_trending = 1
POPULAR_THRESHOLD = 70    # popularity >= 70 -> is_popular = 1

# Từ khóa phát hiện thể loại Latin
LATIN_KEYWORDS = [
    "latin", "reggaeton", "salsa", "bachata", "merengue", "cumbia",
    "trap latino", "latin pop", "latin hip hop", "urbano", "vallenato",
    "corrido", "norteño", "ranchera", "sertanejo", "funk carioca",
    "bossa nova", "mpb", "forró", "pagode", "axé", "argentine",
    "colombian", "brazilian", "mexican", "puerto rican", "cuarteto",
    "dembow", "reggae", "cubano", "tropical", "chicano"
]
# Từ khóa phát hiện K-Pop
KPOP_KEYWORDS = ["k-pop", "kpop", "korean", "k pop"]

# Danh sách chuẩn hóa 41 cột cốt lõi phục vụ Insight
FINAL_INSIGHT_COLUMNS = [
    # 1. Nhận dạng & Không gian & Thời gian (10 cột)
    "track_id", "track_name", "artist_individual", "artist_genre",
    "country", "language", "week", "year", "month", "quarter",
    # 2. Xếp hạng & Lượt nghe (5 cột)
    "rank", "streams", "log_streams", "weeks_on_chart", "peak_rank",
    # 3. 9 Audio Features (9 cột)
    "danceability", "energy", "loudness", "speechiness",
    "acousticness", "instrumentalness", "liveness", "valence", "tempo",
    # 4. Kinh tế - Xã hội World Bank (5 cột)
    "gdp_value", "gdp_log", "income_group", "region_wb", "country_code",
    # 5. Calculated Fields phục vụ 5 bài toán Insight (12 cột)
    "is_trending", "is_popular", "mood_category", "stream_share_country",
    "covid_phase", "energy_loudness_index", "is_latin", "is_kpop",
    "is_legacy_artist", "duration_min", "audio_diversity_score", "track_genre"
]


# ===============================================================
# GIAI ĐOẠN 1: NẠP VÀ LÀM SẠCH ĐỘC LẬP TỪNG BẢNG (RAW CLEANING)
# ===============================================================

def load_raw_data():
    """Nạp 5 tập dữ liệu gốc từ thư mục data/raw/."""
    print("=" * 60)
    print("📂 BƯỚC 1: NẠP DỮ LIỆU THÔ")
    print("=" * 60)

    # 1. Weekly Charts (~796.6 MB)
    print("  ⏳ Đang nạp spotify-weekly-charts.csv (~796.6 MB)...")
    charts = pd.read_csv(
        os.path.join(RAW_DIR, "spotify-weekly-charts.csv"),
        low_memory=False
    )
    print(f"  ✅ Weekly Charts: {charts.shape[0]:,} dòng × {charts.shape[1]} cột")

    # 2. Tracks Dataset (~19.8 MB)
    print("  ⏳ Đang nạp spotify-tracks-dataset.csv...")
    tracks = pd.read_csv(
        os.path.join(RAW_DIR, "spotify-tracks-dataset.csv"),
        low_memory=False
    )
    print(f"  ✅ Tracks Dataset: {tracks.shape[0]:,} dòng × {tracks.shape[1]} cột")

    # 3. GDP Data
    print("  ⏳ Đang nạp gdp_data.csv...")
    gdp = pd.read_csv(os.path.join(RAW_DIR, "gdp_data.csv"))
    print(f"  ✅ GDP Data: {gdp.shape[0]:,} dòng × {gdp.shape[1]} cột")

    # 4. Country Codes
    print("  ⏳ Đang nạp country_codes.csv...")
    country_codes = pd.read_csv(os.path.join(RAW_DIR, "country_codes.csv"))
    print(f"  ✅ Country Codes: {country_codes.shape[0]:,} dòng × {country_codes.shape[1]} cột")

    # 5. Best-Selling Artists
    print("  ⏳ Đang nạp best-selling-artists.csv...")
    artists = pd.read_csv(os.path.join(RAW_DIR, "best-selling-artists.csv"))
    print(f"  ✅ Best-Selling Artists: {artists.shape[0]:,} dòng × {artists.shape[1]} cột")

    total = sum(len(df) for df in [charts, tracks, gdp, country_codes, artists])
    print(f"\n  📊 Tổng cộng: {total:,} bản ghi từ 5 bảng")
    return charts, tracks, gdp, country_codes, artists


def clean_raw_charts(df):
    """
    Làm sạch độc lập bảng spotify-weekly-charts.csv.
    Khử trùng lặp, ép kiểu numeric cho audio features, lọc bỏ cột rác.
    """
    print("\n" + "=" * 60)
    print("🧹 BƯỚC 2: LÀM SẠCH BẢNG XẾP HẠNG TUẦN (CHARTS)")
    print("=" * 60)

    df = df.copy()
    n_before = len(df)

    # Loại bỏ index thừa
    unnamed_cols = [c for c in df.columns if "Unnamed" in str(c)]
    if unnamed_cols:
        df.drop(columns=unnamed_cols, inplace=True)

    # Trích xuất track_id từ uri
    if "track_id" not in df.columns and "uri" in df.columns:
        df["track_id"] = df["uri"].str.replace("spotify:track:", "", regex=False)

    # Chuyển đổi week -> datetime + trích thời gian
    df["week"] = pd.to_datetime(df["week"], errors="coerce")
    df["year"] = df["week"].dt.year.astype("Int64")
    df["month"] = df["week"].dt.month.astype("Int64")
    df["quarter"] = df["week"].dt.quarter.astype("Int64")
    df.dropna(subset=["week"], inplace=True)

    # Làm sạch streams
    df["streams"] = pd.to_numeric(df["streams"], errors="coerce").fillna(0).astype(int)
    df = df[df["streams"] > 0]

    # Ép kiểu cột thứ hạng
    for col in ["rank", "weeks_on_chart", "peak_rank"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    # Chuẩn hóa tên quốc gia
    df["country"] = df["country"].str.strip()

    # Ép kiểu duration
    if "duration" in df.columns:
        df["duration"] = pd.to_numeric(df["duration"], errors="coerce")

    # Ép kiểu số thực cho 9 audio features
    for col in AUDIO_FEATURES:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Khử trùng lặp bản ghi (track_id + week + country)
    df.drop_duplicates(subset=["track_id", "week", "country"], keep="first", inplace=True)

    # Loại bỏ sớm 15 cột không cần thiết cho Insight
    drop_cols = [
        "uri", "artist_names", "artists_num", "artist_id",
        "key", "mode", "source", "album_num_tracks", "collab",
        "release_date", "previous_rank", "artist_img", "album_cover",
        "pivot", "region", "region_spotify", "region_x"
    ]
    existing_drops = [c for c in drop_cols if c in df.columns]
    if existing_drops:
        df.drop(columns=existing_drops, inplace=True)

    print(f"  📊 Charts sau làm sạch: {n_before:,} -> {len(df):,} dòng, {len(df.columns)} cột")
    return df


def clean_raw_tracks(df):
    """
    Làm sạch bảng spotify-tracks-dataset.csv.
    Dedup track_id theo popularity cao nhất, kiểm định miền giá trị âm học.
    """
    df = df.copy()

    unnamed_cols = [c for c in df.columns if "Unnamed" in str(c)]
    if unnamed_cols:
        df.drop(columns=unnamed_cols, inplace=True)

    # Dedup track_id giữ popularity cao nhất
    if "popularity" in df.columns:
        df = df.sort_values("popularity", ascending=False).drop_duplicates("track_id", keep="first")
    else:
        df = df.drop_duplicates("track_id", keep="first")

    # Validate boundary âm học [0, 1]
    for col in AUDIO_0_1:
        if col in df.columns:
            df[col] = df[col].clip(0, 1)

    if "loudness" in df.columns:
        df["loudness"] = df["loudness"].clip(-60, 5)
    if "tempo" in df.columns:
        df["tempo"] = df["tempo"].clip(0, 300)

    # Lọc chỉ giữ 3 cột cần thiết cho JOIN
    keep = [c for c in ["track_id", "track_genre", "popularity"] if c in df.columns]
    df = df[keep]
    print(f"  📊 Tracks sau làm sạch: {len(df):,} bài hát độc nhất")
    return df


def clean_raw_artists(df):
    """Làm sạch bảng best-selling-artists.csv."""
    df = df.copy()
    df["artist_name_clean"] = df["Artist name"].str.strip().str.lower()
    df.rename(columns={"Artist name": "legacy_artist_name"}, inplace=True)
    out = df[["artist_name_clean", "legacy_artist_name"]].drop_duplicates("artist_name_clean")
    print(f"  📊 Best-Selling Artists: {len(out):,} nghệ sĩ huyền thoại")
    return out


def clean_raw_gdp(df):
    """Làm sạch bảng gdp_data.csv."""
    df = df.copy()
    unnamed_cols = [c for c in df.columns if "Unnamed" in str(c)]
    if unnamed_cols:
        df.drop(columns=unnamed_cols, inplace=True)
    if "value" in df.columns:
        df.rename(columns={"value": "gdp_value"}, inplace=True)
    df["gdp_value"] = pd.to_numeric(df["gdp_value"], errors="coerce")
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    return df[["country_name", "country_code", "year", "gdp_value"]].dropna(subset=["country_name", "year"])


def clean_raw_country_codes(df):
    """Làm sạch bảng country_codes.csv."""
    df = df.copy()
    unnamed_cols = [c for c in df.columns if "Unnamed" in str(c)]
    if unnamed_cols:
        df.drop(columns=unnamed_cols, inplace=True)
    if "region" in df.columns:
        df.rename(columns={"region": "region_wb"}, inplace=True)
    return df[["country_code", "region_wb", "income_group"]].dropna(subset=["country_code"])


# ===============================================================
# GIAI ĐOẠN 2: XÂY DỰNG MASTER DATASET HỢP NHẤT (41 CỘT INSIGHT)
# ===============================================================

def build_master_dataset(charts, gdp, country_codes, tracks, artists, save=True):
    """
    Xây dựng tệp dữ liệu lớn duy nhất (Master Dataset) tích hợp cả Kinh tế - Xã hội và COVID Timeline.
    Lọc giữ chính xác 41 cột phục vụ Insight cho đồ án.
    """
    print("\n" + "=" * 60)
    print("🌍 BƯỚC 3: XÂY DỰNG MASTER DATASET HỢP NHẤT (41 CỘT INSIGHT)")
    print("=" * 60)

    # 1. Lọc chuỗi thời gian trọng tâm 2020 - 2022 (Bao quát cả 3 pha COVID và dữ liệu 74 quốc gia)
    df = charts[charts["year"].isin([2020, 2021, 2022])].copy()
    print(f"  🔹 Lọc Charts 2020 - 2022: {len(df):,} dòng")

    # 2. JOIN 1: Charts + GDP (country + year)
    print("  🔹 JOIN 1: Charts ⋈ GDP...")
    df = pd.merge(
        df,
        gdp[["country_name", "country_code", "year", "gdp_value"]],
        left_on=["country", "year"],
        right_on=["country_name", "year"],
        how="left"
    )

    # 3. JOIN 2: + Country Codes (country_code)
    print("  🔹 JOIN 2: + Country Codes (World Bank)...")
    df = pd.merge(df, country_codes, on="country_code", how="left")

    # 4. JOIN 3: + Tracks Dataset (track_id)
    print("  🔹 JOIN 3: + Tracks Dataset (Audio Genres & Popularity)...")
    df = pd.merge(df, tracks, on="track_id", how="left")

    # 5. JOIN 4: + Best-Selling Artists (artist_name)
    print("  🔹 JOIN 4: + Best-Selling Artists...")
    df["_artist_clean"] = df["artist_individual"].str.strip().str.lower()
    df = pd.merge(df, artists, left_on="_artist_clean", right_on="artist_name_clean", how="left")

    # 6. Tính toán toàn bộ các Calculated Fields phục vụ Insight
    print("  🔹 Tính toán các Calculated Fields...")

    # covid_phase (3 pha đại dịch toàn cầu)
    df["covid_phase"] = "Unknown"
    df.loc[df["year"] <= 2020, "covid_phase"] = "Lockdown & Shock"
    df.loc[df["year"] == 2021, "covid_phase"] = "Vaccine & Escapism"
    df.loc[df["year"] >= 2022, "covid_phase"] = "Reopening & New Normal"

    # is_trending (Hit Top 50) & is_popular (Spotify Popularity >= 70)
    df["is_trending"] = (df["rank"] <= TRENDING_THRESHOLD).astype(int)
    df["is_popular"] = 0
    mask_pop = df["popularity"].notna() & (df["popularity"] >= POPULAR_THRESHOLD)
    df.loc[mask_pop, "is_popular"] = 1

    # mood_category (Mô hình Russell 4 góc phần tư)
    v_hi = df["valence"] >= 0.5
    e_hi = df["energy"] >= 0.5
    df["mood_category"] = "Unknown"
    df.loc[v_hi & e_hi, "mood_category"] = "Happy Energetic"
    df.loc[v_hi & ~e_hi, "mood_category"] = "Peaceful Positive"
    df.loc[~v_hi & e_hi, "mood_category"] = "Tense Aggressive"
    df.loc[~v_hi & ~e_hi, "mood_category"] = "Sad Melancholic"

    # stream_share_country (Thị phần lượt nghe theo tuần tại từng quốc gia)
    total_streams = df.groupby(["country", "week"])["streams"].transform("sum")
    df["stream_share_country"] = np.where(total_streams > 0, df["streams"] / total_streams, 0)

    # energy_loudness_index (Chỉ số cường độ âm thanh gộp chuẩn hóa)
    l_min = df["loudness"].min()
    l_range = df["loudness"].max() - l_min
    l_norm = (df["loudness"] - l_min) / l_range if l_range > 0 else 0.5
    df["energy_loudness_index"] = (df["energy"] + l_norm) / 2

    # is_latin & is_kpop (Làn sóng âm nhạc toàn cầu)
    genre_combo = df["artist_genre"].fillna("").str.lower() + " " + df["track_genre"].fillna("").str.lower()
    latin_pat = "|".join(re.escape(kw) for kw in LATIN_KEYWORDS)
    lang_latin = df["language"].fillna("").str.lower().isin(["spanish", "portuguese"])
    df["is_latin"] = (genre_combo.str.contains(latin_pat, na=False) | lang_latin).astype(int)

    kpop_pat = "|".join(re.escape(kw) for kw in KPOP_KEYWORDS)
    lang_kr = df["language"].fillna("").str.lower().isin(["korean"])
    df["is_kpop"] = (genre_combo.str.contains(kpop_pat, na=False) | lang_kr).astype(int)

    # is_legacy_artist
    df["is_legacy_artist"] = df["legacy_artist_name"].notna().astype(int)

    # duration_min
    if "duration" in df.columns:
        df["duration_min"] = df["duration"] / 60_000

    # audio_diversity_score
    div_cols = ["danceability", "energy", "valence", "acousticness"]
    df["audio_diversity_score"] = df[div_cols].std(axis=1)

    # log_streams & gdp_log
    df["log_streams"] = np.log1p(df["streams"])
    df["gdp_log"] = np.log1p(df["gdp_value"])

    # 7. Lọc giữ chính xác 41 cột phục vụ Insight
    final_cols = [c for c in FINAL_INSIGHT_COLUMNS if c in df.columns]
    df = df[final_cols]

    print(f"  ✅ Master Dataset hoàn chỉnh: {len(df):,} dòng × {len(df.columns)} cột")

    # 8. Xuất file Master
    if save:
        os.makedirs(PROCESSED_DIR, exist_ok=True)
        out_path = os.path.join(PROCESSED_DIR, "merged_spotify_data.csv")
        df.to_csv(out_path, index=False)
        mb = os.path.getsize(out_path) / (1024 * 1024)
        print(f"  💾 Đã lưu File Master: {out_path} ({len(df):,} dòng, {mb:.1f} MB)")

    return df


# ===============================================================
# GIAI ĐOẠN 3: SINH CÁC TẬP SAMPLE CHO NHÓM VÀ MACHINE LEARNING
# ===============================================================

def generate_sample_datasets(df_master, sample_size=20000, save=True):
    """
    Sinh 2 tệp sample gọn nhẹ trong data/sample/:
    1. spotify_sample_merged.csv: 20,000 dòng đầy đủ 41 cột cho Dashboard & EDA.
    2. tracks_sample_ml.csv: Dữ liệu Song-level chuẩn hóa cho Thành Tài làm ML.
    """
    print("\n" + "=" * 60)
    print("🔬 BƯỚC 4: SINH CÁC TẬP SAMPLE PHỤC VỤ NHÓM & MACHINE LEARNING")
    print("=" * 60)

    os.makedirs(SAMPLE_DIR, exist_ok=True)

    # 1. Sample cho Dashboard & EDA (20,000 dòng có đầy đủ 41 cột)
    sample_df = df_master.sample(n=min(sample_size, len(df_master)), random_state=42)
    sample_path = os.path.join(SAMPLE_DIR, "spotify_sample_merged.csv")
    if save:
        sample_df.to_csv(sample_path, index=False)
        mb1 = os.path.getsize(sample_path) / (1024 * 1024)
        print(f"  💾 [Sample 1] Dashboard Sample: {sample_path} ({len(sample_df):,} dòng × {len(sample_df.columns)} cột, {mb1:.1f} MB)")

    # 2. Sample Song-level cho Thành Tài (Machine Learning không bị rò rỉ dữ liệu)
    # Gom nhóm theo track_id độc nhất từ sample
    agg_rules = {
        "track_name": "first",
        "artist_individual": "first",
        "artist_genre": "first",
        "language": "first",
        "danceability": "first",
        "energy": "first",
        "loudness": "first",
        "speechiness": "first",
        "acousticness": "first",
        "instrumentalness": "first",
        "liveness": "first",
        "valence": "first",
        "tempo": "first",
        "duration_min": "first",
        "is_latin": "first",
        "is_kpop": "first",
        "is_trending": "max"  # 1 nếu từng lọt Top 50 trong sample
    }
    avail_rules = {k: v for k, v in agg_rules.items() if k in df_master.columns}
    ml_sample = df_master.groupby("track_id").agg(avail_rules).reset_index()

    ml_path = os.path.join(SAMPLE_DIR, "tracks_sample_ml.csv")
    if save:
        ml_sample.to_csv(ml_path, index=False)
        mb2 = os.path.getsize(ml_path) / (1024 * 1024)
        hit_rate = ml_sample["is_trending"].mean() * 100 if "is_trending" in ml_sample.columns else 0
        print(f"  💾 [Sample 2] ML Dataset cho Thành Tài: {ml_path} ({len(ml_sample):,} bài hát độc nhất × {len(ml_sample.columns)} cột, {mb2:.1f} MB, Tỷ lệ Hit: {hit_rate:.1f}%)")

    return sample_df, ml_sample


# ===============================================================
# GIAI ĐOẠN 4: HÀM ĐIỀU PHỐI CHÍNH & HÀM NẠP TIỆN ÍCH
# ===============================================================

def run_full_pipeline(sample_size=None, save=True):
    """Chạy toàn bộ quy trình: Nạp thô -> Làm sạch -> Master Dataset -> Các tệp Sample."""
    t0 = datetime.now()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  🚀 SPOTIFY AUDIO TRENDS — UNIFIED MASTER DATA PIPELINE  ║")
    print("║  1 File Master (41 cột Insight) & Sample cho Thành Tài   ║")
    print(f"║  Bắt đầu: {t0:%Y-%m-%d %H:%M:%S}                          ║")
    print("╚══════════════════════════════════════════════════════════╝")

    # 1. Nạp dữ liệu thô
    charts, tracks, gdp, country_codes, artists = load_raw_data()

    if sample_size:
        print(f"\n  ⚡ CHẾ ĐỘ SAMPLE: lấy {sample_size:,} dòng từ Charts để chạy thử nghiệm")
        charts = charts.sample(n=min(sample_size, len(charts)), random_state=42)

    # 2. Làm sạch độc lập
    charts_clean = clean_raw_charts(charts)
    tracks_clean = clean_raw_tracks(tracks)
    artists_clean = clean_raw_artists(artists)
    gdp_clean = clean_raw_gdp(gdp)
    country_codes_clean = clean_raw_country_codes(country_codes)

    # 3. Xây dựng Master Dataset
    df_master = build_master_dataset(
        charts_clean, gdp_clean, country_codes_clean, tracks_clean, artists_clean, save=save
    )

    # 4. Sinh các tệp Sample
    df_sample, df_ml = generate_sample_datasets(df_master, sample_size=20000, save=save)

    elapsed = datetime.now() - t0
    print("\n" + "=" * 60)
    print(f"🎉 PIPELINE HOÀN THÀNH TRONG: {elapsed}")
    print("=" * 60)
    return df_master, df_sample, df_ml


# Các hàm tiện ích nạp dữ liệu cho Dashboard, Notebooks và ML
def load_master_data(nrows=None):
    """Nạp tệp Master dữ liệu lớn (merged_spotify_data.csv)."""
    p = os.path.join(PROCESSED_DIR, "merged_spotify_data.csv")
    if not os.path.exists(p):
        raise FileNotFoundError(f"File chưa tồn tại: {p}\nChạy: python src/data_loader.py")
    df = pd.read_csv(p, nrows=nrows, low_memory=False)
    df["week"] = pd.to_datetime(df["week"], errors="coerce")
    print(f"✅ Nạp Master Data: {len(df):,} dòng × {len(df.columns)} cột")
    return df


def load_sample_data():
    """Nạp tệp sample đa dụng 20,000 dòng có đầy đủ 41 cột (phục vụ Dashboard và EDA)."""
    p = os.path.join(SAMPLE_DIR, "spotify_sample_merged.csv")
    if not os.path.exists(p):
        raise FileNotFoundError(f"File chưa tồn tại: {p}\nChạy: python src/data_loader.py")
    df = pd.read_csv(p, low_memory=False)
    df["week"] = pd.to_datetime(df["week"], errors="coerce")
    print(f"✅ Nạp Sample: {len(df):,} dòng × {len(df.columns)} cột")
    return df


def load_ml_sample():
    """Nạp tệp sample cấp độ bài hát (Song-level) chuyên dụng cho Thành Tài làm ML."""
    p = os.path.join(SAMPLE_DIR, "tracks_sample_ml.csv")
    if not os.path.exists(p):
        raise FileNotFoundError(f"File chưa tồn tại: {p}\nChạy: python src/data_loader.py")
    df = pd.read_csv(p)
    print(f"✅ Nạp ML Sample (Thành Tài): {len(df):,} bài hát × {len(df.columns)} cột")
    return df


def data_quality_report(df, name="Dataset"):
    """Tạo bảng báo cáo chất lượng dữ liệu."""
    report = pd.DataFrame({
        "Column": df.columns,
        "Dtype": df.dtypes.astype(str).values,
        "Non-Null": df.notna().sum().values,
        "Null": df.isnull().sum().values,
        "Null%": (df.isnull().mean() * 100).round(2).values,
        "Unique": df.nunique().values,
    })
    print(f"\n📋 Data Quality — {name} ({len(df):,} rows × {len(df.columns)} cols)")
    return report


# Các alias tên hàm tương thích ngược
clean_weekly_charts = clean_raw_charts
clean_tracks_dataset = clean_raw_tracks
clean_best_selling_artists = clean_raw_artists
join_all_tables = build_master_dataset


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--sample":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 20_000
        print(f"🔬 Chế độ sample ({n:,} dòng)…")
        run_full_pipeline(sample_size=n)
    else:
        run_full_pipeline()
