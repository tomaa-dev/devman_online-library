import json
import os
import math
from functools import partial
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked
from urllib.parse import quote


def split_books(books):
    half = math.ceil(len(books) / 2)
    columns = list(chunked(books, half))
    return columns


def split_pages(books):
    books_amount = 20
    pages = list(chunked(books, books_amount))
    return pages


def on_reload(template, directory_to_pages, pages, pages_dirname):
    total = len(pages)
    for page_id, page in enumerate(pages, start=1):
        columns = split_books(page)
        prev_link = f"/{pages_dirname}/index{page_id-1}.html" if page_id > 1 else None
        next_link = f"/{pages_dirname}/index{page_id+1}.html" if page_id < total else None
        page_links = [f"/{pages_dirname}/index{i}.html" for i in range(1, total + 1)]

        rendered_page = template.render(
            columns=columns,
            prev_link=prev_link,
            next_link=next_link,
            page_links=page_links,
            current_page=page_id
        )

        filename = f"index{page_id}.html"
        filepath_pages = os.path.join(directory_to_pages, filename)
        with open(filepath_pages, 'w', encoding="utf8") as file:
            file.write(rendered_page)


def regenerate(env, directory_to_pages, pages_dirname):
        with open("meta_data.json", "r", encoding="utf-8") as file:
            books = json.load(file)

        pages = split_pages(books)

        template = env.get_template('template.html')
        on_reload(template, directory_to_pages, pages, pages_dirname)


def main():
    pages_dirname = 'pages'
    base_directory = os.path.abspath(os.path.dirname(__file__))

    env = Environment(
        loader=FileSystemLoader(base_directory),
        autoescape=select_autoescape(['html', 'xml'])
    )
    env.filters['urlencode'] = quote


    directory_to_pages = os.path.join(base_directory, pages_dirname)
    os.makedirs(directory_to_pages, exist_ok=True)

    regenerate_no_args = partial(regenerate, env, directory_to_pages, pages_dirname)
    regenerate_no_args()

    server = Server()
    server.watch('template.html', regenerate_no_args)
    server.serve(root=base_directory, host='127.0.0.1', port=5500, debug=True)


if __name__ == '__main__':
    main()