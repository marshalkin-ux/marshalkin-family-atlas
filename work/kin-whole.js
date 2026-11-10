const whole=get('whole-svg'), frame=get('whole'), routeBox=get('whole-route');
const view={x:0,y:0,z:1},mapW=1000,mapH=610,cx=500,cy=305;
let detailView=false,previousRoute=[],initializedMap=false;
const kinSets=new Map(people.map(n=>[n.id,n.id]));
function rep(id){let current=id;while(kinSets.get(current)!==current)current=kinSets.get(current);return current}
for(const n of people){const mates=n.spouseIds||(n.id==='K30'?['K30b']:[]);for(const m of mates)if(by.has(m)){const a=rep(n.id),b=rep(m);if(a!==b)kinSets.set(b,a)}}
const families=new Map();
for(const n of people){const k=rep(n.id);if(!families.has(k))families.set(k,{members:[],kids:[],parent:null,weight:1});families.get(k).members.push(n)}
const unit=id=>families.get(rep(id));
for(const u of families.values()){
for(const n of u.members){const older=n.parents.find(id=>by.has(id)&&unit(id)!==u);if(older){u.parent=unit(older);break}}
if(u.parent)u.parent.kids.push(u);
}
const roots=[...families.values()].filter(u=>!u.parent);
function weigh(u){const descendants=u.kids.reduce((v,k)=>v+weigh(k),0);return u.weight=Math.max(u.members.length*.7,descendants,1)}
roots.forEach(weigh);
const palette=['#99c5a5','#dbab76','#96c9d0','#d29782','#b6bddf','#c8c58b','#abccbb','#d4acc7'];
const chosen=grouped?['full-F11','full-L105','full-L175','full-L311','full-H477','full-F569','full-H29','full-J636']:['G3','G14','G29','E39'];
const principal=grouped?['full-B9','full-D10','full-J104','full-H29','full-L105','full-L175','full-L311','full-H477','full-F569','full-F11']:['B14','C14','F14','G3','G14','G29','E39'];
const positions=new Map(),rankMap=new Map();
function place(u,start,end,inherited){
const member=u.members.find(p=>chosen.includes(p.id));u.color=member?palette[chosen.indexOf(member.id)%palette.length]:inherited;
const middle=(start+end)/2;let left=start;
for(const k of u.kids){const span=(end-start)*k.weight/u.kids.reduce((sum,c)=>sum+c.weight,0);place(k,left,left+span,u.color);left+=span}
u.members.forEach((p,i)=>{
const a=middle+(i-(u.members.length-1)/2)*Math.min((end-start)/(u.members.length+1),.055);
const pt={p,a,color:u.color};positions.set(p.id,pt);if(!rankMap.has(p.gen))rankMap.set(p.gen,[]);rankMap.get(p.gen).push(pt);
});
}
const gap=.056,extra=.08,sumWeight=roots.reduce((v,u)=>v+u.weight,0);
let start=-Math.PI*.92;
roots.forEach((u,i)=>{const span=extra+(Math.PI*2-roots.length*(gap+extra))*u.weight/sumWeight;place(u,start,start+span,palette[i%palette.length]);start+=span+gap});
for(const [gen,pts] of rankMap){
pts.sort((a,b)=>a.a-b.a);const radius=.08+.90*(gen-1)/Math.max(1,generations-1);
const separation=Math.min(.037/Math.max(.3,radius),5.9/pts.length);
const low=-Math.PI*.92,high=low+Math.PI*2;
let last=low-separation;for(const pt of pts){pt.a=Math.max(pt.a,last+separation);last=pt.a}
last=high+separation;for(let i=pts.length-1;i>=0;i--){const pt=pts[i];pt.a=Math.min(pt.a,last-separation);last=pt.a;pt.x=cx+Math.cos(pt.a)*462*radius;pt.y=cy+Math.sin(pt.a)*275*radius}
}
const fmt=v=>v.toFixed(2), coord=pt=>fmt(pt.x)+' '+fmt(pt.y);
function curved(a,b){const mx=(a.x+b.x)/2,my=(a.y+b.y)/2;
return 'M'+coord(a)+' Q'+fmt(mx+(a.y-b.y)*.08)+' '+fmt(my+(b.x-a.x)*.08)+' '+coord(b)}
const edgesHtml=[],spouseLinks=new Set();
for(const p of people){const v=positions.get(p.id);if(!v)continue;
for(const older of p.parents){const a=positions.get(older);if(a)edgesHtml.push('<path class="whole-path" data-pa="'+older+'" data-ch="'+p.id+'" stroke="'+v.color+'" d="'+curved(a,v)+'"'+(p.uncertain?' stroke-dasharray="3 2"':'')+'/>')}
for(const mate of p.spouseIds||(p.id==='K30'?['K30b']:[])){const k=[p.id,mate].sort().join('/');if(spouseLinks.has(k)||!positions.has(mate))continue;spouseLinks.add(k);edgesHtml.push('<path class="whole-mate" d="'+curved(v,positions.get(mate))+'"/>')}
}
const labelBoxes=[];
function headline(pt){const p=pt.p,txt=p.name.replace(/\s*\(.*$/,'')+(p.year?' · '+p.year:''),tw=txt.length*6.6+9;
const offsets=[[9,-5],[9,14],[9,-19],[-tw-8,-6],[-tw-8,17],[16,-31],[-tw-15,31],[14,39]];
const fits=(x,y)=>x>2&&x+tw<mapW-2&&y>12&&y<mapH-3&&!labelBoxes.some(b=>x<b.x+b.w+4&&x+tw>b.x-4&&y-13<b.y+4&&y>b.y-13);
let labelPos=null;for(const [dx,dy] of offsets){const x=pt.x+dx,y=pt.y+dy;if(fits(x,y)){labelPos={x,y,w:tw};break}}
if(!labelPos)return '';labelBoxes.push(labelPos);const {x,y}=labelPos;
return '<g class="whole-head" data-who="'+p.id+'" role="button" tabindex="0"><path d="M'+coord(pt)+' L'+fmt(x+(x<pt.x?tw:0))+' '+fmt(y-4)+'" stroke="'+pt.color+'"/><rect x="'+fmt(x-2)+'" y="'+fmt(y-13)+'" width="'+fmt(tw)+'" height="16" rx="3"/><text x="'+fmt(x+2)+'" y="'+fmt(y)+'">'+esc(txt)+'</text></g>'
}
const nodeHTML=[...positions.values()].map(pt=>{const p=pt.p;return '<g class="whole-dot" data-who="'+p.id+'" role="button" aria-label="'+esc(label(p))+'" transform="translate('+coord(pt)+')"><title>'+esc(label(p))+'</title><circle class="whole-hit" r="3.7"/><circle r="'+(principal.includes(p.id)?3.8:1.75)+'" fill="'+pt.color+'"/><text x="2" y="-1">'+esc(p.name)+'</text></g>'}).join('');
whole.innerHTML='<g class="whole-lines">'+edgesHtml.join('')+'</g><g>'+nodeHTML+'</g><g class="whole-labels">'+principal.filter(id=>positions.has(id)).map(id=>headline(positions.get(id))).join('')+'</g><g id="kin-whole-active" pointer-events="none"></g>';
const activeLayer=get('whole-active');
function paintRoute(p,anc){
const marks=[];for(const id of anc){const n=by.get(id),pt=positions.get(id);if(!pt)continue;for(const v of n.parents)if(anc.has(v)&&positions.has(v))marks.push('<path d="'+curved(positions.get(v),pt)+'"/>');marks.push('<circle cx="'+fmt(pt.x)+'" cy="'+fmt(pt.y)+'" r="2.2"/>')}
const pt=positions.get(p.id);
if(pt)marks.push('<circle class="whole-selected" cx="'+fmt(pt.x)+'" cy="'+fmt(pt.y)+'" r="6"/>');
activeLayer.innerHTML=marks.join('');
let line=[p],n=p;const visited=new Set([p.id]);while(n.parents.length){const a=by.get(n.parents[0]);if(!a||visited.has(a.id))break;visited.add(a.id);line.unshift(a);n=a}
routeBox.innerHTML='<span>Линия предков</span>'+line.map(n=>'<button data-who="'+n.id+'">'+esc(n.name)+'</button>').join('<i>›</i>');
}
function applyView(){const w=mapW/view.z,h=mapH/view.z;
view.x=Math.max(0,Math.min(mapW-w,view.x));view.y=Math.max(0,Math.min(mapH-h,view.y));
whole.setAttribute('viewBox',[view.x,view.y,w,h].join(' '));whole.classList.toggle('magnified',view.z>=5);get('zoom-out').disabled=view.z<=1;get('zoom-in').disabled=view.z>=32;
get('zoom-reset').textContent=Math.round(view.z*100)+' %';
}
function zoom(factor,fx=.5,fy=.5){const before=view.z;view.z=Math.max(1,Math.min(32,view.z*factor));
view.x+=(mapW/before-mapW/view.z)*fx;view.y+=(mapH/before-mapH/view.z)*fy;applyView()}
function openOverview(scroll=true){detailView=false;root.dataset.view='whole';activeLayer.innerHTML='';view.z=1;applyView();if(scroll)frame.scrollIntoView({behavior:'smooth',block:'start'})}
get('whole-return').onclick=()=>openOverview();
get('zoom-in').onclick=()=>zoom(2);get('zoom-out').onclick=()=>zoom(.5);get('zoom-reset').onclick=()=>{view.z=1;applyView()};
let drag=null,suppress=false;
whole.onpointerdown=e=>{if(e.button===0&&view.z>1){drag={x:e.clientX,y:e.clientY,vx:view.x,vy:view.y};suppress=false}};
whole.onpointermove=e=>{if(!drag)return;const dx=e.clientX-drag.x,dy=e.clientY-drag.y;if(Math.abs(dx)+Math.abs(dy)>5){suppress=true;whole.setPointerCapture(e.pointerId);const scale=whole.getScreenCTM().a;view.x=drag.vx-dx/scale;view.y=drag.vy-dy/scale;applyView()}};
whole.onpointerup=whole.onpointercancel=()=>{drag=null};
whole.addEventListener('click',e=>{if(suppress){suppress=false;e.stopPropagation()}},{capture:true,signal});
whole.onkeydown=e=>{if(['Enter',' '].includes(e.key)&&e.target.dataset.who){e.preventDefault();select(e.target.dataset.who)}};
whole.onwheel=e=>{if(!e.ctrlKey||detailView)return;e.preventDefault();const r=whole.getBoundingClientRect();zoom(e.deltaY<0?1.4:1/1.4,(e.clientX-r.left)/r.width,(e.clientY-r.top)/r.height)};
get('whole-count').textContent=people.length+' записей · '+generations+' поколений';
applyView();
