from war_import import *
from military_stats import section as service_section, biographies
from familio_enrich import section as familio_section
from story_revision import apply as revise_story
from editorial_build import apply as editorial
from secrets import token_urlsafe,token_bytes
from hashlib import pbkdf2_hmac
from base64 import b64encode
from urllib.parse import urlsplit
import subprocess,sys
(base/'outputs').mkdir(exist_ok=True)
subprocess.run([sys.executable,str(work/'assemble.py')],check=True)
out=base/'outputs'
out.mkdir(exist_ok=True)
matches={44:'R387',45:'R387',59:'R180',71:'R57',97:'R150',163:'R97',171:'R342',174:'R137',191:'R95',220:'R68',221:'R614',308:'P275',320:'P275',370:'R465',396:'R552',414:'R517',473:'T424',474:'T424',489:'R96',494:'R324',694:'R96',685:'P307'}
notes={45:'Расходится день рождения: в древе 12 октября, в военной записи 12 марта.',59:'23 января 1942 года в военной записи — дата пропажи без вести. Возраст смерти исключён из статистики.',163:'Совпадают имя, отчество, год рождения, село и дата выбытия. Звание в выгрузке — младший лейтенант.',174:'Подтверждается статус «пропал без вести» в марте 1943 года.',191:'Военная запись даёт 1910 год рождения. По этой строке нельзя разрешить разночтение о дне гибели.',220:'Совпадают также день и месяц рождения — 14 сентября.',370:'В подборке есть несколько одноимённых Николаев 1918 года рождения. Эта карточка указывает Михайловку, но версия требует проверки.',494:'Год рождения совпадает с датой на надгробье, приведённой в Xmind; в схеме также фигурирует 1904 год.',694:'Вариант написания фамилии и иной военкомат. Награда относится к военной записи; личность требует сверки.'}
esc=lambda s:html.escape(str(s),quote=True)
def render(private):
    cards=[]
    for r in archive:
        no=r['no'];cell=matches.get(no);place=re.split(r',?\s+(?:ул\.|улица|ул\s)',r['place'],flags=re.I)[0]
        if no==257:place='г. Орджоникидзе'
        birth=r['birth'].replace('__.__.','').replace('00.00.','')
        fields=[('Рождение',place),('Звание',r['rank']),('Призыв / служба',r['service']),('Выбытие',r['fate']),('Награды',r['award']),('Источник в выгрузке',r['source'])]
        go=f'<p><button data-family="full-{cell}" onclick="window.focusPerson(this.dataset.family)">Открыть {cell} в древе ↗</button> {esc(notes.get(no,"Предполагаемое соответствие по имени, отчеству, году и региону."))}</p>' if private and cell else ''
        cards.append(f'<details id="pn-{no}" class="pnrecord"><summary><strong>{esc(r["fio"])}</strong> · {esc(birth or "год неизвестен")} <small>№ {no}</small></summary><p>{esc(r["category"])}</p><dl>'+''.join(f'<dt>{k}</dt><dd>{esc(v)}</dd>' for k,v in fields if v)+'</dl>'+go+f'<a target="_blank" rel="noopener" href="{esc(r["url"])}">Карточка «Памяти народа» ↗</a></details>')
    return f'''<section class="pn" id="military"><span>ВОЕННЫЙ АРХИВ · СТАВРОПОЛЬЕ</span><h2>Маршалкины на страницах военных документов</h2><p>Из 737 строк семейной выгрузки отобраны {len(cards)} записей. {sum(r['category']=='Место рождения' for r in archive)} содержат ставропольское место рождения, {sum(r['category']=='Призыв или служба' for r in archive)} связаны с краем по графе службы или призыва. Ещё {sum(r['category']=='Исторический край' for r in archive)} выделены по историческому названию Орджоникидзевского края. У одного человека может быть несколько документов.</p><label>Поиск по имени, населённому пункту, награде <input type="search" id="pnq" placeholder="Например, Курсавка"></label><p id="pncount"></p><div>'''+''.join(cards)+'''</div></section><script>(()=>{let q=document.querySelector('#pnq'),a=[...document.querySelectorAll('.pnrecord')];function find(){let words=q.value.toLowerCase().replaceAll('ё','е').trim().split(/\s+/);for(const r of a)r.hidden=!words.every(w=>r.textContent.toLowerCase().replaceAll('ё','е').includes(w));document.querySelector('#pncount').textContent='Записей: '+a.filter(r=>!r.hidden).length}q.oninput=find;find()})()</script>'''
style='''<style>.pn,.ww{max-width:1100px;margin:2rem auto;padding:20px}.pn>span,.ww-k{font:600 12px system-ui;letter-spacing:.15em;color:#966340}.pnrecord{padding:12px;border-bottom:1px solid #b5b5a5}.pnrecord summary{cursor:pointer}.pnrecord dt{font-weight:600}.pnrecord dd{margin:0 0 6px}.pnrecord small{color:#786b54}.pn input{padding:9px;width:min(100%,360px)}.pn [hidden]{display:none}.ww-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(210px,100%),1fr));gap:10px}.ww-grid article{background:#eee9dc;border-top:3px solid #997542;padding:13px}.ww-grid h4{margin:.35em 0}.ww h3{margin:23px 0 8px}.ww p{max-width:78ch}.ww a{color:#2c624e}.ww-marker{font:600 14px system-ui;color:#81532c}.ww nav{display:flex;gap:14px;flex-wrap:wrap}.ww details{margin:12px 0}.ww summary{cursor:pointer}.ww-bar{height:10px;display:flex;border-radius:9px;overflow:hidden}.ww-bar i{background:#305e4e}.ww-bar b{background:#ae8050}.ww-bar em{background:#9aafb2}</style>'''
def chapter(private):
    def evidence(n):
        r=next(r for r in archive if r['no']==n)
        family_link=f' · <button data-family="full-{matches[n]}" onclick="window.focusPerson(this.dataset.family)">К семье ↗</button>' if private and n in matches else ''
        return f'<a href="{esc(r["url"])}" target="_blank" rel="noopener">Запись № {n} ↗</a>{family_link}'
    events=[
        ('1941 · призыв и плен','Алексей Давыдович Маршалкин','24 июня его призвал Ворошиловский РВК. Карточка относит пленение к 29 июля и сообщает об освобождении. Дата освобождения в выгрузке не указана.',45),
        ('1942 · пропажа без вести','Андрей Васильевич Маршалкин','Красноармеец 99-й стрелковой дивизии пропал без вести 23 января в Сталинской области. В семейной схеме эта же дата стояла второй датой жизни. В обновлённом атласе она исключена из расчёта возраста смерти.',59),
        ('1942–1943 · призыв и потеря связи','Ефим Иванович Маршалкин','Ефима, уроженца Михайловского 1908 года рождения, призвали 18 марта 1942 года. В марте 1943-го он числится пропавшим без вести. В семье сохранились сведения и о службе его брата Василия.',174),
        ('1943 · смерть от ран','Дмитрий Андреевич Маршалкин','Младший лейтенант 1373-го стрелкового полка 416-й стрелковой дивизии умер от ран 28 июня. Указан хутор Морской Чулак в Неклиновском районе Ростовской области. В карточке записан орден Красной Звезды.',163),
        ('1944 · гибель во Львовской области','Иван Илларионович Маршалкин','Гвардии ефрейтор, уроженец Михайловки 1900 года рождения, погиб 20 июля у села Дембино. День выбытия совпадает со второй датой в семейной записи.',221),
        ('1945 · извещение о пропаже','Михаил Тимофеевич Маршалкин','Карточка уроженца Михайловского 1895 года рождения относит пропажу без вести к апрелю. Место боя по этой записи установить нельзя.',313)]
    tiles=''.join(f'<article><span class="ww-marker">{year}</span><h4>{name}</h4><p>{desc}</p>{evidence(n)}</article>' for year,name,desc,n in events)
    return f'''<section class="ww" id="world-war"><span class="ww-k">ВТОРАЯ МИРОВАЯ ВОЙНА · СТАВРОПОЛЬЕ</span><h2>Маршалкины в годы Великой Отечественной войны</h2><nav><a href="#ww-years">По годам</a><a href="#ww-units">Служба и награды</a><a href="#ww-evidence">Как читать записи</a><a href="#military">Весь реестр ↓</a></nav><p>Великая Отечественная война началась 22 июня 1941 года и непосредственно затронула семью Маршалкиных. Родственники были призваны на службу; среди них были погибшие, пропавшие без вести и вернувшиеся с фронта. Военные документы сохранили сведения об их службе и наградах. Ниже прослежены судьбы 1941–1945 годов; для каждого эпизода можно открыть карточку источника.</p><h3 id="ww-years">От призыва до последнего известия</h3><div class="ww-grid">{tiles}</div><h3 id="ww-units">Где служили и за что награждены</h3><p><b>Оборона Кавказа.</b> Медаль «За оборону Кавказа» указана у младшего лейтенанта Ивана Ивановича и старшего сержанта Павла Васильевича. У Ивана совпадает полная дата рождения — 14 сентября 1904 года. У Павла в выгрузке указаны 317-я стрелковая дивизия и 18-я армия. Даты конкретного боя в этих строках отсутствуют. {evidence(220)} · {evidence(396)}</p><p><b>Из Ставрополя через Баку.</b> Василий Иванович, 1916 года рождения, был призван в 1942 году Октябрьским РВК Баку. Эта запись добавляет звание старшего сержанта. Сообщение о его награждении орденом Красной Звезды приводится отдельно, по семейной карте. {evidence(97)}</p><p><b>Награды разных лет.</b> В карточке Тимофея Ивановича указана медаль «За отвагу». Орден Отечественной войны II степени у Фёдора Андреевича приведён в юбилейной картотеке. По ней нельзя датировать награждение годами войны. {evidence(473)} · {evidence(489)}</p><h3 id="ww-evidence">Что добавила выгрузка</h3><div class="ww-bar" aria-label="68 записей по рождению, 11 по службе, 9 по историческому краю"><i style="flex:68"></i><b style="flex:11"></b><em style="flex:9"></em></div><p><b>68</b> записей отобраны по месту рождения, <b>11</b> — по службе или призыву, ещё <b>9</b> — по историческому названию края в месте рождения. Из этих 88 строк в 76 заполнено звание, в 44 — сведения о выбытии, в 31 — награда. Категории пересекаются.</p><p>Для 22 строк отмечены возможные соответствия 18 карточкам семейного дерева. Остальные 66 сохранены как региональный материал. Однофамильцы могут происходить из разных семей, а на одного бойца могут приходиться несколько записей. Ссылки ведут к карточкам, сохранённым в Excel; степень родства проверяется отдельно.</p></section>'''
private=out/'Маршалкины.html'
atlas=private.read_text('utf8')
atlas=atlas.replace('<section id="sources"',style+chapter(True)+service_section(True)+render(True)+biographies()+'<section id="sources"',1).replace('<a href="#sources">','<a href="#world-war">Война 1941–1945</a><a href="#military-stats">Звания и награды</a><a href="#lives">Люди и призвания</a><a href="#sources">',1)
lookup={}
for no,c in matches.items():lookup.setdefault('full-'+c,[]).append(no)
script="""<script>document.addEventListener('personchange',e=>{const ids=WARIDS[e.detail.id];if(!ids)return;const card=document.querySelector('#kin-focus .kin-card');if(!card)return;const h=document.createElement('h4');h.textContent='Военные записи для сверки';card.append(h);for(const n of ids){const d=document.getElementById('pn-'+n),a=document.createElement('a');a.className='sourceJump';a.href='#pn-'+n;a.textContent=d.querySelector('summary').textContent;a.onclick=()=>{document.querySelector('#pnq').value='';document.querySelector('#pnq').dispatchEvent(new Event('input'));d.open=true};card.append(a)}})</script>""".replace('WARIDS',json.dumps(lookup))
atlas=atlas.replace('</body>',script+'</body>').replace('У Ефима в марте 1943 года','Для Андрея R180 выгрузка указывает пропажу без вести 23.01.1942; эту дату исключили из расчёта смерти. У Ефима в марте 1943 года')
from names_build import section as names_section
atlas=atlas.replace('<section id="sources"',names_section()+'<section id="sources"',1)
atlas=atlas.replace('<a href="#stats">В цифрах</a>','<a href="#stats">В цифрах</a><a href="#names">Имена семьи</a>',1)
from origins_build import section as origins_section
atlas=atlas.replace('<main>','<main>'+origins_section(),1)
atlas=atlas.replace('<a href="#tree">Древо</a>','<a href="#origins">Истоки рода</a><a href="#tree">Древо</a>',1)
from heritage_build import apply_private,apply_public
atlas=atlas.replace('<section id="sources"',(work/'familio-family.html').read_text('utf8')+'<section id="sources"',1)
atlas=atlas.replace('<a href="lives">','<a href="lives">')
atlas=atlas.replace('<a href="#sources">','<a href="#yaroslav-family">Семья Ярослава</a><a href="#sources">',1)
atlas=atlas.replace('<section id="sources"',familio_section()+'<section id="sources"',1)
atlas=atlas.replace('<a href="#sources">','<a href="#familio-review">Находки Familio</a><a href="#sources">',1)
atlas=editorial(revise_story(apply_private(atlas)))
from surname_build import apply as apply_surname
atlas=apply_surname(atlas)
private.write_text(atlas,'utf8')
(out/'index.html').write_text(atlas,'utf8')
(base/'index.html').write_text(atlas,'utf8')
print('Built public atlas:', len(atlas.encode()), 'bytes')
