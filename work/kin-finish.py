from pathlib import Path
p=Path('work/tree-section.html');s=p.read_text('utf8')
s=s.replace('<button id="kin-open"', '<button id="kin-faint" type="button" aria-pressed="false">Светло-серые записи</button><button id="kin-open"')
s=s.replace('button:first-of-type{background:', 'button#kin-open{background:')
s=s.replace('#tree .kin-controls button:disabled', '#tree #kin-faint[aria-pressed=true]{background:#d9ddcd;border-color:#526a55}#tree [hidden]{display:none!important}\n#tree .kin-controls button:disabled')
s=s.replace("let active,selected=null,fromId=null,dispose=()=>{};", """let selected=null,dispose=()=>{};
const stories=new Map();let storyN=0;
document.querySelectorAll('[onclick*="focusPerson"]').forEach(el=>{
if(root.contains(el))return;
const record=el.closest('.cx-row,.hx-entry,article,details')||el.parentElement;
if(!record)return;const id=el.getAttribute('onclick').match(/focusPerson\(['"]([^'"]+)['"]\)/)?.[1];if(!id)return;
if(!record.id)record.id='kin-story-'+(++storyN);
const title=record.querySelector('h3,h4,summary,strong')?.textContent.trim()||'Упоминание в атласе';
if(!stories.has(id))stories.set(id,new Map());stories.get(id).set(record.id,title);
});""")
s=s.replace("active=mode;source.value=mode;", "source.value=mode;")
s=s.replace("const grouped=mode==='full';", "const grouped=mode==='full';let faintOnly=false;")
s=s.replace("get('total').textContent=people.length+' человек · '+generations+' поколений';","get('total').textContent=(grouped?'Записей: ':'Людей: ')+people.length+' · поколений: '+generations;")
s=s.replace('const matches=options.filter(p=>{const source=', 'const matches=options.filter(p=>{if(faintOnly&&!p.faint)return false;const source=')
s=s.replace("function populate(){", """const faintCount=people.filter(p=>p.faint).length;
get('faint').hidden=!faintCount;
get('faint').textContent='Светло-серые записи · '+faintCount;
function setFaint(value){faintOnly=value;get('faint').setAttribute('aria-pressed',String(value))}
setFaint(false);
get('faint').onclick=()=>{setFaint(!faintOnly);get('q').value='';populate();if(!get('open').disabled)select(get('pick').value)};
function populate(){""")
s=s.replace("get('q').value='';populate()}","get('q').value='';if(!p.faint)setFaint(false);populate()}")
s=s.replace("const record=(grouped?", """const storyLinks=[...(stories.get(id)||[])].map(([anchor,title])=>'<p><a href="#'+esc(anchor)+'">'+esc(title)+' →</a></p>').join('');
const record=(grouped?""")
s=s.replace("(p.faint?'<p>В источнике запись выделена бледным цветом.</p>':'')", "(p.faint&&!p.note?.includes('шрифт')?'<p>В источнике запись выделена бледным цветом.</p>':'')")
s=s.replace("(bio?'<a href=\"#'+esc(bio)+'\">К биографии →</a>':'')", """(p.repeatOf&&by.has(p.repeatOf)?'<p>Параллельная запись</p>'+relative(by.get(p.repeatOf),false):'')+(bio?'<a href="#'+esc(bio)+'">К биографии →</a>':'')+storyLinks""")
s=s.replace("window.focusPerson=(id,remember=true)=>{if(by.has(id))return select(id,remember);", """window.focusPerson=(id,remember=true,scroll=true)=>{const reveal=()=>{if(scroll)get('focus').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth',block:'center'})};
if(by.has(id)){const ok=select(id,remember);reveal();return ok}""")
s=s.replace("mount(target,id);return true", "mount(target,id);reveal();return true").replace("window.focusPerson(allBack.pop(),false)","window.focusPerson(allBack.pop(),false,false)")
s=s.replace("data-from=\"'+key(a)+'\"", "data-from=\"'+key(a)+'\"")
p.write_text(s,'utf8')
