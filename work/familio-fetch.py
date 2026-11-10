import urllib.request,json,concurrent.futures,pathlib
root=pathlib.Path('work');url='https://familio.org/api/v3/persons?surnameId=82f1f245-5672-45a0-890c-e6710cf61db2&page={}&itemsPerPage=20&orderBy=person_updated_at&orderDirection=desc&mentions=false'
def get(n):
 with urllib.request.urlopen(url.format(n),timeout=40) as r:return n,json.load(r)
first=get(1)[1];(root/'familio-page1.json').write_text(json.dumps(first,ensure_ascii=False,indent=2),encoding='utf8');print(str(first)[:250])
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 pages=list(pool.map(get,range(1,29)))
(root/'familio-all-pages.json').write_text(json.dumps(dict(pages),ensure_ascii=False),encoding='utf8');print('Fetched',len(pages),'pages')
