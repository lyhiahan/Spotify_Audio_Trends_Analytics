"""Build report figures from existing processed data without changing datasets."""
from pathlib import Path
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import spearmanr
from statsmodels.tools import add_constant
from statsmodels.stats.outliers_influence import variance_inflation_factor

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
DATA = ROOT / 'data' / 'processed'
sns.set_theme(style='whitegrid', font='DejaVu Sans', font_scale=1.05)
plt.rcParams['axes.unicode_minus'] = False
m = pd.read_parquet(DATA / 'ml_tracks.parquet')
w = pd.read_parquet(DATA / 'mart_audio_trend_weekly.parquet')
a = pd.read_parquet(DATA / 'mart_country_year.parquet')

fig, axes = plt.subplots(1, 2, figsize=(12, 4.3))
counts = m.is_hit.value_counts().reindex([0, 1])
axes[0].bar(['Non-Hit', 'Hit'], counts, color=['#466c89', '#bd7048'])
for i, value in enumerate(counts):
    axes[0].text(i, value + 500, f'{value:,}\n{value / len(m):.2%}', ha='center')
axes[0].set_ylim(0, 41000)
axes[0].set_ylabel('Số bài hát')
axes[0].set_title('Nhãn nghiên cứu ở cấp bài hát')
axes[1].hist(m.pop_score, bins=40, color='#466c89', edgecolor='white')
axes[1].axvline(50, color='#bd7048', linestyle='--', label='Hit: ≥ 50')
axes[1].axvline(70, color='#7c508b', linestyle='--', label='Mega Hit: ≥ 70')
axes[1].set(xlabel='pop_score', ylabel='Số bài hát', title='Phân phối điểm tổng hợp')
axes[1].legend()
fig.tight_layout()
fig.savefig(OUT / '01_labels_score.png', dpi=170)
plt.close(fig)

configs = [('loudness', 'Loudness (dB)'), ('energy', 'Energy (0–1)'),
           ('speechiness', 'Speechiness (0–1)'), ('valence', 'Valence (0–1)'),
           ('duration', 'Duration (phút)')]
fig, axes = plt.subplots(2, 3, figsize=(14, 8))
for ax, (col, label) in zip(axes.flat, configs):
    values = m[col] / 60000 if col == 'duration' else m[col]
    ax.hist(values, bins=55, color='#466c89', edgecolor='white')
    ax.axvline(values.mean(), color='#bd7048', linestyle='--', label='Trung bình')
    ax.axvline(values.median(), color='#52774c', label='Trung vị')
    ax.set(xlabel=label, ylabel='Số bài hát', title=label)
    ax.legend(fontsize=9)
last = axes.flat[5]
dur = m.duration / 60000
last.hist(dur[dur <= 10], bins=55, color='#466c89', edgecolor='white')
last.set(xlabel='Duration (phút)', ylabel='Số bài hát', xlim=(0, 10),
         title='Phóng to 0–10 phút; 29 bài ngoài miền')
fig.suptitle('Audio features của 39.190 bài độc nhất', fontsize=15)
fig.tight_layout()
fig.savefig(OUT / '02_audio_distributions.png', dpi=170)
plt.close(fig)

cols = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness',
        'instrumentalness', 'liveness', 'valence', 'tempo', 'duration']
corr = m[cols].corr(method='spearman')
fig, ax = plt.subplots(figsize=(10.5, 8.5))
sns.heatmap(corr, mask=np.triu(np.ones_like(corr, dtype=bool)), annot=True,
            fmt='.2f', cmap='RdBu_r', center=0, vmin=-1, vmax=1,
            square=True, ax=ax, cbar_kws={'label': 'Spearman ρ'})
ax.set_title('Tương quan ở cấp bài hát (n = 39.190)', pad=18)
fig.tight_layout()
fig.savefig(OUT / '03_spearman.png', dpi=170)
plt.close(fig)

g = w[w.chart_country == 'Global'].sort_values('week').copy()
fig, ax = plt.subplots(figsize=(13, 5.5))
colors = ['#466c89', '#bd7048', '#52774c', '#7c508b']
for feature, color in zip(['danceability', 'energy', 'valence', 'acousticness'], colors):
    ax.plot(g.week, g[feature + '_weighted'].rolling(4, min_periods=1).mean(),
            label=feature, color=color, linewidth=1.8)
for year in range(2017, 2022):
    ax.axvspan(pd.Timestamp(year, 12, 1), pd.Timestamp(year, 12, 31),
               color='#bd7048', alpha=.12)
ax.set(xlabel='Tuần chart', ylabel='Chỉ số âm thanh (0–1)',
       title='Global: chỉ số trọng số stream, trung bình trượt 4 tuần')
ax.legend(ncol=4, loc='lower left')
fig.tight_layout()
fig.savefig(OUT / '04_global_trends.png', dpi=170)
plt.close(fig)

x = add_constant(m[cols].astype(float))
extra = {
    'vif_10_continuous_with_intercept': {
        col: float(variance_inflation_factor(x.values, i))
        for i, col in enumerate(x.columns) if col != 'const'
    },
    'global_week_counts_by_year': g.groupby(g.week.dt.year).size().to_dict(),
    'happiness_valence_spearman': {},
}
for year, sub in a.groupby('year'):
    rho, pvalue = spearmanr(sub.happiness_score, sub.valence_weighted)
    extra['happiness_valence_spearman'][str(year)] = {
        'n': len(sub), 'rho': float(rho), 'pvalue': float(pvalue)}
(OUT / 'additional_statistics.json').write_text(
    json.dumps(extra, indent=2, ensure_ascii=False), encoding='utf-8')
print('Generated 4 figures and additional_statistics.json')
