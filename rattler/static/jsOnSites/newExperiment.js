// It is important to embed the dropzone.js-file _BEFORE_ this file in your html!
Dropzone.autoDiscover = false;
$( document ).ready(function() {

    $('.tooltipped').tooltip({delay: 50});

    // setting up the dropzone
    var myDropzone = new Dropzone("div#dropzoneDiv", {
        url: "/FAKEURL", // we dont use the url, but dropzone needs one to work properly
        addRemoveLinks: false,
        autoQueue: false, // important so the files arent uploaded directly after dropping them into the dropzone
        maxFiles: 1 // how many files you can upload at the same time
    });

    // setup datepicker in the right language (at the moment hardcoded German) and the right format
    // if you want to include other languages, you might want to take a look @ https://github.com/amsul/pickadate.js/tree/3.5.6/lib/translations
        // get the dateFormat which is the base.py constant "DATE_FORMAT"
        var color = ['#005C47','#FF6600' , '#006E94' , '#FDC300', '#B28700' , '#FF3400']
        var dateFormat = $("#dateFormat").val();
        $('.datepicker').pickadate({
            monthsFull: [ 'Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember' ],
            monthsShort: [ 'Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez' ],
            weekdaysFull: [ 'Sonntag', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag' ],
            weekdaysShort: [ 'So', 'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa' ],
            today: 'Heute',
            clear: 'Löschen',
            close: 'Schließen',
            firstDay: 1,
            format: 'dddd, dd. mmmm yyyy',
            formatSubmit: dateFormat
        });

    // executed when a file is dropped into the dropzone
    myDropzone.on("addedfile", function(file){
        // instance of FileReader
        const reader = new FileReader();
        // when the reader reads the file (see reader.readAsText(file) below)
        reader.onload = function() {
            // disable the Dropzone
            myDropzone.disable();
            // delete the section containing the dropzone
            $("#dataUploadSection").remove();
            $("#schritt1-card card-title").remove();
            // Papaparse parses our csv data into an array
            var results = Papa.parse(reader.result);
            // if rows at the end are empty: delete them
            for(i = results.data.length - 1; i >= 0 && results.data[i][0] == ""; i--){
                results.data.splice(i, 1); // deletes row i ("delete 1 row beginning at row i")
            };
            // amount of cols
            amountOfCols = results.data[0].length;
            // create empty header
            var header = [];
            for(i=0; i < amountOfCols; i++){
                header[i] = "";
            }
            // iterate over all elements of the first row of the array
            for(i = 0; i < amountOfCols; i++){
                /*
                    We try to cast the element to float.
                    If it is a string, we assume it is a header of a column and the cast (parseFloat) results to NaN.
                    The header will be deleted from the array using .shift() and saved to the header array.
                */
                if(isNaN(parseFloat(results.data[0][i]))){
                    header = results.data.shift();
                    break;
                }
            }
            // Now we're sure that the data begins at row 0.

            // Display the cols to the user and make him enter the data
            // build up the scaffold for the column form
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
            "                                            <li>Kreuze bitte auch an, welche Spalte die Zeitreihe enthält.<br/>" +
                                                            "Diese dient gleich als x-Achse der ersten Visualisierung.</li>" +
            "                                            <li>Bei der Einordnung der Spalten helfen dir Auszüge aus den" +
            "                                                Daten der jeweiligen Spalte.</li>" +
            "                                        </ul>" +
            "                                    </div>" +
            "                                </li>" +
            "                            </ul>" +
            "                        </div>" +
            "                        <fieldset id='timeRowCol' style='border:none; padding-bottom: 0'>" +
            "                            <!-- Reihe aller Spalten -->" +
            "                            <div class='row' id='allDataColsRow' style='margin:0'>" +
            "                            </div>" +
            "                        </fieldset>" +
            "                    </div>"   
            );
            // insert the data cols
            // Check the first col as timerow.
            var checked = "checked='checked'";
            // variable used in the for loop below
            var exampleDataVar = "";
            // for loop over the data cols
            for(i=0; i < amountOfCols; i++){
                // prepare example data
                for(j=0; j < results.data.length && j < 51; j++){
                    exampleDataVar += parseFloat(results.data[j][i]);
                    if(j!=results.data.length-1 || j!=50){
                        exampleDataVar += "\r\n";
                    }
                }
                // insert a row before a pair of two  cols
                if(i % 4 == 0){
                    $("#allDataColsRow").append("<div id='dataColumnRow" + i + "' class='row' style='background: #eee; padding: 10px 0'></div>");
                } else if(i % 2 == 0){ // grey background for every 2nd row
                    $("#allDataColsRow").append("<div id='dataColumnRow" + i + "' class='row' style='padding: 10px 0'></div>");
                }
                if(header[i]!=""){
                    var nameSoFar = "               Bisheriger Name: <b class='bisherigerSpaltenname'>" + header[i] + "</b>";
                } else {
                    var nameSoFar = "";
                }
                $("#dataColumnRow" + (i - (i%2)) ).append("" +
                    "   <div class='col m6 s12' style=''>" +
                    "       <div class='row' style='margin: 0'>" +
                    "           <div class='col s12'>" +
                    "               <b>Spalte " + (Number(i)+1) + "</b>&emsp;" +
                    "               <input name='timeRowCol' type='radio' id='ZeitreiheChoiceSpalte" + i + "' value='" + i + "'  " + checked +"/>" +
                    "               <label for='ZeitreiheChoiceSpalte" + i + "'>Zeitreihe</label>" +
                    //"               <br/>" + nameSoFar +
                    "           </div>" +
                    "           <div class='input-field col s12'>" +
                    "               <input name='spaltenname" + i + "' id='spaltenname" + i + "' type='text' value='"+header[i]+"'>" +
                    "               <label for='spaltenname" + i + "'>Titel</label>" +
                    "           </div>" +
                    "           <div class='input-field col s5' style='z-index: 5000'>" +
                    "               <select style='width: 100%' id='einheitSpalte"+i+"'>" +
                    "                   <optgroup label='Zeit'>" +
                    "                       <option value='ms' selected>ms</option>" +
                    "                       <option value='sec'>sek</option>" +
                    "                       <option value='min'>min</option>" +
                    "                       <option value='h'>h</option>" +
                    "                   </optgroup>" +
                    "                   <optgroup label='Kraft'>" +
                    "                       <option value='N'>N</option>" +
                    "                       <option value='kN'>kN</option>" +
                    "                   </optgroup>" +
                    "                   <optgroup label='Weg'>" +
                    "                       <option value='m'>m</option>" +
                    "                       <option value='mm'>mm</option>" +
                    "                       <option value='cm'>cm</option>" +
                    "                       <option value='µm'>µm</option>" +
                    "                   </optgroup>" +
                    "                   <optgroup label='Geschwindigkeit'>" +
                    "                       <option value='m/s'>m/s</option>" +
                    "                       <option value='km/h'>km/h</option>" +
                    "                       <option value='mm/s'>mm/s</option>" +
                    "                   </optgroup>" +
                    "                   <optgroup label='Beschleunigung'>" +
                    "                       <option value='m/s²'>m/s²</option>" +
                    "                       <option value='g'>g</option>" +
                    "                       <option value='mm/s²'>mm/s²</option>" +
                    "                   </optgroup>" +
                    "               </select>" +
                    "               <label>Einheit</label>" +
                    "           </div>" +
                    "           <div class='input-field col s7' style='z-index: 5000'>" +
                    "               <select style='width: 100%' id='measurementInstrument"+i+"'>" +
                    "                       <option value='sensor'>Sensor</option>" +
                    "                       <option value='actuator'>Aktor</option>" +
                    "                       <option value='none' selected>-</option>" +
                    "               </select>" +
                    "               <label>Messinstrument</label>" +
                    "           </div>" +
                    "           <div class='input-field col s12'>" +
                    "               <input name='spaltenname" + i + "' id='spaltenname" + i + "' type='text' value='"+header[i]+"'>" +
                    "               <label for='spaltenname" + i + "'>Titel</label>" +
                    "           </div>" +
                    "           <textarea class='col s12' style='resize: none; width:100%; min-width: 100%; max-width: 100%; height: 100px; max-height: 100px; min-height: 100px; border:none; border-top: 1px solid #ccc;' disabled>" +
                                exampleDataVar +
                    "           </textarea>" +
                    "       </div>" +
                    "   </div>"
                );
                checked = "";
                exampleDataVar = "";
            }

            // Update Materialize Text Fields to make them look fine
            Materialize.updateTextFields();
            
            // insert button for validating the form
            $("#allDataColsRow").append(""+
                "   <div id='validateDataColumnFormRow' style='margin:0' class='row'>" +
                "       <button type='button' class='btn waves-effect waves-light' id='validateDataColumnForm' style=position: relative; z-index: auto;'><i class='material-icons left'>timeline</i> Alle Spalten bestimmt!</button>" +
                "   </div>"
                );

            // materialize makes everthing look perfectly nice beautiful tremendous great
            $('select').material_select();
            $('.collapsible').collapsible();
            
            // when the validate button is pressed
            $("#validateDataColumnForm").click(function() {
                // column of the timerow
                timeRowCol = $("input[name='timeRowCol']:checked").val();
                var colTitles = [];
                var colUnits = [];
                var measurementInstruments = [];
                // get titles and units and measurement instr.s of the cols
                for(i=0; i < amountOfCols; i++){
                    colTitles[i] = $("#spaltenname" + i).val();
                    colUnits[i] = $('#einheitSpalte' + i).val();
                    measurementInstruments[i] = $('#measurementInstrument' + i).val();
                }

                // insert the colTitles of the columns into the hidden textarea "#jsonMeasurementInstruments" to pass them to python later
                $("#jsonHeader").html(JSON.stringify(colTitles));
                // insert the colUnits of the columns into the hidden textarea "#jsonMeasurementInstruments" to pass them to python later
                $("#jsonEinheiten").html(JSON.stringify(colUnits));
                // insert the measurement instruments of the columns into the hidden textarea "#jsonMeasurementInstruments" to pass them to python later
                $("#jsonMeasurementInstruments").html(JSON.stringify(measurementInstruments));
                // timeRowCol in input "#timeRowCol" einfügen, um sie python später zu übergeben
                $("#timeRowCol").val(timeRowCol);

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


                // https://stackoverflow.com/a/34979219
                const arrayColumnAsRow = (arr, n) => arr.map(x => x[n]);
                var traces = [];
                timeColumn = arrayColumnAsRow(results.data, timeRowCol);
                //console.log(timeColumn);
                console.log(colTitles);
                console.log(colUnits);

                // Plotly: Graph
                    //var d3 = Plotly.d3;
                    var layout = {
                        'xaxis': {
                            autotick: true,
                            rangeslider: {}
                        },
                        'margin': {
                            t: 0,
                            pad: 0,
                        },
                    }

                    // iterate through all cols and prepare them for visualisation
                    for(i=0; i < amountOfCols; i++){ // i = index for cols
                        traces[i] = {
                            x: timeColumn,
                            y: arrayColumnAsRow(results.data, i),
                            name: colTitles[i] + "(" + colUnits[i] + ")",
                            type: 'scatter',
                            line: {
                                color: color[i%6],
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
                    traces[timeRowCol] = [];
                    traces[timeRowCol].shift();
                    
                    var d3 = Plotly.d3;
                    var node = d3.select('#graph').node();

                    Plotly.newPlot(node, traces, layout);

                    window.onresize = function() {
                        Plotly.Plots.resize(node);
                    };
                    
                // vars containing the selection of the user
                // at the beginning, the whole data is selected
                var rangeStart = results.data[0][timeRowCol];
                var rangeEnd = results.data[results.data.length-1][timeRowCol];
                
                var rangeStartIndex = 0;
                var rangeEndIndex = results.data.length - 1;

                // called when user changes the selection
                document.getElementById("graph").on('plotly_relayout', function(eventdata){
                    // get the rangeStart and rangeEnd
                        if(eventdata['xaxis.range[0]']){
                            rangeStart = eventdata['xaxis.range[0]'];
                            rangeEnd = eventdata['xaxis.range[1]'];
                        } else if(typeof eventdata['xaxis.range'] == 'undefined'){ // when you double click on the graph
                            var rangeStart = results.data[0][timeRowCol];
                            var rangeEnd = results.data[results.data.length-1][timeRowCol];
                        } else {
                            rangeStart = eventdata['xaxis.range'][0];
                            rangeEnd = eventdata['xaxis.range'][1];
                        }
                        
                    // get the indices for the rangeStart and rangeEnd
                        for(i = 0; i < results.data.length - 1; i++){
                            if(parseFloat(results.data[i+1][timeRowCol]) > parseFloat(rangeStart)){
                                rangeStartIndex = i;
                                break;
                            }
                        }
                        // determinate end
                        for(i = results.data.length - 1; i > 0; i--){
                            if(parseFloat(results.data[i-1][timeRowCol]) < parseFloat(rangeEnd)){
                                rangeEndIndex = i;
                                break;
                            }
                        }
                        
                    if(rangeEndIndex-rangeStartIndex > maxDatarows){
                        $("#validateGraphSelection").addClass("disabled");
                        $("#validateGraphSelectionContainer").addClass("tooltipped").attr("data-position","bottom").attr("data-tooltip","ausgewählter Bereich ist zu groß!");
                    } else {
                        $("#validateGraphSelection").removeClass("disabled");
                        $('.tooltipped').tooltip('remove');
                        $("#validateGraphSelectionContainer").removeClass('tooltipped');
                    }
                    $('.tooltipped').tooltip({delay: 50});
                });
                
                // when the user has finished selecting
                $("#validateGraphSelection").click(function() {
                    $("#visualisationSection").remove(); // deleting the graph
                    $("#neueSchwingungsdatenCardAction").show(); // 
                    $(".datensatzInformationenFelder").show();
                    $("#neueSchwingungsdatenCol").addClass("l6");
                    // cut the data to the range the user selected, convert it in JSON and write it in the textarea w/ id=jsonData & name=jsonData
                    // rangeStartIndex and rangeEndIndex are variables whose scope is one level higher. They might be altered by the event function which is called when the user changes the range.
                    $("#jsonData").html(JSON.stringify(results.data.slice(rangeStartIndex, rangeEndIndex)));
                })
            });
        };

        // reader reads the data
        reader.onabort = function() { console.log('file reading was aborted')};
        reader.onerror = function() { console.log('file reading has failed')};
        reader.readAsText(file);
    });
});
