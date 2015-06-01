# -*- coding: utf-8 -*-

__version__ = '0.1.0'


import sys
import os
import markdown
import json
import shutil
from datetime import date, datetime
import http.server
import socketserver
import argparse as ap
import jinja2 as jn

"""
statico --> creates structure directory in current directory
statico -g or --generate --> the output/public directory
statico -p or --page "page_title"
statico -a or --article "article_title"
statico -d or --deploy
"""


def normalize_title(title):
    return title.lower().replace(' ', '-')


def copy_directory(src, dest):
    try:
        shutil.copytree(src, dest)
    # Directories are the same
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Directory not copied. Error: %s' % e)


def run_server():
    print('cd output')
    os.chdir('output')

    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)

    print("Serving at http://127.0.0.1:" + str(PORT) + ' ...')
    httpd.serve_forever()


def deploy():
    pass


def validate_date(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        return False

    return True


def parse_metadata(fp):
    found_open = False
    found_close = False
    rest = []
    data = {}

    for line in fp:
        line = line.strip()

        if line == '---' and not found_open:
            found_open = True
        elif line == '---' and found_open:
            found_close = True
        elif found_open and not found_close:
            parts = line.split(':')
            attr = parts[0]
            value = parts[1].strip()

            if validate_date(value):
                data[attr] = datetime.strptime(value, '%Y-%m-%d').strftime('%B %d, %Y')
            else:
                data[attr] = value
        else:  # Found close
            rest.append(line)

    return rest, data


def parse_index(filename, o):
    """
    ---
    layout: default/custom
    ---
    if custom the write here:
    ...
    """
    fp = open(filename)
    rest, data = parse_metadata(fp)
    html = markdown.markdown(''.join(rest))
    data['articles'] = get_articles(o.get('articles'))
    data['content'] = html
    data['site'] = o.get('settings')

    template = o.get('env').get_template('default.html')
    page = template.render(data)
    open(os.path.join('output', 'index.html'), 'w').write(page)


def clear_workspace():
    if os.path.isfile('settings.json'):
        os.remove('settings.json')
    shutil.rmtree('content', True)
    shutil.rmtree('output', True)
    shutil.rmtree('static', True)
    shutil.rmtree('templates', True)


def get_articles(f_articles):
    articles = []

    for f_article in f_articles:
        fp = open(f_article)
        rest, data = parse_metadata(fp)
        data['content'] = markdown.markdown(''.join(rest))
        articles.append(data)

    return articles


def create():
    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path)

    # Settings
    shutil.copy(os.path.join(dir_path, 'settings.json'), 'settings.json')
    print(' - settings.json [DONE]')

    # Static
    static_path = os.path.join(dir_path, 'static')
    copy_directory(static_path, 'static')
    print(' - Static assets [DONE]')

    # Templates
    templates_path = os.path.join(dir_path, 'templates')
    copy_directory(templates_path, 'templates')
    print(' - Templates [DONE]')

    # Content
    os.makedirs('content')
    os.makedirs(os.path.join('content', 'articles'))
    os.makedirs(os.path.join('content', 'pages'))
    index = open(os.path.join('content', 'index.md'), 'w')
    index.writelines([
        '---\n',
        'layout: default\n',
        '---\n'
    ])
    print(' - Contents directory [DONE]')

    # Output
    os.makedirs('output')
    print(' - Output directory [DONE]')


def new_page(name):
    settings = json.load(open('settings.json'))
    filename = os.path.join('content', 'pages', name + '.md')

    if os.path.isfile(filename):
        if input(name + ' already exists! Do you want to overwrite it? [y/n] ') == 'n':
            return

    page = open(filename, 'w')
    page.writelines([
        '---\n',
        'layout: page\n',
        'title: ' + name + '\n',
        'date: ' + date.today().isoformat() + '\n',
        'author: ' + settings.get('author') + '\n',
        '---\n'
    ])
    page.close()


def new_article(title):
    # 2015/05/27/99-challenge/
    settings = json.load(open('settings.json'))
    filename = os.path.join('content', 'articles', date.today().isoformat() + '-' + normalize_title(title) + '.md')

    if os.path.isfile(filename):
        if input(title + ' already exists! Do you want to overwrite it? [y/n]') == 'n':
            return

    article = open(filename, 'w')
    article.writelines([
        '---\n',
        'layout: article\n',
        'title: ' + title + '\n',
        'date: ' + date.today().isoformat() + '\n',
        'author: ' + settings.get('author') + '\n',
        'summary: A beautiful page\n',
        '---\n'
    ])


def generate():
    settings = json.load(open('settings.json'))

    # Get all filenames
    pages = [os.path.join('content', 'pages', f) for f in os.listdir(os.path.join('content', 'pages'))]
    articles = [os.path.join('content', 'articles', f) for f in os.listdir(os.path.join('content', 'articles'))]

    files = pages + articles

    # BEGIN: Parse files
    loader = jn.FileSystemLoader(os.path.join(os.getcwd(), 'templates'))
    env = jn.Environment(loader=loader)

    print(' - Parsing articles and pages')
    for f in files:
        fp = open(f)
        file_no_ext = os.path.basename(os.path.normpath(f.split('.')[0]))
        rest, data = parse_metadata(fp)
        html = markdown.markdown(''.join(rest))

        target = data.get('layout') + 's'
        target_dir = os.path.join('output', target)
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
        os.makedirs(target_dir)

        # Create file in output direction
        layout = data.get('layout')
        template = env.get_template(layout + '.html')

        data['content'] = html
        data['site'] = settings
        page = template.render(data)  # Date and other things

        open(os.path.join('output', target, file_no_ext + '.html'), 'w').write(page)

    # Copy index
    print(' - Parsing index page')
    parse_index(os.path.join('content', 'index.md'), {'env': env, 'settings': settings, 'articles': articles})

    # END: Parse files

    # Copy static directory
    print(' - Generating static directory')
    static = os.path.join('output', 'static')
    if os.path.exists(static):
        shutil.rmtree(static)
    copy_directory('static', os.path.join('output', 'static'))


def main():

    # Create directory structure
    if len(sys.argv[1:]) == 0:
        print('Creating site...')
        create()
    else:
        parser = ap.ArgumentParser()
        parser.add_argument('-g', '--generate', help='Generate the output directory to upload to the web server',
                            action='store_true')
        parser.add_argument('-p', '--page', help='Create a page', type=str)
        parser.add_argument('-a', '--article', help='Create an article', type=str)
        parser.add_argument('-c', '--clear', help='Clear directory', action='store_true')
        parser.add_argument('-P', '--preview', help='Preview your site', action='store_true')
        parser.add_argument('-d', '--deploy', help='Deploy to GitHub', action='store_true')
        args = parser.parse_args()

        if args.generate:
            print('Generating site...')
            generate()
            print('Head to "output" to view your generated site.\n'
                  'Type "statico --deploy" to deploy your site to GitHub, otherwise upload manually.\n'
                  'Type "statico --preview" to get a preview of your site.')
        elif args.page:
            new_page(args.page)
        elif args.article:
            new_article(args.article)
        elif args.clear:
            if input('Are you sure you want to clear the workspace? [y/n] ') == 'y':
                clear_workspace()
        elif args.preview:
            run_server()
        elif args.deploy:
            deploy()