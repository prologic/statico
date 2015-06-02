var main = (function (paginate) {

    var init = function () {

        var pag = paginate.create({
            'selector': '.entry',
            'itemsOnPage': 10,
            'edges': 2,
            'displayedPages': 5
        });

    };

    return {
        'init': init
    }

})(paginate);

window.onload = main.init;