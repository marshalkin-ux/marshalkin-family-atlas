from pathlib import Path
import re,json,base64
from hashlib import pbkdf2_hmac
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
s=Path('work/story-revision-baseline.html').read_text('utf8');pack=json.loads(re.search(r'const sealed=(\[.*?\]);',s)[1]);salt,iv,data=map(base64.b64decode,pack);pw=Path('outputs/Пароль к семейному атласу.txt').read_text('utf8').strip();h=AESGCM(pbkdf2_hmac('sha256',pw.encode(),salt,600000,32)).decrypt(iv,data,None).decode();Path('work/pre-revision-private.html').write_text(h,'utf8')
from sys import path
path.insert(0,'work');import origins_build
imgs=re.findall(r'<img[^>]+src="(data:image/[^;]+;base64,[^"]+)"[^>]+alt="([^"]+)"',h)
keys={'PAINTING':'Семьи переселенцев','MAKAR':'Рукописный лист','BROTHERS':'Ревизская сказка с','MOVE':'Фрагмент о переходе','MANUSCRIPT':'Вертикальная рукопись'}
for key,label in keys.items():
 matches=[x for x in imgs if x[1].startswith(label)]
 if matches:
  p=Path('work/assets-revision/'+key.lower()+'.jpg');p.write_bytes(base64.b64decode(matches[0][0].split(',')[1]));print(key,'saved')
 else:print(key,'MISSING',[(x[1]) for x in imgs[:12]])

