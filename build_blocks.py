from pathlib import Path
import csv, html

ROOT = Path(__file__).parent
OUT = ROOT / 'блоки'
OUT.mkdir(exist_ok=True)
embeds = []

def E(name, value):
    embeds.append((name, 'Редактируемый текст', value))
    return f'<cr-embed name="{name}"></cr-embed>'

def I(name, note):
    embeds.append((name, 'Загружаемая картинка', note))
    return f'<cr-embed name="{name}"></cr-embed>'

def C(name, note, side='dark'):
    embeds.append((name, 'Контейнер для компонентов', note))
    return f'<cr-embed name="{name}" colorside="{side}"></cr-embed>'

def save(name, content):
    (OUT / name).write_text(content.strip() + '\n')

save('00_header.html', f'''
<div class="hb-page hb-head" id="hb-top">
  <div class="hb-topline"><div class="hb-wrap"><span class="hb-stock">{E('top_status','Склад в РФ · Отгрузка за 24 ч')}</span><span>{E('top_dealer','Официальный дилер HAIBO · ООО «САНМАКС»')}</span></div></div>
  <header class="hb-header"><div class="hb-wrap hb-header__inner">
    <a class="hb-logo" href="#hb-top">HAIBO<span>.</span><small>{E('head_subtitle','Официальный дилер в России')}</small></a>
    <nav class="hb-nav" aria-label="Основная навигация"><a href="#hb-compare">Преимущества</a><a href="#hb-tech">Технология</a><a href="#hb-catalog">Каталог</a><a href="#hb-install">Установка</a><a href="#hb-warranty">Гарантия</a></nav>
    <details class="hb-menu"><summary>Меню ☰</summary><nav aria-label="Мобильная навигация"><a href="#hb-compare">Преимущества</a><a href="#hb-tech">Технология</a><a href="#hb-catalog">Каталог</a><a href="#hb-gps">GPS-якорь</a><a href="#hb-install">Установка</a><a href="#hb-combo">Комплект</a><a href="#hb-warranty">Гарантия</a><a href="#hb-faq">Вопросы</a></nav></details>
    <a class="hb-button hb-button--lime hb-header__cta" href="#hb-contacts">{E('head_cta','Подобрать мотор')}</a>
  </div></header>
</div>''')

save('01_hero.html', f'''
<section class="hb-page hb-hero" id="hb-hero">
  <div class="hb-hero__photo">{I('hero_photo','Загрузить hero_bg_image.jpg из папки медиа')}</div><div class="hb-hero__shade"></div>
  <div class="hb-wrap hb-hero__inner"><div class="hb-hero__copy">
    <div class="hb-eyebrow hb-eyebrow--light">{E('hero_badge','Линейка HAIBO iPenguin 2025/2026')}</div>
    <h1>{E('hero_title','HAIBO iPenguin. Держит точку.')}<br><em>{E('hero_title_accent','Вы ловите.')}</em></h1>
    <p class="hb-lead">{E('hero_lead','Лодочный электромотор с электронным GPS-якорем удерживает лодку с точностью до 1 метра. Вы выбираете точку с пульта — мотор берёт управление на себя.')}</p>
    <div class="hb-actions"><a class="hb-button hb-button--lime" href="#hb-catalog">{E('hero_catalog','Смотреть моторы')}</a><a class="hb-button hb-button--outline" href="#hb-combo">{E('hero_combo','Собрать комплект')}</a></div>
    <ul class="hb-hero__facts"><li>{E('hero_fact_1','Официальный дилер в России')}</li><li>{E('hero_fact_2','Гарантия 2 года')}</li><li>{E('hero_fact_3','Сервисный центр в РФ')}</li></ul>
  </div><div class="hb-hero__media"><div class="hb-media-slot">{C('hero_video','Перетащить штатное видео Creatium или загрузить рекламный ролик')}</div><div class="hb-media-caption"><strong>{E('hero_video_title','HAIBO iPenguin в работе')}</strong><span>{E('hero_video_meta','12 / 24 / 36 В · Для лодок до 7,5 м')}</span></div></div></div>
</section>''')

bad = [
('Тяжёлый якорь и мокрая верёвка','Каждая перестановка точки отнимает время и силы.'),
('Снос ветром и течением','Лодка уходит с выбранной позиции, приходится вставать заново.'),
('Меньше времени на ловлю','Вместо рыбалки приходится контролировать положение лодки.')]
good = [
('Удержание с пульта','Выберите точку — мотор автоматически подруливает.'),
('Точный контроль','GPS, ГЛОНАСС и BeiDou помогают держать позицию.'),
('Руки свободны','Вы сосредоточены на рыбалке, а не на якоре.')]
def compare_list(items, prefix):
    return ''.join(f'<li><b>{E(prefix+"_title_"+str(i), t)}</b><span>{E(prefix+"_text_"+str(i), d)}</span></li>' for i,(t,d) in enumerate(items,1))
save('02_comparison.html', f'''
<section class="hb-page hb-section hb-section--warm" id="hb-compare"><div class="hb-wrap">
  <div class="hb-eyebrow">{E('compare_kicker','Решение на воде')}</div><h2>{E('compare_title','От верёвочного якоря — к точному удержанию')}</h2><p class="hb-intro">{E('compare_intro','Сравните, как меняется день на рыбалке с электромотором HAIBO iPenguin.')}</p>
  <div class="hb-compare"><div class="hb-compare__old"><h3>{E('compare_old','Обычный якорь')}</h3><ul>{compare_list(bad,'compare_bad')}</ul></div><div class="hb-compare__new"><h3>{E('compare_new','HAIBO iPenguin')}</h3><ul>{compare_list(good,'compare_good')}</ul></div></div>
</div></section>''')

tech = [
('Электронный GPS-якорь','Удерживает лодку в выбранной точке.'),
('Беспроводной пульт','Скорость, курс и точка удержания под рукой.'),
('Носовое крепление','Корма остаётся свободной для основного мотора.'),
('Три напряжения','Модели на 12, 24 и 36 В под разные лодки.'),
('Штанга и винт','Подбор длины штанги под высоту носа.')]
tech_cards=''.join(f'<article class="hb-tech-card"><span>{i:02d}</span><h3>{E(f"tech_title_{i}",t)}</h3><p>{E(f"tech_text_{i}",d)}</p></article>' for i,(t,d) in enumerate(tech,1))
save('03_technology.html',f'''
<section class="hb-page hb-section hb-section--white" id="hb-tech"><div class="hb-wrap"><div class="hb-eyebrow">{E('tech_kicker','Технология iPenguin')}</div><h2>{E('tech_title','Пять узлов, которые меняют рыбалку')}</h2><p class="hb-intro">{E('tech_intro','Носовой мотор берёт управление лодкой на себя, пока вы выбираете следующую точку.')}</p><div class="hb-tech-grid">{tech_cards}</div></div></section>''')

save('04_catalog.html',f'''
<section class="hb-page hb-section hb-section--white hb-catalog" id="hb-catalog"><div class="hb-wrap"><div class="hb-eyebrow">{E('cat_kicker','Каталог HAIBO')}</div><h2>{E('cat_title','Моторы и оригинальное оборудование')}</h2><p class="hb-intro">{E('cat_intro','Выберите мотор и совместимое оборудование. Цены и карточки обновляются из таблицы HaiboProducts.')}</p>
  <div class="hb-tabs" role="tablist" aria-label="Товары"><button type="button" class="is-active" data-filter="all">Все товары</button><button type="button" data-filter="motor">Моторы</button><button type="button" data-filter="12">12 В</button><button type="button" data-filter="24">24 В</button><button type="button" data-filter="36">36 В</button><button type="button" data-filter="accessory">Аксессуары</button></div>
  <p class="hb-catalog__status" aria-live="polite"></p><div class="hb-products" aria-live="polite"></div><div class="hb-catalog__form">{C('cat_form','Штатная кнопка Creatium с формой подбора', 'light')}</div>
</div></section>''')

save('05_gps.html',f'''
<section class="hb-page hb-section hb-section--pine" id="hb-gps"><div class="hb-wrap hb-split"><div><div class="hb-eyebrow hb-eyebrow--light">{E('gps_kicker','GPS-якорь на воде')}</div><h2>{E('gps_title','Лодка остаётся в выбранной точке')}</h2><p class="hb-intro">{E('gps_intro','Мотор считывает сигналы спутников и подруливает винтом, компенсируя ветер и течение.')}</p><ul class="hb-feature-list"><li><strong>{E('gps_feature_1','Удержание позиции')}</strong><span>{E('gps_feature_text_1','Точка задаётся с беспроводного пульта.')}</span></li><li><strong>{E('gps_feature_2','Контроль курса')}</strong><span>{E('gps_feature_text_2','Встроенный компас помогает держать направление.')}</span></li><li><strong>{E('gps_feature_3','Смещение Jog')}</strong><span>{E('gps_feature_text_3','Переход на соседнюю точку без подъёма якоря.')}</span></li></ul></div><div><div class="hb-video-slot">{C('gps_video','Перетащить штатное видео Creatium с демонстрацией GPS-якоря')}</div><p class="hb-video-note">{E('gps_caption','Полевые испытания HAIBO на воде')}</p></div></div></section>''')

save('06_installation.html',f'''
<section class="hb-page hb-section hb-section--warm" id="hb-install"><div class="hb-wrap"><div class="hb-eyebrow">{E('install_kicker','Установка')}</div><h2>{E('install_title','Для ПВХ-лодок и жёстких катеров')}</h2><p class="hb-intro">{E('install_intro','Подберите площадку и длину штанги под высоту носа вашего судна.')}</p><div class="hb-install-grid"><article><div class="hb-install-image">{I('install_pvc_image','Загрузить install_image_1.jpg')}</div><h3>{E('install_pvc_title','Монтаж на ПВХ-лодку')}</h3><p>{E('install_pvc_text','Носовая площадка формирует прочное основание для установки мотора.')}</p></article><article><div class="hb-install-image">{I('install_boat_image','Загрузить install_image_2.jpg')}</div><h3>{E('install_boat_title','Монтаж на катер')}</h3><p>{E('install_boat_text','Быстросъёмная площадка помогает снять мотор после выхода на воду.')}</p></article></div></div></section>''')

save('07_combo.html',f'''
<section class="hb-page hb-section hb-section--white" id="hb-combo"><div class="hb-wrap"><div class="hb-eyebrow">{E('combo_kicker','Подбор комплекта')}</div><h2>{E('combo_title','Соберите комплект под свою лодку')}</h2><p class="hb-intro">{E('combo_intro','Мотор, аккумулятор и монтаж из текущего каталога. Калькулятор покажет сумму и отсеет несовместимые позиции.')}</p><div class="hb-combo-panel"><div class="hb-combo-fields"><label>1. Электромотор<select data-combo="motor"></select></label><label>2. Аккумулятор<select data-combo="battery"></select></label><label>3. Монтаж и защита<select data-combo="accessory"></select></label></div><div class="hb-combo-result"><div><span>Стоимость комплекта</span><strong data-combo="total">—</strong><p data-combo="note"></p></div><div class="hb-combo-form">{C('combo_form','Штатная кнопка Creatium с формой заказа комплекта')}</div></div></div></div></section>''')

steps=[('Длина и масса лодки','Проверьте предельную длину судна в карточке конкретной модели.'),('Напряжение питания','P-001 — 12 В, P-002 — 24 В, P-003 — 36 В.'),('Высота носа','Выберите штангу 54, 60 или 72 дюйма под посадку мотора.')]
steps_html=''.join(f'<article><span>0{i}</span><h3>{E(f"step_title_{i}",t)}</h3><p>{E(f"step_text_{i}",d)}</p></article>' for i,(t,d) in enumerate(steps,1))
save('08_steps.html',f'''
<section class="hb-page hb-section hb-section--warm" id="hb-steps"><div class="hb-wrap"><div class="hb-eyebrow">{E('steps_kicker','Простой выбор')}</div><h2>{E('steps_title','Как выбрать мотор за три шага')}</h2><div class="hb-steps">{steps_html}</div></div></section>''')

save('09_warranty.html',f'''
<section class="hb-page hb-section hb-section--pine" id="hb-warranty"><div class="hb-wrap hb-split"><div><div class="hb-eyebrow hb-eyebrow--light">{E('war_kicker','Официальный дилер')}</div><h2>{E('war_title','Гарантия 2 года и сервис в России')}</h2><p class="hb-intro">{E('war_intro','ООО «САНМАКС» помогает подобрать мотор, организует поставку и сервисное обслуживание.')}</p><a class="hb-button hb-button--lime" href="tel:88005053995">{E('war_phone','8 800 505-39-95')}</a></div><div class="hb-warranty-info"><div><strong>{E('war_fact_1','2 года')}</strong><span>{E('war_text_1','Гарантия со дня продажи')}</span></div><div><strong>{E('war_fact_2','Россия')}</strong><span>{E('war_text_2','Сервис и поддержка дилера')}</span></div><div><strong>{E('war_fact_3','HAIBO')}</strong><span>{E('war_text_3','Оригинальное оборудование')}</span></div></div></div></section>''')

faq=[('Чем отличаются 12, 24 и 36 В?','Это серии P-001, P-002 и P-003. Аккумулятор должен соответствовать напряжению мотора.'),('Что такое электронный якорь?','Мотор удерживает лодку в выбранной точке с помощью GPS, ГЛОНАСС и BeiDou.'),('Подойдёт ли мотор для ПВХ?','Да, для ПВХ-лодок есть носовая площадка. Совместимость конкретного крепежа проверяйте по карточке.'),('Какой нужен аккумулятор?','Для P-001 нужен 12 В, для P-002 — 24 В. В текущем каталоге нет 36-вольтового аккумулятора для P-003.'),('Что входит в комплект?','Состав различается по модели. Точный перечень смотрите в карточке товара.'),('Какая гарантия?','На моторы заявлена гарантия 2 года со дня продажи при личном использовании.')]
faq_html=''.join(f'<details><summary>{E(f"faq_q_{i}",q)}</summary><p>{E(f"faq_a_{i}",a)}</p></details>' for i,(q,a) in enumerate(faq,1))
save('10_faq.html',f'''
<section class="hb-page hb-section hb-section--white" id="hb-faq"><div class="hb-wrap"><div class="hb-eyebrow">{E('faq_kicker','Вопросы')}</div><h2>{E('faq_title','Коротко и по делу')}</h2><div class="hb-faq">{faq_html}</div></div></section>''')

save('11_cta.html',f'''
<section class="hb-page hb-section hb-section--cta" id="hb-contacts"><div class="hb-cta-photo">{I('cta_photo','Загрузить cta_bg_image.jpg')}</div><div class="hb-wrap hb-split hb-cta-content"><div><div class="hb-eyebrow hb-eyebrow--light">{E('cta_kicker','Поможем выбрать')}</div><h2>{E('cta_title','Расскажите о лодке — подберём мотор')}</h2><p class="hb-intro">{E('cta_intro','Напишите длину лодки и высоту носа. Подскажем модель, штангу, аккумулятор и крепёж.')}</p><a class="hb-cta-phone" href="tel:88005053995">{E('cta_phone','8 800 505-39-95')}</a></div><div class="hb-cta-card"><h3>{E('cta_form_title','Заявка на подбор')}</h3><p>{E('cta_form_text','Оставьте номер телефона — специалист свяжется с вами.')}</p>{C('cta_form','Перетащить штатную форму Creatium, поля: имя, телефон, лодка')}</div></div></section>''')

save('12_footer.html',f'''
<footer class="hb-page hb-footer" id="hb-footer"><div class="hb-wrap hb-footer__grid"><div><a class="hb-logo" href="#hb-top">HAIBO<span>.</span></a><p>{E('foot_about','Официальный дилер лодочных электромоторов в России.')}</p></div><div><h3>{E('foot_nav_title','Разделы')}</h3><a href="#hb-catalog">Каталог</a><a href="#hb-install">Установка</a><a href="#hb-warranty">Гарантия</a><a href="#hb-faq">Вопросы</a></div><div><h3>{E('foot_contact_title','Связаться')}</h3><a href="tel:88005053995">{E('foot_phone','8 800 505-39-95')}</a><p>{E('foot_company','ООО «САНМАКС»')}</p></div></div><div class="hb-wrap hb-footer__bottom">{E('foot_note','© HAIBO. Официальный дилер в России.')}</div></footer>''')

def block_for(name):
    prefix=name.split('_')[0]
    return {'top':'00_header','head':'00_header','hero':'01_hero','compare':'02_comparison',
            'tech':'03_technology','cat':'04_catalog','gps':'05_gps','install':'06_installation',
            'combo':'07_combo','step':'08_steps','steps':'08_steps','war':'09_warranty',
            'faq':'10_faq','cta':'11_cta','foot':'12_footer'}[prefix]

with (ROOT/'ВСТРАИВАНИЯ.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['block','name','type','initial_text_or_action'])
    w.writerows((block_for(name),name,kind,value) for name,kind,value in embeds)

lines=['# Поля для вкладки «Встраивания»','',
       'В каждом HTML-компоненте создайте поля только из его раздела. Имя копируйте точно.',
       'Для типа «Редактируемый текст» после сохранения кликните по месту на странице и введите значение из последней колонки.',
       'Картинки загружаются по клику; в контейнеры перетаскиваются штатные компоненты Creatium.','']
for block in sorted({block_for(name) for name,_,_ in embeds}):
    lines += ['## '+block,'','| Имя | Тип | Текст или действие |','| --- | --- | --- |']
    for name,kind,value in embeds:
        if block_for(name)==block:
            lines.append('| `'+name+'` | '+kind+' | '+value.replace('|','\\|')+' |')
    lines.append('')
(ROOT/'ВСТРАИВАНИЯ.md').write_text('\n'.join(lines))
print('blocks',len(list(OUT.glob('*.html'))),'embeds',len(embeds))
