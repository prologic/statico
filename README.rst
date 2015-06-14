statico
=========
A simple and extensible static site generator in Python

Install
-------
:code:`pip install statico`


Commands
--------

* :code:`statico -h | statico --help` - If you're stuck this is your friend
* :code:`statico` - Create a new web site in the current directory.
* :code:`statico [-a|--article] [title]` - Create a new article.
* :code:`statico [-p|--page] [page_name]` - Create a new page.
* :code:`statico [-g|--generate]` - Generate the web site in the 'output' directory.
* :code:`statico [-P|--preview]` - Preview the web site (on 127.0.0.1:8000).
* :code:`statico [-c|--clear]` - Clears the workspace.

Web site structure
------------------
* content/
    - articles/       
    - index.md
    - pages/
* output/
* settings.json
* static/
    - css/
    - images/
    - js/
* templates/
    - article.html
    - base.html
    - default.html
    - includes/
        - after_footer.html
        - asides/
        - footer.html
        - header.html
        - head.html
        - navigation.html
    - page.html
    
License
-------
MIT © `Ossama Edbali
<http://oss6.github.io>`_.