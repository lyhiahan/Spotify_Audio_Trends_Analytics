"""Shared descriptive analysis; never writes model or data artifacts."""
import numpy as np
import pandas as pd

FEATURES = ['danceability', 'energy', 'valence', 'acousticness', 'speechiness',
            'instrumentalness', 'liveness', 'loudness', 'tempo']


def global_slots(charts):
    """One listening event per Global chart slot, not per artist credit."""
    g = charts.loc[charts.chart_country.eq('Global')].copy()
    g['week'] = pd.to_datetime(g.week)
    return g.drop_duplicates(['week', 'rank', 'track_id'])


def artist_history(charts):
    g = charts.loc[charts.chart_country.eq('Global')].dropna(
        subset=['artist_id', 'track_id', 'week']).copy()
    g['week'] = pd.to_datetime(g.week)
    g = g.drop_duplicates(['artist_id', 'track_id', 'week'])
    if g.empty:
        raise ValueError('Không có dữ liệu BXH Global để tính lịch sử nghệ sĩ.')
    first = g.groupby(['artist_id', 'track_id'], observed=True).week.min().reset_index()
    new = first.groupby(['artist_id', 'week'], observed=True).size()
    weekly = g.groupby(['artist_id', 'week'], observed=True).agg(
        S=('streams', 'sum'), R=('rank', 'min'))
    weekly['N'] = new.reindex(weekly.index).fillna(0)
    weekly['W'] = 1
    grid = pd.MultiIndex.from_product(
        [g.artist_id.unique(), sorted(g.week.unique())], names=['artist_id', 'week'])
    h = weekly.reindex(grid)
    h[['S', 'N', 'W']] = h[['S', 'N', 'W']].fillna(0)
    h['R'] = h.R.fillna(201)
    h[['S', 'N', 'W']] = h.groupby(level=0)[['S', 'N', 'W']].cumsum()
    h['R'] = h.groupby(level=0).R.cummin()
    h = h.groupby(level=0).shift().reset_index()
    h[['S', 'N', 'W']] = h[['S', 'N', 'W']].fillna(0)
    h['R'] = h.R.fillna(201)
    active = h.W.gt(0)
    logs = np.log1p(h.S).where(active)
    low = logs.groupby(h.week).transform('min')
    high = logs.groupby(h.week).transform('max')
    caps = {c: h[c].where(active).groupby(h.week).transform(
        lambda v: np.ceil(v.quantile(.95))).clip(lower=1) for c in ['N', 'W']}
    h['stream_points'] = 40 * ((logs-low)/(high-low).replace(0, np.nan)).fillna(0).clip(0, 1)
    h['track_points'] = 25 * (h.N/caps['N']).fillna(0).clip(0, 1)
    h['week_points'] = 20 * (h.W/caps['W']).fillna(0).clip(0, 1)
    h['rank_points'] = np.where(h.R.between(1, 200), 15*(200-h.R)/199, 0)
    points = ['stream_points', 'track_points', 'week_points', 'rank_points']
    h['artist_popularity_prior'] = h[points].sum(axis=1).round(1)
    return h


def track_analysis(charts, tracks, warmup_weeks=52):
    """Descriptive sample, not an ML dataset: prior history and 8 calendar weeks.

    Window includes entry week through entry+7 weeks; missing chart appearances
    contribute no observed chart streams, not an estimate of all Spotify plays.
    Warmup reduces left censoring; it does not reconstruct pre-dataset careers.
    """
    h = artist_history(charts)
    slots = global_slots(charts)
    entries = slots.groupby('track_id', observed=True).week.min().rename('first_global_week')
    slots = slots.merge(entries, on='track_id', validate='many_to_one')
    observed = slots[slots.week.lt(slots.first_global_week + pd.Timedelta(weeks=8))]
    streams = observed.groupby('track_id', observed=True).streams.sum().rename('streams_first_8w')
    points = ['stream_points', 'track_points', 'week_points', 'rank_points']
    t = tracks.drop_duplicates('track_id').merge(entries, on='track_id', validate='one_to_one')
    t = t.merge(streams, on='track_id', validate='one_to_one').merge(
        h[['artist_id', 'week', *points, 'artist_popularity_prior']],
        left_on=['artist_id', 'first_global_week'], right_on=['artist_id', 'week'],
        how='left', validate='many_to_one').drop(columns='week')
    t = t[t.first_global_week.ge(slots.week.min() + pd.Timedelta(weeks=warmup_weeks))
          & (t.first_global_week + pd.Timedelta(weeks=7)).le(slots.week.max())]
    return t.dropna(subset=FEATURES + ['artist_popularity_prior', 'streams_first_8w']).reset_index(drop=True)
