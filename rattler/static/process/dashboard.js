// Upload-Script für das Dashboard

// setzt die Dropzone auf
var myDropzone = new Dropzone("div#dropzoneDiv", {
url: "/file/post", // @TODO vllt noch ändern, ieine URL muss aber da stehen, damit Dropzone funktioniert 
autoQueue: false, // wichtig, damit Files nicht sofort hochgeladen werden
maxFiles: 1 // wieviele Files man gleichzeitig hochladen kann
});
// wird ausgeführt sobald ein File in die Dropzone geladen wird
myDropzone.on("addedfile", function(file){
// FileReader instanzieren
const reader = new FileReader();
// sobald der Reader das File gelesen hat (das passiert bei reader.readAsText(file); unten)
reader.onload = () => {
    // Papaparse parses our csv data into an array
    var results = Papa.parse(reader.result);
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
    console.log("Der Header:");
    console.log(header);
    console.log("restliches Array:");
    console.log(results.data);
    
    // @ TODO Hier evtl. falls für plotly erforderlich alle Array-Inhalte in floats casten
    
    // Nun werden dem User die Spalten angezeigt und er gibt die jeweiligen Daten ein
    // Grundgerüst für Spalten-Formular aufbauen
    $('#schritt1-card').append("<div class='divider'></div>" +
    "                    <div class='section'>" +
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
    "                                            <li>Kreuze bitte auch an, welche Spalte die Zeitreihe enthält.</li>" +
    "                                            <li>Bei der Einordnung der Spalten helfen dir Auszüge aus den" +
    "                                                Daten der jeweiligen Spalte.</li>" +
    "                                        </ul>" +
    "                                    </div>" +
    "                                </li>" +
    "                            </ul>" +
    "                        </div>" +
    "                        <fieldset id='ZeitreihenSpalte' style='border:none'>" +
    "                            <!-- Reihe aller Spalten -->" +
    "                            <div class='row' id='allDataColsRow'>" +
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
        for(j=0; j < results.data.length && j < 51; j++){
            bspDaten += parseFloat(results.data[j][i]);
            if(j==results.data.length-1 || j==50){
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
            var bisherigerName = "               Bisheriger Name: <b>" + header[i] + "</b>";
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
            "               <select style='width: 100%'>" +
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
    // Materialize macht alles wieder schön
    $('select').material_select();
    $('.collapsible').collapsible();
};

// Hier liest der reader die hochgeladene Datei ein.
reader.onabort = () => console.log('file reading was aborted');
reader.onerror = () => console.log('file reading has failed');
reader.readAsText(file);
});

