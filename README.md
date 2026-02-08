# Онлайн-библиотека

Cкрипт генерирует статические HTML‑страницы онлайн‑библиотеки из файла meta_data.json и шаблона template.html. 
Результат — папка pages/ с файлами index.html (первая страница), index1.html, index2.html и т.д.

## "Скачать библиотеку"

Проект опубликован на GitHub Pages - [Online-library](https://tomaa-dev.github.io/devman_online-library/pages), достаточно просто перейти по ссылке на сайт и читать книги онлайн.

## "Хочу такой же"

Операционная система: любая, где доступен Python 3 (Windows, macOS, Linux).

- Скачайте код
- Установите зависимости командой `pip install -r requirements.txt`
- Запустите livereload-сервер командой `python3 render_website.py`

Основные файлы в проекте:

- render_website.py — основной скрипт генерации.
- template.html — Jinja2 шаблон страницы.
- meta_data.json — данные о книгах.
- pages/ — выходная директория с HTML‑страницами (создаётся скриптом).
- requirements.txt — список зависимостей.

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
