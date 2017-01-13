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

function ajaxFormRequest(form_id, url) {
    $.ajax({
        url:                url, 
        type:               "POST", 
        dataType:           "html", 
        data: $("#"+form_id).serialize(), 
        success: function(response) { 
            console.log(response);
            response = JSON.parse(response);
            if (response.error != 'NO') {
                userMessage.show(response.error);
            }else{
                location.href = '.';
            }
        },
        error: function(response) { 
            userMessage.show('Что то пошло не так...');
        }   
    });
}

$('#reg_user').click(function(){
    var form = $('#registration_form');

    var pas1 = form.find('#id_password1').val(),
        pas2 = form.find('#id_password2').val(),
        user_name = form.find('#id_username').val();

    if (user_name.length == 0) {
        userMessage.show('Введите имя пользователя.');      
        return; 
    }

    if (pas1.length == 0) {
        userMessage.show('Введите пароль.');
        return;
    }

    if (pas1 != pas2) {
        userMessage.show('Пароли не равны.');
        return;
    }

    ajaxFormRequest('registration_form', 'login/register');
})

$('#login_user').click(function(){
    var form = $('#login_form');

    var pas = form.find('#id_password').val(),
        user_name = form.find('#id_username').val();

    if (user_name.length == 0) {
        userMessage.show('Введите имя пользователя.');      
        return; 
    }

    if (pas.length == 0) {
        userMessage.show('Введите пароль.');
        return;
    }

    ajaxFormRequest('login_form', 'login/auth');
})

$(document).ready(function () { 
    userMessage.init();
})