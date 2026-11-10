from pathlib import Path
from collections import Counter
import json,re
from build import people,groups
from life_stats import graph,root

cross='''G3 L105 H3 N106 H4 N124 H5 N131 H6 N133 H7 N134 I7 P136 J7 R137 J8 R138 K8 T140 J9 R141 K9 T142 L9 V144 M9 X145 J10 R150 K10 T151 L10 V152 M10 X154 J11 R156 E12 H18 J12 R157 E13 H568 H13 N172 B14 B9 C14 D10 D14 F17 E14 H29 F14 J104 G14 L311 H14 N312 I14 P321 J14 R331 K14 T332 L14 V335 I15 P343 J15 R344 K15 T345 L15 V346 H16 N382 I16 P389 J16 R390 K16 T393 L16 V394 L17 V405 L18 V413 M18 X414 M19 X416 L20 V419 L21 V422 K22 T424 L22 V425 M22 X426 K23 T431 L23 V432 L24 V438 H25 N470 H26 N472 H27 N474 H28 N475 G29 L175 H29 N176 I29 P202 J29 R203 K29 T241 L29 V242 K30 T214 K30b T215 L30 V233 L31 V238 K32 T243 L32 V248 I33 P178 J33 R180 K33 T181 L33 V182 M33 X186 H34 N294 H35 N295 H36 N296 H37 N297 H38 N310 E39 H477 F39 J504 G39 L506 H39 N522 I39 P531 J39 R533 K39 T534 L39 V535 M39 X539 M39b X536'''.split()
links=dict(zip(cross[::2],cross[1::2]))
assert len(links)==len(people)
big={p['cell']:p for p in graph}
for p in people:
    other=big[links[p['id']]]
    p['otherCard']=other['id'];other['otherCard']=p['id']
    if p.get('contact'):other['contact']=p['contact']
    if p['id']=='K32':p['note']+=' В полной диаграмме запись T243 расположена в семье Фёдора R203.'
    if p['id']=='L24':p['note']='В полном листе V438 указан Виктор, 16.11.1958. Виктор Фёдорович в комментарии называет профессию артиста балета, жену Ирину и детей Анну и Сергея.'
    if other['cell']=='P129':other['name']='Афанасьева Александра Ефремова'
for p in graph:
    if p['cell']=='P129':p['name']='Афанасьева Александра Ефремова'
    if p['cell']=='N106':p['name']='Изидаръ'
html=(root/'story.html').read_text('utf8')
html=html.replace('именных записей в основной семейной диаграмме. Каждый столбец диаграммы соответствует одному поколению, начиная с Корнея.', 'карточки большого листа, включая безымянных родственников и повторные записи. Поколения отсчитаны от столбца Макара.').replace('Сверху — число людей','Сверху — число записей').replace('именным записям основной семейной диаграммы','карточкам полного листа').replace('Мужские имена ·','Мужские записи ·').replace('Женские имена ·','Женские записи ·')
html=html.replace('В дополнительной схеме контактов','В основном листе имена занимают чётные столбцы B–Z. Число слева обозначает место среди детей, «ж» и «м» — супругов. Связи восстановлены по последовательности внутри семейных ветвей. Приёмное родство, отчимы и неясные привязки требуют чтения исходной подписи. Все варианты и повторы имеют собственные адреса ячеек. В дополнительной схеме контактов')
html=html.replace("p.textContent=names.map(x=>x.name).join(' · ');","""names.forEach(x=>{const b=document.createElement('button');b.type='button';b.className='recordChip';b.id='timeline-'+x.id;b.textContent=x.name;b.title='Найти в основном древе';b.onclick=()=>window.timelineSearch(b,x.name);p.append(b,' ')})""")
html=html.replace('Один человек может встречаться в нескольких записях.','Нажмите имя, чтобы найти кандидатов в дереве. Сопоставление требует проверки по родственникам и годам: в нескольких группах встречаются тёзки.')
for token,fn in [('TREE','tree-section.html'),('CASES','cases-section.html'),('HISTORY','history-section.html'),('STATS','stats-section.html')]:
    fragment=(root/fn).read_text('utf8')
    fragment=fragment.replace('связывает Маршалкиных с Кузьмиными','связывает Матвея с семьёй младенца').replace('Год рождения','Год рождения')
    if token in ['HISTORY','CASES']:
        fragment=re.sub(r"focusPerson\('([A-Z][0-9]+b?)'\)",lambda m:"focusPerson('full-"+links[m[1]]+"')",fragment)
    if token=='HISTORY':
        fragment=fragment.replace('Есть две даты рождения','В полном листе R95 записано 6 февраля, в заметке к военной карточке — 19 февраля. Есть две даты рождения')
    html=html.replace('{{'+token+'}}',fragment)
html=html.replace('{{DATA}}',json.dumps([people,groups,graph],ensure_ascii=False,separators=(',',':')).replace('</','<\\/'))
html=html.replace('расходятся дни смерти','расходится месяц смерти').replace('<a href="#stats">В цифрах</a>', '<a href="#stats">В цифрах</a><a href="#longevity">Долгожители</a>')
html=html.replace('<details class="folioDisclosure"><summary>Как читать разночтения и числа', '''<details class="folioDisclosure"><summary>Что удалось сверить между источниками</summary><p><b>Охват.</b> В представлении листа в браузере и в его табличной разметке сверены 704 строки, 877 непустых ячеек в столбцах имён и 19 почти белых записей. Первая схема даёт 91 карточку контактов, а указатель Time.Graphics — 209 подписей событий. В расчёте возраста используется проверка каждой из 903 карточек большого листа. Эти три счётчика описывают разные вещи.</p><p><b>Сопоставление биографий.</b> В R150 большого листа и в Xmind у Василия стоит 1916, в J10 короткой схемы — 1816. В T424 у Тимофея записана смерть 7 августа 1998 года, в Xmind — 8 августа; в обоих случаях ему было 73 года. В V438 текущее имя Виктор совпадает с пояснением Виктора Фёдоровича, хотя прежняя подпись комментария — Виталий.</p><p><b>Исторический контекст.</b> Датировки основания села, укреплённой линии и революции снабжены отдельными историческими ссылками. Поездка 1723 года, переселение 1785 года и сведения о военной службе восходят к семейным источникам. Тексты архивных записей и недоступные напрямую сканы ОБД переданы по выпискам Дениса Маршалкина. Положение людей в дереве следует обозначениям составителя, оно само по себе не удостоверяет каждое родство.</p><a href="#audit-age" onclick="document.getElementById('audit-age').open=true">Посмотреть решение по каждой карточке →</a></details><details class="folioDisclosure"><summary>Как читать разночтения и числа''')
html=html.replace('</body>',(root/'nav-extra.html').read_text('utf8')+'</body>')
assert not re.search(r'\{\{[A-Z]+\}\}',html)
out=root.parent/'outputs'/'Маршалкины.html'
out.write_text(html,'utf8')
print(out.stat().st_size)
