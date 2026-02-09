import json
import os
import math
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def read_file():
    with open("meta_data.json", "r", encoding="utf-8") as file:
        meta_data = file.read()

    books = json.loads(meta_data)
    return books


def create_directory(directory):
    os.makedirs(directory, exist_ok=True)


def split_books(books):
    half = math.ceil(len(books) / 2)
    columns = list(chunked(books, half))
    return columns


def split_pages(books):
    books_amount = 20
    pages = list(chunked(books, books_amount))
    return pages


def on_reload(template, directory, pages):
    total = len(pages)
    for page_id, page in enumerate(pages, start=1):
        columns = split_books(page)
        prev_link = f"index{page_id-1}.html" if page_id > 1 else None
        next_link = f"index{page_id+1}.html" if page_id < total else None
        page_links = [f"index{i}.html" for i in range(1, total + 1)]

        rendered_page = template.render(
            columns=columns,
            prev_link=prev_link,
            next_link=next_link,
            page_links=page_links,
            current_page=page_id
        )

        if page_id == 1:
            filepath_root = os.path.join(directory, 'index.html')
            with open(filepath_root, 'w', encoding="utf8") as f:
                f.write(rendered_page)

            first_filepath = os.path.join(directory, 'index1.html')
            with open(first_filepath, 'w', encoding="utf8") as f:
                f.write(rendered_page)
        else:
            filename = f"index{page_id}.html"
            filepath = os.path.join(directory, filename)
            with open(filepath, 'w', encoding="utf8") as file:
               file.write(rendered_page)


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    directory = os.path.join(os.path.dirname(__file__), 'pages')
    create_directory(directory)


    def regenerate():
        books = read_file()
        pages = split_pages(books)
        on_reload(template, directory, pages)

    regenerate()

    server = Server()
    server.watch('template.html', regenerate)
    print("server.serve start")
    server.serve(root=directory, host='127.0.0.1', port=5500, debug=True)


if __name__ == '__main__':
    main()