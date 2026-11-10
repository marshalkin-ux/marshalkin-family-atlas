from pathlib import Path
import json, re
from collections import Counter
from openpyxl import load_workbook

root = Path(__file__).resolve().parent
s = load_workbook(root/'living.xlsx').active
people = []
female = set('Пелагея Ирина Мария Елена Раиса Анна Любовь Татьяна Клавдия Валентина Наталья Надежда Марфа Ульяна Екатерина Галина Евдокия'.split())
for row in s['B3':'M39']:
    for c in row:
        if not c.value: continue
        parts = str(c.value).replace(' и ж.', '\n').splitlines()
        for i, part in enumerate(parts):
            name = part.split()[0]
            year = re.search(r'\d{4}', part)
            p = dict(id=c.coordinate+('b' if i else ''), cell=c.coordinate, name=name, raw=part, year=int(year[0]) if year else None, row=c.row, gen=c.column-1, sex='ж' if name in female else 'м', parents=[], note='')
            if c.coordinate == 'J10': p.update(year=1916,note='В таблице записано «Василий 1816». Карта Xmind приводит 1916–1946, отчество Иванович и ссылки на военные документы. В графике принят 1916 год.')
            people.append(p)
byid = {p['id']:p for p in people}
special={'E12':'D14','E13':'D14','E39':'D14','G3':'F14','G29':'F14','K32':None}
for p in people:
    rr, col=p['row'],p['gen']
    if p['id']=='K30b': continue
    if p['cell'] in special:
        par=special[p['cell']]
        if par: p['parents']=[par]
        p['uncertain']=True
        continue
    for candidate in people:
        if candidate['gen']!=col-1: continue
        coord=candidate['cell']
        end=next((rg.max_row for rg in s.merged_cells.ranges if rg.start_cell.coordinate==coord),candidate['row'])
        if candidate['row']<=rr<=end: p['parents'].append(candidate['id'])
    if p['id']=='J10': assert p['parents']==['I7']
for p in people:
    r=p['row']
    if s['O'+str(r)].value and p['gen']==max(x['gen'] for x in people if x['row']==r):
        p['contact']=s['O'+str(r)].value
for cell, note in {'H6':'В Xmind указаны 1861–1868. Возраст по годам — 6–7 лет.', 'J7':'В Xmind: Ефим, 1908 г. р., пропал без вести в марте 1943 года.', 'K10':'В Xmind приведены даты 10.02.1940–02.04.2003.', 'E14':'В карте также Ермил. Автор приводит альтернативную датировку 1751 г.', 'E39':'В Xmind указан 1754 год. Автор карты разбирает, но оставляет открытым вопрос о братстве Николая и Ермолая.', 'L24':'В комментарии V438 второй таблицы назван Виктором Фёдоровичем, артистом балета. В самой ячейке написано «Виталий». Сопоставление вероятно по Фёдору, имени и году.', 'K32':'На схеме рядом есть несколько возможных старших родственников. Связь Петра с предыдущим поколением требует проверки.'}.items():byid[cell]['note']=note
groups=json.loads((root/'groups.json').read_text('utf-8-sig'))
data=json.dumps([people,groups],ensure_ascii=False).replace('</','<\\/')
