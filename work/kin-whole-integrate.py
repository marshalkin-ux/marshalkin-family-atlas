from pathlib import Path
p=Path('work/tree-section.html');s=p.read_text('utf8')
s=s.replace('</style>', '''
#tree #kin-whole{border-radius:6px;padding:clamp(12px,2vw,24px);background:radial-gradient(ellipse at 47% 48%,#244b3b,#15382e 78%);color:#f9f0dc;scroll-margin-top:5rem;min-width:0}
#tree .whole-toolbar,#tree .whole-tools,#tree .whole-foot{display:flex;align-items:center;justify-content:space-between;gap:7px;flex-wrap:wrap}
#tree .whole-toolbar h3{font:normal clamp(25px,3vw,38px)/1.1 Georgia,serif;margin:0;color:#fff4da}
#tree #kin-whole-count,#tree .whole-foot,#tree #kin-whole-route{font:13px/1.5 system-ui,sans-serif;color:#cedcca}
#tree #kin-whole button{background:#254b3b;color:#fff3d9;border:1px solid #728777;border-radius:4px;padding:5px 9px;cursor:pointer;font:14px/1.3 system-ui,sans-serif}
#tree #kin-whole button:disabled{opacity:.4}
#tree #kin-whole-svg{display:block;width:100%;height:clamp(235px,56svh,640px);touch-action:pan-y;user-select:none;border:0;background:transparent}
#tree #kin-whole-svg.magnified{touch-action:none}
#tree .whole-path{stroke-width:1;fill:none;opacity:.61}
#tree .whole-mate{stroke:#e3d8c1;stroke-dasharray:1.5 2;stroke-width:1;fill:none;opacity:.72}
#tree .whole-dot,#tree .whole-head{cursor:pointer}
#tree .whole-dot .whole-hit{fill:transparent}
#tree .whole-dot text{display:none;font:2.5px Georgia,serif;fill:#fff3dc;paint-order:stroke;stroke:#1b3d30;stroke-width:.6}
#tree .magnified .whole-dot text{display:block}
#tree .magnified .whole-labels{display:none}
#tree .whole-dot:hover circle:last-of-type{stroke:#fff;stroke-width:1.4}
#tree .whole-head rect{fill:#1a3d30;opacity:.91}
#tree .whole-head text{fill:#f8e8ca;font:12px Georgia,serif}
#tree .whole-head:focus text,#tree .whole-head:hover text{fill:#ffc98c}
#tree #kin-whole-active path{fill:none;stroke:#ffd18f;stroke-width:3}
#tree #kin-whole-active circle{fill:#ffbf70;stroke:#fff2ca;stroke-width:1}
#tree #kin-whole-active .whole-selected{fill:none;stroke:#fff4d9;stroke-width:2}
#tree .whole-foot{border-top:1px solid #4e6e58;padding-top:9px;justify-content:flex-start;gap:8px 20px}
#tree .whole-foot i{display:inline-block;width:20px;border-top:2px solid #a8c8ad;margin-right:6px;vertical-align:middle}
#tree .whole-foot i.mate{border-top-style:dotted}#tree .whole-foot i.guess{border-top-style:dashed}
#tree[data-view="whole"] :is(#kin-stage,#kin-focus,#kin-whole-route,#kin-whole-return){display:none!important}
#tree[data-view="family"] #kin-viz-pair{display:grid;grid-template-columns:minmax(0,2.7fr) minmax(225px,1fr);gap:12px;align-items:start}
#tree[data-view="family"] #kin-stage{grid-column:1;grid-row:1}
#tree[data-view="family"] #kin-whole{grid-column:2;grid-row:1}
#tree[data-view="family"] #kin-whole-svg{height:auto;aspect-ratio:1000/610;margin:7px 0}
#tree[data-view="family"] .whole-toolbar h3{font-size:21px}
#tree[data-view="family"] :is(.whole-foot,.whole-tools,#kin-whole-count){display:none}
#tree #kin-whole-route{display:flex;align-items:center;gap:2px 4px;flex-wrap:wrap;margin-top:10px}
#tree #kin-whole-route>span{width:100%;color:#eed2a5;font-size:12px}
#tree #kin-whole-route button{padding:2px 0;background:none;border:none;font:13px Georgia,serif}
#tree #kin-whole-route i{font-style:normal;color:#aabdac}
@media(max-width:820px){#tree[data-view="family"] #kin-viz-pair{grid-template-columns:1fr}
#tree[data-view="family"] #kin-whole{grid-column:1;grid-row:2}#tree[data-view="family"] #kin-whole-svg{height:115px}#tree[data-view="family"] .whole-toolbar{align-items:center}}
@media(max-width:550px){#tree #kin-whole-svg{height:auto;aspect-ratio:1.2}#tree .whole-toolbar h3{font-size:24px}}
</style>''')
s=s.replace('<div id="kin-stage">','''<div id="kin-viz-pair"><div id="kin-whole"><div class="whole-toolbar"><div><h3>Всё семейное древо</h3><span id="kin-whole-count"></span></div><div class="whole-tools"><button id="kin-zoom-out" type="button" aria-label="Уменьшить">−</button><button id="kin-zoom-reset" type="button" title="Уместить всё древо">100 %</button><button id="kin-zoom-in" type="button" aria-label="Увеличить">+</button></div><button id="kin-whole-return" type="button">← Ко всему древу</button></div>
<svg id="kin-whole-svg" aria-label="Все записи древа с линиями от родителей к детям и между супругами" role="group"></svg>
<div class="whole-foot"><span><i></i>Родители и дети</span><span><i class="mate"></i>Супруги</span><span><i class="guess"></i>Предполагаемое родство</span></div><div id="kin-whole-route"></div></div><div id="kin-stage">''')
s=s.replace('<details class="kin-overview"><summary>Обзор всего древа по поколениям','</div><details class="kin-overview"><summary>Указатель записей по строкам и поколениям')
s=s.replace('const stage=get(',Path('work/kin-whole.js').read_text('utf-8-sig')+'\nconst stage=get(')
s=s.replace('const up=family(p,\'up\'),down=family(p,\'down\');',"""const up=family(p,'up'),down=family(p,'down');
if(initializedMap){detailView=true;root.dataset.view='family';view.z=1;applyView();paintRoute(p,up)}""")
s=s.replace("selected=id;plot(id,true);window.selectedPersonId=id;","selected=id;window.selectedPersonId=id;").replace("const [x,y]=coords(p);get('ring')","plot(id,true);const [x,y]=coords(p);get('ring')")
s=s.replace("populate();select(initial||", "initializedMap=Boolean(initial);populate();select(initial||")
s=s.replace("people[0].id)),false);","people[0].id)),false);initializedMap=true;if(!initial)openOverview(false);")
s=s.replace('Выберите имя на ветви, чтобы открыть семью этого человека. Поиск охватывает все записи полного древа.','Каждая точка — отдельная запись. От старших поколений в центре линии расходятся к потомкам. Выберите человека на дереве или найдите его через поиск.')
p.write_text(s,'utf8')
