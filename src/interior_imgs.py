"""Готовит фото «в интерьере»: src/interior/raw/* -> docs/img/interior/<стр>-<n>-{640,1280}.webp"""
import os
from PIL import Image, ImageOps
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, 'src', 'interior', 'raw')
OUT = os.path.join(ROOT, 'docs', 'img', 'interior')
os.makedirs(OUT, exist_ok=True)
count = {}
for line in open(os.path.join(ROOT, 'src', 'interior.txt'), encoding='utf-8'):
    line = line.strip()
    if not line or line.startswith('#'): continue
    f, page = line.split('|'); page = int(page)
    count[page] = count.get(page, 0) + 1
    im = ImageOps.exif_transpose(Image.open(os.path.join(RAW, f))).convert('RGB')
    for w in (640, 1280):
        h = round(im.height * w / im.width)
        im.resize((w, h), Image.LANCZOS).save(os.path.join(OUT, f'{page:02d}-{count[page]}-{w}.webp'), quality=80, method=6)
print('ok', sum(count.values()))
