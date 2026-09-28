from pathlib import Path
from bs4 import BeautifulSoup

root = Path(__file__).parent
values = {}
for line in (root / 'ВСТАВКА.md').read_text().splitlines():
    if line.startswith('| `tech_scroll_'):
        cells = [cell.strip() for cell in line.strip('|').split('|')]
        values[cells[0].strip('`')] = cells[1]

soup = BeautifulSoup((root / 'HTML.html').read_text(), 'html.parser')
for embed in soup.find_all('cr-embed'):
    embed.replace_with(values[embed['name']])
video = soup.find('video')
video['src'] = '../медиа/scroll_3d_motor.mp4'

html = ('<!doctype html><html lang="ru"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>HAIBO — 3D-мотор при прокрутке</title><style>body{margin:0}'
        + (root / 'CSS.css').read_text() + '</style></head><body>'
        + str(soup) + '<script>' + (root / 'JS.js').read_text()
        + '</script></body></html>')
(root / 'ПРЕДПРОСМОТР.html').write_text(html)
print('preview bytes', len(html))
