



function stickRightBar(id){
    $('#' + id).unstick();
    $('#' + id).sticky({topSpacing: 70});
}

var currentState = '';
var csrf_token = '';

function ajaxLoadUsers(state){
    // using jQuery
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
    });

    $.ajax({
        url: location,
        type: 'POST',
        data: {state : state, csrfmiddlewaretoken : csrf_token},
        dataType: 'text',
        timeout: 60000,
        success: function(response){

            console.log('response***' + response + '****');
            $('#users_list_container').html(response);

            if (currentState == 'True') {
                $('#user_status').text('Accepted');
            }else{
                $('#user_status').text('False accepted');
            }

        },
        error: function(){
            alert('Упс... Что то пошло не так, обновите страницу и повторите попытку.');
            if (currentState == 'True') {
                currentState = 'False';
            }else{
                currentState = 'True';
            }
        }
    });
}

$('#change_status_button').click(function(){

    if (currentState == 'True') {
        currentState = 'False';
    }else{
        currentState = 'True';
    }

    ajaxLoadUsers(currentState);
})

$(document).ready(function () {
    stickRightBar('right_side_bar');

    // текущий статус
    currentState = $('#user_status').attr('status-val');

    // токен
    csrf_token = $('#csrf_token_val').attr('csrf_token');

    // юзвери
    ajaxLoadUsers(currentState);
})


$(window).resize(function () {
    stickRightBar('right_side_bar');
})