$(document).ready(function () {

  function arrayColnAsRow(arr, n) {
      return arr.map(function(x) { return x[n]})
  }

      var color = ['#005C47', '#FF6600', '#006E94', '#FDC300', '#B28700', '#FF3400'];
  // Plotly: Graph von vorheriger Seite wieder plotten
      var traces = [];
      // s. Variablenname
      zeitreihenSpalteAlsZeile = arrayColnAsRow(dataArray, zeitreihenSpalte);

  var layout = {
      title: 'Dein Experiment:',
      xaxis: {
          title: spaltenTitel[zeitreihenSpalte]+' ('+spaltenEinheiten[zeitreihenSpalte]+')',
      }
  }


  // Alle Spalten durchlaufen und Daten für die Visualisierung aufbereiten

  for(var j=0; j < anzSpalten; j++){
      // i = Index über Spalten
      traces[j] = {
          x: zeitreihenSpalteAlsZeile,
          y: arrayColnAsRow(dataArray, j),
          name: spaltenTitel[j] + ' ('+spaltenEinheiten[j]+')',
          type: 'scatter',
          line: {
              color: color[j],
              width: 1.5,
          }
      }

  }
  traces[zeitreihenSpalte] = [];
  traces[zeitreihenSpalte].shift();

  Plotly.newPlot('firstGraph', traces, layout);


    // Clone firstCol select to secondCol select
    $("#secondCol").html($("#firstCol").html());

    // init vars
    var firstCol, secondCol, newColName, newColUnit, intOrDevFctCode;
    var numTasks = 0;
    // @TODO: the following vars have to be initialized w/ the existing cols of the experiment,
    // because Fraunhofer want all the existing cols saved to the new experiment, too.
    var xHeaders = JSON.parse($("#jsonHeader").val());
    var xUnits = JSON.parse($("#jsonEinheiten").html());
    var xMeasurementInstruments = JSON.parse($("#jsonMeasurementInstruments").html());
    var xData = JSON.parse($("#jsonData").html());

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

                //anzSpalten = dataArray[0].length;
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

                // Append new info and data to fields containing the vars we send to python to create a new experiment
                // add the new heading to the headers
                xHeaders.push(newColName);
                $("#jsonHeader").val(JSON.stringify(xHeaders));
                // add the new unit to the units
                xUnits.push(newColUnit);
                $("#jsonEinheiten").html(JSON.stringify(xUnits));
                // add new empty Instrument to MeasurementInstruments
                xMeasurementInstruments.push("No");
                $("#jsonMeasurementInstruments").html(JSON.stringify(xMeasurementInstruments));
                // add new col data to data
                var horizontalLength = xData[0].length;
                for(i=0; i<xData.length; i++){
                    xData[i][horizontalLength] = newColData[i];
                }
                $("#jsonData").html(JSON.stringify(xData));
                // add sentence about the completed task to the experiment description
                $("#experimentDescr").html($("#experimentDescr").html() + "\nSpalte " + firstCol + " wurde über Spalte " + secondCol + " in die neue Spalte \"" + newColName + "\" " + intOrDeriv + ".");

                // Show the info of the completed task in the completed tasks section
                $(".newestCompletedTask").removeClass("hide").removeClass("newestCompletedTask");
                $("#completedTasksSection").removeClass("hide");
                $("#completedTasksDivider").removeClass("hide");

                // clear new task form for next task and make the fields look good again
                $('#newTaskForm').trigger("reset");
                Materialize.updateTextFields();
                $('#experimentDescr').trigger('autoresize');

                // Show new task form again
                $("#newTaskInProgress").addClass("hide");
                $("#newTask").removeClass("hide");


                dataArray = xData;
                spaltenTitel = xHeaders;
                spaltenEinheiten = xUnits;
                anzSpalten = dataArray[0].length;

                // Funktion, um Spalte in 2. Dimension als Zeile auszugeben
                // https://stackoverflow.com/a/34979219
                function arrayColnAsRow(arr, n) {
                    return arr.map(function (x) { return x[n] })
                }

                // Plotly: Graph von vorheriger Seite wieder plotte
                var color = ['#005C47','#FF6600' , '#006E94' , '#FDC300', '#B28700' , '#FF3400']
                var traces = [];
                // s. Variablenname
                zeitreihenSpalteAlsZeile = arrayColnAsRow(dataArray, zeitreihenSpalte);
                var layout = {
                    title: 'Dein Experiment:',
                    xaxis: {
                        title: spaltenTitel[zeitreihenSpalte] + ' (' + spaltenEinheiten[zeitreihenSpalte] + ')',
                    }
                }

                // Alle Spalten durchlaufen und Daten für die Visualisierung aufbereiten

                for (var j = 0; j < anzSpalten; j++) { // i = Index über Spalten
                    traces[j] = {
                        x: zeitreihenSpalteAlsZeile,
                        y: arrayColnAsRow(dataArray, j),
                        name: spaltenTitel[j] + ' (' + spaltenEinheiten[j] + ')',
                        type: 'scatter',
                        line: {
                            color: color[j],
                            width: 1.5,
                        }
                    }}


                for(var j=0; j < anzSpalten; j++) { // i = Index über Spalten
                    traces[j] = {
                        x: zeitreihenSpalteAlsZeile,
                        y: arrayColnAsRow(dataArray, j),
                        name: spaltenTitel[j] + ' (' + spaltenEinheiten[j] + ')',
                        type: 'scatter',
                        line: {
                        color: color[j],
                        width: 1.5,
                      }}
                      traces[zeitreihenSpalte] = [];
                      traces[zeitreihenSpalte].shift();

                      Plotly.newPlot('firstGraph', traces, layout);
                    }



            },
            error: function(xhr, status, error) {
                console.log("ERROR " + error);
            }
        })


    })
})
