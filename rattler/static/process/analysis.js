// Die Variablen müssen wegen Jinja in der html-Datei vorbereitet werden!

// Funktion, um Spalte in 2. Dimension als Zeile auszugeben
// https://stackoverflow.com/a/34979219
const arrayColumnAsRow = (arr, n) => arr.map(x => x[n]);
// Plotly: Graph von vorheriger Seite wieder plotten
    var traces = [];
    // s. Variablenname
    zeitreihenSpalteAlsZeile = arrayColumnAsRow(dataArray, zeitreihenSpalte);

    var layout = {
        title: 'Schöner Graph',
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
            showlegend: true,
            hoverinfo: 'all',
            mode: 'lines',
            line: {
                width: 1.5
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
            zeroline: true,
            showline: true,
            autotick: true,
            showticklabels: false,
        }
        if(i!=0){
            layout[yaxisTitle]['overlaying'] = 'y';
        }
    }


    traces[zeitreihenSpalte] = [];
    traces[zeitreihenSpalte].shift();
    Plotly.newPlot('secondGraph', traces,layout);