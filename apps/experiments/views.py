from django.shortcuts import render, HttpResponseRedirect
from apps.calc.measurement import measurement_obj
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
import numpy as np
import apps.calc.measurement.calculus as calc
from apps.analysis.json import NumPyArangeEncoder
from apps.projects.models import Experiment, Project, Datarow, Value
import numpy as np
from django.conf import settings
from django.core.exceptions import PermissionDenied
from apps.projects.models import MeasurementInstruments
from datetime import datetime
from django.utils import timezone


# Create your views here.
@login_required
def index(request, experimentId):
    # The experiment id is passed in the variable experimentId (see urls.py)

    # current user
    curruser_id = request.user.id
    projectId = Experiment.objects.get(id=experimentId).project_id
    # owner of experiment
    expowner_id = Project.objects.get(id=projectId).user_id
    if not curruser_id == expowner_id and not Project.objects.get(id=projectId).visibility:
            raise PermissionDenied()

    # Read Data from DB
    header_list = Datarow.objects.filter(experiment_id=experimentId).values_list('name', flat=True)
    jsonHeader = np.asarray(header_list)
    einheiten_list = Datarow.objects.filter(experiment_id=experimentId).values_list('unit', flat=True)
    jsonEinheiten = np.asarray(einheiten_list)
    zeitreihenSpalte = Experiment.objects.get(id=experimentId).timerow
    datarow_id = Datarow.objects.filter(experiment_id=experimentId).values_list('id', flat=True)
    value_amount = len(Value.objects.filter(datarow_id=datarow_id[0]))
    datarow_amount = len(datarow_id)
    #values_wrongorder, filled with 0
    values_wo = [0] * datarow_amount
    #fill values_wo with only datarow_amount-times of database fetches
    i = 0
    while i < datarow_amount:
        values_wo[i] = Value.objects.filter(datarow_id=datarow_id[i]).values_list('value', flat=True)
        i += 1
    # order the values in values_wo, so that they can be used without database fetching
    jsonData = np.transpose(values_wo).astype(float)

    experimentName = Experiment.objects.get(id=experimentId).name
    experimentDateCreated = Experiment.objects.get(id=experimentId).created
    # @TODO hier noch anderes Datum, sobald Modell da ist
    experimentDescr = Experiment.objects.get(id=experimentId).description
    projectName = Project.objects.get(id=projectId).name

    jsonHeader = json.dumps(jsonHeader, cls=NumPyArangeEncoder)
    jsonEinheiten = json.dumps(jsonEinheiten, cls=NumPyArangeEncoder)
    jsonData = json.dumps(jsonData, cls=NumPyArangeEncoder)
    zeitreihenSpalte = json.dumps(zeitreihenSpalte, cls=NumPyArangeEncoder)

    # Prepare the Data for Rendering
    dataForRender = {
        'jsonData': jsonData,
        'jsonHeader': jsonHeader,
        'jsonEinheiten': jsonEinheiten,
        'zeitreihenSpalte': zeitreihenSpalte,
        'projectId': projectId,
        'experimentId': experimentId,
        'experimentName': experimentName,
        'experimentDateCreated': experimentDateCreated,
        'experimentDescr': experimentDescr,
        'projectName': projectName,
        'current_user_id': curruser_id,
        'experiment_owner_id': expowner_id,
    }

    # Safe all Data from the measurement object into the session storage to get them when applying filter
    request.session['measurementData'] = jsonData
    request.session['measurementHeader'] = jsonHeader
    request.session['measurementUnits'] = jsonEinheiten
    request.session['measurementTimeIndex'] = zeitreihenSpalte

    return render(request, "experiments/index.html", dataForRender)


# page to upload your csv
@login_required
def newE(request, id):
    # check if the current user owns the project. if he doesnt: redirect him to his dashboard
    if not request.user.id == Project.objects.get(id=id).user_id:
            raise PermissionDenied()

    dataForRender = {
        'projectId': id,
        'dateFormat': settings.DATE_FORMAT
    }

    return render(request, "experiments/new.html", dataForRender)


def month_to_string(month):
    months = {'Januar': 1, 'Februar': 2, 'März': 3, 'April': 4, 'Mai': 5, 'Juni': 6,
              'Juli': 7, 'August': 8, 'September': 9, 'Oktober': 10, 'November': 11, 'Dezember': 12}
    return months[month]

# is called after the user uploaded his csv. file
@login_required
def newESave(request):
    # titles in an array
    jsonHeader = request.POST.get("jsonHeader", "")
    header = json.loads(jsonHeader)
    empty_array = [None] * len(header)
    # units in an array
    jsonEinheiten = request.POST.get("jsonEinheiten", "")
    # measurement instruments in an array
    jsonMeasurementInstruments = request.POST.get("jsonMeasurementInstruments", "")
    # data types in an array
    jsonDataType = request.POST.get("jsonDataType", json.dumps(empty_array, cls=NumPyArangeEncoder))
    # data format in an array
    jsonDataFormat = request.POST.get("jsonDataFormat", json.dumps(empty_array, cls=NumPyArangeEncoder))
    # function types in an array
    jsonFunctionType = request.POST.get("jsonFunctionType", json.dumps(empty_array, cls=NumPyArangeEncoder))
    # response directions in an array
    jsonResName = request.POST.get("jsonResName", json.dumps(empty_array, cls=NumPyArangeEncoder))
    # response nodes in an array
    jsonResNode = request.POST.get("jsonResNode", json.dumps(empty_array, cls=NumPyArangeEncoder))
    # response directions in an array
    jsonResDir = request.POST.get("jsonResDir", json.dumps(empty_array, cls=NumPyArangeEncoder))
    # reference names in an array
    jsonRefName = request.POST.get("jsonRefName", json.dumps(empty_array, cls=NumPyArangeEncoder))
    # reference nodes in an array
    jsonRefNode = request.POST.get("jsonRefNode", json.dumps(empty_array, cls=NumPyArangeEncoder))
    # reference directions in an array
    jsonRefDir = request.POST.get("jsonRefDir", json.dumps(empty_array, cls=NumPyArangeEncoder))
    # column which contains the x axis (= time)
    zeitreihenSpalte = request.POST.get("zeitreihenSpalte", "")
    # Array of the vibration-data
    jsonData = request.POST.get("jsonData", "")
    # ID of the new project
    projectId = request.POST.get("projectId", "")
    # title of the experiment
    experiment_name = request.POST.get("datensatzName", "")
    # date the experiment took place
    experimentDate = request.POST.get("erfassungsDatum", "")

    # format date so that it fits into the model 'Day, DD. Month, YYYY'  -> timezone aware object
    if experimentDate == '':
        experimentDate = 0
    else:
        experimentDate = experimentDate.split(' ')
        experimentDate = datetime(int(experimentDate[3]), month_to_string(experimentDate[2]),
                                  int(experimentDate[1].rstrip('.')))
        experimentDate = timezone.make_aware(experimentDate, timezone.get_current_timezone())

    description = request.POST.get("experimentDescr", "")

    #decoding json arrays
    units = json.loads(jsonEinheiten)
    measurement_instruments = json.loads(jsonMeasurementInstruments)
    data_type = json.loads(jsonDataType)
    data_format = json.loads(jsonDataFormat)
    function_type = json.loads(jsonFunctionType)
    res_name = json.loads(jsonResName)
    res_node = json.loads(jsonResNode)
    res_dir = json.loads(jsonResDir)
    ref_name = json.loads(jsonRefName)
    ref_node = json.loads(jsonRefNode)
    ref_dir = json.loads(jsonRefDir)

    time_row = zeitreihenSpalte
    data = json.loads(jsonData)
    if experimentDate == 0:
        new_experiment = Experiment(project_id=projectId, timerow=time_row, name=experiment_name,
                                    description=description)
    else:
        new_experiment = Experiment(project_id=projectId, timerow=time_row, name=experiment_name,
                                    description=description, measured=experimentDate)
    new_experiment.save()
    experiment_id = new_experiment.id
    i = 0
    while i < len(header):
        if measurement_instruments[i] == 'actuator':
            new_datarow = Datarow(experiment_id=experiment_id, unit=units[i],
                                  name=header[i], data_type=data_type[i],
                                  data_format=data_format[i], function_type=function_type[i],
                                  response_name=res_name[i], response_node=res_node[i],
                                  response_dir=res_dir[i], reference_name=ref_name[i],
                                  reference_node=ref_node[i], reference_dir=ref_dir[i],
                                  measuring_instrument='Ac')
        elif measurement_instruments[i] == 'sensor':
            new_datarow = Datarow(experiment_id=experiment_id, unit=units[i],
                                  name=header[i], data_type=data_type[i],
                                  data_format=data_format[i], function_type=function_type[i],
                                  response_name=res_name[i], response_node=res_node[i],
                                  response_dir=res_dir[i], reference_name=ref_name[i],
                                  reference_node=ref_node[i], reference_dir=ref_dir[i], measuring_instrument='Se')
        else:
            new_datarow = Datarow(experiment_id=experiment_id, unit=units[i],
                                  name=header[i], data_type=data_type[i],
                                  data_format=data_format[i], function_type=function_type[i],
                                  response_name=res_name[i], response_node=res_node[i],
                                  response_dir=res_dir[i], reference_name=ref_name[i],
                                  reference_node=ref_node[i], reference_dir=ref_dir[i], measuring_instrument='No')
        new_datarow.save()
        j = 0
        values_list = []
        while j < len(data):
            values_list.append(Value(value=data[j][i], datarow_id=new_datarow.id))
            j += 1
        Value.objects.bulk_create(values_list)
        i += 1


    # @TODO Diesem Redirect muss noch die ID des neuen Experimentes angegeben werden. Die Seite die da aufgerufen wird, ist die Experiment-Detail-Seite!
    # Zudem müssen wir dann noch die experiments/index.html-Seite und die Funktion index(request) (in diesem File) anpassen, damit sie das Experiment aus der DB liest!
    return HttpResponseRedirect('/experiments/' + str(experiment_id))

# derivation and integration "app"
@login_required
def derivate(request, experimentId):
    projectId = Experiment.objects.get(id=experimentId).project_id
    expowner_id = Project.objects.get(id=projectId).user_id
    curruser_id = request.user.id

    # read graph visibility from post
    graph_visibility = request.POST.get("graphVisibilities", "").split(',')

    # copied from index function and deleted stuff we don't need here
    # Read Data from DB
    header_list = np.asarray(Datarow.objects.filter(experiment_id=experimentId).values_list('name', flat=True))
    einheiten_list = np.asarray(Datarow.objects.filter(experiment_id=experimentId).values_list('unit', flat=True))
    mInstruments_list = np.asarray(Datarow.objects.filter(experiment_id=experimentId).values_list('measuring_instrument', flat=True))
    data_format_list = np.asarray(Datarow.objects.filter(experiment_id=experimentId).values_list('data_format', flat=True))
    experimentName = Experiment.objects.get(id=experimentId).name
    dateCreated = Experiment.objects.get(id=experimentId).created
    timerow = Experiment.objects.get(id=experimentId).timerow
    datarow_id = Datarow.objects.filter(experiment_id=experimentId).values_list('id', flat=True)
    value_amount = len(Value.objects.filter(datarow_id=datarow_id[0]))
    datarow_amount = len(datarow_id)
    # values in the right order will be put in here, but for now initialize with 0
    values_wo = [0] * datarow_amount
    #fill values_wo with only datarow_amount-times of database fetches
    i = 0
    while i < datarow_amount:
        values_wo[i] = Value.objects.filter(datarow_id=datarow_id[i]).values_list('value', flat=True)
        i += 1
    # order the values in values_wo, so that they can be used without database fetching
    data = np.transpose(values_wo).astype(float)

    # convert data to json
    jsonData = json.dumps(data, cls=NumPyArangeEncoder)

    # Prepare the Data for Rendering
    dataForRender = {
        'jsonHeader': header_list,
        'jsonHeaderRealJson': json.dumps(header_list, cls=NumPyArangeEncoder),
        'jsonEinheiten': einheiten_list,
        'jsonEinheitenRealJson': json.dumps(einheiten_list, cls=NumPyArangeEncoder),
        'jsonHeaderAndUnits': zip(header_list, einheiten_list),
        'jsonData': jsonData,
        'jsonMInstrumentsRealJson': json.dumps(mInstruments_list, cls=NumPyArangeEncoder),
        'jsonDataFormat': json.dumps(data_format_list, cls=NumPyArangeEncoder),
        'experimentId': experimentId,
        'experimentName': experimentName,
        'numOfCols': datarow_amount,
        'projectId': projectId,
        'dateFormat': settings.DATE_FORMAT,
        'dateCreated': dateCreated,
        'timerow': timerow,
        'timerowRealJson': json.dumps(timerow, cls=NumPyArangeEncoder),
        'experiment': Experiment.objects.get(id=experimentId),
        'current_user_id': curruser_id,
        'experiment_owner_id': expowner_id,
        'graphVisibility': json.dumps(graph_visibility, cls=NumPyArangeEncoder),
    }

    return render(request, "experiments/deriv.html", dataForRender)


# is called @ the end of the intderiv process
def derivateRefresh(request,experimentId):
    if request.method != 'POST':
        return JsonResponse({"error": "the Request Method hasnt been POST!"})

    # Recreate measurement object from the session storage --> deprecated
    # measurement = measurement_obj.Measurement(request.session['measurementData'],request.session['measurementHeader'],
    #                               request.session['measurementUnits'],request.session['measurementTimeIndex'])
    # jsonHeader = request.POST.get("jsonHeader", "")
    # jsonEinheiten = request.POST.get("jsonEinheiten", "")
    # zeitreihenSpalte = request.POST.get("zeitreihenSpalte", "")
    # jsonData = request.POST.get("intderivresult", "")

    # get the task data
    function =      int(request.POST.get('function'))
    firstCol =      int(request.POST.get('firstCol'))
    secondCol =     int(request.POST.get('secondCol'))
    newColName =    request.POST.get('newColName')
    newColUnit =    request.POST.get('newColUnit')

    # Read Data from DB - copied from index function
    datarow_id = Datarow.objects.filter(experiment_id=experimentId).values_list('id', flat=True)
    value_amount = len(Value.objects.filter(datarow_id=datarow_id[0]))
    datarow_amount = len(datarow_id)
    # values in the right order will be put in here, but for now initialize with 0
    values_wo = [0] * datarow_amount
    #fill values_wo with only datarow_amount-times of database fetches
    i = 0
    while i < datarow_amount:
        values_wo[i] = Value.objects.filter(datarow_id=datarow_id[i]).values_list('value', flat=True)
        i += 1
    # order the values in values_wo, so that they can be used without database fetching
    data = np.transpose(values_wo).astype(float)

    # convert data to json (which wouldnt be necessary if we'd change the trapez_for_each & the numerical
    # _approx function to accepting python lists instead of json arrays)
    jsonData = json.dumps(data, cls=NumPyArangeEncoder)

    # call function: 1 == Integration; 0/Else == Derivation (?)
    if function == 1:
        result = calc.trapez_for_each(jsonData, firstCol, secondCol)
    else:
        result = calc.numerical_approx(jsonData, firstCol, secondCol)


    # convert result to json
    result = json.dumps(result, cls=NumPyArangeEncoder)


    #
    responseData = {

        'result': result,
    }

    # return render(request, "experiments/start.html",dataForRender)
    return JsonResponse(responseData)


# delete an experiment
@login_required
def delete_experiment(request, experimentId):
    project_id = Experiment.objects.get(id=experimentId).project_id
    project_name = Project.objects.get(id=project_id).name
    Experiment.objects.filter(id=experimentId).delete()

    return HttpResponseRedirect('/projects/detail/' + str(project_name) + '/' + str(project_id))

#render the experiment edit page:
@login_required
def render_edit_experiment(request, experimentId):
    experiment = Experiment.objects.get(id=experimentId)
    datarows = Datarow.objects.filter(experiment_id=experimentId)
    amt_datarows = len(datarows)
    datarow_ids = Datarow.objects.filter(experiment_id=experimentId).values_list('id', flat=True)

    data_for_render = {
        'experiment': experiment,
        'datarows': datarows,
        'amt_datarows': amt_datarows,
        'experimentId': experimentId,
        'datarow_ids': datarow_ids,
    }

    return render(request, "experiments/edit.html", data_for_render)


# experiment in database gets changed according to user input
@login_required
def edit_experiment(request, experimentId):
    if request.method != 'POST':
        return HttpResponseRedirect('/dashboard/')

    # get POST data
    datarow_ids = request.POST['datarow_ids']
    experiment_name = request.POST['experiment_name']
    experiment_description = request.POST['experiment_description']
    experiment_measured = request.POST['experiment_measured']
    amt_datarows = request.POST['amt_datarows']

    # prepare POST data for further usage
    datarow_ids = datarow_ids[11:-2].split(', ')
    # format date so that it fits into the model 'Day, DD. Month, YYYY'  -> timezone aware object
    experiment_measured = experiment_measured.split(' ')
    if experiment_measured[0] == 'None' or experiment_measured[0][-1] == '.':
        experiment_measured = 0
    else:
        experiment_measured = datetime(int(experiment_measured[3]), month_to_string(experiment_measured[2]),
                                       int(experiment_measured[1].rstrip('.')))
        experiment_measured = timezone.make_aware(experiment_measured, timezone.get_current_timezone())

    # update database
    if experiment_measured == 0:
        Experiment.objects.filter(id=experimentId).update(name=experiment_name, description=experiment_description)
    else:
        Experiment.objects.filter(id=experimentId).update(name=experiment_name, description=experiment_description,
                                                          measured=experiment_measured)

    i = 0
    while i < int(amt_datarows):
        datarow_name = request.POST['datarow_name' + str(datarow_ids[i])]
        datarow_unit = request.POST['datarow_unit' + str(datarow_ids[i])]
        datarow_measuring_instrument = request.POST['datarow_measuring_instrument' + str(datarow_ids[i])]
        datarow_data_type = request.POST['datarow_data_type' + str(datarow_ids[i])]
        datarow_data_format = request.POST['datarow_data_format' + str(datarow_ids[i])]
        datarow_function_type = request.POST['datarow_function_type' + str(datarow_ids[i])]
        datarow_response_name = request.POST['datarow_res_name' + str(datarow_ids[i])]
        datarow_response_node = request.POST['datarow_res_node' + str(datarow_ids[i])]
        datarow_response_direction = request.POST['datarow_res_dir' + str(datarow_ids[i])]
        datarow_reference_name = request.POST['datarow_ref_name' + str(datarow_ids[i])]
        datarow_reference_node = request.POST['datarow_ref_node' + str(datarow_ids[i])]
        datarow_reference_direction = request.POST['datarow_ref_dir' + str(datarow_ids[i])]
        Datarow.objects.filter(id=datarow_ids[i]).update(name=datarow_name, unit=datarow_unit,
                                                         measuring_instrument=datarow_measuring_instrument,
                                                         data_type=datarow_data_type, data_format=datarow_data_format,
                                                         function_type=datarow_function_type,
                                                         response_name=datarow_response_name,
                                                         response_node=datarow_response_node,
                                                         response_dir=datarow_response_direction,
                                                         reference_name=datarow_reference_name,
                                                         reference_node=datarow_reference_node,
                                                         reference_dir=datarow_reference_direction)
        i = i + 1

    return HttpResponseRedirect('/experiments/' + str(experimentId))
