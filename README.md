# statico
A simple and extensible static site generator in Python

## Install
With pip:
`pip install statico`


## Commands

* `statico -h | statico --help` - If you're stuck this is your friend
* `statico` - Create a new web site in the current directory.
* `statico [-a|--article] [title]` - Create a new article.
* `statico [-p|--page] [page_name]` - Create a new page.
* `statico [-g|--generate]` - Generate the web site in the 'output' directory.
* `statico [-P|--preview]` - Preview the web site (on 127.0.0.1:8000).
* `statico [-c|--clear]` - Clears the workspace.

## Web site structure
    content/            # The content directory (here you make your changes).
        articles/       
        index.md        # Do not change if you want the default look
        pages/
    output/             # Output directory to transfer to your web server
    settings.json       # Look inside, self-explanatory
    static/
        css/
        images/
        js/
    templates
        article.html
        base.html
        default.html
        includes/
            after_footer.html
            asides/
            footer.html
            header.html
            head.html
            navigation.html
        page.html
    
## License
MIT © [Ossama Edbali](http://oss6.github.io)