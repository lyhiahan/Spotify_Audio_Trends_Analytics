"""
src/data_loader.py
==================
Pipeline ETL phân nhánh tối ưu (Branching Pipeline) nạp, làm sạch và kết nối 5 bảng dữ liệu.

Kiến trúc 3 nhánh chuyên biệt:
    1. Nhánh Kinh tế - Xã hội & Bản đồ (2021 - 2022, 74 quốc gia)
       -> data/processed/spotify_socioeconomic_2021_2022.csv
       -> data/sample/spotify_sample_merged.csv (Sample 20K dòng)
    2. Nhánh Dòng thời gian Đại dịch COVID-19 (2020 - 2022, Global)
       -> data/processed/spotify_covid_timeline_2020_2022.csv
    3. Nhánh Machine Learning cấp độ bài hát (Song-level, chống Data Leakage)
       -> data/processed/tracks_ml_dataset.csv

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

# Danh sách cột chuẩn hóa cho Nhánh 1 (Kinh tế - Xã hội)
FINAL_SOCIOECONOMIC_COLUMNS = [
    # Nhận dạng & Thời gian
    "track_id", "track_name", "artist_individual", "artist_genre",
    "country", "language", "week", "year", "month", "quarter",
    # Xếp hạng & Streams
    "rank", "streams", "log_streams", "weeks_on_chart", "peak_rank",
    # 9 Audio Features
    "danceability", "energy", "loudness", "speechiness",
    "acousticness", "instrumentalness", "liveness", "valence", "tempo",
    # Kinh tế – Xã hội
    "gdp_value", "gdp_log", "income_group", "region_wb", "country_code",
    # Calculated Fields
    "is_trending", "is_popular", "mood_category", "stream_share_country",
    "energy_loudness_index", "is_latin", "is_kpop", "is_legacy_artist",
    "duration_min", "audio_diversity_score", "track_genre"
]


# ===============================================================
# GIAI ĐOẠN 1: NẠP VÀ LÀM SẠCH ĐỘC LẬP TỪNG BẢNG (RAW CLEANING)
# ===============================================================

def load_raw_data():
    """Nạp 5 tập dữ liệu gốc từ thư mục data/raw/."""
    print("=" * 60)
    print("📂 BƯỚC 1: NẠP DỮ LIỆU THÔ")
    print("=" * 60)

    # 1. Weekly Charts (~835 MB)
    print("  ⏳ Đang nạp spotify-weekly-charts.csv (~835 MB)...")
    charts = pd.read_csv(
        os.path.join(RAW_DIR, "spotify-weekly-charts.csv"),
        low_memory=False
    )
    print(f"  ✅ Weekly Charts: {charts.shape[0]:,} dòng × {charts.shape[1]} cột")

    # 2. Tracks Dataset (~20 MB)
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

    # Lọc sớm 15 cột không cần thiết trước khi phân nhánh
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

    def _parse_millions(text):
        if pd.isna(text):
            return np.nan
        m = re.search(r"([\d,.]+)\s*million", str(text), re.IGNORECASE)
        if m:
            try:
                return float(m.group(1).replace(",", ""))
            except ValueError:
                return np.nan
        return np.nan

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
# GIAI ĐOẠN 2: 3 NHÁNH XỬ LÝ CHUYÊN BIỆT (BRANCHING PIPELINE)
# ===============================================================

def build_socioeconomic_dataset(charts, gdp, country_codes, tracks, artists, save=True):
    """
    NHÁNH 1: Dữ liệu Kinh tế - Xã hội & Bản đồ thế giới 74 Quốc gia (2021 - 2022).
    Lọc sớm bỏ Global trước khi JOIN -> Tỷ lệ khớp GDP đạt ~98% (không bị null giả tạo).
    """
    print("\n" + "=" * 60)
    print("🌍 NHÁNH 1: XÂY DỰNG DỮ LIỆU KINH TẾ - XÃ HỘI (2021 - 2022)")
    print("=" * 60)

    # 1. Lọc trước khi JOIN (Bỏ Global và chỉ lấy 2021 - 2022)
    df = charts[(charts["year"].isin([2021, 2022])) & (charts["country"] != "Global")].copy()
    print(f"  🔹 Lọc Charts 74 nước (2021-2022): {len(df):,} dòng")

    # 2. JOIN 1: Charts + GDP (country + year)
    df = pd.merge(df, gdp[["country_name", "country_code", "year", "gdp_value"]],
                  left_on=["country", "year"], right_on=["country_name", "year"], how="left")
    rate_gdp = df["gdp_value"].notna().mean() * 100
    print(f"  🔹 JOIN GDP Match rate: {rate_gdp:.1f}% (Gần 100% nhờ loại bỏ Global sớm)")

    # 3. JOIN 2: + Country Codes (country_code)
    df = pd.merge(df, country_codes, on="country_code", how="left")

    # 4. JOIN 3: + Tracks Dataset (track_id)
    df = pd.merge(df, tracks, on="track_id", how="left")

    # 5. JOIN 4: + Best-Selling Artists (artist_name)
    df["_artist_clean"] = df["artist_individual"].str.strip().str.lower()
    df = pd.merge(df, artists, left_on="_artist_clean", right_on="artist_name_clean", how="left")

    # 6. Tính toán Calculated Fields
    df["is_trending"] = (df["rank"] <= TRENDING_THRESHOLD).astype(int)
    df["is_popular"] = 0
    mask_pop = df["popularity"].notna() & (df["popularity"] >= POPULAR_THRESHOLD)
    df.loc[mask_pop, "is_popular"] = 1

    # mood_category (Russell Model)
    v_hi = df["valence"] >= 0.5
    e_hi = df["energy"] >= 0.5
    df["mood_category"] = "Unknown"
    df.loc[v_hi & e_hi, "mood_category"] = "Happy Energetic"
    df.loc[v_hi & ~e_hi, "mood_category"] = "Peaceful Positive"
    df.loc[~v_hi & e_hi, "mood_category"] = "Tense Aggressive"
    df.loc[~v_hi & ~e_hi, "mood_category"] = "Sad Melancholic"

    # stream_share_country
    total_streams = df.groupby(["country", "week"])["streams"].transform("sum")
    df["stream_share_country"] = np.where(total_streams > 0, df["streams"] / total_streams, 0)

    # energy_loudness_index
    l_min = df["loudness"].min()
    l_range = df["loudness"].max() - l_min
    l_norm = (df["loudness"] - l_min) / l_range if l_range > 0 else 0.5
    df["energy_loudness_index"] = (df["energy"] + l_norm) / 2

    # is_latin & is_kpop
    genre_combo = df["artist_genre"].fillna("").str.lower() + " " + df["track_genre"].fillna("").str.lower()
    latin_pat = "|".join(re.escape(kw) for kw in LATIN_KEYWORDS)
    lang_latin = df["language"].fillna("").str.lower().isin(["spanish", "portuguese"])
    df["is_latin"] = (genre_combo.str.contains(latin_pat, na=False) | lang_latin).astype(int)

    kpop_pat = "|".join(re.escape(kw) for kw in KPOP_KEYWORDS)
    lang_kr = df["language"].fillna("").str.lower().isin(["korean"])
    df["is_kpop"] = (genre_combo.str.contains(kpop_pat, na=False) | lang_kr).astype(int)

    df["is_legacy_artist"] = df["legacy_artist_name"].notna().astype(int)
    if "duration" in df.columns:
        df["duration_min"] = df["duration"] / 60_000

    div_cols = ["danceability", "energy", "valence", "acousticness"]
    df["audio_diversity_score"] = df[div_cols].std(axis=1)
    df["log_streams"] = np.log1p(df["streams"])
    df["gdp_log"] = np.log1p(df["gdp_value"])

    # Lọc danh sách cột chuẩn hóa
    final_cols = [c for c in FINAL_SOCIOECONOMIC_COLUMNS if c in df.columns]
    df = df[final_cols]

    # Xuất file
    if save:
        os.makedirs(PROCESSED_DIR, exist_ok=True)
        os.makedirs(SAMPLE_DIR, exist_ok=True)

        f1_path = os.path.join(PROCESSED_DIR, "spotify_socioeconomic_2021_2022.csv")
        df.to_csv(f1_path, index=False)
        mb1 = os.path.getsize(f1_path) / (1024 * 1024)
        print(f"  💾 Đã lưu File 1: {f1_path} ({len(df):,} dòng, {mb1:.1f} MB)")

        # Sample 20K dòng cho dev nhanh
        sample_df = df.sample(n=min(20_000, len(df)), random_state=42)
        samp_path = os.path.join(SAMPLE_DIR, "spotify_sample_merged.csv")
        sample_df.to_csv(samp_path, index=False)
        smb = os.path.getsize(samp_path) / (1024 * 1024)
        print(f"  💾 Đã lưu Sample: {samp_path} ({len(sample_df):,} dòng, {smb:.1f} MB)")

    return df


def build_covid_timeline_dataset(charts, tracks, artists, save=True):
    """
    NHÁNH 2: Dòng thời gian Đại dịch COVID-19 (Global 2020 - 2022).
    Bỏ qua hoàn toàn JOIN GDP và Country Codes (vì Global không có GDP) -> Xử lý siêu tốc 0.1s.
    """
    print("\n" + "=" * 60)
    print("🦠 NHÁNH 2: XÂY DỰNG DỮ LIỆU ĐẠI DỊCH COVID-19 (GLOBAL 2020 - 2022)")
    print("=" * 60)

    # 1. Lọc bảng Global 2020 - 2022
    df = charts[(charts["country"] == "Global") & (charts["year"].isin([2020, 2021, 2022]))].copy()
    print(f"  🔹 Lọc Charts Global (2020-2022): {len(df):,} dòng")

    # 2. JOIN Tracks (lấy thể loại) & Artists (lấy legacy status)
    df = pd.merge(df, tracks, on="track_id", how="left")
    df["_artist_clean"] = df["artist_individual"].str.strip().str.lower()
    df = pd.merge(df, artists, left_on="_artist_clean", right_on="artist_name_clean", how="left")

    # 3. Tính toán 3 Pha đại dịch COVID-19
    df["covid_phase"] = "Unknown"
    df.loc[df["year"] <= 2020, "covid_phase"] = "Lockdown & Shock"
    df.loc[df["year"] == 2021, "covid_phase"] = "Vaccine & Escapism"
    df.loc[df["year"] >= 2022, "covid_phase"] = "Reopening & New Normal"

    # mood_category (Russell Model)
    v_hi = df["valence"] >= 0.5
    e_hi = df["energy"] >= 0.5
    df["mood_category"] = "Unknown"
    df.loc[v_hi & e_hi, "mood_category"] = "Happy Energetic"
    df.loc[v_hi & ~e_hi, "mood_category"] = "Peaceful Positive"
    df.loc[~v_hi & e_hi, "mood_category"] = "Tense Aggressive"
    df.loc[~v_hi & ~e_hi, "mood_category"] = "Sad Melancholic"

    # energy_loudness_index
    l_min = df["loudness"].min()
    l_range = df["loudness"].max() - l_min
    l_norm = (df["loudness"] - l_min) / l_range if l_range > 0 else 0.5
    df["energy_loudness_index"] = (df["energy"] + l_norm) / 2

    # Các cờ bổ trợ
    df["is_trending"] = (df["rank"] <= TRENDING_THRESHOLD).astype(int)
    df["is_legacy_artist"] = df["legacy_artist_name"].notna().astype(int)
    if "duration" in df.columns:
        df["duration_min"] = df["duration"] / 60_000
    df["log_streams"] = np.log1p(df["streams"])

    div_cols = ["danceability", "energy", "valence", "acousticness"]
    df["audio_diversity_score"] = df[div_cols].std(axis=1)

    # Dọn dẹp cột tạm
    drop_temp = ["_artist_clean", "artist_name_clean", "legacy_artist_name", "duration", "popularity"]
    df.drop(columns=[c for c in drop_temp if c in df.columns], inplace=True)

    if save:
        os.makedirs(PROCESSED_DIR, exist_ok=True)
        f2_path = os.path.join(PROCESSED_DIR, "spotify_covid_timeline_2020_2022.csv")
        df.to_csv(f2_path, index=False)
        mb2 = os.path.getsize(f2_path) / (1024 * 1024)
        print(f"  💾 Đã lưu File 2: {f2_path} ({len(df):,} dòng × {len(df.columns)} cột, {mb2:.1f} MB)")

    return df


def build_ml_dataset(charts, save=True):
    """
    NHÁNH 3: Dữ liệu Huấn luyện Machine Learning (Thành Tài).
    Gom nhóm theo track_id độc nhất (Song-level) -> Loại bỏ hoàn toàn Data Leakage.
    """
    print("\n" + "=" * 60)
    print("🤖 NHÁNH 3: XÂY DỰNG DỮ LIỆU MACHINE LEARNING (SONG-LEVEL)")
    print("=" * 60)

    # 1. Gom nhóm theo từng bài hát duy nhất từ bảng Charts
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
        # Nhãn mục tiêu: 1 nếu bài hát đã từng lọt Top 50, 0 nếu không
        "rank": lambda r: int((r <= TRENDING_THRESHOLD).any())
    }
    if "duration" in charts.columns:
        agg_rules["duration"] = "first"

    df_ml = charts.groupby("track_id").agg(agg_rules).reset_index()
    df_ml.rename(columns={"rank": "is_trending"}, inplace=True)

    # 2. Tính duration_min, is_latin, is_kpop
    if "duration" in df_ml.columns:
        df_ml["duration_min"] = df_ml["duration"] / 60_000
        df_ml.drop(columns=["duration"], inplace=True)

    genre_str = df_ml["artist_genre"].fillna("").str.lower()
    latin_pat = "|".join(re.escape(kw) for kw in LATIN_KEYWORDS)
    lang_latin = df_ml["language"].fillna("").str.lower().isin(["spanish", "portuguese"])
    df_ml["is_latin"] = (genre_str.str.contains(latin_pat, na=False) | lang_latin).astype(int)

    kpop_pat = "|".join(re.escape(kw) for kw in KPOP_KEYWORDS)
    lang_kr = df_ml["language"].fillna("").str.lower().isin(["korean"])
    df_ml["is_kpop"] = (genre_str.str.contains(kpop_pat, na=False) | lang_kr).astype(int)

    print(f"  📊 ML Dataset: {len(df_ml):,} bài hát độc nhất × {len(df_ml.columns)} cột")
    print(f"     Tỷ lệ nhãn Hit (is_trending = 1): {df_ml['is_trending'].mean()*100:.1f}%")

    if save:
        os.makedirs(PROCESSED_DIR, exist_ok=True)
        f3_path = os.path.join(PROCESSED_DIR, "tracks_ml_dataset.csv")
        df_ml.to_csv(f3_path, index=False)
        mb3 = os.path.getsize(f3_path) / (1024 * 1024)
        print(f"  💾 Đã lưu File 3: {f3_path} ({len(df_ml):,} dòng, {mb3:.1f} MB)")

    return df_ml


# ===============================================================
# GIAI ĐOẠN 3: HÀM ĐIỀU PHỐI CHÍNH & TIỆN ÍCH
# ===============================================================

def run_full_pipeline(sample_size=None, save=True):
    """
    Chạy toàn bộ Branching Pipeline: Nạp thô -> Làm sạch -> 3 Nhánh chuyên biệt.
    """
    t0 = datetime.now()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  🚀 SPOTIFY AUDIO TRENDS — BRANCHING DATA PIPELINE       ║")
    print("║  3 Nhánh chuyên biệt: Kinh tế • COVID • Machine Learning ║")
    print(f"║  Bắt đầu: {t0:%Y-%m-%d %H:%M:%S}                          ║")
    print("╚══════════════════════════════════════════════════════════╝")

    # 1. Nạp dữ liệu thô
    charts, tracks, gdp, country_codes, artists = load_raw_data()

    if sample_size:
        print(f"\n  ⚡ CHẾ ĐỘ SAMPLE: lấy {sample_size:,} dòng từ Charts")
        charts = charts.sample(n=min(sample_size, len(charts)), random_state=42)

    # 2. Làm sạch độc lập
    charts_clean = clean_raw_charts(charts)
    tracks_clean = clean_raw_tracks(tracks)
    artists_clean = clean_raw_artists(artists)
    gdp_clean = clean_raw_gdp(gdp)
    country_codes_clean = clean_raw_country_codes(country_codes)

    # 3. Chạy 3 nhánh chuyên biệt
    df_socio = build_socioeconomic_dataset(charts_clean, gdp_clean, country_codes_clean, tracks_clean, artists_clean, save=save)
    df_covid = build_covid_timeline_dataset(charts_clean, tracks_clean, artists_clean, save=save)
    df_ml = build_ml_dataset(charts_clean, save=save)

    elapsed = datetime.now() - t0
    print("\n" + "=" * 60)
    print(f"🎉 PIPELINE HOÀN THÀNH TRONG: {elapsed}")
    print("=" * 60)
    return df_socio, df_covid, df_ml


# Các hàm tiện ích nạp dữ liệu cho Dashboard và Notebooks
def load_socioeconomic_data():
    """Nạp dữ liệu kinh tế - xã hội 74 quốc gia (2021 - 2022)."""
    p = os.path.join(PROCESSED_DIR, "spotify_socioeconomic_2021_2022.csv")
    if not os.path.exists(p):
        raise FileNotFoundError(f"File chưa tồn tại: {p}\nChạy: python src/data_loader.py")
    df = pd.read_csv(p, low_memory=False)
    df["week"] = pd.to_datetime(df["week"], errors="coerce")
    print(f"✅ Nạp Socioeconomic: {len(df):,} dòng × {len(df.columns)} cột")
    return df


def load_covid_data():
    """Nạp dữ liệu dòng thời gian 3 giai đoạn đại dịch COVID-19 (Global 2020 - 2022)."""
    p = os.path.join(PROCESSED_DIR, "spotify_covid_timeline_2020_2022.csv")
    if not os.path.exists(p):
        raise FileNotFoundError(f"File chưa tồn tại: {p}\nChạy: python src/data_loader.py")
    df = pd.read_csv(p, low_memory=False)
    df["week"] = pd.to_datetime(df["week"], errors="coerce")
    print(f"✅ Nạp COVID Timeline: {len(df):,} dòng × {len(df.columns)} cột")
    return df


def load_ml_data():
    """Nạp dữ liệu cấp độ bài hát (Song-level) chuyên dụng cho Machine Learning."""
    p = os.path.join(PROCESSED_DIR, "tracks_ml_dataset.csv")
    if not os.path.exists(p):
        raise FileNotFoundError(f"File chưa tồn tại: {p}\nChạy: python src/data_loader.py")
    df = pd.read_csv(p)
    print(f"✅ Nạp ML Dataset: {len(df):,} bài hát × {len(df.columns)} cột")
    return df


def load_sample_data():
    """Nạp dữ liệu mẫu từ data/sample/ (test nhanh cho Dashboard)."""
    p = os.path.join(SAMPLE_DIR, "spotify_sample_merged.csv")
    if not os.path.exists(p):
        raise FileNotFoundError(f"File chưa tồn tại: {p}\nChạy: python src/data_loader.py --sample")
    df = pd.read_csv(p, low_memory=False)
    df["week"] = pd.to_datetime(df["week"], errors="coerce")
    print(f"✅ Nạp Sample: {len(df):,} dòng × {len(df.columns)} cột")
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


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--sample":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 20_000
        print(f"🔬 Chế độ sample ({n:,} dòng)…")
        run_full_pipeline(sample_size=n)
    else:
        run_full_pipeline()
