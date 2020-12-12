$(function(){
    $('.banner-section__slider').slick({
        dots: true,
        prevArrow: '<button class="banner-section__slider-btn banner-section__slider-btnprev">' +
            '<img src="images/arrow-left.svg" alt=""></button>',
        nextArrow: '<button class="banner-section__slider-btn banner-section__slider-btnnext">' +
            '<img src="images/arrow-right.svg" alt=""></button>',
        responsive: [
            {
                breakpoint: 969,
                settings: {
                    arrows: false,
                }
            }
        ]
    });

    $('.tab').on('click', function (e) {
        e.preventDefault();
        $($(this).siblings()).removeClass('tab--active');
        $($(this).closest('.tabs-wrapper').siblings().find('div')).removeClass('tabs-content--active');

        $(this).addClass('tab--active');
        $($(this).attr('href')).addClass('tabs-content--active');

        $('.product-slider').slick('setPosition');

    });


    $('.product-item__favorite').on('click',function () {
        $(this).toggleClass('product-item__favorite--active')
    });

    $('.catalog__filter-btngrid').on('click', function () {
        $(this).addClass('catalog__filter-button--active');
        $('.catalog__filter-btnline').removeClass('catalog__filter-button--active');
        $('.product-item__wrapper').removeClass('product-item__wrapper--list')
    });

    $('.catalog__filter-btnline').on('click', function () {
        $(this).addClass('catalog__filter-button--active');
        $('.catalog__filter-btngrid').removeClass('catalog__filter-button--active');
        $('.product-item__wrapper').addClass('product-item__wrapper--list')
    });

    $('.product-slider').slick({
        slidesToScroll: 1,
        slidesToShow: 4,
        prevArrow: '<button class="product-slider__slider-btn product-slider__slider-btnprev">' +
            '<img src="images/arrow-black-left.svg" alt=""></button>',
        nextArrow: '<button class="product-slider__slider-btn product-slider__slider-btnnext">' +
            '<img src="images/arrow-black-right.svg" alt=""></button>',
        responsive: [
            {
                breakpoint: 1301,
                settings: {
                    arrows: false,
                    dots: true,
                }
            },
            {
                breakpoint: 1201,
                settings: {
                    slidesToShow: 3,
                    arrows: false,
                    dots: true,
                }
            },
            {
                breakpoint: 870,
                settings: {
                    slidesToShow: 2,
                    arrows: false,
                    dots: true,
                }
            },
            {
                breakpoint: 590,
                settings: {
                    slidesToShow: 1,
                    arrows: false,
                    dots: true,
                }
            }
        ]
    });

    $('.filter-style').styler();

    $('.filter__item-drop, .filter-extra').on('click', function () {
        $(this).toggleClass('filter__item-drop--active');
        $(this).next().slideToggle('200');
    });

    $('.rate-yo').rateYo({
        ratedFill: "#1C62CD",
        spacing: "7px",
        normalFill: "#c4c4c4"
    });

    $('.menu__btn').on('click',function () {
        $('.menu-mobile__list').toggleClass('menu-mobile__list--active');
    });


    var $range = $(".js-range-slider");
    var $inputFrom = $(".js-input-from");
    var $inputTo = $(".js-input-to");
    var instance;
    var min = 0;
    var max = 1500000;
    var from = 100000;
    var to = 500000;

    $(".js-range-slider").ionRangeSlider({
        type: "double",
        grid: false,
        min: min,
        max: max,
        from: 100000,
        to: 500000,
        onStart: updateInputs,
        onChange: updateInputs,
    });

    instance = $range.data("ionRangeSlider");

    function updateInputs (data) {
        from = data.from;
        to = data.to;

        $inputFrom.prop("value", from);
        $inputTo.prop("value", to);
    }

    $inputFrom.on("input", function () {
        var val = $(this).prop("value");

        // validate
        if (val < min) {
            val = min;
        } else if (val > to) {
            val = to;
        }

        instance.update({
            from: val
        });
    });

    $inputTo.on("input", function () {
        var val = $(this).prop("value");

        // validate
        if (val < from) {
            val = from;
        } else if (val > max) {
            val = max;
        }

        instance.update({
            to: val
        });
    });

    $('.footer__topdrop').on('click', function () {
        $(this).toggleClass('footer__topdrop--active');
        $(this).next().toggleClass('footer-list--active');
    });

    $('.aside__btn').on('click', function () {
        $(this).next().slideToggle();
    });


});