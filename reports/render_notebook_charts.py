"""Export static HTML views of the nine Plotly figures saved in 04_story.ipynb.

The browser screenshots are produced separately, so this script keeps the
notebook's actual figure data and layout rather than reconstructing charts.
"""

import json
from pathlib import Path

import plotly.graph_objects as go


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "04_story.ipynb"
ASSETS = ROOT / "reports" / "chart_assets"
ASSETS.mkdir(parents=True, exist_ok=True)

notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
code_cells = [3, 6, 9, 12, 15, 18, 21, 24, 27]

for number, cell_index in enumerate(code_cells, 1):
    output = notebook["cells"][cell_index]["outputs"][0]
    figure = go.Figure(output["data"]["application/vnd.plotly.v1+json"])
    height = 680 if number in (3, 6, 7) else 610
    figure.update_layout(
        width=1120,
        height=height,
        autosize=False,
        font=dict(size=18),
        margin=dict(l=90, r=80, t=45, b=80),
        paper_bgcolor="white",
        plot_bgcolor="white",
        title_text="",
    )
    if number == 1:
        figure.update_xaxes(tickfont=dict(size=17))
        figure.update_yaxes(tickfont=dict(size=17))
    if number == 3:
        figure.update_traces(
            textfont_size=16,
            texttemplate="%{label}<br>%{value:.3s}",
        )
    if number == 4 and figure.layout.annotations:
        figure.layout.annotations[0].text = "<b>Cơ cấu bài hát trong dữ liệu</b>"
    if number == 7:
        figure.update_layout(polar=dict(angularaxis=dict(tickfont=dict(size=18))))
    if number == 5 and len(figure.layout.annotations) >= 2:
        figure.layout.annotations[0].text = "<b>2017: khoảng 218 giây</b>"
        figure.layout.annotations[1].text = (
            "<b>2020: khoảng 198 giây</b><br>Thấp hơn năm 2017 khoảng 20 giây"
        )
    # A printed page is not interactive; the caption supplies the title.
    figure.layout.updatemenus = ()

    html = figure.to_html(
        full_html=True,
        include_plotlyjs=True,
        config={"displayModeBar": False, "responsive": False},
        div_id=f"figure-{number}",
    )
    html = html.replace("<body>", "<body style='margin:0;background:white'>")
    target = ASSETS / f"chart_{number:02}.html"
    target.write_text(html, encoding="utf-8")
    print(target)
