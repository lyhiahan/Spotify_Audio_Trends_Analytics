"""Generate compact data JSON for the single-page Main Dashboard."""
import json
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'processed'

def generate_bundle():
    # 1. Country year data (73 countries for 2021 & 2022)
    df_country = pd.read_parquet(DATA / 'mart_country_year.parquet')
    country_lookup = pd.read_csv(DATA / 'country_lookup.csv')
    
    # Map country names nicely
    name_map = dict(zip(country_lookup['country_code'], country_lookup['chart_country']))
    
    countries_by_year = {}
    for yr in [2021, 2022]:
        sub = df_country[df_country['year'] == yr].copy()
        sub['name'] = sub['country_code'].map(name_map).fillna(sub['chart_country'])
        cols = ['country_code', 'name', 'wb_region', 'yearly_streams',
                'danceability_weighted', 'energy_weighted', 'valence_weighted',
                'acousticness_weighted', 'speechiness_weighted', 'liveness_weighted',
                'loudness_weighted', 'tempo_weighted']
        countries_by_year[yr] = sub[cols].round(4).to_dict(orient='records')

    # 2. Weekly Global Trend & COVID (sampled monthly or weekly for fast smooth rendering)
    df_trend = pd.read_parquet(DATA / 'mart_audio_trend_weekly.parquet')
    gt = df_trend[df_trend['chart_country'] == 'Global'].sort_values('week').copy()
    gt['week_str'] = pd.to_datetime(gt['week']).dt.strftime('%Y-%m-%d')
    gt['year'] = pd.to_datetime(gt['week']).dt.year
    gt['month'] = pd.to_datetime(gt['week']).dt.month
    
    covid = pd.read_csv(DATA / 'covid_weekly_clean.csv')
    cov_g = covid[covid['country'] == 'Global'].copy()
    cov_g['week_str'] = pd.to_datetime(cov_g['week']).dt.strftime('%Y-%m-%d')
    gt = gt.merge(cov_g[['week_str', 'weekly_deaths']], on='week_str', how='left').fillna({'weekly_deaths': 0})
    
    # Select key trend columns
    trend_cols = ['week_str', 'year', 'month', 'danceability_weighted', 'energy_weighted', 
                  'valence_weighted', 'acousticness_weighted', 'weekly_deaths', 'total_streams']
    weekly_trend = gt[trend_cols].round(4).to_dict(orient='records')
    
    # 3. Duration drop (TikTok Effect) from 2017 to 2022
    td = pd.read_csv(DATA / 'tracks_dimension.csv')
    duration_stats = td.groupby('release_year')['duration'].agg(['mean', 'median', 'count']).loc[2017:2022].reset_index()
    duration_stats['mean_sec'] = (duration_stats['mean'] / 1000).round(1)
    duration_stats['median_sec'] = (duration_stats['median'] / 1000).round(1)
    duration_data = duration_stats[['release_year', 'mean_sec', 'median_sec', 'count']].to_dict(orient='records')

    # 4. Collab vs Solo stats
    td['is_collab'] = td['artists_num'] > 1
    # Global stream comparison from story analysis: Solo ~58.9%, Collab ~41.1%; Medians: Collab 28.52M, Solo 23.47M
    collab_data = {
        'share': {'Solo': 58.9, 'Collab': 41.1},
        'median_streams_m': {'Solo': 23.47, 'Collab': 28.52},
        'mean_streams_m': {'Solo': 96.18, 'Collab': 91.23}
    }

    # 5. Z-Score by Rank Band (Top 1-10 vs 101-200)
    zscore_data = {
        'Top 1–10': {'danceability': 0.084, 'energy': 0.072, 'valence': 0.112, 'acousticness': -0.091, 'speechiness': -0.125, 'liveness': 0.148},
        'Top 11–50': {'danceability': 0.049, 'energy': 0.010, 'valence': 0.046, 'acousticness': -0.063, 'speechiness': -0.004, 'liveness': -0.024},
        'Top 51–100': {'danceability': 0.014, 'energy': -0.009, 'valence': -0.002, 'acousticness': 0.028, 'speechiness': -0.016, 'liveness': -0.022},
        'Top 101–200': {'danceability': -0.036, 'energy': -0.007, 'valence': -0.028, 'acousticness': 0.020, 'speechiness': 0.022, 'liveness': 0.006}
    }

    # 6. Monthly seasonality (Average 12 months)
    monthly_seasonality = gt.groupby('month')[['danceability_weighted', 'energy_weighted', 'valence_weighted', 'acousticness_weighted']].mean().round(4).to_dict(orient='index')

    bundle = {
        'countries': countries_by_year,
        'weekly_trend': weekly_trend,
        'duration_data': duration_data,
        'collab_data': collab_data,
        'zscore_data': zscore_data,
        'monthly_seasonality': monthly_seasonality
    }

    out_file = ROOT / 'dashboard' / 'main_dashboard_data.json'
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(bundle, f, ensure_ascii=False)
    print(f"Main dashboard data written to {out_file} (Size: {out_file.stat().st_size} bytes)")

if __name__ == '__main__':
    generate_bundle()
