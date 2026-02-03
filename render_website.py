import json
import math
import pprint
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def read_file():
    with open("meta_data.json", "r", encoding="utf-8") as file:
        meta_data = file.read()

    books = json.loads(meta_data)
    return books


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    books = read_file()
    half = math.ceil(len(books) / 2)
    columns = list(chunked(books, half))

    rendered_page = template.render(
        columns=columns,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def main():  
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    print("server.serve start")
    server.serve(root='.', host='127.0.0.1', port=5500, debug=True)


if __name__ == '__main__':
    main()