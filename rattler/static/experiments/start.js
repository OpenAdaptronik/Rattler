$( document ).ready(function() {
 //Token Configuration
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
$('form').submit(function(event){
    event.preventDefault();

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
//Prepare Submission Data
        var data = {
            'function':$("#function").val(),
            'first':$("#first").val(),
            'second':$("#second").val(),
            'dataArray':$("#jsonData").val(),
            'jsonHeader':$("#jsonHeader").val()
        }

$.ajax({

        url: '/experiments/newexperiments/refresh',

        method: 'post',
        data: data  ,
        cache:false,
        dataType: 'json',
        success: function (data) {

            dataArray = JSON.parse(data.jsonData);
            intderivresult = JSON.parse(data.intderivresult);
            spaltenTitel = JSON.parse(data.jsonHeader);
            spaltenEinheiten = JSON.parse(data.jsonEinheiten);
            zeitreihenSpalte = data.zeitreihenSpalte;
            anzSpalten = dataArray[0].length;
            $('#dataTest').text(intderivresult)
        }})


})}