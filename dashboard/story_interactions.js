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
 if(key==='genre_box')return `${boxLabel[state.boxfeature]} giữa các thể loại`;
 if(key==='artist_tree')return `Lượt nghe ghi nhận cho ${treeRows().length} nghệ sĩ dẫn đầu`;
 if(key==='radar'){const name=code=>{const value=current.allCountries.find(r=>r[0]===code)?.[1]||code;return ({Vietnam:'Việt Nam',Japan:'Nhật Bản'})[value]||value};return `So sánh âm thanh: ${name(state.country)} và ${name(state.compare)}`}
 if(key==='covid')return `${featureLabel(state.feature)} và tử vong COVID-19 theo tuần`;
 return book.worksheets[key];
}
const meta={danceability:'Độ dễ nhảy',energy:'Cường độ năng lượng',valence:'Sắc thái tích cực',acousticness:'Khả năng âm học mộc',speechiness:'Mức hiện diện lời nói',instrumentalness:'Khả năng không có giọng hát',liveness:'Dấu hiệu biểu diễn trực tiếp',loudness:'Âm lượng trung bình · dB',tempo:'Nhịp độ · BPM'};
const fi=f=>bundle.features.indexOf(f),tv=(t,f)=>t[5+fi(f)],cv=(r,f)=>r[(state.weight==='mean'?15:6)+fi(f)],unit=f=>f==='tempo'?'BPM':f==='loudness'?'dB':'0–1';
const mean=a=>{const v=a.filter(Number.isFinite);return v.length?v.reduce((s,x)=>s+x,0)/v.length:null},median=a=>{const v=a.filter(Number.isFinite).sort((a,b)=>a-b),i=Math.floor(v.length/2);return v.length?(v.length%2?v[i]:(v[i-1]+v[i])/2):null};
const fmt=(v,f=state.feature)=>Number.isFinite(v)?v.toFixed(f==='tempo'?1:f==='loudness'?2:3):'—',num=v=>Number.isFinite(v)?v.toLocaleString('vi-VN',{maximumFractionDigits:0}):'—',short=r=>bundle.region_short[r]||r;
const shortStreams=v=>!Number.isFinite(v)?'—':v>=1e9?(v/1e9).toLocaleString('vi-VN',{maximumFractionDigits:2})+' tỷ':(v/1e6).toLocaleString('vi-VN',{maximumFractionDigits:1})+' triệu';
let book=clone(bundle.workbook),position=0,state={},generation=0,detailMode='data',statusTimer,current;
function defaults(s={}){return {year:2021,fromyear:2017,toyear:2022,feature:'danceability',boxfeature:'danceability',region:'Tất cả',country:'VNM',compare:'JPN',weight:'weighted',genre:'',artist:'',band:'',collab:'',month:'',weeks:[],...s}}
const point=()=>book.story_points[position],dash=()=>book.dashboards[point().dashboard_id],kind=()=>dash().id;
function validate(b){if(b.version!==5||!Array.isArray(b.story_points)||b.story_points.length!==4||!b.dashboards)throw Error('Cần workbook v5 với bốn dashboard');for(const p of b.story_points){const d=b.dashboards[p.dashboard_id];if(!d||!['hits','artists','geography','time'].includes(d.id)||typeof p.caption!=='string'||typeof p.annotation!=='string'||typeof d.description!=='string')throw Error('Point không hợp lệ');const s=defaults(p.saved_state);if(!bundle.features.includes(s.feature)||!boxFeatures.includes(s.boxfeature)||![2021,2022].includes(s.year)||!['weighted','mean'].includes(s.weight)||s.fromyear<2017||s.toyear>2022||s.fromyear>s.toyear||!['','0','1','2','3'].includes(s.band)||!['','0','1'].includes(s.collab)||!['',...bundle.genres].includes(s.genre)||!['',...Array.from({length:12},(_,i)=>String(i+1))].includes(s.month)||!Array.isArray(s.weeks))throw Error('Bộ lọc không hợp lệ');p.saved_state=s;d.worksheets=clone(bundle.workbook.dashboards[d.id].worksheets);}b.worksheets=clone(bundle.workbook.worksheets);return b}
const storageKey='spotify-workbook-v5';try{const old=localStorage.getItem(storageKey);if(old)book=validate(JSON.parse(old))}catch(e){console.warn(e.message)}
// Refresh only unchanged legacy copy; preserve any title/caption edited by the user.
if(book.dashboards.hits?.title==='Công thức tạo hit & xu hướng')book.dashboards.hits.title=bundle.workbook.dashboards.hits.title;
for(const p of book.story_points)if(p.dashboard_id==='hits'&&p.caption==='Điều gì đi cùng một bản hit streaming?'){const s=p.saved_state;if(p.annotation===''&&s?.fromyear===2020&&s?.toyear===2022&&s?.feature==='danceability'&&s?.boxfeature==='energy'&&!s.genre&&!s.artist&&s.band===''&&s.collab==='')s.boxfeature='danceability';p.caption=bundle.workbook.story_points.find(x=>x.dashboard_id==='hits').caption}
function options(el,items){el.replaceChildren();for(const [value,text] of items){const o=document.createElement('option');o.value=value;o.textContent=text;el.append(o)}}
for(const id of ['fromyear','toyear'])options($(id),Array.from({length:6},(_,i)=>[2017+i,2017+i]));
options($('genre'),[['','Tất cả thể loại'],...bundle.genres.map(g=>[g,genreLabel(g)])]);
const regions=[...new Set(bundle.countries.map(r=>r[3]))].sort();options($('region'),[['Tất cả','Tất cả khu vực'],...regions.map(r=>[r,short(r)])]);
options($('month'),[['','Cả 12 tháng'],...Array.from({length:12},(_,i)=>[i+1,'Tháng '+(i+1)])]);
function notify(text){clearTimeout(statusTimer);$('status').textContent=text;if(text)statusTimer=setTimeout(()=>$('status').textContent='',4500)}
function download(name,data,type){const a=document.createElement('a'),url=URL.createObjectURL(new Blob([data],{type}));a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1500)}
function nav(){const host=$('navigator');host.replaceChildren();book.story_points.forEach((p,i)=>{const b=document.createElement('button'),label=document.createElement('span');b.className='point'+(i===position?' active':'');label.textContent=book.dashboards[p.dashboard_id].title;b.title=p.caption;b.append(label);b.onclick=()=>go(i);host.append(b)});$('prev').disabled=position===0;$('next').disabled=$('explore-next').disabled=position===book.story_points.length-1}
function go(i){position=Math.max(0,Math.min(book.story_points.length-1,i));state=defaults(clone(point().saved_state));notify('');render()}
function buildModel(){
  const artistSet=state.artist?new Set(bundle.artists[state.artist]?.[2]||[]):null;
  const eligible=new Set(bundle.tracks.flatMap((t,i)=>(!state.genre||t[2]===state.genre)&&(!artistSet||artistSet.has(i))&&(!state.collab||Number(t[3]>1)===Number(state.collab))?[i]:[]));
  const context=bundle.global_rows.filter(r=>eligible.has(r[0])&&r[1]>=state.fromyear&&r[1]<=state.toyear&&(!state.month||r[2]===Number(state.month)));
  const rows=context.filter(r=>state.band===''||r[3]===Number(state.band));
  // Every hit panel must use tracks observed in the selected Global chart period.
  const selectedIndices=new Set(rows.map(r=>r[0]));
  const tracks=bundle.tracks.flatMap((t,i)=>selectedIndices.has(i)?[{t,i}]:[]);
  const countries=bundle.countries.filter(r=>r[2]===state.year&&(state.region==='Tất cả'||r[3]===state.region));
  const allCountries=bundle.countries.filter(r=>r[2]===state.year);
  const weeks=bundle.weekly.filter(r=>Number(r[0].slice(0,4))>=state.fromyear&&Number(r[0].slice(0,4))<=state.toyear);
  const covid=weeks.filter(r=>Number.isFinite(r[13])&&(!state.month||Number(r[0].slice(5,7))===Number(state.month)));
  const analysis=bundle.analysis.filter(r=>eligible.has(r[0])&&Number(r[1].slice(0,4))>=state.fromyear&&Number(r[1].slice(0,4))<=state.toyear);
  return {tracks,context,rows,countries,allCountries,weeks,covid,analysis};
}
function controls(){const k=kind();$('hit-flow').hidden=true;
  const visible={hits:['fromyear','toyear','genre','band','feature'],artists:['fromyear','toyear','genre','artist','collab','feature'],geography:['year','weight','region','country','compare','feature'],time:['fromyear','toyear','month','feature']}[k];
  document.querySelectorAll('.filters label').forEach(el=>{el.hidden=!visible.includes(el.querySelector('select')?.id)});
  if(k==='hits'){state.artist='';state.collab='';state.month='';state.weeks=[]}
  else if(k==='artists'){state.band='';state.month='';state.weeks=[]}
  else {state.genre='';state.artist='';state.band='';state.collab=''}
  const genres=k==='hits'?['pop','latin','k-pop','rap','dance pop']:bundle.genres;
  if(!genres.includes(state.genre))state.genre='';
  options($('genre'),[['','Tất cả thể loại'],...genres.map(g=>[g,genreLabel(g)])]);
  $('genre').closest('label').firstChild.nodeValue=k==='artists'?'Thể loại → nghệ sĩ':'Thể loại';
  $('band').closest('label').classList.toggle('wide',k==='hits');
  $('collab').closest('label').classList.toggle('wide',k==='artists');
  const choices=k==='geography'?mapFeatures:bundle.features;options($('feature'),choices.map(f=>[f,featureLabel(f)]));if(!choices.includes(state.feature))state.feature=choices[0];
  const all=bundle.countries.filter(r=>r[2]===state.year),local=all.filter(r=>state.region==='Tất cả'||r[3]===state.region);
  if(!local.some(r=>r[0]===state.country))state.country=local[0]?.[0]||'';if(!all.some(r=>r[0]===state.compare))state.compare=all[0]?.[0]||'';
  options($('country'),local.slice().sort((a,b)=>a[1].localeCompare(b[1])).map(r=>[r[0],r[1]]));options($('compare'),all.slice().sort((a,b)=>a[1].localeCompare(b[1])).map(r=>[r[0],r[1]]));
  const artists=Object.entries(bundle.artists).filter(([id,a])=>!state.genre||a[1]===state.genre).sort((a,b)=>a[1][0].localeCompare(b[1][0]));if(state.artist&&!artists.some(([id])=>id===state.artist))state.artist='';options($('artist'),[['','Tất cả nghệ sĩ'],...artists.map(([id,a])=>[id,a[0]])]);
  for(const id of ['year','fromyear','toyear','genre','artist','band','collab','region','country','compare','weight','month','feature'])$(id).value=state[id];
  $('scope').textContent=k==='hits'?`${state.fromyear}–${state.toyear} · BXH Global`:k==='geography'?`${local.length} quốc gia · ${state.year} · ${state.weight==='weighted'?'theo stream':'trung bình thường'}`:`${state.fromyear}–${state.toyear} · ${current?.covid.length||0} tuần COVID`;
}
function hitStats(rows=current.context){const accum=Array.from({length:4},()=>bundle.features.map(()=>({n:0,s:0,q:0})));for(const r of rows){const t=bundle.tracks[r[0]];bundle.features.forEach((f,j)=>{const x=tv(t,f);if(Number.isFinite(x)){const a=accum[r[3]][j];a.n+=r[4];a.s+=x*r[4];a.q+=x*x*r[4]}})}
  const baseline=bundle.features.map((_,j)=>{const n=accum.reduce((s,a)=>s+a[j].n,0),s=accum.reduce((s,a)=>s+a[j].s,0),q=accum.reduce((s,a)=>s+a[j].q,0),m=n?s/n:null;return {mean:m,std:n?Math.sqrt(Math.max(0,q/n-m*m)):null,n}});
  const raw=accum.map(a=>a.map(x=>x.n?x.s/x.n:null));const z=raw.map(a=>a.map((m,j)=>m!==null&&baseline[j].std>0?(m-baseline[j].mean)/baseline[j].std:null));return {raw,z,baseline,counts:accum.map(a=>a[0].n)};
}
function collabStats(){
  if(kind()==='artists')return [0,1].map(c=>{const rows=current.analysis.filter(r=>Number(bundle.tracks[r[0]][3]>1)===c),values=rows.map(r=>r[3]);return {type:c?'Collab':'Solo',count:rows.length,charted:rows.length,median:median(values),mean:mean(values)}});
  // Global chart slots are already de-duplicated across artist credits.
  const streamsByTrack=new Map();
  for(const r of current.rows)streamsByTrack.set(r[0],(streamsByTrack.get(r[0])||0)+r[5]);
  return [0,1].map(c=>{
    const ts=current.tracks.filter(({t})=>Number(t[3]>1)===c);
    const streamValues=ts.map(({i})=>streamsByTrack.get(i)||0).filter(v=>v>0);
    return {type:c?'Collab':'Solo',count:ts.length,median:median(streamValues),mean:mean(streamValues),charted:streamValues.length};
  });
}
function treeRows(){const sums=new Map();for(const r of bundle.credits){const a=bundle.artists[r[0]];if(r[1]<state.fromyear||r[1]>state.toyear||state.genre&&a[1]!==state.genre||state.artist&&r[0]!==state.artist||state.band!==''&&r[3]!==+state.band||state.collab!==''&&r[4]!==+state.collab||state.month&&r[2]!==+state.month)continue;sums.set(r[0],(sums.get(r[0])||0)+r[5])}return [...sums].sort((a,b)=>b[1]-a[1]).slice(0,80)}
function figure(key){const f=state.feature,fig={data:[],layout:{}};
 if(key==='hit_heatmap'){const a=hitStats();fig.data=[{type:'heatmap',x:bundle.features,y:bands,z:a.z,text:a.z.map(r=>r.map(v=>v===null?'':Math.abs(v)<.005?'<span style="color:#64748B">0.00</span>':Math.abs(v)>=.11?`<span style="color:#FFFFFF">${v>0?'+':''}${v.toFixed(2)}</span>`:`<span style="color:#1E293B">${v>0?'+':''}${v.toFixed(2)}</span>`)),texttemplate:'%{text}',textfont:{size:14,family:"'Segoe UI', sans-serif"},customdata:a.raw,colorscale:diverge,zmid:0,zmin:-.15,zmax:.15,colorbar:{thickness:12,len:.75,title:{text:'Độ lệch chuẩn hóa',font:{size:12,family:"'Segoe UI', sans-serif"}},tickvals:[-.15,0,.15],ticktext:['Thấp hơn TB','Bằng TB','Cao hơn TB'],tickfont:{size:11,family:"'Segoe UI', sans-serif"}},hovertemplate:'%{y}<br>%{x}<br>Giá trị thực tế: %{customdata:.2f}<br>Độ lệch chuẩn hóa: %{z:+.2f}<extra></extra>'}];fig.layout={margin:{l:85,r:20,t:12,b:72},xaxis:{tickangle:-28,tickfont:{size:13,family:"'Segoe UI', sans-serif"}},yaxis:{autorange:'reversed',tickfont:{size:13,family:"'Segoe UI', sans-serif"}},shapes:[{type:'rect',xref:'paper',yref:'paper',x0:fi(f)/bundle.features.length,x1:(fi(f)+1)/bundle.features.length,y0:0,y1:1,line:{color:'#3A98A8',width:2}}]};if(state.band!=='')fig.layout.shapes.push({type:'rect',xref:'paper',yref:'y',x0:0,x1:1,y0:+state.band-.48,y1:+state.band+.48,line:{color:theme.accent,width:2}})}
 else if(key==='genre_box'){const feature=state.boxfeature,genres=['pop','latin','k-pop','rap','dance pop'];fig.data=genres.map(g=>{const ts=current.tracks.filter(({t})=>t[2]===g&&Number.isFinite(tv(t,feature)));return {type:'box',name:g,y:ts.map(({t})=>tv(t,feature)),customdata:ts.map(({t})=>t[1]),boxmean:true,boxpoints:'outliers',fillcolor:genreBoxColors[g],marker:{color:genreLines[g],size:5},line:{color:genreLines[g],width:2.2},hovertemplate:genreLabel(g)+'<br>'+featureLabel(feature)+': %{y:.4f}<br>%{customdata}<br>'+ts.length+' bài trong nhóm<extra></extra>'}}).filter(t=>t.y.length);fig.layout={margin:{l:44,r:12,t:14,b:42},showlegend:false,xaxis:{categoryorder:'array',categoryarray:genres,tickvals:genres,ticktext:['Pop','Latin','K-Pop','Rap','Dance Pop'],tickfont:{size:13,family:"'Segoe UI', sans-serif"}},yaxis:{title:{text:unit(feature),font:{size:13,family:"'Segoe UI', sans-serif"}},tickfont:{size:13,family:"'Segoe UI', sans-serif"}}}}
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
 else if(key==='duration'){const conditional=state.genre||state.artist||state.band!==''||state.collab!=='';let points;if(conditional){const bins=new Map();for(const r of current.rows){const dur=bundle.tracks[r[0]][14];if(!Number.isFinite(dur))continue;const k=r[1]+'-'+String(r[2]).padStart(2,'0');const b=bins.get(k)||[0,0];b[0]+=dur*r[5];b[1]+=r[5];bins.set(k,b)}points=[...bins].sort((a,b)=>a[0].localeCompare(b[0])).map(([d,a])=>[d+'-01',a[1]?a[0]/a[1]/1000:null])}else points=bundle.weekly.filter(r=>{const year=Number(r[0].slice(0,4));return year>=state.fromyear&&year<=state.toyear}).map(r=>[r[0],r[3]/1000]);const smooth=points.map((r,i)=>mean(points.slice(Math.max(0,i-3),i+1).map(x=>x[1])));fig.data=[{type:'scatter',mode:'lines',name:conditional?'Trung bình tháng':'Trung bình tuần',x:points.map(r=>r[0]),y:points.map(r=>r[1]),line:{color:'#CBD5E1',width:1.5},hovertemplate:'%{x}<br>%{y:.1f} giây<extra></extra>'},{type:'scatter',mode:'lines',name:conditional?'TB 4 tháng':'TB 4 tuần',x:points.map(r=>r[0]),y:smooth,line:{color:'#3B82F6',width:3.0},hovertemplate:'%{x}<br>%{y:.1f} giây<extra></extra>'}];fig.layout={margin:{l:48,r:12,t:28,b:36},xaxis:{tickfont:{size:13,family:"'Segoe UI', sans-serif"}},yaxis:{title:{text:'Giây',font:{size:13,family:"'Segoe UI', sans-serif"}},tickfont:{size:13,family:"'Segoe UI', sans-serif"}},hovermode:'x unified'}}
 else if(key==='map'){const rows=current.countries,all=current.allCountries.map(r=>cv(r,f)).filter(Number.isFinite);fig.data=[{type:'choropleth',locations:rows.map(r=>r[0]),z:rows.map(r=>cv(r,f)),customdata:rows.map(r=>[r[1],r[3],r[5]]),colorscale:[[0,'#FCE4EC'],[.2,'#F8BBD0'],[.4,'#F06292'],[.6,'#E2738E'],[.8,'#880E4F'],[1,'#4A148C']],zmin:Math.min(...all),zmax:Math.max(...all),marker:{line:{color:theme.panel,width:.5}},colorbar:{thickness:8,len:.65,title:{text:f}},hovertemplate:'<b>%{customdata[0]}</b><br>'+f+': %{z:.4f}<br>%{customdata[1]}<br>%{customdata[2]} tuần<extra></extra>'}];for(const [code,color] of [[state.country,countryColors[0]],[state.compare,countryColors[1]]])if(rows.some(r=>r[0]===code))fig.data.push({type:'choropleth',locations:[code],z:[1],showscale:false,colorscale:[[0,color],[1,color]],marker:{line:{color:theme.ink,width:1.5}},customdata:[[current.allCountries.find(r=>r[0]===code)?.[1],cv(current.allCountries.find(r=>r[0]===code),f)]],hovertemplate:'%{customdata[0]}<br>'+f+': %{customdata[1]:.4f}<extra></extra>'});fig.layout={margin:{l:0,r:10,t:5,b:0},geo:{projection:{type:'natural earth'},showframe:false,showland:true,landcolor:'#E8E5DE',showcoastlines:true,coastlinecolor:'#C7C6BF',bgcolor:theme.panel}}}
 else if(key==='radar'){const features=['acousticness','danceability','energy','valence','speechiness','liveness'];for(const [i,code] of [state.country,state.compare].entries()){const row=current.allCountries.find(r=>r[0]===code);if(!row)continue;const values=features.map(f=>cv(row,f));fig.data.push({type:'scatterpolar',r:[...values,values[0]],theta:[...features,features[0]],name:row[1],fill:'toself',line:{color:countryColors[i],width:2},fillcolor:i?'rgba(83,109,254,0.22)':'rgba(226,115,142,0.22)',customdata:[...features,features[0]],hovertemplate:row[1]+'<br>%{theta}: %{r:.4f}<extra></extra>'})}fig.layout={margin:{l:65,r:65,t:40,b:35},polar:{radialaxis:{range:[0,1],tickfont:{size:9}},angularaxis:{tickfont:{size:10}}},legend:{orientation:'h',x:.3,y:1.12}}}
 else if(key==='seasonal'){fig.data=['danceability','acousticness'].map(f=>({type:'bar',x:Array.from({length:12},(_,i)=>i+1),y:Array.from({length:12},(_,m)=>mean(current.weeks.filter(r=>+r[0].slice(5,7)===m+1).map(r=>r[4+fi(f)]))),name:f,customdata:Array.from({length:12},(_,m)=>current.weeks.filter(r=>+r[0].slice(5,7)===m+1).length),marker:{color:featureColors[f],opacity:Array.from({length:12},(_,m)=>!state.month||+state.month===m+1?1:.25)},hovertemplate:'Tháng %{x}<br>'+f+': %{y:.4f}<br>%{customdata} tuần<extra></extra>'}));fig.layout={barmode:'group',margin:{l:42,r:9,t:30,b:35},xaxis:{dtick:1,title:{text:'Tháng trong năm'}},yaxis:{title:{text:'0–1'},range:[0,1]}}}
 else if(key==='covid'){const rows=current.covid,x=[],y=[];let prev=null;for(const r of rows){if(prev&&new Date(r[0])-new Date(prev)>8*86400000){x.push(r[0]);y.push(null)}x.push(r[0]);y.push(r[4+fi(f)]);prev=r[0]}fig.data=[{type:'bar',x:rows.map(r=>r[0]),y:rows.map(r=>r[13]),name:'Tử vong / tuần',yaxis:'y2',marker:{color:'#C9BDB580'},hovertemplate:'%{x}<br>%{y:,.0f} ca<extra></extra>'},{type:'scatter',mode:'lines',x,y,name:f,line:{color:featureColors[f],width:2.6},hovertemplate:'%{x}<br>'+f+': %{y:.4f}<extra></extra>'}];fig.layout={margin:{l:48,r:50,t:30,b:40},hovermode:'x unified',yaxis:{title:{text:f+' · '+unit(f)}},yaxis2:{overlaying:'y',side:'right',title:{text:'Tử vong'},showgrid:false,rangemode:'tozero'},shapes:state.weeks.map(w=>({type:'line',xref:'x',yref:'paper',x0:w,x1:w,y0:0,y1:1,line:{color:theme.accent,width:2,dash:'dot'}}))}}
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
 else return;
 notify('Đã liên kết lựa chọn trong dashboard');render();
}
async function render(){const token=++generation;controls();current=buildModel();controls();nav();$('dashboard-name').textContent=dash().title;$('caption').textContent=point().caption;$('description').textContent=dash().description;$('note').textContent=dash().note;$('note').title=dash().note;$('counter').textContent=`${position+1} / 3 · ${bundle.source.covid_weeks} tuần COVID ghép được`;inspector();
 host=$('dashboard');host.querySelectorAll('.plot').forEach(el=>Plotly.purge(el));host.replaceChildren();host.className='dashboard '+(kind()==='geography'?'geo':kind());
 for(const key of dash().worksheets){const panel=document.createElement('article');panel.className='panel panel-'+key;const head=document.createElement('div');head.className='panel-head';const title=document.createElement('h2');title.textContent=chartTitle(key);title.title=title.textContent;const tools=document.createElement('div');
 if(key==='genre_box'){const select=document.createElement('select');select.setAttribute('aria-label','Chỉ số boxplot');options(select,boxFeatures.map(f=>[f,featureLabel(f)]));select.value=state.boxfeature;select.onchange=()=>{state.boxfeature=select.value;render()};tools.append(select)}
 if(key==='artist_tree'&&(state.genre||state.artist)){const up=document.createElement('button');up.textContent='↑ Gốc';up.title='Quay về toàn bộ thể loại/nghệ sĩ';up.onclick=()=>{state.genre='';state.artist='';render()};tools.append(up)}
 const png=document.createElement('button'),csv=document.createElement('button');png.textContent='PNG';png.title='Tải ảnh biểu đồ';csv.textContent='CSV';csv.title='Tải dữ liệu biểu đồ';tools.append(png,csv);head.append(title,tools);const el=document.createElement('div');el.className='plot';panel.append(head,el);host.append(panel);
 const fig=figure(key);if(key==='artist_tree'){const tree=fig.data[0];tree.labels=tree.labels.map((label,i)=>tree.ids[i].startsWith('g:')?genreLabel(label):label);tree.text=tree.text.map((label,i)=>tree.ids[i].startsWith('g:')?genreLabel(label):label);if(el.clientWidth<420&&!state.genre&&!state.artist)tree.maxdepth=2}fig.layout={paper_bgcolor:theme.panel,plot_bgcolor:theme.panel,colorway:colors,font:{family:"'Segoe UI', sans-serif",size:el.clientWidth<350?11:13,color:theme.ink},legend:{orientation:'h',x:0,y:1.13,font:{size:13,family:"'Segoe UI', sans-serif"}},hoverlabel:{bgcolor:theme.ink,font:{color:'#FFFEFB',size:13,family:"'Segoe UI', sans-serif"}},...fig.layout,height:el.clientHeight,width:el.clientWidth};
 if(key==='hit_heatmap'){fig.layout.xaxis.tickvals=bundle.features;fig.layout.xaxis.tickangle=-28;fig.layout.xaxis.ticktext=['Danceability','Energy','Valence','Acousticness','Speechiness','Instrumentalness','Liveness','Loudness','Tempo'];fig.layout.xaxis.tickfont={size:13,family:"'Segoe UI', sans-serif"};fig.layout.margin.b=72;if(el.clientWidth<580){fig.layout.xaxis.tickfont.size=11;fig.data[0].textfont.size=12}if(el.clientWidth<400){fig.layout.margin.l=65;fig.layout.margin.b=50;fig.data[0].textfont.size=10}}
 if(!fig.data.length){el.className+=' empty';el.textContent='Không có dữ liệu trong phạm vi chọn';continue}
 await Plotly.newPlot(el,fig.data,fig.layout,{responsive:true,displaylogo:false,displayModeBar:'hover',modeBarButtonsToRemove:['toImage']});if(token!==generation)return;
 if(key==='artist_tree')el.on('plotly_treemapclick',e=>{setTimeout(()=>link(key,e.points?.[0]),0);return false});else el.on('plotly_click',e=>link(key,e.points?.[0]));png.onclick=async()=>{try{const url=await Plotly.toImage(el,{format:'png',width:key==='hit_heatmap'?1600:1200,height:800});download(key+'.png',await fetch(url).then(r=>r.blob()),'image/png')}catch(e){notify('Không xuất được PNG: '+e.message)}};csv.onclick=()=>exportCsv(chartRows(key),key);
 }
}
function chartRows(key){if(key==='hit_heatmap'){const a=hitStats();return bands.flatMap((band,i)=>bundle.features.map((f,j)=>({rank_band:band,feature:f,mean:a.raw[i][j],z_score:a.z[i][j],slots:a.counts[i]})))}
 if(key==='genre_box')return current.tracks.filter(({t})=>['pop','latin','k-pop','rap','dance pop'].includes(t[2])).map(({t})=>({track_id:t[0],track_name:t[1],genre:t[2],feature:state.boxfeature,value:tv(t,state.boxfeature)}));
 if(key==='artist_tree')return treeRows().map(([id,v])=>({artist:bundle.artists[id][0],genre:bundle.artists[id][1],credited_streams:v}));
 if(key==='collab')return collabStats().map(r=>({type:r.type,global_chart_tracks:r.count,tracks_with_streams:r.charted,median_global_streams:r.median,mean_global_streams:r.mean}));
 if(key==='duration'){const fig=figure(key);return fig.data[0].x.map((date,i)=>({date,duration_seconds:fig.data[0].y[i],rolling_4:fig.data[1].y[i]}))}
 if(['map','radar'].includes(key))return (key==='radar'?current.allCountries.filter(r=>[state.country,state.compare].includes(r[0])):current.countries).map(r=>({country:r[1],code:r[0],year:r[2],region:r[3],weight:state.weight,...Object.fromEntries(bundle.features.map(f=>[f,cv(r,f)]))}));
 if(key==='seasonal')return Array.from({length:12},(_,i)=>({month:i+1,weeks:current.weeks.filter(r=>+r[0].slice(5,7)===i+1).length,...Object.fromEntries(['danceability','acousticness'].map(f=>[f,mean(current.weeks.filter(r=>+r[0].slice(5,7)===i+1).map(r=>r[4+fi(f)]))]))}));
 return current.covid.map(r=>({week:r[0],weekly_deaths:r[13],...Object.fromEntries(bundle.features.map(f=>[f,r[4+fi(f)]]))}));
}
function exportCsv(rows,key){if(!rows.length){notify('Phạm vi này không có dữ liệu');return}const columns=Object.keys(rows[0]),quote=v=>'"'+String(v??'').replaceAll('"','""')+'"';download(key+'.csv','\ufeff'+[columns.map(quote).join(','),...rows.map(r=>columns.map(k=>quote(r[k])).join(','))].join('\r\n'),'text/csv;charset=utf-8')}
function table(headers,rows){const host=$('detail'),t=document.createElement('table'),thead=document.createElement('thead'),h=document.createElement('tr');headers.forEach(text=>{const th=document.createElement('th');th.textContent=text;h.append(th)});thead.append(h);t.append(thead);const body=document.createElement('tbody');for(const values of rows){const tr=document.createElement('tr');for(const value of values){const td=document.createElement('td');if(value&&typeof value==='object'&&value.action){const b=document.createElement('button');b.textContent=value.label;b.onclick=value.action;td.append(b)}else td.textContent=value??'—';tr.append(td)}body.append(tr)}t.append(body);host.append(t)}
function insight(){const k=kind(),f=state.feature;let evidence='',hypothesis='',context='',metrics=[];
 if(k==='hits'){
   const a=hitStats(),j=fi(f),c=collabStats(),z=a.z[0][j];
   const ratio=c[0].median>0&&Number.isFinite(c[1].median)?c[1].median/c[0].median:null;
   const rankText=Number.isFinite(z)?Math.abs(z)<.005?`Top 10 có ${featureLabel(f)} tương đương mức trung bình toàn bảng xếp hạng.`:`Top 10 có ${featureLabel(f)} ${z>0?'vượt trội':'thấp hơn'} so với mức trung bình toàn BXH (${z>0?'+':''}${z.toFixed(2)} điểm chuẩn).`:`Top 10 chưa đủ dữ liệu về ${featureLabel(f)}.`;
   const collabText=ratio===null?'Dữ liệu phân hóa giữa hai hình thức biểu diễn.':ratio>1?`Bài hợp tác đạt trung vị ${(c[1].median/1e6).toFixed(1)} triệu stream, cao hơn đơn ca ${((ratio-1)*100).toFixed(0)}%.`:`Bài đơn ca và hợp tác có lượng stream trung vị xấp xỉ nhau (${(c[0].median/1e6).toFixed(1)} triệu stream).`;
   evidence=[rankText,collabText].join(' ');
   hypothesis=ratio>1?'Hợp tác nghệ sĩ tạo hiệu ứng cộng hưởng người nghe giúp bứt phá lượt stream.':'Cơ cấu thể loại và thời điểm ra mắt đóng vai trò quyết định độ phổ biến.';
   if(state.artist&&bundle.artists[state.artist]){const artist=bundle.artists[state.artist],credited=treeRows().find(([id])=>String(id)===String(state.artist))?.[1];context=`Nghệ sĩ ${artist[0]} (${genreLabel(artist[1])}) ghi nhận ${shortStreams(credited)} stream được ghi công.`}
   else if(state.genre)context=`Thể loại ${genreLabel(state.genre)} có ${num(current.tracks.length)} bài lọt BXH Global giai đoạn ${state.fromyear}–${state.toyear}.`;
 }
 else if(k==='geography'){
   const a=current.allCountries.find(r=>r[0]===state.country),b=current.allCountries.find(r=>r[0]===state.compare);
   if(a&&b){
     const va=cv(a,f),vb=cv(b,f);
     evidence=`${a[1]} ghi nhận ${featureLabel(f)} ở mức ${fmt(va)}, trong khi ${b[1]} đạt ${fmt(vb)} (chênh lệch ${fmt(Math.abs(va-vb))} ${unit(f)}).`;
     metrics=[[a[1]+' · '+f,fmt(va)],[b[1]+' · '+f,fmt(vb)]];
   } else evidence='Không có đủ dữ liệu cho cặp quốc gia đã chọn.';
   hypothesis='Khác biệt âm học phản ánh thói quen thưởng thức âm nhạc và ngôn ngữ đặc trưng giữa các khu vực.';
 }
 else {
   const december=current.weeks.filter(r=>+r[0].slice(5,7)===12),other=current.weeks.filter(r=>+r[0].slice(5,7)!==12),dm=mean(december.map(r=>r[4])),om=mean(other.map(r=>r[4])),delta=dm!==null&&om!==null?dm-om:null;
   const cutoff=median(current.covid.map(r=>r[13])),hi=current.covid.filter(r=>r[13]>=cutoff),lo=current.covid.filter(r=>r[13]<cutoff),dh=mean(hi.map(r=>r[4+fi(f)])),dl=mean(lo.map(r=>r[4+fi(f)]));
   evidence=`Tháng 12 ghi nhận tính chu kỳ rõ rệt với độ mộc mạc tăng cao; các tuần đỉnh dịch có ${featureLabel(f)} đạt ${dh!==null?fmt(dh):'—'} so với ${dl!==null?fmt(dl):'—'} ở tuần thấp điểm.`;
   hypothesis='Mùa lễ hội cuối năm và biến cố đại dịch thúc đẩy xu hướng nghe các giai điệu êm dịu, an ủi tinh thần.';
   const selected=current.covid.filter(r=>state.weeks.includes(r[0]));
   metrics=[['Tuần COVID có dữ liệu',num(current.covid.length)],[f+(selected.length?' · tuần chọn':' · trung bình'),fmt(mean((selected.length?selected:current.covid).map(r=>r[4+fi(f)])))]];
 }
 return {evidence,hypothesis,context,metrics};
}
function inspector(){const data=insight();document.querySelector('.inspector').classList.toggle('inspector-hits',kind()==='hits');$('metrics').replaceChildren();for(const [label,value] of data.metrics){const box=document.createElement('div');box.className='metric';const small=document.createElement('small'),strong=document.createElement('strong');small.textContent=label;strong.textContent=value;box.append(small,strong);$('metrics').append(box)}$('insight').replaceChildren();if(data.context){const context=document.createElement('span');context.className='insight-context';context.textContent=data.context;$('insight').append(context)}const observed=document.createElement('span'),possible=document.createElement('span');observed.textContent=point().annotation||data.evidence;possible.className='hypothesis';possible.textContent=(kind()==='hits'?'Diễn giải: ':'Giả thuyết: ')+data.hypothesis;$('insight').append(observed,possible);$('detail').replaceChildren();
 if(detailMode==='method'){const texts=[meta[state.feature]+' · '+unit(state.feature),dash().note,kind()==='hits'?'Cùng phạm vi năm và tầng hạng: heatmap tính theo lần xuất hiện BXH; boxplot và donut tính mỗi bài một lần. Cột Solo/Collab là trung vị tổng stream Global của từng bài trong phạm vi lọc, đã bỏ dòng lặp nghệ sĩ; hover cho xem thêm trung bình. Treemap hiện thể loại trước trên màn hình hẹp: bấm thể loại để xem nghệ sĩ. Z-score đo độ lệch của từng nhóm so với mức trung bình chung của toàn bộ bảng xếp hạng.':kind()==='geography'?'Radar giữ giá trị gốc 0–1; cả hai nước và bản đồ cùng phương pháp. Trung bình thường không giống trung bình theo luồng nghe.':'Mùa vụ dùng tất cả tuần Global trong năm chọn; COVID chỉ các tuần ghép được. Các năm và tháng có số tuần khác nhau.'];for(const text of texts){const p=document.createElement('p');p.textContent=text;$('detail').append(p)}return}
 if(kind()==='hits'){if(state.artist||state.genre){const ranked=treeRows().slice(0,6);table(['Nghệ sĩ · drill-down','Stream ghi công'],ranked.map(([id,v])=>[{label:bundle.artists[id][0],action:()=>{state.artist=id;state.genre=bundle.artists[id][1];render()}},(v/1e9).toFixed(2)+' tỷ']))}else {const a=hitStats(),j=fi(state.feature);table(['Nhóm hạng','z · '+state.feature],bands.map((b,i)=>[{label:b,action:()=>{state.band=String(i);render()}},fmt(a.z[i][j])+' điểm']));const c=collabStats();const p=document.createElement('p');p.textContent=c.map(r=>r.type+': '+r.count+' bài BXH Global; trung vị '+(r.median===null?'—':(r.median/1e6).toFixed(1))+' triệu/bài; trung bình '+(r.mean===null?'—':(r.mean/1e6).toFixed(1))+' triệu/bài').join(' · ');$('detail').append(p)}}
 else if(kind()==='geography'){const a=current.allCountries.find(r=>r[0]===state.country),b=current.allCountries.find(r=>r[0]===state.compare);table(['Đặc trưng',a?.[1]||'A',b?.[1]||'B'],bundle.features.map(f=>[{label:f,action:()=>{if(mapFeatures.includes(f)){state.feature=f;render()}else notify(meta[f])}},a?fmt(cv(a,f),f):'—',b?fmt(cv(b,f),f):'—']))}
 else if(state.weeks.length){const r=current.covid.find(r=>state.weeks.includes(r[0]));if(r){table(['Tuần '+r[0],'Giá trị'],bundle.features.map(f=>[{label:f,action:()=>{state.feature=f;render()}},fmt(r[4+fi(f)],f)]))}}
 else if(state.month){const sums=new Map();for(const r of bundle.global_rows){if(r[1]>=state.fromyear&&r[1]<=state.toyear&&r[2]===+state.month)sums.set(r[0],(sums.get(r[0])||0)+r[5])}table(['Top bài · tháng '+state.month,'Stream Global'],[...sums].sort((a,b)=>b[1]-a[1]).slice(0,6).map(([i,v])=>[bundle.tracks[i][1],(v/1e6).toFixed(1)+' tr']))}
 else {table(['Năm · độ phủ','Thời lượng TB'],Array.from({length:6},(_,i)=>2017+i).map(yr=>{const rows=bundle.weekly.filter(r=>r[0].startsWith(String(yr)));return [yr+' · '+rows.length+' tuần',fmt(mean(rows.map(r=>r[3]/1000)),'tempo')+' giây']}))}
}
function resize(){document.querySelectorAll('.plot').forEach(el=>{if(el.data)Plotly.relayout(el,{width:el.clientWidth,height:el.clientHeight})})}new ResizeObserver(resize).observe($('dashboard'));
for(const id of ['year','fromyear','toyear','genre','artist','band','collab','region','country','compare','weight','month','feature'])$(id).onchange=()=>{state[id]=['year','fromyear','toyear'].includes(id)?Number($(id).value):$(id).value;if(id==='genre')state.artist='';if(id==='fromyear'&&state.fromyear>state.toyear)state.toyear=state.fromyear;if(id==='toyear'&&state.toyear<state.fromyear)state.fromyear=state.toyear;if(['month','fromyear','toyear'].includes(id))state.weeks=[];render()};
document.querySelectorAll('#hit-flow button').forEach(button=>button.onclick=()=>$(button.dataset.focus).focus());
$('prev').onclick=()=>go(position-1);$('next').onclick=$('explore-next').onclick=()=>go(position+1);$('restore').onclick=$('clear').onclick=()=>go(position);for(const [id,mode] of [['tab-data','data'],['tab-method','method']])$(id).onclick=()=>{detailMode=mode;$('tab-data').className=mode==='data'?'active':'';$('tab-method').className=mode==='method'?'active':'';inspector()};
$('filters-toggle').onclick=()=>{document.body.classList.toggle('inspector-open');resize()};$('fullscreen').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen()}catch(e){notify('Hãy dùng chế độ toàn màn hình của trình duyệt')}};$('print').onclick=()=>window.print();document.addEventListener('keydown',e=>{if(['INPUT','TEXTAREA','SELECT'].includes(e.target.tagName)||$('editor').open||$('guide').open)return;if(e.key==='ArrowRight')go(position+1);if(e.key==='ArrowLeft')go(position-1)});
$('edit').onclick=()=>{$('edit-caption').value=point().caption;$('edit-description').value=dash().description;$('edit-annotation').value=point().annotation;$('editor-sheets').textContent=dash().worksheets.map(k=>book.worksheets[k]).join(' · ');$('move-left').disabled=position===0;$('move-right').disabled=position===book.story_points.length-1;$('editor').showModal()};$('cancel').onclick=()=>$('editor').close();$('apply').onclick=()=>{if(!$('edit-caption').value.trim())return;point().caption=$('edit-caption').value;point().annotation=$('edit-annotation').value;point().saved_state=clone(state);dash().description=$('edit-description').value;$('editor').close();render();notify('Đã chụp trạng thái · bấm Lưu để giữ khi mở lại')};function move(n){const j=position+n;[book.story_points[position],book.story_points[j]]=[book.story_points[j],book.story_points[position]];$('editor').close();go(j)}$('move-left').onclick=()=>move(-1);$('move-right').onclick=()=>move(1);
$('save').onclick=()=>{try{localStorage.setItem(storageKey,JSON.stringify(book));notify('Đã lưu workbook v5 trên trình duyệt')}catch(e){notify('Không lưu được; hãy xuất JSON')}};$('export').onclick=()=>download('spotify_workbook_v5.json',JSON.stringify(book,null,2),'application/json');$('open').onclick=()=>$('file').click();$('file').onchange=async()=>{try{book=validate(JSON.parse(await $('file').files[0].text()));go(0);notify('Đã mở workbook')}catch(e){notify('Không mở được: '+e.message)}$('file').value=''};
$('export-html').onclick=()=>{const doc=document.documentElement.cloneNode(true);doc.querySelectorAll('dialog').forEach(d=>d.removeAttribute('open'));doc.querySelector('#dashboard').replaceChildren();doc.querySelector('#status').textContent='';let html='<!doctype html>'+doc.outerHTML;const a=html.indexOf('const bundle='),b=html.indexOf(';\nconst $',a);if(a<0||b<0){notify('Không xuất được HTML');return}const payload={...bundle,workbook:clone(book)};payload.workbook.story_points[position].saved_state=clone(state);html=html.slice(0,a)+'const bundle='+JSON.stringify(payload).replaceAll('</','<\\/')+html.slice(b);download('spotify_data_story.html',html,'text/html;charset=utf-8');notify('Đã tải story HTML · bản đồ cần mạng để tải địa giới')};
$('help').onclick=()=>$('guide').showModal();$('close-guide').onclick=()=>$('guide').close();const glossary=document.createElement('p');glossary.style.fontSize='11px';glossary.textContent=Object.entries(meta).map(([f,t])=>f+': '+t).join(' · ');$('glossary').append(glossary);

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
   // Keep the measured fill; selection is an outline, never a replacement value.
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
const baseRows=chartRows;
chartRows=function(key){if(key==='correlation'||key==='collab_box')return current.analysis.map(r=>({track:bundle.tracks[r[0]][1],entry:r[1],artist_popularity_prior:r[2],streams_first_8w:r[3],...Object.fromEntries(bundle.features.map(f=>[f,tv(bundle.tracks[r[0]],f)]))}));if(key==='collab'&&kind()==='artists')return collabStats().map(r=>({type:r.type,tracks:r.count,median_streams_first_8w:r.median,mean_streams_first_8w:r.mean}));return baseRows(key)};
const baseInsight=insight;
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
 // Compare group-mean ranges using the same chart appearances and metric.
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
insight=function(){
 if(kind()==='hits'){const a=hitStats(),j=fi(state.feature),z=a.z[0][j];return {evidence:Number.isFinite(z)?`Top 10 có ${featureLabel(state.feature)} ${z>=0?'cao':'thấp'} hơn nền BXH ${Math.abs(z).toFixed(2)} SD. Boxplot đối chiếu phân phối giữa các thể loại trong phạm vi chọn.`:'Không đủ dữ liệu cho nhóm Top 10.',hypothesis:'Khác biệt có thể gắn với cấu trúc thể loại và ngữ cảnh nghe. Mức chênh lệch không phải xác suất tạo hit.',context:'Hồ sơ âm thanh → khác biệt theo thể loại',metrics:[]}}
 if(kind()==='artists'){
   const a=correlationStats(),j=fi(state.feature),rho=a.z[9][10],audio=a.z[j][10],c=collabStats(),ratio=c[0].median>0?c[1].median/c[0].median:null;
   return {evidence:`Tên tuổi trước khi vào BXH: ρ = ${fmt(rho)} với stream 8 tuần đầu; ${featureLabel(state.feature)}: ρ = ${fmt(audio)}. ${ratio!==null&&Number.isFinite(ratio)?`Trung vị Collab ${ratio>=1?'cao':'thấp'} hơn Solo ${Math.abs((ratio-1)*100).toFixed(1)}%.`:'Chưa đủ hai nhóm để so sánh.'}`,hypothesis:'Tên tuổi và hợp tác có thể mở rộng tệp khán giả. Tương quan mô tả mối liên hệ; chưa tách ảnh hưởng của thể loại, năm và quy mô phát hành.',context:`${num(a.n)} bài · cùng cửa sổ 8 tuần · nghệ sĩ ghi nhận trong dữ liệu bài hát`,metrics:[]};
 }
 if(kind()==='time'){
   const dec=current.weeks.filter(r=>+r[0].slice(5,7)===12),rest=current.weeks.filter(r=>+r[0].slice(5,7)!==12),ad=mean(dec.map(r=>r[7])),ar=mean(rest.map(r=>r[7]));
   const rho=pearson(current.covid.map(r=>r[13]),current.covid.map(r=>r[4+fi(state.feature)]));
   return {evidence:`Acousticness tháng 12: ${fmt(ad)}, các tháng khác: ${fmt(ar)}. ${featureLabel(state.feature)} và tử vong tuần: Pearson r = ${fmt(rho)} (${current.covid.length} tuần).`,hypothesis:'Catalog nhạc lễ hội có thể tạo chu kỳ cuối năm. Cần kiểm soát mùa vụ trước khi gắn biến động âm học với đại dịch; số tử vong không đo trực tiếp phong tỏa.',context:'Xu hướng dài hạn → mùa vụ → đồng biến động COVID',metrics:[]};
 }
 const data=baseInsight();data.hypothesis='Khác biệt có thể gắn với cơ cấu thể loại và bài hát phổ biến từng thị trường. Đặc trưng âm thanh không trực tiếp đo tâm lý hay toàn bộ văn hóa nghe nhạc.';return data;
};
const baseInspector=inspector;
inspector=function(){baseInspector();const conclusion=document.createElement('span');conclusion.className='story-conclusion';conclusion.textContent='Kết luận: '+({hits:'Hồ sơ âm thanh phân hóa theo tầng hạng và thể loại; không có một chỉ số duy nhất đại diện thành công.',artists:'Đánh giá thành tích cùng cả âm thanh, nền tảng nghệ sĩ và hình thức hợp tác.',geography:'Cùng khu vực địa lý vẫn có thể có hồ sơ âm thanh khác nhau.',time:'Tách chu kỳ mùa vụ khỏi xu hướng dài hạn trước khi giải thích biến động đại dịch.'}[kind()]);$('insight').append(conclusion);if(kind()!=='artists')return;$('detail').replaceChildren();if(detailMode==='method'){for(const text of [dash().note,'Loại 52 tuần đầu để tích lũy lịch sử và loại bài chưa đủ 8 tuần theo dõi. Chỉ số nghệ sĩ thuộc nghệ sĩ được ghi nhận trong bảng bài hát; không tổng hợp điểm mọi nghệ sĩ hợp tác.','Treemap là stream ghi công trong giai đoạn chọn; tổng các nghệ sĩ có thể lặp stream bài hợp tác.']){const p=document.createElement('p');p.textContent=text;$('detail').append(p)}return}const a=correlationStats();table(['Yếu tố','ρ với stream 8 tuần'],corrKeys.slice(0,10).map((f,i)=>[f==='artist_popularity_prior'?'Tên tuổi nghệ sĩ':featureLabel(f),fmt(a.z[i][10])]).sort((a,b)=>Number(b[1])-Number(a[1])))};
const storyInspector=inspector;
inspector=function(){storyInspector();if(detailMode==='method'&&kind()==='hits'){$('detail').replaceChildren();for(const text of ['Z-score = (trung bình nhóm − trung bình toàn BXH) / độ lệch chuẩn toàn BXH. Tính theo lần xuất hiện bài–tuần, không lặp nghệ sĩ.','Bấm ô chọn tầng hạng và đặc trưng; boxplot lọc theo tầng đã chọn. Dropdown boxplot có bốn chỉ số riêng.','Khác biệt âm học mô tả bài hát đã vào BXH, không đánh giá xác suất vào BXH của toàn bộ bài phát hành.']){const p=document.createElement('p');p.textContent=text;$('detail').append(p)}}};
const baseRender=render;
const detailedInspector=inspector;
inspector=function(){detailedInspector();const stories={hits:audioStory,artists:artistStory,geography:geographyStory,time:timeStory};if(!stories[kind()])return;$('insight').replaceChildren();for(const [heading,text] of stories[kind()]()){const paragraph=document.createElement('p'),title=document.createElement('strong');paragraph.className='audio-story-item';paragraph.style.whiteSpace='pre-line';title.textContent=heading+': ';paragraph.append(title,document.createTextNode(text));$('insight').append(paragraph)}};
render=async function(){await baseRender();$('counter').textContent=`${position+1} / ${book.story_points.length}`;if(kind()==='artists'){const panel=document.querySelector('.panel-collab,.panel-collab_box');if(panel){const toggle=document.createElement('select');toggle.setAttribute('aria-label','Cách xem Solo và Collab');options(toggle,[['collab','Cơ cấu & trung vị'],['collab_box','Phân phối chi tiết']]);toggle.value=dash().worksheets[2];toggle.onchange=()=>{dash().worksheets[2]=toggle.value;render()};panel.querySelector('.panel-head>div').prepend(toggle)}}};
go(0);
