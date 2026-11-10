from pathlib import Path
from base64 import b64encode
import re

ROOT = Path(__file__).resolve().parent
ASSETS = {
    'PAINTING': ROOT/'assets-revision/unused.jpg',
    'MAKAR': ROOT/'assets-revision/unused.jpg',
    'BROTHERS': ROOT/'assets-revision/unused.jpg',
    'MOVE': ROOT/'assets-revision/unused.jpg',
    'MANUSCRIPT': ROOT/'assets-revision/unused.jpg',
    'VILLAGE': ROOT / 'origin-begichevo.jpg',
    'ARMS': ROOT / 'origin-oboyan.png',
}

for key in ['PAINTING','MAKAR','BROTHERS','MOVE','MANUSCRIPT']:
    ASSETS[key]=ROOT/'assets-revision'/(key.lower()+'.jpg')

def section():
    markup = (ROOT / 'origins-section.html').read_text('utf8')
    for key, path in ASSETS.items():
        mime = 'image/png' if path.suffix == '.png' else 'image/jpeg'
        markup = markup.replace('{{' + key + '}}', 'data:' + mime + ';base64,' + b64encode(path.read_bytes()).decode())
    assert not re.search(r'\{\{[A-Z]+\}\}', markup)
    return markup
