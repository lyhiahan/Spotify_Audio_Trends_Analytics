"""Execute every code cell in a new IPython kernel, without rewriting notebook outputs."""
import json
import sys
from pathlib import Path
from jupyter_client import KernelManager

ROOT = Path(__file__).resolve().parents[1]

def execute(client, code):
    message = client.execute(code)
    error = None
    while True:
        reply = client.get_iopub_msg(timeout=300)
        if reply.get('parent_header', {}).get('msg_id') != message:
            continue
        content = reply['content']
        if reply['msg_type'] == 'error':
            error = '\n'.join(content['traceback'])
        if reply['msg_type'] == 'status' and content['execution_state'] == 'idle':
            break
    if error:
        raise RuntimeError(error)

if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
    manager = KernelManager()
    manager.kernel_spec.argv[0] = sys.executable
    print('Starting a fresh IPython kernel...', flush=True)
    manager.start_kernel(cwd=str(ROOT / 'notebooks'))
    client = manager.client()
    client.start_channels()
    try:
        client.wait_for_ready(timeout=60)
        execute(client, "import plotly.io as pio; pio.renderers.default = 'json'")
        notebook = json.loads((ROOT / 'notebooks/04_story.ipynb').read_text(encoding='utf-8'))
        for i, cell in enumerate(notebook['cells']):
            if cell['cell_type'] == 'code':
                execute(client, ''.join(cell['source']))
                print(f'PASS cell {i}', flush=True)
        execute(client, "assert df_corr.track_id.is_unique; assert track_streams.track_id.is_unique; assert features[0] == 'acousticness_weighted'")
        execute(client, '''
import story_data
bundle = story_data.load_bundle()
rows = pd.DataFrame(bundle['analysis'], columns=['i','date','prior','streams','artist_id'])
rows['track_id'] = rows['i'].map(lambda i: bundle['tracks'][int(i)][0])
comparison = df_analysis.merge(rows, on='track_id', validate='one_to_one')
assert len(comparison) == len(df_analysis) == len(rows)
assert np.allclose(comparison['artist_popularity_prior'], comparison['prior'])
assert np.allclose(comparison['streams_first_8w'], comparison['streams'])
global_by_year = global_slots(df_charts).groupby(['track_id','year'])['streams'].sum()
for row in bundle['tracks']:
    for year, value in row[-1].items():
        assert value == global_by_year.loc[(row[0], int(year))]
print(f"QA: notebook/dashboard agree on {len(comparison):,} songs, prior scores, eight-week streams and Global annual totals.")
''')
        print('PASS: complete notebook from a fresh kernel; no data/model files written.')
    finally:
        client.stop_channels()
        manager.shutdown_kernel(now=True)
