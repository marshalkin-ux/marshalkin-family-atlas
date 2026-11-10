const stage=get('stage'), branchMap=get('branch-map'), toggle=get('direction'), pageBar=get('branch-pages');
let direction='down',branchPage=0, branchPerson=null;
const relations=(p,dir)=>dir==='down'?children.get(p.id):p.parents.map(id=>by.get(id)).filter(Boolean);
function twig(x,y,flip){
return '<g class="kin-twig" transform="translate('+x+' '+y+') scale('+flip+' 1)"><path d="M0 0q10 -5 20 -24M7 -6q-2 -8 2 -14q5 7 -2 14M14 -15q9 0 15 -6q-9 -2 -15 6"/></g>';
}
function plot(id,reset){
const p=by.get(id);if(!p)return;
if(reset){
branchPage=0;branchPerson=id;
if(!relations(p,direction).length&&relations(p,direction==='up'?'down':'up').length)direction=direction==='up'?'down':'up';
}
const all=relations(p,direction),nodes=all.slice(branchPage*3,branchPage*3+3);
const mobile=stage.clientWidth<715, w=mobile?Math.max(270,stage.clientWidth-28):1000;
const up=direction==='up', first=up?'Родители':'Дети', second=up?'Бабушки и дедушки':'Внуки';
const layer=nodes.map(n=>{const family=relations(n,direction);return {n,subset:family.slice(0,2),total:family.length}});
get('branch-name').textContent=p.name;
get('branch-subtitle').textContent=up?'Родители и их родители':'Дети и их дети';
toggle.value=direction;
Array.from(toggle.options).forEach(o=>o.disabled=!relations(p,o.value).length&&o.value!==direction);
const parentId=p.parents[0],upButton=get('branch-parent');
upButton.disabled=!parentId;upButton.onclick=()=>{if(parentId)select(parentId)};
const mateList=p.spouseIds||(id==='K30'?['K30b']:id==='K30b'?['K30']:[]);
get('branch-mates').innerHTML=mateList.length?'<span>Супружеские связи</span> '+mateList.filter(v=>by.has(v)).map(v=>'<button type="button" data-who="'+v+'">'+esc(by.get(v).name)+'</button>').join(' '):'';
const allPages=Math.ceil(all.length/3);
pageBar.innerHTML=allPages>1?(branchPage?'<button type="button" data-bpage="-1">←</button>':'')+'<span>'+first+' · '+(branchPage*3+1)+'–'+Math.min(all.length,(branchPage+1)*3)+' из '+all.length+'</span>'+(branchPage+1<allPages?'<button type="button" data-bpage="1">→</button>':''):'';
const links=[],leaves=[],labels=[];
const link=(x1,y1,x2,y2,uncertain,level)=>{
const midY=y1+(y2-y1)*.51;
const d=mobile?'M'+x1+' '+y1+' C'+x1+' '+(y1+23)+' '+(x2-25)+' '+y2+' '+x2+' '+y2:'M'+x1+' '+y1+' C'+x1+' '+midY+' '+x2+' '+midY+' '+x2+' '+y2;
links.push('<path d="'+d+'" class="kin-limb l'+level+'"'+(uncertain?' stroke-dasharray="5 4"':'')+'/>');
if(!mobile&&Math.abs(x2-x1)>65)leaves.push(twig((x2+x1)/2,midY,x2>x1?1:-1));
};
function point(n,x,y,level,extra='',allowed=165){
const size=mobile?(level===0?23:level===1?18:16):(level===0?31:level===1?25:19);
const available=mobile?w-x-13:allowed;
const max=Math.max(9,Math.floor(available/(size*.54)));
const name=n.name.length>max?n.name.slice(0,max-1)+'…':n.name;
const note=[n.year||'',extra].filter(Boolean).join(' · ');
const ox=mobile?12:0,oy=mobile?-1:-13,align=mobile?'start':'middle';
labels.push('<g class="kin-branch-node l'+level+'" transform="translate('+x+' '+y+')" data-who="'+n.id+'" tabindex="0" role="button" aria-label="'+esc(label(n))+'"><title>'+esc(label(n))+'</title><rect x="'+(mobile?-6:-allowed/2)+'" y="'+(mobile?-20:-46)+'" width="'+(mobile?available+14:allowed)+'" height="49" rx="15" fill="transparent"/><circle r="'+(level===0?6:4.5)+'"/><text x="'+ox+'" y="'+oy+'" text-anchor="'+align+'" font-size="'+size+'">'+esc(name)+'</text>'+(note?'<text class="kin-node-meta" x="'+ox+'" y="'+(oy+(mobile?15:31))+'" text-anchor="'+align+'" font-size="'+(mobile?11:13)+'">'+esc(note)+'</text>':'')+'</g>');
}
let height;
if(mobile){
point(p,13,34,0);let y=48;
for(const {n,subset,total} of layer){
y+=48;const childY=y;link(13,38,39,childY,up?p.uncertain:n.uncertain,1);
point(n,39,childY,1,total>subset.length?(up?'родит. ':'детей ')+total:'');
for(const v of subset){y+=41;link(39,childY+4,69,y,up?n.uncertain:v.uncertain,2);point(v,69,y,2)}
}
height=y+26;
}else{
height=nodes.length?323:135;const rootY=height-43,childY=169,grandY=55;
point(p,w/2,rootY,0,'',350);
layer.forEach(({n,subset,total},i)=>{
const groupW=(w-38)/layer.length,x=19+groupW*(i+.5);
link(w/2,rootY-7,x,childY+4,up?p.uncertain:n.uncertain,1);
point(n,x,childY,1,total>subset.length?(up?'родит. ':'детей ')+total:'',Math.min(groupW-10,300));
subset.forEach((v,j)=>{const gx=x+(j-(subset.length-1)/2)*Math.min(167,groupW/2);
link(x,childY-7,gx,grandY+3,up?n.uncertain:v.uncertain,2);point(v,gx,grandY,2,'',Math.min(groupW/subset.length-5,235))});
});
}
branchMap.setAttribute('viewBox','0 0 '+w+' '+height);
branchMap.innerHTML='<g class="kin-sketch">'+links.join('')+leaves.join('')+labels.join('')+'</g>';
const info=(!nodes.length?'В этой записи родители и дети не указаны.':layer.some(g=>g.total>2)?'У каждой ветви показаны до двух '+(up?'предков':'внуков')+'. Выберите имя, чтобы развернуть ветвь.':'Выберите имя, чтобы перейти к его семье.');
get('branch-help').textContent=info;
}
toggle.onchange=()=>{direction=toggle.value;branchPage=0;plot(selected,false)};
pageBar.onclick=e=>{const b=e.target.closest('[data-bpage]');if(b){branchPage+=Number(b.dataset.bpage);plot(selected,false)}};
branchMap.onkeydown=e=>{const n=e.target.closest('[data-who]');if(n&&['Enter',' '].includes(e.key)){e.preventDefault();select(n.dataset.who);branchMap.querySelector('[data-who="'+n.dataset.who+'"]')?.focus({preventScroll:true})}};
let lastSize=stage.clientWidth;
const ro=new ResizeObserver(()=>{if(stage.clientWidth!==lastSize){lastSize=stage.clientWidth;if(branchPerson)plot(branchPerson,false)}});ro.observe(stage);signal.addEventListener('abort',()=>ro.disconnect());
