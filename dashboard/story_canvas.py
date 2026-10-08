"""Build the project's template-based story with real, filterable mart data."""
import json
from pathlib import Path
import sys
from plotly.offline import get_plotlyjs
sys.path.insert(0, str(Path(__file__).resolve().parent))
import importlib
import story_data
FEATURES=story_data.FEATURES
REGION_SHORT={'East Asia & Pacific':'Đông Á & TBD','Europe & Central Asia':'Châu Âu & Trung Á','Latin America & Caribbean':'Mỹ Latinh','Middle East & North Africa':'Trung Đông & Bắc Phi','North America':'Bắc Mỹ','South Asia':'Nam Á','Sub-Saharan Africa':'Châu Phi hạ Sahara'}
LABELS={'hit_heatmap':'01 · Hồ sơ z-score theo thứ hạng','genre_box':'02 · Phân phối âm học theo thể loại','artist_tree':'03 · Thể loại → nghệ sĩ · Top 80','collab':'04 · Đơn ca và hợp tác','duration':'05 · Thời lượng: tuần và xu hướng 4 tuần','map':'06 · Bản đồ âm thanh toàn cầu','radar':'07 · Đối chiếu ADN âm nhạc · 6 trục','seasonal':'08 · Mùa vụ qua 12 tháng','covid':'09 · Âm thanh và tử vong COVID theo tuần'}

def workbook():
    specs=[
      ('hits','Công thức tạo hit & xu hướng','Điều gì đi cùng một bản hit streaming?', 'Thứ hạng → thể loại → nghệ sĩ → hợp tác → thời lượng. Khám phá sự khác biệt trong mẫu, không coi đó là công thức nhân quả.', ['hit_heatmap','genre_box','artist_tree','collab','duration'], 'Z-score là độ lệch trung bình nhóm so với toàn BXH, không phải hệ số tương quan. Stream bài hát bỏ dòng lặp nghệ sĩ; treemap ghi nhận lượt stream được ghi công cho nghệ sĩ.'),
      ('geography','Bản sắc địa lý & ADN âm nhạc','Cùng châu lục, âm nhạc có thể rất khác nhau', 'Bản đồ định vị khác biệt; radar đối chiếu hai quốc gia bằng cùng phương pháp tính. Mặc định Việt Nam và Nhật Bản, năm 2021.', ['map','radar'], 'Chọn thống nhất trung bình theo luồng nghe hoặc trung bình thường. Âm học không tự xác định thể loại, văn hóa hay tâm lý cá nhân.'),
      ('time','Mùa vụ & đại dịch COVID-19','Tách tính mùa vụ khỏi biến động trong đại dịch', 'Chọn tháng để drill-down những bài hát nổi bật và lọc chuỗi COVID. Chuyển giữa đủ chín đặc trưng để kiểm tra câu chuyện.', ['seasonal','covid'], 'COVID dùng các tuần ghép được trong 2020–07/2022. Hai trục riêng; không suy ra nguyên nhân, giãn cách hoặc tác dụng chữa lành từ đồng biến động.')]
    dashboards={};points=[]
    for key,title,caption,description,sheets,note in specs:
      dashboards[key]=dict(id=key,title=title,worksheets=sheets,description=description,note=note)
      points.append(dict(id='point_'+key,dashboard_id=key,caption=caption,annotation='',saved_state=dict(year=2021,fromyear=2020 if key=='hits' else 2017,toyear=2022,feature='acousticness' if key!='hits' else 'danceability',boxfeature='energy',region='Tất cả',country='VNM',compare='JPN',weight='weighted',genre='',artist='',band='',collab='',month='',weeks=[])))
    return dict(version=4,title='Spotify · Từ bản hit đến thế giới',worksheets=LABELS,dashboards=dashboards,story_points=points)

def data_bundle():
    return dict(workbook=workbook(),region_short=REGION_SHORT,**importlib.reload(story_data).load_bundle())

def canvas_html():
    encoded=json.dumps(data_bundle(),ensure_ascii=False,allow_nan=False).replace('</','<\\/')
    template=(Path(__file__).parent/'story_canvas.html').read_text(encoding='utf-8')
    script=(Path(__file__).parent/'story_interactions.js').read_text(encoding='utf-8')
    return template.replace('/*PLOTLY_LIBRARY*/',get_plotlyjs()).replace('/*WORKBOOK_DATA*/',encoded).replace('/*STORY_SCRIPT*/',script)
