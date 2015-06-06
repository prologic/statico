var main = (function (paginator, numberOfItems) {

    var init = function () {
        paginator.create('.blog-index .entry');
    };

    return { 'init': init };

})(paginator, numberOfItems);

window.onload = main.init;