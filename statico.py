#!/usr/bin/env python


__version__ = '0.1.0'


import sys
import os
import markdown
import shutil
from datetime import date
import argparse as ap

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


def parse_metadata(fp):
    found_open = False
    found_close = False
    rest = []
    data = {}

    for line in fp:
        print(line)
        if line == '---' and not found_open:
            found_open = True
        elif line == '---' and found_open:
            found_close = True
        elif found_open and not found_close:
            parts = line.split(':')
            print(parts)
            attr = parts[0]
            value = parts[1].strip()
            data[attr] = value
        else:  # Found close
            rest.append(line + '\n')

    return rest, data


def create():
    settings = open('settings.py', 'w')

    os.makedirs('static')
    os.makedirs(os.path.join('static', 'css'))
    os.makedirs(os.path.join('static', 'js'))
    os.makedirs(os.path.join('static', 'images'))
    style = open(os.path.join('static', 'css', 'main.css'), 'w')
    js = open(os.path.join('static', 'js', 'main.js'), 'w')

    os.makedirs('templates')
    os.makedirs(os.path.join('templates', 'includes'))
    base = open(os.path.join('templates', 'base.html'), 'w')
    article = open(os.path.join('templates', 'article.html'), 'w')
    page = open(os.path.join('templates', 'page.html'), 'w')

    os.makedirs('content')
    os.makedirs(os.path.join('content', 'articles'))
    os.makedirs(os.path.join('content', 'pages'))
    index = open(os.path.join('content', 'index.html'), 'w')
    index.writelines([
        '---\n',
        'layout: default\n',
        '---\n'
    ])

    os.makedirs('output')


def new_page(name):
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
        'author: Ossama Edbali\n',  # Read settings
        'summary: A beautiful page\n',
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
        '---\n',
        'layout: article\n',
        'title: ' + title + '\n',
        'date: ' + date.today().isoformat() + '\n',
        'author: Ossama Edbali\n',  # Read settings
        'summary: A beautiful page\n',
        '---'
    ])


def generate():
    # Go into 'content' and retrieve all files
    # Parse metadata from files
    # Convert the rest of file into html
    # Output into another directory, respecting their metadata.

    # Get all filenames
    files = [os.path.join('content', 'index.md')]
    pages = [f for f in os.listdir(os.path.join('content', 'pages'))]
    articles = [f for f in os.listdir(os.path.join('content', 'articles'))]

    files = files + pages + articles

    for f in files:
        fp = open(f)
        file_no_ext = f.split('.')[0]
        rest, data = parse_metadata(fp)
        print(rest)
        print(data)
        html = markdown.markdown(''.join(rest))

        if file_no_ext == 'index':
            target = ''
        else:
            target = data.get('layout')
            os.makedirs(os.path.join('output', target))

        # Create file in output direction
        open(os.path.join('output', target, file_no_ext + '.html')).writelines(html)

    # Copy static directory
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


if __name__ == '__main__':
    main()