import sys
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_parquet('data/processed/mart_country_year.parquet')
df_2022 = df[df['year'] == 2022].copy()
common_countries = set(df[df['year'] == 2021]['country_code']).intersection(set(df[df['year'] == 2022]['country_code']))
df_common = df[df['country_code'].isin(common_countries)].copy()

features = ['danceability', 'energy', 'valence', 'acousticness', 'speechiness', 'instrumentalness', 'liveness', 'loudness', 'tempo']
feat_cols = [f'{f}_weighted' for f in features]
feat_labels = ['Danceability', 'Energy', 'Valence', 'Acousticness', 'Speechiness', 'Instrumentalness', 'Liveness', 'Loudness (dB)', 'Tempo (BPM)']

# Test Fig 4
reg_means = df_2022.groupby('wb_region')['acousticness_weighted'].mean().to_dict()
df_2022['reg_mean'] = df_2022['wb_region'].map(reg_means)
df_2022['diff_from_mean'] = df_2022['acousticness_weighted'] - df_2022['reg_mean']
sorted_regions = sorted(reg_means.keys(), key=lambda r: reg_means[r], reverse=True)

fig4 = go.Figure()
for region in sorted_regions:
    sub = df_2022[df_2022['wb_region'] == region].copy()
    fig4.add_trace(go.Scatter(
        x=[region] * len(sub),
        y=sub['acousticness_weighted'],
        mode='markers',
        name=region,
        marker=dict(size=9, opacity=0.75),
        customdata=sub[['chart_country', 'country_code', 'acousticness_weighted', 'diff_from_mean', 'reg_mean']],
        hovertemplate='<b>%{customdata[0]}</b> (%{customdata[1]})<br>Acousticness: <b>%{customdata[2]:.3f}</b><br>TB Khu vực: %{customdata[4]:.3f}<br>Chênh lệch (Δ): %{customdata[3]:+.3f}<extra></extra>',
        showlegend=False
    ))
    fig4.add_trace(go.Scatter(
        x=[region],
        y=[reg_means[region]],
        mode='markers',
        marker=dict(symbol='diamond', size=14, color='black', line=dict(width=1.5, color='white')),
        name='Trung bình vùng',
        showlegend=(region == sorted_regions[0]),
        hovertemplate='<b>Trung bình %{x}:</b> %{y:.3f}<extra></extra>'
    ))

notable = ['IDN', 'VNM', 'JPN', 'ISL', 'FIN']
for code in notable:
    c_row = df_2022[df_2022['country_code'] == code]
    if not c_row.empty:
        r = c_row.iloc[0]
        fig4.add_annotation(
            x=r['wb_region'],
            y=r['acousticness_weighted'],
            text=f"<b>{r['chart_country']}</b> ({r['acousticness_weighted']:.3f})",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1.5,
            ax=45 if code in ['IDN', 'ISL'] else -45,
            ay=-25 if code in ['IDN', 'VNM', 'ISL'] else 25,
            bgcolor='rgba(255, 255, 255, 0.85)',
            bordercolor='black',
            borderwidth=1,
            font=dict(size=10)
        )

fig4.update_layout(
    title='Khác Biệt Nội Bộ Khu Vực: Phân Bố Acousticness Của Từng Quốc Gia (2022)',
    yaxis=dict(title='Acousticness (Chỉ số mộc)', range=[0.10, 0.56], zeroline=False),
    xaxis=dict(title='Khu vực World Bank'),
    height=550
)
print('Fig 4 created successfully!')

# Test Fig 5: 3x3 Dot Plot 2021 vs 2022
reg_yearly = df_common.groupby(['wb_region', 'year'])[feat_cols].mean().reset_index()
fig5 = make_subplots(
    rows=3, cols=3,
    subplot_titles=[f"<b>{lbl}</b>" for lbl in feat_labels],
    horizontal_spacing=0.10,
    vertical_spacing=0.14
)

regions = sorted(df_common['wb_region'].unique())

for idx, (feat, col, lbl) in enumerate(zip(features, feat_cols, feat_labels)):
    r = idx // 3 + 1
    c = idx % 3 + 1
    
    piv = reg_yearly.pivot(index='wb_region', columns='year', values=col).loc[regions]
    
    # Add connecting lines
    for reg in regions:
        val21 = piv.loc[reg, 2021]
        val22 = piv.loc[reg, 2022]
        fig5.add_trace(go.Scatter(
            x=[val21, val22],
            y=[reg, reg],
            mode='lines',
            line=dict(color='#BDC3C7', width=2),
            showlegend=False,
            hoverinfo='skip'
        ), row=r, col=c)
        
    # Points 2021
    fig5.add_trace(go.Scatter(
        x=piv[2021],
        y=regions,
        mode='markers',
        name='Năm 2021',
        marker=dict(size=8, color='#3498DB', symbol='circle'),
        showlegend=(idx == 0),
        hovertemplate='<b>%{y}</b> (2021)<br>' + lbl + ': %{x:.4f}<extra></extra>'
    ), row=r, col=c)
    
    # Points 2022
    fig5.add_trace(go.Scatter(
        x=piv[2022],
        y=regions,
        mode='markers',
        name='Năm 2022',
        marker=dict(size=9, color='#E74C3C', symbol='diamond'),
        showlegend=(idx == 0),
        hovertemplate='<b>%{y}</b> (2022)<br>' + lbl + ': %{x:.4f}<extra></extra>'
    ), row=r, col=c)
    
    # Format axes: only show yticklabels on col 1
    if c != 1:
        fig5.update_yaxes(showticklabels=False, row=r, col=c)
    else:
        fig5.update_yaxes(tickfont=dict(size=9), row=r, col=c)
        
    fig5.update_xaxes(tickfont=dict(size=9), row=r, col=c)

fig5.update_layout(
    title=dict(
        text='<b>Hồ Sơ Âm Thanh Thay Đổi Giữa Hai Năm (2021 vs 2022) Theo 7 Khu Vực</b>',
        x=0.01, y=0.99,
        font=dict(size=15)
    ),
    legend=dict(
        orientation='h',
        x=0.99, y=1.03,
        xanchor='right', yanchor='bottom',
        font=dict(size=11),
        bgcolor='rgba(255, 255, 255, 0.7)'
    ),
    height=880,
    margin=dict(l=150, r=30, t=80, b=50),
    template='plotly_white'
)
print('Fig 5 created successfully!')
