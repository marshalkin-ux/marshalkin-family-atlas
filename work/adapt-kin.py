from pathlib import Path
p=Path('work/tree-section.html')
s=p.read_text('utf-8-sig').replace('<label>Поиск по дереву','<label>Источник<select id="kin-source"><option value="full">Полное родословное древо</option><option value="contacts">Схема контактов</option></select></label><label>Поиск по дереву')
s=s.replace('<div class="kin-legend"><span>', '<div id="kin-band" hidden></div><div class="kin-legend"><span>').replace('Предки и потомки выбранного человека','Линия выбранного человека')
s=s.replace('#tree .kin-focus{display:grid;', '''#kin-band{background:#234b40;border:1px solid #617666;padding:12px;margin:10px 0;color:#fff9ec}
#kin-band p{margin:0 0 7px;font:15px/1.45 system-ui,sans-serif}
#kin-band .kin-band-names{display:flex;gap:5px;flex-wrap:wrap}
#kin-band button{background:#f6f3e9;color:#254b3e;font:14px/1.4 system-ui,sans-serif;border:0;border-radius:3px;padding:5px 8px;cursor:pointer}
#kin-band button[aria-current=true]{background:#ffc493}
#kin-band .kin-pages{display:flex;gap:9px;align-items:center;font:13px system-ui;margin-top:8px}
#tree .kin-group text{font:600 12px system-ui,sans-serif;pointer-events:none;fill:#173c31}
#tree .kin-group rect{fill:#d0d9bd;stroke:#3f5e4d;stroke-width:1}
#tree .kin-group.active rect{fill:#f2ae77}
#tree .kin-group{cursor:pointer;outline:0}#tree .kin-group:focus rect,#tree .kin-group:hover rect{stroke:white;stroke-width:3}
#tree .kin-focus{display:grid;''')
s=s.replace("const people=window.people, root=document.querySelector('#tree');","const root=document.querySelector('#tree');\nconst full=window.fullPeople||[],contacts=window.people||[],allBack=[];\nif(!root||root.dataset.initialized)return;root.dataset.initialized='1';\nconst source=document.getElementById('kin-source');if(!full.length)source.options[0].disabled=true;\nlet active,selected=null,fromId=null,dispose=()=>{};\nfunction mount(mode,initial){\nconst people=mode==='full'?full:contacts;active=mode;source.value=mode;dispose();const ctrl=new AbortController(),signal=ctrl.signal;dispose=()=>ctrl.abort();\nconst grouped=mode==='full';")
s=s.replace("if(!Array.isArray(people)||!people.length||root.dataset.initialized)return;\nroot.dataset.initialized='1';","if(!people.length)return;")
s=s.replace('let selected=null,history=[];','')
a=s.index('const width=');b=s.index('const grid=',a)
s=s[:a]+'''const bandSize=80, maximumRow=Math.max(...rows), width=980;
const bandIndex=p=>Math.floor((p.row-1)/bandSize),key=p=>p.gen+'-'+bandIndex(p);
const clusters=new Map();
if(grouped)for(const p of people){const k=key(p);if(!clusters.has(k))clusters.set(k,[]);clusters.get(k).push(p)}
const bandCount=Math.ceil(maximumRow/bandSize);
const height=grouped?bandCount*40+37:(maximumRow-minRow)*11+57;
const coords=p=>[grouped?102+(p.gen-1)*(width-130)/Math.max(1,generations-1):25+(p.gen-1)*(width-50)/Math.max(1,generations-1),grouped?39+bandIndex(p)*40:32+(p.row-minRow)*11+(p.id.endsWith('b')?5.5:0)];
const svg=get('atlas');svg.setAttribute('viewBox','0 0 '+width+' '+height);
const label=p=>p.name+(p.year?' · '+p.year:'')+' · '+p.cell;
''' + s[b:]
a=s.index('svg.innerHTML=');b=s.index('const options=',a)
s=s[:a]+'''const groupEdges=new Map();
if(grouped)for(const p of people)for(const parentId of p.parents){
const parent=by.get(parentId);if(!parent)continue;
const k=key(parent)+'/'+key(p);if(!groupEdges.has(k))groupEdges.set(k,{p,parent});
}
function clusterPath(pair){const p=pair.p,a=pair.parent,[x,y]=coords(a),[u,v]=coords(p),mid=(x+u)/2;return '<path class="kin-edge" data-from="'+key(a)+'" data-to="'+key(p)+'" d="M'+x+' '+y+' C'+mid+' '+y+' '+mid+' '+v+' '+u+' '+v+'"/>'}
function clusterNode([k,list]){const p=list[0],[x,y]=coords(p);return '<g class="kin-group" tabindex="0" role="button" aria-label="Поколение '+p.gen+', строки '+(bandIndex(p)*bandSize+1)+'–'+Math.min(maximumRow,(bandIndex(p)+1)*bandSize)+', человек: '+list.length+'" data-group="'+k+'" transform="translate('+x+' '+y+')"><rect x="-17" y="-10" width="34" height="20" rx="6"/><text text-anchor="middle" y="4">'+list.length+'</text></g>'}
const bandLabels=grouped?Array.from({length:bandCount},(_,i)=>'<text x="0" y="'+(43+i*40)+'" fill="#d0dbc9" font-size="14">'+(i*bandSize+1)+'–'+Math.min(maximumRow,(i+1)*bandSize)+'</text>').join(''):'';
svg.innerHTML=grid+(grouped?bandLabels+[...groupEdges.values()].map(clusterPath).join('')+[...clusters].map(clusterNode).join(''):edges+nodes)+'<circle id="kin-ring" r="'+(grouped?20:7)+'"/>';
get('total').textContent=people.length+' человек · '+generations+' поколений';
svg.previousElementSibling.querySelector('h3').textContent=grouped?'Поколения и строки древа':'Все ветви рода';
get('band').hidden=!grouped;
let currentGroup='',pageIndex=0;
function displayGroup(k,page){const list=clusters.get(k);if(!list)return;
currentGroup=k;pageIndex=Math.max(0,Math.min(Math.ceil(list.length/10)-1,page));
const p=list[0],i=bandIndex(p);
get('band').innerHTML='<p><b>Поколение '+p.gen+'</b> · строки '+(i*bandSize+1)+'–'+Math.min(maximumRow,(i+1)*bandSize)+' · записей: '+list.length+'</p><div class="kin-band-names">'+list.slice(10*pageIndex,10*pageIndex+10).map(n=>'<button type="button" data-who="'+n.id+'" aria-current="'+(selected===n.id)+'">'+esc(label(n))+'</button>').join('')+'</div>'+(list.length>10?'<div class="kin-pages">'+(pageIndex?'<button data-step="-1">← Ранее</button>':'')+'<span>'+String(pageIndex+1)+' / '+Math.ceil(list.length/10)+'</span>'+(10*(pageIndex+1)<list.length?'<button data-step="1">Далее →</button>':'')+'</div>':'');
}
''' +s[b:]
s=s.replace('if(remember&&selected&&id!==selected)history.push(selected);','if(remember&&selected&&id!==selected)allBack.push(selected);')
s=s.replace('!history.length','!allBack.length')
s=s.replace("const [x,y]=coords(p);get('ring')","""if(grouped){
const pathGroups=new Set([...up,...down].map(id=>key(by.get(id))));
const pathEdges=new Set();
for(const id of new Set([...up,...down])){const n=by.get(id);for(const a of n.parents)if((up.has(a)&&up.has(id))||(down.has(a)&&down.has(id)))pathEdges.add(key(by.get(a))+'/'+key(n))}
svg.querySelectorAll('.kin-group').forEach(n=>n.classList.toggle('active',pathGroups.has(n.dataset.group)));
svg.querySelectorAll('[data-from]').forEach(e=>e.classList.toggle('active',pathEdges.has(e.dataset.from+'/'+e.dataset.to)));
displayGroup(key(p),Math.floor(clusters.get(key(p)).indexOf(p)/10));
}
const [x,y]=coords(p);get('ring')""")
s=s.replace("const spouse=id==='K30'?by.get('K30b'):id==='K30b'?by.get('K30'):null;", "const spouseIds=p.spouseIds||(id==='K30'?['K30b']:id==='K30b'?['K30']:[]);\nconst spouses=spouseIds.map(v=>by.get(v)).filter(Boolean);")
s=s.replace("(spouse?'<p>Супруг'+(spouse.sex==='ж'?'а':'')+'</p>'+relative(spouse,false):'')", "spouses.map(n=>'<p>'+ (n.sex==='ж'?'Супруга':'Супруг')+'</p>'+relative(n,false)).join('')")
s=s.replace("Схема контактов · ячейка '+esc(p.cell)","'+(grouped?'Полное древо':'Схема контактов')+' · ячейка '+esc(p.cell)")
s=s.replace("window.focusPerson=id=>select(id);", """window.focusPerson=(id,remember=true)=>{if(by.has(id))return select(id,remember);const target=id?.startsWith('full-')?'full':'contacts';
if(!(target==='full'?full:contacts).some(p=>p.id===id))return false;
if(remember&&selected!==id)allBack.push(selected);mount(target,id);return true};
source.onchange=()=>{if(selected)allBack.push(selected);mount(source.value)};
get('q').value='';""")
s=s.replace("'input',populate);","'input',populate,{signal});").replace("select(get('pick').value)});","select(get('pick').value)},{signal});")
s=s.replace("if(history.length)select(history.pop(),false)","if(allBack.length)window.focusPerson(allBack.pop(),false)")
s=s.replace("root.addEventListener('click',e=>{const n=", """root.addEventListener('click',e=>{const step=e.target.closest('[data-step]'),g=e.target.closest('[data-group]');
if(step){displayGroup(currentGroup,pageIndex+Number(step.dataset.step));return}
if(g){select(clusters.get(g.dataset.group)[0].id);return}
const n=""")
s=s.replace("focus({preventScroll:true})});","focus({preventScroll:true})},{signal});")
s=s.replace("svg.addEventListener('keydown',e=>{const n=", """svg.addEventListener('keydown',e=>{const g=e.target.closest('[data-group]');if(g&&['Enter',' '].includes(e.key)){e.preventDefault();select(clusters.get(g.dataset.group)[0].id);return}
const n=""")
s=s.replace("focus({preventScroll:true})}});","focus({preventScroll:true})}},{signal});")
s=s.replace("populate();select(by.has('F14')?'F14':people[0].id,false);", """populate();select(initial||(grouped?(by.has('full-D10')?'full-D10':people[0].id):(by.has('F14')?'F14':people[0].id)),false);
}
mount(full.length?'full':'contacts');""")
s=s.replace("const edges=people.flatMap","const edges=grouped?'':people.flatMap").replace("const nodes=people.map","const nodes=grouped?'':people.map")
s=s.replace("n=>family(n,direction,out)","n=>n&&family(n,direction,out)")
s=s.replace("<span><i class=\"dash\"></i>Предполагаемая связь</span>", "<span id=\"kin-dash\"><i class=\"dash\"></i>Предполагаемая связь</span>")
s=s.replace("get('band').hidden=!grouped;","get('band').hidden=!grouped;get('dash').hidden=grouped;\nroot.querySelector('.kin-head p').textContent=grouped?'Вверху указаны поколения, слева — строки исходной таблицы. Число в группе показывает, сколько в ней записей. Выберите группу или найдите человека по имени.':'Выберите точку на схеме или найдите имя. В карточке можно перейти к родителям и детям.';")
p.write_text(s,'utf-8')
