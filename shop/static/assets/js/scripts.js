'use strict';
(function ($) {

    var px = ''; //'rt--'

    /**
     * Функция для вывода набора jQuery по селектору, к селектору добавляются
     * префиксы
     *
     * @param {string} selector Принимает селектор для формирования набора
     * @return {jQuery} Возвращает новый jQuery набор по выбранным селекторам
     */
    function $x(selector) {
        return $(x(selector));
    }

    /**
     * Функция для автоматического добавления префиксов к селекторы
     *
     * @param {string} selector Принимает селектор для формирования набора
     * @return {string} Возвращает новый jQuery набор по выбранным селекторам
     */
    function x(selector) {
        var arraySelectors = selector.split('.'),
            firstNotClass = !!arraySelectors[0];

        selector = '';

        for (var i = 0; i < arraySelectors.length; i++) {
            if (!i) {
                if (firstNotClass) selector += arraySelectors[i];
                continue;
            }
            selector += '.' + px + arraySelectors[i];
        }

        return selector;
    }

// Прелоадер
    $(function () {

var menu = function(){
    var $menuMain = $('.menu_main');
    $menuMain.css('position', 'absolute');
    var menuHeight = $('.menu_main').outerHeight();
    $menuMain.css('position', 'static');
    var $body = $('body');
    function refresh(){
        if (window.innerWidth<991) {
            // $('.menuModal').each(function(){
            //     var $this = $(this);
            //     setTimeout(function(){
            //         if ($this.attr('height') > 0) {
            //             $this.css('height', 0);
            //         }
            //     }, 100);
            // });
            $('.menuModal').css('height', 0);
            $menuMain.css('position', 'absolute');
            menuHeight = $('.menu_main').outerHeight();
            $menuMain.css('position', 'static');
        } else {
            menuHeight = $('.menu_main').outerHeight();
            $('.menuModal')
                .removeClass("menuModal_OPEN")
                .css('height', '');
            $body.removeClass("Site_menuOPEN");
            $('.menuTrigger').removeClass("menuTrigger_OPEN");
        }
    }

    return {
        init: function(){
            if (window.innerWidth<991) {
            $(".menuModal").css('height', menuHeight);
            // Меню для мобильных
                $(".menuTrigger").each(function () {
                    $($(this).attr('href')).css('height', 0);
                });
            }

            $(".menuTrigger").click(function(e){
                var $this = $(this),
                    href = $this.attr("href");

                if ($this.hasClass("menuTrigger_OPEN")) {
                    $body.removeClass("Site_menuOPEN");
                    $(href)
                        .removeClass("menuModal_OPEN")
                        .css('height', 0);
                    $this.removeClass("menuTrigger_OPEN");
                }else{
                    $body.addClass("Site_menuOPEN");
                    $(href)
                        .addClass("menuModal_OPEN")
                        .css('height', menuHeight);
                    $this.addClass("menuTrigger_OPEN");
                }
                e.preventDefault();
            });
            $(window).on('resize', refresh);
        }
    };
};
menu().init();
var search = function(){
    var $searchLink = $('.Header-searchLink');
    return {
        init: function(){
            $searchLink.each(function(){
                var $this = $(this);
                $this.on('click', function(){
                    var $thisClick = $(this);
                    $thisClick.next('.Header-search').toggleClass('Header-search_open');
                });
            });
        }
    };
};
search().init();
var form = function(){
    var $selectList = $('.selectList');
    var $input = $('.form-input, .form-textarea');
    var $form = $('.form');
    var $select = $('.form-select');
    return {
        init: function(){
            $selectList.each(function(){
                var $this = $(this),
                    $radio= $this.find('input[type="radio"]');
                function changeTitle($block, $element) {
                    $block.find('.selectList-title')
                        .text( $element.closest('.selectList-item')
                            .find('.selectList-text').text())
                }
                changeTitle($this, $radio.filter('[checked="checked"]'));
                $radio.on('change', function(){
                    changeTitle($this, $(this));
                });
                
            });
            $(document).on('click', function(e){
                var $this = $(e.target);
                if (!$this.hasClass('selectList-header') ) {
                    $this = $(e.target).closest('.selectList-header');
                }
                if ( $this.length ){
                    e.preventDefault();
                    $this.closest('.selectList').toggleClass('selectList_OPEN');
                } else {
                    $('.selectList').removeClass('selectList_OPEN');
                }
            });

            $('#id_address').on('input', function() {
                var address_text = $(this).val();
                $('#id_info_address').html(address_text)
            });

            $('#id_city').on('input', function() {
                var city_text = $(this).val();
                $('#id_info_city').html(city_text)
            });

             $('input[name=delivery_type]').on('change', function() {
                if (this.value == '1') {
                    var delivery = JSON.parse(document.getElementById('price_usual').textContent);
                    $('#info_delivery').html('Обычная доставка')
                }
                else if (this.value == '2') {
                    var delivery = JSON.parse(document.getElementById('price_express').textContent);
                    $('#info_delivery').html('Экспресс доставка')
                }
                var total_cart = JSON.parse(document.getElementById('total_price').textContent);
                var str = 'Доставка: ' + delivery + ' руб.';
                var total = parseFloat(total_cart) + parseFloat(delivery)
                $('#block_delivery').html(str)
                $('#total_value').html(total.toString() + ' руб.')
            });

            $('input[name=payment_type]').on('change', function() {
                if (this.value == '1') {
                    $('#info_payment').html('Онлайн картой')
                    $('#generate_btn').hide()
                }
                else if (this.value == '2') {
                    $('#info_payment').html('Онлайн со случайного чужого счета')
                    $('#generate_btn').removeClass('btn_disabled')
                    $('#generate_btn').show()
                }
            });
            
            // Валидация полей
            $input.on('blur input', function(){
                function validateEmail(email)
                {
                  return email.match(
                    /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
                  );
                };

                function validatePassword(password)
                {
                  return password.match(/^.*(?=.{8,})(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!#$%&?]).*$/);
                };

                function validatePhone(number)
                {
                    return number.match(/^\d{10}$/);
                };

                function validateRepeatPassword(repeat)
                {
                    var value = '';
                    if ($('#id_password1').length){
                        value = $('#id_password1').val();
                    } else if ($('#id_new_password1').length){
                        value = $('#id_new_password1').val();
                    }
                    return repeat == value;
                };

                var $this = $(this),
                    validate = $this.data('validate'),
                    message = '',
                    error = false;
                if (validate){
                    validate = validate.split(' ');
                    validate.forEach(function(v){
                        switch (v){
                            case 'requireMail':
                                if  (!$this.val()) {
                                    message = 'Это поле обязательно для заполнения. ';
                                    error = true;
                                } else if (!validateEmail($this.val())) {
                                    message = 'e-mail неправильный ';
                                    error = true;
                                }
                                break;
                            case 'requireCard':
                                if  (!$this.val()) {
                                    message = 'Это поле обязательно для заполнения. ';
                                    error = true;
                                } else if ($this.val().length < 8) {
                                    message = 'Некорректный номер карты';
                                    error = true;
                                }
                                break;
                            case 'requirePhone':
                                if  (!$this.val()) {
                                    message = 'Это поле обязательно для заполнения. ';
                                    error = true;
                                } else if (!validatePhone($this.val())) {
                                    message = 'Номер телефона неправильный ';
                                    error = true;
                                }
                                break;
                            case 'requirePassword':
                                if  (!$this.val()) {
                                    message = 'Это поле обязательно для заполнения. ';
                                    error = true;
                                } else if (!validatePassword($this.val())) {
                                    message = 'Password must contain 8 characters and at least one number, one letter, one letter in Upper case and one unique character such as !#$%&?';
                                    error = true;
                                }
                                break;
                            case 'requireRepeatPassword':
                                if  (!$this.val()) {
                                    message = 'Это поле обязательно для заполнения. ';
                                    error = true;
                                } else if (!validateRepeatPassword($this.val())) {
                                    message = 'Пароли не совпадают';
                                    error = true;
                                }
                                break;
                            case 'require':
                                if (!$this.val()) {
                                    message = 'Это поле обязательно для заполнения. ';
                                    error = true;
                                }
                                break;
                            case 'pay':
                                var val = $this.val().replace(' ', '');
                                val = val + '';
                                if (parseFloat(val)%2!==0) {
                                    message += 'Номер должен быть четным. ';
                                    error = true;
                                }
                                break;
                        }
                        if (error) {
                            $this.next('.form-error').remove();
                            if ($this.hasClass('form-input')){
                                $this.addClass('form-input_error');
                            }
                            if ($this.hasClass('form-textarea')){
                                $this.addClass('form-textarea_error');
                            }
                            if (!$this.next('.form-error').length){
                                $this.after('<div class="form-error">'+message+'</div>');
                            }
                            $this.data('errorinput', true);
                        } else {
                            $this.next('.form-error').remove();
                            $this.removeClass('form-input_error');
                            $this.removeClass('form-textarea_error');
                            $this.data('errorinput', false);
                        }
                        message = '';

                    });
                }
            });
            $form.on('submit', function(e){
                var $this = $(this),
                    $validate = $this.find('[data-validate]');

                $validate.each(function(){
                    var $this = $(this);
                    $this.trigger('blur');
                    if ($this.data('errorinput')){
                        e.preventDefault();
                    }
                });
            });
            $select.wrap('<div class="form-selectWrap"></div>');
            $('[data-mask]').each(function(){
                var $this = $(this);
                $this.mask($this.data('mask'), {placeholder:'x'});
            });
        }
    };
};
form().init();
let modal = function(){
    let $trigger = $('.trigger'),
        $body = $('body'),
        $modal = $('.modal');

    let template = {
        img: (img) => '<div class="modal">' +
                        '<div class="modal-window">' +
                            '<a href="#" class="modal-close fa fa-close"></a>' +
                            '<img src="' + img + '" />' +
                        '</div>' +
                    '</div>'
    };

    return {
        refresh: function(){
        },
        init: function(){
            function modalClick(e) {

                let $target = $(e.target),
                    $this = $(this);

                if ( $target.hasClass('modal-close') ) {
                    $target = $this;
                }

                if ( $this.is($target)) {
                    e.preventDefault();
                    $body.removeClass("Site_modalOPEN");
                    $this.removeClass("modal_OPEN");
                    $('[href="' + $this.attr('id') + '"]').removeClass("trigger_OPEN");
                }
            }

            $trigger.click(function(e){
                e.preventDefault();

                let $this = $(this),
                    href = $this.attr("href"),
                    $href = $(href);

                if ( !$(href).length ) {
                    let $img = $( template.img( $this.data('src') ) );
                    $img.attr('id', href.replace('#','') );
                    $body.append( $img );
                    $href = $(href);
                    $modal = $modal.add( $href );
                    $href.click(modalClick);
                }

                $href.addClass("modal_OPEN");
                $body.addClass("Site_modalOPEN");
                $this.addClass("trigger_OPEN");
            });

            $modal.click(modalClick);

        }
    };
};

modal().init();
var range = function(){
    return {
        init: function(){
            var $range = $('.range'),
                $line = $range.find('.range-line');
            
            $line.ionRangeSlider({
                onStart: function(data){
                    $('.rangePrice').text(
                        'Р' + data.from + ' - Р' + data.to
                    )
                },
                onChange: function(data){
                    $('.rangePrice').text(
                        'Р' + data.from + ' - Р' + data.to
                    )
                }
            });
        }
    };
};
range().init();
var table = function(){
    return {
        init: function(){
        }
    };
};
table().init();
//END
var PanelAdd = function(){
    return {
        init: function(){
        }
    };
};
PanelAdd().init();
var ControlPanel = function(){
    return {
        init: function(){
        }
    };
};
ControlPanel().init();
var Slider = function(){
    let $block = $('.Slider').not('.Slider_carousel'),
        $container = $block.children('.Slider-box'),
        $carousel = $('.Slider_carousel'),
        $containerCar = $carousel.children('.Slider-box');
    return {
        init: function(){
            $container.each(function(){
                var $this = $(this);
                var $navigate = $this.closest($block).find('.Slider-navigate');
                $this.slick({
                    dots: true,
                    arrows: true,
                    autoplay: true,
                    appendArrows: $navigate,
                    appendDots: $navigate,
                    autoplaySpeed: 3000
                });
            });
            $containerCar.each(function(){
                var $this = $(this);
                var $navigate = $this.closest($carousel).find('.Slider-navigate');
                if($this.hasClass('Cards_hz')){
                    $this.slick({
                        appendArrows: $navigate,
                        appendDots: $navigate,
                        dots: true,
                        arrows: true,
                        slidesToShow: 3,
                        slidesToScroll: 2,
                        responsive: [
                            {
                                breakpoint: 1600,
                                settings: {
                                    slidesToShow: 2,
                                    slidesToScroll: 2
                                }
                            },
                            {
                                breakpoint: 900,
                                settings: {
                                    slidesToShow: 1,
                                    slidesToScroll: 1
                                }
                            }
                        ]
                    });
    
                } else {
                    $this.slick({
                        appendArrows: $navigate,
                        appendDots: $navigate,
                        dots: true,
                        arrows: true,
                        slidesToShow: 4,
                        slidesToScroll: 2,
                        responsive: [
                            {
                                breakpoint: 1600,
                                settings: {
                                    slidesToShow: 3,
                                    slidesToScroll: 2
                                }
                            },
                            {
                                breakpoint: 1230,
                                settings: {
                                    slidesToShow: 2,
                                    slidesToScroll: 2
                                }
                            },
                            {
                                breakpoint: 570,
                                settings: {
                                    slidesToShow: 1,
                                    slidesToScroll: 1
                                }
                            }
                        ]
                    });
                
                }
            });

        }
    };
};
Slider().init();
var CartBlock = function(){
    return {
        init: function(){
        }
    };
};
CartBlock().init();
var CategoriesButton = function(){
    return {
        init: function(){
            $(document).on('click', function(e){
                var $this = $(e.target);
                if ($this.is('a.CategoriesButton-arrow') && $this.closest('.CategoriesButton-link').length){
                    e.preventDefault();
                    if($this.next('.CategoriesButton-submenu').is(':visible')) {
                        $('.CategoriesButton .CategoriesButton-submenu').hide(0);
                    } else {
                        $('.CategoriesButton .CategoriesButton-submenu').hide(0);
                        $this.next('.CategoriesButton-submenu').show(0);
                    }
                }
                else {
                    if (!$this.hasClass('CategoriesButton-title') ) {
                        $this = $(e.target).closest('.CategoriesButton-title');
                    }
                    if ( $this.length ){
                        e.preventDefault();
                        $this.closest('.CategoriesButton').toggleClass('CategoriesButton_OPEN');
                    } else {
                        $('.CategoriesButton').removeClass('CategoriesButton_OPEN');
                        $('.CategoriesButton .CategoriesButton-submenu').hide(0);
                    }
                }
            });
        }
    };
};
CategoriesButton().init();
var Middle = function(){
    return {
        init: function(){
        }
    };
};
Middle().init();
var Section = function(){
    return {
        init: function(){
        }
    };
};
Section().init();
var BannersHome = function(){
    return {
        init: function(){
        }
    };
};
BannersHome().init();
var Card = function(){
    return {
        init: function(){
        }
    };
};
Card().init();
var CountDown = function(){
    var $blocks = $('.CountDown');
    function getTimeRemaining(endtime){
        endtime = endtime.split(' ');
        var date = endtime[0].split('.');
        var time = endtime[1].split(':');
        var t = new Date(date[2], date[1] - 1, date[0] - 1, time[0], time[1]) - new Date();
        var seconds = Math.floor( (t/1000) % 60 );
        var minutes = Math.floor( (t/1000/60) % 60 );
        var hours = Math.floor( (t/(1000*60*60)) % 24 );
        var days = Math.floor( t/(1000*60*60*24) );
        return {
            'total': t,
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds
        };
    }
    function initializeClock(clock, endtime){
        function updateClock(){
            var t = getTimeRemaining(endtime);
            clock.find('.CountDown-days').text(t.days);
            clock.find('.CountDown-hours').text(t.hours);
            clock.find('.CountDown-minutes').text(t.minutes);
            clock.find('.CountDown-secs').text(t.seconds);
            if(t.total<=0){
                clearInterval(timeinterval);
            }
        }
        updateClock();
        var timeinterval = setInterval(updateClock,1000);
    }
    return {
        init: function(){
            $blocks.each(function(){
                var $this = $(this);
                initializeClock($this, $this.data('date'));
            });
        }
    };
};
CountDown().init();
var Rating = function(){
    return {
        init: function(){
            $('.Rating_input:not(.Rating_inputClick)').on('click', function(){
                $(this).addClass('Rating_inputClick');
            });
        }
    };
};
Rating().init();
var Choice = function(){
    return {
        init: function(){
        }
    };
};
Choice().init();
var Map = function(){
    return {
        init: function(){
        }
    };
};
Map().init();
var Pagination = function(){
    return {
        init: function(){
        }
    };
};
Pagination().init();
var Sort = function(){
    return {
        init: function(){
        }
    };
};
Sort().init();
var Compare = function(){
    var $compare = $('.Compare');
    var $products = $compare.find('.Compare-products');
    var $checkDifferent = $('.Compare-checkDifferent input');
    return {
        init: function(){
            $products.on('scroll', function(){
                var $this = $(this);
                $products.each(function(){
                    $(this)[0].scrollLeft = $this[0].scrollLeft;
                })
            });
            $checkDifferent.on('change', function(){
                var $this = $(this),
                    $rowsHide = $this.closest($compare).find('.Compare-row_hide');
                if ($this.prop('checked')){
                    $rowsHide.hide(0);
                } else {
                    $rowsHide.show(0);
                }
            });
            $checkDifferent.trigger('change');
        }
    };
};
Compare().init();
var Sort = function(){
    return {
        init: function(){
        }
    };
};
Sort().init();
var NavigateProfile = function(){
    return {
        init: function(){
        }
    };
};
NavigateProfile().init();
var Profile = function(){
    var $avatar = $('.Profile-avatar');
    return {
        init: function(){

            var $avatarfile = $avatar.find('.Profile-file');
            if (document.getElementById('user_avatar')) {
                var loadedAvatar = JSON.parse(document.getElementById('user_avatar').textContent);
            }


            if (loadedAvatar) {
                $('.Profile-img img').attr('src', loadedAvatar);
                $('.Profile-avatar').removeClass('Profile-avatar_noimg');
                $('.Profile-avatar').next('.form-error').remove();
                $('.Profile-avatar').find('input[type="file"]').data('errorinput', false);
            }

            function readURL(input) {

                if (input.files && input.files[0]) {
                    var file = input.files[0],
                        ext = 'неизвестно';
                    ext = file.name.split('.').pop();
                    if ((ext==='png' || ext==='jpg' || ext==='gif') && (file.size <= 2 * 1024 * 1024)){
                        var reader = new FileReader();

                         reader.onload = function(e) {
                            $(input).closest($avatar).find('.Profile-img img').attr('src', e.target.result);
                        }

                        reader.readAsDataURL(file);
                        return true;
                    }
                    return false;
                }
            }


            $avatarfile.change(function() {
                var $thisAvatar = $(this).closest($avatar);
                if(readURL(this)){
                    $thisAvatar.removeClass('Profile-avatar_noimg');
                    $thisAvatar.next('.form-error').remove();
                    $thisAvatar.find('input[type="file"]').data('errorinput', false);
                } else {
                    if (!$thisAvatar.next('.form-error').length){
                        $thisAvatar.find('input[type="file"]').data('errorinput', true);
                        $thisAvatar.after('<div class="form-error">Для загрузки допустимы лишь картинки с расширением png, jpg, gif и размером не более 2MB</div>');
                    }
                };
            });
        }
    };
};
Profile().init();
var Cart = function(){
    return {
        init: function(){
        }
    };
};

$(document).ready(function() {

    // отслеживаем событие отправки формы
    $('*[data-validate="requireMail"]').keyup(function () {
        if  ($(this).val().length > 3) {
            // создаем AJAX-вызов
            $.ajax({
                data: $(this).serialize(), // получаем данные формы
                url: JSON.parse(document.getElementById('validate_email_url').textContent),
                // если успешно, то
                success: function (response) {
                    if (response.is_taken == true) {
                        $('#id_email').removeClass('is-valid').addClass('is-invalid');
                        $('#id_email').next('.form-error').remove();
                        if (!$("#emailError").length){
                          $('#id_email').after('<div class="invalid-feedback d-block" id="emailError">Пользователь с таким email уже зарегистрирован</div>')
                          }
                    }
                    else {
                        $('#id_email').removeClass('is-invalid').addClass('is-valid');
                        $('#emailError').remove();
                    }
                },
                // если ошибка, то
                error: function (response) {
                    // предупредим об ошибке
                    console.log(response.responseJSON.errors)
                }
            });
            return false;
        }
    });

    $('*[data-validate="requirePhone"]').keyup(function () {
        if  ($(this).val()) {
            // создаем AJAX-вызов
            $.ajax({
                data: $(this).serialize(), // получаем данные формы
                url: JSON.parse(document.getElementById('validate_phone_url').textContent),
                // если успешно, то
                success: function (response) {
                    if (response.is_taken == true) {
                        $('#id_phoneNumber').removeClass('is-valid').addClass('is-invalid');
                        $('#id_phoneNumber').next('.form-error').remove();
                        if (!$("#phoneError").length){
                          $('#id_phoneNumber').after('<div class="invalid-feedback d-block" id="phoneError">Пользователь с таким номером уже зарегистрирован</div>')
                        }
                    }
                    else {
                        $('#id_phoneNumber').removeClass('is-invalid').addClass('is-valid');
                        $('#phoneError').remove();
                    }
                },
                // если ошибка, то
                error: function (response) {
                    // предупредим об ошибке
                    console.log(response.responseJSON.errors)
                }
            });
            return false;
        }
    });


    $("#generate_btn").click(function() {
        var min = 10000000;
        var max = 99999999;
        var result = Math.floor(Math.random() * (max - min + 1)) + min;
        $('#id_card_number').val(result);
    });

    // Log in button
    if ($('#login_modal_url').length) {
        $("#login-btn").modalForm({
         formURL: JSON.parse(document.getElementById('login_modal_url').textContent)
        });
    }

    $('#id_phoneNumber').inputmask({ mask: "+7(999)99-99-999", removeMaskOnSubmit: true, autoUnmask: true});

    //card mask
    $('#id_card_number').inputmask({ mask: "9999-9999", removeMaskOnSubmit: true, autoUnmask: true, greedy: false});

    //email mask
    $('#id_email, #id_username').inputmask({
      mask: "*{1,20}[.*{1,20}][.*{1,20}][.*{1,20}]@*{1,20}[.*{2,6}][.*{1,2}]",
      greedy: false,
      onBeforePaste: function (pastedValue, opts) {
        pastedValue = pastedValue.toLowerCase();
        return pastedValue.replace("mailto:", "");
      },
      definitions: {
        '*': {
          validator: "[0-9A-Za-z!#$%&'*+/=?^_`{|}~\-]",
          casing: "lower"
        }
      }
    });


    if ($('.Comment').not(":visible").length > 0) {
        $(".btn-more").show()
        $(".btn-more").on('click', function(e){
            $('.Comment').not(":visible").each(function (index, element) {
                $(element).show()
                $(element).css('display', 'flex');
                if (index == 1) {
                    return false
                }
        });
        if ($('.Comment').not(":visible").length == 0) {
                    $(".btn-more").hide()
                }
    });
    } else {
        $(".btn-more").hide()
    }



    $("#filter_form").submit(function() {
      $(this).find(":input").filter(function(){ return !this.value; }).attr("disabled", "disabled");
      return true; // ensure form still submits
    });

    if ($('#generate_btn').length > 0) {
        if ($('input[name="payment_type"]:checked').val() == 2) {
            $('#generate_btn').removeClass('btn_disabled')
            $('#generate_btn').show()
        }
    }

    if ($('#payment_code').length > 0) {
        var code = JSON.parse(document.getElementById('payment_code').textContent);
        if (code != 1 || $('#pay_btn').is(":hidden")) {
            setTimeout(function() {
                var data = {};
                var url = JSON.parse(document.getElementById('url_payment').textContent);
                var order_id = JSON.parse(document.getElementById('order_id').textContent);
                data.order_id = order_id;
                $.ajax({
                url: url,
                type: 'GET',
                data: data,
                cache: true,
                success: function (response){
                    if (response.status) {
                        $('#error_type').html('Оплата не прошла');
                        $('#error_info').html(response.status);
                        if (response.code != 1){
                            $('#pay_btn').removeClass('btn_disabled');
                            $('#pay_btn').show();
                        }
                    }
                    if (response.code == 1){
                            $('.Order-info_error').hide();
                            $('#status').html('Оплачен');
                    }
                },
                // если ошибка, то
                error: function (response) {
                    // предупредим об ошибке
                    console.log(response.responseJSON.errors)
                }
                });
            }, 2000);
        };
    };

    function submit_cart(e) {
        e.preventDefault();
        var data = {};
        if ($('#id_quantity').length) {
            var value = parseFloat($('#id_quantity').val());
        } else {
            var value = 1
        }
        data.update = "False";
        data.quantity = value;
        var csrf_token = $(this).siblings('[name="csrfmiddlewaretoken"]').val();
        var url = $(this).parents('form').attr('action');
        data['csrfmiddlewaretoken'] = csrf_token
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function (data){
                toastr.options.positionClass = "toast-bottom-right";
                toastr.success('Товар добавлен в корзину')
                var data = {};
                data['csrfmiddlewaretoken'] = csrf_token
                $.ajax({
                    data: data,
                    url: JSON.parse(document.getElementById('cart_url').textContent),
                    success: function (response) {
                      $('.CartBlock-amount').html(response.total_len)
                      $('.CartBlock-price').html(response.total + 'Р')
                      },
                    })
            }
        });
    };
    $("#btn-submit").on("click", submit_cart);
    $("a.Card-btn").on("click", submit_cart);
});

Cart().init();
var Amount = function(){
    var $amount = $('.Amount');
    var $add = $('.Amount-add');
    var $input = $('.Amount-input');
    var $remove = $('.Amount-remove');
    return {
        init: function(){
            $add.on('click', function(e){
                e.preventDefault();
                var $inputThis = $(this).siblings($input).filter($input);
                var value = parseFloat($inputThis.val());
                $inputThis.val(value + 1);
                $input.trigger('input');
            });
            $remove.on('click', function(e){
                e.preventDefault();
                var $inputThis = $(this).siblings($input).filter($input);
                var value = parseFloat($inputThis.val());
                $inputThis.val(value>1?value - 1:1);
                $input.trigger('input');
            });
            $input.on('input', function(e){
                e.preventDefault();
                var data = {};
                var $inputThis = $(this)
                var product_id = $inputThis.siblings('#product_id').val();
                var value = parseFloat($inputThis.val());
                data.update = "True";
                data.quantity = value
                var url = $('#cart_form').attr('action');
                var csrf_token = $('#cart_form [name="csrfmiddlewaretoken"]').val();
                data['csrfmiddlewaretoken'] = csrf_token
                if (value){
                    $.ajax({
                    url: url,
                    type: 'POST',
                    data: data,
                    cache: true,
                    success: function (data){
                        $.ajax({
                        data: {product: product_id},
                        url: JSON.parse(document.getElementById('cart_url').textContent),
                        success: function (response) {
                          $inputThis.closest('.form').find('#product-price').html(response.total_item)
                          $('.Cart-total').find('.Cart-price').html(response.total)
                          $('.CartBlock-amount').html(response.total_len)
                          $('.CartBlock-price').html(response.total + 'Р')
                          },
                        })
                    }
                    })

                }
            });
        }
    };
};
Amount().init();
var Order = function(){
    var $next = $('.Order-next'),
        $blocks = $('.Order-block'),
        $navigate = $('.Order-navigate');
    return {
        init: function(){
            $next.add($navigate.find('.menu-link')).on('click', function(e){
                e.preventDefault();
                var $this = $(this),
                    href = $this.attr('href'),
                    error = false,
                    $validate = $this.closest($blocks).find('[data-validate]')
                if ($(e.target).is('.Order-next')) {
                    $validate.each(function(){
                        var $this = $(this);
                        $this.trigger('blur');
                        if ($this.data('errorinput')){
                            error = true
                        }
                    });
                }
                if ( error===false && ($(e.target).is('.Order-next') ||
                    $blocks.index($(href)) < $blocks.index($blocks.filter('.Order-block_OPEN')))
                ) {
                    $blocks.removeClass('Order-block_OPEN');
                    $(href).addClass('Order-block_OPEN');
                    $navigate.find('.menu-item').removeClass('menu-item_ACTIVE');
                    $navigate.find('.menu-link[href="' + href + '"]')
                        .closest('.menu-item')
                        .addClass('menu-item_ACTIVE');
                }
                
            });
        }
    };
};
Order().init();
var Account = function(){
    return {
        init: function(){
        }
    };
};
Account().init();
var Payment = function(){
    return {
        init: function(){
            $('.Payment-generate').on('click', function(e){
                var $this = $(this),
                    $bill = $this.closest('.Payment').find('.Payment-bill'),
                    billNumber = '';
                e.preventDefault();
                do {
                    billNumber = Math.random() + '';
                    billNumber = billNumber.slice(-9, -1);
                } while(parseFloat(billNumber)%2!==0);
                billNumber = billNumber.slice(0, 4) + ' ' + billNumber.slice(4, 8);
                $bill.val(billNumber);
            });
            $('.Payment-pay .btn').on('click', function(e){
                var $this = $(this),
                    $validate = $this.closest('.form').find('[data-validate]');
    
                $validate.each(function(){
                    var $this = $(this);
                    $this.trigger('blur');
                    if ($this.data('errorinput')){
                        e.preventDefault();
                    }
                });
            });
        }
    };
};
Payment().init();
var Tabs = function(){
    var $tabs = $('.Tabs');
    var $tabsLink = $('.Tabs-link');
    var $tabsBlock = $('.Tabs-block');
    return {
        init: function(){
            // var $steps = $('.Tabs_steps');
            // var $step = $steps.find($tabsLink).not($steps.find($tabs).find($tabsLink));
            // var $blocks = $steps.find($tabsBlock).not($steps.find($tabs).find($tabsBlock));
            // $blocks.hide(0);
            // var href = $step.eq(0).attr('href');
            // var $active = $(href);
            // var $links= $step.add($step.siblings($tabsLink));
            // $links.removeClass('Tabs-link_ACTIVE');
            // $step.eq(0).addClass('Tabs-link_ACTIVE');
            // $active.show(0);

            $tabsLink.on('click', function(e){
                var $this = $(this);
                var href = $this.attr('href');
                if (href[0]==="#"){
                    e.preventDefault();
                    var $parent = $this.closest($tabs);
                    if ($parent.hasClass('Tabs_steps')) {
                    } else {
                        var $blocks = $parent.find($tabsBlock).not($parent.find($tabs).find($tabsBlock));
                        var $links= $this.add($this.siblings($tabsLink));
                        var $active = $(href);
                        $links.removeClass('Tabs-link_ACTIVE');
                        $this.addClass('Tabs-link_ACTIVE');
                        $blocks.hide(0);
                        $active.show(0);
                    }
                }

            });
            $('.TabsLink').on('click', function(e){
                var $this = $(this);
                var href = $this.attr('href');
                var $active = $(href);
                var $parent = $active.closest($tabs);
                if ($parent.hasClass('Tabs_steps')) {
                } else {
                    var $blocks = $parent.find($tabsBlock).not($parent.find($tabs).find($tabsBlock));
                    var $link = $('.Tabs-link[href="' + href + '"]');
                    var $links= $link.add($link.siblings($tabsLink));
                    $links.removeClass('Tabs-link_ACTIVE');
                    $link.addClass('Tabs-link_ACTIVE');
                    $blocks.hide(0);
                    $active.show(0);
                }

            });
            $tabs.each(function(){
                $(this).find($tabsLink).eq(0).trigger('click');
            });
        }
    };
};
Tabs().init();
// setTimeout(function(){
//     $('body').css('opacity', '1');
// }, 100);
var ProductCard = function(){
    var $picts = $('.ProductCard-pict');
    var $photo = $('.ProductCard-photo');
    return {
        init: function(){
            $picts.on('click', function(e){
                e.preventDefault();
                var $this = $(this);
                var href = $this.attr('href');
                $photo.empty();
                $photo.append('<img src="'+ href +'" />');
                $picts.removeClass('ProductCard-pict_ACTIVE');
                $this.addClass('ProductCard-pict_ACTIVE');
            });
        }
    };
};
ProductCard().init();
var Comments = function(){
    return {
        init: function(){
            $('[data-action="comments-show"]').on('click', function(e){
                console.log(123);
                e.preventDefault();
                var $this = $(this),
                    text = $this.data('text-alt'),
                    $comments = $this.prev('.Comments').find('.Comments-wrap_toggle');
                $this.data('text-alt', $this.text());
                $this.text(text);
                $comments
                    .toggleClass('Comments-wrap_HIDE');
                $('.fixScrollBlock').trigger('render.airStickyBlock');
            });
        }
    };
};
Comments().init();
var Product = function(){
    return {
        init: function(){
        }
    };
};
Product().init();
var ProgressPayment = function(){
    return {
        init: function(){
        }
    };
};
ProgressPayment().init();
var Categories = function(){
    return {
        init: function(){
            if ($(window).width() < 990) {
                var $more= $('.Categories-more'),
                    $trigger = $('.Categories-trigger');
                $trigger.on('click', function(e){
                    e.preventDefault();
                    var $this = $(this),
                        text = $this.data('text-alt'),
                        $block= $this.prev($more);
                    $this.data('text-alt', $this.text());
                    $this.text(text);
                    $this.toggleClass('Categories-trigger_OPEN');
                    $block.toggle(0);
                });
            }
        }
    };
};
Categories().init();
//ENDion.js
//END


    });


})(jQuery);