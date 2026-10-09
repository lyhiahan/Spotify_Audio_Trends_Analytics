const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),{execFileSync}=require('node:child_process');
const bundle=JSON.parse(execFileSync('python',['-c',"import sys,json,pandas as pd; sys.path.insert(0,'dashboard'); import story_canvas; b=story_canvas.data_bundle(); b['_test_corr']=pd.DataFrame([[*b['tracks'][r[0]][5:14],r[2],r[3]] for r in b['analysis']]).corr(method='spearman').values.tolist(); print(json.dumps(b))"],{encoding:'utf8',maxBuffer:30*1024*1024}));
const element=()=>({replaceChildren(){},append(){},prepend(){},style:{},closest(){return element()},firstChild:{nodeValue:''},classList:{toggle(){},add(){}},querySelectorAll(){return[]},querySelector(){return element()},setAttribute(){},removeAttribute(){},on(){}}),elements=new Map();
const ctx=vm.createContext({bundle,console,setTimeout,clearTimeout,localStorage:{getItem(){return null}},ResizeObserver:class{observe(){}unobserve(){}disconnect(){}},window:{print(){}},Plotly:{newPlot:async()=>{},relayout(){},purge(){}},document:{getElementById(id){if(!elements.has(id))elements.set(id,element());return elements.get(id)},querySelectorAll(){return[]},querySelector(){return element()},createElement:element,createTextNode(text){return{nodeValue:text}},addEventListener(){},body:{classList:{toggle(){}}},documentElement:{requestFullscreen(){}}}});
vm.runInContext(fs.readFileSync('dashboard/story_interactions.js','utf8').split('const hints=')[0],ctx);
const run=s=>vm.runInContext(s,ctx);
run('state=defaults({fromyear:2017,toyear:2022});current=buildModel()');
assert.equal(bundle.tracks.length,39190);
const collab=run('collabStats()');assert.equal(collab.reduce((s,r)=>s+r.count,0),new Set(bundle.global_rows.map(r=>r[0])).size);assert.ok(collab[1].mean/collab[0].mean<1.5,'Artist-credit duplicates must not inflate Collab to three times Solo');
assert.ok(collab.every(r=>r.charted>0&&r.mean>0));
const raw=run('hitStats()');
for(let j=0;j<9;j++){
 const rows=bundle.global_rows,valid=rows.filter(r=>Number.isFinite(bundle.tracks[r[0]][5+j])),n=valid.reduce((s,r)=>s+r[4],0),mean=valid.reduce((s,r)=>s+bundle.tracks[r[0]][5+j]*r[4],0)/n;
 assert.ok(Math.abs(raw.baseline[j].mean-mean)<1e-8);
 const weightedZ=raw.z.reduce((s,a,i)=>s+(a[j]||0)*raw.counts[i],0)/n;
 assert.ok(Math.abs(weightedZ)<1e-6,'Band z-scores must center on the full slot population');
}
run("state.genre='pop';state.band='0';current=buildModel()");assert.ok(run('current.rows.every(r=>r[3]===0&&bundle.tracks[r[0]][2]==="pop")'));
assert.ok(run('figure("genre_box").data.every(t=>t.name==="pop")'));
assert.ok(run('figure("duration").data[0].x.length')>0,'Filtered duration must use numeric track durations');
run("state=defaults({year:2021,weight:'mean'});current=buildModel()");const radar=run('figure("radar")');assert.equal(radar.data.length,2);const vn=bundle.countries.find(r=>r[0]==='VNM'&&r[2]===2021);assert.equal(radar.data[0].r[0],vn[18]);
run("state.weight='weighted';current=buildModel()");assert.equal(run('figure("radar").data[0].r[0]'),vn[9]);
run("state=defaults({month:'12'});current=buildModel()");assert.ok(run('current.covid.every(r=>Number(r[0].slice(5,7))===12)'));const covid=run('figure("covid")');assert.ok(covid.data[1].y.includes(null),'Filtered months must not draw lines across missing months');
const counts=run('figure("seasonal").data[0].customdata');assert.equal(counts.reduce((s,n)=>s+n,0),bundle.weekly.length);
run("state=defaults({fromyear:2022,toyear:2022,genre:'nonexistent'});current=buildModel()");assert.equal(run('figure("genre_box").data.length'),0);assert.ok(run('hitStats().z.every(r=>r.every(v=>v===null))'));
run('position=2;state=defaults({fromyear:2017,toyear:2022});current=buildModel()');
const correlation=run('correlationStats()');assert.equal(correlation.n,bundle.analysis.length);
for(let i=0;i<11;i++)for(let j=0;j<11;j++)assert.ok(Math.abs(correlation.z[i][j]-bundle._test_corr[i][j])<1e-10,'Spearman must match pandas');
assert.equal(run('collabStats().reduce((s,r)=>s+r.count,0)'),bundle.analysis.length);
assert.ok(run('artistStory().every(r=>typeof r[1]==="string")'));
run("state.genre='nonexistent';current=buildModel()");assert.equal(run('figure("correlation").data.length'),0);assert.ok(run('artistStory().every(r=>typeof r[1]==="string")'));
console.log('Passed: de-duplicated Global Collab, nine z-scores, hierarchical filters, duration drill-down, consistent radar, month linking, empty populations and Spearman parity with pandas.');
// Opening EDA keeps the full track population separate from the training cohort.
assert.equal(bundle.workbook.version,6);
assert.equal(bundle.workbook.story_points.length,5);
assert.equal(bundle.workbook.story_points[0].dashboard_id,'overview');
assert.equal(bundle.eda.tracks,bundle.tracks.length);
assert.equal(bundle.eda.train.count,2625);
assert.equal(bundle.eda.train.positives,622);
assert.equal(bundle.eda.train.tiers.reduce((n,t)=>n+t.count,0),2625);
assert.equal(bundle.eda.train.tiers.reduce((n,t)=>n+t.positives,0),622);
for(const feature of bundle.eda.features){
 run(`state=defaults({feature:${JSON.stringify(feature)}});current=buildModel()`);
 const dist=run('figure("eda_distribution")');
 assert.equal(dist.data[0].y.reduce((a,b)=>a+b,0),39190);
 assert.equal(run('chartRows("eda_distribution").reduce((n,r)=>n+r.tracks,0)'),39190);
 assert.equal(dist.layout.shapes[1].x0,bundle.eda.distributions[feature].median);
}
const matrix=run('figure("eda_correlation")');
assert.equal(matrix.data[0].z[0][0],null);
assert.ok(Math.abs(bundle.eda.correlations[2][1]-.690178959)<1e-8);
assert.equal(run('chartRows("eda_correlation").length'),45);
assert.equal(run('figure("eda_rank").data[0].customdata.reduce((n,r)=>n+r[0],0)'),2625);
run('legacy=clone(bundle.workbook);legacy.version=5;delete legacy.dashboards.overview;legacy.story_points.shift();legacy.story_points[0].caption="Caption đã biên tập";migrated=validate(legacy)');
assert.equal(run('migrated.story_points[0].dashboard_id'),'overview');
assert.equal(run('migrated.story_points[1].caption'),'Caption đã biên tập');
assert.equal(run('migrated.version'),6);
run('state=defaults({feature:"energy"});link("eda_correlation",{x:"loudness",y:"energy",z:.69})');
assert.equal(run('state.feature'),'loudness');
run('link("eda_rank",{x:"51–100"})');assert.equal(run('state.eda_tier'),'51–100');
run('link("eda_rank",{x:"51–100"})');assert.equal(run('state.eda_tier'),'');
console.log('Passed: opening EDA populations, distributions, Spearman, rank tiers, linked selections and v5 migration.');

// The opening gallery must use the exact saved PNG outputs from 02_eda.
const notebook=JSON.parse(fs.readFileSync('notebooks/02_eda.ipynb','utf8'));
assert.deepEqual(bundle.workbook.dashboards.overview.worksheets,Object.keys(bundle.eda_figures));
assert.equal(Object.keys(bundle.eda_figures).length,4);
for(const asset of Object.values(bundle.eda_figures)){
 const output=notebook.cells[asset.cell-1].outputs.find(o=>o.data?.['image/png']);
 const encoded=output.data['image/png'];
 assert.equal(asset.image,'data:image/png;base64,'+(Array.isArray(encoded)?encoded.join(''):encoded));
 const raw=Buffer.from(asset.image.split(',')[1],'base64');
 assert.equal(raw.subarray(1,4).toString(),'PNG');
 assert.equal(asset.width,raw.readUInt32BE(16));
 assert.equal(asset.height,raw.readUInt32BE(20));
 assert.equal(asset.sha256,require('node:crypto').createHash('sha256').update(raw).digest('hex'));
}
console.log('Passed: four static EDA figures match the notebook PNG outputs exactly.');
