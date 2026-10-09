"""Build the project's template-based story with real, filterable mart data."""
import json
from pathlib import Path
import sys
from plotly.offline import get_plotlyjs
sys.path.insert(0, str(Path(__file__).resolve().parent))
import importlib
import story_data
FEATURES = story_data.FEATURES
REGION_SHORT = {
    'East Asia & Pacific': 'Đông Á & TBD',
    'Europe & Central Asia': 'Châu Âu & Trung Á',
    'Latin America & Caribbean': 'Mỹ Latinh',
    'Middle East & North Africa': 'Trung Đông & Bắc Phi',
    'North America': 'Bắc Mỹ',
    'South Asia': 'Nam Á',
    'Sub-Saharan Africa': 'Châu Phi hạ Sahara'
}
LABELS = {
    'eda_distribution': 'Phân phối đặc trưng âm thanh · mỗi bài một lần',
    'eda_correlation': 'Tương quan Spearman · 10 đặc trưng',
    'eda_rank': 'Hạng tuần đầu và khả năng đạt Top 50 · chỉ Train',
    'hit_heatmap': 'Đặc trưng âm thanh giữa các nhóm thứ hạng',
    'genre_box': 'So sánh đặc trưng âm thanh giữa các thể loại',
    'artist_tree': 'Lượt nghe ghi nhận cho 80 nghệ sĩ dẫn đầu',
    'collab': 'Đơn ca và hợp tác: số bài và lượt nghe',
    'duration': 'Thời lượng bài hát thay đổi theo thời gian',
    'map': 'Đặc trưng âm thanh trên BXH các quốc gia',
    'radar': 'So sánh đặc trưng âm thanh giữa hai quốc gia',
    'seasonal': 'Âm thanh thay đổi theo tháng trong năm',
    'covid': 'Đặc trưng âm thanh và tử vong COVID-19 theo tuần',
    'correlation': 'Mối liên hệ giữa âm thanh, nghệ sĩ và lượt nghe',
    'collab_box': 'Phân bố lượt nghe 8 tuần: đơn ca và hợp tác',
    'decision_boundary': 'Không gian quyết định 2D & Ranh giới phân loại',
    'confusion_heatmap': 'Ma trận nhầm lẫn tương tác (Confusion Matrix)',
    'tradeoff_curve': 'Đánh đổi Precision – Recall theo ngưỡng τ',
    'model_coefficients': 'Hệ số hồi quy (Odds Ratio) của 12 biến'
}

def workbook():
    specs = [
        (
            'overview', 'Cái nhìn về dữ liệu',
            'Cái nhìn về dữ liệu',
            'Bốn hình tĩnh từ EDA: phân phối âm thanh, tương quan, nhãn Train và xu hướng theo tuần.',
            ['eda_static_distribution', 'eda_static_correlation', 'eda_static_labels', 'eda_static_trend'],
            'Audio: mỗi track_id một lần trên toàn bộ mẫu chart. Nhãn: chỉ Train Global; Top 50 ở t0+7 đến t0+56 ngày, đủ tám tuần quan sát. Không suy ra quan hệ nhân quả.'
        ),
        (
            'hits',
            'Hồ sơ âm thanh',
            'Bài hát thịnh hành có hồ sơ âm thanh như thế nào?',
            'Đối chiếu 9 đặc trưng theo tầng thứ hạng, rồi khám phá sự khác biệt giữa các thể loại.',
            ['hit_heatmap', 'genre_box'],
            'Z-score đo độ lệch trung bình nhóm so với toàn BXH. Stream bài hát không đếm lặp nghệ sĩ; Treemap tính lượt stream được ghi công.'
        ),
        (
            'artists', 'Nghệ sĩ & hợp tác',
            'Tên tuổi nghệ sĩ và hợp tác liên hệ với thành tích ra sao?',
            'So sánh tên tuổi trước khi vào BXH với stream 8 tuần đầu; đối chiếu Solo và Collab trên cùng mẫu bài hát.',
            ['correlation', 'artist_tree', 'collab'],
            'Spearman trên mỗi bài một dòng. Điểm nghệ sĩ chỉ dùng lịch sử trước tuần vào Global. Stream 8 tuần đầu là stream ghi nhận trên BXH, không phải toàn bộ Spotify. Treemap dùng stream ghi công toàn giai đoạn chọn.'
        ),
        (
            'geography',
            'Bản sắc địa lý và ADN âm nhạc',
            'Hồ sơ âm thanh khác nhau thế nào giữa các quốc gia?',
            'Đối chiếu hồ sơ âm thanh của các BXH quốc gia trên cùng năm và cùng phương pháp tổng hợp.',
            ['map', 'radar'],
            'Bản đồ và Radar đồng bộ phương pháp tính: theo luồng nghe hoặc trung bình thường. Năm phân tích chuẩn: 2021.'
        ),
        (
            'time',
            'Chu kỳ thời gian và đại dịch',
            'Xu hướng dài hạn, mùa vụ và biến động trong đại dịch',
            'Phân biệt thay đổi thời lượng, chu kỳ tháng và đồng biến động với tử vong COVID-19.',
            ['duration', 'seasonal', 'covid'],
            'Phân biệt xu hướng thời lượng, mùa vụ và đồng biến động COVID. Số tử vong không trực tiếp đo phong tỏa hay tâm lý người nghe.'
        ),
        (
            'forecast',
            'Mô hình & Ngưỡng dự báo',
            'Làm sao chuyển điểm số xác suất thành quyết định hành động?',
            'Khám phá không gian quyết định 2D, điều chỉnh ngưỡng τ và quan sát biến động tức thời trên ma trận nhầm lẫn cùng đường trade-off.',
            ['decision_boundary', 'confusion_heatmap', 'tradeoff_curve', 'model_coefficients'],
            'Hồi quy Logistic 12 biến tuần đầu. Ngưỡng tối ưu F1 = 0.79 chọn trên Validation; đánh giá độc lập trên Test (2021–2022). Lưu ý cảnh báo nhóm hạng 51–200 và hiệu chuẩn xác suất.'
        )
    ]
    dashboards = {}
    points = []
    for key, title, caption, description, sheets, note in specs:
        dashboards[key] = dict(id=key, title=title, worksheets=sheets, description=description, note=note)
        points.append(dict(
            id='point_' + key,
            dashboard_id=key,
            caption=caption,
            annotation='',
            saved_state=dict(
                year=2021,
                fromyear=2020 if key == 'hits' else 2017,
                toyear=2022,
                feature='energy' if key == 'overview' else 'danceability' if key in ['hits', 'artists'] else 'acousticness',
                boxfeature='energy',
                region='Tất cả',
                country='VNM',
                compare='JPN',
                weight='weighted',
                genre='',
                artist='',
                band='',
                collab='',
                month='',
                weeks=[],
                threshold=0.79,
                split='test',
                boundary_y='rank_first_week'
            )
        ))
    return dict(version=6, title='Spotify Audio Trends & Analytics', worksheets=LABELS, dashboards=dashboards, story_points=points)

def data_bundle():
    from eda_data import notebook_figures
    figures = notebook_figures()
    book = workbook()
    book['worksheets'].update({key: value['title'] for key, value in figures.items()})
    return dict(workbook=book, region_short=REGION_SHORT, eda_figures=figures, **importlib.reload(story_data).load_bundle())

def canvas_html():
    encoded = json.dumps(data_bundle(), ensure_ascii=False, allow_nan=False).replace('</', '<\\/')
    template = (Path(__file__).parent / 'story_canvas.html').read_text(encoding='utf-8')
    script = (Path(__file__).parent / 'story_interactions.js').read_text(encoding='utf-8')
    return template.replace('/*PLOTLY_LIBRARY*/', get_plotlyjs()).replace('/*WORKBOOK_DATA*/', encoded).replace('/*STORY_SCRIPT*/', script)
