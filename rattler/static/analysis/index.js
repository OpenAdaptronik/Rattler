$( document ).ready(function() {

    // Die Variablen müssen wegen Jinja in der html-Datei vorbereitet werden!

    // Funktion, um Spalte in 2. Dimension als Zeile auszugeben
    // https://stackoverflow.com/a/34979219
    const arrayColumnAsRow = (arr, n) => arr.map(x => x[n]);

    // Plotly: Graph von vorheriger Seite wieder plotten
        var traces = [];
        // s. Variablenname
        zeitreihenSpalteAlsZeile = arrayColumnAsRow(dataArray, zeitreihenSpalte);

        var layout = {
            title: 'Graph zur Orientierung:',
            'xaxis': {
                autotick: true
            }
        }

        // Alle Spalten durchlaufen und Daten für die Visualisierung aufbereiten
        for(i=0; i < anzSpalten; i++){ // i = Index über Spalten
            traces[i] = {
                x: zeitreihenSpalteAlsZeile,
                y: arrayColumnAsRow(dataArray, i),
                name: spaltenTitel[i] + "(" + spaltenEinheiten[i] + ")",
                type: 'scatter',
                line: {
                    width: 1.5,
                }
            }
            var yaxisTitle;
            if(i==0){
                traces[i]['yaxis'] = 'y';
                yaxisTitle = 'yaxis';
            } else {
                traces[i]['yaxis'] = 'y' + (i+1);
                yaxisTitle = 'yaxis' + (i+1);
            }
            layout[yaxisTitle] = {
                showgrid: false,
                zeroline: false,
                showline: false,
                autotick: true,
                showticklabels: false,
            }
            if(i!=0){
                layout[yaxisTitle]['overlaying'] = 'y';
            }
        }
        traces[zeitreihenSpalte] = [];
        traces[zeitreihenSpalte].shift();

        Plotly.newPlot('firstGraph', traces, layout);


    // Spalten aufzählen, um spaltenweise Features auswählen zu können
        for(i=0; i < anzSpalten; i++){
            if(i!=zeitreihenSpalte){

                // clone column section in collapsible & append it to the collapsible
                $("#spaltenColTemplate").clone().attr("id", "spaltenCol" + i).appendTo("#spaltenCollapsible").show();

                // Spaltentitel einfügen
                $("#spaltenCol" + i + " .colHeader").html("Spalte " + i + ": <b>" + spaltenTitel[i] + "</b>");

                // IDs, names, fors
                    $("#spaltenCol" + i + " #hochpass").attr("name", "hochpass" + i).attr("id", "hochpass" + i);
                    $("#spaltenCol" + i + " .hochpassLabel").attr("for", "hochpass" + i);

                        $("#spaltenCol" + i + " #hochpassOrder").attr("id", "hochpassOrder" + i);
                        $("#spaltenCol" + i + " .hochpassOrderLabel").attr("for", "hochpassOrder" + i);

                        $("#spaltenCol" + i + " #hochpassCofreq").attr("id", "hochpassCofreq" + i);
                        $("#spaltenCol" + i + " .hochpassCofreqLabel").attr("for", "hochpassCofreq" + i);

                    $("#spaltenCol" + i + " #tiefpass").attr("name", "tiefpass" + i).attr("id", "tiefpass" + i);
                    $("#spaltenCol" + i + " .tiefpassLabel").attr("for", "tiefpass" + i);

                        $("#spaltenCol" + i + " #tiefpassOrder").attr("id", "tiefpassOrder" + i);
                        $("#spaltenCol" + i + " .tiefpassOrderLabel").attr("for", "tiefpassOrder" + i);

                        $("#spaltenCol" + i + " #tiefpassCofreq").attr("id", "tiefpassCofreq" + i);
                        $("#spaltenCol" + i + " .tiefpassCofreqLabel").attr("for", "tiefpassCofreq" + i);

                    $("#spaltenCol" + i + " #gauss").attr("name", "gauss" + i).attr("id", "gauss" + i);
                    $("#spaltenCol" + i + " .gaussLabel").attr("for", "gauss" + i);

                        $("#spaltenCol" + i + " #gaussStd").attr("id", "gaussStd" + i);
                        $("#spaltenCol" + i + " .gaussStdLabel").attr("for", "gaussStd" + i);

                        $("#spaltenCol" + i + " #gaussM").attr("id", "gaussM" + i);
                        $("#spaltenCol" + i + " .gaussMLabel").attr("for", "gaussM" + i);
            }
        }



    $('form').submit(function(event){
        event.preventDefault();


        //Token Configuration
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        //console.log($("form").serialize())

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
        /*
        console.log('neue Daten eingelesen')
        console.log('resampling neu:')
        console.log($("#resampling").prop('checked'))*/
        var data = {
            'resampling':$("#resampling").prop('checked'),
            'resamplingScale':$("#resamplingScale").val(),
            'fourier':$("#fourier").prop('checked'),
        }
        for(i=0; i < anzSpalten; i++){
            if(i!=zeitreihenSpalte){
                data['hochpassOrder'+i] = $("#spaltenCol" + i + " #hochpassOrder").val();
                data['hochpassCofreq'+i] = $("#spaltenCol" + i + " #hochpassCofreq").val();
                data['tiefpassOrder'+i] = $("#spaltenCol" + i + " #tiefpassOrder").val();
                data['tiefpassCofreq'+i] = $("#spaltenCol" + i + " #tiefpassCofreq").val();

                data['hochpass'+i] = $("#spaltenCol" + i + " #hochpass").prop('checked');
                data['tiefpass'+i] = $("#spaltenCol" + i + " #tiefpass").prop('checked');
                data['gauss'+i] = $("#spaltenCol" + i + " #gauss").prop('checked');
                data['gaussStd'+i] = $("#spaltenCol" + i + " #gaussStd").val();
                data['gaussM'+i] = $("#spaltenCol" + i + " #gaussM").val();
                }
            }


        $.ajax({

        url: '/analysis/refresh',

        method: 'post',
        data: data  ,
        cache:false,
        dataType: 'json',
        success: function (data) {
            console.log('neue Visualisierung:')
            //alert('its some kind of magic!')


           console.log(data.log)
           dataArray = JSON.parse(data.jsonData);
           spaltenTitel = JSON.parse(data.jsonHeader);
           spaltenEinheiten = JSON.parse(data.jsonEinheiten);
           zeitreihenSpalte = data.zeitreihenSpalte;
           anzSpalten = dataArray[0].length;


        // Funktion, um Spalte in 2. Dimension als Zeile auszugeben
        // https://stackoverflow.com/a/34979219
        const arrayColumnAsRow = (arr, n) => arr.map(x => x[n]);

        // Plotly: Graph von vorheriger Seite wieder plotten
            var traces = [];
            // s. Variablenname
            zeitreihenSpalteAlsZeile = arrayColumnAsRow(dataArray, zeitreihenSpalte);

        var layout = {
            title: 'Graph zur Orientierung:',
            'xaxis': {
                autotick: true
            }
        }
        console.log(dataArray)





        // Alle Spalten durchlaufen und Daten für die Visualisierung aufbereiten
        for(var j=0; j < anzSpalten; j++){ // i = Index über Spalten
            console.log('j')
            console.log(j)
            console.log('anzSpalten')
            console.log(anzSpalten)
            traces[j] = {
                x: zeitreihenSpalteAlsZeile,
                y: arrayColumnAsRow(dataArray, j),
                name: spaltenTitel[j] + "(" + spaltenEinheiten[j] + ")",
                type: 'scatter',
                line: {
                    width: 1.5,
                }
            }
            var yaxisTitle;
            if(j==0){
                traces[j]['yaxis'] = 'y';
                yaxisTitle = 'yaxis';
            } else {
                traces[j]['yaxis'] = 'y' + (j+1);
                yaxisTitle = 'yaxis' + (j+1);
            }
            layout[yaxisTitle] = {
                showgrid: false,
                zeroline: false,
                showline: false,
                autotick: true,
                showticklabels: false,
            }
            if(j!=0){
                layout[yaxisTitle]['overlaying'] = 'y';
            }
        }
        traces[zeitreihenSpalte] = [];
        traces[zeitreihenSpalte].shift();

        Plotly.newPlot('firstGraph', traces, layout);



        }});
    })



});