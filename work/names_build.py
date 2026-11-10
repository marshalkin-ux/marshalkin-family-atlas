import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
AMBIGUOUS = {'L33', 'N61', 'N75', 'N125', 'R161', 'N474', 'J479', 'H503', 'J571', 'P292', 'X361'}
SURNAMES = set('Корнилова Куцова Селютин Шестопалов Казанцева Данилов Солгалов Маршалкин Емельянова Давыденко Лактионов Ефремов Лимаренко Проймин Панкова Алексеева Сивцева Хохулина Кузнецова Шарошкина Крикунова Сальник Митина Колесников Пеньзева Уварова Пеньзев Полекарпова Ворошилов Пьянова Меленина Бойко Поляшенко Будилов Манюхина Ярошенко Иноземцева Мисько Артовский Калинина Семыкина Панков Еремин Быкова Шаталова Ширина'.split())

def name_of(person):
    if person['placeholder'] or person['cell'] in AMBIGUOUS:
        return None
    name = re.sub(r'\([^)]*\)', '', person['name'])
    name = re.sub(r'\b(?:ж|от)\.', ' ', name)
    name = name.replace('приемный', '').replace('2я', '').replace('ж.Афанасьева', '')
    words = re.findall(r'[А-Яа-яЁёIiі]+', name)
    words = [w.replace('i', 'и').replace('і', 'и').replace('ё', 'е').rstrip('ъ') for w in words]
    words = [w for w in words if w not in SURNAMES and w != 'Афанасьева' and not re.fullmatch('[ХхXx]+', w)]
    return words[0] if words else None

def section():
    people = json.loads((ROOT / 'fullPeople.json').read_text('utf8'))
    records = [{**{k: p[k] for k in ('id', 'cell', 'name', 'sex', 'year', 'gen', 'faint', 'parents')}, 'given': name_of(p)} for p in people]
    (ROOT / 'names-audit.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), 'utf8')
    template = (ROOT / 'names-section.html').read_text('utf8')
    return template.replace('NAMES_RECORDS', json.dumps(records, ensure_ascii=False).replace('</', '<\\/'))

if __name__ == '__main__':
    section()
