var main = (function (paginator, itemsPerPage) {

    var init = function () {
        paginator.create('.blog-index .entry', {
            'itemsPerPage': itemsPerPage
        });
    };

    return { 'init': init };

})(paginator, itemsPerPage);

window.onload = main.init;