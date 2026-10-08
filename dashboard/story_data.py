"""Small, reusable data views for the three research dashboards.

The chart table is expanded by credited artists. Chart-level calculations therefore
deduplicate song–country–week–rank before aggregating streams or audio features.
"""

import json
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
FEATURES = AUDIO

FEATURE_LABEL = {
    "danceability": "Danceability", "energy": "Energy", "valence": "Valence",
    "acousticness": "Acousticness", "speechiness": "Speechiness",
    "instrumentalness": "Instrumentalness", "liveness": "Liveness",
    "loudness": "Loudness (dB)", "tempo": "Tempo (BPM)",
}

RANK_LABELS = ["Top 1–10", "Hạng 11–50", "Hạng 51–100", "Hạng 101–200"]
GENRE_LABELS = ["Pop", "Latin", "K-Pop", "Rap", "Dance Pop"]
GENRES = ["pop", "latin", "k-pop", "rap", "dance pop", "canadian pop", "trap latino"]


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


def records(df: pd.DataFrame):
    return json.loads(df.to_json(orient="values", date_format="iso", double_precision=8))


def load_bundle():
    tracks = pd.read_csv(DATA / "tracks_dimension.csv").drop_duplicates("track_id").reset_index(drop=True)
    charts = pd.read_parquet(DATA / "charts_clean.parquet")
    # Artist rows are credits, not additional listening events.
    slots = charts.drop_duplicates(["chart_country", "week", "rank", "track_id"]).copy()
    slots["month"] = pd.to_datetime(slots.week).dt.month
    slots["band"] = pd.cut(slots["rank"], [0, 10, 50, 100, 200], labels=False)
    index = {key: i for i, key in enumerate(tracks.track_id)}
    streams = slots.groupby(["track_id", "year"], observed=True).streams.sum()
    by_track = {}
    for (track, year), value in streams.items():
        by_track.setdefault(track, {})[str(int(year))] = int(value)
    track_cols = ["track_id", "track_name", "artist_genre", "artists_num", "release_year"] + FEATURES + ["duration"]
    track_rows = records(tracks[track_cols])
    for i, row in enumerate(track_rows):
        row.append(by_track.get(row[0], {}))
    global_slots = slots[(slots.chart_country == "Global") & slots.year.between(2017, 2022)].copy()
    global_slots["i"] = global_slots.track_id.map(index)
    grouped = global_slots.groupby(["i", "year", "month", "band"], observed=True).agg(n=("streams", "size"), streams=("streams", "sum")).reset_index()
    credited = charts[(charts.chart_country == "Global") & charts.year.between(2017, 2022)].drop_duplicates(["week", "rank", "track_id", "artist_id"]).copy()
    credited["month"] = pd.to_datetime(credited.week).dt.month
    credited["band"] = pd.cut(credited["rank"], [0, 10, 50, 100, 200], labels=False)
    credited["collab"] = (credited.artists_num > 1).astype(int)
    artist_mart_df = pd.read_parquet(DATA / "mart_artist_chart.parquet")
    allowed = artist_mart_df[artist_mart_df.artist_genre.isin(GENRES)].copy().drop_duplicates("artist_id")
    credited = credited[credited.artist_id.isin(allowed.artist_id)]
    artist_tracks = credited.groupby("artist_id").track_id.unique().apply(lambda a: [index[t] for t in a if t in index]).to_dict()
    artists = {r.artist_id: [r.artist_name, r.artist_genre, artist_tracks.get(r.artist_id, [])] for r in allowed.itertuples()}
    credits = credited.groupby(["artist_id", "year", "month", "band", "collab"], observed=True).streams.sum().reset_index()
    countries = pd.read_parquet(DATA / "mart_country_year.parquet")
    country_cols = ["country_code", "chart_country", "year", "wb_region", "yearly_streams", "n_weeks"] + [f + "_weighted" for f in FEATURES] + [f + "_mean" for f in FEATURES]
    countries = countries[(countries.chart_country != "Global") & countries.country_code.notna()]
    weekly = pd.read_parquet(DATA / "mart_audio_trend_weekly.parquet")
    weekly = weekly[weekly.chart_country == "Global"].copy().sort_values("week")
    weekly = weekly[pd.to_datetime(weekly.week).dt.year.between(2017, 2022)]
    covid = pd.read_csv(DATA / "covid_weekly_clean.csv")
    covid["week"] = pd.to_datetime(covid.week)
    weekly["week"] = pd.to_datetime(weekly.week)
    weekly = weekly.merge(covid[covid.country == "Global"][["week", "weekly_deaths"]], on="week", how="left", validate="one_to_one")
    weekly.loc[~weekly.week.between("2020-01-01", "2022-07-31"), "weekly_deaths"] = float("nan")
    weekly["date"] = weekly.week.dt.strftime("%Y-%m-%d")
    cols = ["date", "total_streams", "track_count", "duration_weighted"] + [f + "_weighted" for f in FEATURES] + ["weekly_deaths"]
    return dict(
        features=FEATURES, genres=GENRES, tracks=track_rows, global_rows=records(grouped),
        artists=artists, credits=records(credits), countries=records(countries[country_cols]),
        weekly=records(weekly[cols]),
        source=dict(notebook="04_story.ipynb", chart_rows=len(charts), chart_slots=len(slots),
                    covid_weeks=int(weekly.weekly_deaths.notna().sum()),
                    countries_by_year=countries.groupby("year").size().to_dict())
    )
