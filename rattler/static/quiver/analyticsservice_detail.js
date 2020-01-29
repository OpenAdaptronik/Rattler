function add_table_row(){

    $(document).ready(function() {
    $('select').material_select();
    });

    var table = document.getElementById("parameter_table").children[1];
    var row = table.insertRow(-1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);

    tablelength = table.getElementsByTagName("tr").length;

    name_input_box = document.createElement("input");
    name_input_box.id = "parameter_name_" + (tablelength-1).toString();
    name_input_box.name = "parameter_name_" + (tablelength-1).toString();

    value_input_box = document.createElement("input");
    value_input_box.id = "parameter_value_" + (tablelength-1).toString();
    value_input_box.name = "parameter_value_" + (tablelength-1).toString();

    div = document.createElement("div");
    div.class = "input-field col s12";

    select = document.createElement("select");
    select.id = 'type_select_' + (tablelength-1).toString();
    select.name = 'type_select_' + (tablelength-1).toString();


    option1 = document.createElement("option");
    option1.text = 'Integer';
    option1.value = 'int';
    option2 = document.createElement("option");
    option2.text = 'String';
    option2.value = 'str';
    option3 = document.createElement("option");
    option3.text = 'Float';
    option3.value = 'float';
    option4 = document.createElement("option");
    option4.text = 'Decimal';
    option4.value = 'dec';


    select.appendChild(option1);
    select.appendChild(option2);
    select.appendChild(option3);
    select.appendChild(option4);

    div.appendChild(select);


    type_select_box = div;

    cell1.appendChild(name_input_box);
    cell2.appendChild(value_input_box);
    cell3.appendChild(type_select_box);

    var rowcounter = document.getElementById("rowcounter");
    rowcounter.value = tablelength
    console.log(tablelength)
}

//When button is pressed
$('form').submit(function(event){
    event.preventDefault();

    // disable button until task is finished
    $('#submit_button').prop('disabled', true).addClass('disabled');


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
            //'data1':$("#data1 :selected").val(),
            'project_id': $("input[name='project_checkbox']:checked").val(),
            'rowcounter': $("#rowcounter").val(),
        }

        var rowcounter = $("#rowcounter").val();
        var service_id = $("#service_id").val();
        var i = 0;
        while (i < rowcounter){
            data['parameter_name_' + String(i)] = document.getElementById('parameter_name_' + String(i)).value;
            data['parameter_value_' + String(i)] = document.getElementById('parameter_value_' + String(i)).value;
            data['type_select_' + String(i)] = document.getElementById('type_select_' + String(i)).value;
            i += 1;
        }
        console.log(data)
    $.ajax({
        url: '/quiver/execute_service/' + service_id,
        method: 'post',
        data: data  ,
        cache:false,
        dataType: 'json',
        success: function (data) {

            $('#executeResult').show();
            $('#result').text(data);
            console.log(data)
            // Hide progress bar
            $("#newTaskInProgress").addClass("hide");
            $('#submit_button').prop('disabled', false).removeClass('disabled');

        }
    });
});
