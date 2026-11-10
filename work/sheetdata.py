import re, json
from collections import Counter
from pathlib import Path
from lxml import html
from openpyxl.utils import get_column_letter
from datetime import date
root=Path(__file__).resolve().parent
doc=html.fromstring((root/'fullsheet.html').read_text('utf8'))
css=''.join(doc.xpath('//style/text()'))
styles=dict(re.findall(r'\.waffle \.(s\d+)\s*\{([^}]+)\}',css))
rows=[]
for tr in doc.xpath('//tr[th[@id]]'):
    label=tr[0].text_content().strip()
    if not label.isdigit():continue
    rows.append((int(label),tr.xpath('td')))
def content(c):
    return ' '.join(c.text_content().split())
def attr(c,key):
    css=styles.get(c.get('class','').split()[0],'')
    match=re.search(r'(?:^|;)'+key+r':([^;]+)',css)
    return match[1] if match else ''
entries=[]
for r,cells in rows:
    if r<9:continue
    for j in range(1,len(cells),2):
        c=cells[j]
        raw=content(c)
        if not raw:continue
        entries.append(dict(row=r,gen=(j+1)//2,cell=get_column_letter(j+1)+str(r),mark=content(cells[j-1]),raw=raw,ink=attr(c,'color'),bg=attr(c,'background-color')))
if __name__=='__main__':
    print('Rows',len(rows),'records',len(entries),'colors',Counter(e['ink'] for e in entries),'bg',Counter(e['bg'] for e in entries))
    for e in entries:
        if not e['mark'] or len(e['raw'])>60 or not re.search('[А-Яа-я]',e['raw']):
            print(e['cell'],e['mark'],e['raw'])
    print('DATES')
    for e in entries:
        if len(re.findall(r'(?<!\d)(?:1[56789]|20)\d\d(?!\d)',e['raw']))>=2: print(e['cell'],e['raw'])
