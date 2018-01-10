$( document ).ready(function() {
    // Funktion, um Spalte in 2. Dimension als Zeile auszugeben
    // https://stackoverflow.com/a/34979219
    function arrayColnAsRow(arr, n) {
            return arr.map(function(x) { return x[n]})
        }

    // Plotly: Graph von vorheriger Seite wieder plotten
        var traces = [];
        // s. Variablenname
        zeitreihenSpalteAlsZeile = arrayColumnAsRow(dataArray, zeitreihenSpalte);

    var layout = {
        title: 'Dein Experiment:',
        xaxis: {
            title: spaltenTitel[zeitreihenSpalte]+' ('+spaltenEinheiten[zeitreihenSpalte]+')',
        }
    }

    // Alle Spalten durchlaufen und Daten für die Visualisierung aufbereiten

    for(var j=0; j < anzSpalten; j++){ // i = Index über Spalten
        traces[j] = {
            x: zeitreihenSpalteAlsZeile,
            y: arrayColumnAsRow(dataArray, j),
            name: spaltenTitel[j] + ' ('+spaltenEinheiten[j]+')',
            type: 'scatter',
            line: {
                width: 1.5,
            }
        }

    }
    traces[zeitreihenSpalte] = [];
    traces[zeitreihenSpalte].shift();

    Plotly.newPlot('firstGraph', traces, layout);


    for(i=0; i < anzSpalten; i++) {
        if (i != zeitreihenSpalte) {
            $("#data1").append(
                "<option value="+i+">"+spaltenTitel[i]+"</option>")
            $("#data2").append(
                "<option value="+i+">"+spaltenTitel[i]+"</option>")
        }
    }

    //Validation
    $(document).on("keyup blur change", "#tessForm", function() {
        if ($("#data1 :selected").val()!=$("#data2 :selected").val()
            &&$("#data1 :selected").val()!=""&&$("#data2 :selected").val()!="") {
            $('#refreshButton').prop('disabled', false);
            $('#validationMessage').hide();
        }
        else {
            $('#refreshButton').prop('disabled', true);
            $('#validationMessage').show();
    }});

});

//When button is pressed
$('form').submit(function(event){
    event.preventDefault();


    //Token Configuration
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
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
            'data1':$("#data1 :selected").val(),
            'data2':$("#data2 :selected").val(),
        }

    $.ajax({
        url: '/tess/refresh',
        method: 'post',
        data: data  ,
        cache:false,
        dataType: 'json',
        success: function (data) {
            $('#tessResult').show()
            $('#strat1').text(data.strategie1)
            $('#param1').text(data.param1)
            $('#strat2').text(data.strategie2)
            $('#param2').text(data.param2)
            $('#strat3').text(data.strategie3)
            $('#param3').text(data.param3)
            $('#strat4').text(data.strategie4)
            $('#param4').text(data.param4)
            $('#strat5').text(data.strategie5)
            $('#param5').text(data.param5)
        }
    });
});