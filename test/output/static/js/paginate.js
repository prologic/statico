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

    var goTo = function () {

    };

    _.Paginator = function (opt) {

        var sel = opt.selector,
            perPage = opt.itemsOnPage,
            edges = opt.edges,
            displayedPages = opt.displayedPages,
            element = document.querySelectorAll(sel);

        createLinks(Math.ceil(element.length / perPage));
    };

    _.create = function (opt) {
        return new _.Paginator(opt);
    };

    return _;

})();