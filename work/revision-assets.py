from pathlib import Path
from base64 import b64encode
import mimetypes
ROOT=Path(__file__).parent/'assets-revision'
def asset(name):
 p=ROOT/name
 return 'data:'+mimetypes.guess_type(p.name)[0]+';base64,'+b64encode(p.read_bytes()).decode()
