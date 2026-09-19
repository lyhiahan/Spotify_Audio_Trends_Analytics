"""
src/data_loader.py

ETL pipeline: nạp 5 bảng, làm sạch, join thành một file master (42 cột)
và xuất file dữ liệu cấp bài hát cho Machine Learning.

Đầu ra:
    data/processed/merged_spotify_data.csv   file master (42 cột)
    data/processed/tracks_ml_data.csv        dữ liệu cấp bài hát cho ML (18 cột)

Author: Đinh Quốc Anh
"""

import os
import re
import sys
import warnings
from datetime import datetime

import numpy as np
import pandas as pd

# tránh lỗi in tiếng Việt trên Windows
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
# các feature nằm trong khoảng [0, 1]
AUDIO_0_1 = [
    "danceability", "energy", "speechiness", "acousticness",
    "instrumentalness", "liveness", "valence",
]
TRENDING_THRESHOLD = 50   # rank <= 50 thì is_trending = 1
POPULAR_THRESHOLD = 70    # popularity >= 70 thì is_popular = 1

LATIN_KEYWORDS = [
    "latin", "reggaeton", "salsa", "bachata", "merengue", "cumbia",
    "trap latino", "latin pop", "latin hip hop", "urbano", "vallenato",
    "corrido", "norteño", "ranchera", "sertanejo", "funk carioca",
    "bossa nova", "mpb", "forró", "pagode", "axé", "argentine",
    "colombian", "brazilian", "mexican", "puerto rican", "cuarteto",
    "dembow", "reggae", "cubano", "tropical", "chicano",
]
KPOP_KEYWORDS = ["k-pop", "kpop", "korean", "k pop"]

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

FINAL_INSIGHT_COLUMNS = [
    # định danh, không gian, thời gian
    "track_id", "track_name", "artist_individual", "artist_genre",
    "country", "language", "week", "year", "month",
    # xếp hạng và lượt stream
    "rank", "streams", "log_streams", "weeks_on_chart", "peak_rank",
    # 9 audio features
    "danceability", "energy", "loudness", "speechiness", "acousticness",
    "instrumentalness", "liveness", "valence", "tempo",
    # kinh tế World Bank
    "gdp_value", "gdp_log", "income_group", "region_wb", "country_code",
    # các cột phân loại và tính thêm
    "is_trending", "is_popular", "mood_category", "stream_share_country",
    "covid_phase", "energy_loudness_index", "is_latin", "is_kpop",
    "is_legacy_artist", "duration_min", "audio_diversity_score",
    "track_genre", "popularity", "explicit",
]


# Bước 1: nạp và làm sạch dữ liệu thô


def load_raw_data():
    """Đọc 5 file thô từ thư mục data/raw/."""
    print("Nạp dữ liệu thô")

    p_charts = os.path.join(RAW_DIR, "spotify-weekly-charts.csv")
    print("  đang đọc spotify-weekly-charts.csv (~800 MB)...")
    charts = pd.read_csv(p_charts, low_memory=False)
    print(f"  charts: {len(charts):,} dòng, {len(charts.columns)} cột")

    p_tracks = os.path.join(RAW_DIR, "spotify-tracks-dataset.csv")
    print("  đang đọc spotify-tracks-dataset.csv...")
    tracks = pd.read_csv(p_tracks, low_memory=False)
    print(f"  tracks: {len(tracks):,} dòng, {len(tracks.columns)} cột")

    p_gdp = os.path.join(RAW_DIR, "gdp_data.csv")
    gdp = pd.read_csv(p_gdp)
    print(f"  gdp: {len(gdp):,} dòng, {len(gdp.columns)} cột")

    p_codes = os.path.join(RAW_DIR, "country_codes.csv")
    country_codes = pd.read_csv(p_codes)
    print(f"  country codes: {len(country_codes):,} dòng, {len(country_codes.columns)} cột")

    p_artists = os.path.join(RAW_DIR, "best-selling-artists.csv")
    artists = pd.read_csv(p_artists)
    print(f"  best-selling artists: {len(artists):,} dòng, {len(artists.columns)} cột")

    total = len(charts) + len(tracks) + len(gdp) + len(country_codes) + len(artists)
    print(f"  tổng: {total:,} bản ghi")
    return charts, tracks, gdp, country_codes, artists


def clean_raw_charts(df):
    """
    Làm sạch bảng weekly charts:
      - lọc theo ngày hợp lệ, trích xuất year/month/track_id
      - bỏ dòng thiếu, bỏ trùng lặp, lọc streams > 0
      - ép kiểu số cho các cột âm thanh và thứ hạng
    """
    print("\nLàm sạch bảng charts")
    n_before = len(df)
    df = df.copy()

    unnamed_cols = [c for c in df.columns if "Unnamed" in str(c)]
    if unnamed_cols:
        df.drop(columns=unnamed_cols, inplace=True)

    df["week"] = pd.to_datetime(df["week"], errors="coerce")
    df["year"] = df["week"].dt.year.astype("Int64")
    df["month"] = df["week"].dt.month.astype("Int64")
    df["quarter"] = df["week"].dt.quarter.astype("Int64")
    df.dropna(subset=["week"], inplace=True)

    # trích track_id từ uri (spotify:track:XXXXX -> XXXXX)
    if "uri" in df.columns and "track_id" not in df.columns:
        df["track_id"] = df["uri"].str.replace("spotify:track:", "", regex=False)

    df["streams"] = pd.to_numeric(df["streams"], errors="coerce").fillna(0).astype(int)
    df = df[df["streams"] > 0]

    for col in ["rank", "weeks_on_chart", "peak_rank"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    df["country"] = df["country"].str.strip()

    if "duration" in df.columns:
        df["duration"] = pd.to_numeric(df["duration"], errors="coerce")

    for col in AUDIO_FEATURES:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df.drop_duplicates(subset=["track_id", "week", "country"], keep="first", inplace=True)

    # bỏ sớm các cột không cần cho phân tích
    drop_cols = [
        "uri", "artist_names", "artists_num", "artist_id",
        "key", "mode", "source", "album_num_tracks", "collab",
        "release_date", "previous_rank", "artist_img", "album_cover",
        "pivot", "region", "region_spotify", "region_x",
    ]
    existing_drops = [c for c in drop_cols if c in df.columns]
    if existing_drops:
        df.drop(columns=existing_drops, inplace=True)

    print(f"  {n_before:,} -> {len(df):,} dòng, {len(df.columns)} cột")
    return df


def clean_raw_tracks(df):
    """
    Làm sạch bảng tracks:
      - mỗi track_id giữ bản có popularity cao nhất
      - ép kiểu boolean cho explicit và numeric cho popularity
      - kẹp các feature về đúng miền [0, 1]
    """
    df = df.copy()

    unnamed_cols = [c for c in df.columns if "Unnamed" in str(c)]
    if unnamed_cols:
        df.drop(columns=unnamed_cols, inplace=True)

    if "popularity" in df.columns:
        df["popularity"] = pd.to_numeric(df["popularity"], errors="coerce")
        df = df.sort_values("popularity", ascending=False).drop_duplicates("track_id", keep="first")
    else:
        df = df.drop_duplicates("track_id", keep="first")

    if "explicit" in df.columns:
        df["explicit"] = df["explicit"].astype("boolean")

    # kẹp giá trị về đúng miền
    for col in AUDIO_0_1:
        if col in df.columns:
            df[col] = df[col].clip(0, 1)

    if "loudness" in df.columns:
        df["loudness"] = df["loudness"].clip(-60, 5)
    if "tempo" in df.columns:
        df["tempo"] = df["tempo"].clip(0, 300)

    # chỉ giữ cột cần để join
    keep = [c for c in ["track_id", "track_genre", "popularity", "explicit"] if c in df.columns]
    df = df[keep]
    print(f"  tracks sau làm sạch: {len(df):,} bài hát")
    return df


def clean_raw_artists(df):
    """Làm sạch bảng best-selling artists."""
    df = df.copy()
    df["artist_name_clean"] = df["Artist name"].str.strip().str.lower()
    df.rename(columns={"Artist name": "legacy_artist_name"}, inplace=True)
    out = df[["artist_name_clean", "legacy_artist_name"]].drop_duplicates("artist_name_clean")
    print(f"  best-selling artists: {len(out):,} nghệ sĩ")
    return out


def clean_raw_gdp(df):
    """Làm sạch bảng GDP."""
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
    """Làm sạch bảng country codes và bổ sung mã chuẩn cho các vùng lãnh thổ."""
    df = df.copy()
    unnamed_cols = [c for c in df.columns if "Unnamed" in str(c)]
    if unnamed_cols:
        df.drop(columns=unnamed_cols, inplace=True)
    if "region" in df.columns:
        df.rename(columns={"region": "region_wb"}, inplace=True)
    out = df[["country_code", "region_wb", "income_group"]].dropna(subset=["country_code"])
    # Bổ sung TWN (Taiwan) chuẩn World Bank / IMF nếu chưa có trong bảng thô
    if "TWN" not in out["country_code"].values:
        twn_row = pd.DataFrame([{"country_code": "TWN", "region_wb": "East Asia & Pacific", "income_group": "High income"}])
        out = pd.concat([out, twn_row], ignore_index=True)
    return out


# Bước 2: tạo file master


def build_master_dataset(charts, gdp, country_codes, tracks, artists, save=True):
    """Join các bảng, tính các cột phái sinh và giữ lại 42 cột dùng cho phân tích."""
    print("\nXây dựng master dataset")

    # chỉ lấy 2020-2022 để bao đủ 3 pha COVID
    df = charts[charts["year"].isin([2020, 2021, 2022])].copy()
    print(f"  lọc 2020-2022: {len(df):,} dòng")

    # 1. Chuẩn hóa tên quốc gia World Bank
    df["_country_wb"] = df["country"].replace(COUNTRY_NAME_MAPPING)

    # 2. Lập bảng tra country_code từ gdp + Taiwan
    name_to_code = gdp[["country_name", "country_code"]].drop_duplicates().set_index("country_name")["country_code"].to_dict()
    name_to_code["Taiwan"] = "TWN"
    df["country_code"] = df["_country_wb"].map(name_to_code)

    # 3. Join GDP theo (country_code, year)
    df = pd.merge(
        df,
        gdp[["country_code", "year", "gdp_value"]].drop_duplicates(["country_code", "year"]),
        on=["country_code", "year"],
        how="left",
    )

    # 4. Join country codes theo country_code
    df = pd.merge(df, country_codes, on="country_code", how="left")

    # Xóa cột tạm
    if "_country_wb" in df.columns:
        df.drop(columns=["_country_wb"], inplace=True)

    # 5. Join tracks (genre, popularity, explicit)
    df = pd.merge(df, tracks, on="track_id", how="left")

    # 6. Join best-selling artists theo tên đã chuẩn hóa
    df["_artist_clean"] = df["artist_individual"].str.strip().str.lower()
    df = pd.merge(df, artists, left_on="_artist_clean", right_on="artist_name_clean", how="left")

    # các cột tính thêm

    # 3 pha COVID
    df["covid_phase"] = "Unknown"
    df.loc[df["year"] <= 2020, "covid_phase"] = "Lockdown & Shock"
    df.loc[df["year"] == 2021, "covid_phase"] = "Vaccine & Escapism"
    df.loc[df["year"] >= 2022, "covid_phase"] = "Reopening & New Normal"

    df["is_trending"] = (df["rank"] <= TRENDING_THRESHOLD).astype(int)
    df["is_popular"] = 0
    mask_pop = df["popularity"].notna() & (df["popularity"] >= POPULAR_THRESHOLD)
    df.loc[mask_pop, "is_popular"] = 1

    # mood theo valence/energy (4 góc phần tư của mô hình Russell)
    v_hi = df["valence"] >= 0.5
    e_hi = df["energy"] >= 0.5
    df["mood_category"] = "Unknown"
    df.loc[v_hi & e_hi, "mood_category"] = "Happy Energetic"
    df.loc[v_hi & ~e_hi, "mood_category"] = "Peaceful Positive"
    df.loc[~v_hi & e_hi, "mood_category"] = "Tense Aggressive"
    df.loc[~v_hi & ~e_hi, "mood_category"] = "Sad Melancholic"

    # thị phần stream của bài trong từng quốc gia theo tuần
    total_streams = df.groupby(["country", "week"])["streams"].transform("sum")
    df["stream_share_country"] = np.where(total_streams > 0, df["streams"] / total_streams, 0)

    # gộp energy và loudness (đã min-max) thành một chỉ số
    l_min = df["loudness"].min()
    l_range = df["loudness"].max() - l_min
    l_norm = (df["loudness"] - l_min) / l_range if l_range > 0 else 0.5
    df["energy_loudness_index"] = (df["energy"] + l_norm) / 2

    # latin / kpop: dựa vào genre hoặc ngôn ngữ
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

    # giữ đúng các cột cần dùng
    final_cols = [c for c in FINAL_INSIGHT_COLUMNS if c in df.columns]
    df = df[final_cols]

    # làm tròn số thực
    float_cols = df.select_dtypes(include=["float64", "float32"]).columns
    for c in float_cols:
        if c == "gdp_value":
            df[c] = df[c].round(0)
        elif c != "popularity":
            df[c] = df[c].round(3)

    print(f"  master: {len(df):,} dòng, {len(df.columns)} cột")

    if save:
        os.makedirs(PROCESSED_DIR, exist_ok=True)
        out_path = os.path.join(PROCESSED_DIR, "merged_spotify_data.csv")
        df.to_csv(out_path, index=False)
        mb = os.path.getsize(out_path) / 1e6
        print(f"  đã lưu {out_path} ({mb:.1f} MB)")

    return df


# Bước 3: xuất file dữ liệu cấp bài hát cho ML


def generate_ml_dataset(df_master, save=True):
    """
    Tạo file tracks_ml_data.csv: mỗi bài một dòng (song-level), dùng cho ML.
    Gom theo track_id để tránh rò rỉ dữ liệu (data leakage) giữa train và test.
    """
    print("\nTạo dữ liệu cấp bài hát cho ML")

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
        "is_trending": "max",  # 1 nếu bài từng vào top 50
    }
    avail_rules = {k: v for k, v in agg_rules.items() if k in df_master.columns}
    ml_data = df_master.groupby("track_id").agg(avail_rules).reset_index()

    ml_float_cols = ml_data.select_dtypes(include=["float64", "float32"]).columns
    for c in ml_float_cols:
        ml_data[c] = ml_data[c].round(3)

    ml_path = os.path.join(PROCESSED_DIR, "tracks_ml_data.csv")
    if save:
        os.makedirs(PROCESSED_DIR, exist_ok=True)
        ml_data.to_csv(ml_path, index=False)
        mb2 = os.path.getsize(ml_path) / 1e6
        hit_rate = ml_data["is_trending"].mean() * 100 if "is_trending" in ml_data.columns else 0
        print(f"  {ml_path} ({len(ml_data):,} bài, {len(ml_data.columns)} cột, {mb2:.1f} MB, tỷ lệ hit {hit_rate:.1f}%)")

    return ml_data


# Hàm chạy chính và các hàm nạp dữ liệu tiện dụng


def run_full_pipeline(save=True):
    """Chạy cả pipeline: nạp, làm sạch, tạo master và tạo tập dữ liệu ML."""
    t0 = datetime.now()
    print(f"Spotify audio trends pipeline, bắt đầu lúc {t0:%Y-%m-%d %H:%M:%S}\n")

    charts, tracks, gdp, country_codes, artists = load_raw_data()

    charts_clean = clean_raw_charts(charts)
    tracks_clean = clean_raw_tracks(tracks)
    artists_clean = clean_raw_artists(artists)
    gdp_clean = clean_raw_gdp(gdp)
    country_codes_clean = clean_raw_country_codes(country_codes)

    df_master = build_master_dataset(
        charts_clean, gdp_clean, country_codes_clean, tracks_clean, artists_clean, save=save
    )

    df_ml = generate_ml_dataset(df_master, save=save)

    print(f"\nXong, mất {datetime.now() - t0}")
    return df_master, df_ml


def load_master_data(nrows=None):
    """Đọc file master (merged_spotify_data.csv)."""
    p = os.path.join(PROCESSED_DIR, "merged_spotify_data.csv")
    if not os.path.exists(p):
        raise FileNotFoundError(f"Chưa có file: {p}\nChạy: python src/data_loader.py")
    df = pd.read_csv(p, nrows=nrows, low_memory=False)
    df["week"] = pd.to_datetime(df["week"], errors="coerce")
    if "explicit" in df.columns:
        df["explicit"] = df["explicit"].astype("boolean")
    print(f"Đã nạp master: {len(df):,} dòng, {len(df.columns)} cột")
    return df


def load_ml_data():
    """Đọc dữ liệu cấp bài hát dùng cho ML."""
    p = os.path.join(PROCESSED_DIR, "tracks_ml_data.csv")
    if not os.path.exists(p):
        raise FileNotFoundError(f"Chưa có file: {p}\nChạy: python src/data_loader.py")
    df = pd.read_csv(p)
    print(f"Đã nạp dữ liệu ML: {len(df):,} bài, {len(df.columns)} cột")
    return df


def data_quality_report(df, name="Dataset"):
    """Bảng tóm tắt chất lượng dữ liệu: kiểu, null, số giá trị khác nhau."""
    report = pd.DataFrame({
        "Column": df.columns,
        "Dtype": df.dtypes.astype(str).values,
        "Non-Null": df.notna().sum().values,
        "Null": df.isnull().sum().values,
        "Null%": (df.isnull().mean() * 100).round(2).values,
        "Unique": df.nunique().values,
    })
    print(f"\nData quality - {name} ({len(df):,} dòng, {len(df.columns)} cột)")
    return report


# alias tương thích ngược
load_ml_sample = load_ml_data
clean_weekly_charts = clean_raw_charts
clean_tracks_dataset = clean_raw_tracks
clean_best_selling_artists = clean_raw_artists
join_all_tables = build_master_dataset


if __name__ == "__main__":
    run_full_pipeline()
