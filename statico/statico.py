# -*- coding: utf-8 -*-

__version__ = '0.0.1'


import sys
import os
import re
import markdown
import json
import shutil
from pathlib import Path
from datetime import date, datetime
import argparse as ap
import jinja2 as jn
from github3 import GitHub, GitHubError

from six.moves import socketserver
from six.moves import SimpleHTTPServer

"""
statico --> creates structure directory in current directory
statico -g or --generate --> the output/public directory
statico -p or --page "page_title"
statico -a or --article "article_title"
statico -d or --deploy
"""


def _normalize_title(title):
    return re.sub(' +', ' ', title).lower().replace(' ', '-')


def _copy_directory(src, dest):
    try:
        shutil.copytree(src, dest)
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
    except OSError as e:
        print('Directory not copied. Error: %s' % e)


def _get_mtime(f):
    return f.stat().st_mtime


def _sorted_list_dir(path):
    p = Path(path)
    paths = [x for x in p.iterdir()]
    return sorted(paths, key=_get_mtime)


def _run_server():
    print('cd output')
    os.chdir('output')

    PORT = 8000
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)

    print("Serving at http://127.0.0.1:" + str(PORT) + ' ...')
    httpd.serve_forever()


def _validate_date(date_text):
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

            if _validate_date(value):
                data[attr] = datetime.strptime(
                    value, '%Y-%m-%d').strftime('%B %d, %Y')
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
    articles, recent_articles = get_articles(o.get('articles'))
    data['articles'] = articles
    data['content'] = html
    data['paginate'] = True
    if o.get('repos'):
        data['gh_repos'] = o.get('repos')
    data['site'] = o.get('settings')
    data['site']['recent_articles'] = recent_articles

    template = o.get('env').get_template('default.html')
    page = template.render(data)
    open(os.path.join('output', 'index.html'), 'w').write(page)


def clear_workspace():
    if os.path.isfile('settings.json'):
        os.remove('settings.json')

    if os.path.isfile('.statico'):
        os.remove('.statico')

    shutil.rmtree('content', True)
    shutil.rmtree('output', True)
    shutil.rmtree('static', True)
    shutil.rmtree('templates', True)
    shutil.rmtree('.templates', True)


def get_articles(f_articles, limit=5):
    articles = []
    recent_articles = []

    for idx, f_article in enumerate(f_articles):
        fp = f_article.open()  # open(f_article)
        rest, data = parse_metadata(fp)
        data['url'] = 'articles/' + f_article.name.split('.')[0] + '.html'
        if idx < limit:
            recent_articles.append(data)

        data['content'] = markdown.markdown(''.join(rest))
        articles.append(data)
        fp.close()

    return articles, recent_articles


def get_recent_articles(f_articles, limit=5):
    recent_articles = []

    for idx, f_article in enumerate(f_articles):
        if idx == limit:
            break

        fp = f_article.open() # open(f_article)
        _, data = parse_metadata(fp)
        data['url'] = 'articles/' + f_article.name.split('.')[0] + '.html'
        recent_articles.append(data)
        fp.close()

    return recent_articles


def create():
    path = os.path.abspath(__file__)
    dir_path = os.path.join(os.path.dirname(path), 'data')

    open('.statico', 'w')

    # Settings
    shutil.copy(os.path.join(dir_path, 'settings.json'), 'settings.json')
    print(' - settings.json [DONE]')

    # Static
    static_path = os.path.join(dir_path, 'static')
    _copy_directory(static_path, 'static')
    print(' - Static assets [DONE]')

    # Templates
    templates_path = os.path.join(dir_path, 'templates')
    _copy_directory(templates_path, 'templates')
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
    print('Page created successfully:', filename)


def new_article(title):
    # 2015/05/27/99-challenge/
    settings = json.load(open('settings.json'))
    filename = os.path.join('content', 'articles', date.today(
    ).isoformat() + '-' + _normalize_title(title) + '.md')

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
        '---\n'
    ])
    article.close()
    print('Article created successfully:', filename)


def generate():
    settings = json.load(open('settings.json'))

    # Get all filenames
    pages = _sorted_list_dir(os.path.join('content', 'pages'))
    articles = _sorted_list_dir(os.path.join('content', 'articles'))

    files = pages + articles

    # BEGIN: Parse files
    loader = jn.FileSystemLoader(os.path.join(os.getcwd(), 'templates'))
    env = jn.Environment(loader=loader)

    # Add GitHub repos
    repos = None
    if settings.get('github_user') and settings.get('github_repo_count'):
        try:
            gh = GitHub()
            repo_limit_maybe = settings.get('github_repo_count')
            repo_limit = int(repo_limit_maybe) if repo_limit_maybe else 5
            repos = list(map(lambda r: r.repository, list(gh.search_repositories(
                'user:' + settings['github_user'], sort='updated'))[:repo_limit]))
        except GitHubError:
            repos = None
            print(
                'GitHub search repositories error. Check "github_user" in settings.json')

    print(' - Parsing articles and pages')
    for f in files:
        fp = f.open()
        file_no_ext = f.name.split('.')[0]
        rest, data = parse_metadata(fp)
        html = markdown.markdown(''.join(rest))

        target = data.get('layout') + 's'
        target_dir = os.path.join('output', target)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        # Create file in output direction
        layout = data.get('layout')
        template = env.get_template(layout + '.html')

        data['content'] = html
        data['url'] = target + '/' + file_no_ext + '.html'
        data['site'] = settings
        data['site']['recent_articles'] = get_recent_articles(articles)
        if repos:
            data['gh_repos'] = repos
        page = template.render(data)  # Date and other things

        file_out = open(
            os.path.join('output', target, file_no_ext + '.html'), 'w')
        file_out.write(page)
        file_out.close()

    # Copy index
    print(' - Parsing index page')
    parse_index(os.path.join('content', 'index.md'), {
        'env': env,
        'settings': settings,
        'articles': articles,
        'repos': repos
    })

    # END: Parse files

    # Copy static directory
    print(' - Generating static directory')
    static = os.path.join('output', 'static')
    if os.path.exists(static):
        shutil.rmtree(static)
    _copy_directory('static', os.path.join('output', 'static'))


def run():  # noqa
    # XXX: Refactor this.
    # XXX: C901: This is too complex.

    # Create directory structure
    if len(sys.argv) == 1:
        print('Creating site...')
        create()
        return

    parser = ap.ArgumentParser()
    parser.add_argument('-g', '--generate', help='Generate the output directory to upload to the web server',
                        action='store_true')
    parser.add_argument('-p', '--page', help='Create a page', type=str)
    parser.add_argument(
        '-a', '--article', help='Create an article', type=str)
    parser.add_argument(
        '-c', '--clear', help='Clear directory', action='store_true')
    parser.add_argument(
        '-P', '--preview', help='Preview your site', action='store_true')
    args = parser.parse_args()

    if not os.path.isfile('.statico'):
        print(
            'This is not a "statico" directory. Run "statico" to mark it as so.')
        return

    if args.generate:
        print('Generating site...')
        generate()
        print(
            'Head to "output" to view your generated site.\n'
            'Now you are ready to upload your site (next release will support GH pages deployment).\n'
            'Type "statico --preview" to get a preview of your site.'
        )
    elif args.page:
        new_page(args.page)
    elif args.article:
        new_article(args.article)
    elif args.clear:
        if input('Are you sure you want to clear the workspace? [y/n] ') == 'y':
            clear_workspace()
    elif args.preview:
        _run_server()
