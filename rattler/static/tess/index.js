$( document ).ready(function() {
    // Funktion, um Spalte in 2. Dimension als Zeile auszugeben
    // https://stackoverflow.com/a/34979219
    function arrayColnAsRow(arr, n) {
            return arr.map(function(x) { return x[n]})
        }

    // Plotly: Graph von vorheriger Seite wieder plotten
        var traces1 = [];
        var traces2 = [];
        // s. Variablenname
        zeitreihenSpalteAlsZeile = arrayColnAsRow(dataArray, zeitreihenSpalte);

    var firstGraph = document.getElementById("firstGraph");
    var secondGraph = document.getElementById("secondGraph");

    var layout1 = {
        title: 'Dein Experiment1:',
        xaxis: {
            title: spaltenTitel[zeitreihenSpalte]+' ('+spaltenEinheiten[zeitreihenSpalte]+')',
        },
        updatemenus: [{
        y: 1,
        yanchor: 'top',
        buttons: [{
            method: 'relayout',
            args: ['yaxis.type', 'linear'],
            label: 'linear'
        }, {
            method: 'relayout',
            args: ['yaxis.type', 'log'],
            label: 'log'
        }]
    }],
        yaxis: {
            fixedrange: true,
        }
    }

    var layout2 = {
        title: 'Dein Experiment2:',
        xaxis: {
            title: spaltenTitel[zeitreihenSpalte]+' ('+spaltenEinheiten[zeitreihenSpalte]+')',
        },
        updatemenus: [{
        y: 1,
        yanchor: 'top',
        buttons: [{
            method: 'relayout',
            args: ['yaxis.type', 'linear'],
            label: 'linear'
        }, {
            method: 'relayout',
            args: ['yaxis.type', 'log'],
            label: 'log'
        }]
    }],
        yaxis: {
            fixedrange: true,
        }
    }

    // Alle Spalten durchlaufen und Daten für die Visualisierung aufbereiten
    for(var j=0; j < anzSpalten; j++){ // i = Index über Spalten
        traces1[j] = {
            x: zeitreihenSpalteAlsZeile,
            y: arrayColnAsRow(dataArray, j),
            name: spaltenTitel[j] + ' ('+spaltenEinheiten[j]+')',
            type: 'scatter',
            visible: graphVisibility[j-1],
            line: {
                width: 1.5,
            }
        }
    }

    // Alle Spalten durchlaufen und Daten für die Visualisierung aufbereiten
    for(var j=0; j < anzSpalten; j++){ // i = Index über Spalten
        traces2[j] = {
            x: zeitreihenSpalteAlsZeile,
            y: arrayColnAsRow(dataArray, j),
            name: spaltenTitel[j] + ' ('+spaltenEinheiten[j]+')',
            type: 'scatter',
            visible: graphVisibility[j-1],
            line: {
                width: 1.5,
            }
        }
    }

    traces1[zeitreihenSpalte] = [];
    traces1[zeitreihenSpalte].shift();
    traces2[zeitreihenSpalte] = [];
    traces2[zeitreihenSpalte].shift();

    Plotly.newPlot(firstGraph, traces1, layout1);
    Plotly.newPlot(secondGraph, traces2, layout2);


    var divs = [firstGraph, secondGraph];


    var plots = [firstGraph, secondGraph];
    //add event listener to each graph to call relayout function when a graph gets relayouted
    plots.forEach(div => {div.on("plotly_relayout", function(ed) {
            console.log(ed);
            relayout(ed, divs);
        });
    });

    var divs = [firstGraph, secondGraph];

    //relayout function
    function relayout(ed, divs) {
        divs.forEach((div) => {
            //synchronize log/linear-switch button
            if ((ed["yaxis.type"] != div.layout.yaxis.type) && ed["yaxis.type"] != undefined){
                Plotly.relayout(div, ed)
                return;
            //if user zooms out when he is already at max zoom out
        } else if ((ed["xaxis.autorange"] && div.layout.xaxis.autorange) && ed["xaxis.autorange"] != undefined){
                return;
            //synchronize xaxis
        } else if ((div.layout.xaxis.range[0] != ed["xaxis.range[0]"] || div.layout.xaxis.range[1] != ed["xaxis.range[1]"]) &&
                   (ed["xaxis.range[0]"] != undefined || ed["xaxis.autorange"] != undefined)) {
                Plotly.relayout(div, ed);
                return;
        } else {
                return;
        }
        });
    }

    //add event listener to each graph to call restyle when a graph gets restyled
    plots.forEach(div => {div.on("plotly_restyle", function(ed) {
            console.log(ed);
            restyle(ed, divs);

        });
    });

    //restyle function
    function restyle(ed, divs) {
        divs.forEach((div) => {
            //if visibilities are different between both graphs restyle the unchanged graph
            if (ed[0].visible[0] != div.data[ed[1][0]].visible){
                Plotly.restyle(div, {visible: ed[0].visible}, ed[1][0]);
                return;
            //if visibility is already the same, no need to change it, just return nothing
        }  else {
                return;
        }
        });
    }


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

    // Show Progress Bar
    $("#newTaskInProgress").removeClass("hide");


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
            $('#tessResult').show();
            $('#strat1').text(data.strategie1);
            $('#param1').text(data.param1);
            $('#strat2').text(data.strategie2);
            $('#param2').text(data.param2);
            $('#strat3').text(data.strategie3);
            $('#param3').text(data.param3);
            $('#strat4').text(data.strategie4);
            $('#param4').text(data.param4);
            $('#strat5').text(data.strategie5);
            $('#param5').text(data.param5);
            // Hide progress bar
            $("#newTaskInProgress").addClass("hide");
        }
    });
});
