from pathlib import Path
p=Path('work/tree-section.html');s=p.read_text('utf8')
s=s.replace("up?'Родители и их родители':'Дети и их дети'","up?'Родители, бабушки и дедушки':'Дети и внуки'")
s=s.replace("const name=n.name.length>max?n.name.slice(0,max-1)+'…':n.name;", """const words=n.name.trim().split(/\s+/);
const twoLines=!mobile&&level===2&&words.length>1&&n.name.length*size*.58>available*.74;
const cut=(v,limit)=>v.length>limit?v.slice(0,limit-1)+'…':v;
const name=twoLines?cut(words[0],max):cut(n.name,max);
const subName=twoLines?cut(words.slice(1).join(' '),max):'';""")
s=s.replace("+(note?'<text class=", "+(subName?'<text x=\"'+ox+'\" y=\"'+(oy-20)+'\" text-anchor=\"'+align+'\" font-size=\"'+(size-2)+'\">'+esc(name)+'</text>':'')+(note?'<text class=")
s=s.replace(">'+esc(name)+'</text>'+(subName?", ">'+esc(subName||name)+'</text>'+(subName?")
s=s.replace("const meta=p.raw?.match(/\\(([^)]*)\\)/)?.[1];","const meta=grouped?'':p.raw?.match(/\\(([^)]*)\\)/)?.[1];")
p.write_text(s,'utf8')
