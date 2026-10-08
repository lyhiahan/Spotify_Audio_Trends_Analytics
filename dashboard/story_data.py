"""Small, reusable data views for the three research dashboards.

The chart table is expanded by credited artists. Chart-level calculations therefore
deduplicate song–country–week–rank before aggregating streams or audio features.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"

AUDIO = [
    "danceability", "energy", "valence", "acousticness", "speechiness",
    "instrumentalness", "liveness", "loudness", "tempo",
]

FEATURE_LABEL = {
    "danceability": "Danceability", "energy": "Energy", "valence": "Valence",
    "acousticness": "Acousticness", "speechiness": "Speechiness",
    "instrumentalness": "Instrumentalness", "liveness": "Liveness",
    "loudness": "Loudness (dB)", "tempo": "Tempo (BPM)",
}

RANK_LABELS = ["Top 1–10", "Hạng 11–50", "Hạng 51–100", "Hạng 101–200"]
GENRE_LABELS = ["Pop", "Latin", "K-Pop", "Rap", "Dance Pop"]


def genre_group(value: object) -> str:
    if pd.isna(value):
        return "Khác"
    genre = str(value).casefold()
    if any(term in genre for term in ("k-pop", "korean pop", "kpop")):
        return "K-Pop"
    if any(term in genre for term in ("latin", "reggaeton", "salsa", "bachata", "brazilian funk", "urbano")):
        return "Latin"
    if any(term in genre for term in ("dance pop", "pop dance", "edm", "electropop", "electronic dance")):
        return "Dance Pop"
    if any(term in genre for term in ("rap", "hip hop", "hip-hop", "trap", "drill")):
        return "Rap"
    if "pop" in genre:
        return "Pop"
    return "Khác"


@st.cache_data(show_spinner=False)
def global_charts() -> pd.DataFrame:
    cols = [
        "track_id", "track_name", "artist_names", "artists_num", "artist_genre",
        "chart_country", "week", "year", "rank", "streams", "duration",
    ] + AUDIO
    frame = pd.read_parquet(
        DATA / "charts_clean.parquet", columns=cols,
        filters=[("chart_country", "==", "Global")],
    )
    frame = frame.drop_duplicates(["chart_country", "week", "rank", "track_id"]).copy()
    frame["week"] = pd.to_datetime(frame["week"]).astype("datetime64[ns]")
    frame["genre_group"] = frame["artist_genre"].map(genre_group)
    frame["rank_band"] = pd.cut(
        frame["rank"], bins=[0, 10, 50, 100, 200], labels=RANK_LABELS,
        include_lowest=True,
    )
    return frame


@st.cache_data(show_spinner=False)
def weekly_audio() -> pd.DataFrame:
    frame = pd.read_parquet(DATA / "mart_audio_trend_weekly.parquet")
    frame["week"] = pd.to_datetime(frame["week"]).astype("datetime64[ns]")
    return frame


@st.cache_data(show_spinner=False)
def artist_mart() -> pd.DataFrame:
    frame = pd.read_parquet(DATA / "mart_artist_chart.parquet")
    frame["genre_group"] = frame["artist_genre"].map(genre_group)
    return frame


@st.cache_data(show_spinner=False)
def country_year() -> pd.DataFrame:
    return pd.read_parquet(DATA / "mart_country_year.parquet")


@st.cache_data(show_spinner=False)
def covid_weekly() -> pd.DataFrame:
    frame = pd.read_csv(DATA / "covid_weekly_clean.csv")
    frame["week"] = pd.to_datetime(frame["week"]).astype("datetime64[ns]")
    frame["weekly_deaths"] = pd.to_numeric(frame["weekly_deaths"], errors="coerce")
    return frame


def rank_profile(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return original means and standardized group means for all nine features."""
    means = frame.groupby("rank_band", observed=False)[AUDIO].mean().reindex(RANK_LABELS)
    overall = frame[AUDIO].mean()
    std = frame[AUDIO].std(ddof=0).replace(0, np.nan)
    scores = (means - overall) / std
    return means, scores.fillna(0)


def track_summary(frame: pd.DataFrame) -> pd.DataFrame:
    """One row per song in the selected Global chart period."""
    best = frame.sort_values(["rank", "week"]).drop_duplicates("track_id")
    streams = frame.groupby("track_id", observed=True)["streams"].sum()
    tracks = best[["track_id", "track_name", "artists_num", "genre_group"] + AUDIO].copy()
    tracks["total_streams"] = tracks["track_id"].map(streams)
    tracks["collaboration"] = np.where(tracks["artists_num"].gt(1), "Hợp tác", "Đơn ca")
    return tracks


def aligned_covid(country: str) -> pd.DataFrame:
    """Match nearest reporting weeks within four days, without fabricating values."""
    audio = weekly_audio()
    audio = audio.loc[
        audio["chart_country"].eq(country)
        & audio["week"].between("2020-01-01", "2022-12-31")
    ].sort_values("week").copy()
    deaths = covid_weekly()
    deaths = deaths.loc[
        deaths["country"].eq(country)
        & deaths["week"].between("2020-01-01", "2022-12-31"),
        ["week", "weekly_deaths"],
    ].dropna().sort_values("week").drop_duplicates("week")
    if audio.empty or deaths.empty:
        return pd.DataFrame()
    joined = pd.merge_asof(
        audio, deaths, on="week", direction="nearest",
        tolerance=pd.Timedelta(days=4),
    ).dropna(subset=["weekly_deaths"])
    joined["deaths_ma4"] = joined["weekly_deaths"].rolling(4, min_periods=1).mean()
    for feature in AUDIO:
        joined[f"{feature}_ma4"] = joined[f"{feature}_weighted"].rolling(4, min_periods=1).mean()
    return joined
