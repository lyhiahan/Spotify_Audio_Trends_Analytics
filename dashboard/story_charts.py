"""Plotly figures extracted from notebooks/04_story.ipynb; notebook stays unchanged."""

import os
from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
PROJECT_ROOT = str(Path(__file__).resolve().parents[1])

country_year_path = os.path.join(PROJECT_ROOT, 'data', 'processed', 'mart_country_year.parquet')
df_country_all = pd.read_parquet(country_year_path)
df_2022 = df_country_all[df_country_all['year'] == 2022].copy()
countries_2021 = set(df_country_all[df_country_all['year'] == 2021]['country_code'])
countries_2022 = set(df_country_all[df_country_all['year'] == 2022]['country_code'])
common_countries = countries_2021.intersection(countries_2022)
df_common = df_country_all[df_country_all['country_code'].isin(common_countries)].copy()
AUDIO_FEATURES_9 = ['danceability', 'energy', 'valence', 'acousticness', 'speechiness', 'instrumentalness', 'liveness', 'loudness', 'tempo']
FEATURE_COLS_WEIGHTED = [f'{f}_weighted' for f in AUDIO_FEATURES_9]
FEATURE_LABELS = ['Danceability', 'Energy', 'Valence', 'Acousticness', 'Speechiness', 'Instrumentalness', 'Liveness', 'Loudness (dB)', 'Tempo (BPM)']

audio_trend_path = os.path.join(PROJECT_ROOT, 'data', 'processed', 'mart_audio_trend_weekly.parquet')
covid_path = os.path.join(PROJECT_ROOT, 'data', 'processed', 'covid_weekly_clean.csv')
df_audio_all = pd.read_parquet(audio_trend_path)
df_covid_all = pd.read_csv(covid_path)
df_audio_global = df_audio_all[df_audio_all['chart_country'] == 'Global'].copy()
df_covid_global = df_covid_all[df_covid_all['country'] == 'Global'].copy()
ALL_9_FEATURES = ['danceability', 'energy', 'valence', 'acousticness', 'instrumentalness', 'speechiness', 'liveness', 'loudness', 'tempo']
for f in ALL_9_FEATURES:
    if f'{f}_weighted' in df_audio_global.columns:
        df_audio_global[f] = df_audio_global[f'{f}_weighted']
df_audio_global['week'] = pd.to_datetime(df_audio_global['week'])
df_covid_global['week'] = pd.to_datetime(df_covid_global['week'])
df_merged = pd.merge(df_audio_global, df_covid_global[['week', 'weekly_deaths', 'cumulative_deaths']], on='week', how='inner').sort_values('week')
df_merged['year'] = df_merged['week'].dt.year
df_merged['year_month'] = df_merged['week'].dt.to_period('M').astype(str)
SHORT_TITLES = ['Danceability', 'Energy', 'Valence', 'Acousticness', 'Instrumentalness', 'Speechiness', 'Liveness', 'Loudness (dB)', 'Tempo (BPM)']
FEATURE_META = {'danceability': ('Danceability', 'Độ dễ nhảy', '#1ABC9C', 'Tỉ lệ (0–1)'), 'energy': ('Energy', 'Cường độ năng lượng', '#E67E22', 'Tỉ lệ (0–1)'), 'valence': ('Valence', 'Cảm xúc tích cực', '#F1C40F', 'Tỉ lệ (0–1)'), 'acousticness': ('Acousticness', 'Độ mộc mạc', '#9B59B6', 'Tỉ lệ (0–1)'), 'instrumentalness': ('Instrumentalness', 'Độ khí nhạc', '#34495E', 'Tỉ lệ (0–1)'), 'speechiness': ('Speechiness', 'Độ dày lời ca', '#E74C3C', 'Tỉ lệ (0–1)'), 'liveness': ('Liveness', 'Độ sống động', '#2ECC71', 'Tỉ lệ (0–1)'), 'loudness': ('Loudness', 'Âm lượng trung bình', '#3498DB', 'dB'), 'tempo': ('Tempo', 'Nhịp độ bài hát', '#D35400', 'BPM')}

def plot_heatmap_regional_profiles(df_year):
    reg_raw = df_year.groupby('wb_region')[FEATURE_COLS_WEIGHTED].mean()
    reg_raw.columns = FEATURE_LABELS
    reg_norm = (reg_raw - reg_raw.min()) / (reg_raw.max() - reg_raw.min())
    custom_hover = []
    for r in reg_raw.index:
        row_vals = []
        for c in reg_raw.columns:
            val = reg_raw.loc[r, c]
            if 'Loudness' in c:
                row_vals.append(f'{val:.2f} dB')
            elif 'Tempo' in c:
                row_vals.append(f'{val:.1f} BPM')
            else:
                row_vals.append(f'{val:.4f}')
        custom_hover.append(row_vals)
    fig = go.Figure(data=go.Heatmap(z=reg_norm.values, x=FEATURE_LABELS, y=reg_norm.index.tolist(), colorscale='Viridis', customdata=custom_hover, text=np.round(reg_norm.values, 2), texttemplate='%{text:.2f}', textfont=dict(size=11), hovertemplate='<b>Khu vực:</b> %{y}<br><b>Đặc trưng:</b> %{x}<br><b>Điểm chuẩn hóa (0-1):</b> %{z:.2f}<br><b>Giá trị gốc:</b> %{customdata}<extra></extra>', colorbar=dict(title=dict(text='Điểm Chuẩn Hóa<br>(0: Thấp nhất, 1: Cao nhất)', font=dict(size=11)), thickness=15, len=0.85)))
    fig.update_layout(title=dict(text='<b>Hồ Sơ Âm Thanh 7 Khu Vực World Bank (Spotify Charts 2022)</b><br><sup>Chuẩn hóa Min-Max theo từng đặc trưng • Hover xem giá trị gốc</sup>', x=0.01, y=0.96, font=dict(size=15)), xaxis=dict(tickangle=-25, tickfont=dict(size=11)), yaxis=dict(tickfont=dict(size=11)), height=520, margin=dict(l=170, r=40, t=80, b=70), template='plotly_white')
    return fig

def plot_grouped_bar_key_features(df_year):
    features_4 = ['danceability', 'energy', 'valence', 'acousticness']
    cols_4 = [f'{f}_weighted' for f in features_4]
    labels_4 = ['Danceability', 'Energy', 'Valence', 'Acousticness']
    palette_4 = ['#1DB954', '#FF5722', '#FFB300', '#9C27B0']
    reg_summary = df_year.groupby('wb_region')[cols_4].mean()
    reg_summary.columns = labels_4
    reg_summary = reg_summary.sort_values('Danceability', ascending=False)
    fig = go.Figure()
    for feat, color in zip(labels_4, palette_4):
        fig.add_trace(go.Bar(x=reg_summary.index, y=reg_summary[feat], name=feat, marker_color=color, text=reg_summary[feat].round(2), texttemplate='%{text:.2f}', textposition='outside', hovertemplate='<b>Khu vực:</b> %{x}<br><b>Đặc trưng:</b> ' + feat + '<br><b>Giá trị:</b> %{y:.4f}<extra></extra>'))
    fig.update_layout(barmode='group', title=dict(text='<b>So Sánh 4 Đặc Trưng Phân Hóa Nổi Bật Giữa 7 Khu Vực (2022)</b><br><sup>Danceability • Energy • Valence • Acousticness (Giá trị trung bình luồng nghe)</sup>', x=0.01, y=0.96, font=dict(size=15)), xaxis=dict(tickangle=-15, tickfont=dict(size=11)), yaxis=dict(title='Giá trị trung bình (0 – 1)', range=[0, 0.84], tickfont=dict(size=10)), legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=0.99, font=dict(size=11)), height=540, margin=dict(l=60, r=30, t=90, b=80), template='plotly_white')
    return fig

def plot_choropleth_acousticness(df_year):
    df_sorted = df_year.sort_values('acousticness_weighted', ascending=False).copy()
    df_sorted['global_rank'] = range(1, len(df_sorted) + 1)
    fig = go.Figure(data=go.Choropleth(locations=df_sorted['country_code'], locationmode='ISO-3', z=df_sorted['acousticness_weighted'], customdata=df_sorted[['chart_country', 'wb_region', 'global_rank', 'acousticness_weighted']], colorscale='Tealgrn', colorbar=dict(title=dict(text='Acousticness<br>(Độ mộc mạc)', font=dict(size=11)), thickness=15, len=0.75), hovertemplate='<b>%{customdata[0]}</b> (%{locations})<br>' + 'Khu vực: %{customdata[1]}<br>' + 'Acousticness: <b>%{customdata[3]:.4f}</b><br>' + 'Thứ hạng toàn cầu: <b>#%{customdata[2]}/73</b><extra></extra>'))
    fig.update_layout(title=dict(text='<b>Bản Đồ Phân Bố Toàn Cầu: Chỉ Số Nhạc Mộc (Acousticness) Năm 2022</b><br><sup>Tâm điểm tập trung tại Đông Nam Á • Vùng trũng tại Bắc Âu & Đông Âu</sup>', x=0.01, y=0.96, font=dict(size=15)), geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth', coastlinecolor='#BDC3C7', countrycolor='#E0E0E0'), height=560, margin=dict(l=0, r=0, t=70, b=0))
    return fig

def plot_strip_intra_regional_diversity(df_year):
    reg_means = df_year.groupby('wb_region')['acousticness_weighted'].mean().to_dict()
    df_plot = df_year.copy()
    df_plot['reg_mean'] = df_plot['wb_region'].map(reg_means)
    df_plot['diff_from_mean'] = df_plot['acousticness_weighted'] - df_plot['reg_mean']
    sorted_regions = sorted(reg_means.keys(), key=lambda r: reg_means[r], reverse=True)
    fig = go.Figure()
    for region in sorted_regions:
        sub = df_plot[df_plot['wb_region'] == region]
        fig.add_trace(go.Scatter(x=[region] * len(sub), y=sub['acousticness_weighted'], mode='markers', name=region, marker=dict(size=9, opacity=0.75), customdata=sub[['chart_country', 'country_code', 'acousticness_weighted', 'diff_from_mean', 'reg_mean']], hovertemplate='<b>%{customdata[0]}</b> (%{customdata[1]})<br>' + 'Acousticness: <b>%{customdata[2]:.4f}</b><br>' + 'Trung bình vùng: %{customdata[4]:.4f}<br>' + 'Chênh lệch (Δ): <b>%{customdata[3]:+.4f}</b><extra></extra>', showlegend=False))
        fig.add_trace(go.Scatter(x=[region], y=[reg_means[region]], mode='markers', marker=dict(symbol='diamond', size=13, color='black', line=dict(width=1.5, color='white')), name='Trung bình vùng', showlegend=region == sorted_regions[0], hovertemplate='<b>Trung bình %{x}:</b> %{y:.4f}<extra></extra>'))
    annotations = [('IDN', 'Indonesia (0.513) - #1 Thế giới', 45, -25), ('VNM', 'Việt Nam (0.454) - #2 Thế giới', -50, -20), ('JPN', 'Nhật Bản (0.180) - Đối lập cực đoan', -50, 30), ('ISL', 'Iceland (0.349) - Ngoại lệ Châu Âu', 45, -25), ('FIN', 'Phần Lan (0.156) - Thấp nhất', 45, 25)]
    for code, text_label, ax_val, ay_val in annotations:
        c_row = df_plot[df_plot['country_code'] == code]
        if not c_row.empty:
            r = c_row.iloc[0]
            fig.add_annotation(x=r['wb_region'], y=r['acousticness_weighted'], text=f'<b>{text_label}</b>', showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=1.5, ax=ax_val, ay=ay_val, bgcolor='rgba(255, 255, 255, 0.9)', bordercolor='#34495E', borderwidth=1, font=dict(size=10))
    fig.update_layout(title=dict(text='<b>Độ Phân Hóa Nội Bộ Từng Khu Vực: Phân Bố Acousticness Của Từng Quốc Gia (2022)</b><br><sup>Mỗi chấm là một quốc gia • Hình thoi đen là trung bình vùng • Đối chiếu Indonesia, Việt Nam vs Nhật Bản</sup>', x=0.01, y=0.96, font=dict(size=15)), xaxis=dict(tickangle=-15, tickfont=dict(size=11), title='Khu vực World Bank'), yaxis=dict(title='Acousticness (Chỉ số mộc)', range=[0.11, 0.56], tickfont=dict(size=10)), legend=dict(x=0.99, y=1.02, xanchor='right', yanchor='bottom', orientation='h'), height=560, margin=dict(l=60, r=40, t=80, b=80), template='plotly_white')
    return fig

def plot_dotplot_regional_evolution(df_common_data):
    features_all = ['danceability', 'energy', 'valence', 'acousticness', 'speechiness', 'instrumentalness', 'liveness', 'loudness', 'tempo']
    cols_all = [f'{f}_weighted' for f in features_all]
    titles_all = ['Danceability', 'Energy', 'Valence', 'Acousticness', 'Speechiness', 'Instrumentalness', 'Liveness', 'Loudness (dB)', 'Tempo (BPM)']
    reg_yearly = df_common_data.groupby(['wb_region', 'year'])[cols_all].mean().reset_index()
    regions = sorted(df_common_data['wb_region'].unique())
    fig = make_subplots(rows=3, cols=3, subplot_titles=[f'<b>{t}</b>' for t in titles_all], horizontal_spacing=0.1, vertical_spacing=0.14)
    for idx, (f_col, t_label) in enumerate(zip(cols_all, titles_all)):
        r = idx // 3 + 1
        c = idx % 3 + 1
        piv = reg_yearly.pivot(index='wb_region', columns='year', values=f_col).loc[regions]
        for reg in regions:
            val_21 = piv.loc[reg, 2021]
            val_22 = piv.loc[reg, 2022]
            fig.add_trace(go.Scatter(x=[val_21, val_22], y=[reg, reg], mode='lines', line=dict(color='#BDC3C7', width=2), showlegend=False, hoverinfo='skip'), row=r, col=c)
        fig.add_trace(go.Scatter(x=piv[2021], y=regions, mode='markers', name='Năm 2021', marker=dict(size=8, color='#3498DB', symbol='circle'), showlegend=idx == 0, hovertemplate='<b>%{y}</b> (2021)<br>' + t_label + ': %{x:.4f}<extra></extra>'), row=r, col=c)
        fig.add_trace(go.Scatter(x=piv[2022], y=regions, mode='markers', name='Năm 2022', marker=dict(size=9, color='#E74C3C', symbol='diamond'), showlegend=idx == 0, hovertemplate='<b>%{y}</b> (2022)<br>' + t_label + ': %{x:.4f}<extra></extra>'), row=r, col=c)
        if c != 1:
            fig.update_yaxes(showticklabels=False, row=r, col=c)
        else:
            fig.update_yaxes(tickfont=dict(size=9), row=r, col=c)
        fig.update_xaxes(tickfont=dict(size=9), row=r, col=c)
    fig.update_layout(title=dict(text='<b>Biến Chuyển Hồ Sơ Âm Thanh 2021 – 2022 Theo 7 Khu Vực (Lưới 3×3 Thang Đo Riêng)</b><br><sup>Xét trên 68 quốc gia hiện diện ở cả hai năm • Đánh giá nét âm thanh ổn định và biến đổi</sup>', x=0.01, y=0.99, font=dict(size=15)), legend=dict(orientation='h', x=0.99, y=1.03, xanchor='right', yanchor='bottom', font=dict(size=11), bgcolor='rgba(255, 255, 255, 0.7)'), height=880, margin=dict(l=150, r=30, t=80, b=50), template='plotly_white')
    return fig

def plot_covid_audio_stacked(df, feature_key):
    name, desc, color, unit = FEATURE_META[feature_key]
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08, subplot_titles=['<b>Số Ca Tử Vong COVID-19 Toàn Cầu Theo Tuần (weekly_deaths)</b>', f'<b>Đặc Trưng Âm Thanh: {name} ({desc}) [{unit}]</b>'], row_heights=[0.42, 0.58])
    fig.add_trace(go.Bar(x=df['week'], y=df['weekly_deaths'], name='Tử vong COVID/tuần', marker=dict(color='#E74C3C', opacity=0.7), hovertemplate='<b>Tuần:</b> %{x|%d/%m/%Y}<br><b>Tử vong:</b> %{y:,.0f} ca<extra></extra>'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['week'], y=df[feature_key], name=name, mode='lines+markers', line=dict(color=color, width=2.5), marker=dict(size=4), hovertemplate='<b>Tuần:</b> %{x|%d/%m/%Y}<br><b>' + name + ':</b> %{y:.4f}<extra></extra>'), row=2, col=1)
    fig.update_xaxes(showgrid=True, gridcolor='#F0F0F0', rangebreaks=[], row=2, col=1)
    fig.update_yaxes(title_text='Ca tử vong', row=1, col=1)
    fig.update_yaxes(title_text=f'{name} ({unit})', row=2, col=1)
    fig.update_layout(title=dict(text=f'<b>Đối Chiếu Làn Sóng COVID-19 & Xu Hướng {name} (2020 – 2022)</b>', x=0.01, y=0.98, font=dict(size=15)), showlegend=False, height=520, margin=dict(l=60, r=30, t=70, b=40), template='plotly_white')
    return fig

def plot_scatter_covid_features(df):
    year_colors = {2020: '#3498DB', 2021: '#E67E22', 2022: '#2ECC71'}
    fig = make_subplots(rows=3, cols=3, subplot_titles=[f'<b>{name}</b>' for name in SHORT_TITLES], horizontal_spacing=0.07, vertical_spacing=0.1)
    for idx, (col, short_name) in enumerate(zip(ALL_9_FEATURES, SHORT_TITLES)):
        r = idx // 3 + 1
        c = idx % 3 + 1
        for yr in [2020, 2021, 2022]:
            sub = df[df['year'] == yr]
            fig.add_trace(go.Scatter(x=sub['weekly_deaths'], y=sub[col], mode='markers', name=f'Năm {yr}', marker=dict(color=year_colors[yr], size=6, opacity=0.7), showlegend=idx == 0, hovertemplate='<b>Tuần:</b> %{customdata|%d/%m/%Y}<br><b>Tử vong:</b> %{x:,.0f}<br><b>' + short_name + ':</b> %{y:.4f}<extra></extra>', customdata=sub['week']), row=r, col=c)
        fig.update_xaxes(title_text='Ca tử vong/tuần' if r == 3 else None, tickfont=dict(size=9), row=r, col=c)
        fig.update_yaxes(title_text=short_name if c == 1 else None, tickfont=dict(size=9), row=r, col=c)
    fig.update_layout(title=dict(text='<b>Phân Bố Đặc Trưng Âm Thanh Theo Mức Tử Vong COVID-19 Hàng Tuần</b>', x=0.01, y=0.99, font=dict(size=15)), legend=dict(orientation='h', x=0.99, y=1.03, xanchor='right', yanchor='bottom', font=dict(size=11), bgcolor='rgba(255, 255, 255, 0.7)'), height=820, margin=dict(l=60, r=30, t=70, b=50), template='plotly_white')
    return fig

def plot_heatmap_monthly_with_covid_bar(df):
    w_cols = ALL_9_FEATURES
    monthly = df.groupby('year_month').agg({**{c: 'mean' for c in w_cols}, 'weekly_deaths': 'sum'}).reset_index()
    monthly.rename(columns={'weekly_deaths': 'monthly_deaths'}, inplace=True)
    norm_features = pd.DataFrame()
    for col in w_cols:
        c_min = monthly[col].min()
        c_max = monthly[col].max()
        norm_features[col] = (monthly[col] - c_min) / (c_max - c_min)
    fig = make_subplots(rows=1, cols=2, column_widths=[0.68, 0.32], shared_yaxes=True, horizontal_spacing=0.03, subplot_titles=['<b>Hồ Sơ Âm Thanh Theo Tháng (Chuẩn Hóa Min-Max 0–1)</b>', '<b>Tổng Ca Tử Vong COVID-19 Trong Tháng</b>'])
    fig.add_trace(go.Heatmap(z=norm_features.values, x=SHORT_TITLES, y=monthly['year_month'], colorscale='YlGnBu', colorbar=dict(title=dict(text='Điểm<br>chuẩn hóa', font=dict(size=10)), x=0.64, thickness=12, len=0.8), hovertemplate='<b>Tháng:</b> %{y}<br><b>Đặc trưng:</b> %{x}<br><b>Chuẩn hóa:</b> %{z:.2f}<extra></extra>'), row=1, col=1)
    fig.add_trace(go.Bar(x=monthly['monthly_deaths'], y=monthly['year_month'], orientation='h', marker=dict(color='#E74C3C', opacity=0.8), name='Tử vong/tháng', hovertemplate='<b>Tháng:</b> %{y}<br><b>Tử vong:</b> %{x:,.0f} ca<extra></extra>'), row=1, col=2)
    fig.update_xaxes(tickangle=-30, tickfont=dict(size=10), row=1, col=1)
    fig.update_xaxes(title_text='Ca tử vong', tickfont=dict(size=9), row=1, col=2)
    fig.update_yaxes(title_text='Năm - Tháng', tickfont=dict(size=9), autorange='reversed', row=1, col=1)
    fig.update_layout(title=dict(text='<b>Đối Chiếu Hồ Sơ Âm Thanh Hàng Tháng Và Quy Mô Đại Dịch COVID-19</b>', x=0.01, y=0.98, font=dict(size=15)), showlegend=False, height=740, margin=dict(l=70, r=30, t=70, b=60), template='plotly_white')
    return fig

def plot_dotplot_death_groups(df):
    median_deaths = df['weekly_deaths'].median()
    df_temp = df.copy()
    df_temp['death_group'] = np.where(df_temp['weekly_deaths'] >= median_deaths, 'Tử vong cao (≥ Median)', 'Tử vong thấp (< Median)')
    group_summary = df_temp.groupby('death_group')[ALL_9_FEATURES].mean().reset_index()
    fig = make_subplots(rows=3, cols=3, subplot_titles=[f'<b>{name}</b>' for name in SHORT_TITLES], horizontal_spacing=0.08, vertical_spacing=0.12)
    for idx, (col, short_name) in enumerate(zip(ALL_9_FEATURES, SHORT_TITLES)):
        r = idx // 3 + 1
        c = idx % 3 + 1
        val_low = group_summary.loc[group_summary['death_group'] == 'Tử vong thấp (< Median)', col].values[0]
        val_high = group_summary.loc[group_summary['death_group'] == 'Tử vong cao (≥ Median)', col].values[0]
        fig.add_trace(go.Scatter(x=[val_low, val_high], y=['Hồ sơ', 'Hồ sơ'], mode='lines', line=dict(color='#BDC3C7', width=3), showlegend=False, hoverinfo='skip'), row=r, col=c)
        fig.add_trace(go.Scatter(x=[val_low], y=['Hồ sơ'], mode='markers', name='Tử vong thấp (< Median)', marker=dict(size=11, color='#2ECC71', symbol='circle'), showlegend=idx == 0, hovertemplate='<b>Tử vong thấp:</b> %{x:.4f}<extra></extra>'), row=r, col=c)
        fig.add_trace(go.Scatter(x=[val_high], y=['Hồ sơ'], mode='markers', name='Tử vong cao (≥ Median)', marker=dict(size=11, color='#E74C3C', symbol='diamond'), showlegend=idx == 0, hovertemplate='<b>Tử vong cao:</b> %{x:.4f}<extra></extra>'), row=r, col=c)
        fig.update_xaxes(tickfont=dict(size=9), row=r, col=c)
        fig.update_yaxes(showticklabels=False, row=r, col=c)
    fig.update_layout(title=dict(text=f'<b>So Sánh Hồ Sơ Âm Thanh: Tuần Tử Vong Cao vs Thấp (Ngưỡng Trung Vị = {median_deaths:,.0f} ca/tuần)</b>', x=0.01, y=0.99, font=dict(size=15)), legend=dict(orientation='h', x=0.99, y=1.03, xanchor='right', yanchor='bottom', font=dict(size=11), bgcolor='rgba(255, 255, 255, 0.7)'), height=780, margin=dict(l=40, r=30, t=70, b=50), template='plotly_white')
    return fig

def plot_dotplot_yearly_comparison(df):
    df_temp = df[df['year'].isin([2021, 2022])].copy()
    yearly_summary = df_temp.groupby('year')[ALL_9_FEATURES].mean().reset_index()
    fig = make_subplots(rows=3, cols=3, subplot_titles=[f'<b>{name}</b>' for name in SHORT_TITLES], horizontal_spacing=0.08, vertical_spacing=0.12)
    for idx, (col, short_name) in enumerate(zip(ALL_9_FEATURES, SHORT_TITLES)):
        r = idx // 3 + 1
        c = idx % 3 + 1
        val_2021 = yearly_summary.loc[yearly_summary['year'] == 2021, col].values[0]
        val_2022 = yearly_summary.loc[yearly_summary['year'] == 2022, col].values[0]
        fig.add_trace(go.Scatter(x=[val_2021, val_2022], y=['Toàn cầu', 'Toàn cầu'], mode='lines', line=dict(color='#BDC3C7', width=3), showlegend=False, hoverinfo='skip'), row=r, col=c)
        fig.add_trace(go.Scatter(x=[val_2021], y=['Toàn cầu'], mode='markers', name='Năm 2021', marker=dict(size=11, color='#E67E22', symbol='circle'), showlegend=idx == 0, hovertemplate='<b>2021:</b> %{x:.4f}<extra></extra>'), row=r, col=c)
        fig.add_trace(go.Scatter(x=[val_2022], y=['Toàn cầu'], mode='markers', name='Năm 2022', marker=dict(size=11, color='#2ECC71', symbol='diamond'), showlegend=idx == 0, hovertemplate='<b>2022:</b> %{x:.4f}<extra></extra>'), row=r, col=c)
        fig.update_xaxes(tickfont=dict(size=9), row=r, col=c)
        fig.update_yaxes(showticklabels=False, row=r, col=c)
    fig.update_layout(title=dict(text='<b>Chuyển Dịch Hồ Sơ Âm Thanh Toàn Cầu: Năm 2021 vs Năm 2022</b>', x=0.01, y=0.99, font=dict(size=15)), legend=dict(orientation='h', x=0.99, y=1.03, xanchor='right', yanchor='bottom', font=dict(size=11), bgcolor='rgba(255, 255, 255, 0.7)'), height=780, margin=dict(l=40, r=30, t=70, b=50), template='plotly_white')
    return fig
