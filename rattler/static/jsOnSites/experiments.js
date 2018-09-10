$( document ).ready(function() {
    // Funktion, um Spalte in 2. Dimension als Zeile auszugeben
    // https://stackoverflow.com/a/34979219
    function arrayColnAsRow(arr, n) {
            return arr.map(function(x) { return x[n]})
        }

    // Plotly: Graph von vorheriger Seite wieder plotten
        var color = ['#005C47', '#FF6600', '#006E94', '#FDC300', '#B28700', '#FF3400'];
        var traces = [];
        // s. Variablenname
        zeitreihenSpalteAlsZeile = arrayColnAsRow(dataArray, zeitreihenSpalte);

    var layout = {
        //title: 'Dein Experiment:',
        xaxis: {
            title: spaltenTitel[zeitreihenSpalte]+' ('+spaltenEinheiten[zeitreihenSpalte]+')',
        },
        'margin': {
            t: 0,
            pad: 0,
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
    };

    // Alle Spalten durchlaufen und Daten für die Visualisierung aufbereiten
    for(var j=0; j < anzSpalten; j++){ // i = Index über Spalten
        traces[j] = {
            x: zeitreihenSpalteAlsZeile,
            y: arrayColnAsRow(dataArray, j),
            name: spaltenTitel[j] + ' ('+spaltenEinheiten[j]+')',
            type: 'scatter',
            line: {
                width: 1.5,
                color: color[j%6]
            }
        }

    }
    traces[zeitreihenSpalte] = [];
    traces[zeitreihenSpalte].shift();

    Plotly.newPlot('firstGraph', traces, layout);

    //create vars for user chosen visibility of graph 


    //Set hidden Data to submit it with the form
    $('#jsonHeader').html(JSON.stringify(spaltenTitel));
    $('#jsonEinheiten').html(JSON.stringify(spaltenEinheiten));
    $('#zeitreihenSpalte').text(zeitreihenSpalte);
    $('#jsonData').html(JSON.stringify(dataArray));

    var deleteButton = document.getElementById("deleteExperimentButton");
    deleteButton.addEventListener("click", changeButton);
    function changeButton() {
      if (deleteButton.type=="button") {
        deleteButton.type = "submit";
        deleteButton.innerHTML = "Unwiderrufliches Löschen!";
        event.preventDefault();
        deleteButton.removeEventListener("click", changeButton);
      }
    }

});
