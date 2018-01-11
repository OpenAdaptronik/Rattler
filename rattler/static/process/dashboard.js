Dropzone.autoDiscover = false;
$( document ).ready(function() {

    $('.tooltipped').tooltip({delay: 50});    

    // setzt die Dropzone auf --> @TODO Überarbeiten, damit die komischen UI-Fehler der Dropzone nicht auftreten
    var myDropzone = new Dropzone("div#dropzoneDiv", {
        url: "/file/post", // @TODO vllt noch ändern, ieine URL muss aber da stehen, damit Dropzone funktioniert
        addRemoveLinks: false,
        autoQueue: false, // wichtig, damit Files nicht sofort hochgeladen werden
        maxFiles: 1 // wieviele Files man gleichzeitig hochladen kann 
    });
    // wird ausgeführt sobald ein File in die Dropzone geladen wird
    myDropzone.on("addedfile", function(file){
        // FileReader instanzieren
        const reader = new FileReader();
        // sobald der Reader das File gelesen hat (das passiert bei reader.readAsText(file); unten)
        reader.onload = () => {
            // Dropzone disablen
            myDropzone.disable();
            // Bereich mit Dropzone löschen
            $("#dataUploadSection").remove();
            // Papaparse parses our csv data into an array
            var results = Papa.parse(reader.result);
            // Falls letzte Zeile(n) leer ist/sind, wird sie entfernt
            for(i = results.data.length - 1; i >= 0 && results.data[i][0] == ""; i--){
                results.data.splice(i, 1); // entfernt die Zeile i ("ab Zeile i wird 1 Zeile entfernt") 
            };
            //console.log(results.data);
            // Anz. der Spalten abspeichern
            anzSpalten = results.data[0].length;
            // Leeren Header erstellen
            var header = [];
            for(i=0; i < anzSpalten; i++){
                header[i] = "";
            }
            // Über alle Elemente der ersten Zeile des Arrays laufen.
            for(i = 0; i < anzSpalten; i++){
                /*
                    Es wird versucht, das Element zu einer float zu casten.
                    Falls das Element ein String ist (also wahrscheinlich die Überschrift einer Spalte),
                    so ergibt das Casten (mittels parseFloat) NaN.
                    Das ist für uns das Anzeichen, dass es sich bei der ersten Zeile um den Header handelt.
                    Diesen löschen wir mittels .shift() aus dem Array heraus und speichern ihn in der Variable header.
                */
                if(isNaN(parseFloat(results.data[0][i]))){
                    header = results.data.shift();
                    break;
                }
            }
            // Jetzt fangen die Daten in jedem Fall bei Zeile 0 an.

            // Einige Ausgaben zur Überprüfung:
            /*
            console.log("Der Header:");
            console.log(header);
            console.log("restliches Array:");
            console.log(results.data);
            */
            
            // @ TODO Hier evtl. falls für plotly erforderlich alle Array-Inhalte in floats casten
            
            // Nun werden dem User die Spalten angezeigt und er gibt die jeweiligen Daten ein
            // Grundgerüst für Spalten-Formular aufbauen
            $('#schritt1-card').append("" +
            "                    <div class='section' id='spaltenInfosDiv' style='margin:0; padding-bottom:0'>" +
            "                        <div class='row' style='margin:0;'>" +
            "                            Wir haben deine Datei analysiert.<br/>" +
            "                            Aber: <b>was steht in welcher Spalte?</b><br/>" +
            "                            <ul class='collapsible collapsible-accordion' data-collapsible='accordion' style=''>" +
            "                                <li>" +
            "                                    <div class='collapsible-header'><i class='material-icons'>help</i>Hilfe beim Ausfüllen</div>" +
            "                                    <div class='collapsible-body'>" +
            "                                        <ul class='browser-default' style='margin:0;padding:0 0 0 15px;'>" +
            "                                            <li>Die <u>Spaltennamen</u> sind für dich zur Orientierung.</li>" +
            "                                            <li>Die eingestellten <u>Einheiten</u> wird auch unser Programm" +
            "                                                im weiteren Verlauf verwenden, lass dabei also bitte" +
            "                                                Sorgfalt walten, damit du die richtigen Ergebnisse erhälst.</li>" +
            "                                            <li>Kreuze bitte auch an, welche Spalte die Zeitreihe enthält." +
                                                            "Diese dient gleich als x-Achse der ersten Visualisierung.</li>" +
            "                                            <li>Bei der Einordnung der Spalten helfen dir Auszüge aus den" +
            "                                                Daten der jeweiligen Spalte.</li>" +
            "                                        </ul>" +
            "                                    </div>" +
            "                                </li>" +
            "                            </ul>" +
            "                        </div>" +
            "                        <fieldset id='ZeitreihenSpalte' style='border:none; padding-bottom: 0'>" +
            "                            <!-- Reihe aller Spalten -->" +
            "                            <div class='row' id='allDataColsRow' style='margin:0'>" +
            "                            </div>" +
            "                        </fieldset>" +
            "                    </div>"   
            );
            // Die einzelnen Datenspalten einfügen
            // Damit die erste Spalte standardmäßig als Zeitreihe ausgewählt ist.
            var checked = "checked='checked'";
            // Variable, die in der For-Schleife verwendet wird, um einige Daten aus der Spalte einzufügen
            var bspDaten = "";
            // for-Schleife über die Datenspalten
            for(i=0; i < anzSpalten; i++){
                // Bsp-Daten vorbereiten
                for(j=0; j < results.data.length && j < 51; j++){
                    bspDaten += parseFloat(results.data[j][i]);
                    if(j!=results.data.length-1 || j!=50){
                        bspDaten += "\r\n";
                    }
                }
                // vor einem Pärchen von 2 Spalten eine Row einfügen
                if(i % 4 == 0){
                    $("#allDataColsRow").append("<div id='dataColumnRow" + i + "' class='row' style='background: #eee; padding: 10px 0'></div>");
                } else if(i % 2 == 0){ // bei jeder 2. Zeile => Zeile leicht grau hinterlegen
                    $("#allDataColsRow").append("<div id='dataColumnRow" + i + "' class='row' style='padding: 10px 0'></div>");
                } 
                // bisheriger Name der Spalte
                if(header[i]!=""){
                    var bisherigerName = "               Bisheriger Name: <b class='bisherigerSpaltenname'>" + header[i] + "</b>";
                } else {
                    var bisherigerName = "";
                }
                $("#dataColumnRow" + (i - (i%2)) ).append("" +
                    "   <div class='col m6 s12' style=''>" +
                    "       <div class='row' style='margin: 0'>" +
                    "           <div class='col s12'>" +
                    "               <b>Spalte " + (Number(i)+1) + "</b>&emsp;" +
                    "               <input name='ZeitreihenSpalte' type='radio' id='ZeitreiheChoiceSpalte" + i + "' value='" + i + "'  " + checked +"/>" +
                    "               <label for='ZeitreiheChoiceSpalte" + i + "'>Zeitreihe</label><br/>" +
                    bisherigerName +
                    "           </div>" +
                    "           <div class='input-field col s12'>" +
                    "               <input name='spaltenname" + i + "' id='spaltenname" + i + "' type='text' value=''>" +
                    "               <label for='spaltenname" + i + "'>Titel</label>" +
                    "           </div>" +
                    "           <div class='input-field col s12' style='z-index: 5000'>" +
                    "               <select style='width: 100%' id='einheitSpalte"+i+"'>" +
                    "                   <optgroup label='Zeit'>" +
                    "                       <option value='ze-ms' selected>ms</option>" +
                    "                       <option value='ze-sec'>sek</option>" +
                    "                       <option value='ze-min'>min</option>" +
                    "                       <option value='ze-h'>h</option>" +
                    "                   </optgroup>" +
                    "                   <optgroup label='Kraft'>" +
                    "                       <option value='kr-n'>N</option>" +
                    "                       <option value='kr-kn'>kN</option>" +
                    "                   </optgroup>" +
                    "                   <optgroup label='Weg'>" +
                    "                       <option value='we-m'>m</option>" +
                    "                       <option value='we-mm'>mm</option>" +
                    "                       <option value='we-cm'>cm</option>" +
                    "                       <option value='we-microm'>µm</option>" +
                    "                   </optgroup>" +
                    "                   <optgroup label='Geschwindigkeit'>" +
                    "                       <option value='ge-m-s'>m/s</option>" +
                    "                       <option value='ge-km-h'>km/h</option>" +
                    "                       <option value='ge-mm-s'>mm/s</option>" +
                    "                   </optgroup>" +
                    "                   <optgroup label='Beschleunigung'>" +
                    "                       <option value='be-m-s2'>m/s²</option>" +
                    "                       <option value='be-g'>g</option>" +
                    "                       <option value='be-mm-s2'>mm/s²</option>" +
                    "                   </optgroup>" +
                    "               </select>" +
                    "               <label>Einheit</label>" +
                    "           </div>" +
                    "           <textarea class='col s12' style='resize: none; width:100%; min-width: 100%; max-width: 100%; height: 100px; max-height: 100px; min-height: 100px; border:none; border-top: 1px solid #ccc;' disabled>" +
                                bspDaten +
                    "           </textarea>" +
                    "       </div>" +
                    "   </div>"
                );
                checked = "";
                bspDaten = "";
            }
            
            // Button zum Überprüfen des Forms einfügen
            $("#allDataColsRow").append(""+
                "   <div id='validateDataColumnFormRow' style='margin:0' class='row'>" +
                "       <button type='button' class='btn waves-effect waves-light' id='validateDataColumnForm' style=position: relative; z-index: auto;'><i class='material-icons left'>timeline</i> Alle Spalten bestimmt!</button>" +
                "   </div>"
                );

            // Materialize macht alles wieder schön
            $('select').material_select();
            $('.collapsible').collapsible();
            
            // Wenn der Button zur Validierung der eingegebenen Spalten-Daten gedrückt wird:
            $("#validateDataColumnForm").click(function() {
                // In welcher Zeile steht die Zeitreihe?
                zeitreihenSpalte = $("input[name='ZeitreihenSpalte']:checked").val();
                //console.log("Die Zeitreihe steht in Spalte: " + zeitreihenSpalte);
                var spaltenTitel = [];
                var spaltenEinheiten = [];
                // Die Titel und Einheiten der Spalten holen
                for(i=0; i < anzSpalten; i++){
                    spaltenTitel[i] = $("#spaltenname" + i).val();
                    spaltenEinheiten[i] = $('#einheitSpalte' + i).val();
                }
                /*
                console.log("Die Spaltentitel:");
                console.log(spaltenTitel);
                console.log("Die Spalteneinheiten:");
                console.log(spaltenEinheiten);
                */

                // Spaltentitel in textarea "#jsonHeader" einfügen, um sie python später zu übergeben
                $("#jsonHeader").html(JSON.stringify(spaltenTitel));
                // Spalteneinheiten in textarea "#jsonEinheiten" einfügen, um sie python später zu übergeben
                $("#jsonEinheiten").html(JSON.stringify(spaltenEinheiten));
                // Zeitreihenspalte in input "#zeitreihenSpalte" einfügen, um sie python später zu übergeben
                $("#zeitreihenSpalte").val(zeitreihenSpalte);

                $("#spaltenInfosDiv").remove();
                $("#neueSchwingungsdatenCol").removeClass("l6");
                $('#schritt1-card').append("<div class='section' id='visualisationSection'>"+
                    "Wir haben die hochgeladenen Daten jetzt für dich visualisiert. "+
                    "Wähle diejenigen aus, die du in die Analyse geben möchtest." +
                    "<div id='graph'></div>"+
                    "<div id='validateGraphSelectionContainer' style='display:inline;' data-position='bottom' data-tooltip='ausgewählter Bereich ist zu groß!'><button type='button' class='btn waves-effect waves-light' id='validateGraphSelection' style=position: relative; z-index: auto;'>Bereich ausgewählt!</button></div>" +
                    "</div>"
                    );
                    
                // read the maxDatarows which is the user's maxDatarows value 
                maxDatarows = Number($("#maxDatarows").val());

                if(results.data.length - 1 > maxDatarows){
                    $("#validateGraphSelection").addClass("disabled");
                    $("#validateGraphSelectionContainer").addClass("tooltipped");
                }
                $('.tooltipped').tooltip({delay: 50});


                // Funktion, um Spalte in 2. Dimension als Zeile auszugeben
                // https://stackoverflow.com/a/34979219
                const arrayColumnAsRow = (arr, n) => arr.map(x => x[n]);
                /*
                console.log("Zeitreihe: ");
                console.log(arrayColumnAsRow(results.data, zeitreihenSpalte));
                */
                var traces = [];
                // s. Variablenname
                zeitreihenSpalteAlsZeile = arrayColumnAsRow(results.data, zeitreihenSpalte);
                /*
                console.log("traces:");
                console.log(traces);
                */

                //var selectorOptions = 
                
                // Plotly: Graph
                    //var d3 = Plotly.d3;
                    var layout = {
                        /*title: 'Erste Visualisierung',*/
                        'xaxis': {
                            autotick: true,
                            //ticks: 'outside',
                            //tickcolor: '#f00',
                            //rangeselector: selectorOptions,
                            rangeslider: {}
                        }
                    }

                    // Alle Spalten durchlaufen und Daten für die Visualisierung aufbereiten
                    for(i=0; i < anzSpalten; i++){ // i = Index über Spalten
                        //if(i!=zeitreihenSpalte){
                            traces[i] = {
                                x: zeitreihenSpalteAlsZeile,
                                y: arrayColumnAsRow(results.data, i),
                                name: spaltenTitel[i] + "(" + spaltenEinheiten[i] + ")",
                                type: 'scatter',
                                line: {
                                    width: 1.5,
                                }
                            }
                        //}
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
                    /*
                    console.log(traces);
                    console.log(layout);
                    */
                    traces[zeitreihenSpalte] = [];
                    traces[zeitreihenSpalte].shift();
                    
                    Plotly.newPlot('graph', traces, layout);
                    
                // Variablen, in denen die Auswahl des Users gespeichert wird.
                // Werden so definiert, dass zu Anfang der ganze Datenbereich ausgewählt ist
                var rangeStart = results.data[0][zeitreihenSpalte];
                /*
                console.log(results.data.length);
                console.log(results.data);
                console.log(results.data[(results.data.length) - 1]);
                console.log(results.data[results.data.length-1][zeitreihenSpalte]);
                */
                var rangeEnd = results.data[results.data.length-1][zeitreihenSpalte];
                //console.log("rangeStart: " + rangeStart + " | rangeEnd: " + rangeEnd);
                

                
                var rangeStartIndex = 0;
                var rangeEndIndex = results.data.length - 1;

                // Funktion, die aufgerufen wird, wenn der 
                document.getElementById("graph").on('plotly_relayout',
                    function(eventdata){
                        // get the rangeStart and rangeEnd
                            if(eventdata['xaxis.range[0]']){
                                rangeStart = eventdata['xaxis.range[0]'];
                                rangeEnd = eventdata['xaxis.range[1]'];
                            } else if (typeof eventdata['xaxis.range'] == 'undefined'){ // when you double click on the graph
                                var rangeStart = results.data[0][zeitreihenSpalte];
                                var rangeEnd = results.data[results.data.length-1][zeitreihenSpalte];
                            } else {
                                rangeStart = eventdata['xaxis.range'][0];
                                rangeEnd = eventdata['xaxis.range'][1];
                            }
                            
                        // get the indices for the rangeStart and rangeEnd
                            for(i = 0; i < results.data.length - 1; i++){
                                if(parseFloat(results.data[i+1][zeitreihenSpalte]) > parseFloat(rangeStart)){
                                    rangeStartIndex = i;
                                    break;
                                }
                            }
                            // Ende bestimmen
                            for(i = results.data.length - 1; i > 0; i--){
                                if(parseFloat(results.data[i-1][zeitreihenSpalte]) < parseFloat(rangeEnd)){
                                    rangeEndIndex = i;
                                    break;
                                }
                            }
                            
                        if(rangeEndIndex-rangeStartIndex > maxDatarows){
                            $("#validateGraphSelection").addClass("disabled");
                            $("#validateGraphSelectionContainer").addClass("tooltipped").attr("data-position","bottom").attr("data-tooltip","ausgewählter Bereich ist zu groß!");
                        } else {
                            $("#validateGraphSelection").removeClass("disabled");
                            $("#validateGraphSelectionContainer").tooltip('remove').DearMrHackerWhyAreYouReadingTheConsoleStopThisThisIsNoneOfYourBusinessDoNotHackUsPlease();
                        }
                        $('.tooltipped').tooltip({delay: 50});

                    });
                
                // sobald der User seinen Bereich im Graphen ausgesucht hat
                $("#validateGraphSelection").click(function() {
                    $("#visualisationSection").remove(); // der Graph wird gelöscht
                    $("#neueSchwingungsdatenCardAction").show(); // 
                    $(".datensatzInformationenFelder").show();
                    $("#neueSchwingungsdatenCol").addClass("l6");
                    //console.log("rangeStart: " + rangeStart + " | rangeEnd: " + rangeEnd);
                    // Der ausgewählte Teil des Graphen wird ausgeschnitten
                        // Schritt 1: Wir suchen die Indizes in results.data raus, die den Begrenzungen des ausgewählten Bereichs entsprechen
                            // Beginn bestimmen
                            var rangeStartIndex = 0;
                            for(i = 0; i < results.data.length - 1; i++){
                                if(parseFloat(results.data[i+1][zeitreihenSpalte]) > parseFloat(rangeStart)){
                                    rangeStartIndex = i;
                                    break;
                                }
                            }
                            // Ende bestimmen
                            var rangeEndIndex = results.data.length - 1;
                            for(i = results.data.length - 1; i > 0; i--){
                                if(parseFloat(results.data[i-1][zeitreihenSpalte]) < parseFloat(rangeEnd)){
                                    rangeEndIndex = i;
                                    break;
                                }
                            }
                        // Schritt 2: tatsächlich ausschneiden, in JSON konvertieren & in Textarea schreiben
                        $("#jsonData").html(JSON.stringify(results.data.slice(rangeStartIndex, rangeEndIndex)));
                }) 
                
                // Nachricht wegen Beta
                /*
                $('#schritt1-card').append("<span style='color: #d00'>" +
                    "An diesem Punkt wird man in Zukunft, nach dem man seine Auswahl getroffen hat, " +
                    "die Analyse starten.<br/>" +
                    "Zudem werden der Graph und das Formular noch etwas schöner gestaltet."
                    );
                */
            });
        };

        // Hier liest der reader die hochgeladene Datei ein.
        reader.onabort = () => console.log('file reading was aborted');
        reader.onerror = () => console.log('file reading has failed');
        reader.readAsText(file);
    });
});
