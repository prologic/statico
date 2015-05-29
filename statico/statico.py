# -*- coding: utf-8 -*-

__version__ = '0.1.0'


import sys
import os
import markdown
import shutil
from datetime import date
import argparse as ap
import jinja2 as jn

"""
statico --> creates structure directory in current directory
statico -g or --generate --> the output/public directory
statico -p or --page "page_title"
statico -a or --article "article_title"
statico -d or --deploy
"""

"""
Directory structure of 'generate':

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
            data[attr] = value
        else:  # Found close
            rest.append(line)

    return rest, data


def get_posts():
    return None


def create():
    settings = open('settings.py', 'w')

    # Static
    os.makedirs('static')
    os.makedirs(os.path.join('static', 'css'))
    os.makedirs(os.path.join('static', 'js'))
    os.makedirs(os.path.join('static', 'images'))
    style = open(os.path.join('static', 'css', 'main.css'), 'w')
    js = open(os.path.join('static', 'js', 'main.js'), 'w')

    # Templates
    path = os.path.abspath(__file__)
    dir_path = os.path.join(os.path.dirname(path), 'templates')
    copy_directory(dir_path, 'templates')

    # Content
    os.makedirs('content')
    os.makedirs(os.path.join('content', 'articles'))
    os.makedirs(os.path.join('content', 'pages'))
    index = open(os.path.join('content', 'index.html'), 'w')
    index.writelines([
        '---',
        'layout: default',
        '---'
    ])

    os.makedirs('output')


def new_page(name):
    filename = os.path.join('content', 'pages', name + '.md')

    if os.path.isfile(filename):
        if input(name + ' already exists! Do you want to overwrite it? [y/n] ') == 'n':
            return

    page = open(filename, 'w')
    page.writelines([
        '---',
        'layout: page',
        'title: ' + name,
        'date: ' + date.today().isoformat(),
        'author: Ossama Edbali',  # Read settings
        'summary: A beautiful page',
        '---'
    ])
    page.close()


def new_article(title):
    # 2015/05/27/99-challenge/
    filename = os.path.join('content', 'articles', date.today().isoformat() + '-' + normalize_title(title) + '.md')

    if os.path.isfile(filename):
        if input(title + ' already exists! Do you want to overwrite it? [y/n]') == 'n':
            return

    article = open(filename, 'w')
    article.writelines([
        '---',
        'layout: article',
        'title: ' + title,
        'date: ' + date.today().isoformat(),
        'author: Ossama Edbali',  # Read settings
        'summary: A beautiful page',
        '---'
    ])


def generate():
    # Go into 'content' and retrieve all files
    # Parse metadata from files
    # Convert the rest of file into html
    # Output into another directory, respecting their metadata.

    # Get all filenames
    files = [os.path.join('content', 'index.html')]
    pages = [os.path.join('content', 'pages', f) for f in os.listdir(os.path.join('content', 'pages'))]
    articles = [os.path.join('content', 'articles', f) for f in os.listdir(os.path.join('content', 'articles'))]

    files = files + pages + articles

    # BEGIN: Parse files

    for f in files:
        fp = open(f)
        file_no_ext = os.path.basename(os.path.normpath(f.split('.')[0]))
        rest, data = parse_metadata(fp)
        html = markdown.markdown(''.join(rest))

        if file_no_ext == 'index':
            target = ''
        else:
            target = data.get('layout') + 's'
            target_dir = os.path.join('output', target)
            if os.path.exists(target_dir):
                shutil.rmtree(target_dir)
            os.makedirs(target_dir)

        # Create file in output direction
        layout = data.get('layout')
        env = jn.Environment(loader=jn.PackageLoader('statico', 'templates'))
        template = env.get_template(layout + '.html')
        if layout == 'default':
            # Get all posts and pass them to render
            page = template.render({'posts': get_posts()})
        else:
            data['content'] = html
            page = template.render(data)  # Date and other things

        open(os.path.join('output', target, file_no_ext + '.html'), 'w').write(page)

    # END: Parse files

    # Copy static directory
    static = os.path.join('output', 'static')
    if os.path.exists(static):
        shutil.rmtree(static)
    copy_directory('static', os.path.join('output', 'static'))


def main():

    # Create directory structure
    if len(sys.argv[1:]) == 0:
        create()
    else:
        parser = ap.ArgumentParser()
        parser.add_argument('-g', '--generate', help='Generate the output directory to upload to the web server',
                            action='store_true')
        parser.add_argument('-p', '--page', help='Create a page', type=str)
        parser.add_argument('-a', '--article', help='Create an article', type=str)
        parser.add_argument('-d', '--deploy', help='Deploy', action='store_true')
        args = parser.parse_args()

        if args.generate:
            generate()
        elif args.page:
            new_page(args.page)
        elif args.article:
            new_article(args.article)
        elif args.deploy:
            pass