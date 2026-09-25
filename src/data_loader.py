"""
src/data_loader.py

ETL pipeline hoàn chỉnh: nạp 6 bảng dữ liệu thô từ data/raw/, làm sạch,
kết hợp Waterfall bài hát đa nguồn, chuẩn hóa nghệ sĩ, join thành Master Dataset
và xuất file dữ liệu cấp bài hát cho Machine Learning.

6 bảng đầu vào (data/raw/):
    1. spotify-weekly-charts.csv   — Bảng xương sống chuỗi thời gian (Top 200 Weekly)
    2. songs.csv                   — Kho bài hát 550K (Kaggle Serkan Tysz)
    3. spotify-tracks-dataset.csv  — Kho bài hát 114K (Spotify Web API, có explicit)
    4. artists.csv                 — Hồ sơ 71,440 nghệ sĩ (Followers, Popularity, Main Genre)
    5. gdp_data.csv                — GDP World Bank (1960–2022)
    6. country_codes.csv           — Phân loại vùng & thu nhập World Bank

Đầu ra (data/processed/):
    1. spotify.csv                 — Master Dataset chuẩn hóa 45 cột
    2. tracks_ml_data.csv          — Dữ liệu Song-level không rò rỉ cho ML

Author: Đinh Quốc Anh (MSSV: 24133003 — Data Engineer & Data Analyst)
"""

import os
import re
import sys
import warnings
from datetime import datetime

import numpy as np
import pandas as pd

# Tránh lỗi font tiếng Việt trên terminal Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

warnings.filterwarnings("ignore")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

AUDIO_FEATURES = [
    "danceability", "energy", "loudness", "speechiness",
    "acousticness", "instrumentalness", "liveness", "valence", "tempo",
]
AUDIO_0_1 = [
    "danceability", "energy", "speechiness", "acousticness",
    "instrumentalness", "liveness", "valence",
]
TRENDING_THRESHOLD = 50   # rank <= 50 thì is_trending = 1

LATIN_KEYWORDS = [
    "latin", "reggaeton", "salsa", "bachata", "merengue", "cumbia",
    "trap latino", "latin pop", "latin hip hop", "urbano", "vallenato",
    "corrido", "norteño", "ranchera", "sertanejo", "funk carioca",
    "bossa nova", "mpb", "forró", "pagode", "axé", "cuarteto",
    "dembow", "reggae", "cubano", "tropical", "chicano",
]
KPOP_KEYWORDS = ["k-pop", "kpop", "k pop", "k-rap"]

# Chuẩn hóa tên quốc gia giữa Spotify Charts và World Bank
COUNTRY_NAME_MAPPING = {
    "Czech Republic": "Czechia",
    "Egypt": "Egypt, Arab Rep.",
    "Hong Kong": "Hong Kong SAR, China",
    "Korea": "Korea, Rep.",
    "Slovakia": "Slovak Republic",
    "Turkey": "Turkiye",
    "Venezuela": "Venezuela, RB",
}

# Danh sách 40 cột chuẩn mực giữ lại trong Master Dataset (Khớp 100% Data Dictionary)
FINAL_COLUMNS = [
    # Định danh, không gian, thời gian (9 cột)
    "track_id", "track_name", "artist_individual", "artist_genre",
    "chart_country", "chart_language", "chart_week", "chart_year", "chart_month",
    # Xếp hạng và lượt stream (4 cột)
    "rank", "streams", "weeks_on_chart", "peak_rank",
    # 9 đặc trưng âm học (9 cột)
    "danceability", "energy", "loudness", "speechiness", "acousticness",
    "instrumentalness", "liveness", "valence", "tempo",
    # Cấp bài hát (4 cột - Đã loại bỏ explicit, song_popularity_raw, has_song_popularity, popularity_is_imputed)
    "song_genre", "song_genre_source", "song_popularity", "popularity_status",
    # Cấp nghệ sĩ (2 cột - artist_popularity giữ NaN tự nhiên theo Phương án A, artist_chart_score đo phong độ toàn kỳ)
    "artist_popularity", "artist_chart_score",
    # Kinh tế & Địa lý World Bank (5 cột)
    "gdp_value", "gdp_log", "income_group", "region_wb", "country_code",
    # Các trường tính toán phái sinh (7 cột)
    "is_trending", "mood_category", "stream_share_country",
    "macro_genre", "duration_min", "chart_longevity", "tempo_category",
]


# ============================================================
# BƯỚC 1: NẠP VÀ LÀM SẠCH 6 BẢNG DỮ LIỆU THÔ
# ============================================================

def load_raw_data():
    """Đọc 6 file thô từ thư mục data/raw/."""
    print("Nạp dữ liệu thô (6 bảng)")

    p_charts = os.path.join(RAW_DIR, "spotify-weekly-charts.csv")
    print("  1. Đang đọc spotify-weekly-charts.csv (~800 MB)...")
    charts = pd.read_csv(p_charts, low_memory=False, encoding_errors="ignore")
    print(f"     charts: {len(charts):,} dòng, {len(charts.columns)} cột")

    p_songs = os.path.join(RAW_DIR, "songs.csv")
    print("  2. Đang đọc songs.csv (550K bài)...")
    songs = pd.read_csv(p_songs, low_memory=False, encoding_errors="ignore")
    print(f"     songs: {len(songs):,} dòng, {len(songs.columns)} cột")

    p_tracks = os.path.join(RAW_DIR, "spotify-tracks-dataset.csv")
    print("  3. Đang đọc spotify-tracks-dataset.csv (114K bài)...")
    tracks = pd.read_csv(p_tracks, low_memory=False, encoding_errors="ignore")
    print(f"     tracks-dataset: {len(tracks):,} dòng, {len(tracks.columns)} cột")

    p_artists = os.path.join(RAW_DIR, "artists.csv")
    print("  4. Đang đọc artists.csv (71K nghệ sĩ)...")
    artists = pd.read_csv(p_artists, encoding_errors="ignore")
    print(f"     artists: {len(artists):,} dòng, {len(artists.columns)} cột")

    p_gdp = os.path.join(RAW_DIR, "gdp_data.csv")
    gdp = pd.read_csv(p_gdp)
    print(f"  5. gdp: {len(gdp):,} dòng, {len(gdp.columns)} cột")

    p_codes = os.path.join(RAW_DIR, "country_codes.csv")
    country_codes = pd.read_csv(p_codes)
    print(f"  6. country codes: {len(country_codes):,} dòng, {len(country_codes.columns)} cột")

    total = len(charts) + len(songs) + len(tracks) + len(artists) + len(gdp) + len(country_codes)
    print(f"  Tổng cộng: {total:,} bản ghi thô từ 6 nguồn")
    return charts, songs, tracks, artists, gdp, country_codes


def clean_charts(df):
    """
    Làm sạch bảng weekly charts:
      - Loại bỏ dòng header lẫn trong dữ liệu
      - Trích xuất year/month/track_id từ week/uri
      - Ép kiểu số cho các cột âm thanh và thứ hạng
      - Kẹp giá trị audio features về đúng miền chuẩn [0, 1]
      - Bỏ dòng trùng lặp và streams <= 0
    """
    print("\nLàm sạch bảng charts")
    n_before = len(df)

    unnamed_cols = [c for c in df.columns if "Unnamed" in str(c)]
    if unnamed_cols:
        df.drop(columns=unnamed_cols, inplace=True)

    # Loại bỏ header bị lẫn vào dữ liệu
    df = df[df["rank"].astype(str).str.strip() != "rank"].copy()

    # Xử lý thời gian
    df["week"] = pd.to_datetime(df["week"], errors="coerce")
    df["year"] = df["week"].dt.year.astype("Int64")
    df["month"] = df["week"].dt.month.astype("Int64")
    df.dropna(subset=["week"], inplace=True)

    # Trích xuất track_id từ uri (spotify:track:XXXXX -> XXXXX)
    if "uri" in df.columns and "track_id" not in df.columns:
        df["track_id"] = df["uri"].str.replace("spotify:track:", "", regex=False)

    # Ép kiểu số
    df["streams"] = pd.to_numeric(df["streams"], errors="coerce").fillna(0).astype(int)
    df = df[df["streams"] > 0]

    for col in ["rank", "weeks_on_chart", "peak_rank", "previous_rank"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    df["country"] = df["country"].str.strip()

    if "duration" in df.columns:
        df["duration"] = pd.to_numeric(df["duration"], errors="coerce")

    for col in AUDIO_FEATURES:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in AUDIO_0_1:
        if col in df.columns:
            df[col] = df[col].clip(0, 1)

    # Khử trùng lặp bản ghi
    df.drop_duplicates(subset=["track_id", "country", "week"], keep="first", inplace=True)

    n_after = len(df)
    print(f"  charts: {n_before:,} → {n_after:,} dòng (loại bỏ {n_before - n_after:,} dòng rác/trùng)")
    return df


def build_track_waterfall(songs_df, tracks_df):
    """
    Kỹ thuật Waterfall bài hát:
    Kết hợp 2 nguồn bài hát để tối đa hóa độ phủ dữ liệu thật:
      - songs.csv (550K bài)
      - spotify-tracks-dataset.csv (114K bài, bổ sung thêm cột explicit)
    Ưu tiên lấy điểm và thể loại từ songs.csv, nếu thiếu thì tự động lấy từ tracks-dataset.
    """
    print("\nXây dựng bảng tra cứu bài hát tổng hợp (Track Waterfall)")

    # 1. Làm sạch songs.csv
    s = songs_df.copy()
    s["popularity"] = pd.to_numeric(s["popularity"], errors="coerce")
    s = s.sort_values("popularity", ascending=False).drop_duplicates("id", keep="first")
    s_keep = s[["id", "genre", "popularity"]].rename(columns={
        "id": "track_id",
        "genre": "genre_songs",
        "popularity": "pop_songs",
    })

    # 2. Làm sạch spotify-tracks-dataset.csv
    t = tracks_df.copy()
    t["popularity"] = pd.to_numeric(t["popularity"], errors="coerce")
    t = t.sort_values("popularity", ascending=False).drop_duplicates("track_id", keep="first")
    t_keep = t[["track_id", "track_genre", "popularity", "explicit"]].rename(columns={
        "track_genre": "genre_tracks",
        "popularity": "pop_tracks",
    })

    # 3. Kết hợp Outer Join 2 nguồn
    m = pd.merge(s_keep, t_keep, on="track_id", how="outer")

    # Waterfall gộp dữ liệu
    m["song_popularity_raw"] = m["pop_songs"].fillna(m["pop_tracks"])
    m["song_genre_raw"] = m["genre_songs"].fillna(m["genre_tracks"])
    m["explicit"] = m["explicit"].fillna(False).astype(bool)

    # Đánh dấu nguồn gốc bài hát
    m["track_source"] = np.where(
        m["pop_songs"].notna(), "songs_550k",
        np.where(m["pop_tracks"].notna(), "tracks_114k", "unknown")
    )

    out = m[["track_id", "song_popularity_raw", "song_genre_raw", "explicit", "track_source"]].copy()
    print(f"  Bảng bài hát tổng hợp: {len(out):,} bài hát độc nhất")
    print(f"  Số bài có popularity thật: {out['song_popularity_raw'].notna().sum():,} bài")
    return out


def clean_artists(df):
    """
    Làm sạch bảng artists.csv (71,440 nghệ sĩ):
      - Khử trùng lặp theo id
      - Giữ cột cần thiết: id, main_genre, followers, popularity
      - Chuẩn hóa tên cột thô (_raw) để đảm bảo tính minh bạch dữ liệu
    """
    print("\nLàm sạch bảng artists")
    df = df.copy()

    unnamed_cols = [c for c in df.columns if "Unnamed" in str(c)]
    if unnamed_cols:
        df.drop(columns=unnamed_cols, inplace=True)

    df["followers"] = pd.to_numeric(df["followers"], errors="coerce")
    df["popularity"] = pd.to_numeric(df["popularity"], errors="coerce")
    df = df.drop_duplicates("id", keep="first")

    keep_cols = [c for c in ["id", "main_genre", "followers", "popularity"] if c in df.columns]
    df = df[keep_cols].copy()

    df.rename(columns={
        "id": "artist_id_clean",
        "main_genre": "artist_main_genre",
        "followers": "artist_followers_raw",
        "popularity": "artist_popularity_raw",
    }, inplace=True)

    print(f"  artists sau làm sạch: {len(df):,} nghệ sĩ")
    return df


def clean_gdp(df):
    """Làm sạch bảng GDP World Bank: chuẩn hóa tên cột, ép kiểu số."""
    df = df.copy()
    unnamed_cols = [c for c in df.columns if "Unnamed" in str(c)]
    if unnamed_cols:
        df.drop(columns=unnamed_cols, inplace=True)

    if "value" in df.columns:
        df.rename(columns={"value": "gdp_value"}, inplace=True)
    df["gdp_value"] = pd.to_numeric(df["gdp_value"], errors="coerce")
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    return df[["country_name", "country_code", "year", "gdp_value"]].dropna(subset=["country_name", "year"])


def clean_country_codes(df):
    """Làm sạch bảng country codes và tự động bổ sung Taiwan."""
    df = df.copy()
    unnamed_cols = [c for c in df.columns if "Unnamed" in str(c)]
    if unnamed_cols:
        df.drop(columns=unnamed_cols, inplace=True)

    if "region" in df.columns:
        df.rename(columns={"region": "region_wb"}, inplace=True)

    out = df[["country_code", "region_wb", "income_group"]].dropna(subset=["country_code"])

    # Bổ sung TWN (Taiwan) nếu chưa có
    if "TWN" not in out["country_code"].values:
        twn = pd.DataFrame([{
            "country_code": "TWN",
            "region_wb": "East Asia & Pacific",
            "income_group": "High income",
        }])
        out = pd.concat([out, twn], ignore_index=True)
    return out


# ============================================================
# BƯỚC 2: XÂY DỰNG MASTER DATASET (JOIN 6 BẢNG + CALCULATED FIELDS)
# ============================================================

def build_master_dataset(charts, track_waterfall, artists, gdp, country_codes, save=True):
    """
    Join 6 bảng dữ liệu theo kiến trúc hình sao mở rộng (Star Schema):
        charts (base) LEFT JOIN gdp           on [country_code, year]
        charts (base) LEFT JOIN country_codes on country_code
        charts (base) LEFT JOIN track_waterfall on track_id
        charts (base) LEFT JOIN artists       on artist_id
    """
    print("\nXây dựng master dataset (Mô hình Hình Sao 6 Bảng)")

    # Lọc giai đoạn trọng tâm 2020–2022
    df = charts[charts["year"].isin([2020, 2021, 2022])].copy()
    print(f"  Lọc 2020–2022: {len(df):,} dòng")

    # --- JOIN 1: GDP World Bank ---
    df["_country_wb"] = df["country"].replace(COUNTRY_NAME_MAPPING)
    name_to_code = (
        gdp[["country_name", "country_code"]]
        .drop_duplicates()
        .set_index("country_name")["country_code"]
        .to_dict()
    )
    name_to_code["Taiwan"] = "TWN"
    df["country_code"] = df["_country_wb"].map(name_to_code)

    df = pd.merge(
        df,
        gdp[["country_code", "year", "gdp_value"]].drop_duplicates(["country_code", "year"]),
        on=["country_code", "year"],
        how="left",
    )
    print(f"  sau JOIN GDP: {len(df):,} dòng, GDP match {df['gdp_value'].notna().mean():.1%}")

    # --- JOIN 2: Country Codes (Vùng miền & Thu nhập) ---
    df = pd.merge(df, country_codes, on="country_code", how="left")
    df.drop(columns=["_country_wb"], errors="ignore", inplace=True)
    print(f"  sau JOIN Country Codes: {len(df):,} dòng, Region match {df['region_wb'].notna().mean():.1%}")

    # --- JOIN 3: Track Waterfall (Cứu dữ liệu bài hát từ cả 2 nguồn) ---
    df = pd.merge(df, track_waterfall, on="track_id", how="left")
    real_pop_count = df["song_popularity_raw"].notna().sum()
    print(f"  sau JOIN Track Waterfall: {len(df):,} dòng")
    print(f"     Số dòng có Popularity THẬT: {real_pop_count:,} dòng ({real_pop_count / len(df):.1%})")

    # --- JOIN 4: Artists (71K hồ sơ nghệ sĩ) ---
    if "artist_id" in df.columns:
        df["_artist_id_clean"] = df["artist_id"].astype(str).str.replace("spotify:artist:", "", regex=False)
        df = pd.merge(
            df,
            artists,
            left_on="_artist_id_clean",
            right_on="artist_id_clean",
            how="left",
        )
        df.drop(columns=["_artist_id_clean", "artist_id_clean"], errors="ignore", inplace=True)
        print(f"  sau JOIN Artists: {len(df):,} dòng, Artist match {df['artist_main_genre'].notna().mean():.1%}")

    # ============================================================
    # TÍNH TOÁN CÁC TRƯỜNG PHÁI SINH & XỬ LÝ KHUYẾT THIẾU
    # ============================================================

    # 1. is_trending: 1 nếu bài thuộc Top 50 tuần
    df["is_trending"] = (df["rank"] <= TRENDING_THRESHOLD).astype(int)

    # 2. mood_category: Phân loại cảm xúc theo mô hình Russell
    has_audio = df["valence"].notna() & df["energy"].notna()
    v_hi = df["valence"] >= 0.5
    e_hi = df["energy"] >= 0.5
    df["mood_category"] = "Unknown"
    df.loc[has_audio & v_hi & e_hi, "mood_category"] = "Happy Energetic"
    df.loc[has_audio & v_hi & ~e_hi, "mood_category"] = "Peaceful Positive"
    df.loc[has_audio & ~v_hi & e_hi, "mood_category"] = "Tense Aggressive"
    df.loc[has_audio & ~v_hi & ~e_hi, "mood_category"] = "Sad Melancholic"

    # 3. stream_share_country: Thị phần stream trong từng thị trường tuần
    total_streams = df.groupby(["country", "week"])["streams"].transform("sum")
    df["stream_share_country"] = np.where(total_streams > 0, df["streams"] / total_streams, 0)

    # 4. macro_genre: Dòng nhạc vĩ mô chuẩn hóa (ổn định per track bằng mode)
    df["macro_genre"] = compute_macro_genre(df)
    track_macro_mode = (
        df.groupby("track_id")["macro_genre"]
        .agg(lambda x: x.value_counts().index[0])
    )
    df["macro_genre"] = df["track_id"].map(track_macro_mode)

    # 5. XỬ LÝ NGHỆ SĨ (Bảo tồn NaN tự nhiên theo Phương án A & Tính artist_chart_score theo Percentile Rank)
    # Không điền trung vị nữa để tránh bóp méo dữ liệu ca sĩ bản địa/indie
    df["artist_popularity"] = df["artist_popularity_raw"]

    # artist_chart_score: Điểm phong độ toàn kỳ 2020-2022 theo Percentile Rank trên 9,704 nghệ sĩ độc nhất
    # Giả định collab: Mỗi nghệ sĩ trong bài hát chung nhận nguyên vẹn streams của bài đó
    art_tot = df.groupby("artist_individual")["streams"].sum()
    art_pct = (art_tot.rank(pct=True) * 100).round(2)
    df["artist_chart_score"] = df["artist_individual"].map(art_pct)

    # 6. BẬC THANG 4 TẦNG CHO THỂ LOẠI (song_genre) KÈM CỘT NGUỒN GỐC
    artist_genre_clean = (
        df["artist_genre"]
        .astype(str)
        .str.strip()
        .str.lower()
        .replace(["0", "", "none", "nan", "unknown"], np.nan)
    )
    song_genre_raw_clean = (
        df["song_genre_raw"]
        .astype(str)
        .str.strip()
        .str.lower()
        .replace(["0", "", "none", "nan", "unknown"], np.nan)
    )
    artist_main_clean = (
        df["artist_main_genre"]
        .astype(str)
        .str.strip()
        .str.lower()
        .replace(["0", "", "none", "nan", "unknown"], np.nan)
    )
    macro_clean = df["macro_genre"].astype(str).str.strip().str.lower()

    # Bậc thang gộp thể loại
    df["song_genre"] = (
        song_genre_raw_clean
        .fillna(artist_genre_clean)
        .fillna(artist_main_clean)
        .fillna(macro_clean)
    )

    # Ghi nhận nguồn gốc thể loại (song_genre_source)
    df["song_genre_source"] = np.where(
        song_genre_raw_clean.notna(), "track_dataset",
        np.where(artist_genre_clean.notna(), "artist_detailed_chart",
        np.where(artist_main_clean.notna(), "artist_main_profile", "macro_fallback"))
    )
    print(f"  sau xử lý song_genre bậc thang: {df['song_genre'].notna().mean():.1%} đầy đủ, {df['song_genre'].nunique():,} nhãn độc nhất")

    # 7. PHƯƠNG ÁN A: BẢO TOÀN DỮ LIỆU THẬT CHO EDA & LOẠI BỎ HỒI QUY NHÂN TẠO
    # Tuyệt đối không dùng mô hình Machine Learning ở bước tiền xử lý để chế số liệu.
    # Cột song_popularity giữ 100% dữ liệu gốc từ Spotify (42.2% có điểm thật, 57.8% giữ NaN).
    df["song_popularity"] = df["song_popularity_raw"]
    df["has_song_popularity"] = df["song_popularity"].notna().astype(int)
    df["popularity_is_imputed"] = 0
    df["popularity_status"] = np.where(
        df["song_popularity"].notna(),
        "Official Spotify Score",
        "Unindexed / Regional Hits"
    )
    print(f"  sau xử lý song_popularity (Phương án A - Chuẩn EDA): Có điểm thật: {df['has_song_popularity'].mean():.1%}, Unindexed/Indie: {(1 - df['has_song_popularity'].mean()):.1%}")

    # 8. duration_min
    if "duration" in df.columns:
        df["duration_min"] = df["duration"] / 60_000

    # 9. chart_longevity
    if "weeks_on_chart" in df.columns:
        df["chart_longevity"] = df.groupby("track_id")["weeks_on_chart"].transform("max")

    # 10. tempo_category
    df["tempo_category"] = pd.cut(
        df["tempo"],
        bins=[0, 90, 120, 150, 300],
        labels=["Slow", "Medium", "Fast", "Very Fast"],
        right=False,
    ).astype(str).replace("nan", "Unknown")

    # 11. gdp_log
    df["gdp_log"] = np.log1p(df["gdp_value"])

    # ============================================================
    # CHỌN CỘT & LƯU FILE
    # ============================================================

    # Đổi tên các trường không gian - thời gian chuẩn mực theo Data Dictionary
    df.rename(columns={
        "country": "chart_country",
        "language": "chart_language",
        "week": "chart_week",
        "year": "chart_year",
        "month": "chart_month",
    }, inplace=True)

    final_cols = [c for c in FINAL_COLUMNS if c in df.columns]
    df = df[final_cols]

    # Làm tròn số thực
    float_cols = df.select_dtypes(include=["float64", "float32"]).columns
    for c in float_cols:
        if c in ["gdp_value"]:
            df[c] = df[c].round(0)
        else:
            df[c] = df[c].round(3)

    print(f"\n  Master Dataset: {len(df):,} dòng, {len(df.columns)} cột")

    if save:
        os.makedirs(PROCESSED_DIR, exist_ok=True)
        out_path = os.path.join(PROCESSED_DIR, "spotify.csv")
        df.to_csv(out_path, index=False)
        mb = os.path.getsize(out_path) / 1e6
        print(f"  Đã ghi đè thành công: {out_path} ({mb:.1f} MB)")

    return df


def compute_macro_genre(df):
    """
    Phân loại dòng nhạc vĩ mô (macro_genre) dựa trên tổ hợp:
      - artist_genre (từ charts)
      - song_genre_raw (từ track waterfall)
      - artist_main_genre (từ artists.csv)
    """
    genre_combo = (
        df["artist_genre"].fillna("").astype(str).str.lower()
        + " "
        + df.get("song_genre_raw", pd.Series("", index=df.index)).fillna("").astype(str).str.lower()
        + " "
        + df.get("artist_main_genre", pd.Series("", index=df.index)).fillna("").astype(str).str.lower()
    )

    def _wb_pat(keywords):
        escaped = [re.escape(kw) for kw in keywords]
        return r"\b(?:" + "|".join(escaped) + r")\b"

    kpop_pat = _wb_pat(KPOP_KEYWORDS)
    latin_pat = _wb_pat(LATIN_KEYWORDS)
    hiphop_pat = _wb_pat(["hip hop", "hip-hop", "rap", "trap"])
    rock_pat = _wb_pat(["rock", "metal", "punk"])
    pop_pat = _wb_pat(["pop", "electropop"])

    cond_kpop = genre_combo.str.contains(kpop_pat, regex=True, na=False)
    cond_latin = genre_combo.str.contains(latin_pat, regex=True, na=False)
    cond_hiphop = genre_combo.str.contains(hiphop_pat, regex=True, na=False)
    cond_rock = genre_combo.str.contains(rock_pat, regex=True, na=False)
    cond_pop = genre_combo.str.contains(pop_pat, regex=True, na=False)

    conditions = [cond_kpop, cond_latin, cond_hiphop, cond_rock, cond_pop]
    choices = ["K-Pop", "Latin", "Hip-Hop/Rap", "Rock/Metal", "Pop"]

    return np.select(conditions, choices, default="Others")


# ============================================================
# BƯỚC 3: XUẤT DỮ LIỆU CẤP BÀI HÁT CHO ML (Chống rò rỉ dữ liệu)
# ============================================================

def generate_ml_dataset(df_master, save=True):
    """
    Tạo file tracks_ml_data.csv: mỗi bài một dòng (song-level), dùng cho ML.
    Gom theo track_id để triệt tiêu data leakage.
    """
    print("\nTạo dữ liệu cấp bài hát cho ML")

    def _mode_or_first(s):
        vc = s.value_counts()
        return vc.index[0] if len(vc) > 0 else s.iloc[0]

    agg_rules = {
        "track_name": "first",
        "artist_individual": "first",
        "artist_genre": _mode_or_first,
        "song_genre": _mode_or_first,
        "song_genre_source": _mode_or_first,
        "song_popularity": "max",
        "popularity_status": _mode_or_first,
        "artist_popularity": "max",
        "chart_language": _mode_or_first,
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
        "macro_genre": "first",
        "tempo_category": "first",
        "chart_longevity": "max",
        "is_trending": "max",
    }
    avail_rules = {k: v for k, v in agg_rules.items() if k in df_master.columns}
    ml_data = df_master.groupby("track_id").agg(avail_rules).reset_index()

    ml_float_cols = ml_data.select_dtypes(include=["float64", "float32"]).columns
    for c in ml_float_cols:
        ml_data[c] = ml_data[c].round(3)

    if save:
        os.makedirs(PROCESSED_DIR, exist_ok=True)
        ml_path = os.path.join(PROCESSED_DIR, "tracks_ml_data.csv")
        ml_data.to_csv(ml_path, index=False)
        mb = os.path.getsize(ml_path) / 1e6
        print(f"  Đã lưu {ml_path} ({len(ml_data):,} bài, {len(ml_data.columns)} cột, {mb:.1f} MB, tỷ lệ hit {ml_data['is_trending'].mean():.1%})")

    return ml_data


# ============================================================
# HÀM NẠP TIỆN ÍCH DÙNG CHO CÁC MODULE KHÁC
# ============================================================

def load_master_data(nrows=None):
    """Nạp file Master Dataset đã xử lý sạch."""
    p = os.path.join(PROCESSED_DIR, "spotify.csv")
    if not os.path.exists(p):
        raise FileNotFoundError(f"Chưa có file {p}. Hãy chạy main() trước.")
    return pd.read_csv(p, nrows=nrows, low_memory=False)


def load_ml_data():
    """Nạp file ML song-level."""
    p = os.path.join(PROCESSED_DIR, "tracks_ml_data.csv")
    if not os.path.exists(p):
        raise FileNotFoundError(f"Chưa có file {p}. Hãy chạy main() trước.")
    return pd.read_csv(p)


def main():
    t0 = datetime.now()
    print(f"Spotify 6-Table Waterfall ETL Pipeline, bắt đầu lúc {t0.strftime('%Y-%m-%d %H:%M:%S')}")

    charts_raw, songs_raw, tracks_raw, artists_raw, gdp_raw, codes_raw = load_raw_data()

    charts = clean_charts(charts_raw)
    track_waterfall = build_track_waterfall(songs_raw, tracks_raw)
    artists = clean_artists(artists_raw)
    gdp = clean_gdp(gdp_raw)
    codes = clean_country_codes(codes_raw)

    master = build_master_dataset(charts, track_waterfall, artists, gdp, codes, save=True)
    generate_ml_dataset(master, save=True)

    print(f"\nHoàn tất 100%! Thời gian thực thi: {datetime.now() - t0}")


if __name__ == "__main__":
    main()
