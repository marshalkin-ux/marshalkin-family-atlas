from pathlib import Path
p=Path('work/tree-section.html');s=p.read_text('utf8').replace('<div id="kin-band" hidden>', '<div id="kin-mobile-groups"></div><div id="kin-band" hidden>')
s=s.replace('#kin-band{background:', '''#kin-mobile-groups{display:none}
@media(max-width:660px){#tree[data-grouped="true"] #kin-atlas{display:none}#tree[data-grouped="true"] #kin-mobile-groups{display:grid;gap:9px;margin:12px 0;font:14px/1.4 system-ui,sans-serif}
#kin-mobile-groups label{color:#fff9ec;display:flex;align-items:center;gap:9px}
#kin-mobile-groups select{font:inherit;color:#173b32;background:#f6f2e6}
#kin-mobile-groups .kin-mobile-bands{display:grid;grid-template-columns:repeat(auto-fit,minmax(115px,1fr));gap:5px}
#kin-mobile-groups button{background:transparent;color:#f8f5e8;border:1px solid #798f7d;text-align:left;padding:7px;font:14px/1.35 system-ui;border-radius:3px}
#kin-mobile-groups button[aria-pressed=true]{background:#f4bf94;color:#183d34}}
#kin-band{background:''')
s=s.replace("let currentGroup='',pageIndex=0;", """let currentGroup='',pageIndex=0;
root.dataset.grouped=String(grouped);
function mobileBands(gen,selectedGroup){
const mobile=get('mobile-groups');
if(!mobile.firstChild){
mobile.innerHTML='<label>Поколение <select aria-label="Поколение на обзорной схеме">'+Array.from({length:generations},(_,i)=>'<option value="'+(i+1)+'">'+(i+1)+'</option>').join('')+'</select></label><div class="kin-mobile-bands"></div>';
mobile.querySelector('select').onchange=e=>{mobileBands(Number(e.target.value),currentGroup)};
}
mobile.querySelector('select').value=gen;
mobile.querySelector('.kin-mobile-bands').innerHTML=[...clusters].filter(([,list])=>list[0].gen===gen).map(([k,list])=>{const i=bandIndex(list[0]);return '<button type="button" data-group="'+k+'" aria-pressed="'+(k===selectedGroup)+'">Стр. '+(i*bandSize+1)+'–'+Math.min(maximumRow,(i+1)*bandSize)+' · '+list.length+'</button>'}).join('');
}
get('mobile-groups').innerHTML='';
""")
s=s.replace('const p=list[0],i=bandIndex(p);','const p=list[0],i=bandIndex(p);mobileBands(p.gen,k);')
s=s.replace("const grid=Array.from", "const grid=Array.from")
s=s.replace("const record=(p.note?", """const record=(grouped?'<p>Запись в таблице: «'+esc(p.raw)+'».</p>':'')+(p.faint?'<p>В источнике запись выделена бледным цветом.</p>':'')+(p.note?""")
s=s.replace("'':'';","'':'';")
s=s.replace("spouses.map(n=>'<p>'+ (n.sex==='ж'?'Супруга':'Супруг')", "spouses.map(n=>'<p>'+ (n.sex==='ж'?'Супруга':n.sex==='м'?'Супруг':'Супружеская связь')")
s=s.replace("const next=direction==='up'?p.parents.map(id=>by.get(id)):children.get(p.id);","const next=direction==='up'?p.parents.map(id=>by.get(id)):children.get(p.id);")
s=s.replace('const parents=p.parents.map(v=>relative(by.get(v),p.uncertain))','const parents=p.parents.filter(v=>by.has(v)).map(v=>relative(by.get(v),p.uncertain))')
s=s.replace("p.year+' г. р.'","p.year+' г. р.'")
p.write_text(s,'utf8')
