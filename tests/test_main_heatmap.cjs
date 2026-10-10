const fs = require('node:fs'), vm = require('node:vm'), assert = require('node:assert/strict');
const {execFileSync} = require('node:child_process');
const script = `import sys,json,pandas as pd
sys.path.insert(0,'dashboard')
import story_canvas
b=story_canvas.data_bundle()
f=b['features']
c=pd.read_parquet('data/processed/charts_clean.parquet',columns=['chart_country','week','rank','track_id','year',*f])
c=c[c.chart_country.eq('Global') & c.year.between(2020,2022)].drop_duplicates(['chart_country','week','rank','track_id'])
bands=pd.cut(c['rank'],[0,10,50,100,200],labels=False)
b['_expected'] = ((c.groupby(bands)[f].mean()-c[f].mean())/c[f].std(ddof=0)).values.tolist()
print(json.dumps(b))`;
const bundle = JSON.parse(execFileSync('python', ['-X','utf8','-c',script], {encoding:'utf8',maxBuffer:40*1024*1024}));
const element = () => ({replaceChildren(){},append(){},prepend(){},style:{},closest(){return element()},firstChild:{nodeValue:''},classList:{toggle(){},add(){}},querySelectorAll(){return[]},querySelector(){return element()},setAttribute(){},removeAttribute(){},on(){}});
const elements = new Map();
const ctx = vm.createContext({bundle,console,setTimeout,clearTimeout,localStorage:{getItem(){return null}},ResizeObserver:class{observe(){}},window:{print(){}},Plotly:{newPlot:async()=>{},relayout(){},restyle(){},purge(){}},document:{getElementById(id){if(!elements.has(id))elements.set(id,element());return elements.get(id)},querySelectorAll(){return[]},querySelector(){return element()},createElement:element,createTextNode(text){return{nodeValue:text}},addEventListener(){},body:{classList:{toggle(){}}},documentElement:{requestFullscreen(){}}}});
vm.runInContext(fs.readFileSync('dashboard/story_interactions.js','utf8').split('const hints=')[0],ctx);
const run = code => vm.runInContext(code,ctx);
run("position=0;state=defaults({fromyear:2017,toyear:2022});current=buildModel()");
assert.equal(run('kind()'),'main_dashboard');
const actual = run('figure("hit_heatmap").data[0].z');
for(let i=0;i<4;i++)for(let j=0;j<9;j++){
  assert.ok(Math.abs(actual[i][j]-bundle._expected[i][j])<1e-5,`Notebook parity: band ${i}, feature ${j}`);
  assert.equal(actual[i][j].toFixed(2),bundle._expected[i][j].toFixed(2));
}
assert.equal(run('chartRows("hit_heatmap")[0].z_score'),actual[0][0]);
assert.equal(actual[0][0].toFixed(2),'0.13');
assert.equal(actual[0][8].toFixed(2),'0.16');
assert.ok(run('chartTitle("hit_heatmap")').includes('2020–2022'));
console.log('Passed: all 36 Main Dashboard heatmap cells match notebook calculations and exported values.');
