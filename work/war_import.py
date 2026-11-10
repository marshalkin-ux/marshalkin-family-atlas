import re, json, html
from pathlib import Path
from collections import Counter
from urllib.parse import urlparse
from openpyxl import load_workbook

work=Path(__file__).resolve().parent
base=work.parent
file=work/'data/military.xlsx'
sheet=load_workbook(file,data_only=False)['Записи']
family=re.compile('м[ао]рш[ао]лкин',re.I)
region=re.compile(r'ставропольск(?:ий|ого) кр|г\.\s*ставропол[ья]|шпаковск|курcав|курсав|минеральные воды|минераловодск|невинномыс|кисловодск|ессентук|пятигорск|старо[ -]?марьевск|\bск\s+с\.\s*михайловск|ворошиловск.{0,45}с\.\s*михайловск',re.I)
archive=[]
allrows=list(sheet.values)[1:]
for index,row in enumerate(allrows,2):
    no,surname,variant,name,pat,birth,place,rank,service,fate,award,kind,source,docs,_=row
    if not family.search(' '.join(str(v or '') for v in (surname,variant))):continue
    def local(s):
        s=(s or '').lower().replace('ё','е')
        return bool(region.search(s)) and not any(bad in s for bad in ['куйбышевск','ворошиловградск','самарск'])
    birth_local=local(place)
    service_local=local(service)
    historic='орджоникидзевский край' in str(place or '').lower()
    if no==206:birth_local=True # Both city and historical region occur in this row.
    if not (birth_local or service_local or historic):continue
    target=sheet.cell(index,15).hyperlink
    url=target.target if target else ''
    if not url and str(row[14]).startswith('='):url=re.search(r'https?://[^"]+',row[14])[0]
    assert urlparse(url).hostname in ('pamyat-naroda.ru','www.pamyat-naroda.ru'),(no,url)
    archive.append(dict(no=no,fio=' '.join(str(v) for v in [surname,name,pat] if v),surname=surname,name=name,pat=pat,birth=birth or '',place=place or '',rank=rank or '',service=service or '',fate=fate or '',award=award or '',source=source or '',docs=docs or '',url=url,category='Место рождения' if birth_local else 'Призыв или служба' if service_local else 'Исторический край'))
if __name__=='__main__':
    print('TOTAL',len(allrows),len(archive),Counter(r['category'] for r in archive))
    for r in archive:print(r['no'],r['fio'],r['birth'],r['place'])
