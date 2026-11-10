from pathlib import Path
p=Path('work/tree-section.html');s=p.read_text('utf8')
s=s.replace('</style>', '''
#tree #kin-stage{position:relative;border:1px solid #31594a;border-radius:6px;padding:clamp(15px,2.1vw,29px);background:radial-gradient(ellipse at 53% 63%,#294e3e,#16392f 69%);color:#fff5df;scroll-margin-top:5rem}
#tree .kin-stage-head{display:flex;justify-content:space-between;align-items:start;gap:12px;flex-wrap:wrap}
#tree .kin-stage-head h3{font:normal clamp(29px,4vw,47px)/1.1 Georgia,serif;color:#f8edd6;margin:0}
#tree #kin-branch-subtitle,#tree .kin-stage-foot,#tree .kin-stage-controls{font:14px/1.45 system-ui,sans-serif;color:#d5dfce}
#tree .kin-stage-controls{display:flex;gap:7px;flex-wrap:wrap;align-items:center}
#tree #kin-stage :is(button,select){font:14px/1.45 system-ui,sans-serif;border:1px solid #809781;background:#214838;color:#fcf5e4;border-radius:4px;padding:7px 10px;cursor:pointer}
#tree #kin-stage button:disabled{opacity:.45}
#tree #kin-branch-map{display:block;width:100%;height:auto;margin:5px 0}
#tree .kin-limb,#tree .kin-twig path{fill:none;stroke:#d6ab77;stroke-width:2.1;stroke-linecap:round}
#tree .kin-limb.l2{stroke:#b7b497;stroke-width:1.5}
#tree .kin-twig path{stroke:#a9ad87;stroke-width:1;opacity:.75}
#tree .kin-branch-node{cursor:pointer;outline:none}
#tree .kin-branch-node circle{fill:#c6cba9;stroke:#233f32;stroke-width:2}
#tree .kin-branch-node.l0 circle{fill:#edbd80}
#tree .kin-branch-node text{font-family:Georgia,serif;fill:#fff4d9;paint-order:stroke;stroke:#204333;stroke-width:5;stroke-linejoin:round}
#tree .kin-branch-node .kin-node-meta{font-family:system-ui,sans-serif;fill:#d6dbc2;stroke-width:4}
#tree .kin-branch-node:focus text,#tree .kin-branch-node:hover text{fill:#ffcd8a}
#tree .kin-branch-node:focus circle,#tree .kin-branch-node:hover circle{stroke:#ffdab1;stroke-width:3}
#tree .kin-stage-foot{padding-top:10px;border-top:1px solid #58705b;display:flex;justify-content:space-between;gap:8px;align-items:center;flex-wrap:wrap}
#tree #kin-branch-pages,#tree #kin-branch-mates{display:flex;align-items:center;gap:7px;flex-wrap:wrap}
#tree #kin-branch-mates:empty,#tree #kin-branch-pages:empty{display:none}
#tree .kin-sketch{animation:kinReveal .4s ease-out}
#tree .kin-overview{margin-top:14px;border:1px solid #c5c7b7;background:#f6f3e8;border-radius:4px;padding:0}
#tree .kin-overview>summary{padding:12px 16px;color:#254334;font:600 15px/1.5 system-ui,sans-serif}
#tree .kin-overview .kin-map{border-radius:0}
</style>''')
s=s.replace('<div class="kin-map"><div class="kin-map-head">','''<div id="kin-stage">
<div class="kin-stage-head"><div><h3 id="kin-branch-name"></h3><span id="kin-branch-subtitle"></span></div>
<div class="kin-stage-controls"><select id="kin-direction" aria-label="Направление ветви"><option value="down">Потомки</option><option value="up">Предки</option></select><button type="button" id="kin-branch-parent">На поколение вверх ↑</button></div></div>
<svg id="kin-branch-map" role="group" aria-label="Именное дерево выбранной семьи"></svg>
<div class="kin-stage-foot"><span id="kin-branch-help"></span><div id="kin-branch-pages"></div><div id="kin-branch-mates"></div></div></div>
<details class="kin-overview"><summary>Обзор всего древа по поколениям</summary><div class="kin-map"><div class="kin-map-head">''')
s=s.replace('<div class="kin-focus"','</details><div class="kin-focus"')
s=s.replace('function select(id,remember=true){',Path('work/branch-engine.js').read_text('utf-8-sig')+'\nfunction select(id,remember=true){')
s=s.replace("selected=id;window.selectedPersonId=id;","selected=id;plot(id,true);window.selectedPersonId=id;")
s=s.replace("if(scroll)get('focus').scrollIntoView", "if(scroll)get('stage').scrollIntoView").replace("block:'center'","block:'start'")
s=s.replace("by.has('full-D10')?'full-D10'", "by.has('full-J104')?'full-J104'")
s=s.replace("root.querySelector('.kin-head p').textContent=grouped?", "root.querySelector('.kin-head p').textContent=grouped?").replace('Вверху указаны поколения, слева — строки исходной таблицы. Число в группе показывает, сколько в ней записей. Выберите группу или найдите человека по имени.', 'Выберите имя на ветви, чтобы открыть семью этого человека. Поиск охватывает все записи полного древа.').replace('Выберите точку на схеме или найдите имя. В карточке можно перейти к родителям и детям.', 'Выберите имя на ветви, чтобы открыть семью этого человека. Найти запись можно также по фамилии из заметок о контактах.')
p.write_text(s,'utf8')
