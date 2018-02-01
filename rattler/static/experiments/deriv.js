$(document).ready(function () {
    // Clone firstCol select to secondCol select
    $("#secondCol").html($("#firstCol").html());
    
    // init vars
    var firstCol, secondCol, newColName, newColUnit, intOrDevFctCode;
    var numTasks = 0;

    // get vars from python (submitted through hidden html fields)
    var experimentId = parseInt($("#experimentId").val());
    var numOfCols = parseInt($("#numOfCols").val());
    
    // triggered when function is submitted
    $('#newTaskForm').submit(function (event) {
        event.preventDefault();
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
        
        firstCol = $("#firstCol").val();
        secondCol = $("#secondCol").val();
        newColName = $("#newColName").val();
        newColUnit = $("#newColUnit").val();
        intOrDevFctCode = $("#function").val();

        //Prepare Submission Data
        var submitData = {
            'function': intOrDevFctCode,
            'firstCol': firstCol,
            'secondCol': secondCol,
            'newColName': newColName,
            'newColUnit': newColUnit,
            //'dataArray': $("#jsonData").val(), // wird jetzt eig. aus Datenbank geladen ... hoffentlich
            //'jsonHeader': $("#jsonHeader").val() // brauchen wir eig. nicht
        }

        $.ajax({
            url: '/experiments/' + experimentId + '/derivate/refresh/', // emerges to "experiments/<int:experimentId>/derivate/refresh/"
            method: 'post',
            data: submitData,
            cache: false,
            dataType: 'json',
            success: function (data) {
                //dataArray = JSON.parse(data.jsonData);
                newColData = JSON.parse(data.result);
                //spaltenTitel = JSON.parse(data.jsonHeader);
                //spaltenEinheiten = JSON.parse(data.jsonEinheiten);
                //zeitreihenSpalte = data.zeitreihenSpalte;
                //anzSpalten = dataArray[0].length;
                console.log(newColData);

                // count the cols!
                numOfCols++;
                // count the successful tasks!
                numTasks++;

                // Add task to completed task list
                $("#taskFinishedTemplate").clone().appendTo("#completedTasksCollection").attr("id","").addClass("newestCompletedTask");
                $(".newestCompletedTask .taskNumber").html(numTasks);
                $(".newestCompletedTask .firstColInfo").html(firstCol);
                $(".newestCompletedTask .secondColInfo").html(secondCol);
                if(intOrDevFctCode == "0") var intOrDeriv = "abgeleitet";
                if(intOrDevFctCode == "1") var intOrDeriv = "integriert";
                $(".newestCompletedTask .tastNumber").html(numTasks+1);
                $(".newestCompletedTask .intOrDeriv").html(intOrDeriv);
                $(".newestCompletedTask .resultColInfo").html(numOfCols + " (\"" + newColName + "\" (" + newColUnit + "))");
                $(".newestCompletedTask").removeClass("hide").removeClass("");
                $("#completedTasksSection").removeClass("hide");
                $("#completedTasksDivider").removeClass("hide");

                // Show new task form again
                $("#newTaskInProgress").addClass("hide");
                $("#newTask").removeClass("hide");
                
                // clear new task form for next task
                $('#newTaskForm').trigger("reset");
                Materialize.updateTextFields();
            },
            error: function(xhr, status, error) {
                console.log("ERROR " + error);
            }
        })


    })
})