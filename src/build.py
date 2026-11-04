#!/usr/bin/env python3
"""Сборка сайта М МЕБЕЛЬ.
Запуск: python3 src/build.py  ->  обновляет HTML-файлы в папке docs/
Все тексты, контакты и модели правятся здесь и в src/products.txt
"""
import json, html, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'docs')
VER = '3'

# ================= КОНТАКТЫ =================
WA = '79288204184'
WA_TXT = '+7 (928) 820-41-84'
SHOPS = [
    dict(name='Михайловское шоссе, 14', city='Ставрополь', phone='8 (968) 266-12-93', tel='+79682661293'),
    dict(name='ул. Доваторцев, 74', city='Ставрополь', phone='8 (928) 820-41-84', tel='+79288204184', wa=True),
]
B2B_FURN = dict(person='Рудольф', phone='+7 (928) 321-17-46', tel='+79283211746')
B2B_DOWN = dict(person='Радислав', phone='8 (928) 329-05-53', tel='+79283290553')
TG = 'https://t.me/mmebel_m'
IG = 'https://instagram.com/mmebel_m'
PIN = 'https://pinterest.com/mmebel_m'
CITIES = ['Анапа','Астрахань','Армавир','Баксан','Благодарный','Владикавказ','Геленджик','Георгиевск','Грозный',
 'Донское','Ингушетия','Ипатово','Кисловодск','Красногвардейское','Краснодар','Курганинск','Лечинкай','Миллерово',
 'Михайловск','Москва','Нальчик','Невинномысск','Нефтекумск','Новоалександровск','Новопавловск','Отрадное',
 'Прохладный','Пятигорск','Ростов-на-Дону','Светлоград','Ставрополь','Сургут','Усть-Джегута','Черкесск']
NEW_CITIES = ['Донецк','Луганск','Симферополь','Севастополь']

def wa(text=''):
    from urllib.parse import quote
    return f'https://wa.me/{WA}' + (f'?text={quote(text)}' if text else '')

def map_url(addr):
    from urllib.parse import quote
    return f'https://yandex.ru/map-widget/v1/?text={quote(addr)}&z=16'

def map_link(addr):
    from urllib.parse import quote
    return f'https://yandex.ru/maps/?text={quote(addr)}'

# ================= ИКОНКИ =================
I = {
 'wa':'<svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.4-.5c.2-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.2-.3-.3-.6-.4zM12 2C6.5 2 2 6.5 2 12c0 1.8.5 3.5 1.3 4.9L2 22l5.2-1.4c1.4.8 3.1 1.2 4.8 1.2 5.5 0 10-4.5 10-10S17.5 2 12 2zm0 18.2c-1.6 0-3.1-.4-4.4-1.2l-.3-.2-3.1.8.8-3-.2-.3C4 15.1 3.6 13.6 3.6 12c0-4.6 3.8-8.4 8.4-8.4s8.4 3.8 8.4 8.4-3.8 8.2-8.4 8.2z"/></svg>',
 'tg':'<svg viewBox="0 0 24 24" fill="currentColor"><path d="M21.9 4.6 18.7 19.7c-.2 1.1-.9 1.3-1.8.8l-4.9-3.6-2.4 2.3c-.3.3-.5.5-1 .5l.4-5 9.1-8.2c.4-.4-.1-.6-.6-.2L6.3 13.4l-4.8-1.5c-1-.3-1.1-1 .2-1.5L20.5 3.2c.9-.3 1.6.2 1.4 1.4z"/></svg>',
 'ig':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>',
 'pin':'<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-3.6 19.3c-.1-.8-.2-2 0-2.9l1.2-5s-.3-.6-.3-1.5c0-1.4.8-2.4 1.8-2.4.9 0 1.3.6 1.3 1.4 0 .9-.5 2.1-.8 3.3-.2 1 .5 1.8 1.5 1.8 1.8 0 3.1-1.9 3.1-4.6 0-2.4-1.7-4.1-4.2-4.1-2.9 0-4.5 2.1-4.5 4.4 0 .9.3 1.8.8 2.3.1.1.1.2.1.3l-.3 1.2c0 .2-.2.3-.4.2-1.3-.6-2.1-2.5-2.1-4 0-3.3 2.4-6.3 6.9-6.3 3.6 0 6.4 2.6 6.4 6 0 3.6-2.3 6.5-5.4 6.5-1.1 0-2.1-.6-2.4-1.2l-.7 2.5c-.2.9-.9 2.1-1.3 2.8A10 10 0 1 0 12 2z"/></svg>',
 'ph':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>',
 'arr':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 'pin2':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
 'x':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 6l12 12M18 6 6 18"/></svg>',
 'l':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 6l-6 6 6 6"/></svg>',
 'r':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 6l6 6-6 6"/></svg>',
}

# ================= ТОВАРЫ =================
TR = dict(zip('абвгдеёжзийклмнопрстуфхцчшщъыьэюя', ['a','b','v','g','d','e','e','zh','z','i','y','k','l','m','n','o','p','r','s','t','u','f','h','c','ch','sh','sch','','y','','e','yu','ya']))
def slug(s):
    s = s.lower().replace('с креслом', 'kreslo')
    r = ''.join(TR.get(ch, ch if ch.isalnum() else '-') for ch in s)
    while '--' in r: r = r.replace('--', '-')
    return r.strip('-')

TYPES = {'corner': 'угловой диван', 'sofa': 'диван', 'chair': 'кресло', 'pouf': 'пуфы'}
COLL = {'mc': 'M Comfort', 'mm': 'М Мебель'}
PRODUCTS = []
for line in open(os.path.join(ROOT, 'src', 'products.txt'), encoding='utf-8'):
    line = line.strip()
    if not line or line.startswith('#'): continue
    page, coll, typ, name, sizes, mech, mat = line.split('|')
    PRODUCTS.append(dict(id=slug(name), page=int(page), img=f'{int(page):02d}', coll=coll, collName=COLL[coll],
        type=typ, typeName=TYPES[typ], name=name, sizes=sizes.split(';'), mech=mech, mat=mat.split(';')))
MECHS = sorted({p['mech'] for p in PRODUCTS})
P = {p['page']: p for p in PRODUCTS}

def e(s): return html.escape(str(s))

def card(p, rail=False):
    first = p['sizes'][0]
    search = (p['name'] + ' ' + p['typeName'] + ' ' + p['mech'] + ' ' + p['collName']).lower()
    href = f'catalog.html#{p["id"]}'
    tag = 'a' if rail else 'article'
    extra = f' href="{href}"' if rail else ''
    return f'''<{tag} class="card" data-id="{p['id']}" data-coll="{p['coll']}" data-type="{p['type']}" data-mech="{e(p['mech'])}" data-search="{e(search)}"{extra}>
  <div class="card-img"><img src="img/products/{p['img']}.webp" alt="{e(p['typeName'].capitalize())} «{e(p['name'])}» — {e(p['collName'])}" loading="lazy" width="1000" height="676"></div>
  <div class="card-body">
    <div class="card-top"><span class="badge {p['coll']}">{p['collName']}</span><span class="card-type">{p['typeName']}</span></div>
    <h3>{e(p['name'])}</h3>
    <div class="meta">{e(first)}</div>
    <div class="meta muted">Механизм: {e(p['mech'])}</div>
    <div class="price"><b>Цена по запросу</b><span class="more">{I['arr']}</span></div>
  </div>
</{tag}>'''

# ================= ОБЩИЕ ЧАСТИ =================
NAV = [('index.html','Главная'),('catalog.html','Каталог'),('production.html','Производство и пух'),('partners.html','Опт и партнёрам'),('contacts.html','Контакты')]

def head(title, desc, page):
    return f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="img/og.jpg">
<meta property="og:type" content="website">
<meta name="theme-color" content="#2f2827">
<link rel="icon" href="img/brand/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,500&family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css?v={VER}">
</head>
<body data-page="{page}">'''

def header(page, dark=True):
    links = ''.join(f'<a href="{h}"{" class=active" if h==page else ""}>{t}</a>' for h, t in NAV)
    mlinks = ''.join(f'<a class="m-link" href="{h}">{t}</a>' for h, t in NAV)
    return f'''
<header class="header{' is-dark' if dark else ''}">
  <div class="container header-inner">
    <a class="logo" href="index.html" aria-label="М Мебель — на главную">
      <img class="l-dark" src="img/brand/mm-dark.png" alt="М Мебель" width="241" height="273">
      <img class="l-light" src="img/brand/mm-light.png" alt="М Мебель" width="241" height="273">
    </a>
    <nav class="nav">{links}</nav>
    <div class="header-cta">
      <a class="header-phone" href="tel:{SHOPS[1]['tel']}">{SHOPS[1]['phone']}</a>
      <a class="btn btn-wa btn-sm" href="{wa('Здравствуйте! Хочу узнать о мебели М Мебель.')}" target="_blank" rel="noopener">{I['wa']} WhatsApp</a>
      <button class="burger" aria-label="Меню" aria-expanded="false"><span></span><span></span></button>
    </div>
  </div>
</header>
<div class="mobile-menu">
  {mlinks}
  <div class="m-foot">
    <a href="tel:{SHOPS[1]['tel']}">{SHOPS[1]['phone']} — ул. Доваторцев, 74</a>
    <a href="tel:{SHOPS[0]['tel']}">{SHOPS[0]['phone']} — Михайловское ш., 14</a>
    <a class="btn btn-wa" href="{wa()}" target="_blank" rel="noopener">{I['wa']} Написать в WhatsApp</a>
  </div>
</div>'''

def footer():
    return f'''
<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <div class="logos"><img src="img/brand/mm-light.png" alt="М Мебель" width="241" height="273"><img src="img/brand/mc-light.png" alt="M Comfort Collection" width="516" height="222"></div>
        <p>Фабрика мягкой мебели «М Мебель». Ставрополь, с 1998 года. Премиальная линия M Comfort Collection — с 2017 года.</p>
      </div>
      <div>
        <h4>Разделы</h4>
        <ul>{''.join(f'<li><a href="{h}">{t}</a></li>' for h,t in NAV[1:])}</ul>
      </div>
      <div>
        <h4>Магазины</h4>
        <ul>
          {''.join(f'<li>{s["name"]}<br><a href="tel:{s["tel"]}">{s["phone"]}</a></li>' for s in SHOPS)}
        </ul>
      </div>
      <div>
        <h4>Связь</h4>
        <ul>
          <li><a href="{wa()}" target="_blank" rel="noopener">WhatsApp {WA_TXT}</a></li>
          <li><a href="{TG}" target="_blank" rel="noopener">Telegram</a></li>
          <li><a href="{IG}" target="_blank" rel="noopener">Instagram</a></li>
          <li><a href="{PIN}" target="_blank" rel="noopener">Pinterest</a></li>
          <li>Мебель оптом: <a href="tel:{B2B_FURN['tel']}">{B2B_FURN['phone']}</a></li>
          <li>Пух оптом: <a href="tel:{B2B_DOWN['tel']}">{B2B_DOWN['phone']}</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 1998–<span id="y">2026</span> «М Мебель». Цены на мебель — по запросу. Информация на сайте не является публичной офертой.</span>
      <span>Ставрополь</span>
    </div>
  </div>
</footer>
<a class="fab" href="{wa('Здравствуйте! Хочу узнать о мебели М Мебель.')}" target="_blank" rel="noopener" aria-label="Написать в WhatsApp">{I['wa']}</a>
<script>document.getElementById('y').textContent=new Date().getFullYear()</script>'''

def end(extra=''):
    return f'''{extra}
<script src="js/main.js?v={VER}"></script>
</body>
</html>'''

def page_hero(crumb, eyebrow, title, lead):
    return f'''
<section class="page-hero">
  <div class="container">
    <div class="crumbs"><a href="index.html">Главная</a> / {crumb}</div>
    <span class="eyebrow">{eyebrow}</span>
    <h1>{title}</h1>
    <p class="lead">{lead}</p>
  </div>
</section>'''

def cta_band():
    return f'''
<section class="cta-band section">
  <div class="container cta-inner rv">
    <div>
      <span class="eyebrow">Цена по запросу</span>
      <h2 style="margin-top:14px">Подберём модель, ткань и цвет — и назовём точную цену</h2>
    </div>
    <div class="hero-actions">
      <a class="btn btn-wa" href="{wa('Здравствуйте! Помогите подобрать диван.')}" target="_blank" rel="noopener">{I['wa']} Написать в WhatsApp</a>
      <a class="btn btn-outline" href="catalog.html">Открыть каталог</a>
    </div>
  </div>
</section>'''

def social_block():
    return f'''
<section class="social section">
  <div class="container">
    <div class="social-card rv">
      <div style="position:relative;z-index:1">
        <span class="eyebrow" style="color:var(--taupe-2)">Мы на связи каждый день</span>
        <h2 style="margin:16px 0 18px">Больше видео, фото и новинок — в наших соцсетях</h2>
        <p style="opacity:.75;max-width:460px">В Telegram-канале — живые видео моделей, механизмы трансформации, новые ткани и подробные описания диванов.</p>
      </div>
      <div class="social-links">
        <a href="{TG}" target="_blank" rel="noopener">{I['tg']}<div><b>Telegram</b><small>t.me/mmebel_m — видео и описания</small></div></a>
        <a href="{IG}" target="_blank" rel="noopener">{I['ig']}<div><b>Instagram</b><small>@mmebel_m</small></div></a>
        <a href="{PIN}" target="_blank" rel="noopener">{I['pin']}<div><b>Pinterest</b><small>mmebel_m — идеи для интерьера</small></div></a>
        <a href="{wa()}" target="_blank" rel="noopener">{I['wa']}<div><b>WhatsApp</b><small>{WA_TXT} — консультация и цены</small></div></a>
      </div>
    </div>
  </div>
</section>'''

def write(name, content):
    with open(os.path.join(OUT, name), 'w', encoding='utf-8') as f:
        f.write(content)
    print('✓', name)

# ================= ГЛАВНАЯ =================
def index():
    hero_pages = [5, 1, 19, 7, 47, 42]
    slides = ''.join(f'<div class="hero-slide{" active" if k==0 else ""}" data-name="{e(P[n]["name"])}" data-coll="{P[n]["collName"]}"><img src="img/products/{P[n]["img"]}.webp" alt="{e(P[n]["name"])}" {"" if k==0 else "loading=lazy"} width="1000" height="676"></div>' for k, n in enumerate(hero_pages))
    mc_rail = ''.join(card(P[n], True) for n in [1, 3, 5, 7, 13, 19])
    mm_rail = ''.join(card(P[n], True) for n in [21, 25, 33, 42, 47, 56])
    shops = ''.join(f'''
      <div class="store rv{' rv-d1' if k else ''}">
        <span class="tag">Фирменный магазин · {s['city']}</span>
        <h3>{s['name']}</h3>
        <a class="ph" href="tel:{s['tel']}">{s['phone']}</a>
        <p class="muted">Вся коллекция M Comfort и М Мебель, образцы тканей, консультация по механизмам.</p>
        <div class="row">
          <a class="btn btn-dark btn-sm" href="tel:{s['tel']}">{I['ph']} Позвонить</a>
          {f'<a class="btn btn-wa btn-sm" href="{wa("Здравствуйте! Пишу по поводу магазина на Доваторцев, 74.")}" target="_blank" rel="noopener">{I["wa"]} WhatsApp</a>' if s.get('wa') else ''}
          <a class="btn btn-outline btn-sm" href="{map_link(s['city']+', '+s['name'])}" target="_blank" rel="noopener">{I['pin2']} Маршрут</a>
        </div>
      </div>''' for k, s in enumerate(SHOPS))
    chips = ''.join(f'<span class="chip">{c}</span>' for c in CITIES)
    n_models = len(PRODUCTS)
    body = f'''
<section class="hero on-dark">
  <div class="container hero-grid">
    <div>
      <span class="eyebrow rv">Фабрика мягкой мебели · Ставрополь</span>
      <h1 class="rv rv-d1" style="margin-top:22px">Мягкая мебель,<br>в которой <em>хочется</em><br>остаться</h1>
      <p class="lead rv rv-d2">«М Мебель» — производство полного цикла с 1998 года. Диваны и кресла от базовых моделей до премиальной линии M Comfort с электрореклайнерами и наполнителем «лебяжий пух».</p>
      <div class="hero-actions rv rv-d3">
        <a class="btn btn-light" href="catalog.html">Смотреть каталог {I['arr']}</a>
        <a class="btn btn-wa" href="{wa('Здравствуйте! Хочу узнать цену на диван.')}" target="_blank" rel="noopener">{I['wa']} Узнать цену</a>
      </div>
    </div>
    <div class="rv rv-d2">
      <div class="hero-stage">{slides}</div>
      <div class="hero-caption"><div><b>Фрэнк</b><span>M Comfort</span></div><div class="hero-dots"></div></div>
    </div>
  </div>
  <div class="hero-scroll" aria-hidden="true"></div>
</section>

<section class="stats">
  <div class="container stats-grid">
    <div class="stat rv"><b>1998</b><span>год основания фабрики</span></div>
    <div class="stat rv rv-d1"><b>{n_models}</b><span>моделей в каталоге: диваны, угловые, кресла, пуфы</span></div>
    <div class="stat rv rv-d2"><b>{len(CITIES)}+</b><span>городов России, где представлена наша мебель</span></div>
    <div class="stat rv rv-d3"><b>100%</b><span>собственное производство — от дизайна до упаковки</span></div>
  </div>
</section>

<section class="collections section" id="collections">
  <div class="container">
    <div class="section-head">
      <div><span class="eyebrow">Две линейки</span><h2>Выберите свою коллекцию</h2></div>
      <div class="switch" data-switch="#coll-stage">
        <span class="pill"></span>
        <button class="active" data-key="mc">M Comfort</button>
        <button data-key="mm">М Мебель</button>
      </div>
    </div>
    <div class="coll-stage" id="coll-stage" data-active="mc">
      <span class="arc"></span>
      <div class="coll-panel active" data-key="mc">
        <div class="c-text">
          <img class="c-logo" src="img/brand/mc-light.png" alt="M Comfort Collection" width="516" height="222">
          <h3>Премиальная линия</h3>
          <p>С 2017 года мы выпускаем Comfort Collection — современные технологии, массив дерева и наполнитель «лебяжий пух» из Южной Кореи, максимально приближенный по ощущениям к натуральному.</p>
          <ul>
            <li>Электрореклайнеры и механизм «Спартак»</li>
            <li>Независимый пружинный блок и HR ППУ повышенной плотности</li>
            <li>Массив прочных пород дерева, березовая фанера</li>
          </ul>
          <a class="btn btn-light" href="catalog.html?c=mc">Модели M Comfort {I['arr']}</a>
        </div>
        <div class="c-visual"><img src="img/products/01.webp" alt="Бруклин угловой" loading="lazy"><img src="img/products/06.webp" alt="Кресло Фрэнк" loading="lazy"></div>
      </div>
      <div class="coll-panel" data-key="mm">
        <div class="c-text">
          <img class="c-logo" src="img/brand/mm-light.png" alt="М Мебель" width="241" height="273">
          <h3>Основная коллекция</h3>
          <p>Практичные и красивые диваны на каждый день: прямые и угловые модели, кресла-кровати и пуфы. Надёжные механизмы трансформации и вместительные бельевые ящики.</p>
          <ul>
            <li>Еврокнижка «тик-так», дельфин, выкатной, аккордеон, книжка</li>
            <li>Независимый пружинный блок или пружина «Змейка»</li>
            <li>Широкий выбор тканей и цветов</li>
          </ul>
          <a class="btn btn-light" href="catalog.html?c=mm">Модели М Мебель {I['arr']}</a>
        </div>
        <div class="c-visual"><img src="img/products/25.webp" alt="Лидер угловой" loading="lazy"><img src="img/products/47.webp" alt="Атлант" loading="lazy"></div>
      </div>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="container">
    <div class="section-head">
      <div><span class="eyebrow">M Comfort Collection</span><h2>Хиты премиальной линии</h2></div>
      <a class="link-arrow" href="catalog.html?c=mc">Все модели {I['arr']}</a>
    </div>
    <div class="rail rv">{mc_rail}</div>
    <div class="section-head" style="margin-top:80px">
      <div><span class="eyebrow">Коллекция М Мебель</span><h2>Популярные модели</h2></div>
      <a class="link-arrow" href="catalog.html?c=mm">Все модели {I['arr']}</a>
    </div>
    <div class="rail rv">{mm_rail}</div>
  </div>
</section>

<section class="down section" id="down">
  <div class="container down-grid">
    <div class="down-visual rv">
      <span class="ring"></span><span class="ring"></span><span class="ring"></span>
      <div class="core"><div>Пух<br>собственного<br>производства<small>мягкость без компромиссов</small></div></div>
      <i class="flake" style="top:8%;left:46%"></i><i class="flake" style="top:30%;right:4%;animation-delay:-3s"></i>
      <i class="flake" style="bottom:14%;left:12%;animation-delay:-5s;width:10px;height:10px"></i><i class="flake" style="bottom:4%;right:30%;animation-delay:-2s;width:18px;height:18px"></i>
    </div>
    <div>
      <span class="eyebrow">Наша гордость</span>
      <h2 style="margin:16px 0 20px">Пух для набивки мы производим сами</h2>
      <p class="lead">Сырьё поступает к нам в неготовом виде и проходит обработку на нашем оборудовании — поэтому мы контролируем качество на каждом этапе. Наш пух поставляется и другим мебельным фабрикам по всей России.</p>
      <div class="down-points">
        <div><i>01</i><p><b>Полный контроль</b><span>От сырья до готового наполнителя — всё на нашем производстве.</span></p></div>
        <div><i>02</i><p><b>«Лебяжий пух» в M Comfort</b><span>Мягкий гипоаллергенный наполнитель из Южной Кореи — ощущения как от натурального пуха.</span></p></div>
        <div><i>03</i><p><b>Продаём отдельно</b><span>Нужен пух для своего производства или для перетяжки? Поставляем оптом и в розницу.</span></p></div>
      </div>
      <div class="hero-actions">
        <a class="btn btn-dark" href="tel:{B2B_DOWN['tel']}">{I['ph']} Купить пух · {B2B_DOWN['person']}</a>
        <a class="link-arrow" href="production.html#down">Подробнее {I['arr']}</a>
      </div>
    </div>
  </div>
</section>

<section class="prod section on-dark">
  <div class="container">
    <div class="section-head">
      <div><span class="eyebrow">Производство полного цикла</span><h2>От разработки дизайна до упаковки готового изделия</h2></div>
      <a class="btn btn-outline" href="production.html">О производстве {I['arr']}</a>
    </div>
    <div class="shops-grid rv">
      <div class="shop"><span class="n">01</span><div><b>Отдел разработки</b><p>Создаём модели и конструкции</p></div></div>
      <div class="shop"><span class="n">02</span><div><b>Столярный цех</b><p>Каркасы из массива и фанеры</p></div></div>
      <div class="shop"><span class="n">03</span><div><b>Швейный цех</b><p>Крой и пошив чехлов</p></div></div>
      <div class="shop"><span class="n">04</span><div><b>Обивочный цех</b><p>Сборка и обивка изделий</p></div></div>
      <div class="shop"><span class="n">05</span><div><b>Пуховой отдел</b><p>Собственный наполнитель</p></div></div>
      <div class="shop"><span class="n">06</span><div><b>Отдел контроля качества</b><p>ОТК проверяет каждый этап</p></div></div>
      <div class="shop"><span class="n">07</span><div><b>Склады</b><p>Готовая продукция и материалы</p></div></div>
      <div class="shop"><span class="n">08</span><div><b>Оборудование</b><p>Из Германии и Австрии</p></div></div>
    </div>
  </div>
</section>

<section class="section" id="where">
  <div class="container">
    <div class="section-head">
      <div><span class="eyebrow">Где купить</span><h2>Приходите посидеть на диванах вживую</h2></div>
      <p class="lead" style="max-width:420px">Цены — по запросу: позвоните или напишите в ближайший к вам магазин, и мы рассчитаем стоимость в нужной ткани.</p>
    </div>
    <div class="where-grid">{shops}</div>
    <div class="cities rv">
      <div class="cities-head">
        <div><span class="eyebrow">По всей России</span><h3 style="margin-top:10px">Наша мебель в салонах {len(CITIES)} городов</h3></div>
        <a class="link-arrow" href="partners.html#cities">Все города и партнёрство {I['arr']}</a>
      </div>
      <div class="chips">{chips}</div>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0" id="b2b">
  <div class="container">
    <div class="section-head"><div><span class="eyebrow">Оптовым партнёрам</span><h2>Работаем с магазинами и фабриками</h2></div></div>
    <div class="b2b-grid">
      <div class="b2b dark rv">
        <span class="num">01 — ДЛЯ МЕБЕЛЬНЫХ МАГАЗИНОВ</span>
        <h3>Мебель оптом</h3>
        <p>Ищем мебельные магазины в регионах России, заинтересованные в продаже готовой качественной мебели от производителя. От вас — заказы и хороший настрой, от нас — стильная и удобная мебель в ваши магазины.</p>
        <div class="who"><div><small>Менеджер</small><b>{B2B_FURN['person']}</b></div><a class="btn btn-light" href="tel:{B2B_FURN['tel']}">{I['ph']} {B2B_FURN['phone']}</a></div>
      </div>
      <div class="b2b sand rv rv-d1">
        <span class="num">02 — ДЛЯ МЕБЕЛЬНЫХ ПРОИЗВОДСТВ</span>
        <h3>Пух оптом и в розницу</h3>
        <p>Пух собственного производства для набивки подушек, спинок и сидений. Уже поставляем другим мебельным фабрикам по всей России.</p>
        <div class="who"><div><small>Менеджер</small><b>{B2B_DOWN['person']}</b></div><a class="btn btn-dark" href="tel:{B2B_DOWN['tel']}">{I['ph']} {B2B_DOWN['phone']}</a></div>
      </div>
    </div>
  </div>
</section>
{social_block()}'''
    write('index.html', head('М Мебель — фабрика мягкой мебели в Ставрополе | диваны M Comfort',
        'Фабрика мягкой мебели «М Мебель» в Ставрополе с 1998 года. Диваны, угловые диваны, кресла с электрореклайнерами. Премиальная линия M Comfort. Мебель и пух оптом.', 'index.html')
        + header('index.html') + '<main>' + body + '</main>' + footer() + end())

# ================= КАТАЛОГ =================
def catalog():
    cards_html = ''
    for c in ['mc', 'mm']:
        logo = 'mc-dark.png' if c == 'mc' else 'mm-dark.png'
        cards_html += f'<div class="coll-divider" data-coll="{c}"><img src="img/brand/{logo}" alt="{COLL[c]}"><span></span></div>'
        cards_html += ''.join(card(p) for p in PRODUCTS if p['coll'] == c)
    mech_opts = ''.join(f'<option value="{e(m)}">{e(m)}</option>' for m in MECHS)
    data = json.dumps(PRODUCTS, ensure_ascii=False)
    body = page_hero('Каталог', 'Каталог мягкой мебели', 'Каталог моделей',
        f'{len(PRODUCTS)} моделей двух коллекций. Нажмите на модель, чтобы увидеть размеры, механизм и наполнение. Цена — по запросу в WhatsApp.') + f'''
<div class="filters">
  <div class="container filters-inner">
    <div class="seg" data-filter="coll"><button data-v="all" class="active">Все</button><button data-v="mc">M Comfort</button><button data-v="mm">М Мебель</button></div>
    <div class="seg" data-filter="type"><button data-v="all" class="active">Все типы</button><button data-v="corner">Угловые</button><button data-v="sofa">Диваны</button><button data-v="chair">Кресла</button><button data-v="pouf">Пуфы</button></div>
    <select class="select" id="f-mech" aria-label="Механизм"><option value="all">Любой механизм</option>{mech_opts}</select>
    <input class="search" id="f-q" type="search" placeholder="Поиск по названию…" aria-label="Поиск">
    <span class="count" id="count"></span>
  </div>
</div>
<section class="section" style="padding-top:40px">
  <div class="container">
    <div class="grid" id="catalog-grid">{cards_html}</div>
    <div class="empty" id="empty"><h3>Ничего не найдено</h3><p>Попробуйте изменить фильтры</p></div>
  </div>
</section>
{cta_band()}
<div class="modal" id="modal" role="dialog" aria-modal="true" aria-labelledby="m-name">
  <div class="modal-bg" data-close></div>
  <div class="modal-box">
    <button class="modal-close" data-close aria-label="Закрыть">{I['x']}</button>
    <div class="modal-media">
      <div class="seg views" id="m-views"><button data-v="photo" class="active">Фото</button><button data-v="page">Страница каталога</button></div>
      <img id="m-img" src="" alt="">
    </div>
    <div class="modal-info">
      <div class="card-top"><span class="badge" id="m-coll"></span><span class="card-type" id="m-type"></span></div>
      <h2 id="m-name"></h2>
      <dl>
        <div class="spec"><dt>Размеры, см</dt><dd><ul id="m-sizes"></ul></dd></div>
        <div class="spec" style="margin-top:14px"><dt>Механизм</dt><dd id="m-mech"></dd></div>
        <div class="spec" style="margin-top:14px"><dt>Конструкция и наполнение</dt><dd><ul id="m-mat"></ul></dd></div>
      </dl>
      <div class="price-note"><b>Цена по запросу.</b> Стоимость зависит от ткани и комплектации — напишите нам, и менеджер рассчитает цену и пришлёт варианты обивки.</div>
      <div class="modal-actions">
        <a class="btn btn-wa" id="m-wa" href="#" target="_blank" rel="noopener">{I['wa']} Узнать цену в WhatsApp</a>
        <div style="display:flex;gap:10px;justify-content:space-between;align-items:center;flex-wrap:wrap">
          <a class="link-arrow" href="contacts.html">Магазины рядом {I['arr']}</a>
          <div class="modal-nav"><button id="m-prev" aria-label="Предыдущая">{I['l']}</button><button id="m-next" aria-label="Следующая">{I['r']}</button></div>
        </div>
      </div>
    </div>
  </div>
</div>'''
    write('catalog.html', head('Каталог диванов и кресел — М Мебель и M Comfort', 'Каталог мягкой мебели фабрики «М Мебель»: угловые и прямые диваны, кресла с электрореклайнерами, пуфы. Размеры, механизмы, наполнение. Цена по запросу.', 'catalog.html')
        + header('catalog.html') + '<main>' + body + '</main>' + footer() + end(f'<script>window.PRODUCTS={data}</script>'))

# ================= ПРОИЗВОДСТВО =================
def production():
    body = page_hero('Производство и пух', 'О фабрике', 'Современная мебельная фабрика на юге России',
        '«М Мебель» — производство полного цикла в Ставрополе. С 1998 года мы сохраняем лучшие традиции и используем проверенные материалы от ведущих производителей.') + f'''
<section class="section">
  <div class="container two-col">
    <div class="rv">
      <span class="eyebrow">Кто мы</span>
      <p class="quote" style="margin-top:18px">Место, где сочетаются качество, уют и современный дизайн.</p>
    </div>
    <div class="prose rv rv-d1">
      <p>Наша мебель создаётся <b>опытной командой профессионалов</b>, тщательно контролирующих качество каждого изделия. Наш главный капитал — специалисты, которые годами оттачивали своё мастерство и с любовью создают качественную и долговечную мебель для вашего комфорта.</p>
      <p>В ассортименте — мебель на любой вкус: <b>от базовых моделей до эксклюзивных диванов и кресел с электрореклайнерами</b>. Вся продукция проходит строгий контроль качества и производится на современном оборудовании из Германии и Австрии.</p>
      <p>В каждом цехе установлено <b>новейшее оборудование</b> и мощные вытяжные системы, обеспечивающие высокое качество продукции и безопасные условия труда.</p>
    </div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="container timeline">
    <div class="tl rv"><b>1998</b><p>Основание фабрики «М Мебель» в Ставрополе.</p></div>
    <div class="tl rv rv-d1"><b>2017</b><p>Запуск премиальной линии M Comfort Collection с «лебяжьим пухом» из Южной Кореи.</p></div>
    <div class="tl rv rv-d2"><b>{len(CITIES)}+</b><p>городов России, где наша мебель представлена в салонах партнёров.</p></div>
  </div>
</section>
<section class="prod section on-dark">
  <div class="container">
    <div class="section-head"><div><span class="eyebrow">Полный цикл</span><h2>В нашей структуре работают</h2></div></div>
    <div class="shops-grid rv">
      <div class="shop"><span class="n">01</span><div><b>Отдел разработки</b><p>Дизайн, конструкция, прототипы</p></div></div>
      <div class="shop"><span class="n">02</span><div><b>Столярный цех</b><p>Каркасы из массива прочных пород и березовой фанеры</p></div></div>
      <div class="shop"><span class="n">03</span><div><b>Швейный цех</b><p>Крой и пошив чехлов</p></div></div>
      <div class="shop"><span class="n">04</span><div><b>Обивочный цех</b><p>Сборка, набивка и обивка</p></div></div>
      <div class="shop"><span class="n">05</span><div><b>Пуховой отдел</b><p>Обработка сырья и производство наполнителя</p></div></div>
      <div class="shop"><span class="n">06</span><div><b>ОТК</b><p>Отдел технического контроля на каждом этапе</p></div></div>
      <div class="shop"><span class="n">07</span><div><b>Склады</b><p>Хранение материалов и готовой продукции</p></div></div>
      <div class="shop"><span class="n">08</span><div><b>Офисы</b><p>Продажи, логистика, работа с партнёрами</p></div></div>
    </div>
    <div class="feature-row">
      <div class="feature rv"><b>Оборудование из Германии и Австрии</b><p>Точность раскроя и стабильное качество каждой партии.</p></div>
      <div class="feature rv rv-d1"><b>Строгий контроль ОТК</b><p>Каждый этап проверяется — ваш диван приедет в целости и сохранности.</p></div>
      <div class="feature rv rv-d2"><b>Проверенные материалы</b><p>Массив дерева, березовая фанера, HR ППУ, независимый пружинный блок.</p></div>
    </div>
  </div>
</section>
<section class="down section" id="down">
  <div class="container down-grid">
    <div class="down-visual rv">
      <span class="ring"></span><span class="ring"></span><span class="ring"></span>
      <div class="core"><div>Собственный<br>пух<small>оптом и в розницу</small></div></div>
      <i class="flake" style="top:8%;left:46%"></i><i class="flake" style="top:30%;right:4%;animation-delay:-3s"></i>
      <i class="flake" style="bottom:14%;left:12%;animation-delay:-5s;width:10px;height:10px"></i>
    </div>
    <div>
      <span class="eyebrow">Пух для мебели</span>
      <h2 style="margin:16px 0 20px">Высококачественный пух собственного производства</h2>
      <p class="lead">Для набивки нашей мебели мы используем пух собственного производства, который проходит обработку на нашем оборудовании. Сырьё поступает к нам в неготовом виде — это позволяет контролировать качество на каждом этапе.</p>
      <div class="down-points">
        <div><i>01</i><p><b>Для мебельных фабрик</b><span>Наш пух уже поставляется другим производствам по всей России.</span></p></div>
        <div><i>02</i><p><b>Для частных покупателей</b><span>Продаём отдельно — для перетяжки, подушек и ремонта мебели.</span></p></div>
        <div><i>03</i><p><b>«Лебяжий пух» в M Comfort</b><span>В премиальной линии — гипоаллергенный наполнитель из Южной Кореи (Thinsulate).</span></p></div>
      </div>
      <div class="hero-actions">
        <a class="btn btn-dark" href="tel:{B2B_DOWN['tel']}">{I['ph']} {B2B_DOWN['phone']}</a>
        <span class="muted">Менеджер по пуху — {B2B_DOWN['person']}</span>
      </div>
    </div>
  </div>
</section>
{cta_band()}'''
    write('production.html', head('Производство и пух — фабрика М Мебель, Ставрополь', 'Производство мягкой мебели полного цикла в Ставрополе: столярный, швейный, обивочный цеха, ОТК. Пух собственного производства оптом и в розницу.', 'production.html')
        + header('production.html') + '<main>' + body + '</main>' + footer() + end())

# ================= ПАРТНЁРАМ =================
def partners():
    chips = ''.join(f'<span class="chip">{c}</span>' for c in CITIES)
    new = ''.join(f'<span class="chip new">{c}</span>' for c in NEW_CITIES)
    body = page_hero('Опт и партнёрам', 'Оптовым партнёрам', 'Мебель и пух оптом от производителя',
        'Уже более 25 лет «М Мебель» успешно сотрудничает с оптовыми партнёрами. Мы наладили прочные связи с множеством городов по всей России и продолжаем расширять географию.') + f'''
<section class="section">
  <div class="container">
    <div class="b2b-grid">
      <div class="b2b dark rv">
        <span class="num">01 — ДЛЯ МЕБЕЛЬНЫХ МАГАЗИНОВ</span>
        <h3>Мебель оптом</h3>
        <p>Мы ищем мебельные магазины в регионах России, заинтересованные в продаже готовой качественной мебели от производителя. От вас ждём заказы и хороший настрой. От нас гарантируем стильную и удобную мебель в ваши магазины.</p>
        <ul style="list-style:none;display:grid;gap:8px;opacity:.85;font-size:15px">
          <li>— {len(PRODUCTS)} моделей в двух ценовых сегментах</li>
          <li>— Премиальная линия M Comfort для требовательных клиентов</li>
          <li>— Стабильное качество и контроль ОТК</li>
        </ul>
        <div class="who"><div><small>Менеджер по опту</small><b>{B2B_FURN['person']}</b></div><a class="btn btn-light" href="tel:{B2B_FURN['tel']}">{I['ph']} {B2B_FURN['phone']}</a></div>
      </div>
      <div class="b2b sand rv rv-d1">
        <span class="num">02 — ДЛЯ МЕБЕЛЬНЫХ ПРОИЗВОДСТВ</span>
        <h3>Пух оптом и в розницу</h3>
        <p>Высококачественный пух собственного производства. Сырьё обрабатывается на нашем оборудовании, поэтому мы отвечаем за качество на каждом этапе. Поставляем фабрикам по всей России.</p>
        <div class="who"><div><small>Менеджер по пуху</small><b>{B2B_DOWN['person']}</b></div><a class="btn btn-dark" href="tel:{B2B_DOWN['tel']}">{I['ph']} {B2B_DOWN['phone']}</a></div>
      </div>
    </div>
  </div>
</section>
<section class="section" style="padding-top:0" id="cities">
  <div class="container">
    <div class="cities rv" style="margin-top:0">
      <div class="cities-head"><div><span class="eyebrow">География</span><h2 style="margin-top:12px">Города, в которых мы уже представлены</h2></div></div>
      <div class="chips">{chips}</div>
      <p class="muted" style="margin-top:22px;font-size:14px">Хотите узнать адрес салона в вашем городе? Напишите нам в <a href="{wa('Здравствуйте! Где можно посмотреть вашу мебель в моём городе: ')}" target="_blank" rel="noopener" style="text-decoration:underline">WhatsApp</a> — подскажем ближайший магазин.</p>
    </div>
    <div class="cities rv" style="margin-top:26px;background:var(--sand)">
      <div class="cities-head"><div><span class="eyebrow">Ищем партнёров</span><h3 style="margin-top:10px">Актуальные города для сотрудничества</h3></div>
        <a class="btn btn-dark btn-sm" href="tel:{B2B_FURN['tel']}">{I['ph']} Обсудить сотрудничество</a></div>
      <div class="chips">{new}</div>
      <p class="muted" style="margin-top:22px;font-size:14px">Если вы находитесь в одном из этих городов — будем очень рады сотрудничеству.</p>
    </div>
  </div>
</section>
{social_block()}'''
    write('partners.html', head('Мебель и пух оптом от производителя — М Мебель', 'Оптовые поставки мягкой мебели для магазинов и пуха для мебельных производств от фабрики «М Мебель», Ставрополь. Представлены в 30+ городах России.', 'partners.html')
        + header('partners.html') + '<main>' + body + '</main>' + footer() + end())

# ================= КОНТАКТЫ =================
def contacts():
    a0 = SHOPS[1]['city'] + ', ' + SHOPS[1]['name']
    shops = ''.join(f'''
      <div class="c-card rv">
        <span class="tag">Магазин · {s['city']}</span>
        <b>{s['name']}</b>
        <a class="ph" href="tel:{s['tel']}">{s['phone']}</a>
        <div class="row">
          {f'<a class="btn btn-wa btn-sm" href="{wa()}" target="_blank" rel="noopener">{I["wa"]} WhatsApp</a>' if s.get('wa') else f'<a class="btn btn-dark btn-sm" href="tel:{s["tel"]}">{I["ph"]} Позвонить</a>'}
          <button class="btn btn-outline btn-sm" data-map-btn="{map_url(s['city']+', '+s['name'])}">{I['pin2']} На карте</button>
        </div>
      </div>''' for s in SHOPS)
    body = page_hero('Контакты', 'Контакты', 'Будем рады вам', 'Цены на мебель — по запросу. Напишите в WhatsApp или позвоните в ближайший магазин — подберём модель и ткань.') + f'''
<section class="section">
  <div class="container">
    <div class="contact-grid">
      <div class="c-card rv" style="background:var(--ink);color:#fff;border-color:var(--ink)">
        <span class="tag" style="color:var(--taupe-2)">Розница · консультация</span>
        <b>WhatsApp</b>
        <a class="ph" href="{wa()}" target="_blank" rel="noopener">{WA_TXT}</a>
        <p style="opacity:.7;font-size:14px">Цены, ткани, наличие, доставка</p>
        <div class="row"><a class="btn btn-wa btn-sm" href="{wa('Здравствуйте! Хочу узнать цену на диван.')}" target="_blank" rel="noopener">{I['wa']} Написать</a></div>
      </div>
      {shops}
      <div class="c-card rv">
        <span class="tag">Мебель оптом</span>
        <b>{B2B_FURN['person']}</b>
        <a class="ph" href="tel:{B2B_FURN['tel']}">{B2B_FURN['phone']}</a>
        <p class="muted" style="font-size:14px">Для мебельных магазинов</p>
      </div>
      <div class="c-card rv rv-d1">
        <span class="tag">Пух оптом и продажа</span>
        <b>{B2B_DOWN['person']}</b>
        <a class="ph" href="tel:{B2B_DOWN['tel']}">{B2B_DOWN['phone']}</a>
        <p class="muted" style="font-size:14px">Для производств и частных покупателей</p>
      </div>
      <div class="c-card rv rv-d2">
        <span class="tag">Соцсети</span>
        <b>@mmebel_m</b>
        <div class="row" style="margin-top:0">
          <a class="btn btn-outline btn-sm" href="{TG}" target="_blank" rel="noopener">{I['tg']} Telegram</a>
          <a class="btn btn-outline btn-sm" href="{IG}" target="_blank" rel="noopener">{I['ig']} Instagram</a>
          <a class="btn btn-outline btn-sm" href="{PIN}" target="_blank" rel="noopener">{I['pin']} Pinterest</a>
        </div>
      </div>
    </div>
    <div class="map" id="map" data-map="{map_url(a0)}"></div>
  </div>
</section>
{social_block()}'''
    write('contacts.html', head('Контакты — магазины М Мебель в Ставрополе', 'Магазины мягкой мебели «М Мебель» в Ставрополе: Михайловское шоссе, 14 и ул. Доваторцев, 74. WhatsApp, телефоны оптовых менеджеров.', 'contacts.html')
        + header('contacts.html') + '<main>' + body + '</main>' + footer() + end())

if __name__ == '__main__':
    index(); catalog(); production(); partners(); contacts()
    open(os.path.join(OUT, '.nojekyll'), 'w').close()
