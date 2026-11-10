from pathlib import Path
from story_revision import asset
ROOT=Path(__file__).parent
def apply(atlas):
    scenes=[]
    html='<div id="reading-progress" aria-hidden="true"></div><template id="editorial-scenes">'
    for target,num,kicker,title,body,img,caption in scenes:
        html+=f'<section class="editorial-scene scene-{num}" data-before="{target}" aria-label="{kicker}"><div class="scene-media"><img class="parallax-image" data-source="{img}" alt="{caption}" loading="lazy"></div><div class="scene-shade"></div><div class="scene-copy"><span class="scene-kicker">{num} / {kicker}</span><h2>{title}</h2><p>{body}</p><a href="#{target}">Продолжить чтение <span aria-hidden="true">↓</span></a></div><small class="scene-caption">{caption}</small><span class="scene-number" aria-hidden="true">{num}</span></section>'
    html+='</template><style>'+ (ROOT/'editorial-fonts.css').read_text('utf8')+(ROOT/'editorial.css').read_text('utf8')+'</style><script>'+(ROOT/'editorial.js').read_text('utf8')+'</script>'
    return '\n'.join(line.rstrip() for line in atlas.replace('</body>',html+'</body>').splitlines())+'\n'
