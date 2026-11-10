from pathlib import Path
import math,re

ROOT=Path(__file__).resolve().parent

def artwork(private=True):
    branches=[]
    for side in [-1,1]:
        for i in range(9):
            x=round(300+side*(80+120*math.sin(i*math.pi/12)));y=90+i*27
            branches.append(f'<path class="twig" d="M300 365 C{300+side*35} {270+i*5} {x-side*55} {y+45} {x} {y}"/>')
            for j in [0,1,2]:
                ex=x+side*(13+j*6);ey=y-20+j*9
                branches.append(f'<path class="twig" d="M{x} {y} Q{x+side*20} {y+5} {ex} {ey} Q{x} {ey-7} {x} {y}"/>')
            branches.append(f'<circle class="halo" cx="{x}" cy="{y}" r="2"/>')
        for i in range(9):
            branches.append(f'<path class="root" d="M300 355 Q{300+side*(i*9)} 405 {300+side*(35+i*22)} {425+(i%3)*9} l{side*12} 8"/>')
    def med(x,y,name,sub,target):
        link=f'href="#tree" onclick="window.focusPerson(\'{target}\');return false"' if private else 'href="#gate"'
        return f'<a {link} aria-label="{name} — открыть"><ellipse class="medallion" cx="{x}" cy="{y}" rx="62" ry="41"/><ellipse cx="{x}" cy="{y}" rx="57" ry="36" fill="none" stroke="#bb9658" stroke-width=".7"/><text x="{x}" y="{y-1}" font-size="25">{name}</text><text x="{x}" y="{y+16}" font-size="10" letter-spacing="1">{sub}</text></a>'
    return '<svg class="heritage-art" viewBox="0 0 600 460" role="img" aria-label="Декоративное древо памяти. Медальоны Макара и Корнея открывают семейные карточки."><defs><linearGradient id="heritage-gold" x1="0" y1="1" x2="1" y2="0"><stop stop-color="#8f632e"/><stop offset=".5" stop-color="#f3d797"/><stop offset="1" stop-color="#b9924d"/></linearGradient></defs>'+''.join(branches)+'<path class="twig" style="stroke-width:4" d="M300 385Q280 280 300 70"/><circle cx="300" cy="70" r="27" fill="none" stroke="#d3ab61"/><circle cx="300" cy="70" r="21" fill="none" stroke="#d3ab61"/><text x="300" y="80" font-size="29">М</text>'+med(300,185,'Макар','ИСТОКИ РОДА','full-B9')+med(300,300,'Корней','ЛИНИЯ ПОТОМКОВ','full-D10')+'<text x="300" y="458" font-size="10" letter-spacing="2">ПАМЯТЬ • РОДСТВО • ПРОДОЛЖЕНИЕ</text></svg>'

def cover(private=True):
    body='<span class="heritage-overline">Летопись ведётся с 1700 года · 1700–2026</span><h2>Фамильная летопись<br><em>Маршалкиных</em></h2><p>Первый датированный документ — запись 1700 года о Макаре Маршалкине и его сыновьях в Обояни. История семьи прослежена до 2026 года.</p>'
    actions='<a href="#origins">Читать историю рода ↓</a><a href="#tree">Открыть всё древо ↗</a>' if private else '<a href="#world-war">Военная глава ↓</a><a href="#gate">Доступ к семейному древу</a>'
    ornament=''.join('<svg class="heritage-corner c'+str(i)+'" viewBox="0 0 100 100" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="1"><path d="M4 96V4h92M11 78Q12 13 78 11M12 58Q45 50 38 25Q30 5 21 20Q17 30 27 29M58 12Q50 45 25 38Q5 30 20 21M17 65Q25 45 45 45Q45 25 65 17"/><path d="M12 80Q5 60 20 53Q28 70 12 80M80 12Q60 5 53 20Q70 28 80 12M25 49Q14 38 17 32Q31 35 25 49M49 25Q38 14 32 17Q35 31 49 25"/></g></svg>' for i in range(1,5))
    return '<div class="heritage-cover">'+ornament+'<div class="heritage-copy">'+body+'<div class="heritage-actions">'+actions+'</div></div>'+artwork(private)+'</div>'

def apply_private(atlas):
    # Last style wins over legacy section styles while keeping data/geometry intact.
    atlas=atlas.replace('</body>','<style id="heritage-theme">'+(ROOT/'heritage.css').read_text('utf8')+'</style></body>')
    atlas=atlas.replace('<nav class="folioNav"',cover()+'<nav class="folioNav"',1)
    atlas=atlas.replace('<div class="chapter atlasTree">',(ROOT/'homelands.html').read_text('utf8')+(ROOT/'southward.html').read_text('utf8')+'<div class="chapter atlasTree">',1)
    atlas=atlas.replace('<a href="#origins">Истоки рода</a>','<a href="#origins">Истоки рода</a><a href="#homelands">Родовые места</a><a href="#southward">На юг</a>',1)
    house='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2 11L12 2l10 9M5 9v12h14V9M10 21v-7h4v7" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>'
    evidence='<div class="village-evidence"><div class="village-number"><strong>22</strong><span>двора · 1649 год</span><div class="village-houses" aria-label="22 пиктограммы, каждая обозначает один двор">'+house*22+'</div></div><div><h3>Бегичево</h3><p>Раннее название Бегичева — Вышняя Рыбница. Роспись 1649 года описывает поселение детей боярских на Рыбнице под Ровным лесом. В нём было 22 двора. Издатели документа отождествляют его с современным Бегичевом; в росписи 1651 года оно названо Переверзевой.</p><p>Это число хозяйств, а не жителей и не семей Маршалкиных. Оно даёт представление о масштабе раннего поселения. Его планировка и расположение отдельных домов пока неизвестны.</p><a href="https://www.old-kursk.ru/book/babin/190127.html" target="_blank" rel="noopener">Бабин, Озеров · публикация росписи, лист 473 ↗</a> · <a href="https://proza.ru/2025/04/07/878" target="_blank" rel="noopener">Фёдор Сергеев · краеведческая справка, присланная семьёй ↗</a></div></div>'
    atlas=atlas.replace('<span class="source-label">Западные исследования и свидетельство путешественника</span>',evidence+'<span class="source-label">Западные исследования и свидетельство путешественника</span>')
    atlas=atlas.replace('</body>',(ROOT/'chapters-menu.html').read_text('utf8')+'</body>')
    return atlas

def apply_public(public):
    fonts=(ROOT/'fontbundle.css').read_text('utf8')
    css=(ROOT/'heritage.css').read_text('utf8')
    css+=':root{--serif: Cormorant Garamond,Georgia,serif;--sans:Manrope,Arial,sans-serif}header{background:#2d2016;color:#f1dfbd;padding:25px max(5vw,calc((100vw - 1060px)/2))}header h1{font-family:var(--serif);font-size:clamp(30px,4vw,48px)}header a{color:#e7c58a}body{font-family:var(--sans)}h2,h3,h4{font-family:var(--serif)}button,input{font-family:var(--sans)}header button{background:#d8b778;color:#2d1e10}footer{background:#2c2016;color:#e5cfa8}.ww-k,.ww-marker,.pn>span{font-family:var(--sans)}'
    public=public.replace('<header>',cover(False)+'<header>',1)
    return public.replace('</html>','<style id="heritage-theme">'+fonts+css+'</style></html>')

