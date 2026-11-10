"""Record-level military audit. Never deduplicates people from names alone."""
import json,re
from collections import Counter,defaultdict
from pathlib import Path
from war_import import archive,allrows,sheet,family

ROOT=Path(__file__).resolve().parent
STATUS={'призывник','военнообязанный','военнообязанный зап.','военнослужащий','курсант','мл. командир','мл. нач. состав','командир отделения','б/зв.','артиллерист','гидроакустик'}
def rank_tokens(raw):
    values=[]
    for token in (raw or '').lower().split('|'):
        token=token.strip()
        if not token or token in STATUS:continue
        token=re.sub(r'^гв\.\s*','',token)
        token=re.sub(r'^ст\.\s*','старший ',token)
        token=re.sub(r'^мл\.\s*','младший ',token)
        token=token.replace('мед. сл.','медицинской службы').replace('медслужбы','медицинской службы').replace('арт.-тех. сл.','артиллерийско-технической службы').replace('админ. сл.','административной службы').replace('тех. сл.','технической службы')
        if token not in values:values.append(token)
    return values

records=[]
for index,row in enumerate(allrows,2):
    no,surname,variant,name,pat,birth,place,rank,service,fate,award,kind,source,docs,_=row
    target=sheet.cell(index,15).hyperlink
    url=target.target if target else ''
    if not url and str(row[14]).startswith('='):
        match=re.search(r'https?://[^\"]+',row[14]);url=match[0] if match else ''
    records.append(dict(no=no,fio=' '.join(str(v) for v in [surname,name,pat] if v),surname=surname,birth=birth or '',place=place or '',rank=rank or '',award=award or '',service=service or '',source=source or '',url=url,rank_tokens=rank_tokens(rank),guard=bool(re.search(r'\bгв\.',str(rank or ''),re.I)),marshalkin_family_spelling=bool(family.search(' '.join(str(v or '') for v in (surname,variant)))),in_stavropol_selection=no in {r['no'] for r in archive}))

def counter_rows(rs,key):
    groups=defaultdict(list)
    for r in rs:
        vals=r[key] if isinstance(r[key],list) else [r[key]]
        for val in vals:
            if val:groups[val].append(r['no'])
    return [dict(label=k,count=len(v),record_ids=v) for k,v in sorted(groups.items(),key=lambda kv:(-len(kv[1]),kv[0]))]

def audit(rs):
    exact=defaultdict(list)
    yearly=defaultdict(list)
    for r in rs:
        exact[(r['fio'],r['birth'])].append(r['no'])
        yr=re.search(r'\b(18|19|20)\d{2}\b',r['birth'])
        if yr:yearly[(r['fio'],yr[0])].append(r['no'])
    nr=sum(bool(r['rank_tokens']) for r in rs)
    return dict(total_records=len(rs),rank_field_nonempty=sum(bool(r['rank']) for r in rs),records_with_recognized_rank=nr,rank_field_empty=sum(not r['rank'] for r in rs),status_or_occupation_only=sum(bool(r['rank']) and not r['rank_tokens'] for r in rs),rank_mentions=sum(len(r['rank_tokens']) for r in rs),guard_record_count=sum(r['guard'] for r in rs),award_field_nonempty=sum(bool(r['award']) for r in rs),award_field_empty=sum(not r['award'] for r in rs),award_types=len({r['award'] for r in rs if r['award']}),hero_award_record_ids=[r['no'] for r in rs if re.search(r'геро[йя]|золотая звезда',r['award'],re.I)],ranks=counter_rows(rs,'rank_tokens'),rank_raw=counter_rows(rs,'rank'),awards=counter_rows(rs,'award'),exact_fio_birth_groups=[dict(fio=k[0],birth=k[1],record_ids=v) for k,v in exact.items() if len(v)>1],fio_year_candidate_groups=[dict(fio=k[0],birth_year=k[1],record_ids=v) for k,v in yearly.items() if len(v)>1],same_url_groups=[dict(url=k,record_ids=[r['no'] for r in rs if r['url']==k]) for k,n in Counter(r['url'] for r in rs if r['url']).items() if n>1])

scopes={'stavropol_88':[r for r in records if r['in_stavropol_selection']], 'marshalkin_spellings_547':[r for r in records if r['marshalkin_family_spelling']], 'entire_workbook_737':records}
data=dict(methodology={'unit':'Строка выгрузки, не уникальный человек. Награда в строке не равна всей совокупности наград человека.','rank':'Снято обозначение гвардейской части, раскрыты сокращения. Различия родов службы сохранены. Несколько званий через | учитываются отдельно, одна строка может попасть в две категории.','missing':'Пустое поле означает отсутствие сведений в выгрузке, а не отсутствие звания/наград.','scope':'737 строк содержат 547 записей написаний Маршалкин/Моршалкин и вариантов; ещё 190 строк — Маршанский/Моршанский. Ставропольская выборка 88 — географический отбор, не доказанный список родственников.','period':'Награды и звания могут относиться к послевоенному периоду. Без дат документов нельзя называть все награды полученными в 1941–1945 годах.','identity':'Совпадение ФИО и года/даты рождения — кандидат на сопоставление, не автоматическая идентификация.'},scopes={k:audit(rs) for k,rs in scopes.items()},records=records,high_rank_records=[r['no'] for r in records if re.search(r'полковник|майор|генерал|военврач 2 ранга',r['rank'],re.I)],highlight_records={'stavropol_captain':[410],'stavropol_courage':[r['no'] for r in records if r['in_stavropol_selection'] and 'За отвагу' in r['award']],'stavropol_glory':[205],'stavropol_red_star':[163,679],'outside_colonels':[73,74,78,79,80,81,389,390,392],'outside_red_banner':[76]},cross_scope_candidates=[dict(record_ids=[399,400],reason='Полное совпадение ФИО и полной даты рождения; у №399 нет места рождения, звание майор административной службы, у №400 старший лейтенант медслужбы. Соответствие требует проверки исходных документов.')])
assert len(records)==737 and len(scopes['marshalkin_spellings_547'])==547 and len(scopes['stavropol_88'])==88
assert data['scopes']['stavropol_88']['award_field_nonempty']==31
assert all(not v['hero_award_record_ids'] for v in data['scopes'].values())
(ROOT/'military-audit.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),'utf8')
for scope,a in data['scopes'].items():
    print(scope,{k:v for k,v in a.items() if not isinstance(v,list)})
