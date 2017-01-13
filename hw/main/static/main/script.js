var userMessage = {};
userMessage.show = function(text){
    var obj = this
    obj.html.css('display', 'flex');
    obj.html.find('#message_block').find('.message').text(text);
} 
userMessage.init = function(){
    var obj = this;
    obj.html = $('#user_message');
    obj.html.find('#message_block').find('.close').click(function(){
        obj.html.hide();
    })
}

var infinityList = {};
infinityList.updateGeneral = function(){
    var obj = this;
    obj.pageHeight = parseInt($(document).height());
    obj.winHeight = parseInt($(window).height());
}
infinityList.init = function(){
    var obj = this;

    obj.HTML_loading = $('#loading_block');
    obj.HTML_loading.hide();

    obj.footerHeight = $('footer').height();
    $('footer').hide();
    obj.updateGeneral();

    obj.scrollIndex = 0;
    obj.eror_lock = false;
    obj.load_lock = false;
    obj.end_of_list  = false;

    // ловим событие скрола
    $(document).scroll(function () { 
        var pos = parseInt($(document).scrollTop());

        if ((pos + obj.winHeight > obj.pageHeight - obj.footerHeight) &&  
            (!obj.load_lock) &&
            (!obj.end_of_list)) 
        {
            obj.HTML_loading.show();
            obj.scrollIndex++;
            console.log(obj.scrollIndex);
            obj.load_lock = true;
            $.ajax({
                url: '/page/' + obj.scrollIndex,
                type: 'GET',
                data: {},
                dataType: 'text',
                timeout: 60000,
                success: function(response){

                    console.log('response***' + response + '****');

                    if (response.trim() == 'N/A') {
                        obj.end_of_list = true;
                        $('footer').show();
                    }else{
                        obj.HTML_loading.before(response);
                    }

                    obj.HTML_loading.hide();
                    obj.updateGeneral();
                    obj.load_lock = false;
                },
                error: function(){
                    if (!obj.eror_lock) {
                        obj.scrollIndex--;
                        obj.eror_lock = true;
                        $(document).scrollTop(0);
                        alert('Что то пошло не так, обновите страницу и повторите попытку.');
                        setTimeout(function() { 
                            location.reload();
                        }, 1);
                    }
                }
            });
        }else{
            obj.HTML_loading.hide();
        }
    });

    // ресайз
    $(window).resize(function () {
        obj.updateGeneral();
    });
}

var modalWindow = {}
modalWindow.State = function(state){
    var obj = this;
    if (state == 'show') {
        obj.HTML.css('display', 'flex');
    }else{
        obj.HTML.css('display', 'none');
    }
}
modalWindow.init = function(){
    var obj = this;

    obj.maxImgSize = 1000000;

    obj.HTML = $('#modal_window');
    
    obj.State('hide');

    $('#show_modal_window').click(function(){
        
        obj.State('show');
    })

    $('#hide_modal_window').click(function(){
        
        obj.State('hide');
    })

    $('#new_rec_img').change(function(){

        var input = this;

        // выкачиваем данные из инпута
        if (input.files && input.files[0] && input.files[0].size <= obj.maxImgSize) {

            //  номальный файл
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#pre_img').css('background-image','url('+e.target.result+')');
                $('#pre_img').addClass('show');                
            }
            reader.readAsDataURL(input.files[0]);
        }else{
            userMessage.show('Максимальный размер файла: ' + obj.maxImgSize + ' байт');
            input.value = null;
            $('#pre_img').removeClass('show');
        }   
    })
}

function stickLeftBar(id){
    $('#' + id).unstick();
    $('#' + id).sticky({topSpacing: 70});
}

function isFigure(char) {
    for (var i = 0; i < 10; i++) {
        if (i.toString() == char) {
            return true;
        }
    }
    return false;
}

function addZero(int){
    if (int < 10) {
        return '0' + int.toString();
    }
    return int.toString();
}

$('#add_rec_button').click(function(){

    var form = $('#form_add');

    var name = form.find('#new_rec_name').val(),
        address = form.find('#new_rec_address').val(),
        time = form.find('#new_rec_time').val(),
        desc = form.find('#new_rec_desc').val();

    if (name.length == 0) {
        userMessage.show('Введите название конференции.');
        return;
    }

    if (address.length == 0) {
        userMessage.show('Введите адрес конференции.');
        return;
    }

    if (time.length == 0) {
        userMessage.show('Введите время мероприятия в формате ДД.ММ.ГГГГ ЧЧ:ММ.');      
        return;
    }


    var excludes = {'2': '.', '5': '.', '10': ' ', '13': ':'};
    var error_datetime = 'Неверный формат ввода даты и времени';

    for (var i = 0; i < time.length; i++) {
        var char = excludes[i.toString()];
        if (char === undefined) {
            if(!isFigure(time.charAt(i))){ userMessage.show(error_datetime); return; };
        }else{
            if (time.charAt(i) != char) { userMessage.show(error_datetime); return; }
        }     
    }

    var newDate = new Date(parseInt(time.slice(6,10)), parseInt(time.slice(3,5)) - 1, parseInt(time.slice(0,2)));
    newDate.setHours(parseInt(time.slice(11,13)), parseInt(time.slice(14,16)));
    
    time = '';

    time += addZero(newDate.getDate());
    time += '.';
    time += addZero(newDate.getMonth() + 1);
    time += '.';
    time += (newDate.getFullYear()).toString();
    time += ' ';
    time += addZero(newDate.getHours());
    time += ':';
    time += addZero(newDate.getMinutes());

    if (desc.length == 0) {
        userMessage.show('Введите описание конференции.');
        return;
    }

    var input = document.getElementById('new_rec_img');
    if (!input.files || !input.files[0] || input.files[0].size == 0) {
        userMessage.show('Добавьте картинку для конференции.');
        return;
    }

    form.submit();
})

$(document).ready(function () {
    infinityList.init();
    modalWindow.init();
    userMessage.init();
    stickLeftBar('left_bar_stick');
})

$(window).resize(function(){
    stickLeftBar('left_bar_stick');
})




    
