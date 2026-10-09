import sys
import unittest
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'dashboard'))
from story_analysis import FEATURES, artist_history, global_slots, track_analysis


class StoryAnalysisTest(unittest.TestCase):
    def setUp(self):
        weeks = pd.date_range('2020-01-02', periods=10, freq='7D')
        rows = []
        for i, week in enumerate(weeks):
            rows.append(dict(artist_id='a', track_id='old', week=week, streams=10, rank=20, chart_country='Global'))
            if i >= 1:
                for artist in ['a', 'b']:
                    rows.append(dict(artist_id=artist, track_id='new', week=week, streams=100, rank=1, chart_country='Global'))
        rows.append(dict(artist_id='a', track_id='new', week=weeks[1], streams=9999, rank=1, chart_country='Vietnam'))
        self.charts = pd.DataFrame(rows)
        self.tracks = pd.DataFrame([
            dict(track_id=t, artist_id='a', **{f: .5 for f in FEATURES}) for t in ['old', 'new']])

    def test_credit_duplicates_and_market_overlap(self):
        t = track_analysis(self.charts, self.tracks, warmup_weeks=0).set_index('track_id')
        self.assertEqual(t.loc['new', 'streams_first_8w'], 800)
        self.assertEqual(t.loc['old', 'streams_first_8w'], 80)
        self.assertEqual(len(global_slots(self.charts)), 19)

    def test_prior_excludes_entry_and_future(self):
        h = artist_history(self.charts)
        entry = self.charts.week.min() + pd.Timedelta(weeks=1)
        a = h[h.artist_id.eq('a') & h.week.eq(entry)].iloc[0]
        self.assertEqual((a.S, a.N, a.W, a.R), (10, 1, 1, 20))
        changed = self.charts.copy()
        changed.loc[changed.week.ge(entry), 'streams'] *= 100
        h2 = artist_history(changed)
        b = h2[h2.artist_id.eq('a') & h2.week.eq(entry)].iloc[0]
        self.assertEqual(a.artist_popularity_prior, b.artist_popularity_prior)

    def test_incomplete_followup_removed(self):
        t = track_analysis(self.charts[self.charts.week.lt(self.charts.week.max()-pd.Timedelta(weeks=1))], self.tracks, warmup_weeks=0)
        self.assertNotIn('new', t.track_id.tolist())


if __name__ == '__main__': unittest.main()
