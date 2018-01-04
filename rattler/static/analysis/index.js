$( document ).ready(function() {

    $('form').submit(function(event){
        console.log('Triggert')
        event.preventDefault();

         $.ajax(
              {
            url: '/analysis/refresh',

            method: 'post',

            data: {
                discount_code: 1,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },

            dataType: 'json',
            success: function (data) {
                alert('its some kind of magic!')
                console.log('Juhuu Drinne!!!');
                console.log(data)
            }});
    })


});