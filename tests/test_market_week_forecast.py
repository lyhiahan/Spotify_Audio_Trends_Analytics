"""Read-only audit of the exported market-week forecasting dataset.

Run from the repository root: python tests/test_market_week_forecast.py
Checks reconstruct features/labels independently; failures do not mutate data.
"""
from pathlib import Path
import json
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RESULTS = []


def check(name, mask, detail=""):
    values = np.asarray(pd.Series(mask).fillna(False), dtype=bool)
    failures = int((~values).sum())
    RESULTS.append(dict(test=name, passed=failures == 0,
                        checked=int(values.size), failures=failures, detail=detail))
    print(f"{'PASS' if failures == 0 else 'FAIL'} {name}: {failures}/{values.size} failures {detail}")


def main():
    d = pd.read_parquet(ROOT / 'data/processed/ml_market_week_forecast.parquet')
    source = pd.read_parquet(ROOT / 'data/processed/charts_clean.parquet')
    source = source[source.chart_country != 'Global'].copy()
    s = source.drop_duplicates(['track_id', 'chart_country', 'week']).copy()
    keys = ['track_id', 'chart_country', 'week']
    check('unique_sample_key', ~d.duplicated(keys))
    check('country_only', d.chart_country != 'Global')
    check('source_sample_count', [len(d) == len(s)])
    check('source_sample_keys', [set(map(tuple, d[keys].to_numpy())) == set(map(tuple, s[keys].to_numpy()))])
    check('calendar_week_idx', d.week == d.week.min() + pd.to_timedelta(d.week_idx.astype(int) * 7, unit='D'))
    check('rank_range', d.local_rank_t.between(1, 200))
    check('positive_streams', d.local_streams_t > 0)
    check('cohort_definition', (d.cohort_group == 'breakthrough') == (d.local_rank_t > 50))
    check('rating_range', d.rating_t.between(0, 100))
    expected_rating = .4 * (100 * (200 - d.local_rank_t) / 199) + 35 * d.streams_ratio_to_top1_t + 25 * d.other_market_coverage_t
    check('rating_formula', np.isclose(d.rating_t, expected_rating, atol=2e-5))
    check('stream_share_sums_to_one', np.isclose(d.groupby(['chart_country', 'week'], observed=True).local_chart_stream_share_t.sum(), 1, atol=1e-6))
    rank_lookup = s.set_index(['track_id', 'chart_country', 'week'])['rank']
    reference_rank = rank_lookup.reindex(pd.MultiIndex.from_frame(d[keys])).to_numpy()
    check('local_rank_matches_source', d.local_rank_t.to_numpy() == reference_rank)
    market_count = s.groupby('week', observed=True).chart_country.nunique()
    track_count = s.groupby(['track_id', 'week'], observed=True).chart_country.nunique()
    observed_count = d.week.map(market_count).to_numpy()
    other_count = track_count.reindex(pd.MultiIndex.from_frame(d[['track_id', 'week']])).to_numpy() - 1
    check('other_markets_count', d.n_other_markets_charted_t.to_numpy() == other_count)
    check('coverage_denominator', np.isclose(d.other_market_coverage_t, other_count / (observed_count - 1), atol=1e-6))
    # Calendar-based future lookup, independent of notebook week-index merge.
    market_weeks = set(map(tuple, s[['chart_country', 'week']].drop_duplicates().to_numpy()))
    expected_valid = np.ones(len(d), dtype=bool)
    expected_hit = np.zeros(len(d), dtype=bool)
    for k in range(1, 9):
        future = d[keys].copy()
        future['week'] += pd.Timedelta(weeks=k)
        ranks = rank_lookup.reindex(pd.MultiIndex.from_frame(future)).to_numpy()
        expected_hit |= ranks <= 50
        expected_valid &= np.array([(c, w) in market_weeks for c, w in future[['chart_country', 'week']].itertuples(index=False, name=None)])
    check('future_calendar_coverage_flag', d.has_valid_future_window.to_numpy() == expected_valid)
    check('unknown_labels_preserved', d.hit_next_8_weeks.isna().to_numpy() == ~expected_valid)
    check('future_label_from_clean_source', d.loc[expected_valid, 'hit_next_8_weeks'].astype(int).to_numpy() == expected_hit[expected_valid].astype(int))
    for left, right in [('train', 'val'), ('val', 'test')]:
        end = d.loc[d.split_group == left, 'week'].max() + pd.Timedelta(weeks=8)
        start = d.loc[d.split_group == right, 'week'].min()
        check(f'{left}_{right}_label_embargo', [end < start], f'{end.date()} < {start.date()} (publication timestamps unavailable)')
    check('model_splits_have_labels', d.loc[d.split_group.isin(['train', 'val', 'test']), 'hit_next_8_weeks'].notna())
    prior = d[keys].copy()
    prior['week'] -= pd.Timedelta(weeks=1)
    previous_rank = rank_lookup.reindex(pd.MultiIndex.from_frame(prior)).to_numpy()
    check('rank_lag_calendar', np.isclose(d.rank_improvement_1w.astype(float), previous_rank - d.local_rank_t, atol=1e-5, equal_nan=True))
    stream_lookup = s.set_index(keys)['streams']
    previous_stream = stream_lookup.reindex(pd.MultiIndex.from_frame(prior)).to_numpy()
    expected_change = np.log(d.local_streams_t.astype(float)) - np.log(previous_stream)
    check('stream_change_exported_log_contract', np.isclose(d.log_stream_change_1w.astype(float), expected_change, atol=1e-6, rtol=0, equal_nan=True))
    log1p_change = np.log1p(d.local_streams_t.astype(float)) - np.log1p(previous_stream)
    print('INFO max log versus log1p delta:', float(np.nanmax(np.abs(expected_change - log1p_change))))
    # Independently walk groups to test ordering, streak and observed calendar rolling mean.
    ordered = d.sort_values(['chart_country', 'track_id', 'week']).copy()
    group = ordered.groupby(['chart_country', 'track_id'], observed=True, sort=False)
    gap = group.week.diff().dt.days.ne(7)
    streak_group = gap.groupby([ordered.chart_country, ordered.track_id], observed=True).cumsum()
    streak = ordered.groupby([ordered.chart_country, ordered.track_id, streak_group], observed=True).cumcount() + 1
    check('consecutive_streak', ordered.consecutive_chart_weeks_t.to_numpy() == streak.to_numpy())
    check('historical_best_rank', ordered.best_local_rank_to_date.to_numpy() == group.local_rank_t.cummin().to_numpy())
    share_lookup = ordered.set_index(keys).local_chart_stream_share_t
    sums = np.zeros(len(ordered))
    counts = np.zeros(len(ordered))
    streak_sums = np.zeros(len(ordered))
    streak_counts = np.zeros(len(ordered))
    for k in range(4):
        past = ordered[keys].copy()
        past['week'] -= pd.Timedelta(weeks=k)
        shares = share_lookup.reindex(pd.MultiIndex.from_frame(past)).to_numpy()
        exists = ~np.isnan(shares)
        sums += np.nan_to_num(shares)
        counts += exists
        continuous = exists & (ordered.consecutive_chart_weeks_t.to_numpy() > k)
        streak_sums += np.where(continuous, shares, 0)
        streak_counts += continuous
    rolling = sums / counts
    check('share_mean_consecutive_streak_alignment', np.isclose(ordered.chart_stream_share_mean_4w, streak_sums / streak_counts, atol=1e-7, rtol=1e-5))
    check('share_mean_four_calendar_weeks', np.isclose(ordered.chart_stream_share_mean_4w, rolling, atol=1e-7, rtol=1e-5))
    # Multiple artists: compare exported flag with ANY credited artist's strictly prior success.
    first_top = source[source['rank'] <= 50].groupby(['artist_id', 'chart_country'], observed=True).week.min().rename('first_top50')
    links = source[['track_id', 'chart_country', 'week', 'artist_id']].drop_duplicates().merge(first_top, on=['artist_id', 'chart_country'], how='left')
    links['prior'] = links.first_top50.notna() & (links.first_top50 < links.week)
    any_prior = links.groupby(keys, observed=True).prior.any().reindex(pd.MultiIndex.from_frame(d[keys])).to_numpy()
    check('artist_prior_any_credited_artist', d.artist_prior_local_top50.to_numpy() == any_prior)
    counts = s.groupby(['chart_country', 'week'], observed=True)['rank'].nunique()
    check('target_source_full_top200', counts == 200, 'Incomplete clean charts cannot certify absence; recover raw chart rows before label creation.')
    summary = d.groupby(['split_group', 'cohort_group'], observed=True).agg(rows=('track_id', 'size'), labeled=('hit_next_8_weeks', 'count'), hits=('hit_next_8_weeks', 'sum'))
    print('\nSPLIT SUMMARY\n', summary.to_string())
    output = ROOT / 'reports/market_week_forecast_audit.json'
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps({'rows': len(d), 'columns': len(d.columns), 'checks': RESULTS}, indent=2), encoding='utf-8')
    print(f'\n{sum(r["passed"] for r in RESULTS)}/{len(RESULTS)} checks passed. Report: {output}')
    return 0 if all(r['passed'] for r in RESULTS) else 1


if __name__ == '__main__':
    sys.exit(main())
