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
        }]
        }


        // Alle Spalten durchlaufen und Daten für die Visualisierung aufbereiten
        for(var j=0; j < anzSpalten; j++){
            // i = Index über Spalten
            traces[j] = {
                x: zeitreihenSpalteAlsZeile,
                y: arrayColnAsRow(dataArray, j),
                name: spaltenTitel[j] + ' ('+spaltenEinheiten[j]+')',
                type: 'scatter',
                visible: graphVisibility[j-1],
                line: {
                    color: color[j],
                    width: 1.5,
                }
            }

        }
        console.log(dataArray);

        traces[zeitreihenSpalte] = [];
        traces[zeitreihenSpalte].shift();

        Plotly.newPlot('firstGraph', traces, layout);




        //neue Tabellenzeile beim Klicken von "Parameter hinzufügen"-Button hinzufügen
        document.getElementById("addParameter").onclick = insertParameterRow;
        var i = 0;

        function insertParameterRow(){
            var table = document.getElementById("parameterTable").getElementsByTagName('tbody')[0];
            var row = table.children[table.children.length-1];
            var clone = row.cloneNode(true);
            // neue ids für die dropdown festlegen(nach materialize Dokumentation)
            clone.children[1].children[0].children[1].attributes[3].value = i.toString();
            clone.children[1].children[0].children[2].attributes[0].value = i.toString();
            clone.children[1].children[0].children[3].attributes[2].value = i.toString();

            table.appendChild(clone);

            //id des dropdown menüs zum event anhängen definieren
            var selector_string = '#' + i.toString();

            //Klick Event anhängen
            $(selector_string).on('click', 'li', function() {
                //alle ausgewählten optionen entfernen
                $( selector_string + " li" ).removeClass( "active selected" );
                //die ausgewählte option wird hervorgehoben
                $( this ).addClass( "active selected" );
                //die ausgewählte option wird im text-field angezeigt
                clone.children[1].children[0].children[1].attributes[clone.children[1].children[0].children[1].attributes.length-1].value = $( this )[0].textContent;
            });

            //erhöhe i für die nächste reihe
            i += 1;

            //reinitialisiere materialize
            $('.select-dropdown').dropdown();

        }


});
