const $=id=>document.getElementById(id),clone=x=>JSON.parse(JSON.stringify(x));
// Editorial palette: a fixed hue identifies each feature or genre across charts.
const theme={ink:'#0F172A',paper:'#FFFFFF',panel:'#FFFFFF',accent:'#3A98A8',spotify:'#10B981',grid:'#E2E8F0'};
const featureColors={danceability:'#D58AA0',energy:'#5686B3',valence:'#D1B638',acousticness:'#416E9B',speechiness:'#C7748F',instrumentalness:'#86AED5',liveness:'#E6CC69',loudness:'#638BB5',tempo:'#C58BA3'};
const genreColors={'pop':'#B3D2EF','canadian pop':'#BFE3EA','k-pop':'#D7C3ED','rap':'#8FA5CB','dance pop':'#FAE7A0','latin':'#F0BBCC','trap latino':'#CE8EA9'};
const genreLines={'pop':'#659ACC','canadian pop':'#4C99A8','k-pop':'#9172B5','rap':'#304F82','dance pop':'#BBA02B','latin':'#C35D7D','trap latino':'#963E66'};
const genreBoxColors={'pop':'#D5E6F7','canadian pop':'#D5EDF2','k-pop':'#E6D9F5','rap':'#B4C4DF','dance pop':'#FCF1C4','latin':'#F6D4E0','trap latino':'#E4BED0'};
const countryColors=['#5686B3','#C7748F'];
const colors=Object.values(featureColors);
const softInk=theme.ink,softGenreColors=genreColors,softPair=['#9FBFE0','#E4A3B3'];
const mapLevels=['#8ABDDD','#66A6D1','#498BBC','#3370A3','#235682','#173D65'];
const mapScale=mapLevels.flatMap((color,i)=>[[i/mapLevels.length,color],[(i+1)/mapLevels.length,color]]);
const diverge=[[0,'#E07052'],[.32,'#F4B5A4'],[.5,'#FAF9F6'],[.68,'#9FD1D9'],[1,'#3A98A8']];
const correlationScale=[[0,'#873953'],[.25,'#AE5676'],[.35,'#C77D97'],[.45,'#E2ADC0'],[.5,'#DBE2EA'],[.55,'#A5C7E6'],[.65,'#6497C1'],[.75,'#457BA8'],[1,'#254F79']];
const mixHex=(a,b,t)=>'#'+[1,3,5].map(i=>Math.round(parseInt(a.slice(i,i+2),16)*(1-t)+parseInt(b.slice(i,i+2),16)*t).toString(16).padStart(2,'0')).join('');
const featureScale=f=>{const hue=featureColors[f]||theme.accent;return [[0,theme.paper],[.35,mixHex(theme.paper,hue,.28)],[.7,mixHex(theme.paper,hue,.62)],[1,hue]]};
const bands=['Top 1–10','11–50','51–100','101–200'],mapFeatures=['valence','danceability','acousticness','energy'],boxFeatures=['energy','danceability','valence','tempo'];
const featureLabel=f=>f.charAt(0).toUpperCase()+f.slice(1),genreLabel=g=>g==='k-pop'?'K-Pop':g.split(' ').map(featureLabel).join(' ');
const boxLabel={energy:'Năng lượng',danceability:'Độ dễ nhảy',valence:'Sắc thái tích cực',tempo:'Nhịp độ'};
function chartTitle(key){
 if(key==='genre_box')return `${boxLabel[state.boxfeature]||featureLabel(state.boxfeature)} giữa các thể loại`;
 if(key==='artist_tree')return `Lượt nghe ghi nhận cho ${treeRows().length} nghệ sĩ dẫn đầu`;
 if(key==='radar'){const name=code=>{const value=current.allCountries.find(r=>r[0]===code)?.[1]||code;return ({Vietnam:'Việt Nam',Japan:'Nhật Bản'})[value]||value};return `So sánh âm thanh: ${name(state.country)} và ${name(state.compare)}`}
 if(key==='covid')return `${featureLabel(state.feature)} và tử vong COVID-19 theo tuần`;
 if(key==='decision_boundary')return `Không gian quyết định 2D: Log Streams vs ${state.boundary_y==='rank_first_week'?'Thứ hạng tuần đầu':featureLabel(state.boundary_y)}`;
 if(key==='confusion_heatmap')return `Ma trận nhầm lẫn tại ngưỡng τ = ${Number(state.threshold||0.79).toFixed(2)}`;
 if(key==='tradeoff_curve')return `Đánh đổi Precision – Recall theo ngưỡng quyết định (τ)`;
 if(key==='model_coefficients')return `Hệ số Logistic chuẩn hóa (β) và tỷ số chênh (OR) của 12 biến đầu vào`;
 return book.worksheets[key]||key;
}
const meta={danceability:'Độ dễ nhảy',energy:'Cường độ năng lượng',valence:'Sắc thái tích cực',acousticness:'Khả năng âm học mộc',speechiness:'Mức hiện diện lời nói',instrumentalness:'Khả năng không có giọng hát',liveness:'Dấu hiệu biểu diễn trực tiếp',loudness:'Âm lượng trung bình · dB',tempo:'Nhịp độ · BPM'};
const fi=f=>bundle.features.indexOf(f),tv=(t,f)=>t[5+fi(f)],cv=(r,f)=>r[(state.weight==='mean'?15:6)+fi(f)],unit=f=>f==='tempo'?'BPM':f==='loudness'?'dB':'0–1';
const mean=a=>{const v=a.filter(Number.isFinite);return v.length?v.reduce((s,x)=>s+x,0)/v.length:null},median=a=>{const v=a.filter(Number.isFinite).sort((a,b)=>a-b),i=Math.floor(v.length/2);return v.length?(v.length%2?v[i]:(v[i-1]+v[i])/2):null};
const fmt=(v,f=state.feature)=>Number.isFinite(v)?v.toFixed(f==='tempo'?1:f==='loudness'?2:3):'—',num=v=>Number.isFinite(v)?v.toLocaleString('vi-VN',{maximumFractionDigits:0}):'—',short=r=>bundle.region_short[r]||r;
const shortStreams=v=>!Number.isFinite(v)?'—':v>=1e9?(v/1e9).toLocaleString('vi-VN',{maximumFractionDigits:2})+' tỷ':(v/1e6).toLocaleString('vi-VN',{maximumFractionDigits:1})+' triệu';

let book=clone(bundle.workbook),position=0,state={},generation=0,detailMode='data',statusTimer,current;
function defaults(s={}){return {eda_tier:'',year:2021,fromyear:2017,toyear:2022,feature:'danceability',boxfeature:'danceability',region:'Tất cả',country:'VNM',compare:'JPN',weight:'weighted',genre:'',artist:'',band:'',collab:'',month:'',weeks:[],threshold:0.79,split:'test',boundary_y:'rank_first_week',...s}}
const point=()=>book.story_points[position],dash=()=>book.dashboards[point().dashboard_id],kind=()=>dash().id;

function validate(b){
  if(!b || !Array.isArray(b.story_points) || !b.dashboards) throw Error('Cần workbook hợp lệ');
  for(const p of b.story_points){
    const d=b.dashboards[p.dashboard_id];
    if(!d || !['overview','main_dashboard','hits','artists','geography','time','forecast'].includes(d.id)) throw Error('Dashboard không hợp lệ');
    p.saved_state=defaults(p.saved_state);
    d.worksheets=clone(bundle.workbook.dashboards[d.id]?.worksheets||[]);
  }
  b.worksheets=clone(bundle.workbook.worksheets);
  return b;
}

const storageKey='spotify-workbook-v12-main';
try{
  const old=localStorage.getItem(storageKey);
  if(old){
    const parsed=JSON.parse(old);
    if(parsed && parsed.story_points && parsed.story_points.length===bundle.workbook.story_points.length){
      book=validate(parsed);
    }
  }
}catch(e){console.warn(e.message)}

function options(el,items){el.replaceChildren();for(const [value,text] of items){const o=document.createElement('option');o.value=value;o.textContent=text;el.append(o)}}
for(const id of ['fromyear','toyear'])options($(id),Array.from({length:6},(_,i)=>[2017+i,2017+i]));
options($('genre'),[['','Tất cả thể loại'],...bundle.genres.map(g=>[g,genreLabel(g)])]);
const regions=[...new Set(bundle.countries.map(r=>r[3]))].sort();options($('region'),[['Tất cả','Tất cả khu vực'],...regions.map(r=>[r,short(r)])]);
options($('month'),[['','Cả 12 tháng'],...Array.from({length:12},(_,i)=>[i+1,'Tháng '+(i+1)])]);
function notify(text){clearTimeout(statusTimer);$('status').textContent=text;if(text)statusTimer=setTimeout(()=>$('status').textContent='',4500)}
function download(name,data,type){const a=document.createElement('a'),url=URL.createObjectURL(new Blob([data],{type}));a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1500)}

function nav(){
  const host=$('navigator');host.replaceChildren();
  book.story_points.forEach((p,i)=>{
    const b=document.createElement('button'),label=document.createElement('span');
    b.className='point'+(i===position?' active':'');
    label.textContent=book.dashboards[p.dashboard_id].title;
    b.title=p.caption;
    b.append(label);
    b.onclick=()=>go(i);
    host.append(b);
  });
  $('prev').disabled=position===0;
  $('next').disabled=$('explore-next').disabled=position===book.story_points.length-1;
}

function go(i){
  position=Math.max(0,Math.min(book.story_points.length-1,i));
  state=defaults(clone(point().saved_state));
  notify('');
  render();
}

function buildModel(){
  const artistSet=state.artist?new Set(bundle.artists[state.artist]?.[2]||[]):null;
  const eligible=new Set(bundle.tracks.flatMap((t,i)=>(!state.genre||t[2]===state.genre)&&(!artistSet||artistSet.has(i))&&(!state.collab||Number(t[3]>1)===Number(state.collab))?[i]:[]));
  const context=bundle.global_rows.filter(r=>eligible.has(r[0])&&r[1]>=state.fromyear&&r[1]<=state.toyear&&(!state.month||r[2]===Number(state.month)));
  const rows=context.filter(r=>state.band===''||r[3]===Number(state.band));
  const selectedIndices=new Set(rows.map(r=>r[0]));
  const tracks=bundle.tracks.flatMap((t,i)=>selectedIndices.has(i)?[{t,i}]:[]);
  const countries=bundle.countries.filter(r=>r[2]===state.year&&(state.region==='Tất cả'||r[3]===state.region));
  const allCountries=bundle.countries.filter(r=>r[2]===state.year);
  const weeks=bundle.weekly.filter(r=>Number(r[0].slice(0,4))>=state.fromyear&&Number(r[0].slice(0,4))<=state.toyear);
  const covid=weeks.filter(r=>Number.isFinite(r[13])&&(!state.month||Number(r[0].slice(5,7))===Number(state.month)));
  const analysis=bundle.analysis.filter(r=>eligible.has(r[0])&&Number(r[1].slice(0,4))>=state.fromyear&&Number(r[1].slice(0,4))<=state.toyear);
  
  // Forecast data processing
  const fc = bundle.forecast || {};
  const allFcSamples = fc.samples || [];
  const fcSamples = allFcSamples.filter(r => state.split === 'all' || r[9] === state.split);
  const tau = Number(state.threshold) || 0.79;
  
  let tp = 0, fp = 0, fn = 0, tn = 0;
  for (let i = 0; i < fcSamples.length; i++) {
    const s = fcSamples[i];
    const yTrue = s[8];
    const p = s[7];
    const pred = p >= tau ? 1 : 0;
    if (yTrue === 1 && pred === 1) tp++;
    else if (yTrue === 0 && pred === 1) fp++;
    else if (yTrue === 1 && pred === 0) fn++;
    else tn++;
  }
  const total = fcSamples.length || 1;
  const acc = (tp + tn) / total;
  const prec = (tp + fp) > 0 ? tp / (tp + fp) : 0;
  const rec = (tp + fn) > 0 ? tp / (tp + fn) : 0;
  const f1 = (prec + rec) > 0 ? (2 * prec * rec) / (prec + rec) : 0;
  const fcMetrics = { tp, fp, fn, tn, acc, prec, rec, f1, n: fcSamples.length };
  
  const fcCurves = [];
  for (let t = 0.10; t <= 0.9001; t += 0.01) {
    const th = Math.round(t * 100) / 100;
    let c_tp = 0, c_fp = 0, c_fn = 0, c_tn = 0;
    for (let i = 0; i < fcSamples.length; i++) {
      const s = fcSamples[i];
      const y = s[8];
      const p = s[7];
      if (y === 1) {
        if (p >= th) c_tp++; else c_fn++;
      } else {
        if (p >= th) c_fp++; else c_tn++;
      }
    }
    const c_prec = (c_tp + c_fp) > 0 ? c_tp / (c_tp + c_fp) : 1;
    const c_rec = (c_tp + c_fn) > 0 ? c_tp / (c_tp + c_fn) : 0;
    const c_f1 = (c_prec + c_rec) > 0 ? (2 * c_prec * c_rec) / (c_prec + c_rec) : 0;
    fcCurves.push({ th, prec: c_prec, rec: c_rec, f1: c_f1, tp: c_tp, fp: c_fp, fn: c_fn, tn: c_tn });
  }
  
  const sub50 = fcSamples.filter(r => r[4] > 50);
  const sub50_pos = sub50.filter(r => r[8] === 1).length;
  const sub50_pred_pos = sub50.filter(r => r[7] >= tau).length;
  const fcSub50 = { count: sub50.length, pos: sub50_pos, pred_pos: sub50_pred_pos };

  return {tracks,context,rows,countries,allCountries,weeks,covid,analysis,fcSamples,fcMetrics,fcCurves,fcSub50};
}

function controls(){
  const k=kind();
  $('hit-flow').hidden=true;
  const visible={
    overview:[],
    main_dashboard:['year','country','compare','feature'],
    hits:['fromyear','toyear','genre','band','feature'],
    artists:['fromyear','toyear','genre','feature'],
    geography:['year','weight','region','country','compare','feature'],
    time:['fromyear','toyear','month','feature'],
    forecast:['split','boundary_y']
  }[k] || [];
  
  document.querySelectorAll('.filters label').forEach(el=>{
    const sel = el.querySelector('select')?.id;
    if(sel) {
      const show = visible.includes(sel);
      el.hidden = !show;
      el.style.display = show ? '' : 'none';
    }
  });
  document.querySelectorAll('.filters .forecast-tau-slider').forEach(el => {
    const isForecast = (k === 'forecast');
    el.hidden = !isForecast;
    el.style.display = isForecast ? 'flex' : 'none';
  });

  if(k==='overview'){
    state.genre='';state.artist='';state.band='';state.collab='';state.month='';state.weeks=[];
  } else if(k==='main_dashboard'){
    state.genre='';state.artist='';state.band='';state.collab='';state.month='';state.weeks=[];
  } else if(k==='hits'){
    state.artist='';state.collab='';state.month='';state.weeks=[];
  } else if(k==='artists'){
    state.artist='';state.collab='';state.band='';state.month='';state.weeks=[];
  } else if(k==='geography'){
    state.genre='';state.artist='';state.band='';state.collab='';state.month='';state.weeks=[];
  } else if(k==='time'){
    state.genre='';state.artist='';state.band='';state.collab='';
  } else if(k==='forecast'){
    $('tau-slider').value = state.threshold;
    $('tau-val').textContent = 'τ = ' + Number(state.threshold).toFixed(2);
    $('split').value = state.split;
    $('boundary_y').value = state.boundary_y;
    const splitLabel = {test: 'Tập Test (941 bài)', validation: 'Tập Validation (840 bài)', train: 'Tập Train (2,625 bài)', all: 'Toàn bộ mẫu (4,406 bài)'}[state.split] || 'Tập Test';
    $('scope').textContent = `${splitLabel} · Ngưỡng τ = ${Number(state.threshold).toFixed(2)} · F1 = ${(current?.fcMetrics?.f1*100 || 62.6).toFixed(1)}%`;
    return;
  }
  
  const genres=k==='hits'?['pop','latin','k-pop','rap','dance pop']:bundle.genres;
  if(!genres.includes(state.genre))state.genre='';
  options($('genre'),[['','Tất cả thể loại'],...genres.map(g=>[g,genreLabel(g)])]);
  $('genre').closest('label').firstChild.nodeValue=k==='artists'?'Thể loại → nghệ sĩ':'Thể loại';
  $('band').closest('label').classList.toggle('wide',k==='hits');
  $('collab').closest('label').classList.toggle('wide',k==='artists');
  const choices=k==='overview'?(bundle.eda?.features||bundle.features):['geography','main_dashboard'].includes(k)?mapFeatures:bundle.features;
  options($('feature'),choices.map(f=>[f,f==='duration_min'?'Duration · phút':featureLabel(f)]));
  if(!choices.includes(state.feature))state.feature=choices[0];
  const all=bundle.countries.filter(r=>r[2]===state.year),local=all.filter(r=>state.region==='Tất cả'||r[3]===state.region);
  if(!local.some(r=>r[0]===state.country))state.country=local[0]?.[0]||'';
  if(!all.some(r=>r[0]===state.compare))state.compare=all[0]?.[0]||'';
  options($('country'),local.slice().sort((a,b)=>a[1].localeCompare(b[1])).map(r=>[r[0],r[1]]));
  options($('compare'),all.slice().sort((a,b)=>a[1].localeCompare(b[1])).map(r=>[r[0],r[1]]));
  const artists=Object.entries(bundle.artists).filter(([id,a])=>!state.genre||a[1]===state.genre).sort((a,b)=>a[1][0].localeCompare(b[1][0]));
  if(state.artist&&!artists.some(([id])=>id===state.artist))state.artist='';
  options($('artist'),[['','Tất cả nghệ sĩ'],...artists.map(([id,a])=>[id,a[0]])]);
  for(const id of ['year','fromyear','toyear','genre','artist','band','collab','region','country','compare','weight','month','feature']){
    const el=$(id);
    if(el)el.value=state[id];
  }
  $('scope').textContent=k==='overview'?'Toàn bộ mẫu chart & Train Global':k==='main_dashboard'?'Toàn cảnh 4 trụ cột cốt lõi':k==='hits'?`${state.fromyear}–${state.toyear} · BXH Global`:k==='artists'?`${state.fromyear}–${state.toyear} · Phân tích nghệ sĩ & collab`:k==='geography'?`${local.length} quốc gia · ${state.year} · ${state.weight==='weighted'?'theo stream':'trung bình thường'}`:`${state.fromyear}–${state.toyear} · ${current?.covid?.length||0} tuần COVID`;
}

function hitStats(rows=current.context){const accum=Array.from({length:4},()=>bundle.features.map(()=>({n:0,s:0,q:0})));for(const r of rows){const t=bundle.tracks[r[0]];bundle.features.forEach((f,j)=>{const x=tv(t,f);if(Number.isFinite(x)){const a=accum[r[3]][j];a.n+=r[4];a.s+=x*r[4];a.q+=x*x*r[4]}})}
  const baseline=bundle.features.map((_,j)=>{const n=accum.reduce((s,a)=>s+a[j].n,0),s=accum.reduce((s,a)=>s+a[j].s,0),q=accum.reduce((s,a)=>s+a[j].q,0),m=n?s/n:null;return {mean:m,std:n?Math.sqrt(Math.max(0,q/n-m*m)):null,n}});
  const raw=accum.map(a=>a.map(x=>x.n?x.s/x.n:null));const z=raw.map(a=>a.map((m,j)=>m!==null&&baseline[j].std>0?(m-baseline[j].mean)/baseline[j].std:null));return {raw,z,baseline,counts:accum.map(a=>a[0].n)};
}

function collabStats(){
  if(kind()==='artists')return [0,1].map(c=>{const rows=current.analysis.filter(r=>Number(bundle.tracks[r[0]][3]>1)===c),values=rows.map(r=>r[3]);return {type:c?'Collab':'Solo',count:rows.length,charted:rows.length,median:median(values),mean:mean(values)}});
  const streamsByTrack=new Map();
  for(const r of current.rows)streamsByTrack.set(r[0],(streamsByTrack.get(r[0])||0)+r[5]);
  return [0,1].map(c=>{
    const ts=current.tracks.filter(({t})=>Number(t[3]>1)===c);
    const streamValues=ts.map(({i})=>streamsByTrack.get(i)||0).filter(v=>v>0);
    return {type:c?'Collab':'Solo',count:ts.length,median:median(streamValues),mean:mean(streamValues),charted:streamValues.length};
  });
}

function treeRows(){const sums=new Map();for(const r of bundle.credits){const a=bundle.artists[r[0]];if(r[1]<state.fromyear||r[1]>state.toyear||state.genre&&a[1]!==state.genre||state.artist&&r[0]!==state.artist||state.band!==''&&r[3]!==+state.band||state.collab!==''&&r[4]!==+state.collab||state.month&&r[2]!==+state.month)continue;sums.set(r[0],(sums.get(r[0])||0)+r[5])}return [...sums].sort((a,b)=>b[1]-a[1]).slice(0,80)}

function figure(key){
 const f=state.feature,fig={data:[],layout:{}};
 if(key==='hit_heatmap'){
   const a=hitStats();
   fig.data=[{type:'heatmap',x:bundle.features,y:bands,z:a.z,text:a.z.map(r=>r.map(v=>v===null?'':Math.abs(v)<.005?'<span style="color:#64748B">0.00</span>':Math.abs(v)>=.11?`<span style="color:#FFFFFF">${v>0?'+':''}${v.toFixed(2)}</span>`:`<span style="color:#1E293B">${v>0?'+':''}${v.toFixed(2)}</span>`)),texttemplate:'%{text}',textfont:{size:14,family:"'Segoe UI', sans-serif"},customdata:a.raw,colorscale:diverge,zmid:0,zmin:-.15,zmax:.15,colorbar:{thickness:12,len:.75,title:{text:'Độ lệch chuẩn hóa',font:{size:12,family:"'Segoe UI', sans-serif"}},tickvals:[-.15,0,.15],ticktext:['Thấp hơn TB','Bằng TB','Cao hơn TB'],tickfont:{size:11,family:"'Segoe UI', sans-serif"}},hovertemplate:'%{y}<br>%{x}<br>Giá trị thực tế: %{customdata:.2f}<br>Độ lệch chuẩn hóa: %{z:+.2f}<extra></extra>'}];
   fig.layout={margin:{l:85,r:20,t:12,b:72},xaxis:{tickangle:-28,tickfont:{size:13,family:"'Segoe UI', sans-serif"}},yaxis:{autorange:'reversed',tickfont:{size:13,family:"'Segoe UI', sans-serif"}},shapes:[{type:'rect',xref:'paper',yref:'paper',x0:fi(f)/bundle.features.length,x1:(fi(f)+1)/bundle.features.length,y0:0,y1:1,line:{color:'#3A98A8',width:2}}]};
   if(state.band!=='')fig.layout.shapes.push({type:'rect',xref:'paper',yref:'y',x0:0,x1:1,y0:+state.band-.48,y1:+state.band+.48,line:{color:theme.accent,width:2}});
 }
 else if(key==='genre_box'){
   const feature=state.boxfeature,genres=['pop','latin','k-pop','rap','dance pop'];
   fig.data=genres.map(g=>{const ts=current.tracks.filter(({t})=>t[2]===g&&Number.isFinite(tv(t,feature)));return {type:'box',name:g,y:ts.map(({t})=>tv(t,feature)),customdata:ts.map(({t})=>t[1]),boxmean:true,boxpoints:'outliers',fillcolor:genreBoxColors[g],marker:{color:genreLines[g],size:5},line:{color:genreLines[g],width:2.2},hovertemplate:genreLabel(g)+'<br>'+featureLabel(feature)+': %{y:.4f}<br>%{customdata}<br>'+ts.length+' bài trong nhóm<extra></extra>'}}).filter(t=>t.y.length);
   fig.layout={margin:{l:44,r:12,t:14,b:42},showlegend:false,xaxis:{categoryorder:'array',categoryarray:genres,tickvals:genres,ticktext:['Pop','Latin','K-Pop','Rap','Dance Pop'],tickfont:{size:13,family:"'Segoe UI', sans-serif"}},yaxis:{title:{text:unit(feature),font:{size:13,family:"'Segoe UI', sans-serif"}},tickfont:{size:13,family:"'Segoe UI', sans-serif"}}};
 }
 else if(key==='artist_tree'){
   const rows=treeRows(),sums=new Map(),named=new Set(),perGenre=new Map();
   for(const [id,v] of rows){const g=bundle.artists[id][1];sums.set(g,(sums.get(g)||0)+v);const count=perGenre.get(g)||0;if(count<(g==='pop'?5:2))named.add(id);perGenre.set(g,count+1)}
   const ids=['root'],labels=['Top '+rows.length+' nghệ sĩ'],parents=[''],values=[rows.reduce((s,[id,v])=>s+v,0)],custom=[['','','']];
   for(const [g,v] of sums){ids.push('g:'+g);labels.push(g);parents.push('root');values.push(v);custom.push(['',g,''])}
   for(const [id,v] of rows){const a=bundle.artists[id];ids.push(id);labels.push(a[0]);parents.push('g:'+a[1]);values.push(v);custom.push([id,a[1],v])}
   const text=labels.map((label,i)=>i<=sums.size||named.has(ids[i])?label:'');
   fig.data=[{type:'treemap',ids,labels,parents,values,text,branchvalues:'total',customdata:custom,marker:{colors:custom.map(c=>genreColors[c[1]]||'#CBD5E1'),line:{color:'#FFFFFF',width:1.5}},textinfo:'label',textfont:{size:14,color:'#1E293B',family:"'Segoe UI', sans-serif"},pathbar:{visible:true,textfont:{size:12,color:'#475569',family:"'Segoe UI', sans-serif"}},hovertemplate:'<b>%{label}</b><br>Stream ghi công: %{value:,.0f}<br>Tỷ trọng trong nhánh: %{percentParent:.1%}<extra></extra>',tiling:{pad:2}}];
   fig.layout={margin:{l:2,r:2,t:3,b:2},uniformtext:{minsize:12,mode:'hide'}};
 }
 else if(key==='collab'){
   const a=collabStats();
   fig.data=[
     {type:'pie',labels:a.map(r=>r.type),values:a.map(r=>r.count),hole:.65,domain:{x:[0,.43],y:[.13,.9]},marker:{colors:softPair,line:{color:'#FFFFFF',width:2}},textinfo:'percent',textfont:{size:13,color:'#FFFFFF',family:"'Segoe UI', sans-serif"},hovertemplate:'%{label}<br>%{value} bài vào BXH Global<br>%{percent}<extra></extra>',showlegend:false},
     {type:'bar',x:a.map(r=>r.type),y:a.map(r=>r.median===null?null:r.median/1e6),text:a.map(r=>r.median===null?'':(r.median/1e6).toFixed(1)+' Tr'),textposition:'outside',cliponaxis:false,xaxis:'x',yaxis:'y',marker:{color:softPair,line:{color:softPair,width:1}},textfont:{size:13,family:"'Segoe UI', sans-serif"},customdata:a.map(r=>[r.charted,r.mean===null?null:r.mean/1e6]),showlegend:false,hovertemplate:'%{x}<br>Trung vị Global: %{y:.2f} triệu/bài<br>Trung bình Global: %{customdata[1]:.2f} triệu/bài<br>%{customdata[0]} bài có stream<extra></extra>'}
   ];
   fig.layout={margin:{l:10,r:12,t:28,b:32},xaxis:{domain:[.57,1],tickfont:{size:13,family:"'Segoe UI', sans-serif"}},yaxis:{domain:[.15,.9],title:{text:'Triệu/bài',font:{size:13,family:"'Segoe UI', sans-serif"}},tickfont:{size:13,family:"'Segoe UI', sans-serif"},rangemode:'tozero'},annotations:[{xref:'paper',yref:'paper',x:.2,y:1.05,text:'Số bài',showarrow:false,font:{size:13,family:"'Segoe UI', sans-serif"}},{xref:'paper',yref:'paper',x:.82,y:1.05,text:'Stream trung vị',showarrow:false,font:{size:13,family:"'Segoe UI', sans-serif"}}]};
 }
 else if(key==='duration'){
   const conditional=state.genre||state.artist||state.band!==''||state.collab!=='';
   let points;
   if(conditional){
     const bins=new Map();
     for(const r of current.rows){
       const dur=bundle.tracks[r[0]][14];if(!Number.isFinite(dur))continue;
       const k=r[1]+'-'+String(r[2]).padStart(2,'0');
       const b=bins.get(k)||[0,0];b[0]+=dur*r[5];b[1]+=r[5];bins.set(k,b);
     }
     points=[...bins].sort((a,b)=>a[0].localeCompare(b[0])).map(([d,a])=>[d+'-01',a[1]?a[0]/a[1]/1000:null]);
   } else {
     points=bundle.weekly.filter(r=>{const year=Number(r[0].slice(0,4));return year>=state.fromyear&&year<=state.toyear}).map(r=>[r[0],r[3]/1000]);
   }
   const smooth=points.map((r,i)=>mean(points.slice(Math.max(0,i-3),i+1).map(x=>x[1])));
   fig.data=[
     {type:'scatter',mode:'lines',name:conditional?'Trung bình tháng':'Trung bình tuần',x:points.map(r=>r[0]),y:points.map(r=>r[1]),line:{color:'#CBD5E1',width:1.5},hovertemplate:'%{x}<br>%{y:.1f} giây<extra></extra>'},
     {type:'scatter',mode:'lines',name:conditional?'TB 4 tháng':'TB 4 tuần',x:points.map(r=>r[0]),y:smooth,line:{color:'#3B82F6',width:3.0},hovertemplate:'%{x}<br>%{y:.1f} giây<extra></extra>'}
   ];
   fig.layout={margin:{l:48,r:12,t:28,b:36},xaxis:{tickfont:{size:13,family:"'Segoe UI', sans-serif"}},yaxis:{title:{text:'Giây',font:{size:13,family:"'Segoe UI', sans-serif"}},tickfont:{size:13,family:"'Segoe UI', sans-serif"}},hovermode:'x unified'};
 }
 else if(key==='map'){
   const rows=current.countries,all=current.allCountries.map(r=>cv(r,f)).filter(Number.isFinite);
   fig.data=[{type:'choropleth',locations:rows.map(r=>r[0]),z:rows.map(r=>cv(r,f)),customdata:rows.map(r=>[r[1],r[3],r[5]]),colorscale:[[0,'#FCE4EC'],[.2,'#F8BBD0'],[.4,'#F06292'],[.6,'#E2738E'],[.8,'#880E4F'],[1,'#4A148C']],zmin:Math.min(...all),zmax:Math.max(...all),marker:{line:{color:theme.panel,width:.5}},colorbar:{thickness:8,len:.65,title:{text:f}},hovertemplate:'<b>%{customdata[0]}</b><br>'+f+': %{z:.4f}<br>%{customdata[1]}<br>%{customdata[2]} tuần<extra></extra>'}];
   for(const [code,color] of [[state.country,countryColors[0]],[state.compare,countryColors[1]]]){
     if(rows.some(r=>r[0]===code)){
       fig.data.push({type:'choropleth',locations:[code],z:[1],showscale:false,colorscale:[[0,color],[1,color]],marker:{line:{color:theme.ink,width:1.5}},customdata:[[current.allCountries.find(r=>r[0]===code)?.[1],cv(current.allCountries.find(r=>r[0]===code),f)]],hovertemplate:'%{customdata[0]}<br>'+f+': %{customdata[1]:.4f}<extra></extra>'});
     }
   }
   fig.layout={margin:{l:0,r:10,t:5,b:0},geo:{projection:{type:'natural earth'},showframe:false,showland:true,landcolor:'#E8E5DE',showcoastlines:true,coastlinecolor:'#C7C6BF',bgcolor:theme.panel}};
 }
 else if(key==='radar'){
   const features=['acousticness','danceability','energy','valence','speechiness','liveness'];
   for(const [i,code] of [state.country,state.compare].entries()){
     const row=current.allCountries.find(r=>r[0]===code);
     if(!row)continue;
     const values=features.map(feat=>cv(row,feat));
     fig.data.push({type:'scatterpolar',r:[...values,values[0]],theta:[...features,features[0]],name:row[1],fill:'toself',line:{color:countryColors[i],width:2},fillcolor:i?'rgba(83,109,254,0.22)':'rgba(226,115,142,0.22)',customdata:[...features,features[0]],hovertemplate:row[1]+'<br>%{theta}: %{r:.4f}<extra></extra>'});
   }
   fig.layout={margin:{l:65,r:65,t:40,b:35},polar:{radialaxis:{range:[0,1],tickfont:{size:9}},angularaxis:{tickfont:{size:10}}},legend:{orientation:'h',x:.3,y:1.12}};
 }
 else if(key==='seasonal'){
   fig.data=['danceability','acousticness'].map(feat=>({type:'bar',x:Array.from({length:12},(_,i)=>i+1),y:Array.from({length:12},(_,m)=>mean(current.weeks.filter(r=>+r[0].slice(5,7)===m+1).map(r=>r[4+fi(feat)]))),name:feat,customdata:Array.from({length:12},(_,m)=>current.weeks.filter(r=>+r[0].slice(5,7)===m+1).length),marker:{color:featureColors[feat],opacity:Array.from({length:12},(_,m)=>!state.month||+state.month===m+1?1:.25)},hovertemplate:'Tháng %{x}<br>'+feat+': %{y:.4f}<br>%{customdata} tuần<extra></extra>'}));
   fig.layout={barmode:'group',margin:{l:42,r:9,t:30,b:35},xaxis:{dtick:1,title:{text:'Tháng trong năm'}},yaxis:{title:{text:'0–1'},range:[0,1]}};
 }
 else if(key==='covid'){
   const rows=current.covid,x=[],y=[];
   let prev=null;
   for(const r of rows){
     if(prev&&new Date(r[0])-new Date(prev)>8*86400000){x.push(r[0]);y.push(null)}
     x.push(r[0]);y.push(r[4+fi(f)]);prev=r[0];
   }
   fig.data=[
     {type:'bar',x:rows.map(r=>r[0]),y:rows.map(r=>r[13]),name:'Tử vong / tuần',yaxis:'y2',marker:{color:'#C9BDB580'},hovertemplate:'%{x}<br>%{y:,.0f} ca<extra></extra>'},
     {type:'scatter',mode:'lines',x,y,name:f,line:{color:featureColors[f],width:2.6},hovertemplate:'%{x}<br>'+f+': %{y:.4f}<extra></extra>'}
   ];
   fig.layout={margin:{l:48,r:50,t:30,b:40},hovermode:'x unified',yaxis:{title:{text:f+' · '+unit(f)}},yaxis2:{overlaying:'y',side:'right',title:{text:'Tử vong'},showgrid:false,rangemode:'tozero'},shapes:state.weeks.map(w=>({type:'line',xref:'x',yref:'paper',x0:w,x1:w,y0:0,y1:1,line:{color:theme.accent,width:2,dash:'dot'}}))};
 }
 else if(key==='decision_boundary'){
   const samples=current.fcSamples||[],tau=Number(state.threshold)||0.79,yFeat=state.boundary_y||'rank_first_week';
   const yIdx={rank_first_week:4,danceability:10,energy:11,valence:12,loudness:13,acousticness:14,speechiness:15,tempo:16}[yFeat]||4;
   const yName={rank_first_week:'Thứ hạng tuần 1',danceability:'Danceability',energy:'Energy',valence:'Valence',loudness:'Loudness (dB)',acousticness:'Acousticness',speechiness:'Speechiness',tempo:'Tempo (BPM)'}[yFeat]||yFeat;
   
   const tp_pts=[],tn_pts=[],fp_pts=[],fn_pts=[];
   for(const s of samples){
     const yTrue=s[8],p=s[7],pred=p>=tau?1:0;
     const pt={x:s[6],y:s[yIdx],custom:[s[1],s[2],s[4],s[5],p,yTrue?'Đạt Top 50':'Không đạt',pred?'Dự báo Hit':'Dự báo Không đạt',pred===yTrue?(yTrue?'TP (Đúng Hit)':'TN (Đúng Không đạt)'):(pred?'FP (Dương giả)':'FN (Âm giả)')]};
     if(yTrue===1&&pred===1)tp_pts.push(pt);
     else if(yTrue===0&&pred===0)tn_pts.push(pt);
     else if(yTrue===0&&pred===1)fp_pts.push(pt);
     else fn_pts.push(pt);
   }
   
   fig.data=[
     {type:'scatter',mode:'markers',name:`TN · Đúng 0 (${tn_pts.length})`,x:tn_pts.map(p=>p.x),y:tn_pts.map(p=>p.y),marker:{color:'#94A3B8',size:5.5,opacity:0.65},customdata:tn_pts.map(p=>p.custom),hovertemplate:'<b>%{customdata[0]}</b> · %{customdata[1]}<br>Log streams: %{x:.2f} (Gốc: %{customdata[3]:,})<br>'+yName+': %{y}<br>Xác suất p̂ = <b>%{customdata[4]:.1%}</b><br>Thực tế: %{customdata[5]} | Dự báo: %{customdata[6]}<br><b>%{customdata[7]}</b><extra></extra>'},
     {type:'scatter',mode:'markers',name:`FP · Dương giả (${fp_pts.length})`,x:fp_pts.map(p=>p.x),y:fp_pts.map(p=>p.y),marker:{color:'#EF4444',size:7.5,opacity:0.85,symbol:'x'},customdata:fp_pts.map(p=>p.custom),hovertemplate:'<b>%{customdata[0]}</b> · %{customdata[1]}<br>Log streams: %{x:.2f} (Gốc: %{customdata[3]:,})<br>'+yName+': %{y}<br>Xác suất p̂ = <b>%{customdata[4]:.1%}</b><br>Thực tế: %{customdata[5]} | Dự báo: %{customdata[6]}<br><b><span style="color:#DC2626;">%{customdata[7]}</span></b><extra></extra>'},
     {type:'scatter',mode:'markers',name:`FN · Âm giả (${fn_pts.length})`,x:fn_pts.map(p=>p.x),y:fn_pts.map(p=>p.y),marker:{color:'#F59E0B',size:7.5,opacity:0.85,symbol:'triangle-up'},customdata:fn_pts.map(p=>p.custom),hovertemplate:'<b>%{customdata[0]}</b> · %{customdata[1]}<br>Log streams: %{x:.2f} (Gốc: %{customdata[3]:,})<br>'+yName+': %{y}<br>Xác suất p̂ = <b>%{customdata[4]:.1%}</b><br>Thực tế: %{customdata[5]} | Dự báo: %{customdata[6]}<br><b><span style="color:#D97706;">%{customdata[7]}</span></b><extra></extra>'},
     {type:'scatter',mode:'markers',name:`TP · Đúng 1 (${tp_pts.length})`,x:tp_pts.map(p=>p.x),y:tp_pts.map(p=>p.y),marker:{color:'#10B981',size:7.5,opacity:0.9},customdata:tp_pts.map(p=>p.custom),hovertemplate:'<b>%{customdata[0]}</b> · %{customdata[1]}<br>Log streams: %{x:.2f} (Gốc: %{customdata[3]:,})<br>'+yName+': %{y}<br>Xác suất p̂ = <b>%{customdata[4]:.1%}</b><br>Thực tế: %{customdata[5]} | Dự báo: %{customdata[6]}<br><b><span style="color:#059669;">%{customdata[7]}</span></b><extra></extra>'}
   ];
   
   const fc=bundle.forecast;
   if(fc&&fc.coefficients){
     const featNames=fc.features,s_mean=fc.scaler_mean,s_std=fc.scaler_std,coef=fc.coefficients,intercept=fc.intercept;
     const idx_streams=featNames.indexOf('log_streams_first_week'),idx_y=featNames.indexOf(yFeat);
     if(idx_streams>=0&&idx_y>=0){
       const b_streams=coef[idx_streams],b_y=coef[idx_y],mu_s=s_mean[idx_streams],std_s=s_std[idx_streams],mu_y=s_mean[idx_y],std_y=s_std[idx_y];
       const logit_tau=Math.log(tau/(1-tau));
       const x_line=[14.5,16.0,18.5];
       const y_line=x_line.map(x_val=>{const z_s=(x_val-mu_s)/std_s*b_streams;return mu_y+((logit_tau-intercept-z_s)/b_y)*std_y});
       fig.data.push({type:'scatter',mode:'lines',name:`Ranh giới p̂ = ${tau.toFixed(2)}`,x:x_line,y:y_line,line:{color:'#1E40AF',width:2.5,dash:'solid'},hoverinfo:'none'});
     }
   }
   fig.layout={margin:{l:50,r:15,t:18,b:42},xaxis:{title:{text:'Lượt nghe tuần đầu (Log streams)',font:{size:12}},tickfont:{size:11}},yaxis:{title:{text:yName,font:{size:12}},tickfont:{size:11},autorange:yFeat==='rank_first_week'?'reversed':true},legend:{orientation:'h',x:0,y:1.15,font:{size:11}}};
 }
 else if(key==='confusion_heatmap'){
   const m=current.fcMetrics||{tp:128,fp:67,fn:86,tn:660,n:941};
   const {tp,fp,fn,tn,n}=m;
   const text=[
     [
       `<b>TN (Đúng Không đạt)</b><br><span style="font-size:16px;font-weight:700;color:#065F46;">${tn}</span><br><b>${(tn/n*100).toFixed(1)}%</b> · <span style="font-size:10px;color:#047857;">Dự báo: 0 | Thực tế: 0</span>`,
       `<b>FP (Dương tính giả)</b><br><span style="font-size:16px;font-weight:700;color:#991B1B;">${fp}</span><br><b>${(fp/n*100).toFixed(1)}%</b> · <span style="font-size:10px;color:#B91C1C;">Dự báo: 1 | Thực tế: 0</span>`
     ],
     [
       `<b>FN (Âm tính giả)</b><br><span style="font-size:16px;font-weight:700;color:#991B1B;">${fn}</span><br><b>${(fn/n*100).toFixed(1)}%</b> · <span style="font-size:10px;color:#B91C1C;">Dự báo: 0 | Thực tế: 1</span>`,
       `<b>TP (Đúng Hit Top 50)</b><br><span style="font-size:16px;font-weight:700;color:#065F46;">${tp}</span><br><b>${(tp/n*100).toFixed(1)}%</b> · <span style="font-size:10px;color:#047857;">Dự báo: 1 | Thực tế: 1</span>`
     ]
   ];
   fig.data=[{type:'heatmap',x:['Dự báo 0 (Không đạt)','Dự báo 1 (Đạt Top 50)'],y:['Thực tế 0 (Không đạt)','Thực tế 1 (Đạt Top 50)'],z:[[1,-1],[-1,1]],text:text,texttemplate:'%{text}',textfont:{size:13,family:"'Segoe UI', sans-serif"},colorscale:[[0,'#FEE2E2'],[0.49,'#FECACA'],[0.5,'#F8FAFC'],[0.51,'#D1FAE5'],[1,'#A7F3D0']],zmin:-1,zmax:1,showscale:false,hoverinfo:'none'}];
   fig.layout={margin:{l:140,r:20,t:25,b:55},xaxis:{side:'bottom',tickfont:{size:12,family:"'Segoe UI', sans-serif"}},yaxis:{autorange:'reversed',tickfont:{size:12,family:"'Segoe UI', sans-serif"}}};
 }
 else if(key==='tradeoff_curve'){
   const curves=current.fcCurves||[],tau=Number(state.threshold)||0.79,m=current.fcMetrics||{prec:0.656,rec:0.598,f1:0.626};
   fig.data=[
     {type:'scatter',mode:'lines',name:'Precision (Độ chuẩn xác)',x:curves.map(c=>c.th),y:curves.map(c=>c.prec),line:{color:'#2563EB',width:2.8},hovertemplate:'Ngưỡng τ = %{x:.2f}<br>Precision: <b>%{y:.1%}</b><extra></extra>'},
     {type:'scatter',mode:'lines',name:'Recall (Độ bao phủ / Nhạy)',x:curves.map(c=>c.th),y:curves.map(c=>c.rec),line:{color:'#DC2626',width:2.8},hovertemplate:'Ngưỡng τ = %{x:.2f}<br>Recall: <b>%{y:.1%}</b><extra></extra>'},
     {type:'scatter',mode:'lines',name:'F1-Score (Cân bằng)',x:curves.map(c=>c.th),y:curves.map(c=>c.f1),line:{color:'#7C3AED',width:2.2,dash:'dot'},hovertemplate:'Ngưỡng τ = %{x:.2f}<br>F1-Score: <b>%{y:.1%}</b><extra></extra>'}
   ];
   fig.layout={margin:{l:48,r:15,t:20,b:42},xaxis:{title:{text:'Ngưỡng quyết định (Threshold τ)',font:{size:12}},tickfont:{size:11},range:[0.10,0.90]},yaxis:{title:{text:'Chỉ số (0–1)',font:{size:12}},tickfont:{size:11},range:[0,1.05]},legend:{orientation:'h',x:0,y:1.15,font:{size:11}},shapes:[{type:'line',xref:'x',yref:'paper',x0:tau,x1:tau,y0:0,y1:1,line:{color:'#0F172A',width:2,dash:'dash'}}],annotations:[{xref:'x',yref:'paper',x:tau,y:0.95,xanchor:tau>0.6?'right':'left',xshift:tau>0.6?-8:8,text:`<b>τ = ${tau.toFixed(2)}</b><br>P = ${(m.prec*100).toFixed(1)}%<br>R = ${(m.rec*100).toFixed(1)}%<br>F1 = ${(m.f1*100).toFixed(1)}%`,showarrow:false,bgcolor:'rgba(255,255,255,0.92)',bordercolor:'#CBD5E1',borderwidth:1,font:{size:10.5,color:'#1E293B'}}]};
 }
 else if(key==='model_coefficients'){
   const coefTable=(bundle.forecast&&bundle.forecast.coef_table)||[];
   const sorted=coefTable.slice().sort((a,b)=>b.coefficient-a.coefficient);
   const featLabels={log_streams_first_week:'Log streams tuần 1',danceability:'Danceability (Dễ nhảy)',valence:'Valence (Tích cực)',loudness:'Loudness (Âm lượng)',duration_min:'Thời lượng (Phút)',energy:'Energy (Năng lượng)',acousticness:'Acousticness (Mộc mạc)',tempo:'Tempo (Nhịp độ)',instrumentalness:'Instrumentalness (Khí nhạc)',liveness:'Liveness (Sống động)',speechiness:'Speechiness (Lời nói)',rank_first_week:'Thứ hạng tuần 1 (Nghịch)'};
   const y=sorted.map(r=>featLabels[r.feature]||r.feature),x=sorted.map(r=>r.coefficient);
   fig.data=[{type:'bar',orientation:'h',y:y,x:x,text:sorted.map(r=>`OR = ${Number(r.odds_ratio).toFixed(2)} (β = ${r.coefficient>0?'+':''}${Number(r.coefficient).toFixed(2)})`),textposition:'outside',marker:{color:x.map(v=>v>=0?'#3B82F6':'#EF4444')},customdata:sorted.map(r=>[r.feature,r.odds_ratio,r.coefficient]),hovertemplate:'<b>%{y}</b><br>Hệ số β: <b>%{customdata[2]:+.3f}</b><br>Odds Ratio (e^β): <b>%{customdata[1]:.2f}</b><extra></extra>'}];
   fig.layout={margin:{l:165,r:25,t:15,b:40},xaxis:{title:{text:'Hệ số hồi quy chuẩn hóa (Standardized β)',font:{size:11}},tickfont:{size:10},range:[-0.7,1.8]},yaxis:{autorange:'reversed',tickfont:{size:11}},shapes:[{type:'line',xref:'x',yref:'paper',x0:0,x1:0,y0:0,y1:1,line:{color:'#94A3B8',width:1.5}}]};
 }
 return fig;
}

function link(key,p){if(!p)return;
 if(key==='hit_heatmap'){state.feature=p.x;state.band=String(bands.indexOf(p.y));if(boxFeatures.includes(p.x))state.boxfeature=p.x}
 else if(key==='genre_box'){state.genre=p.data.name;state.artist=''}
 else if(key==='artist_tree'){const id=p.id||p.data.ids?.[p.pointNumber];if(id==='root'){state.genre='';state.artist=''}else if(id?.startsWith('g:')){state.genre=id.slice(2);state.artist=''}else if(bundle.artists[id]){state.artist=id;state.genre=bundle.artists[id][1]}else return}
 else if(key==='collab'){const label=p.label||p.x;state.collab=label==='Collab'?'1':label==='Solo'?'0':''}
 else if(key==='duration'){const yr=Number(String(p.x).slice(0,4));if(yr>=2017&&yr<=2022)state.fromyear=state.toyear=yr}
 else if(key==='map'){state.country=p.location}
 else if(key==='radar'){if(!mapFeatures.includes(p.theta))return;state.feature=p.theta}
 else if(key==='seasonal'){state.month=String(p.x);state.weeks=[]}
 else if(key==='covid'){state.weeks=[String(p.x).slice(0,10)]}
 else if(key==='tradeoff_curve'){
   if(p.x!==undefined){
     const clickedTau=Math.round(Number(p.x)*100)/100;
     if(clickedTau>=0.10&&clickedTau<=0.90){
       state.threshold=clickedTau;
       $('tau-slider').value=clickedTau;
       $('tau-val').textContent='τ = '+clickedTau.toFixed(2);
       notify(`Đã chuyển ngưỡng quyết định sang τ = ${clickedTau.toFixed(2)}`);
       render();
     }
   }
   return;
 }
 else return;
 notify('Đã liên kết lựa chọn trong dashboard');render();
}

async function render(){
 const token=++generation;controls();current=buildModel();controls();nav();
 $('dashboard-name').textContent=dash().title;$('caption').textContent=point().caption;$('description').textContent=dash().description;$('note').textContent=dash().note;$('note').title=dash().note;
 $('counter').textContent=`${position+1} / ${book.story_points.length}`;
 document.querySelector('.workspace').classList.toggle('overview-workspace',kind()==='overview');
 document.body.classList.toggle('overview-screen',kind()==='overview');
 if(kind()==='overview')$('caption').textContent='CÁI NHÌN VỀ DỮ LIỆU';
 inspector();
 const host=$('dashboard');host.querySelectorAll('.plot').forEach(el=>Plotly.purge(el));host.replaceChildren();host.className='dashboard '+(kind()==='geography'?'geo':kind());
 for(const key of dash().worksheets){
  const panel=document.createElement('article');panel.className='panel panel-'+key;
  const head=document.createElement('div');head.className='panel-head';
  const title=document.createElement('h2');title.textContent=chartTitle(key);title.title=title.textContent;
  const tools=document.createElement('div');
  if(bundle.eda_figures && bundle.eda_figures[key]){
   const asset=bundle.eda_figures[key];panel.classList.add('static-panel');tools.replaceChildren();
   const enlarge=document.createElement('button'),save=document.createElement('button');
   enlarge.textContent='Xem lớn';enlarge.onclick=()=>showEdaImage(asset);save.textContent='PNG';save.title='Tải hình gốc từ notebook';
   save.onclick=async()=>download(key+'.png',await fetch(asset.image).then(r=>r.blob()),'image/png');tools.append(enlarge,save);
   head.append(title,tools);panel.append(head);
   const el=document.createElement('div');el.className='eda-image-wrap';
   const image=document.createElement('img');image.src=asset.image;image.alt=asset.title;image.width=asset.width;image.height=asset.height;image.onclick=()=>showEdaImage(asset);
   el.append(image);panel.append(el);
   const caption=document.createElement('p');caption.className='eda-caption';caption.textContent=asset.caption;caption.title=asset.caption;panel.append(caption);
   host.append(panel);
   continue;
  }
  if(key==='genre_box'){const select=document.createElement('select');select.setAttribute('aria-label','Chỉ số boxplot');options(select,boxFeatures.map(f=>[f,featureLabel(f)]));select.value=state.boxfeature;select.onchange=()=>{state.boxfeature=select.value;render()};tools.append(select)}
  if(key==='artist_tree'&&(state.genre||state.artist)){const up=document.createElement('button');up.textContent='↑ Gốc';up.title='Quay về toàn bộ thể loại/nghệ sĩ';up.onclick=()=>{state.genre='';state.artist='';render()};tools.append(up)}
  if(key==='decision_boundary'){
    const select=document.createElement('select');select.setAttribute('aria-label','Trục Y');
    options(select,[['rank_first_week','Hạng tuần 1'],['danceability','Danceability'],['energy','Energy'],['valence','Valence'],['acousticness','Acousticness'],['speechiness','Speechiness'],['loudness','Loudness'],['tempo','Tempo']]);
    select.value=state.boundary_y;select.onchange=()=>{state.boundary_y=select.value;render()};tools.append(select);
  }
  const png=document.createElement('button'),csv=document.createElement('button');png.textContent='PNG';png.title='Tải ảnh biểu đồ';csv.textContent='CSV';csv.title='Tải dữ liệu biểu đồ';tools.append(png,csv);head.append(title,tools);
  const el=document.createElement('div');el.className='plot';panel.append(head,el);host.append(panel);
  const fig=figure(key);
  if(key==='artist_tree'){const tree=fig.data[0];tree.labels=tree.labels.map((label,i)=>tree.ids[i].startsWith('g:')?genreLabel(label):label);tree.text=tree.text.map((label,i)=>tree.ids[i].startsWith('g:')?genreLabel(label):label);if(el.clientWidth<420&&!state.genre&&!state.artist)tree.maxdepth=2}
  fig.layout={paper_bgcolor:theme.panel,plot_bgcolor:theme.panel,colorway:colors,font:{family:"'Segoe UI', sans-serif",size:el.clientWidth<350?11:13,color:theme.ink},legend:{orientation:'h',x:0,y:1.13,font:{size:13,family:"'Segoe UI', sans-serif"}},hoverlabel:{bgcolor:theme.ink,font:{color:'#FFFEFB',size:13,family:"'Segoe UI', sans-serif"}},...fig.layout,height:el.clientHeight,width:el.clientWidth};
  if(key==='hit_heatmap'){fig.layout.xaxis.tickvals=bundle.features;fig.layout.xaxis.tickangle=-28;fig.layout.xaxis.ticktext=['Danceability','Energy','Valence','Acousticness','Speechiness','Instrumentalness','Liveness','Loudness','Tempo'];fig.layout.xaxis.tickfont={size:13,family:"'Segoe UI', sans-serif"};fig.layout.margin.b=72;if(el.clientWidth<580){fig.layout.xaxis.tickfont.size=11;fig.data[0].textfont.size=12}if(el.clientWidth<400){fig.layout.margin.l=65;fig.layout.margin.b=50;fig.data[0].textfont.size=10}}
  if(!fig.data.length){el.className+=' empty';el.textContent='Không có dữ liệu trong phạm vi chọn';continue}
  await Plotly.newPlot(el,fig.data,fig.layout,{responsive:true,displaylogo:false,displayModeBar:'hover',modeBarButtonsToRemove:['toImage']});if(token!==generation)return;
  if(key==='artist_tree')el.on('plotly_treemapclick',e=>{setTimeout(()=>link(key,e.points?.[0]),0);return false});else el.on('plotly_click',e=>link(key,e.points?.[0]));
  png.onclick=async()=>{try{const url=await Plotly.toImage(el,{format:'png',width:1200,height:800});download(key+'.png',await fetch(url).then(r=>r.blob()),'image/png')}catch(e){notify('Không xuất được PNG: '+e.message)}};
  csv.onclick=()=>exportCsv(chartRows(key),key);
 }
 if(kind()==='artists'){const panel=document.querySelector('.panel-collab,.panel-collab_box');if(panel){const toggle=document.createElement('select');toggle.setAttribute('aria-label','Cách xem Solo và Collab');options(toggle,[['collab','Cơ cấu & trung vị'],['collab_box','Phân phối chi tiết']]);toggle.value=dash().worksheets[2];toggle.onchange=()=>{dash().worksheets[2]=toggle.value;render()};panel.querySelector('.panel-head>div').prepend(toggle)}}
}

function chartRows(key){
 if(key==='hit_heatmap'){const a=hitStats();return bands.flatMap((band,i)=>bundle.features.map((f,j)=>({rank_band:band,feature:f,mean:a.raw[i][j],z_score:a.z[i][j],slots:a.counts[i]})))}
 if(key==='genre_box')return current.tracks.filter(({t})=>['pop','latin','k-pop','rap','dance pop'].includes(t[2])).map(({t})=>({track_id:t[0],track_name:t[1],genre:t[2],feature:state.boxfeature,value:tv(t,state.boxfeature)}));
 if(key==='artist_tree')return treeRows().map(([id,v])=>({artist:bundle.artists[id][0],genre:bundle.artists[id][1],credited_streams:v}));
 if(key==='collab')return collabStats().map(r=>({type:r.type,global_chart_tracks:r.count,tracks_with_streams:r.charted,median_global_streams:r.median,mean_global_streams:r.mean}));
 if(key==='duration'){const fig=figure(key);return fig.data[0].x.map((date,i)=>({date,duration_seconds:fig.data[0].y[i],rolling_4:fig.data[1].y[i]}))}
 if(['map','radar'].includes(key))return (key==='radar'?current.allCountries.filter(r=>[state.country,state.compare].includes(r[0])):current.countries).map(r=>({country:r[1],code:r[0],year:r[2],region:r[3],weight:state.weight,...Object.fromEntries(bundle.features.map(f=>[f,cv(r,f)]))}));
 if(key==='seasonal')return Array.from({length:12},(_,i)=>({month:i+1,weeks:current.weeks.filter(r=>+r[0].slice(5,7)===i+1).length,...Object.fromEntries(['danceability','acousticness'].map(f=>[f,mean(current.weeks.filter(r=>+r[0].slice(5,7)===i+1).map(r=>r[4+fi(f)]))]))}));
 if(key==='covid')return current.covid.map(r=>({week:r[0],weekly_deaths:r[13],...Object.fromEntries(bundle.features.map(f=>[f,r[4+fi(f)]]))}));
 if(key==='decision_boundary'||key==='confusion_heatmap')return (current.fcSamples||[]).map(s=>({track_id:s[0],track_name:s[1],artist:s[2],first_week:s[3],rank_first_week:s[4],streams_first_week:s[5],p_hat:s[7],hit_true:s[8],predicted:s[7]>=state.threshold?1:0}));
 if(key==='tradeoff_curve')return (current.fcCurves||[]).map(c=>({threshold:c.th,precision:c.prec,recall:c.rec,f1:c.f1,tp:c.tp,fp:c.fp,fn:c.fn,tn:c.tn}));
 if(key==='model_coefficients')return (bundle.forecast?.coef_table||[]);
 return [];
}

function exportCsv(rows,key){if(!rows.length){notify('Phạm vi này không có dữ liệu');return}const columns=Object.keys(rows[0]),quote=v=>'"'+String(v??'').replaceAll('"','""')+'"';download(key+'.csv','\ufeff'+[columns.map(quote).join(','),...rows.map(r=>columns.map(k=>quote(r[k])).join(','))].join('\r\n'),'text/csv;charset=utf-8')}
function table(headers,rows){const host=$('detail'),t=document.createElement('table'),thead=document.createElement('thead'),h=document.createElement('tr');headers.forEach(text=>{const th=document.createElement('th');th.textContent=text;h.append(th)});thead.append(h);t.append(thead);const body=document.createElement('tbody');for(const values of rows){const tr=document.createElement('tr');for(const value of values){const td=document.createElement('td');if(value&&typeof value==='object'&&value.action){const b=document.createElement('button');b.textContent=value.label;b.onclick=value.action;td.append(b)}else td.textContent=value??'—';tr.append(td)}body.append(tr)}t.append(body);host.append(t)}

function audioStory(){
 const stats=hitStats(),band=state.band===''?0:Number(state.band),z=stats.z[band],metric=state.boxfeature;
 const group=band===0?'Top 10':'nhóm hạng '+bands[band],signed=v=>Math.abs(v)<.005?'0.00':(v>0?'+':'')+v.toFixed(2);
 const direction=(f,high,low)=>{const v=z[fi(f)];return Number.isFinite(v)?`${Math.abs(v)<.005?'tương đương mức nền ở '+featureLabel(f):v>0?high:low} (${featureLabel(f)} ${signed(v)} SD)`:`${featureLabel(f)} chưa đủ dữ liệu`};
 const focus=['tempo','danceability','energy','acousticness'];
 const trends=[direction('tempo','nhịp độ nhanh hơn','nhịp độ chậm hơn'),direction('danceability','dễ nhảy hơn','ít dễ nhảy hơn'),direction('energy','năng lượng cao hơn','năng lượng thấp hơn'),direction('acousticness','mộc mạc hơn','ít mộc mạc hơn')];
 if(!focus.includes(state.feature)){const v=z[fi(state.feature)];trends.push(Number.isFinite(v)?`${featureLabel(state.feature)} ${v>=0?'cao':'thấp'} hơn (${signed(v)} SD)`:`${featureLabel(state.feature)} chưa đủ dữ liệu`)}
 const first=stats.counts[band]?`Các bài thuộc ${group} có hồ sơ ${trends.join(', ')} so với trung bình BXH trong phạm vi ${state.fromyear}–${state.toyear}${state.genre?' · '+genreLabel(state.genre):''}.`:`Không có bài thuộc ${group} trong phạm vi đang chọn.`;
 const medians=['pop','latin','k-pop','rap','dance pop'].map(g=>({genre:g,value:median(current.tracks.filter(({t})=>t[2]===g).map(({t})=>tv(t,metric)))})).filter(r=>Number.isFinite(r.value)).sort((a,b)=>b.value-a.value);
 let second=medians.length>1?`${medians.slice(0,2).map(r=>genreLabel(r.genre)+' (trung vị '+r.value.toFixed(metric==='tempo'?1:3)+')').join(' và ')} có ${boxLabel[metric]} cao nhất trong các thể loại đang hiển thị.`:medians.length?`Trong nhóm ${genreLabel(medians[0].genre)}, trung vị ${boxLabel[metric]} đạt ${medians[0].value.toFixed(metric==='tempo'?1:3)}.`:'Không đủ dữ liệu thể loại trong phạm vi chọn.';
 const genres=new Map(),ranks=new Map();
 for(const r of current.rows){const t=bundle.tracks[r[0]],value=tv(t,metric);if(!Number.isFinite(value)||!['pop','latin','k-pop','rap','dance pop'].includes(t[2]))continue;for(const [groups,key] of [[genres,t[2]],[ranks,r[3]]]){const a=groups.get(key)||[0,0];a[0]+=value*r[4];a[1]+=r[4];groups.set(key,a)}}
 const range=groups=>{const values=[...groups.values()].map(a=>a[0]/a[1]);return Math.max(...values)-Math.min(...values)};
 if(genres.size>1&&ranks.size>1){const g=range(genres),r=range(ranks),ratio=r>1e-12?g/r:null;second+=` Chênh lệch trung bình ${featureLabel(metric)} giữa thể loại ${g.toFixed(metric==='tempo'?1:3)}, giữa tầng hạng ${r.toFixed(metric==='tempo'?1:3)}${ratio!==null?`; khác biệt theo thể loại ${ratio>=1?'lớn':'nhỏ'} hơn, bằng ${ratio.toFixed(1)} lần khác biệt theo tầng hạng`:''}.`}
 else if(genres.size<2)second+=' Đang lọc một thể loại nên chưa đối chiếu được khác biệt giữa các thể loại.';
 else second+=' Đang lọc một tầng hạng nên chưa đối chiếu được khác biệt giữa các tầng thứ hạng.';
 const values=z.filter(Number.isFinite),maximum=values.length?Math.max(...values.map(Math.abs)):null;
 const third=maximum===null?'Cần thêm dữ liệu để đánh giá hồ sơ âm thanh của nhóm đang chọn.':`Độ lệch lớn nhất của nhóm đang xét là ${maximum.toFixed(2)} SD. Không có một “công thức âm thanh độc tôn” bảo chứng vị trí Top 1. Đặc trưng âm học định hình trải nghiệm thể loại; riêng phân tích này chưa đủ để quyết định thành công thương mại.`;
 return [[band===0?'1. Xu hướng nhóm dẫn đầu':'1. Xu hướng nhóm thứ hạng đang chọn',first],['2. Thể loại định hình âm học',second],['3. Thông điệp cốt lõi',third]];
}

function timeStory(){
 const years=new Map();for(const r of current.weeks){if(!Number.isFinite(r[3]))continue;const year=r[0].slice(0,4),values=years.get(year)||[];values.push(r[3]/1000);years.set(year,values)}
 const yearly=[...years].map(([year,values])=>({year,value:mean(values),n:values.length})).sort((a,b)=>a.year.localeCompare(b.year));
 let first='Chưa đủ dữ liệu thời lượng trong giai đoạn chọn.';
 if(yearly.length>1){const start=yearly[0],last=yearly.at(-1),low=yearly.reduce((a,b)=>a.value<b.value?a:b),drop=start.value-low.value;
   first=`Thời lượng trung bình năm ${start.year} là ${start.value.toFixed(1)} giây; mức thấp nhất trong giai đoạn chọn là ${low.value.toFixed(1)} giây (${low.year})${drop>.05?', giảm '+drop.toFixed(1)+' giây so với năm đầu':''}. Năm ${last.year} đạt ${last.value.toFixed(1)} giây${last.year!==low.year&&last.value>low.value+.05?', tăng lại '+(last.value-low.value).toFixed(1)+' giây từ đáy':''}. Video ngắn và cách tiêu thụ nhạc streaming là các cơ chế giải thích khả dĩ.`;
 }else if(yearly.length){const y=yearly[0],values=current.weeks.map(r=>r[3]/1000).filter(Number.isFinite);first=`Năm ${y.year}: trung bình ${y.value.toFixed(1)} giây, dao động tuần từ ${Math.min(...values).toFixed(1)} đến ${Math.max(...values).toFixed(1)} giây. Phạm vi một năm chưa cho thấy xu hướng co cụm qua nhiều năm.`}
 if(yearly.length&&yearly.at(-1).n<50)first+=` Năm ${yearly.at(-1).year} chỉ có ${yearly.at(-1).n} tuần dữ liệu.`;
 const month=state.month?Number(state.month):12,selected=current.weeks.filter(r=>Number(r[0].slice(5,7))===month),other=current.weeks.filter(r=>Number(r[0].slice(5,7))!==month);
 const acoustic=mean(selected.map(r=>r[7])),base=mean(other.map(r=>r[7])),dance=mean(selected.map(r=>r[4])),danceBase=mean(other.map(r=>r[4]));
 let second=Number.isFinite(acoustic)&&Number.isFinite(base)?`Tháng ${month}, Acousticness đạt ${acoustic.toFixed(3)}, ${acoustic>=base?'cao':'thấp'} hơn mức nền ${base.toFixed(3)} của các tháng khác (${Math.abs(acoustic-base).toFixed(3)}). Danceability đạt ${fmt(dance)}, so với ${fmt(danceBase)} ở các tháng khác.`:'Chưa đủ dữ liệu tháng được chọn và các tháng còn lại để so sánh mùa vụ.';
 if(month===12&&Number.isFinite(acoustic)&&acoustic>base)second+=' Sự trở lại của nhạc Giáng sinh và lễ hội có thể góp phần giải thích mức tăng độ mộc mạc.';
 const covid=current.covid.filter(r=>Number.isFinite(r[13])&&Number.isFinite(r[4+fi(state.feature)])),deaths=covid.map(r=>r[13]),values=covid.map(r=>r[4+fi(state.feature)]),raw=pearson(deaths,values),monthly=new Map();
 for(const r of covid){const key=r[0].slice(5,7),pairs=monthly.get(key)||[];pairs.push([r[13],r[4+fi(state.feature)]]);monthly.set(key,pairs)}
 const centers=new Map([...monthly].map(([month,pairs])=>[month,[mean(pairs.map(p=>p[0])),mean(pairs.map(p=>p[1]))]]));
 const adjusted=pearson(covid.map(r=>r[13]-centers.get(r[0].slice(5,7))[0]),covid.map(r=>r[4+fi(state.feature)]-centers.get(r[0].slice(5,7))[1]));
 let third=Number.isFinite(raw)?`${featureLabel(state.feature)} và tử vong COVID-19 có Pearson r = ${raw.toFixed(3)} (${covid.length} tuần).`:'Chưa đủ dữ liệu hoặc biến thiên để tính tương quan COVID trong phạm vi chọn.';
 if(Number.isFinite(raw)&&Number.isFinite(adjusted)&&monthly.size>1){third+=` Sau khi trừ mức trung bình của từng tháng lịch ở cả hai chuỗi, r = ${adjusted.toFixed(3)}. ${Math.abs(adjusted)<Math.abs(raw)-.005?'Mối liên hệ giảm về độ lớn, phù hợp với khả năng mùa vụ góp phần khuếch đại tương quan gốc.':Math.abs(adjusted)>Math.abs(raw)+.005?'Độ lớn tương quan tăng sau điều chỉnh; dữ liệu này chưa ủng hộ nhận định mùa vụ khuếch đại tương quan gốc.':'Độ lớn tương quan ít thay đổi sau điều chỉnh tháng.'}`}
 else if(Number.isFinite(raw)&&monthly.size===1)third+=' Đang chọn một tháng nên chưa đối chiếu được ảnh hưởng giữa các tháng.';
 third+=' Cần xét mùa vụ và xu hướng thời gian trước khi diễn giải nguyên nhân; điều chỉnh tháng chưa chứng minh tác động của đại dịch.';
 return [[`1. Xu hướng thời lượng (${state.fromyear}–${state.toyear})`,first],[`2. Dấu ấn mùa vụ tháng ${month}`,second],['3. Cẩn trọng với biến động đại dịch',third]];
}

function geographyStory(){
 const f=state.feature,rows=current.countries.filter(r=>Number.isFinite(cv(r,f))),name=r=>({Vietnam:'Việt Nam',Japan:'Nhật Bản'})[r[1]]||r[1];
 const grouped=new Map();for(const r of rows){const values=grouped.get(r[3])||[];values.push(cv(r,f));grouped.set(r[3],values)}
 const regions=[...grouped].map(([region,values])=>({region,value:mean(values),n:values.length})).sort((a,b)=>b.value-a.value);
 let first='Không đủ dữ liệu quốc gia cho phạm vi đang chọn.';
 if(regions.length>1){const high=regions[0],low=regions.at(-1);first=`Năm ${state.year}, ${short(high.region)} có ${featureLabel(f)} trung bình cao nhất (${high.value.toFixed(3)}; ${high.n} quốc gia), còn ${short(low.region)} thấp nhất (${low.value.toFixed(3)}; ${low.n} quốc gia). Chênh lệch ${Math.abs(high.value-low.value).toFixed(3)} cho thấy sự phân hóa theo địa lý. Các trung bình khu vực tính mỗi quốc gia một trọng số như nhau.`}
 else if(rows.length){const sorted=rows.slice().sort((a,b)=>cv(b,f)-cv(a,f)),high=sorted[0],low=sorted.at(-1);first=`Trong ${short(rows[0][3])} năm ${state.year}, ${name(high)} có ${featureLabel(f)} cao nhất (${cv(high,f).toFixed(3)}), ${name(low)} thấp nhất (${cv(low,f).toFixed(3)}). ${rows.length>1?'Chênh lệch '+Math.abs(cv(high,f)-cv(low,f)).toFixed(3)+' cho thấy các quốc gia trong cùng khu vực vẫn có khác biệt.':'Phạm vi hiện chỉ có một quốc gia.'}`}
 const a=current.allCountries.find(r=>r[0]===state.country),b=current.allCountries.find(r=>r[0]===state.compare);
 let second='Chưa đủ dữ liệu cho cặp quốc gia đang chọn.',third='Cần chọn phạm vi có dữ liệu để đánh giá thị hiếu âm học.';
 if(a&&b){
   const profile=r=>`${name(r)}: Acousticness ${fmt(cv(r,'acousticness'))}, Energy ${fmt(cv(r,'energy'))}, Danceability ${fmt(cv(r,'danceability'))}.`;
   const delta=Math.abs(cv(a,f)-cv(b,f)),sameRegion=a[3]===b[3],sameCountry=a[0]===b[0];
   second=sameCountry?`Hai lựa chọn cùng là ${name(a)} nên hồ sơ âm thanh trùng nhau.`:`${name(a)} và ${name(b)} ${sameRegion?'cùng thuộc '+short(a[3]):'thuộc hai khu vực khác nhau'} nhưng cần đối chiếu từng đặc trưng:\n• ${profile(a)}\n• ${profile(b)}\nChênh lệch ${featureLabel(f)} là ${fmt(delta)}; ${delta<.005?'hai nước gần tương đương ở chỉ số này':(cv(a,f)>cv(b,f)?name(a):name(b))+' có giá trị cao hơn'}.`;
   const suffix=state.weight==='weighted'?'theo lượt nghe':'không trọng số';
   third=sameCountry?`Hồ sơ của ${name(a)} đang được đối chiếu với chính nó. Chọn một quốc gia khác để tìm khác biệt phục vụ định hướng phát hành.`:`${delta>=.05?'Khác biệt giữa hai thị trường gợi ý cần điều chỉnh sản phẩm theo từng quốc gia, thay vì áp dụng một công thức chung.':'Hai thị trường tương đối gần nhau ở '+featureLabel(f)+', nhưng cần xét toàn bộ hồ sơ âm thanh khi định hướng phát hành.'} Cơ cấu thể loại và văn hóa nghe nhạc có thể góp phần giải thích. Kết quả dùng trung bình ${suffix} trên BXH Spotify năm ${state.year}.`;
 }
 return [['1. Thị hiếu âm học phân hóa theo địa lý',first],['2. Xóa bỏ định kiến gộp nhóm khu vực',second],['3. Thông điệp cốt lõi',third]];
}

function artistStory(){
 const a=correlationStats(),rho=a.z[9][10],selected=a.z[fi(state.feature)][10];
 const audio=bundle.features.map((f,i)=>({feature:f,rho:a.z[i][10]})).filter(r=>Number.isFinite(r.rho)).sort((x,y)=>Math.abs(y.rho)-Math.abs(x.rho));
 const leading=Number.isFinite(rho)&&rho>0&&audio.length&&rho>=Math.abs(audio[0].rho);
 let first=Number.isFinite(rho)?`Tên tuổi tích lũy trước khi vào BXH có tương quan ${rho>=0?'thuận':'nghịch'} với stream 8 tuần đầu (ρ = ${rho.toFixed(2)}, ${num(a.n)} bài).`:'Mẫu đang chọn chưa đủ biến thiên để tính tương quan tên tuổi nghệ sĩ với stream 8 tuần đầu.';
 if(Number.isFinite(rho)&&audio.length)first+=leading?' Đây là mối liên hệ lớn nhất trong các biến khảo sát.':` ${featureLabel(audio[0].feature)} có độ lớn tương quan nổi bật nhất trong các đặc trưng âm thanh (ρ = ${audio[0].rho.toFixed(2)}).`;
 if(Number.isFinite(rho)&&Number.isFinite(selected)){first+=` ${featureLabel(state.feature)}: ρ = ${selected.toFixed(2)}.`;if(rho>0&&selected>0&&selected>.005)first+=` Tương quan tên tuổi bằng ${(rho/selected).toFixed(1)} lần chỉ số này.`}
 if(Number.isFinite(rho)&&Math.abs(rho)<.2)first+=' Mức liên hệ của tên tuổi vẫn còn yếu.';
 const [solo,collab]=collabStats(),total=solo.count+collab.count;
 let second='Không có bài hát đủ cửa sổ 8 tuần trong phạm vi đang chọn.';
 if(total){const soloPct=100*solo.count/total;second=`Đơn ca chiếm ${soloPct.toFixed(1)}%, hợp tác chiếm ${(100-soloPct).toFixed(1)}% số bài.`;
   if(Number.isFinite(solo.median)&&Number.isFinite(collab.median)&&solo.median>0){const delta=100*(collab.median/solo.median-1);second+=` Collab đạt trung vị ${(collab.median/1e6).toFixed(1)} triệu stream trong 8 tuần đầu, ${Math.abs(delta)<.05?'xấp xỉ đơn ca':`${delta>0?'cao':'thấp'} hơn ${Math.abs(delta).toFixed(1)}% so với đơn ca`} (${(solo.median/1e6).toFixed(1)} triệu).`}
   else {const available=solo.count?solo:collab;second+=` Trung vị ${available.type==='Solo'?'đơn ca':'hợp tác'} là ${(available.median/1e6).toFixed(1)} triệu stream. Chỉ đang chọn một hình thức nên chưa so sánh được hai nhóm.`}
 }
 const rows=treeRows(),groups=new Map(),streamTotal=rows.reduce((sum,[id,value])=>sum+value,0);
 for(const [id,value] of rows){const genre=bundle.artists[id][1];groups.set(genre,(groups.get(genre)||0)+value)}
 const top=[...groups].sort((x,y)=>y[1]-x[1]).slice(0,2);
 let third='Không có nghệ sĩ trong phạm vi treemap đang chọn.';
 if(top.length>1){const share=100*top.reduce((sum,[g,v])=>sum+v,0)/streamTotal;third=`Trong ${rows.length} nghệ sĩ dẫn đầu giai đoạn ${state.fromyear}–${state.toyear}, ${top.map(([g,v])=>genreLabel(g)+' ('+(100*v/streamTotal).toFixed(1)+'%)').join(' và ')} chiếm tổng cộng ${share.toFixed(1)}% stream ghi công của nhóm này. ${share>=50?'Lượt nghe tập trung chủ yếu vào hai nhánh này.':'Lượt nghe phân bổ qua nhiều nhánh thể loại.'}`}
 else if(top.length){third=state.artist?`${bundle.artists[state.artist][0]} ghi nhận ${shortStreams(streamTotal)} stream ghi công trong giai đoạn chọn. Đang lọc một nghệ sĩ nên không đánh giá được mức tập trung giữa các nghệ sĩ.`:`Đang lọc ${genreLabel(top[0][0])}, với ${rows.length} nghệ sĩ và ${shortStreams(streamTotal)} stream ghi công. Phạm vi một thể loại không đại diện cơ cấu thể loại toàn thị trường.`}
 return [[leading?'1. Tên tuổi là đòn bẩy lớn nhất':'1. Tên tuổi và lợi thế ban đầu',first],['2. Hiệu ứng hợp tác (Collab)',second],['3. Tập trung hóa lượt nghe',third]];
}

function forecastStory(){
 const m=current.fcMetrics||{tp:128,fp:67,fn:86,tn:660,n:941,acc:0.837,prec:0.656,rec:0.598,f1:0.626};
 const tau=Number(state.threshold)||0.79;
 const splitName={test:'tập Test (2021–2022)',validation:'tập Validation (2020–2021)',train:'tập Train (2017–2020)',all:'toàn bộ mẫu'}[state.split]||'tập Test';
 
 const first=`Mô hình Logistic dự báo khả năng bài hát vào Global Top 50 (8 tuần tới) từ 12 biến tuần đầu (10 âm học + thứ hạng + log stream). Trên ${splitName}, khảo sát ${num(m.n)} bài, gồm ${num(m.tp+m.fn)} bài hit thực tế (tỷ lệ nền ${((m.tp+m.fn)/m.n*100).toFixed(1)}%).`;
 
 const second=`Đạt ROC-AUC = 0.811 và PR-AUC = 0.690 trên tập Test. Điểm xác suất p̂ phản ánh mức độ tự tin của mô hình, giúp phân loại cấp độ rủi ro thay vì nhận định nhị phân cứng 0/1.`;
 
 const third=`Tại ngưỡng τ = ${tau.toFixed(2)} (tối ưu F1 = 0.79 từ Validation): Precision = ${(m.prec*100).toFixed(1)}%, Recall = ${(m.rec*100).toFixed(1)}%, F1 = ${(m.f1*100).toFixed(1)}%, Accuracy = ${(m.acc*100).toFixed(1)}%. Kéo thanh trượt để điều chỉnh trade-off: giảm τ giúp bắt trọn nhiều hit (tăng Recall), tăng τ giúp chọn lọc bài chắc chắn (tăng Precision).`;
 
 const sub50=current.fcSub50||{count:595,pos:9,pred_pos:20};
 const fourth=`\n• Nhóm hạng 51–200: Khởi đầu ngoài Top 50 chỉ có 1.5% hit thực tế (${sub50.pos}/${sub50.count} bài), dễ gặp dương tính giả (FP) nếu điểm xuất phát ban đầu quá thấp.\n• Điểm xác suất p̂: Phản ánh thứ bậc xếp hạng rủi ro tương đối (ranking score), chưa hiệu chuẩn xác suất tuyệt đối.`;
 
 return [
   ['1. Dữ liệu & Tín hiệu tuần đầu',first],
   ['2. Năng lực xếp hạng (ROC & PR-AUC)',second],
   ['3. Đánh đổi tại ngưỡng quyết định τ',third],
   ['4. Sai lệch & Cảnh báo học thuật',fourth]
 ];
}

function getMetrics(){
  const k=kind(), f=state.feature;
  if(k==='main_dashboard'){
    const a=current.allCountries.find(r=>r[0]===state.country), b=current.allCountries.find(r=>r[0]===state.compare);
    const name=r=>r?({Vietnam:'Việt Nam',Japan:'Nhật Bản'})[r[1]]||r[1]:'—';
    return [
      [name(a)+' · '+featureLabel(f), a?fmt(cv(a,f),f):'—'],
      [name(b)+' · '+featureLabel(f), b?fmt(cv(b,f),f):'—'],
      ['Collab vs Solo stream', '+21.5% vượt trội'],
      ['Thời lượng TB (TikTok)', '198.5s (-20s)']
    ];
  }
  if(k==='forecast'){
    const m=current.fcMetrics||{acc:0.837,prec:0.656,rec:0.598,f1:0.626};
    const tau=Number(state.threshold)||0.79;
    return [
      ['Ngưỡng quyết định (τ)', 'τ = ' + tau.toFixed(2)],
      ['F1-Score tối ưu', (m.f1*100).toFixed(1)+'%'],
      ['Precision (Độ chuẩn)', (m.prec*100).toFixed(1)+'%'],
      ['Recall (Độ bao phủ)', (m.rec*100).toFixed(1)+'%']
    ];
  }
  if(k==='hits'){
    const hs=hitStats(), j=fi(state.feature);
    const zTop10=hs?.z?.[0]?.[j];
    return [
      ['Đặc trưng âm học', featureLabel(f)],
      ['Z-score Top 1–10', Number.isFinite(zTop10)?(zTop10>0?'+':'')+zTop10.toFixed(2)+' σ':'—'],
      ['Số bài Top 200', num(current.tracks.length)],
      ['Tầng hạng chọn', state.band?bands[+state.band]:'Toàn bộ Top 200']
    ];
  }
  if(k==='artists'){
    const a=correlationStats(), rho=a.z[9][10];
    return [
      ['Tên tuổi nghệ sĩ (ρ)', Number.isFinite(rho)?(rho>0?'+':'')+rho.toFixed(2):'—'],
      ['Số bài phân tích', num(current.analysis.length)],
      ['Nghệ sĩ drill-down', state.artist?(bundle.artists[state.artist]?.[0]||'Đã chọn'):'Toàn bộ 80 nghệ sĩ'],
      ['Thể loại đang lọc', state.genre||'Tất cả thể loại']
    ];
  }
  if(k==='geography'){
    const a=current.allCountries.find(r=>r[0]===state.country), b=current.allCountries.find(r=>r[0]===state.compare);
    if(a&&b){
      const va=cv(a,f), vb=cv(b,f);
      const name=r=>({Vietnam:'Việt Nam',Japan:'Nhật Bản'})[r[1]]||r[1];
      const diff=(va!==null&&vb!==null)?(va-vb):null;
      return [
        [name(a)+' · '+featureLabel(f), fmt(va,f)],
        [name(b)+' · '+featureLabel(f), fmt(vb,f)],
        ['Chênh lệch (A − B)', diff!==null?(diff>0?'+':'')+fmt(diff,f):'—'],
        ['Năm bản đồ', String(state.year||2021)]
      ];
    }
    return [['Quốc gia A', '—'], ['Quốc gia B', '—'], ['Chênh lệch', '—'], ['Năm bản đồ', String(state.year||2021)]];
  }
  if(k==='time'){
    const selected=current.covid.filter(r=>state.weeks.includes(r[0]));
    const cov=selected.length?selected:current.covid;
    const avgFeat=mean(cov.map(r=>r[4+fi(f)]));
    return [
      ['Đặc trưng âm học', featureLabel(f)],
      [featureLabel(f)+(selected.length?' · tuần chọn':' · trung bình'), fmt(avgFeat,f)],
      ['Số tuần quan sát', num(cov.length)+' tuần'],
      ['Tổng tử vong tuần', num(cov.reduce((s,r)=>s+r[2],0))+' ca']
    ];
  }
  return [];
}

function showEdaImage(asset){
 let dialog=$('eda-image-dialog');
 if(!dialog){dialog=document.createElement('dialog');dialog.id='eda-image-dialog';dialog.className='eda-image-dialog';document.body.append(dialog);dialog.addEventListener('click',event=>{if(event.target===dialog)dialog.close()})}
 dialog.replaceChildren();const heading=document.createElement('h2'),close=document.createElement('button'),image=document.createElement('img'),caption=document.createElement('p');
 heading.textContent=asset.title;close.textContent='Đóng';close.onclick=()=>dialog.close();image.src=asset.image;image.alt=asset.title;caption.textContent=asset.caption+' Nguồn: '+asset.source+', ô '+asset.cell+'.';
 dialog.append(close,heading,image,caption);dialog.showModal();
}

function openingInspector(){
 document.querySelector('.inspector').classList.toggle('inspector-overview',true);
 document.querySelector('.inspector h2').textContent='Dẫn nhập EDA';
 const e=bundle.eda;
 if(!e) return;
 $('metrics').replaceChildren();
 for(const [label,value] of [['Bài trong mẫu chart',num(e.tracks)],['Quốc gia + Global',num(e.markets)],['Tuần Global',num(e.weeks)],['Train Global',num(e.train?.count)]]){
  const card=document.createElement('div'),small=document.createElement('small'),strong=document.createElement('strong');
  card.className='metric';small.textContent=label;strong.textContent=value;card.append(small,strong);$('metrics').append(card);
 }
 $('insight').replaceChildren();
 const stories=[
  ['1. Đọc hình dạng phân phối',`Năm histogram giữ nguyên từ EDA, mỗi bài một lần. So sánh trung bình với trung vị để nhận ra độ lệch; Speechiness và Duration có đuôi dài.`],
  ['2. Audio có thông tin chồng lấn',`Energy–Loudness: ρ = ${e.correlations?.[e.features.indexOf('energy')]?.[e.features.indexOf('loudness')]?.toFixed(3)||'0.763'}. Heatmap mô tả liên hệ giữa các đặc trưng, không phải khả năng tạo hit.`],
  ['3. Nhãn không cân bằng',`Train có ${(100*(e.train?.rate||0)).toFixed(2)}% nhãn dương. Hình tách nhóm khởi đầu hạng 51–200 để phân biệt bài bứt phá với bài đã ở Top 50.`],
  ['4. Đặt dữ liệu vào thời gian','Đường xu hướng dùng trọng số stream và trung bình trượt bốn tuần. Các biến động theo mùa là mô tả, cần thêm bằng chứng để giải thích nguyên nhân.'],
  ['Phạm vi',`Audio: ${num(e.tracks)} bài từng vào chart, ${e.first_week}–${e.last_week}. Nhãn: ${num(e.train?.count)} bài Train Global; cửa sổ tám tuần sau t0, đủ Top 50. Mẫu không đại diện mọi bài trên Spotify.`]
 ];
 for(const [heading,text] of stories){
  const paragraph=document.createElement('p'),strong=document.createElement('strong');
  paragraph.className='audio-story-item';strong.textContent=heading+': ';
  paragraph.append(strong,document.createTextNode(text));$('insight').append(paragraph);
 }
 $('detail').replaceChildren();
}

function inspector(){
 const k=kind();
 if(k==='overview'){openingInspector();return}
 document.querySelector('.inspector').classList.toggle('inspector-overview',false);
 document.querySelector('.inspector h2').textContent='Bộ lọc & diễn giải';
 document.querySelector('.inspector').classList.toggle('inspector-hits',k==='hits');
 $('metrics').replaceChildren();
 
 const kpis=getMetrics();
 for(const [label,val] of kpis){
   const box=document.createElement('div');box.className='metric';
   const small=document.createElement('small'),strong=document.createElement('strong');
   small.textContent=label;strong.textContent=val;
   box.append(small,strong);$('metrics').append(box);
 }
 
 
function mainStory(){
  const a=current.allCountries.find(r=>r[0]===state.country), b=current.allCountries.find(r=>r[0]===state.compare);
  const name=r=>r?({Vietnam:'Việt Nam',Japan:'Nhật Bản'})[r[1]]||r[1]:'—';
  return [
    ['1. Bản sắc địa lý & Đối đầu ADN', 'Bản đồ thế giới và Radar đối đầu bóc tách sự phân hóa rõ nét: ' + name(a) + ' có ' + featureLabel(state.feature) + ' đạt ' + (a?fmt(cv(a,state.feature),state.feature):'—') + ', đối lập với ' + name(b) + ' (' + (b?fmt(cv(b,state.feature),state.feature):'—') + '). Click trực tiếp trên bản đồ để chọn lại quốc gia A.'],
    ['2. Đòn bẩy hợp tác (Collab vs Solo)', 'Đơn ca chiếm đa số (~59% số bài phát hành), nhưng các dự án Hợp tác (Collab) có trung vị lượt stream cao hơn hẳn (~28.5 triệu so với ~23.5 triệu lượt stream), chứng minh Collab là đòn bẩy tối ưu đưa bài hát vào bảng xếp hạng.'],
    ['3. Hiện tượng \"TikTok-hóa\" âm nhạc', 'Thời lượng bài hát trung bình sụt giảm mạnh từ 218 giây (2017) xuống còn 198.5 giây (2020) — mất đúng 20 giây chỉ sau 3 năm dưới tác động của cơ chế trả bản quyền 30 giây và văn hóa video ngắn.']
  ];
}

const stories={main_dashboard:mainStory,hits:audioStory,artists:artistStory,geography:geographyStory,time:timeStory,forecast:forecastStory};
 if(stories[k]){
   $('insight').replaceChildren();
   for(const [heading,text] of stories[k]()){
     const paragraph=document.createElement('p'),title=document.createElement('strong');
     paragraph.className='audio-story-item';paragraph.style.whiteSpace='pre-line';
     title.textContent=heading+': ';paragraph.append(title,document.createTextNode(text));
     $('insight').append(paragraph);
   }
 }
 
 $('detail').replaceChildren();
 if(detailMode==='method'){
   const texts=k==='forecast'?[
     'Định nghĩa toán học: Y_hat = 1 nếu p_hat >= tau, ngược lại 0.',
     'Hồi quy Logistic: logit(p) = z = beta_0 + sum(beta_j * X_standardized). Xác suất p = 1 / (1 + exp(-z)).',
     'Ngưỡng tối ưu F1 = 0.79 được tối ưu hóa nghiêm ngặt trên tập Validation (2020–2021) và khóa cố định trước khi đánh giá trên tập Test độc lập (2021–2022).',
     'Cảnh báo: Không dùng mô hình để suy diễn nhân quả; các biến chỉ đo mối liên hệ thống kê tuần đầu.'
   ]:[meta[state.feature]+' · '+unit(state.feature),dash().note];
   for(const text of texts){const p=document.createElement('p');p.textContent=text;$('detail').append(p)}
   return;
 }
 
 if(k==='forecast'){
   const samples=(current.fcSamples||[]).slice(0,10);
   const tau=Number(state.threshold)||0.79;
   table(['Bài hát · Nghệ sĩ','Hạng 1','p̂','Dự báo','Thực tế'],samples.map(s=>[
     {label:s[1],action:()=>{notify(`${s[1]} - ${s[2]} (Hạng ${s[4]}, Streams: ${s[5].toLocaleString()}, p̂: ${(s[7]*100).toFixed(1)}%)`)},},
     '#'+s[4],
     (s[7]*100).toFixed(1)+'%',
     s[7]>=tau?'Hit (1)':'K.Đạt (0)',
     s[8]?'Hit (1)':'K.Đạt (0)'
   ]));
 }
 else if(k==='hits'){
   if(state.artist||state.genre){const ranked=treeRows().slice(0,6);table(['Nghệ sĩ · drill-down','Stream ghi công'],ranked.map(([id,v])=>[{label:bundle.artists[id][0],action:()=>{state.artist=id;state.genre=bundle.artists[id][1];render()}},(v/1e9).toFixed(2)+' tỷ']))}
   else {const a=hitStats(),j=fi(state.feature);table(['Nhóm hạng','z · '+state.feature],bands.map((b,i)=>[{label:b,action:()=>{state.band=String(i);render()}},fmt(a.z[i][j])+' điểm']));const c=collabStats();const p=document.createElement('p');p.textContent=c.map(r=>r.type+': '+r.count+' bài BXH Global; trung vị '+(r.median===null?'—':(r.median/1e6).toFixed(1))+' triệu/bài; trung bình '+(r.mean===null?'—':(r.mean/1e6).toFixed(1))+' triệu/bài').join(' · ');$('detail').append(p)}
 }
 else if(k==='geography'){const a=current.allCountries.find(r=>r[0]===state.country),b=current.allCountries.find(r=>r[0]===state.compare);table(['Đặc trưng',a?.[1]||'A',b?.[1]||'B'],bundle.features.map(f=>[{label:f,action:()=>{if(mapFeatures.includes(f)){state.feature=f;render()}else notify(meta[f])}},a?fmt(cv(a,f),f):'—',b?fmt(cv(b,f),f):'—']))}
 else if(k==='artists'){const a=correlationStats();table(['Yếu tố','ρ với stream 8 tuần'],corrKeys.slice(0,10).map((f,i)=>[f==='artist_popularity_prior'?'Tên tuổi nghệ sĩ':featureLabel(f),fmt(a.z[i][10])]).sort((a,b)=>Number(b[1])-Number(a[1])))}
 else if(state.weeks.length){const r=current.covid.find(r=>state.weeks.includes(r[0]));if(r){table(['Tuần '+r[0],'Giá trị'],bundle.features.map(f=>[{label:f,action:()=>{state.feature=f;render()}},fmt(r[4+fi(f)],f)]))}}
 else if(state.month){const sums=new Map();for(const r of bundle.global_rows){if(r[1]>=state.fromyear&&r[1]<=state.toyear&&r[2]===+state.month)sums.set(r[0],(sums.get(r[0])||0)+r[5])}table(['Top bài · tháng '+state.month,'Stream Global'],[...sums].sort((a,b)=>b[1]-a[1]).slice(0,6).map(([i,v])=>[bundle.tracks[i][1],(v/1e6).toFixed(1)+' tr']))}
 else {table(['Năm · độ phủ','Thời lượng TB'],Array.from({length:6},(_,i)=>2017+i).map(yr=>{const rows=bundle.weekly.filter(r=>r[0].startsWith(String(yr)));return [yr+' · '+rows.length+' tuần',fmt(mean(rows.map(r=>r[3]/1000)),'tempo')+' giây']}))}
}

// Compute tied ranks so filtered Spearman matrices match pandas.corr.
function tiedRanks(values){const order=values.map((v,i)=>[v,i]).sort((a,b)=>a[0]-b[0]),ranks=[];for(let i=0;i<order.length;){let j=i+1;while(j<order.length&&order[j][0]===order[i][0])j++;for(let k=i;k<j;k++)ranks[order[k][1]]=(i+j+1)/2;i=j}return ranks}
function pearson(a,b){if(a.length<3)return null;const ma=mean(a),mb=mean(b);let s=0,aa=0,bb=0;for(let i=0;i<a.length;i++){const x=a[i]-ma,y=b[i]-mb;s+=x*y;aa+=x*x;bb+=y*y}return aa&&bb?s/Math.sqrt(aa*bb):null}
const corrKeys=[...bundle.features,'artist_popularity_prior','streams_first_8w'];
const corrLabels=[...bundle.features.map(featureLabel),'Tên tuổi nghệ sĩ','Stream 8 tuần'];
function correlationStats(){const rows=current.analysis,columns=corrKeys.map((f,j)=>rows.map(r=>j<9?tv(bundle.tracks[r[0]],f):r[j===9?2:3]));const ranked=columns.map(tiedRanks);return {n:rows.length,z:ranked.map(a=>ranked.map(b=>pearson(a,b)))}}

const baseFigure=figure;
figure=function(key){
 if(key==='correlation'){
   const a=correlationStats();if(!a.n)return {data:[],layout:{}};
   const triangle=a.z.slice(1).map((row,i)=>row.slice(0,-1).map((v,j)=>j<=i?v:null));
   return {data:[{type:'heatmap',x:corrKeys.slice(0,-1),y:corrKeys.slice(1),z:triangle,text:triangle.map(row=>row.map(v=>v===null?'':`<span style="color:${Math.abs(v)>=.5?'#FFFFFF':'#0F172A'}">${v.toFixed(2)}</span>`)),texttemplate:'%{text}',textfont:{size:13},colorscale:correlationScale,zmin:-1,zmax:1,zmid:0,xgap:1,ygap:1,hoverongaps:false,colorbar:{title:{text:'Spearman ρ'},thickness:14,len:.8,tickmode:'array',tickvals:[-1,-.5,-.3,-.1,0,.1,.3,.5,1],tickfont:{size:11,color:'#334155'}},hovertemplate:'%{y} × %{x}<br>ρ = %{z:.3f}<br>'+a.n+' bài · stream 8 tuần đầu<br>Màu tăng tương phản quanh 0; hệ số giữ nguyên<extra></extra>'}],layout:{margin:{l:125,r:15,t:12,b:110},xaxis:{tickvals:corrKeys.slice(0,-1),ticktext:corrLabels.slice(0,-1),tickangle:-40,tickfont:{size:12},showgrid:false},yaxis:{tickvals:corrKeys.slice(1),ticktext:corrLabels.slice(1),autorange:'reversed',tickfont:{size:12},showgrid:false}}};
 }
 if(key==='collab_box')return {data:[0,1].map((c)=>({type:'box',name:c?'Collab':'Solo',y:current.analysis.filter(r=>Number(bundle.tracks[r[0]][3]>1)===c).map(r=>r[3]/1e6),boxpoints:'outliers',marker:{color:softPair[c],size:4},line:{color:softPair[c]},fillcolor:mixHex('#FFFFFF',softPair[c],.25),hovertemplate:'%{x}<br>Stream 8 tuần: %{y:.2f} triệu<extra></extra>'})),layout:{margin:{l:55,r:15,t:15,b:35},showlegend:false,yaxis:{type:'log',title:{text:'Triệu stream · log'}}}};
 const result=baseFigure(key);
 if(key==='collab'&&kind()==='artists'){result.layout.annotations[1].text='Trung vị · 8 tuần';result.data[1].hovertemplate='%{x}<br>Trung vị 8 tuần: %{y:.2f} triệu/bài<br>Trung bình: %{customdata[1]:.2f} triệu/bài<br>%{customdata[0]} bài<extra></extra>'}
 if(key==='map'){
   result.data[0].colorscale=mapScale;
   result.layout.geo.landcolor='#DEE2E7';result.layout.geo.coastlinecolor='#A8B2BC';
   result.layout.geo.lataxis={range:[-60,85]};result.layout.geo.lonaxis={range:[-180,180]};
   const low=result.data[0].zmin,high=result.data[0].zmax;
   const ticks=Array.from({length:7},(_,i)=>low+(high-low)*i/6);
   result.data[0].colorbar={orientation:'h',x:.5,xanchor:'center',y:0,yanchor:'top',len:.8,thickness:18,outlinewidth:0,tickmode:'array',tickvals:ticks,ticktext:ticks.map(v=>v.toFixed(2)),tickfont:{size:12,color:'#334155'},title:{text:featureLabel(state.feature)+' · 6 mức từ thấp → cao',side:'bottom',font:{size:13,color:'#334155'}}};
   result.layout.margin={l:8,r:8,t:5,b:110};
   result.layout.annotations=[{xref:'paper',yref:'paper',x:.5,y:0,yshift:-78,xanchor:'center',yanchor:'top',showarrow:false,text:'■ Không có dữ liệu trong phạm vi chọn',font:{color:'#536170',size:12},bgcolor:'#DEE2E7',borderpad:3}];
   result.data.slice(1).forEach(trace=>{trace.z=[trace.customdata[0][1]];trace.zmin=result.data[0].zmin;trace.zmax=result.data[0].zmax;trace.colorscale=result.data[0].colorscale;trace.marker.line={color:countryColors[trace.locations[0]===state.compare?1:0],width:1.2}});
 }
 if(key==='collab'){result.data[0].textfont.color='#0F172A'}
 if(key==='radar'){result.layout.polar.angularaxis.tickfont.size=12;result.layout.polar.radialaxis.tickfont.size=11;result.data.forEach((trace,i)=>trace.fillcolor=i?'rgba(228,163,179,0.22)':'rgba(159,191,224,0.22)')}
 if(key==='duration'){result.data[0].line.color='#C3D6EA';result.data[1].line.color='#416E9B'}
 if(key==='covid'){result.data[0].marker.color=['valence','liveness'].includes(state.feature)?'rgba(159,191,224,0.70)':'rgba(241,215,124,0.58)';result.data[1].line.width=3.2}
 if(key==='artist_tree'){
   const trace=result.data[0];trace.marker.colors=trace.customdata.map(c=>genreColors[c[1]]||'#E2E8F0');
   trace.textfont.color='#0F172A';
 }
 return result;
};

const baseLink=link;
link=function(key,p){if(key==='correlation'){const f=bundle.features.includes(p?.x)?p.x:bundle.features.includes(p?.y)?p.y:null;if(f){state.feature=f;render();notify('Đã chọn đặc trưng để đọc tương quan và chi tiết')}return}if(key==='collab_box')return baseLink('collab',{x:p?.data?.name});return baseLink(key,p)};

function resize(){document.querySelectorAll('.plot').forEach(el=>{if(el.data)Plotly.relayout(el,{width:el.clientWidth,height:el.clientHeight})})}new ResizeObserver(resize).observe($('dashboard'));

for(const id of ['year','fromyear','toyear','genre','artist','band','collab','region','country','compare','weight','month','feature','split','boundary_y']){
  const el=$(id);
  if(el){
    el.onchange=()=>{
      state[id]=['year','fromyear','toyear'].includes(id)?Number($(id).value):$(id).value;
      if(id==='genre')state.artist='';
      if(id==='fromyear'&&state.fromyear>state.toyear)state.toyear=state.fromyear;
      if(id==='toyear'&&state.toyear<state.fromyear)state.fromyear=state.toyear;
      if(['month','fromyear','toyear'].includes(id))state.weeks=[];
      render();
    };
  }
}

$('tau-slider').oninput=(e)=>{
  state.threshold=Number(e.target.value);
  $('tau-val').textContent='τ = '+state.threshold.toFixed(2);
  render();
};

document.querySelectorAll('.forecast-presets button').forEach(button=>{
  button.onclick=()=>{
    state.threshold=Number(button.dataset.tau);
    $('tau-slider').value=state.threshold;
    $('tau-val').textContent='τ = '+state.threshold.toFixed(2);
    render();
  };
});

document.querySelectorAll('#hit-flow button').forEach(button=>button.onclick=()=>$(button.dataset.focus).focus());
$('prev').onclick=()=>go(position-1);$('next').onclick=$('explore-next').onclick=()=>go(position+1);$('restore').onclick=$('clear').onclick=()=>go(position);
for(const [id,mode] of [['tab-data','data'],['tab-method','method']])$(id).onclick=()=>{detailMode=mode;$('tab-data').className=mode==='data'?'active':'';$('tab-method').className=mode==='method'?'active':'';inspector()};
$('filters-toggle').onclick=()=>{document.body.classList.toggle('inspector-open');resize()};
$('fullscreen').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen()}catch(e){notify('Hãy dùng chế độ toàn màn hình của trình duyệt')}};
$('print').onclick=()=>window.print();
document.addEventListener('keydown',e=>{if(['INPUT','TEXTAREA','SELECT'].includes(e.target.tagName)||$('editor').open||$('guide').open)return;if(e.key==='ArrowRight')go(position+1);if(e.key==='ArrowLeft')go(position-1)});

$('edit').onclick=()=>{$('edit-caption').value=point().caption;$('edit-description').value=dash().description;$('edit-annotation').value=point().annotation;$('editor-sheets').textContent=dash().worksheets.map(k=>book.worksheets[k]||k).join(' · ');$('move-left').disabled=position===0;$('move-right').disabled=position===book.story_points.length-1;$('editor').showModal()};
$('cancel').onclick=()=>$('editor').close();
$('apply').onclick=()=>{if(!$('edit-caption').value.trim())return;point().caption=$('edit-caption').value;point().annotation=$('edit-annotation').value;point().saved_state=clone(state);dash().description=$('edit-description').value;$('editor').close();render();notify('Đã chụp trạng thái · bấm Lưu để giữ khi mở lại')};
function move(n){const j=position+n;[book.story_points[position],book.story_points[j]]=[book.story_points[j],book.story_points[position]];$('editor').close();go(j)}
$('move-left').onclick=()=>move(-1);$('move-right').onclick=()=>move(1);
$('save').onclick=()=>{try{localStorage.setItem(storageKey,JSON.stringify(book));notify('Đã lưu workbook trên trình duyệt')}catch(e){notify('Không lưu được; hãy xuất JSON')}};
$('export').onclick=()=>download('spotify_workbook.json',JSON.stringify(book,null,2),'application/json');
$('open').onclick=()=>$('file').click();
$('file').onchange=async()=>{try{book=validate(JSON.parse(await $('file').files[0].text()));go(0);notify('Đã mở workbook')}catch(e){notify('Không mở được: '+e.message)}$('file').value=''};
$('export-html').onclick=()=>{const doc=document.documentElement.cloneNode(true);doc.querySelectorAll('dialog').forEach(d=>d.removeAttribute('open'));doc.querySelector('#dashboard').replaceChildren();doc.querySelector('#status').textContent='';let html='<!doctype html>'+doc.outerHTML;const a=html.indexOf('const bundle='),b=html.indexOf(';\nconst $',a);if(a<0||b<0){notify('Không xuất được HTML');return}const payload={...bundle,workbook:clone(book)};payload.workbook.story_points[position].saved_state=clone(state);html=html.slice(0,a)+'const bundle='+JSON.stringify(payload).replaceAll('</','<\\/')+html.slice(b);download('spotify_data_story.html',html,'text/html;charset=utf-8');notify('Đã tải story HTML · bản đồ cần mạng để tải địa giới')};
$('help').onclick=()=>$('guide').showModal();$('close-guide').onclick=()=>$('guide').close();
const glossary=document.createElement('p');glossary.style.fontSize='11px';glossary.textContent=Object.entries(meta).map(([f,t])=>f+': '+t).join(' · ');$('glossary').append(glossary);

go(0);
