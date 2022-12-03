// This function exsist, so that I can get django's csrf token from the cookied to this js file
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function arrayRemove(arr, value) {
    return arr.filter(function(ele){
        return ele != value;
    });
}

function giveEmptyMessage(arr, absoluteLength){
    if (arr.length < absoluteLength){
        var message = 'Please fill out the red fields.';
        var error = '<h6>' + message + '</h6>';
        return error;
    }else{
        return '';
    }
};

function resetFieldColor(arr, absoluteLength){
    $.each(arr, function(i, element) {
        $(element).css('background-color', '#3E6D9C');
        console.log(element)
    })
};

// I need the code below to make ajax post requests
$(document).ready(function(){

    $('#contact-form').submit(function(e){
        e.preventDefault()

        var form = $('#contact-form')[0];
        var formData = new FormData(form);
        const csrftoken = getCookie('csrftoken');
        formData.append('csrfmiddlewaretoken', csrftoken)

        $.ajax({
            type: 'POST',
            url: '/',
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            success: function (){
                 var fieldsArray = ['#id_sender_full_name', '#id_sender_email', '#id_sender_subject', '#id_sender_message'];
                 $.each(fieldsArray, function(i, element){
                    $(element).css('background-color', '#3E6D9C');
                 }),
                $('.form-alert').css('display', 'none');
                form.reset();
                $('#id_sender_full_name').focus();
              },
            error: function (data, xhr, errmsg, err) {
                $('.form-alert').fadeIn();
                var fieldsArray = ['#id_sender_full_name', '#id_sender_email', '#id_sender_subject', '#id_sender_message'];
                var errorEmpty = '';
                var errorValidator = '';
                var message = '';
                var error = '';

                $.each(data.responseJSON.error, function(i, val) {
                    var fieldId = '#id_' + i;

                    if (val[0] == 'This field is required.'){
                        fieldsArray = arrayRemove(fieldsArray, fieldId);
                        $(fieldId).css('background-color', '#FF0000');
                    }else{
                        message = val[1];
                        errorValidator += '<h6>' + message + '</h6>';
                    }
                }),
                errorEmpty += giveEmptyMessage(fieldsArray, 4),
                error = errorEmpty + errorValidator,
                resetFieldColor(fieldsArray),
                $('.form-error').html(error)
            }
        });
    });
});