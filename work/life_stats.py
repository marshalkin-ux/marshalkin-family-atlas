from fullbuild import *
from html import escape
from math import floor

exceptions={'H18','D10','P59','R95','R97','R180','H478'}
extra={'R150':1946,'T151':2003,'P301':1979,'R331':1946,'J571':1863,'R324':1993}
complete_extra={'T151':(date(1940,2,10),date(2003,4,2)),'P301':(date(1896,1,5),date(1979,10,22)),'R324':(date(1900,6,8),date(1993,7,14))}
sample=[]
for p in graph:
    c=p['cell']; raw=p['raw']; y=years(raw)
    if p.get('repeatOf') or 636<=p['row']<=683 or c in exceptions or ' или ' in raw:continue
    if c in extra:y=[p['year'],extra[c]]
    if c=='R324':y[0]=1900
    if c in ['R330','V392']:
        value=18 if c=='R330' else 9
        sample.append(dict(cell=c,name=p['name'],birth=p['year'],death=None,age=value,low=value,high=value,exact=False,source='Xmind · указан возраст'))
        continue
    if len(y)!=2 or y[1]<y[0]:continue
    dates=[date(int(yr),int(m),int(d)) for d,m,yr in re.findall(r'(\d{1,2})\.(\d{1,2})\.((?:1[6789]|20)\d\d)',raw)]
    if c in complete_extra:dates=list(complete_extra[c])
    diff=y[1]-y[0]
    exact=len(dates)==2
    if exact:
        b,d=dates
        age=d.year-b.year-((d.month,d.day)<(b.month,b.day))
        low=high=age
    else:
        low=max(0,diff-1);high=diff;age=(low+high)/2
    recorded_age={'H19':43,'J21':22,'P76':8,'N295':1,'R381':1,'P461':40,'P376':37}
    if c in recorded_age:low=high=age=recorded_age[c]
    sample.append(dict(cell=c,name=p['name'],birth=y[0],death=y[1],age=age,low=low,high=high,exact=exact,source='Xmind · возраст из метрики' if c in recorded_age else 'Xmind и лист' if c in extra else 'Большой лист'))
def fmt(n):return f'{n:.1f}'.replace('.',',')
def med(xs):return median(p['age'] for p in xs)
def avg(xs,key='age'):return mean(p[key] for p in xs)
adult=[p for p in sample if p['low']>=18];children=[p for p in sample if p['high']<18];exact=[p for p in sample if p['exact']]
assert len(adult)+len(children)==len(sample),'border at age 18'
bins=[(0,1,'До года'),(1,5,'1–4'),(5,18,'5–17'),(18,40,'18–39'),(40,60,'40–59'),(60,80,'60–79'),(80,150,'80 и старше')]
hist=[]
for start,end,label in bins:
    sub=[p for p in sample if start<=p['age']<end]
    hist.append((label,len(sub)))
bars=''.join(f'<button class="agebar" type="button" onclick="showAgeBand({i})"><span>{label}</span><i style="width:{count/max(n for _,n in hist)*100:.2f}%"></i><b>{count}</b></button>' for i,(label,count) in enumerate(hist))
hist_rows=''.join(f'<tr data-age="{p["age"]}" data-born="{p["birth"]}"><td><button type="button" onclick="window.focusPerson(\'full-{p["cell"]}\')">{escape(p["name"])} ↗</button></td><td>{p["birth"]}–{p["death"]}</td><td>{p["low"]}' + (f'–{p["high"]}' if p['low']!=p['high'] else '')+f'</td><td>{p["source"]} · {p["cell"]}</td></tr>' for p in sorted(sample,key=lambda x:(x['age'],x['birth'])))
ages=[p['age'] for p in sample]
cohorts=[]
for era,cond in [('До 1850 года',lambda y:y<1850),('1850–1899',lambda y:1850<=y<1900),('С 1900 года',lambda y:y>=1900)]:
    sub=[p for p in sample if p['birth'] and cond(p['birth'])]
    cohorts.append(f'<tr><td>{era}</td><td>{len(sub)}</td><td>{sum(p["high"]<18 for p in sub)}</td><td>{fmt(avg(sub))}</td></tr>')
source_rows=''.join(cohorts)
all_deaths=Counter(p['death'] for p in sample)
band_json=json.dumps([[a,b] for a,b,_ in bins])
template=(root/'stats.template').read_text('utf8')
hist_rows=hist_rows.replace('None–None','годы неизвестны').replace('1907–None','1907 · умерла в 18 лет')
template=template.replace('Для {{N}} человек удалось составить пару «рождение — смерть» без явного противоречия.', 'Из 903 карточек большого листа для {{N}} разных людей установлены возраст смерти или интервал возраста. У остальных карточек другая степень полноты.').replace('Детские смерти составляют {{PCT}}% разобранных биографий.', 'Среди {{N}} разобранных биографий {{KIDS}} детских смертей ({{PCT}}%). Для остальных карточек возраст при смерти не рассчитывался. Одна биография с известным возрастом и без года рождения в таблицу по поколениям рождения не входит.').replace('Основа — большой лист, с дополнениями из Xmind для Василия (R150), Вячеслава (T151), Ивана (P301) и Тимофея (R331).','Основой служит большой лист. Xmind дополняет записи R150, T151, P301, R331 и J571. Для Фёдора R324 принят возраст 93 года по датам надгробья, которое, по словам составителя, опознала Татьяна Алфёрова. В таблице значится другой год рождения — 1904. Для Анны R330 и Надежды V392 родственники назвали возраст прямо: 18 и 9 лет. Для этих двух записей расчёт по разности лет не требуется.')
by_cell={p['cell']:p for p in sample}
def status(p):
    c=p['cell']
    if c in by_cell:return 'В расчёте'
    if p.get('repeatOf') or 636<=p['row']<=683:return 'Повтор или вариант ветви'
    if c in exceptions or c in ['T492','N584']:return 'Датировка спорна'
    return 'Недостаточно данных о возрасте'
coverage=Counter(status(p) for p in graph)
assert sum(coverage.values())==903 and len(by_cell)==len(sample) and len({p['id'] for p in graph})==903
parts=['В расчёте','Недостаточно данных о возрасте','Датировка спорна','Повтор или вариант ветви']
palette=['#265b4e','#9dada0','#bf8053','#d7cba9']
chart=''.join(f'<a href="#audit-age" onclick="document.getElementById(\'audit-age\').open=true" style="flex:{coverage[k]};background:{col}" title="{k}: {coverage[k]}"></a>' for k,col in zip(parts,palette))
key=''.join(f'<span><i style="background:{col}"></i><b>{coverage[k]}</b> {k.lower()}</span>' for k,col in zip(parts,palette))
template=template.replace('<div class="statdeck">',f'<div class="coveragePanel"><strong>От 903 карточек к {len(sample)} биографиям</strong><div class="coverageBar">{chart}</div><div class="coverageKey">{key}</div></div><div class="statdeck">')
template=template.replace('и Дмитрия, а также Фёдора R109 и Марьи H478','и Дмитрия, а также Марьи H478').replace('Для этих двух записей расчёт по разности лет не требуется.','У Фёдора R109 источники совпадают по годам 1888–1895. Сомнение составителя касается возраста отца, поэтому эти даты жизни включены. У Анны и Надежды использован указанный в источнике возраст.')
template=template.replace('</style>','.coveragePanel{margin:18px 0;padding:16px;border:1px solid #c5b99f}.coverageBar{display:flex;height:19px;margin:10px 0}.coverageKey{display:flex;gap:8px 17px;flex-wrap:wrap;font-size:13px}.coverageKey i{display:inline-block;width:10px;height:10px;margin-right:4px}</style>')
audit='<details id="audit-age"><summary>Проверка всех 903 карточек</summary><p>Каждая карточка попала ровно в одну строку сводки. Приоритет проверки: сопоставление личности, оценка дат, затем вычисление возраста.</p>'
for reason,count in coverage.items():
    audit+=f'<details><summary>{reason} · {count}</summary><div class="auditNames">'+''.join(f'<button type="button" onclick="window.focusPerson(\'full-{p["cell"]}\')">{escape(p["name"])} · {p["cell"]}</button>' for p in graph if status(p)==reason)+'</div></details>'
audit+='''<p>У Леонида (1938–1987) и Сергея (1971–2002) в Xmind приведены полные даты. В семье Михаила и Марфы Васильевны, строки 169–170, отдельных карточек этих потомков в большом листе нет. Их возраст — 48 лет и 30 лет — показан отдельно от выборки этого листа. Имена и числа из хронологии также нельзя автоматически прибавлять к реестру.</p></details>'''
template=template.replace('<details id="ageLedger">',audit+'<details id="ageLedger">')
template=template.replace('При указании только лет возможны','Для семи записей с неполными датами составитель привёл возраст из метрики: в расчёт вошло это прямое указание. В частности, Вере Тимофеевне (P376) в записи о смерти дано 37 лет, тогда как из подписи 1882–1918 получаются 35–36. У младенца Алексея R373 расходятся дни смерти по листу и заметке; в обеих версиях полных лет — ноль. При указании только лет возможны')
oldest=sorted((p for p in sample if p['low']>=80),key=lambda p:-p['age'])
names={'R96':'Фёдор Андреевич Маршалкин','R324':'Фёдор · ветвь Ивана 1876 г. р.','T527':'Иван · сын Ивана и Марии Шаталовой'}
lineages=[]
for p in oldest:
    age=str(p['low']) if p['low']==p['high'] else f'{p["low"]}–{p["high"]}'
    lineages.append(f'<button type="button" class="lifeRibbon" onclick="window.focusPerson(\'full-{p["cell"]}\')"><span>{escape(names.get(p["cell"],p["name"]))}<small>{p["birth"]} — {p["death"]} · {p["cell"]}</small></span><i style="--a:{(p["birth"]-1880)/145*100:.2f}%;--b:{(p["death"]-1880)/145*100:.2f}%"></i><strong>{age}</strong></button>')
longevity=f'''<section id="longevity"><div class="eyebrow">Возраст в семейных записях</div><h2>Долгожители семьи</h2><p>Выбран порог в 80 полных лет. Его достигли как минимум {len(oldest)} человек из расчётной выборки. Цветные линии показывают годы их жизни на общей шкале. Нажмите имя, чтобы открыть семью.</p><div class="lifeAxis"><span>Годы жизни</span><i>1880 <b>1950</b> 2025</i><span>Лет</span></div>{''.join(lineages)}<p><b>Самый большой установленный возраст — 95 лет.</b> Иван родился 12 сентября 1927 года и умер 20 сентября 2022-го, через восемь дней после дня рождения. Два разных Фёдора прожили по 93 года. У Фёдора из R324 таблица и надгробье расходятся по году рождения.</p><p>Отдельный случай — Илларион (T492). В источниках стоят 1908 и 1910 годы рождения, в Xmind указан 2001 год смерти. Обе версии дают возраст от 90 до 93 лет. Он показан здесь дополнительно к числу выше.</p></section>'''
template=template.replace('<h3>Что объясняют отдельные случаи</h3>',longevity+'<h3>Что объясняют отдельные случаи</h3>')
template=template.replace('</style>','''.auditNames{display:flex;flex-wrap:wrap;gap:5px}.auditNames button{font:inherit;background:transparent;border:1px solid #c7c5ae;cursor:pointer}.lifeStats #longevity{margin:32px 0}.lifeRibbon,.lifeAxis{display:grid;grid-template-columns:minmax(140px,1.3fr) 2fr 48px;align-items:center;gap:12px;width:100%;text-align:left;color:#24473e}.lifeRibbon{border:0;border-bottom:1px solid #d7cbb5;background:transparent;padding:5px 2px;font:inherit;cursor:pointer}.lifeRibbon:hover{background:#e6e8db}.lifeRibbon small{display:block;font-size:11px}.lifeRibbon i{height:9px;background:linear-gradient(to right,transparent var(--a),#477969 var(--a),#a88d59 var(--b),transparent var(--b));border-bottom:1px solid #c7bcaa}.lifeRibbon strong{text-align:right}.lifeAxis{font-size:12px;margin:10px 0}.lifeAxis i{display:flex;justify-content:space-between;font-style:normal}.lifeAxis span:last-child{text-align:right}</style>''')
values={'N':len(sample),'MEAN':fmt(avg(sample)),'MEDIAN':fmt(med(sample)),'ADULT':fmt(avg(adult)),'NADULT':len(adult),'KIDS':len(children),'PCT':round(len(children)*100/len(sample)),'EXACT':len(exact),'EXACTAVG':fmt(avg(exact)),'LO':fmt(avg(sample,'low')),'HI':fmt(avg(sample,'high')),'BARS':bars,'ROWS':hist_rows,'BANDS':band_json,'COHORTS':source_rows,'1918':all_deaths[1918],'TOTAL':len(graph),'NAMED':sum(not p['placeholder'] for p in graph),'ANON':sum(p['placeholder'] for p in graph),'BIRTH':sum(bool(p['year']) for p in graph),'REPEAT':sum('repeatOf'in p for p in graph)}
for k,v in values.items():template=template.replace('{{'+k+'}}',str(v))
(root/'stats-section.html').write_text(template,'utf8')
print({k:v for k,v in values.items() if k not in ['ROWS','BANDS','BARS','COHORTS']})
