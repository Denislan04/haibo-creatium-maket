from pathlib import Path
from bs4 import BeautifulSoup
import csv,json
root=Path(__file__).parent
rows=list(csv.DictReader((root/'HaiboProducts_v2.csv').open(encoding='utf-8-sig',newline='')))
for row in rows:
 if row.get('product_type')=='motor':
  card=root/'медиа/моторы-карточки'/(row['id']+'.png')
  if card.exists():row['image_url']='медиа/моторы-карточки/'+card.name
manifest={r['name']:r for r in csv.DictReader((root/'ВСТРАИВАНИЯ.csv').open(encoding='utf-8-sig',newline=''))}
images={'hero_photo':'hero_bg_image.jpg','install_pvc_image':'install_image_1.jpg','install_boat_image':'install_image_2.jpg','cta_photo':'cta_bg_image.jpg'}
video={'hero_video':'ad.mp4','gps_video':'gps.mp4'}
parts=[]
for p in sorted((root/'блоки').glob('*.html')):
 soup=BeautifulSoup(p.read_text(),'html.parser')
 for e in soup.find_all('cr-embed'):
  name=e.get('name');item=manifest[name];kind=item['type']
  if kind=='Редактируемый текст':e.string=item['initial_text_or_action']
  elif kind=='Загружаемая картинка':
   if name in images:
    e['style']='background-image:url("медиа/'+images[name]+'")'
   else:
    article=e.find_parent('article')
    photo=article.find('img')
    local=root/'медиа/моторы-карточки'/(article['data-id']+'.png')
    src='медиа/моторы-карточки/'+local.name if local.exists() else photo['src']
    photo['src']=src
    e['style']='background-image:url("'+src+'")'
  elif name in video:
   tag=soup.new_tag('video',src='медиа/'+video[name],poster='' if name=='hero_video' else None)
   tag['autoplay']='';tag['muted']='';tag['loop']='';tag['playsinline']='';tag['controls']=''
   tag['style']='width:100%;height:100%;object-fit:cover;display:block'
   e.append(tag)
  else:
   a=soup.new_tag('a',href='tel:88005053995');a['class']='hb-button hb-button--lime';a.string='Связаться с дилером';e.append(a)
 parts.append(str(soup))
css='\n'.join(p.read_text() for p in sorted((root/'блоки').glob('*.css')))
cat=(root/'блоки/04_catalog.js').read_text()
combo=(root/'блоки/07_combo.js').read_text()
json_rows=json.dumps(rows,ensure_ascii=False).replace('</','<\\/')
html='''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>HAIBO iPenguin — макет для Creatium</title><style>'''+css+'''</style></head><body style="margin:0">'''+''.join(parts)+'''<script>
function hbPreviewScreen(){var w=window.innerWidth,b=document.body;b.classList.remove('screen-md','screen-sm','screen-xs');if(w<=480)b.classList.add('screen-xs');else if(w<=760)b.classList.add('screen-sm');else if(w<=1180)b.classList.add('screen-md')}
window.addEventListener('resize',hbPreviewScreen);hbPreviewScreen();
(function(){var el=document.querySelector('#hb-catalog').parentElement;'''+cat+'''})();(function(){var el=document.querySelector('#hb-combo').parentElement;var data={rows:'''+json_rows+'''};var params={combo_discount:0};'''+combo+'''})();</script></body></html>'''
(root/'ПРЕДПРОСМОТР.html').write_text(html)
catalog_part=next(part for part in parts if 'id="hb-catalog"' in part)
catalog_preview='''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Каталог HAIBO — предпросмотр</title><style>'''+(root/'блоки/04_catalog.css').read_text()+'''</style></head><body style="margin:0">'''+catalog_part+'''<script>var el=document.body;'''+cat+'''</script></body></html>'''
(root/'ПРЕДПРОСМОТР_КАТАЛОГА.html').write_text(catalog_preview)
print('preview bytes',len(html))
