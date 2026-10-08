"""Sources and aggregation matching the nine charts in the latest 04_story.ipynb."""
import json
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'/'processed'
FEATURES=['danceability','energy','valence','acousticness','speechiness','instrumentalness','liveness','loudness','tempo']
GENRES=['pop','latin','k-pop','rap','dance pop','canadian pop','trap latino']

def records(df):
    return json.loads(df.to_json(orient='values',date_format='iso',double_precision=8))

def load_bundle():
    tracks=pd.read_csv(DATA/'tracks_dimension.csv').drop_duplicates('track_id').reset_index(drop=True)
    charts=pd.read_parquet(DATA/'charts_clean.parquet')
    # Artist rows are credits, not additional listening events.
    slots=charts.drop_duplicates(['chart_country','week','rank','track_id']).copy()
    slots['month']=pd.to_datetime(slots.week).dt.month
    slots['band']=pd.cut(slots['rank'],[0,10,50,100,200],labels=False)
    index={key:i for i,key in enumerate(tracks.track_id)}
    streams=slots.groupby(['track_id','year'],observed=True).streams.sum()
    by_track={}
    for (track,year),value in streams.items():
        by_track.setdefault(track,{})[str(int(year))]=int(value)
    track_cols=['track_id','track_name','artist_genre','artists_num','release_year']+FEATURES+['duration']
    track_rows=records(tracks[track_cols])
    for i,row in enumerate(track_rows): row.append(by_track.get(row[0],{}))
    global_slots=slots[(slots.chart_country=='Global') & slots.year.between(2017,2022)].copy()
    global_slots['i']=global_slots.track_id.map(index)
    grouped=global_slots.groupby(['i','year','month','band'],observed=True).agg(n=('streams','size'),streams=('streams','sum')).reset_index()
    credited=charts[(charts.chart_country=='Global') & charts.year.between(2017,2022)].drop_duplicates(['week','rank','track_id','artist_id']).copy()
    credited['month']=pd.to_datetime(credited.week).dt.month
    credited['band']=pd.cut(credited['rank'],[0,10,50,100,200],labels=False)
    credited['collab']=(credited.artists_num>1).astype(int)
    artist_mart=pd.read_parquet(DATA/'mart_artist_chart.parquet')
    allowed=artist_mart[artist_mart.artist_genre.isin(GENRES)].copy().drop_duplicates('artist_id')
    credited=credited[credited.artist_id.isin(allowed.artist_id)]
    artist_tracks=credited.groupby('artist_id').track_id.unique().apply(lambda a:[index[t] for t in a if t in index]).to_dict()
    artists={r.artist_id:[r.artist_name,r.artist_genre,artist_tracks.get(r.artist_id,[])] for r in allowed.itertuples()}
    credits=credited.groupby(['artist_id','year','month','band','collab'],observed=True).streams.sum().reset_index()
    countries=pd.read_parquet(DATA/'mart_country_year.parquet')
    country_cols=['country_code','chart_country','year','wb_region','yearly_streams','n_weeks']+[f+'_weighted' for f in FEATURES]+[f+'_mean' for f in FEATURES]
    countries=countries[(countries.chart_country!='Global') & countries.country_code.notna()]
    weekly=pd.read_parquet(DATA/'mart_audio_trend_weekly.parquet')
    weekly=weekly[weekly.chart_country=='Global'].copy().sort_values('week')
    weekly=weekly[pd.to_datetime(weekly.week).dt.year.between(2017,2022)]
    covid=pd.read_csv(DATA/'covid_weekly_clean.csv');covid['week']=pd.to_datetime(covid.week)
    weekly['week']=pd.to_datetime(weekly.week)
    weekly=weekly.merge(covid[covid.country=='Global'][['week','weekly_deaths']],on='week',how='left',validate='one_to_one')
    weekly.loc[~weekly.week.between('2020-01-01','2022-07-31'),'weekly_deaths']=float('nan')
    weekly['date']=weekly.week.dt.strftime('%Y-%m-%d')
    cols=['date','total_streams','track_count','duration_weighted']+[f+'_weighted' for f in FEATURES]+['weekly_deaths']
    return dict(features=FEATURES,genres=GENRES,tracks=track_rows,global_rows=records(grouped),artists=artists,credits=records(credits),countries=records(countries[country_cols]),weekly=records(weekly[cols]),
                source=dict(notebook='04_story.ipynb',chart_rows=len(charts),chart_slots=len(slots),covid_weeks=int(weekly.weekly_deaths.notna().sum()),countries_by_year=countries.groupby('year').size().to_dict()))
