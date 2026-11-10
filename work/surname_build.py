"""Source-linked surname research; separate from the established family tree."""
from pathlib import Path
from story_revision import asset

def apply(atlas):
    root = Path(__file__).parent
    section = (root/'surname-section.html').read_text('utf8')
    for name in ['surname-polish-excerpt.png', 'surname-ryazan-excerpt.png']:
        section = section.replace('{{'+name+'}}', asset(name))
    return atlas.replace('</body>', section+'</body>')
