import json,re,collections
from pathlib import Path
root=Path('work');pages=json.loads((root/'familio-all-pages.json').read_text('utf8'));rs=[r for p in pages.values() for r in p['data']];people=json.loads((root/'fullPeople.json').read_text('utf8'));d={p['id']:p for p in people}
norm=lambda s:re.sub('[^а-я]','',s.lower().replace('ё','е'))
out=[]
for r in rs:
 if r.get('ownerId')!='2141a674-7746-4af6-95a6-fd6606562cc4':continue
 name=re.sub(r'\([^)]*\)','',r['displayName']).split(); given=name[1] if len(name)>1 else '';year=(r['birthDate'].get('first') or {}).get('year')
 candidates=[p for p in people if norm(given)==norm(p['name'].split()[0]) and year and p.get('year')==year]
 out.append(dict(uuid=r['uuid'],name=r['displayName'],birth=r['birthDate']['formatted'],death=(r.get('deathDate') or {}).get('formatted','Не указано'),bio=r.get('biography',''),candidates=[p['cell'] for p in candidates]))
(root/'familio-candidates.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
for r in out:
 if r['bio'] and len(r['candidates'])==1:print(r['candidates'][0],r['name'],r['birth'],r['death'],re.sub(r'https?://\S+','[link]',r['bio'])[:450])

