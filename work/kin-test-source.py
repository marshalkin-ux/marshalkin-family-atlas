from sheetdata import entries, root
import json
out=[]
for entry in entries:
    ident='full-'+entry['cell']
    previous=next((e for e in reversed(out) if e['gen']==entry['gen']-1),None)
    out.append(dict(entry,id=ident,name=entry['raw'].split()[0],parents=[previous['id']] if previous else [],spouseIds=[],sex='',year=None,note=''))
(root/'kin-test-full.json').write_text(json.dumps(out,ensure_ascii=False),'utf8')
print(len(out))
