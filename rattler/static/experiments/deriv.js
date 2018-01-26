$(document).ready(function () {
    
    // Clone firstCol select to secondCol select because django cant do it by itself
    $("#secondCol").html($("#firstCol").html());

    // get experimentId
    experimentId = parseInt($("#experimentId").val());
    
    // triggered when function is submitted
    $('#newTaskForm').submit(function (event) {
        event.preventDefault();
        console.log("Submit");
        // hide new task form and show preloader
        $("#newTask").addClass("hide");
        $("#newTaskInProgress").removeClass("hide");
        //Token Configuration
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        


        //Prepare Submission Data
        var data = {
            'function': $("#function").val(),
            'firstCol': $("#firstCol").val(),
            'secondCol': $("#secondCol").val(),
            'newColName': $("#newColName").val(),
            'newColUnit': $("#newColUnit").val(),
            //'dataArray': $("#jsonData").val(), // wird jetzt eig. aus Datenbank geladen ... hoffentlich
            //'jsonHeader': $("#jsonHeader").val() // brauchen wir eig. nicht
        }

        $.ajax({
            url: '/experiments/' + experimentId + '/derivate/refresh/', // emerges to "experiments/<int:experimentId>/derivate/refresh/"
            method: 'post',
            data: data,
            cache: false,
            dataType: 'json',
            success: function (data) {
                //dataArray = JSON.parse(data.jsonData);
                console.log("success");
                newColData = JSON.parse(data.result);
                //spaltenTitel = JSON.parse(data.jsonHeader);
                //spaltenEinheiten = JSON.parse(data.jsonEinheiten);
                //zeitreihenSpalte = data.zeitreihenSpalte;
                //anzSpalten = dataArray[0].length;
                console.log(newColData);

                // Show new task form again
                $("#newTaskInProgress").addClass("hide");
                $("#newTask").removeClass("hide");
            },
            error: function(xhr, status, error) {
                console.log("ERROR " + error);
            }
        })


    })
})