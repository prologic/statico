var paginate = (function () {

    var _ = {};

    var createLinks = function (num) {

        var wrapper = document.createElement('div');
        wrapper.className = 'paginate-wrapper';

        // Set previous
        var prev = document.createElement('a');
        prev.setAttribute('href', '#paginate-prev');
        prev.innerHTML = 'Previous';
        wrapper.appendChild(prev);

        // Set numbers
        for (var i = 1; i <= num; i++) {
            var link = document.createElement('a');

            link.setAttribute('href', '#paginate-' + i);
            link.innerHTML = '' + i;
            wrapper.appendChild(link);
        }

        // Set next
        var next = document.createElement('a');
        next.setAttribute('href', '#paginate-next');
        next.innerHTML = 'Next';
        wrapper.appendChild(next);

        document.querySelector('.blog-index').appendChild(wrapper);
    };

    var createPages = function (num, perPage) {
        var page = document.createElement('div'),
            articles = document.querySelectorAll('.entry'),
            blogIndex = document.querySelector('.blog-index');

        page.className = 'paginate-page';

        for (var i = 0; i < num; i++) {
            if (i !== 0 && i % perPage === 0) {
                // Add page to blog index and change page
                blogIndex.appendChild(page);
                page = document.createElement('div');
                page.className = 'paginate-page';
                page.style.display = 'none';
            }

            page.appendChild(articles[i]);
        }

    };

    var goTo = function () {

    };

    _.create = function (opt) {
        var sel = opt.selector,
            perPage = opt.itemsOnPage,
            edges = opt.edges,
            displayedPages = opt.displayedPages,
            element = document.querySelectorAll(sel);

        var n = Math.ceil(element.length / perPage);
        createLinks(n);
        createPages(n, perPage);
    };

    return _;

})();