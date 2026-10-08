"""Three compact, linked Streamlit dashboards for Gia Hân's data story."""

from html import escape

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from dashboard.story_data import (
    AUDIO, FEATURE_LABEL, GENRE_LABELS, RANK_LABELS, aligned_covid,
    artist_mart, country_year, global_charts, rank_profile, track_summary,
    weekly_audio,
)


STORY_PAGES = (
    "Dashboard 1 · Công thức Hit",
    "Dashboard 2 · ADN âm nhạc",
    "Dashboard 3 · Mùa vụ & COVID",
)

PLUM = "#7A3E65"
INK = "#241F21"
MUTED = "#746C70"
TEAL = "#168A76"
AMBER = "#D7894D"
PAPER = "#F7F4EF"
PLOT_CONFIG = {"displayModeBar": False, "scrollZoom": False}


def _css() -> None:
    st.markdown(
        """
        <style>
        .block-container {padding-top: .35rem !important; padding-bottom: .25rem !important;}
        div[data-testid="stVerticalBlock"] {gap: .32rem !important;}
        div[data-testid="stHorizontalBlock"] {gap: .55rem !important;}
        div[data-testid="stSelectbox"], div[data-testid="stSlider"] {margin-bottom: 0 !important;}
        .story-head {display:flex;align-items:flex-end;justify-content:space-between;gap:12px;margin:0 0 5px;}
        .story-kicker {font:700 10px/1.1 Inter,sans-serif;color:#7A3E65;letter-spacing:.13em;text-transform:uppercase;margin-bottom:3px;}
        .story-title {font:800 clamp(18px,2vw,25px)/1.1 Montserrat,Inter,sans-serif;color:#241F21;letter-spacing:-.03em;margin:0;}
        .story-sub {font:400 11px/1.3 Inter,sans-serif;color:#746C70;margin:3px 0 0;}
        .story-chip {white-space:nowrap;background:#EEE9E1;border:1px solid #D8D0C7;border-radius:999px;padding:6px 10px;color:#594C53;font:700 10px Inter,sans-serif;}
        div[data-testid="stVerticalBlockBorderWrapper"] {padding:6px 8px !important;margin-bottom:0 !important;border-radius:10px !important;}
        .story-card {background:#FFF;border:1px solid #D8D0C7;border-radius:11px;padding:7px 10px 0;min-width:0;}
        .story-card-title {display:flex;justify-content:space-between;align-items:center;color:#241F21;font:700 12px Inter,sans-serif;margin:0 0 1px;}
        .story-card-note {color:#8B8186;font:400 10px/1.15 Inter,sans-serif;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
        .story-insights {display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:7px;margin:4px 0 0;}
        .story-insight {background:#FFF;border-left:3px solid #7A3E65;border-radius:8px;padding:7px 9px;min-height:58px;box-shadow:0 1px 3px rgba(36,31,33,.06);}
        .story-insight:nth-child(2){border-left-color:#168A76}.story-insight:nth-child(3){border-left-color:#D7894D}.story-insight:nth-child(4){border-left-color:#746C70}
        .story-insight strong {display:block;color:#7A3E65;font:800 10px Inter,sans-serif;text-transform:uppercase;letter-spacing:.05em;margin-bottom:3px;}
        .story-insight span {display:block;color:#453E42;font:500 10px/1.25 Inter,sans-serif;}
        @media(max-width:1000px){.story-insights{grid-template-columns:repeat(2,minmax(0,1fr));}.story-chip{display:none}}
        </style>
        """,
        unsafe_allow_html=True,
    )


def _head(kicker: str, title: str, subtitle: str, chip: str) -> None:
    st.markdown(
        '<div class="story-head"><div>'
        f'<div class="story-kicker">{escape(kicker)}</div>'
        f'<h1 class="story-title">{escape(title)}</h1>'
        f'<p class="story-sub">{escape(subtitle)}</p></div>'
        f'<div class="story-chip">{escape(chip)}</div></div>',
        unsafe_allow_html=True,
    )


def _card(title: str, note: str = "") -> None:
    st.markdown(
        '<div class="story-card-title">'
        f'<span>{escape(title)}</span><span class="story-card-note">{escape(note)}</span>'
        '</div>', unsafe_allow_html=True,
    )


def _insights(phenomenon: str, mechanism: str, conclusion: str, limit: str) -> None:
    parts = [
        ("Hiện tượng", phenomenon), ("Cơ chế có thể", mechanism),
        ("Kết luận", conclusion), ("Giới hạn", limit),
    ]
    content = "".join(
        f'<div class="story-insight"><strong>{escape(name)}</strong>'
        f'<span>{escape(body)}</span></div>' for name, body in parts
    )
    st.markdown(f'<div class="story-insights">{content}</div>', unsafe_allow_html=True)


def _style(fig: go.Figure, height: int, **kwargs) -> go.Figure:
    fig.update_layout(
        height=height, margin=dict(l=22, r=12, t=8, b=24),
        font=dict(family="Inter, sans-serif", size=10, color=INK),
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        hoverlabel=dict(bgcolor="#FFFFFF", font=dict(color=INK)),
        showlegend=kwargs.get("showlegend", False),
    )
    return fig


def _points(event) -> list:
    try:
        return list(event["selection"]["points"])
    except (KeyError, TypeError, AttributeError):
        return []


def _check_selection(state_key: str, value: str | None) -> bool:
    """Consume each chart selection once; old selections cannot undo a filter reset."""
    if not value or value == st.session_state.get(f"{state_key}_last"):
        return False
    st.session_state[f"{state_key}_last"] = value
    st.session_state[state_key] = value
    return True


def _bump_chart_key(name: str) -> None:
    st.session_state[name] = st.session_state.get(name, 0) + 1


def _empty(message: str) -> None:
    st.info(message)


def _rank_heatmap(frame: pd.DataFrame) -> go.Figure:
    means, z = rank_profile(frame)
    labels = ["Dance", "Energy", "Valence", "Acoustic", "Speech", "Instrumental", "Liveness", "Loudness", "Tempo"]
    max_abs = max(.20, float(np.nanmax(np.abs(z.to_numpy()))))
    fig = go.Figure(go.Heatmap(
        z=z.to_numpy().T, x=RANK_LABELS, y=labels,
        customdata=means.to_numpy().T,
        colorscale=[[0, "#326B98"], [.5, "#F7F4EF"], [1, PLUM]],
        zmin=-max_abs, zmax=max_abs, zmid=0,
        texttemplate="%{z:+.2f}", textfont=dict(size=10),
        hovertemplate="<b>%{y} · %{x}</b><br>Độ lệch: %{z:+.2f} SD<br>Trung bình gốc: %{customdata:.3f}<extra></extra>",
        colorbar=dict(title="SD", thickness=9, len=.84, tickfont=dict(size=9)),
    ))
    fig.update_yaxes(autorange="reversed", tickfont=dict(size=9), showgrid=False)
    fig.update_xaxes(tickfont=dict(size=9), showgrid=False)
    fig = _style(fig, 196)
    fig.update_layout(margin=dict(l=74, r=9, t=5, b=30))
    return fig


def _genre_box(tracks: pd.DataFrame, feature: str) -> go.Figure:
    view = tracks[tracks["genre_group"].isin(GENRE_LABELS)].copy()
    fig = px.box(
        view, x="genre_group", y=feature, color="genre_group",
        category_orders={"genre_group": GENRE_LABELS},
        color_discrete_sequence=[PLUM, AMBER, TEAL, "#596AA7", "#9C7B99"],
        points=False,
    )
    fig.update_traces(hovertemplate="%{x}<br>Giá trị: %{y:.3f}<extra></extra>")
    fig.update_xaxes(title=None, tickangle=-20, tickfont=dict(size=9), showgrid=False)
    fig.update_yaxes(title=None, gridcolor="#EEE9E1", zeroline=False)
    fig = _style(fig, 196)
    fig.update_layout(margin=dict(l=34, r=7, t=4, b=48))
    return fig


def _artist_treemap(genre: str) -> go.Figure:
    top = artist_mart().query("global_streams > 0").nlargest(80, "global_streams").copy()
    if genre != "Tất cả":
        top = top[top["genre_group"].eq(genre)]
    if top.empty:
        return _style(go.Figure(), 184)
    top["streams_m"] = top["global_streams"] / 1_000_000
    fig = px.treemap(
        top, path=["genre_group", "artist_name"], values="global_streams",
        color="genre_group", color_discrete_sequence=[PLUM, TEAL, AMBER, "#596AA7", "#9C7B99", "#A9A09A"],
        custom_data=["streams_m", "n_chart_tracks", "artist_genre"],
    )
    fig.update_traces(
        root_color="#EEE9E1", textfont=dict(size=10),
        hovertemplate="<b>%{label}</b><br>Streams ghi nhận: %{customdata[0]:,.1f} triệu<br>Số ca khúc: %{customdata[1]}<br>Thể loại gốc: %{customdata[2]}<extra></extra>",
    )
    fig = _style(fig, 184)
    fig.update_layout(margin=dict(l=4, r=4, t=2, b=3))
    return fig


def _collab_chart(tracks: pd.DataFrame) -> tuple[go.Figure, pd.DataFrame]:
    summary = tracks.groupby("collaboration", observed=True).agg(
        songs=("track_id", "nunique"), mean_streams=("total_streams", "mean"),
    ).reindex(["Đơn ca", "Hợp tác"]).fillna(0)
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "domain"}, {"type": "xy"}]], column_widths=[.47, .53], horizontal_spacing=.04)
    fig.add_trace(go.Pie(
        labels=summary.index, values=summary["songs"], hole=.64,
        marker=dict(colors=[PLUM, TEAL]), textinfo="percent", textfont=dict(size=10),
        hovertemplate="%{label}: %{value:,.0f} bài (%{percent})<extra></extra>",
        showlegend=False,
    ), row=1, col=1)
    fig.add_trace(go.Bar(
        x=summary["mean_streams"] / 1_000_000, y=summary.index,
        orientation="h", marker_color=[PLUM, TEAL],
        text=(summary["mean_streams"] / 1_000_000).round(1),
        texttemplate="%{text:.0f}M", textposition="outside", cliponaxis=False,
        hovertemplate="%{y}: %{x:,.1f} triệu streams/bài<extra></extra>",
    ), row=1, col=2)
    fig.update_xaxes(title=None, showgrid=True, gridcolor="#EEE9E1", row=1, col=2)
    fig.update_yaxes(title=None, autorange="reversed", tickfont=dict(size=9), row=1, col=2)
    fig = _style(fig, 184)
    fig.update_layout(margin=dict(l=0, r=17, t=4, b=17))
    return fig, summary


def _duration_chart(years: tuple[int, int]) -> tuple[go.Figure, pd.DataFrame]:
    frame = weekly_audio()
    frame = frame[frame["chart_country"].eq("Global") & frame["week"].dt.year.between(*years)].copy()
    frame["month"] = frame["week"].dt.to_period("M").dt.to_timestamp()
    month = frame.groupby("month", as_index=False)[["duration_mean", "duration_weighted"]].mean()
    fig = go.Figure()
    for col, name, color in (
        ("duration_mean", "Không trọng số", TEAL),
        ("duration_weighted", "Theo streams", PLUM),
    ):
        fig.add_trace(go.Scatter(
            x=month["month"], y=month[col] / 1000, mode="lines",
            name=name, line=dict(color=color, width=2.2),
            hovertemplate="%{x|%m/%Y}: %{y:.1f} giây<extra>" + name + "</extra>",
        ))
    fig.update_xaxes(title=None, tickformat="%Y", dtick="M12", showgrid=False)
    fig.update_yaxes(title="Giây", gridcolor="#EEE9E1", zeroline=False)
    fig = _style(fig, 184, showlegend=True)
    fig.update_layout(legend=dict(orientation="h", x=.02, y=1.13, font=dict(size=9)), margin=dict(l=40, r=8, t=22, b=19))
    return fig, frame


def dashboard_hit() -> None:
    charts = global_charts()
    _head("01 / Thành công trên BXH", "Công thức tạo Hit & xu hướng âm nhạc", "Đặc trưng âm thanh · thể loại · nghệ sĩ · hợp tác · thời lượng", "Global Spotify Chart")
    a, b, c, d = st.columns([1.15, 1.05, 1, 1], gap="small")
    with a:
        years = st.slider("Giai đoạn", 2017, 2022, (2017, 2022), key="story_hit_year")
    with b:
        genre = st.selectbox("Nhóm thể loại", ["Tất cả"] + GENRE_LABELS, key="story_hit_genre")
    with c:
        band = st.selectbox("Tầng thứ hạng", ["Tất cả"] + RANK_LABELS, key="story_hit_band")
    with d:
        feature = st.selectbox("Chỉ số boxplot", ["energy", "danceability", "valence", "tempo"],
                               format_func=lambda item: FEATURE_LABEL[item], key="story_hit_box_feature")

    frame = charts[charts["year"].between(*years)].copy()
    if genre != "Tất cả":
        frame = frame[frame["genre_group"].eq(genre)]
    if frame.empty:
        return _empty("Không có bài hát phù hợp với bộ lọc này.")
    base_frame = frame
    collab_filter = st.session_state.get("story_hit_collab", "Tất cả")
    if collab_filter == "Đơn ca":
        frame = frame[frame["artists_num"].le(1)]
    elif collab_filter == "Hợp tác":
        frame = frame[frame["artists_num"].gt(1)]
    if frame.empty:
        return _empty("Không có bài hát phù hợp với lựa chọn đơn ca/hợp tác.")
    # The heatmap keeps all rank tiers visible; a selected tier filters the other song views.
    song_frame = frame if band == "Tất cả" else frame[frame["rank_band"].eq(band)]
    songs = track_summary(song_frame) if not song_frame.empty else pd.DataFrame()
    base_song_frame = base_frame if band == "Tất cả" else base_frame[base_frame["rank_band"].eq(band)]
    base_songs = track_summary(base_song_frame) if not base_song_frame.empty else pd.DataFrame()

    upper = st.columns([1.2, 1], gap="small")
    with upper[0]:
        with st.container(border=True):
            _card("01 · Chín đặc trưng qua bốn tầng thứ hạng", "z-score; hover: trung bình gốc")
            st.plotly_chart(_rank_heatmap(frame), width="stretch", config=PLOT_CONFIG)
    with upper[1]:
        with st.container(border=True):
            _card("02 · Phân phối theo thể loại", "mỗi bài hát một quan sát")
            if not songs.empty and songs["genre_group"].isin(GENRE_LABELS).any():
                st.plotly_chart(_genre_box(songs, feature), width="stretch", config=PLOT_CONFIG)
            else:
                _empty("Không có bài hát thuộc năm thể loại đã chọn.")

    lower = st.columns([1.03, .83, 1.10], gap="small")
    with lower[0]:
        with st.container(border=True):
            _card("03 · 80 nghệ sĩ dẫn đầu", "mart_artist_chart · toàn kỳ")
            st.plotly_chart(_artist_treemap(genre), width="stretch", config=PLOT_CONFIG)
    with lower[1]:
        with st.container(border=True):
            _card("04 · Đơn ca và hợp tác", "tỷ trọng bài · stream trung bình")
            if not base_songs.empty:
                collab_fig, collab = _collab_chart(base_songs)
                # Selecting a bar filters the other chart views on the next rerun.
                collab_key = f"story_collab_event_{st.session_state.get('story_collab_nonce', 0)}"
                event = st.plotly_chart(collab_fig, width="stretch", config=PLOT_CONFIG,
                                        key=collab_key, on_select="rerun", selection_mode="points")
                points = _points(event)
                chosen = str(points[0].get("y", "")) if points else None
                if _check_selection("story_hit_collab", chosen):
                    st.rerun()
            else:
                collab = pd.DataFrame()
                _empty("Không có dữ liệu hợp tác ở tầng này.")
    with lower[2]:
        with st.container(border=True):
            _card("05 · Thời lượng bài hát theo tháng", "Global toàn thể · chỉ lọc theo năm")
            duration_fig, duration_frame = _duration_chart(years)
            st.plotly_chart(duration_fig, width="stretch", config=PLOT_CONFIG)

    # Chart selection is the cross-filter; keep a visible way to return to the full cohort.
    if collab_filter in ("Đơn ca", "Hợp tác"):
        if st.button(f"Đang chọn {collab_filter} · Bỏ chọn", key="story_hit_clear", type="tertiary"):
            st.session_state["story_hit_collab"] = "Tất cả"
            _bump_chart_key("story_collab_nonce")
            st.rerun()

    means, z = rank_profile(frame)
    dance_diff = float(means.loc[RANK_LABELS[0], "danceability"] - means.loc[RANK_LABELS[-1], "danceability"])
    loud_z = float(z.loc[RANK_LABELS[0], "loudness"])
    if np.isfinite(dance_diff) and np.isfinite(loud_z):
        rank_text = (
            f"Top 10 cao hơn hạng 101–200 {dance_diff:+.3f} Danceability; "
            f"Loudness của Top 10 ở mức {loud_z:+.2f} SD so với toàn BXH."
        )
    else:
        rank_text = "Một số tầng thứ hạng không có bài hát dưới bộ lọc này; chưa thể so sánh Top 10 với hạng 101–200."
    duration_frame = duration_frame.assign(year=duration_frame["week"].dt.year)
    yearly = duration_frame.groupby("year")["duration_weighted"].mean() / 1000
    first, last = yearly.iloc[0], yearly.iloc[-1]
    if not collab.empty and (collab["songs"] > 0).all():
        solo_m = collab.loc["Đơn ca", "mean_streams"] / 1e6
        joint_m = collab.loc["Hợp tác", "mean_streams"] / 1e6
        collab_text = f"Trong nhóm đang lọc, hợp tác đạt {joint_m:.1f}M stream/bài; đơn ca {solo_m:.1f}M."
    else:
        collab_text = "Không đủ hai nhóm đơn ca và hợp tác để so sánh."
    _insights(
        rank_text,
        "Thể loại, tệp người hâm mộ, playlist và chiến dịch phát hành có thể cùng tác động; dữ liệu chưa tách riêng các cơ chế này.",
        f"{collab_text} Thời lượng theo streams đi từ {first:.0f}s ({yearly.index[0]}) đến {last:.0f}s ({yearly.index[-1]}).",
        "Streams tính theo các tuần lọt BXH; treemap là streams ghi nhận cho nghệ sĩ toàn kỳ. Kết quả mô tả, chưa chứng minh công thức tạo hit hay tác động của TikTok.",
    )


def _map_figure(frame: pd.DataFrame, feature: str) -> go.Figure:
    col = f"{feature}_weighted"
    fig = px.choropleth(
        frame, locations="country_code", locationmode="ISO-3", color=col,
        hover_name="chart_country", custom_data=["wb_region", "happiness_score", "chart_country"],
        color_continuous_scale=["#EEE3E9", "#B87499", PLUM],
        labels={col: FEATURE_LABEL[feature]}, projection="natural earth",
    )
    fig.update_traces(
        marker_line_color="#FFFFFF", marker_line_width=.6,
        hovertemplate="<b>%{customdata[2]}</b><br>Khu vực: %{customdata[0]}<br>Happiness: %{customdata[1]:.2f}<br>"
                      + FEATURE_LABEL[feature] + ": %{z:.3f}<extra></extra>",
    )
    fig.update_geos(showframe=False, showcoastlines=False, showland=True, landcolor="#EEE9E1", bgcolor="#FFFFFF")
    fig = _style(fig, 370)
    fig.update_layout(coloraxis_colorbar=dict(title="Giá trị", thickness=9, len=.70), margin=dict(l=1, r=1, t=2, b=0))
    return fig


def _radar_figure(full: pd.DataFrame, first: str, second: str) -> go.Figure:
    features = ["danceability", "energy", "valence", "acousticness", "loudness", "tempo"]
    labels = ["Dance", "Energy", "Valence", "Acoustic", "Loudness", "Tempo"]
    percentile = full[["chart_country"] + [f"{f}_weighted" for f in features]].copy()
    for feature in features:
        col = f"{feature}_weighted"
        percentile[col] = percentile[col].rank(pct=True) * 100
    fig = go.Figure()
    for country, color in ((first, PLUM), (second, TEAL)):
        rank_row = percentile[percentile["chart_country"].eq(country)]
        raw_row = full[full["chart_country"].eq(country)]
        if rank_row.empty or raw_row.empty:
            continue
        vals = [float(rank_row.iloc[0][f"{f}_weighted"]) for f in features]
        raw = [float(raw_row.iloc[0][f"{f}_weighted"]) for f in features]
        fig.add_trace(go.Scatterpolar(
            r=vals + [vals[0]], theta=labels + [labels[0]],
            customdata=raw + [raw[0]], name=country, mode="lines+markers",
            line=dict(color=color, width=2.2), marker=dict(size=5),
            fill="toself", fillcolor="rgba(122,62,101,.12)" if color == PLUM else "rgba(22,138,118,.12)",
            hovertemplate="<b>" + escape(country) + " · %{theta}</b><br>Phân vị: %{r:.0f}/100<br>Giá trị gốc: %{customdata:.3f}<extra></extra>",
        ))
    fig.update_layout(
        polar=dict(radialaxis=dict(range=[0, 100], tickvals=[25, 50, 75, 100], tickfont=dict(size=8), gridcolor="#E5DFD9"),
                   angularaxis=dict(tickfont=dict(size=10))),
    )
    fig = _style(fig, 370, showlegend=True)
    fig.update_layout(legend=dict(orientation="h", y=-.03, x=.5, xanchor="center", font=dict(size=10)),
                      margin=dict(l=35, r=35, t=15, b=30))
    return fig


def dashboard_geography() -> None:
    all_countries = country_year()
    _head("02 / Thị hiếu theo quốc gia", "Bản sắc địa lý & ADN âm nhạc", "Bản đồ quốc gia và so sánh sáu chiều âm thanh trên cùng thang phân vị", "2021–2022 · 73 quốc gia tối đa")
    c1, c2, c3, c4, c5 = st.columns([.55, 1.5, 1.05, 1.12, 1.12], gap="small")
    with c1:
        year = st.selectbox("Năm", [2022, 2021], key="story_geo_year")
    full = all_countries[all_countries["year"].eq(year)].copy()
    regions = sorted(full["wb_region"].dropna().unique())
    with c2:
        region = st.selectbox("Khu vực", ["Tất cả"] + regions, key="story_geo_region",
                              on_change=_bump_chart_key, args=("story_geo_map_nonce",))
    mapped = full if region == "Tất cả" else full[full["wb_region"].eq(region)]
    countries = sorted(mapped["chart_country"].tolist())
    with c3:
        feature = st.selectbox("Màu bản đồ", ["valence", "danceability", "acousticness", "energy"],
                               format_func=lambda item: FEATURE_LABEL[item], key="story_geo_feature")
    pending_country = st.session_state.pop("story_geo_pending", None)
    if pending_country in countries:
        st.session_state["story_geo_a"] = pending_country
    if st.session_state.get("story_geo_a") not in countries:
        st.session_state["story_geo_a"] = "Vietnam" if "Vietnam" in countries else countries[0]
    with c4:
        first = st.selectbox("Quốc gia A", countries, key="story_geo_a",
                             on_change=_bump_chart_key, args=("story_geo_map_nonce",))
    country_options = sorted(name for name in full["chart_country"].tolist() if name != first)
    if st.session_state.get("story_geo_b") not in country_options:
        st.session_state["story_geo_b"] = "Japan" if "Japan" in country_options else (
            "Vietnam" if "Vietnam" in country_options else country_options[0]
        )
    with c5:
        second = st.selectbox("So với B", country_options, key="story_geo_b")

    panels = st.columns([1.35, 1], gap="small")
    with panels[0]:
        with st.container(border=True):
            _card("06 · Bản đồ đặc trưng âm thanh", f"{len(mapped)} quốc gia · chọn khu vực rồi bấm quốc gia")
            map_key = f"story_geo_map_{st.session_state.get('story_geo_map_nonce', 0)}"
            event = st.plotly_chart(_map_figure(mapped, feature), width="stretch", config=PLOT_CONFIG,
                                    key=map_key, on_select="rerun", selection_mode="points")
            points = _points(event)
            code = points[0].get("location") if points else None
            if not code and points:
                data = points[0].get("customdata", [])
                clicked_name = data[2] if len(data) > 2 else None
                matches_by_name = mapped.loc[mapped["chart_country"].eq(clicked_name), "country_code"]
                code = matches_by_name.iloc[0] if not matches_by_name.empty else None
            if code:
                matches = mapped.loc[mapped["country_code"].eq(code), "chart_country"]
                if not matches.empty:
                    clicked = str(matches.iloc[0])
                    if clicked != st.session_state.get("story_geo_map_last"):
                        st.session_state["story_geo_map_last"] = clicked
                        st.session_state["story_geo_pending"] = clicked
                        st.rerun()
    with panels[1]:
        with st.container(border=True):
            _card("07 · Hai dấu vân tay âm nhạc", "phân vị giữa các quốc gia cùng năm")
            st.plotly_chart(_radar_figure(full, first, second), width="stretch", config=PLOT_CONFIG)

    fa = full.loc[full["chart_country"].eq(first)].iloc[0]
    fb = full.loc[full["chart_country"].eq(second)].iloc[0]
    region_means = full.groupby("wb_region")["valence_weighted"].mean().sort_values(ascending=False)
    top_region, top_val = region_means.index[0], region_means.iloc[0]
    ac_ratio = float(fa["acousticness_weighted"] / fb["acousticness_weighted"]) if fb["acousticness_weighted"] else float("nan")
    _insights(
        f"{top_region} có Valence trung bình cao nhất ({top_val:.3f}) trong {year}. {first}: Acousticness {fa['acousticness_weighted']:.3f}; {second}: {fb['acousticness_weighted']:.3f}.",
        "Khác biệt có thể liên quan đến thể loại, ngôn ngữ và danh mục bài hát của từng thị trường; các biến đó chưa được kiểm soát trên bản đồ.",
        f"Acousticness của {first} bằng {ac_ratio:.1f} lần {second}; so sánh radar dùng phân vị để không trộn BPM, dB và thang 0–1.",
        "Đây là trung bình có trọng số streams của Top 200, không đại diện mọi lượt nghe. Nhóm khu vực ít quốc gia cần đọc thận trọng.",
    )


def _seasonal_chart(monthly: pd.DataFrame, selected_month: int | None) -> go.Figure:
    fig = go.Figure()
    for col, name, color in (
        ("danceability_weighted", "Danceability", PLUM),
        ("acousticness_weighted", "Acousticness", TEAL),
    ):
        colors = [color if selected_month in (None, month) else "#D8D0C7" for month in monthly["month"]]
        fig.add_trace(go.Bar(
            x=monthly["month"].map(lambda m: f"T{m}"), y=monthly[col],
            name=name, marker_color=colors,
            customdata=monthly["month"],
            hovertemplate="Tháng %{customdata}<br>" + name + ": %{y:.3f}<extra></extra>",
        ))
    fig.update_layout(barmode="group", legend=dict(orientation="h", x=.01, y=1.14, font=dict(size=10)))
    fig.update_xaxes(title=None, showgrid=False)
    fig.update_yaxes(title=None, range=[0, max(.8, float(monthly[["danceability_weighted", "acousticness_weighted"]].max().max()) * 1.08)], gridcolor="#EEE9E1")
    fig = _style(fig, 160, showlegend=True)
    fig.update_layout(margin=dict(l=30, r=8, t=20, b=19))
    return fig


def _covid_chart(frame: pd.DataFrame, feature: str, selected_month: int | None) -> go.Figure:
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(
        x=frame["week"], y=frame["weekly_deaths"], name="Tử vong/tuần",
        marker_color="rgba(215,137,77,.40)",
        hovertemplate="%{x|%d/%m/%Y}<br>Tử vong mới: %{y:,.0f}<extra></extra>",
    ), secondary_y=True)
    fig.add_trace(go.Scatter(
        x=frame["week"], y=frame[f"{feature}_ma4"], mode="lines",
        name=FEATURE_LABEL[feature] + " (MA4)", line=dict(color=PLUM, width=2.5),
        customdata=frame[f"{feature}_weighted"],
        hovertemplate="%{x|%d/%m/%Y}<br>MA4: %{y:.3f}<br>Tuần gốc: %{customdata:.3f}<extra></extra>",
    ), secondary_y=False)
    if selected_month is not None:
        selected = frame[frame["week"].dt.month.eq(selected_month)]
        fig.add_trace(go.Scatter(
            x=selected["week"], y=selected[f"{feature}_ma4"], mode="markers",
            name=f"Các tuần tháng {selected_month}", marker=dict(color=TEAL, size=7, line=dict(color="#FFFFFF", width=1)),
            hovertemplate="%{x|%d/%m/%Y}<br>" + FEATURE_LABEL[feature] + ": %{y:.3f}<extra></extra>",
        ), secondary_y=False)
    fig.update_xaxes(title=None, tickformat="%m/%Y", dtick="M6", gridcolor="#F1ECE6")
    fig.update_yaxes(title_text=FEATURE_LABEL[feature], secondary_y=False, gridcolor="#EEE9E1")
    fig.update_yaxes(title_text="Tử vong mới", secondary_y=True, showgrid=False, tickformat="~s")
    fig = _style(fig, 248, showlegend=True)
    fig.update_layout(hovermode="x unified", barmode="overlay",
                      legend=dict(orientation="h", x=.01, y=1.12, font=dict(size=10)),
                      margin=dict(l=60, r=60, t=24, b=23))
    return fig


def dashboard_time() -> None:
    weekly = weekly_audio()
    country_table = country_year()
    _head("03 / Thời gian & biến cố", "Mùa vụ âm nhạc và COVID-19", "Mô hình 12 tháng · đặc trưng âm thanh và tử vong mới theo tuần", "2022 chỉ đến tháng 7")
    top = st.columns([1.3, 1.1, 1.0, .75], gap="small")
    with top[0]:
        regions = sorted(country_table["wb_region"].dropna().unique())
        region = st.selectbox("Khu vực", ["Toàn cầu"] + regions, key="story_time_region")
    country_options = ["Global"] if region == "Toàn cầu" else sorted(
        country_table.loc[country_table["wb_region"].eq(region), "chart_country"].unique()
    )
    if st.session_state.get("story_time_country") not in country_options:
        st.session_state["story_time_country"] = country_options[0]
    with top[1]:
        country = st.selectbox("Quốc gia", country_options, key="story_time_country")
    with top[2]:
        feature = st.selectbox("Đặc trưng âm thanh", AUDIO, index=AUDIO.index("acousticness"),
                               format_func=lambda item: FEATURE_LABEL[item], key="story_time_feature")
    with top[3]:
        covid_year = st.selectbox("Giai đoạn dịch", ["2020–2022", "2020", "2021", "2022"], key="story_time_covid_year")

    available = weekly.loc[weekly["chart_country"].eq(country)].copy()
    available["year"] = available["week"].dt.year
    if country == "Global":
        season = available[available["year"].between(2017, 2019)]
        season_label = "nền 2017–2019 · đủ năm"
    else:
        season = available[available["year"].eq(2021)]
        season_label = "2021 · đủ năm"
    if season.empty:
        return _empty("Quốc gia này chưa có đủ dữ liệu mùa vụ để hiển thị.")
    season = season.assign(month=season["week"].dt.month)
    monthly = season.groupby("month", as_index=False)[["danceability_weighted", "acousticness_weighted"]].mean()
    monthly = monthly.set_index("month").reindex(range(1, 13)).reset_index()
    if monthly[["danceability_weighted", "acousticness_weighted"]].isna().all(axis=1).any():
        return _empty("Thiếu một số tháng trong dữ liệu mùa vụ của quốc gia này.")

    selected_month = st.session_state.get("story_time_month")
    with st.container(border=True):
        _card("08 · Mùa vụ trong 12 tháng", f"{season_label} · bấm cột tháng để soi trên biểu đồ tuần")
        month_key = f"story_month_event_{st.session_state.get('story_month_nonce', 0)}"
        event = st.plotly_chart(_seasonal_chart(monthly, selected_month), width="stretch", config=PLOT_CONFIG,
                                key=month_key, on_select="rerun", selection_mode="points")
        points = _points(event)
        month_value = points[0].get("x") if points else None
        month = int(str(month_value)[1:]) if str(month_value).startswith("T") and str(month_value)[1:].isdigit() else None
        if month and _check_selection("story_time_month", str(month)):
            st.session_state["story_time_month"] = month
            st.rerun()

    frame = aligned_covid(country)
    if frame.empty:
        return _empty("Không ghép được tuần Spotify với dữ liệu tử vong COVID-19 ở thị trường này.")
    if covid_year != "2020–2022":
        frame = frame[frame["week"].dt.year.eq(int(covid_year))]
    if frame.empty:
        return _empty("Không có tuần giao nhau trong giai đoạn đang chọn.")
    with st.container(border=True):
        _card("09 · Tử vong và đặc trưng âm thanh theo tuần", f"{len(frame)} tuần quan sát · MA4 cho đường âm thanh")
        st.plotly_chart(_covid_chart(frame, feature, selected_month), width="stretch", config=PLOT_CONFIG)

    if selected_month is not None:
        if st.button(f"Đang soi tháng {selected_month} · Xóa lựa chọn", key="story_time_month_clear", type="tertiary"):
            st.session_state["story_time_month"] = None
            _bump_chart_key("story_month_nonce")
            st.rerun()

    dec = monthly.loc[monthly["month"].eq(12)].iloc[0]
    rest = monthly.loc[monthly["month"].ne(12), ["danceability_weighted", "acousticness_weighted"]].mean()
    feature_col = f"{feature}_ma4"
    positive = frame[frame["weekly_deaths"].gt(0)]
    if len(positive) >= 12:
        q1, q3 = positive["weekly_deaths"].quantile([.25, .75])
        low = positive.loc[positive["weekly_deaths"].le(q1), feature_col].mean()
        high = positive.loc[positive["weekly_deaths"].ge(q3), feature_col].mean()
        death_text = f"{FEATURE_LABEL[feature]} ở nhóm tuần tử vong cao chênh {high-low:+.3f} so với nhóm thấp."
    else:
        death_text = "Chưa đủ tuần có ca tử vong để so sánh hai nhóm."
    _insights(
        f"Tháng 12: Danceability {dec['danceability_weighted']:.3f} (11 tháng khác {rest['danceability_weighted']:.3f}); Acousticness {dec['acousticness_weighted']:.3f} (11 tháng khác {rest['acousticness_weighted']:.3f}).",
        "Dòng nhạc lễ hội và catalog cũ là giả thuyết phù hợp với mẫu tháng 12; muốn kiểm chứng cần xét thể loại và tuổi bài hát.",
        death_text + " Đường tuần giúp xem các đợt dịch có trùng thời điểm thay đổi âm thanh hay không.",
        "Đường chồng hai trục và so sánh tuần không chứng minh COVID hay phong tỏa gây đổi gu nghe. Dữ liệu Spotify 2022 chưa đủ năm.",
    )


def render_story_dashboard(page: str) -> None:
    _css()
    if page == STORY_PAGES[0]:
        dashboard_hit()
    elif page == STORY_PAGES[1]:
        dashboard_geography()
    elif page == STORY_PAGES[2]:
        dashboard_time()
