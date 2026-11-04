# Сайт «М Мебель»

Статический сайт (без сервера и базы данных). Его можно бесплатно разместить на GitHub Pages.

## Структура
- `docs/` — готовый сайт: открывать `docs/index.html`. Эта папка и публикуется.
- `src/build.py` — генератор страниц: тексты, контакты, телефоны, список городов.
- `src/products.txt` — каталог моделей (одна строка = одна страница каталога).
- `src/imgs.py` — нарезка фото из PDF-каталога.

## Как вносить правки
1. Отредактировать `src/build.py` или `src/products.txt`.
2. Запустить `python3 src/build.py`, чтобы пересобрать HTML в `docs/`.
3. Сделать commit и push: GitHub Pages обновит сайт сам за 1–2 минуты.

## Публикация на GitHub Pages
Settings → Pages → Source: «Deploy from a branch» → Branch `main`, папка `/docs`.
