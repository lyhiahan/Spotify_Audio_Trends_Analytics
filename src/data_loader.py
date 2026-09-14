"""
src/data_loader.py
==================
Pipeline hoàn chỉnh nạp, làm sạch và kết nối (JOIN) 5 bảng dữ liệu.

6 Bước xử lý:
    1. Nạp dữ liệu thô (Load Raw Data)
    2. Làm sạch bảng xếp hạng tuần (Clean Weekly Charts)
    3. Làm sạch bảng đặc trưng bài hát (Clean Tracks Dataset)
    4. Làm sạch bảng nghệ sĩ bán đĩa (Clean Best-Selling Artists)
    5. JOIN 5 bảng dữ liệu (Merge All Tables)
    6. Tạo 12+ trường tính toán (Calculated Fields)

Output:
    - data/processed/merged_spotify_data.csv (Full dataset)
    - data/sample/spotify_sample_merged.csv  (20,000 rows sample)

Author: Đinh Quốc Anh (Data Engineer & Data Analyst)
"""

import os
import re
import warnings
import numpy as np
import pandas as pd
from datetime import datetime

warnings.filterwarnings("ignore")

# ══════════════════════ Cấu hình đường dẫn ══════════════════════
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
SAMPLE_DIR = os.path.join(BASE_DIR, "data", "sample")

# ══════════════════════ Cấu hình phân tích ══════════════════════
AUDIO_FEATURES = [
    "danceability", "energy", "loudness", "speechiness",
    "acousticness", "instrumentalness", "liveness", "valence", "tempo"
]
AUDIO_0_1 = [
    "danceability", "energy", "speechiness", "acousticness",
    "instrumentalness", "liveness", "valence"
]
TRENDING_THRESHOLD = 50   # rank <= 50 → is_trending = 1
POPULAR_THRESHOLD = 70    # popularity >= 70 → is_popular = 1

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


# ═══════════════════════════════════════════════════════════════
# BƯỚC 1: NẠP DỮ LIỆU THÔ
# ═══════════════════════════════════════════════════════════════

def load_raw_data():
    """
    Nạp 5 tập dữ liệu gốc từ thư mục data/raw/.

    Returns
    -------
    tuple of (charts, tracks, gdp, country_codes, artists) DataFrames.
    """
    print("=" * 60)
    print("📂 BƯỚC 1: NẠP DỮ LIỆU THÔ")
    print("=" * 60)

    # 1. Weekly Charts (~835 MB — cần low_memory=False)
    print("  ⏳ Đang nạp spotify-weekly-charts.csv (~835 MB)...")
    charts = pd.read_csv(
        os.path.join(RAW_DIR, "spotify-weekly-charts.csv"),
        low_memory=False,
    )
    print(f"  ✅ Weekly Charts: {charts.shape[0]:,} dòng × {charts.shape[1]} cột")

    # 2. Tracks Dataset (~20 MB)
    print("  ⏳ Đang nạp spotify-tracks-dataset.csv...")
    tracks = pd.read_csv(
        os.path.join(RAW_DIR, "spotify-tracks-dataset.csv"),
        low_memory=False,
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

    total = sum(df.shape[0] for df in [charts, tracks, gdp, country_codes, artists])
    print(f"\n  📊 Tổng cộng: {total:,} bản ghi từ 5 bảng")
    return charts, tracks, gdp, country_codes, artists


# ═══════════════════════════════════════════════════════════════
# BƯỚC 2: LÀM SẠCH BẢNG XẾP HẠNG TUẦN
# ═══════════════════════════════════════════════════════════════

def clean_weekly_charts(df):
    """
    Làm sạch bảng spotify-weekly-charts.csv.

    Xử lý:
        - Trích ``track_id`` từ cột ``uri``
        - Chuyển ``week`` → datetime; trích ``year``, ``month``, ``quarter``
        - Ép kiểu ``streams``, loại streams ≤ 0
        - Loại bản ghi trùng (track_id + week + country)
        - Đổi tên cột ``region`` → ``region_spotify``
    """
    print("\n" + "=" * 60)
    print("🧹 BƯỚC 2: LÀM SẠCH BẢNG XẾP HẠNG TUẦN")
    print("=" * 60)

    df = df.copy()
    n_before = len(df)

    # 2.1 Loại bỏ cột index dư thừa (Unnamed: 0)
    unnamed_cols = [c for c in df.columns if "Unnamed" in str(c)]
    if unnamed_cols:
        df.drop(columns=unnamed_cols, inplace=True)
        print(f"  🔹 Loại bỏ {len(unnamed_cols)} cột index dư thừa: {unnamed_cols}")

    # 2.2 Trích xuất track_id từ uri
    if "track_id" not in df.columns and "uri" in df.columns:
        df["track_id"] = df["uri"].str.replace("spotify:track:", "", regex=False)
        print(f"  🔹 Trích xuất track_id từ uri → {df['track_id'].nunique():,} bài hát duy nhất")

    # 2.3 Chuyển đổi week → datetime + trích thời gian
    df["week"] = pd.to_datetime(df["week"], errors="coerce")
    df["year"] = df["week"].dt.year.astype("Int64")
    df["month"] = df["week"].dt.month.astype("Int64")
    df["quarter"] = df["week"].dt.quarter.astype("Int64")
    n_bad_dates = df["week"].isna().sum()
    if n_bad_dates > 0:
        print(f"  ⚠️  {n_bad_dates:,} dòng ngày không hợp lệ → Loại bỏ")
        df.dropna(subset=["week"], inplace=True)
    print(f"  🔹 Phạm vi thời gian: {df['week'].min().date()} → {df['week'].max().date()}")
    print(f"  🔹 Các năm có dữ liệu: {sorted(df['year'].dropna().unique().tolist())}")

    # 2.4 Xử lý streams
    df["streams"] = pd.to_numeric(df["streams"], errors="coerce")
    n_na_streams = df["streams"].isna().sum()
    if n_na_streams > 0:
        print(f"  ⚠️  {n_na_streams:,} dòng streams NaN → Đặt = 0")
        df["streams"] = df["streams"].fillna(0)
    df["streams"] = df["streams"].astype(int)
    n_zero = (df["streams"] <= 0).sum()
    if n_zero > 0:
        print(f"  ⚠️  {n_zero:,} dòng streams ≤ 0 → Loại bỏ")
        df = df[df["streams"] > 0]

    # 2.5 Ép kiểu cột ranking
    for col in ["rank", "previous_rank", "weeks_on_chart", "peak_rank"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    # 2.6 Chuẩn hóa tên quốc gia
    df["country"] = df["country"].str.strip()

    # 2.7 Ép kiểu duration (ms)
    if "duration" in df.columns:
        df["duration"] = pd.to_numeric(df["duration"], errors="coerce")

    # 2.7b Ép kiểu tất cả audio features về numeric
    # (Cần thiết vì file CSV lớn có thể đọc mixed types thành string)
    for col in AUDIO_FEATURES:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    n_coerced = sum(1 for c in AUDIO_FEATURES if c in df.columns)
    print(f"  🔹 Ép kiểu numeric cho {n_coerced} audio features")

    # 2.8 Loại bản ghi trùng (track_id + week + country)
    n_dups = df.duplicated(subset=["track_id", "week", "country"]).sum()
    if n_dups > 0:
        print(f"  ⚠️  {n_dups:,} bản ghi trùng (track_id+week+country) → Giữ bản đầu")
        df.drop_duplicates(subset=["track_id", "week", "country"], keep="first", inplace=True)

    # 2.9 Loại cột không cần thiết cho phân tích
    drop_cols = ["artist_img", "album_cover", "pivot"]
    existing_drops = [c for c in drop_cols if c in df.columns]
    if existing_drops:
        df.drop(columns=existing_drops, inplace=True)
        print(f"  🔹 Loại {len(existing_drops)} cột không cần: {existing_drops}")

    # 2.10 Đổi tên region (Spotify) để tránh xung đột với World Bank
    if "region" in df.columns:
        df.rename(columns={"region": "region_spotify"}, inplace=True)
        print("  🔹 Đổi tên 'region' → 'region_spotify'")

    # Nếu đã có region_x từ merge trước đó
    if "region_x" in df.columns:
        df.rename(columns={"region_x": "region_spotify"}, inplace=True)

    n_after = len(df)
    print(f"\n  📊 Kết quả: {n_before:,} → {n_after:,} dòng "
          f"({n_before - n_after:,} dòng bị loại)")
    return df


# ═══════════════════════════════════════════════════════════════
# BƯỚC 3: LÀM SẠCH BẢNG ĐẶC TRƯNG BÀI HÁT
# ═══════════════════════════════════════════════════════════════

def clean_tracks_dataset(df):
    """
    Làm sạch bảng spotify-tracks-dataset.csv.

    Xử lý:
        - Loại cột index dư thừa
        - Dedup ``track_id`` (giữ popularity cao nhất)
        - Validate audio features nằm trong [0, 1]
        - Validate loudness, tempo, duration_ms
        - Giữ lại các cột cần thiết cho JOIN
    """
    print("\n" + "=" * 60)
    print("🧹 BƯỚC 3: LÀM SẠCH BẢNG ĐẶC TRƯNG BÀI HÁT")
    print("=" * 60)

    df = df.copy()

    # 3.1 Loại cột index dư thừa
    unnamed_cols = [c for c in df.columns if "Unnamed" in str(c)]
    if unnamed_cols:
        df.drop(columns=unnamed_cols, inplace=True)
        print(f"  🔹 Loại bỏ {len(unnamed_cols)} cột index dư thừa")

    # 3.2 Dedup track_id — giữ bản ghi popularity cao nhất
    n_before = len(df)
    n_unique = df["track_id"].nunique()
    if n_before > n_unique:
        df = (df
              .sort_values("popularity", ascending=False)
              .drop_duplicates("track_id", keep="first"))
        print(f"  🔹 Dedup track_id: {n_before:,} → {len(df):,} "
              f"({n_before - len(df):,} bản trùng)")

    # 3.3 Validate audio features [0, 1]
    for col in AUDIO_0_1:
        if col in df.columns:
            n_bad = ((df[col] < 0) | (df[col] > 1)).sum()
            if n_bad > 0:
                print(f"  ⚠️  {col}: {n_bad:,} ngoài [0,1] → clip")
                df[col] = df[col].clip(0, 1)

    # 3.4 Validate loudness (thường -60 → 0 dB)
    if "loudness" in df.columns:
        df["loudness"] = df["loudness"].clip(-60, 5)

    # 3.5 Validate tempo (40-300 BPM)
    if "tempo" in df.columns:
        df["tempo"] = df["tempo"].clip(0, 300)

    # 3.6 Xử lý duration_ms bất thường (< 30 s hoặc > 15 min)
    if "duration_ms" in df.columns:
        mask_bad = (df["duration_ms"] < 30_000) | (df["duration_ms"] > 900_000)
        n_bad_dur = mask_bad.sum()
        if n_bad_dur > 0:
            print(f"  ⚠️  duration_ms: {n_bad_dur:,} bài < 30s hoặc > 15 min → NaN")
            df.loc[mask_bad, "duration_ms"] = np.nan

    # 3.7 Giữ cột cần thiết cho JOIN
    # (Audio features đã có trong weekly charts — chỉ cần genre, popularity, …)
    keep = ["track_id", "track_genre", "popularity", "duration_ms",
            "explicit", "artists", "album_name", "time_signature"]
    keep = [c for c in keep if c in df.columns]
    df = df[keep]

    print(f"\n  📊 Bảng tracks sau làm sạch: {len(df):,} bài × {len(df.columns)} cột")
    return df


# ═══════════════════════════════════════════════════════════════
# BƯỚC 4: LÀM SẠCH BẢNG NGHỆ SĨ BÁN ĐĨA
# ═══════════════════════════════════════════════════════════════

def clean_best_selling_artists(df):
    """
    Làm sạch bảng best-selling-artists.csv.

    Xử lý:
        - Parse ``Total certified units`` → triệu đơn vị (float)
        - Parse ``Claimed sales`` → triệu đơn vị (float)
        - Fix encoding ``Active years``; trích career_start / career_end
        - Chuẩn hóa tên nghệ sĩ (lower-case) cho JOIN
    """
    print("\n" + "=" * 60)
    print("🧹 BƯỚC 4: LÀM SẠCH BẢNG NGHỆ SĨ BÁN ĐĨA")
    print("=" * 60)

    df = df.copy()

    # ---- helper parse ----
    def _parse_millions(text):
        """Trích số triệu đầu tiên từ chuỗi phức tạp."""
        if pd.isna(text):
            return np.nan
        text = str(text)
        m = re.search(r"([\d,.]+)\s*million", text, re.IGNORECASE)
        if m:
            try:
                return float(m.group(1).replace(",", ""))
            except ValueError:
                return np.nan
        return np.nan

    # 4.1 Parse certified units
    df["certified_units_million"] = df["Total certified units"].apply(_parse_millions)
    ok = df["certified_units_million"].notna().sum()
    print(f"  🔹 Parse certified units: {ok}/{len(df)} thành công")

    # 4.2 Parse claimed sales
    df["claimed_sales_million"] = df["Claimed sales"].apply(_parse_millions)

    # 4.3 Fix Active years → career_start, career_end
    def _parse_years(text):
        if pd.isna(text):
            return np.nan, np.nan
        years = re.findall(r"\d{4}", str(text))
        if len(years) >= 2:
            return int(years[0]), int(years[-1])
        if len(years) == 1:
            return int(years[0]), np.nan
        return np.nan, np.nan

    df[["career_start", "career_end"]] = df["Active years"].apply(
        lambda x: pd.Series(_parse_years(x))
    )
    print("  🔹 Trích career_start & career_end từ Active years")

    # 4.4 Chuẩn hóa tên nghệ sĩ
    df["artist_name_clean"] = df["Artist name"].str.strip().str.lower()

    # 4.5 Giữ cột cần thiết
    out = df[[
        "Artist name", "artist_name_clean", "Country", "Genre",
        "certified_units_million", "claimed_sales_million",
        "career_start", "career_end",
        "Release year of first charted record",
    ]].copy()
    out.rename(columns={
        "Artist name": "legacy_artist_name",
        "Country": "legacy_artist_country",
        "Genre": "legacy_artist_genre",
        "Release year of first charted record": "first_charted_year",
    }, inplace=True)

    print(f"\n  📊 Best-Selling Artists sau làm sạch: {len(out):,} nghệ sĩ × {len(out.columns)} cột")
    return out


# ═══════════════════════════════════════════════════════════════
# BƯỚC 5: JOIN 5 BẢNG DỮ LIỆU
# ═══════════════════════════════════════════════════════════════

def join_all_tables(charts, tracks, gdp, country_codes, artists):
    """
    Kết nối 5 bảng thành bảng tổng thể (LEFT JOIN từ charts).

    Sơ đồ JOIN::

        charts ⋈ (country, year) ──→ gdp (GDP value)
               ⋈ (country_code)  ──→ country_codes (region, income_group)
               ⋈ (track_id)      ──→ tracks (genre, popularity)
               ⋈ (artist_name)   ──→ best_selling_artists (legacy status)
    """
    print("\n" + "=" * 60)
    print("🔗 BƯỚC 5: JOIN 5 BẢNG DỮ LIỆU")
    print("=" * 60)

    n_start = len(charts)

    # ── JOIN 1: Charts + GDP (country + year) ──
    print("  🔹 JOIN 1: Charts ⋈ GDP (country, year)...")
    merged = pd.merge(
        charts, gdp,
        left_on=["country", "year"],
        right_on=["country_name", "year"],
        how="left",
    )
    if "value" in merged.columns:
        merged.rename(columns={"value": "gdp_value"}, inplace=True)
    rate = merged["gdp_value"].notna().mean() * 100
    print(f"    → Match rate: {rate:.1f}%")

    # ── JOIN 2: + Country Codes (country_code) ──
    print("  🔹 JOIN 2: + Country Codes (country_code)...")
    merged = pd.merge(merged, country_codes, on="country_code", how="left")
    rate = merged["region"].notna().mean() * 100
    print(f"    → Region match rate: {rate:.1f}%")
    merged.rename(columns={"region": "region_wb"}, inplace=True)

    # ── JOIN 3: + Tracks Dataset (track_id) ──
    print("  🔹 JOIN 3: + Tracks Dataset (track_id)...")
    merged = pd.merge(
        merged, tracks,
        on="track_id", how="left",
        suffixes=("", "_tracks"),
    )
    rate = merged["track_genre"].notna().mean() * 100
    print(f"    → Genre match rate: {rate:.1f}%")

    # ── JOIN 4: + Best-Selling Artists (artist name) ──
    print("  🔹 JOIN 4: + Best-Selling Artists (artist_name)...")
    merged["_artist_clean"] = merged["artist_individual"].str.strip().str.lower()
    merged = pd.merge(
        merged,
        artists[["artist_name_clean", "legacy_artist_name",
                  "certified_units_million", "claimed_sales_million",
                  "career_start", "legacy_artist_genre"]],
        left_on="_artist_clean",
        right_on="artist_name_clean",
        how="left",
    )
    n_legacy = merged["legacy_artist_name"].notna().sum()
    print(f"    → {n_legacy:,} bản ghi khớp nghệ sĩ huyền thoại")

    # ── Dọn dẹp cột dư ──
    drop = ["country_name", "artist_name_clean", "_artist_clean"]
    merged.drop(columns=[c for c in drop if c in merged.columns], inplace=True)

    print(f"\n  📊 Sau JOIN: {len(merged):,} dòng × {len(merged.columns)} cột")
    if len(merged) != n_start:
        print(f"  ⚠️  Số dòng thay đổi {n_start:,} → {len(merged):,}")
    return merged


# ═══════════════════════════════════════════════════════════════
# BƯỚC 6: TẠO CALCULATED FIELDS
# ═══════════════════════════════════════════════════════════════

def create_calculated_fields(df):
    """
    Tạo 13 trường tính toán mới (Calculated Fields).

    Phục vụ các hướng phân tích:
        - GDP vs Valence Paradox
        - 3 giai đoạn COVID-19 (Lockdown → Escapism → Reopening)
        - Latin Wave & K-Pop Invasion
        - Đa dạng gu âm nhạc theo thu nhập
        - Công thức bài hát Hit
    """
    print("\n" + "=" * 60)
    print("🧮 BƯỚC 6: TẠO CALCULATED FIELDS")
    print("=" * 60)

    df = df.copy()

    # ── 1. is_trending (rank ≤ 50) ──
    df["is_trending"] = (df["rank"] <= TRENDING_THRESHOLD).astype(int)
    n = df["is_trending"].sum()
    print(f"  ✅ is_trending (rank ≤ {TRENDING_THRESHOLD}): "
          f"{n:,} ({n / len(df) * 100:.1f}%)")

    # ── 2. is_popular (popularity ≥ 70) ──
    df["is_popular"] = 0
    mask = df["popularity"].notna() & (df["popularity"] >= POPULAR_THRESHOLD)
    df.loc[mask, "is_popular"] = 1
    print(f"  ✅ is_popular (popularity ≥ {POPULAR_THRESHOLD}): "
          f"{df['is_popular'].sum():,}")

    # ── 3. mood_category (vectorized) ──
    v_hi = df["valence"] >= 0.5
    e_hi = df["energy"] >= 0.5
    df["mood_category"] = "Unknown"
    df.loc[v_hi & e_hi, "mood_category"] = "Happy Energetic"
    df.loc[v_hi & ~e_hi, "mood_category"] = "Peaceful Positive"
    df.loc[~v_hi & e_hi, "mood_category"] = "Tense Aggressive"
    df.loc[~v_hi & ~e_hi, "mood_category"] = "Sad Melancholic"
    print(f"  ✅ mood_category: {df['mood_category'].value_counts().to_dict()}")

    # ── 4. stream_share_country ──
    total = df.groupby(["country", "week"])["streams"].transform("sum")
    df["stream_share_country"] = np.where(total > 0, df["streams"] / total, 0)
    print(f"  ✅ stream_share_country: "
          f"[{df['stream_share_country'].min():.4f}, "
          f"{df['stream_share_country'].max():.4f}]")

    # ── 5. covid_phase (vectorized) ──
    df["covid_phase"] = "Unknown"
    df.loc[df["year"] <= 2020, "covid_phase"] = "Lockdown & Shock"
    df.loc[df["year"] == 2021, "covid_phase"] = "Vaccine & Escapism"
    df.loc[df["year"] >= 2022, "covid_phase"] = "Reopening & New Normal"
    print(f"  ✅ covid_phase: {df['covid_phase'].value_counts().to_dict()}")

    # ── 6. energy_loudness_index ──
    if "loudness" in df.columns and "energy" in df.columns:
        l_min = df["loudness"].min()
        l_range = df["loudness"].max() - l_min
        l_norm = (df["loudness"] - l_min) / l_range if l_range > 0 else 0.5
        df["energy_loudness_index"] = (df["energy"] + l_norm) / 2
        print(f"  ✅ energy_loudness_index: mean = "
              f"{df['energy_loudness_index'].mean():.3f}")

    # ── 7. is_latin (vectorized) ──
    genre_combo = (df["artist_genre"].fillna("").str.lower()
                   + " " + df["track_genre"].fillna("").str.lower())
    latin_pat = "|".join(re.escape(kw) for kw in LATIN_KEYWORDS)
    lang_latin = df["language"].fillna("").str.lower().isin(["spanish", "portuguese"])
    df["is_latin"] = (genre_combo.str.contains(latin_pat, na=False) | lang_latin).astype(int)
    n = df["is_latin"].sum()
    print(f"  ✅ is_latin: {n:,} ({n / len(df) * 100:.1f}%)")

    # ── 8. is_kpop (vectorized) ──
    kpop_pat = "|".join(re.escape(kw) for kw in KPOP_KEYWORDS)
    lang_kr = df["language"].fillna("").str.lower().isin(["korean"])
    df["is_kpop"] = (genre_combo.str.contains(kpop_pat, na=False) | lang_kr).astype(int)
    n = df["is_kpop"].sum()
    print(f"  ✅ is_kpop: {n:,} ({n / len(df) * 100:.1f}%)")

    # ── 9. is_legacy_artist ──
    df["is_legacy_artist"] = df["legacy_artist_name"].notna().astype(int)
    print(f"  ✅ is_legacy_artist: {df['is_legacy_artist'].sum():,}")

    # ── 10. duration_min ──
    dur_col = "duration" if "duration" in df.columns else "duration_ms"
    if dur_col in df.columns:
        df["duration_min"] = df[dur_col] / 60_000
        print(f"  ✅ duration_min: mean = {df['duration_min'].mean():.2f} phút")

    # ── 11. audio_diversity_score ──
    div_cols = ["danceability", "energy", "valence", "acousticness"]
    avail = [c for c in div_cols if c in df.columns]
    if avail:
        df["audio_diversity_score"] = df[avail].std(axis=1)
        print(f"  ✅ audio_diversity_score: mean = "
              f"{df['audio_diversity_score'].mean():.4f}")

    # ── 12. log_streams ──
    df["log_streams"] = np.log1p(df["streams"])
    print(f"  ✅ log_streams: [{df['log_streams'].min():.2f}, "
          f"{df['log_streams'].max():.2f}]")

    # ── 13. gdp_log ──
    if "gdp_value" in df.columns:
        df["gdp_log"] = np.log1p(df["gdp_value"])
        print(f"  ✅ gdp_log: [{df['gdp_log'].min():.2f}, "
              f"{df['gdp_log'].max():.2f}]")

    print(f"\n  📊 Tổng: {len(df.columns)} cột sau khi thêm Calculated Fields")
    return df


# ═══════════════════════════════════════════════════════════════
# PIPELINE TỔNG THỂ
# ═══════════════════════════════════════════════════════════════

def run_full_pipeline(sample_size=None, save=True):
    """
    Chạy toàn bộ pipeline ETL 6 bước.

    Parameters
    ----------
    sample_size : int, optional
        Nếu chỉ định, lấy mẫu ngẫu nhiên từ charts.
    save : bool
        Nếu ``True``, lưu file CSV output.

    Returns
    -------
    pd.DataFrame
        Bảng dữ liệu tổng hợp hoàn chỉnh.
    """
    t0 = datetime.now()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  🚀 SPOTIFY AUDIO TRENDS — DATA PIPELINE               ║")
    print("║  Tiền xử lý • Làm sạch • JOIN 5 Bảng • Calculated     ║")
    print(f"║  Bắt đầu: {t0:%Y-%m-%d %H:%M:%S}                          ║")
    print("╚══════════════════════════════════════════════════════════╝")

    # Bước 1 – Nạp
    charts, tracks, gdp, country_codes, artists = load_raw_data()

    if sample_size:
        print(f"\n  ⚡ CHẾ ĐỘ SAMPLE: lấy {sample_size:,} dòng từ Charts")
        charts = charts.sample(n=min(sample_size, len(charts)), random_state=42)

    # Bước 2 – Sạch Charts
    charts_clean = clean_weekly_charts(charts)

    # Bước 3 – Sạch Tracks
    tracks_clean = clean_tracks_dataset(tracks)

    # Bước 4 – Sạch Artists
    artists_clean = clean_best_selling_artists(artists)

    # Bước 5 – JOIN
    merged = join_all_tables(charts_clean, tracks_clean, gdp, country_codes, artists_clean)

    # Bước 6 – Calculated Fields
    final = create_calculated_fields(merged)

    # ── Xuất ──
    if save:
        print("\n" + "=" * 60)
        print("💾 XUẤT KẾT QUẢ")
        print("=" * 60)

        os.makedirs(PROCESSED_DIR, exist_ok=True)
        os.makedirs(SAMPLE_DIR, exist_ok=True)

        full_path = os.path.join(PROCESSED_DIR, "merged_spotify_data.csv")
        final.to_csv(full_path, index=False)
        mb = os.path.getsize(full_path) / 1024 / 1024
        print(f"  ✅ Full: {full_path}")
        print(f"     {len(final):,} dòng × {len(final.columns)} cột ({mb:.1f} MB)")

        sample_df = final.sample(n=min(20_000, len(final)), random_state=42)
        samp_path = os.path.join(SAMPLE_DIR, "spotify_sample_merged.csv")
        sample_df.to_csv(samp_path, index=False)
        smb = os.path.getsize(samp_path) / 1024 / 1024
        print(f"  ✅ Sample: {samp_path}")
        print(f"     {len(sample_df):,} dòng × {len(sample_df.columns)} cột ({smb:.1f} MB)")

    # ── Tổng kết ──
    elapsed = datetime.now() - t0
    print("\n" + "═" * 60)
    print("📊 TỔNG KẾT PIPELINE")
    print("═" * 60)
    print(f"  Thời gian : {elapsed}")
    print(f"  Dòng      : {len(final):,}")
    print(f"  Cột       : {len(final.columns)}")
    null_pct = final.isnull().sum().sum() / (len(final) * len(final.columns)) * 100
    print(f"  Missing   : {null_pct:.2f}%")
    print(f"  Quốc gia  : {final['country'].nunique()}")
    print(f"  Bài hát   : {final['track_id'].nunique():,}")
    print(f"  Nghệ sĩ   : {final['artist_individual'].nunique():,}")
    print(f"  Thời gian  : {final['week'].min()} → {final['week'].max()}")

    print("\n  📋 Danh sách cột:")
    for i, col in enumerate(final.columns, 1):
        dt = final[col].dtype
        np_ = final[col].isnull().mean() * 100
        print(f"    {i:2d}. {col:<35s} {str(dt):<12s} null {np_:.1f}%")

    return final


# ═══════════════════════════════════════════════════════════════
# HÀM TIỆN ÍCH (cho Dashboard & Notebooks)
# ═══════════════════════════════════════════════════════════════

def load_processed_data():
    """Nạp dữ liệu đã xử lý từ ``data/processed/``."""
    p = os.path.join(PROCESSED_DIR, "merged_spotify_data.csv")
    if not os.path.exists(p):
        raise FileNotFoundError(
            f"File chưa tồn tại: {p}\n"
            "Chạy: python src/data_loader.py"
        )
    df = pd.read_csv(p, low_memory=False)
    df["week"] = pd.to_datetime(df["week"], errors="coerce")
    print(f"✅ Nạp processed: {len(df):,} dòng × {len(df.columns)} cột")
    return df


def load_sample_data():
    """Nạp dữ liệu mẫu từ ``data/sample/`` (test nhanh)."""
    p = os.path.join(SAMPLE_DIR, "spotify_sample_merged.csv")
    if not os.path.exists(p):
        raise FileNotFoundError(
            f"File chưa tồn tại: {p}\n"
            "Chạy: python src/data_loader.py --sample"
        )
    df = pd.read_csv(p, low_memory=False)
    df["week"] = pd.to_datetime(df["week"], errors="coerce")
    print(f"✅ Nạp sample: {len(df):,} dòng × {len(df.columns)} cột")
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
    print(f"\n{'=' * 70}")
    print(f"📋 Data Quality — {name} "
          f"({len(df):,} rows × {len(df.columns)} cols)")
    print("=" * 70)
    return report


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--sample":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 20_000
        print(f"🔬 Chế độ sample ({n:,} dòng)…")
        run_full_pipeline(sample_size=n)
    else:
        run_full_pipeline()
