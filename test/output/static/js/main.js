var main = (function (paginate, numberOfItems) {

    var init = function () {

        var pag = paginate.create({
            'selector': '.entry',
            'itemsOnPage': numberOfItems,
            'edges': 2,
            'displayedPages': 5
        });

    };

    return {
        'init': init
    }

})(paginate, numberOfItems);

window.onload = main.init;