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

# Create your views here.
@login_required
def index(request, experimentId):
    # The experiment id is passed in the variable experimentId (see urls.py)
    projectId = Experiment.objects.get(id=experimentId).project_id
    if(not request.user.id == Project.objects.get(id=projectId).user_id and not Project.objects.get(id=projectId).visibility):
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
    jsonData = [0] * value_amount
    data_array = [0] * datarow_amount
    i = 0
    while i < value_amount:
        j = 0
        while j < datarow_amount:
            data_array[j] = float(Value.objects.filter(datarow_id=datarow_id[j]).values_list('value', flat=True)[i])
            j += 1
        jsonData[i] = data_array
        data_array = [0] * datarow_amount
        i += 1

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
    }

    # Safe all Data from the measurement object into the session storage to get them when applying filter
    request.session['measurementData'] = jsonData
    request.session['measurementHeader'] = jsonHeader
    request.session['measurementUnits'] = jsonEinheiten
    request.session['measurementTimeIndex'] = zeitreihenSpalte

    return render(request, "experiments/index.html", dataForRender)

# the backend derivation and integration function

# OLD VERSION FROM JÖRG --> delete when finished the real intderiv process
# is called @ the end of the intderiv process
def refreshData(request):
    if request.method != 'POST':
       return HttpResponseRedirect('/dashboard/')

    #Recreate measurement object from the session storage
    measurement = measurement_obj.Measurement(request.session['measurementData'],request.session['measurementHeader'],
                                   request.session['measurementUnits'],request.session['measurementTimeIndex'])
    # jsonHeader = request.POST.get("jsonHeader", "")
    # jsonEinheiten = request.POST.get("jsonEinheiten", "")
    # zeitreihenSpalte = request.POST.get("zeitreihenSpalte", "")
    # jsonData = request.POST.get("intderivresult", "")

    result =request.POST.get('intderivresult')

    # Number of Columns
    anzSpalten = len(measurement.data[0])
    return JsonResponse(result)


# is called @ the end of the intderiv process
def derivateRefresh(request,experimentId):
    if request.method != 'POST':
        return JsonResponse({"error": "the Request Method hasnt been POST!"})

    #Recreate measurement object from the session storage --> deprecated
    #measurement = measurement_obj.Measurement(request.session['measurementData'],request.session['measurementHeader'],
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
    data = [0] * value_amount
    data_array = [0] * datarow_amount
    i = 0
    while i < value_amount:
        j = 0
        while j < datarow_amount:
            data_array[j] = float(Value.objects.filter(datarow_id=datarow_id[j]).values_list('value', flat=True)[i])
            j += 1
        data[i] = data_array
        data_array = [0] * datarow_amount
        i += 1

    # convert data to json (which wouldnt be necessary if we'd change the trapez_for_each & the numerical_approx function to accepting python lists instead of json arrays)
    jsonData = json.dumps(data, cls=NumPyArangeEncoder)

    # call function: 1 == Integration; 0/Else == Derivation (?)
    if (function == 1):
        result = calc.trapez_for_each(jsonData, firstCol, secondCol)
    else:
        result = calc.numerical_approx(jsonData, firstCol, secondCol)

    #@TODO: hier neue Spalte in DB speichern

    # convert result to json
    result = json.dumps(result, cls=NumPyArangeEncoder)

    # 
    responseData = {
        'result': result,
    }

    #return render(request, "experiments/start.html",dataForRender)
    return JsonResponse(responseData)

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

# is called after the user uploaded his csv. file
@login_required
def newESave(request):
    # those are the titles of the columns in an array
    jsonHeader = request.POST.get("jsonHeader", "")
    # those are the units of the columns in an array
    jsonEinheiten = request.POST.get("jsonEinheiten", "")
    # those are the units of the columns in an array
    jsonMeasurementInstruments = request.POST.get("jsonMeasurementInstruments", "")
    # this is the column which contains the x axis (= time; also called "timeindex"), MUSS AUCH IN DIE DB!
    zeitreihenSpalte = request.POST.get("zeitreihenSpalte", "")
    # Array of the Schwingungs data
    jsonData = request.POST.get("jsonData", "")
    # ID of the project the new, received from the new.html file and casted to int (just in case :))
    projectId = request.POST.get("projectId", "")
    # Title of the experiment
    experiment_name = request.POST.get("datensatzName", "")
    # Date the experiment took place
    experimentDate = request.POST.get("erfassungsDatum", "")
    # Description of the experiment
    description = request.POST.get("experimentDescr", "")
    
    #experiment_date = json.loads(experimentDate)
    header = json.loads(jsonHeader)
    units = json.loads(jsonEinheiten)
    # @ MAREN & HUY: Array über die Spalten, das für jede Spalte das Messinstrument enthält (Also entweder "sensor"/"actuator"/<irgendein anderer String für None>)
    measurement_instruments = json.loads(jsonMeasurementInstruments)
    time_row = zeitreihenSpalte
    data = json.loads(jsonData)
    # @TODO Huy & Maren: Hier die Daten usw. in die Datenbank speichern
    new_experiment = Experiment(project_id=projectId, timerow=time_row, name=experiment_name, description=description)
    new_experiment.save()
    experiment_id = new_experiment.id
    i = 0
    while i < len(header):
        if measurement_instruments[i] == 'actuator':
            new_datarow = Datarow(experiment_id=experiment_id, unit=units[i],
                                  name=header[i], measuring_instrument='Ac')
        elif measurement_instruments[i] == 'sensor':
            new_datarow = Datarow(experiment_id=experiment_id, unit=units[i],
                                  name=header[i], measuring_instrument='Se')
        elif measurement_instruments[i] == 'none':
            new_datarow = Datarow(experiment_id=experiment_id, unit=units[i],
                                  name=header[i], measuring_instrument='No')
        new_datarow.save()
        j = 0
        while j < len(data):
            new_value = Value(value=data[j][i], datarow_id=new_datarow.id)
            new_value.save()
            j += 1
        i += 1


    # @TODO Diesem Redirect muss noch die ID des neuen Experimentes angegeben werden. Die Seite die da aufgerufen wird, ist die Experiment-Detail-Seite!
    # Zudem müssen wir dann noch die experiments/index.html-Seite und die Funktion index(request) (in diesem File) anpassen, damit sie das Experiment aus der DB liest!
    return HttpResponseRedirect('/experiments/' + str(experiment_id))

# derivation and integration "app"
@login_required
def derivate(request, experimentId):
    # check if the current user owns the project. if he doesnt: redirect him to his dashboard
    projectId = Experiment.objects.get(id=experimentId).project_id
    if not request.user.id == Project.objects.get(id=projectId).user_id:
            raise PermissionDenied()
    
    # copied from index function and deleted stuff we don't need here
    # Read Data from DB
    header_list = np.asarray(Datarow.objects.filter(experiment_id=experimentId).values_list('name', flat=True))
    einheiten_list = np.asarray(Datarow.objects.filter(experiment_id=experimentId).values_list('unit', flat=True))
    experimentName = Experiment.objects.get(id=experimentId).name
    datarow_id = Datarow.objects.filter(experiment_id=experimentId).values_list('id', flat=True)
    datarow_amount = len(datarow_id)
    
    # Prepare the Data for Rendering
    dataForRender = {
        'jsonHeader': header_list,
        'jsonEinheiten': einheiten_list,
        'jsonHeaderAndUnits': zip(header_list, einheiten_list),
        'experimentId': experimentId,
        'experimentName': experimentName,
        'numOfCols': datarow_amount,
    }

    return render(request, "experiments/deriv.html", dataForRender)