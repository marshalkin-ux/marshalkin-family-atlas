from pathlib import Path
import base64,re
w=Path('work'); p=w/'story.html';s=p.read_text('utf-8-sig')
a=s.index('<header class="mast"');b=s.index('<nav class="folioNav"',a)
s=s[:a]+'''<header class="atlasMast"><div class="folioWidth"><div class="atlasName"><svg class="atlasSprig" viewBox="0 0 62 62" aria-hidden="true"><g fill="none" stroke="#c8b787" stroke-width="1.1"><path d="M11 55Q29 41 45 9M19 46Q18 33 12 23M27 37Q41 36 52 28M34 28Q29 21 28 10"/><g fill="#899e77"><path d="M18 40Q6 39 7 30Q16 30 18 40ZM14 30Q4 24 7 17Q14 20 14 30ZM25 40Q27 29 34 29Q35 36 25 40ZM39 34Q43 23 51 22Q50 30 39 34ZM31 23Q19 20 21 12Q29 14 31 23ZM36 25Q37 15 44 15Q45 21 36 25ZM42 14Q39 5 48 2Q49 10 42 14Z"/></g></g></svg><div><span>Семейный атлас</span><h1>Маршалкины</h1></div></div><p>Ставропольский край</p></div></header>
'''+s[b:]
s=s.replace('<a href="#history">История</a><a href="#tree">Древо</a>','<a href="#tree">Древо</a><a href="#history">История</a>')
s=s.replace('<section id="history" class="chapter">{{HISTORY}}</section>\n<div class="chapter">{{TREE}}</div>','<div class="chapter atlasTree">{{TREE}}</div>\n<section id="history" class="chapter">{{HISTORY}}</section>')
s=s.replace("const art=document.querySelector('.heroArt');","const art=document.querySelector('.atlasSprig');")
s=s.replace("if(!reduce.matches&&scrollY<800){art.style.transform='translateY('+Math.min(42,scrollY*.15)+'px)'}","if(!reduce.matches&&scrollY<150){art.style.transform='rotate('+Math.min(5,scrollY*.06)+'deg)'}")
s=s[:s.index('/* Botanical plate.')]+s[s.index('</script></body></html>'):]
s=s.replace('<div id="groups"></div></section>','<div id="groups"></div><div class="indexPages" id="indexPages"><button type="button" id="groupPrev">← Назад</button><span id="groupPage" aria-live="polite"></span><button type="button" id="groupNext">Далее →</button></div></section>')
s=s.replace('function timeline(){','''let groupPage=0;
const pageSize=3;
function paginate(){
 const items=Array.from($('groups').children);
 const pages=Math.ceil(items.length/pageSize);
 groupPage=Math.min(Math.max(0,groupPage),Math.max(0,pages-1));
 items.forEach((item,i)=>item.hidden=Math.floor(i/pageSize)!==groupPage);
 $('indexPages').hidden=pages<=1;
 $('groupPage').textContent='Страница '+(groupPage+1)+' из '+pages;
 $('groupPrev').disabled=groupPage===0;
 $('groupNext').disabled=groupPage>=pages-1;
}
$('groupPrev').onclick=()=>{groupPage--;paginate()};
$('groupNext').onclick=()=>{groupPage++;paginate()};
function timeline(){''')
s=s.replace("$('groups').replaceChildren(fragment);","$('groups').replaceChildren(fragment);groupPage=0;paginate();")
s=s.replace('Раскройте семейную группу или введите имя. Подписи событий сохранены в порядке исходной ленты.','Найдите имя или выберите семейную группу. Поиск охватывает все страницы указателя.')
fontcss=''
for path in sorted(w.glob('*normal.woff2')):
 n=path.name;family='Atlas Display' if 'cormorant' in n else 'Atlas Sans'
 weight=('100 900' if family=='Atlas Display' else ('100 550' if '400-normal' in n else '551 900'))
 # css range dispatches shared punctuation to the Latin subset
 ranges='U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116' if '-cyrillic-' in n else 'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2190-2199,U+2212,U+2215,U+FEFF,U+FFFD'
 fontcss+="@font-face{font-family:'%s';font-weight:%s;font-display:swap;src:url(data:font/woff2;base64,%s) format('woff2');unicode-range:%s}\n"%(family,weight,base64.b64encode(path.read_bytes()).decode(),ranges)
style='''
:root{--serif:'Atlas Display',Georgia,serif;--sans:'Atlas Sans','Segoe UI',sans-serif}
.atlasMast{background:#253e30;color:#fff7e4}.atlasMast>.folioWidth{display:flex;align-items:center;justify-content:space-between;gap:15px;padding-block:10px}.atlasName{display:flex;align-items:center;gap:13px}.atlasName span,.atlasMast p{font:700 10px/1.2 var(--sans);letter-spacing:.16em;text-transform:uppercase;color:#e1d4b5}.atlasMast p{margin:0}.atlasName h1{font:600 clamp(37px,4.2vw,57px)/.94 var(--serif);letter-spacing:-.044em;margin:1px 0 3px}.atlasSprig{width:52px;height:52px;transform-origin:center bottom}.atlasTree{padding-top:clamp(12px,1.7vw,23px)}#tree .kin-head h2{font:600 clamp(21px,2.5vw,36px)/1.06 var(--serif)!important;margin-bottom:4px}.indexPages{display:flex;gap:14px;align-items:center;justify-content:flex-end;margin:12px 0 0}.indexPages[hidden],#groups [hidden]{display:none}.indexPages span{font-size:12px}.indexPages button{border:1px solid #aca890;border-radius:3px;background:#fffaf0;padding:4px 10px;font-size:13px}.indexPages button:disabled{opacity:.45}.indexPages button:not(:disabled):hover{background:#e9e9d9}.folioDisclosure summary{padding-block:9px}.archiveTools{margin:10px 0}
body :is(.hx,.cx,#tree,#stats,.auditBox,.readingIntro) :is(button,select,input,label,span,small,p,text,li),body :is(.hx-tag,.cx-tag,.cx-k,.kin-controls,.kin-legend){font-family:var(--sans)!important}
body :is(h1,h2,h3,h4),body .hx .hx-route b,body .hx .hx-entry strong,body :is(.cx-year,.cx-ribbon,.auditBox summary,.readingIntro,.genSummary strong),#tree .kin-canopy-label,#tree .kin-card h3{font-family:var(--serif)!important;font-weight:600}
#tree svg text{font-family:var(--sans)!important}
@media(max-width:540px){.atlasSprig{width:33px;height:38px}.atlasName{gap:7px}.atlasMast p{font-size:8px;letter-spacing:.07em;max-width:86px;text-align:right}.atlasMast>.folioWidth{padding-block:7px}.atlasName span{font-size:8px}.folioNav .folioWidth{gap:16px}.folioNav a{padding-block:9px 7px}.atlasTree{padding-top:12px}.indexPages{justify-content:space-between}}
'''
s=s.replace('</style>',fontcss+style+'</style>',1)
licenses='\n'.join((w/f).read_text('utf8') for f in ['cglicense.txt','manlicense.txt'])
s=s.replace('</head>','<script type="text/plain" id="embedded-font-licenses">'+licenses+'</script></head>')
p.write_text(s,'utf8')
