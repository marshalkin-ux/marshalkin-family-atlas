from sheetdata import *
from collections import defaultdict
from statistics import median, mean

fem=set('Агафия Агафья Агофья Агрипина Акилина Александра Алесандра Алина Анастасия Ангелина Анна Валентина Варвара Василина Вера Вероника Виктория Влада Галина Гликерiя Дария Дарья Домна Евгения Евдокия Екатерина Елена Елизавета Елисавета Ефимия Ефросинья Ирина Иулия Клавдия Кристина Ксенiя Ксения Ксенья Лариса Лиля Любовь Людмила Маргарита Мария Маруся Марфа Марья Матрена Матрона Мелания Надежда Настасья Настя Наталия Наталья Нина Ольга Параскева Пелагiя Пелагея Полина Праскева Раиса София Софья Татьяна Томара Улиания Ульяна Фекла Феодосия Хистина Христина'.split())
unknown={'Женя','Ромна','Ане','Лиза'} # Лиза is corrected below
def norm_name(raw):
    value=re.split(r'\d|[?]|\s+умер|\s*\(умер',raw,1)[0]
    return value.strip('+ .-–') or raw
def years(raw):
    return [int(x) for x in re.findall(r'(?<!\d)(?:1[56789]|20)\d\d(?!\d)',raw)]
graph=[]; lookup={}; branches={}; mates={}; markers=0
comments={'H477':'Родство Ермолая и Николая оспаривается автором Xmind.', 'D10':'Год смерти отмечен вопросительным знаком.', 'F17':'Год рождения неизвестен, 1775 указан после тире.', 'H478':'Записанная смерть раньше рождения Матвея в соседней ячейке. Материнство и дата требуют проверки.', 'R150':'В Xmind 1916–1946. В короткой таблице ошибочное 1816.', 'R137':'По Xmind, пропал без вести в марте 1943 года.', 'R156':'По семейной записи в Xmind, воевала в годы Великой Отечественной войны.', 'R95':'Год рождения и февральская дата гибели расходятся с Xmind. Требуется сверка военного документа.', 'R97':'В Xmind встречаются версии гибели и пропажи без вести.', 'H18':'В Xmind другая пара лет: 1747 и 1780. В расчёт возраста не включён.', 'P59':'В Xmind указано возможное смешение двух записей о Вере.', 'T323':'детей не было','R683':'Вторая дата записана с месяцем 16. Возможно повторяет V493.', 'R324':'Автор отметил неопределённость пола.', 'R149':'Повторная запись Фёдора Андреевича (см. R96) как мужа Елены.', 'R142':'Вероятный повтор R95 в роли супруга Елены.'}
skip={'T323','R290'}
for r,cells in rows:
    if r<9:continue
    if r in [636,671,685,692,703]:branches.clear();mates.clear()
    for j in range(1,len(cells),2):
        cell=get_column_letter(j+1)+str(r); raw=content(cells[j]);mark=content(cells[j-1]);gen=(j+1)//2
        if cell in skip or not (raw or mark):continue
        if not raw:markers+=1
        role=re.fullmatch(r'\d*[жм]\d*',mark)
        if cell in ['J637','F18']:role=True;mark='ж'
        is_placeholder=not raw or bool(re.fullmatch(r'[?ХхXx]+|сын\s*\d*|дочь\s*\d*|падчерица\s*[?]+',raw,re.I))
        if cell=='F18':is_placeholder=True
        if not raw or cell=='F18':raw='Супруга (имя не указано)' if mark=='ж' else 'Супруг (имя не указано)'
        name=norm_name(raw) if not is_placeholder else (raw if not re.fullmatch(r'[?ХхXx]+',raw) else 'Имя не указано')
        if cell in ('R373','R374','V395'):name=name.split()[0]
        y=years(raw)
        birth=y[0] if y and cell not in ['F17','T242'] else None
        first=name.split(' ')[0].strip('(.+')
        if role:sex='ж' if 'ж' in mark else 'м'
        elif is_placeholder:sex='ж' if re.search('дочь|падчерица',raw,re.I) else 'м' if 'сын' in raw else '?'
        elif first in fem or first=='Лиза':sex='ж'
        elif cell in ['R286','X361','R324','P292']:sex='?'
        else:sex='м'
        person=dict(id='full-'+cell,cell=cell,row=r,gen=gen,raw=raw,name=name,year=birth,parents=[],spouseIds=[],sex=sex,faint=attr(cells[j],'color')=='#efefef',sourceColor=attr(cells[j],'color'),sourceFill=attr(cells[j],'background-color'),mark=mark,placeholder=is_placeholder,note=comments.get(cell,''),uncertain=False)
        graph.append(person);lookup[cell]=person
        if cell in ['H20','L562','L669'] or mark=='отчим':
            person['note']+=' Отдельная запись в семье. Родственная привязка требует проверки.'
            continue
        if role:
            main=branches.get(gen)
            if cell=='R682':main=lookup['P682']
            if main:
                main['spouseIds'].append(person['id']);person['spouseIds'].append(main['id'])
            mates[gen]=person
        else:
            main=branches.get(gen-1);spouse=mates.get(gen-1)
            if main:
                person['parents']=[main['id']]
                if spouse and spouse['id'] in main['spouseIds'] and cell not in ['J478','V332','V338'] and not main['placeholder']:
                    person['parents'].append(spouse['id'])
            if cell in ['J567','L632']:person['note']='В источнике указано: '+('падчерица.' if cell=='J567' else 'приёмный сын.')+' Тип родства отличен от кровного.'
            if cell=='H477':person['uncertain']=True
            if cell=='R683':person['parents']=['full-P682'];person['uncertain']=True
            branches[gen]=person;mates.pop(gen,None)
# The second wife of Yakov follows the descendants of his son in this column.
a=lookup['N621']
for i in a['spouseIds']:lookup[i[5:]]['spouseIds'].remove(a['id'])
a['spouseIds']=['full-N611'];lookup['N611']['spouseIds'].append(a['id'])
lookup['P287']['note']+=' Помета R290 упоминает других детей и 1957 год. Число и имена в этой записи не определены.'
lookup['R322']['note']+=' В T323 указано, что детей не было.'
lookup['T242']['note']+=' В скобках стоит 17.06.2022. Назначение даты следует уточнить.'
for p in graph:
    # Chronologically implausible links stay visible as hypotheses.
    for par in p['parents']:
        a=lookup[par[5:]]
        if p['year'] and a['year'] and not 12<=p['year']-a['year']<=80:
            p['uncertain']=True
            p['note']+=' Возрастная разница с предполагаемым родителем требует сверки.'
    if p['cell']=='R149':p['repeatOf']='full-R96'
for p in graph:
    if 637<=p['row']<=669:
        earlier=[x for x in graph if 505<=x['row']<=562 and x['gen']==p['gen'] and x['raw']==p['raw']]
        if len(earlier)==1:
            p['repeatOf']=earlier[0]['id']
        p['note']+=' Вариант ветви Алексея в нижней части листа.'
    if p['faint']:p['note']+=' Светло-серый шрифт оригинала. Отдельно показан вариант ветви.'
    if p.get('repeatOf'):p['note']+=' Параллельная запись: '+p['repeatOf'][5:]+'.'
for p in graph:
    if p['cell'] in ['R373','P376','P461','P61','P76','R381','N627','N624','R374']:
        p['note']+=' См. раздел статистики случаев и семейную карту Xmind.'
(root/'fullPeople.json').write_text(json.dumps(graph,ensure_ascii=False),'utf8')
print('graph',len(graph),'name',sum(not p['placeholder'] for p in graph),'marker-only',markers,'repeat',sum('repeatOf' in p for p in graph),'faint',sum(p['faint'] for p in graph),'sex',Counter(p['sex'] for p in graph))

