$( document ).ready(function() {

        // Die Variablen müssen wegen Jinja in der html-Datei vorbereitet werden!

        // Funktion, um Spalte in 2. Dimension als Zeile auszugeben
        // https://stackoverflow.com/a/34979219
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


    // Spalten aufzählen, um spaltenweise Features auswählen zu können
        for(i=0; i < anzSpalten; i++){
            if(i!=zeitreihenSpalte){

                // clone column section in collapsible & append it to the collapsible
                $("#spaltenColTemplate").clone().attr("id", "spaltenCol" + i).appendTo("#spaltenCollapsible").show();

                // Spaltentitel einfügen
                $("#spaltenCol" + i + " .colHeader").html("Spalte " + i + " :  <b>" + spaltenTitel[i] + "</b>");

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

    $('#analyseAuswahlForm').on('keyup blur', function () {
        if ($('#analyseAuswahlForm').valid()) {
            $('#submitButton').prop('disabled', false);
        }
        else {
            $('#submitButton').prop('disabled', 'disabled');
        }
    });});
$('form').submit(function(event){
        event.preventDefault();
        if(!$('form').valid()) {
        return;
        }


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
            'resampling':$("#resampling").prop('checked'),
            'resamplingScale':$("#resamplingScale").val(),
            'fourier':$("#fourier").prop('checked'),
            'fourierval':$("#fourierval").val(),
        }

        for (i = 0; i < anzSpalten; i++) {
            if (i != zeitreihenSpalte) {
                data['hochpassOrder' + i] = $('#spaltenCol' + i).find('#hochpassOrder' + i).val()
                data['hochpassCofreq' + i] = $('#spaltenCol' + i).find('#hochpassCofreq' + i).val()
                data['tiefpassOrder' + i] = $('#spaltenCol' + i).find('#tiefpassOrder' + i).val()
                data['tiefpassCofreq' + i] = $('#spaltenCol' + i).find('#tiefpassCofreq' + i).val()

                data['hochpass' + i] = $('#spaltenCol' + i).find('#hochpass' + i).prop('checked');
                data['tiefpass' + i] = $('#spaltenCol' + i).find('#tiefpass' + i).prop('checked');
                data['gauss' + i] = $('#spaltenCol' + i).find('#gauss' + i).prop('checked');
                data['gaussStd' + i] = $('#spaltenCol' + i).find('#gaussStd' + i).val();
                data['gaussM' + i] = $('#spaltenCol' + i).find('#gaussM' + i).val();
            }
        }
        var experimentId = parseInt($("#experimentId").val());

        $.ajax({

            url: '/analysis/refresh/' + experimentId,

            method: 'post',
            data: data,
            cache: false,
            dataType: 'json',
            success: function (data) {

            dataArray = JSON.parse(data.jsonData);
            spaltenTitel = JSON.parse(data.jsonHeader);
            spaltenEinheiten = JSON.parse(data.jsonEinheiten);
            zeitreihenSpalte = data.zeitreihenSpalte;
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
    }})
});
