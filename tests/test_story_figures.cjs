const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),{execFileSync}=require('node:child_process');
const bundle=JSON.parse(execFileSync('python',['-c',"import sys,json; sys.path.insert(0,'dashboard'); import story_canvas; print(json.dumps(story_canvas.data_bundle()))"],{encoding:'utf8',maxBuffer:30*1024*1024}));
const element=()=>({replaceChildren(){},append(){},style:{}}),elements=new Map();
const ctx=vm.createContext({bundle,console,localStorage:{getItem(){return null}},document:{getElementById(id){if(!elements.has(id))elements.set(id,element());return elements.get(id)},createElement:element}});
vm.runInContext(fs.readFileSync('dashboard/story_interactions.js','utf8').split('const hints=')[0],ctx);
const run=s=>vm.runInContext(s,ctx);
run('state=defaults({fromyear:2017,toyear:2022});current=buildModel()');
const collab=run('collabStats()');assert.equal(collab.reduce((s,r)=>s+r.count,0),39190);assert.ok(collab[1].mean/collab[0].mean<1.5,'Artist-credit duplicates must not inflate Collab to three times Solo');
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
console.log('Passed: de-duplicated Collab, nine z-scores, hierarchical filters, duration drill-down, consistent radar, month linking and empty populations.');
