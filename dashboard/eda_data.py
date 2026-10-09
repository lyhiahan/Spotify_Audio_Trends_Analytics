"""Summaries for the opening story, using the populations in 02_eda."""
import numpy as np
import pandas as pd

AUDIO = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness',
         'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_min']


def opening_summary(tracks, charts):
    """Keep the track population separate from the Global training cohort."""
    assert tracks.track_id.is_unique
    audio = tracks.copy()
    audio['duration_min'] = audio.duration / 60000
    distributions = {}
    for feature in AUDIO:
        values = audio[feature].dropna().to_numpy(dtype=float)
        assert np.isfinite(values).all()
        counts, edges = np.histogram(values, bins=100 if feature == 'duration_min' else 40)
        distributions[feature] = dict(
            count=len(values), mean=float(values.mean()), median=float(np.median(values)),
            q1=float(np.quantile(values, .25)), q3=float(np.quantile(values, .75)),
            p99=float(np.quantile(values, .99)), minimum=float(values.min()), maximum=float(values.max()),
            counts=counts.tolist(), edges=edges.tolist())

    # The future calendar and purge match 02_eda and 03_model.
    columns = ['track_id', 'week', 'rank']
    global_rows = charts.loc[charts.chart_country.eq('Global'), columns].copy()
    global_rows['week'] = pd.to_datetime(global_rows.week)
    global_rows = global_rows.drop_duplicates(['track_id', 'week']).sort_values(['week', 'track_id'])
    calendar = pd.date_range(global_rows.week.min(), global_rows.week.max(), freq='7D')
    complete = (global_rows.loc[global_rows['rank'].between(1, 50)]
                .groupby('week')['rank'].nunique().reindex(calendar, fill_value=0).eq(50))
    first = global_rows.drop_duplicates('track_id').reset_index(drop=True)
    lookup = global_rows.set_index(['track_id', 'week'])['rank']
    valid, hit = np.ones(len(first), dtype=bool), np.zeros(len(first), dtype=bool)
    for offset in range(1, 9):
        future = first[['track_id', 'week']].copy()
        future['week'] += pd.Timedelta(weeks=offset)
        valid &= complete.reindex(future.week).fillna(False).to_numpy(dtype=bool)
        ranks = lookup.reindex(pd.MultiIndex.from_frame(future)).to_numpy()
        hit |= (ranks >= 1) & (ranks <= 50)
    first['hit'] = hit
    first['eligible'] = valid & first.week.ne(global_rows.week.min())
    eligible = first.loc[first.eligible]
    boundary = eligible.loc[eligible.week.ge(eligible.week.quantile(.60)), 'week'].min()
    train = first.loc[first.eligible & (first.week + pd.Timedelta(weeks=8)).lt(boundary)].copy()
    tiers = []
    for low, high in [(1, 50), (51, 100), (101, 150), (151, 200)]:
        group = train.loc[train['rank'].between(low, high)]
        tiers.append(dict(label=f'{low}–{high}', count=len(group), positives=int(group.hit.sum()),
                          rate=float(group.hit.mean()) if len(group) else None))
    assert sum(row['count'] for row in tiers) == len(train)
    return dict(
        features=AUDIO, distributions=distributions,
        correlations=audio[AUDIO].corr(method='spearman').to_numpy().tolist(),
        tracks=len(tracks), markets=int(charts.chart_country.nunique()),
        weeks=int(global_rows.week.nunique()), first_week=str(global_rows.week.min().date()),
        last_week=str(global_rows.week.max().date()),
        train=dict(count=len(train), positives=int(train.hit.sum()), rate=float(train.hit.mean()),
                   first_week=str(train.week.min().date()), last_week=str(train.week.max().date()),
                   validation_start=str(boundary.date()), tiers=tiers))


def notebook_figures():
    """Embed the saved Matplotlib/Seaborn outputs, without redrawing them."""
    import base64
    import hashlib
    import json
    import struct
    from pathlib import Path

    notebook_path = Path(__file__).resolve().parents[1] / 'notebooks' / '02_eda.ipynb'
    notebook = json.loads(notebook_path.read_text(encoding='utf-8'))
    specs = {
        'eda_static_distribution': ('feat_names =', 'Phân phối năm đặc trưng âm thanh',
            'Mỗi bài một lần. Đường nét đứt: trung bình; đường liền: trung vị. Giữ toàn bộ đuôi thời lượng như notebook. Bấm “Xem lớn” để đọc chi tiết.'),
        'eda_static_correlation': ('sns.heatmap(', 'Tương quan giữa các đặc trưng âm thanh',
            'Spearman trên 10 đặc trưng liên tục. Energy và Loudness có thông tin chồng lấn; tương quan không xác nhận nguyên nhân.'),
        'eda_static_labels': ('bar_colors =', 'Phân phối nhãn Top 50 trên Train',
            'Hai mẫu: toàn bộ Train và nhóm khởi đầu hạng 51–200. Y=1 khi đạt Top 50 trong tám tuần sau t0; không tính tuần đầu.'),
        'eda_static_trend': ("palette = {'danceability_weighted'", 'Xu hướng âm thanh trên Global Top 200',
            'Trung bình theo stream, làm mịn bốn tuần. Vùng tô đánh dấu tháng 12; dữ liệu năm 2022 chỉ đến tháng 7.'),
        'eda_static_covid': ('fig, (ax1, ax2) = plt.subplots(2, 1', 'Đối chiếu tử vong COVID-19 và âm thanh',
            'Hai tầng đối chiếu số ca tử vong COVID-19 hàng tuần và các đặc trưng âm học trên Global Top 200 giai đoạn 2020–2022.')
    }
    figures = {}
    for key, (signature, title, caption) in specs.items():
        matches = [(i, cell) for i, cell in enumerate(notebook['cells'])
                   if cell['cell_type'] == 'code' and signature in ''.join(cell['source'])]
        if len(matches) != 1:
            raise ValueError(f'Không xác định được ô biểu đồ EDA: {key}')
        index, cell = matches[0]
        images = [output['data']['image/png'] for output in cell.get('outputs', [])
                  if 'image/png' in output.get('data', {})]
        if len(images) != 1:
            raise ValueError(f'Cần chạy và lưu ô {index + 1} trong 02_eda.ipynb')
        encoded = ''.join(images[0]) if isinstance(images[0], list) else images[0]
        raw = base64.b64decode(encoded)
        assert raw[:8] == b'\x89PNG\r\n\x1a\n'
        width, height = struct.unpack('>II', raw[16:24])
        figures[key] = dict(title=title, caption=caption, cell=index + 1,
                            source='notebooks/02_eda.ipynb', width=width, height=height,
                            sha256=hashlib.sha256(raw).hexdigest(),
                            image='data:image/png;base64,' + encoded)
    return figures
