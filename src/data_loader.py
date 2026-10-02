"""
src/data_loader.py
Module nạp dữ liệu gọn nhẹ cho Đồ án IDVI (Tương tác dữ liệu trực quan).

Chỉ đảm nhiệm:
1. Cấu hình cột giữ/bỏ cho từng bảng thô (COLUMNS_TO_KEEP).
2. Hằng số tham chiếu (AUDIO_FEATURE_COLS, COUNTRY_ALIAS_MAP, GDP_AGGREGATE_NAMES).
3. Kiểm tra file tồn tại (check_raw_files_exist).
4. Nạp từng bảng CSV thô ra DataFrame (load_charts_raw, load_covid_raw, load_gdp_raw, ...).

KHÔNG chứa logic làm sạch sâu, join bảng, hay xuất file.
Toàn bộ logic xử lý đặt trong notebook tương ứng.
"""

import os
from typing import Dict, List, Optional, Union

import numpy as np
import pandas as pd

# ==============================================================================
# CẤU HÌNH CỘT GIỮ LẠI VÀ LOẠI BỎ (COLUMNS_TO_KEEP)
# ==============================================================================
COLUMNS_TO_KEEP: Dict[str, Dict[str, Union[List[str], Dict[str, str]]]] = {
    "spotify-weekly-charts.csv": {
        "drop": {
            "artist_img": "URL ảnh nghệ sĩ, không dùng tính toán, có nhiều giá trị khuyết",
            "album_cover": "URL ảnh bìa album, không dùng tính toán, có nhiều giá trị khuyết",
            "pivot": "Cột kỹ thuật sinh ra trong quá trình crawl dữ liệu gốc",
            "album_num_tracks": "Tổng số bài trong album, không liên quan đến đề tài phân tích",
            "source": "Hãng thu âm/nhà phát hành, không thuộc phạm vi phân tích của đề tài",
            "Unnamed: 0": "Chỉ số index tự sinh khi xuất file CSV gốc",
        },
        "keep": [
            "uri", "track_name", "artist_names", "artist_individual", "artist_id", "rank", "peak_rank",
            "previous_rank", "weeks_on_chart", "streams", "week", "release_date",
            "country", "region", "language", "collab", "artists_num", "artist_genre",
            "danceability", "energy", "key", "mode", "loudness", "speechiness",
            "acousticness", "instrumentalness", "liveness", "valence", "tempo", "duration"
        ],
    },
    "global_deaths.csv": {
        "drop": {},
        "keep": [],  # Bảng ngang 1,144 ngày, giữ toàn bộ cột ngày để unpivot
    },
    "gdp_data.csv": {
        "drop": {},
        "keep": ["country_name", "country_code", "year", "value"],
    },
    "country_codes.csv": {
        "drop": {},
        "keep": ["country_code", "region", "income_group"],
    },
    "whs_years_updated.csv": {
        "drop": {},
        "keep": [],  # Giữ toàn bộ cột để xử lý hài hòa thang đo 10 năm trong notebook
    },
}

# ==============================================================================
# HẰNG SỐ THAM CHIẾU
# ==============================================================================

# 12 đặc trưng âm học chuẩn của Spotify Audio API
AUDIO_FEATURE_COLS: List[str] = [
    "danceability", "energy", "key", "mode", "loudness", "speechiness",
    "acousticness", "instrumentalness", "liveness", "valence", "tempo", "duration"
]

# Ánh xạ tên quốc gia Spotify → tên quốc gia World Bank (7 trường hợp khác biệt)
COUNTRY_ALIAS_MAP: Dict[str, str] = {
    "Czech Republic": "Czechia",
    "Egypt": "Egypt, Arab Rep.",
    "Hong Kong": "Hong Kong SAR, China",
    "Korea": "Korea, Rep.",
    "Slovakia": "Slovak Republic",
    "Turkey": "Turkiye",
    "Venezuela": "Venezuela, RB",
}

# Tên các nhóm tổng hợp/khu vực cần loại khỏi GDP (không phải quốc gia đơn lẻ)
GDP_AGGREGATE_NAMES: List[str] = [
    "World", "High income", "Low income", "Middle income",
    "Upper middle income", "Lower middle income",
    "OECD members", "East Asia & Pacific", "Europe & Central Asia",
    "Latin America & Caribbean", "Middle East & North Africa",
    "North America", "South Asia", "Sub-Saharan Africa",
    "European Union", "Euro area", "Arab World",
    "Africa Eastern and Southern", "Africa Western and Central",
    "Caribbean small states", "Central Europe and the Baltics",
    "Early-demographic dividend", "East Asia & Pacific (excluding high income)",
    "East Asia & Pacific (IDA & IBRD countries)",
    "Europe & Central Asia (excluding high income)",
    "Europe & Central Asia (IDA & IBRD countries)",
    "Fragile and conflict affected situations",
    "Heavily indebted poor countries (HIPC)",
    "IBRD only", "IDA & IBRD total", "IDA blend", "IDA only", "IDA total",
    "Late-demographic dividend", "Latin America & Caribbean (excluding high income)",
    "Latin America & the Caribbean (IDA & IBRD countries)",
    "Least developed countries: UN classification",
    "Low & middle income",
    "Middle East & North Africa (excluding high income)",
    "Middle East & North Africa (IDA & IBRD countries)",
    "Not classified",
    "Other small states", "Pacific island small states",
    "Post-demographic dividend", "Pre-demographic dividend",
    "Small states",
    "South Asia (IDA & IBRD)",
    "Sub-Saharan Africa (excluding high income)",
    "Sub-Saharan Africa (IDA & IBRD countries)",
]


# ==============================================================================
# HÀM KIỂM TRA TỒN TẠI FILE
# ==============================================================================

def check_raw_files_exist(raw_dir: str = "data/raw") -> bool:
    """
    Kiểm tra sự tồn tại của 5 tập tin CSV đầu vào trong thư mục raw_dir.
    Trả về True nếu đủ file, False nếu thiếu (kèm log hướng dẫn).
    """
    expected_files = {
        "spotify-weekly-charts.csv": "Kaggle: Weekly Charts (yelexa)",
        "global_deaths.csv": "JHU CSSE: COVID-19 Global Deaths",
        "gdp_data.csv": "World Bank Open Data (Kaggle: Sazidul Islam)",
        "country_codes.csv": "World Bank Metadata (Kaggle: Sazidul Islam)",
        "whs_years_updated.csv": "World Happiness Report (2015-2024)",
    }
    missing = []
    for fname, source in expected_files.items():
        fpath = os.path.join(raw_dir, fname)
        if not os.path.exists(fpath):
            missing.append((fname, source, fpath))

    if missing:
        print("[LỖI] Không tìm thấy các file dữ liệu thô cần thiết:")
        for fname, source, fpath in missing:
            print(f"  - Thiếu: {fname} | Nguồn: {source}")
            print(f"    Đường dẫn mong đợi: {fpath}")
        print("\n[HƯỚNG DẪN] Tải các file trên và đặt vào thư mục data/raw/.")
        return False
    return True


# ==============================================================================
# HÀM NẠP DỮ LIỆU THÔ (LOAD RAW)
# ==============================================================================

def load_charts_raw(
    path: str,
    chunksize: int = 500_000,
    usecols: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Nạp spotify-weekly-charts.csv theo chunk, loại bỏ dòng header rác,
    ép kiểu cơ bản (streams → int64, rank/peak_rank/weeks_on_chart → int32,
    audio features → float32, week → datetime).

    Trả về DataFrame thô đã lọc cấu trúc, CHƯA làm sạch nghiệp vụ.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Không tìm thấy file charts tại: {path}")

    if usecols is None:
        usecols = COLUMNS_TO_KEEP["spotify-weekly-charts.csv"]["keep"]

    print(f"[LOAD] Đang đọc charts từ {path} (chunksize={chunksize:,}, {len(usecols)} cột)...")

    chunks: List[pd.DataFrame] = []
    total_raw = 0
    total_junk = 0

    for i, chunk in enumerate(pd.read_csv(path, chunksize=chunksize, usecols=usecols, low_memory=False)):
        total_raw += len(chunk)

        # Lọc dòng header rác: rank == 'rank' hoặc streams == 'streams'
        junk = (chunk["rank"].astype(str) == "rank") | (chunk["streams"].astype(str) == "streams")
        junk_n = int(junk.sum())
        total_junk += junk_n
        clean = chunk[~junk].copy()

        # Ép kiểu an toàn sau khi loại dòng rác
        clean["streams"] = pd.to_numeric(clean["streams"], errors="coerce").fillna(0).astype(np.int64)

        for col in ["rank", "peak_rank", "weeks_on_chart"]:
            if col in clean.columns:
                clean[col] = pd.to_numeric(clean[col], errors="coerce").fillna(0).astype(np.int32)

        for col in AUDIO_FEATURE_COLS:
            if col in clean.columns:
                clean[col] = pd.to_numeric(clean[col], errors="coerce").astype(np.float32)

        if "week" in clean.columns:
            clean["week"] = pd.to_datetime(clean["week"], errors="coerce")

        chunks.append(clean)
        print(f"  -> Chunk {i + 1}: {len(clean):,} dòng (loại {junk_n} header rác)")

    df = pd.concat(chunks, ignore_index=True)
    print(f"[LOAD HOÀN THÀNH] Tổng thô: {total_raw:,} | Loại rác: {total_junk} | Còn lại: {len(df):,} dòng, {len(df.columns)} cột")

    if total_junk != 73:
        print(f"  [CẢNH BÁO] Số dòng rác thực tế ({total_junk}) khác kỳ vọng (73).")

    return df


def load_covid_raw(path: str) -> pd.DataFrame:
    """Nạp global_deaths.csv (JHU CSSE COVID-19 Deaths). Trả về DataFrame thô bảng ngang."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Không tìm thấy file COVID tại: {path}")

    df = pd.read_csv(path)
    print(f"[LOAD] COVID: {len(df):,} dòng (thực thể/tỉnh bang), {len(df.columns)} cột (ngày)")
    return df


def load_gdp_raw(path: str) -> pd.DataFrame:
    """Nạp gdp_data.csv. Trả về DataFrame thô (bao gồm cả aggregates)."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Không tìm thấy file GDP tại: {path}")

    usecols = COLUMNS_TO_KEEP["gdp_data.csv"]["keep"]
    df = pd.read_csv(path, usecols=usecols)
    print(f"[LOAD] GDP: {len(df):,} dòng, {len(df.columns)} cột")
    return df


def load_country_codes_raw(path: str) -> pd.DataFrame:
    """Nạp country_codes.csv. Trả về DataFrame thô."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Không tìm thấy file country_codes tại: {path}")

    usecols = COLUMNS_TO_KEEP["country_codes.csv"]["keep"]
    df = pd.read_csv(path, usecols=usecols)
    print(f"[LOAD] country_codes: {len(df):,} dòng, {len(df.columns)} cột")
    return df


def load_whs_raw(path: str) -> pd.DataFrame:
    """Nạp whs_years_updated.csv (World Happiness Report 2015-2024). Trả về DataFrame thô."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Không tìm thấy file WHS tại: {path}")

    df = pd.read_csv(path)
    print(f"[LOAD] WHS: {len(df):,} dòng, {len(df.columns)} cột")
    return df
