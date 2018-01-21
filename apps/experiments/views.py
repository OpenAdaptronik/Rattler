from django.shortcuts import render, HttpResponseRedirect
from apps.calc.measurement import measurement_obj
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from apps.analysis.json import NumPyArangeEncoder
from apps.projects.models import Experiment, Project, Datarow, Value
import numpy as np

# Create your views here.
@login_required
def index(request, experimentId):


    # The experiment id is passed in the variable experimentId (see urls.py)
    
    # @TODO: Überprüfen, ob der angemeldete User überhaupt Zugriff auf das Projekt hat, dem das Experiment angehört!
    # + sichtbarkeit

    # ownerid = Project.objects.get(id=id).user_id
    # ownerbool = request.User.id == ownerid

    # @TODO: stattdessen Daten aus der Datenbank rauslesen. Vllt sollte man das nicht hier machen, sondern direkt in der HTML --> geht das? macht das Sinn?
    # Read Data from POST request
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

    jsonHeader = json.dumps(jsonHeader, cls=NumPyArangeEncoder)
    jsonEinheiten = json.dumps(jsonEinheiten, cls=NumPyArangeEncoder)
    jsonData = json.dumps(jsonData, cls=NumPyArangeEncoder)
    zeitreihenSpalte = json.dumps(zeitreihenSpalte, cls=NumPyArangeEncoder)
    # Create/Initialize the measurement object
    # data spalten = 2 dimenion
    # data zeile = 1. dimension
    # array Zeile Spalte
    measurement = measurement_obj.Measurement(jsonData, jsonHeader, jsonEinheiten, zeitreihenSpalte)

    # Prepare the Data for Rendering
    dataForRender = {
        'jsonData': json.dumps(measurement.data, cls=NumPyArangeEncoder),
        'jsonHeader': json.dumps(measurement.colNames, cls=NumPyArangeEncoder),
        'jsonEinheiten': json.dumps(measurement.colUnits, cls=NumPyArangeEncoder),
        'zeitreihenSpalte': json.dumps(measurement.timeIndex, cls=NumPyArangeEncoder)
    }

    # Safe all Data from the measurement object into the session storage to get them when applying filter
    request.session['measurementData'] = json.dumps(measurement.data, cls=NumPyArangeEncoder)
    request.session['measurementHeader'] = json.dumps(measurement.colNames, cls=NumPyArangeEncoder)
    request.session['measurementUnits'] = json.dumps(measurement.colUnits, cls=NumPyArangeEncoder)
    request.session['measurementTimeIndex'] = json.dumps(measurement.timeIndex, cls=NumPyArangeEncoder)

    return render(request, "experiments/index.html", dataForRender)

@login_required
def newE(request, id):

    ownerid = Project.objects.get(id=id).user_id
    ownerbool = request.user.id == ownerid

    if ownerbool is not True:
        return HttpResponseRedirect('/dashboard')

    return render(request, "experiments/new.html", {'projectId': id})

@login_required
def newESave(request):
    # those are the titles of the columns in an array
    jsonHeader = request.POST.get("jsonHeader", "")
    # those are the units of the columns in an array
    jsonEinheiten = request.POST.get("jsonEinheiten", "")
    # this is the column which contains the x axis (= time; also called "timeindex"), MUSS AUCH IN DIE DB!
    zeitreihenSpalte = request.POST.get("zeitreihenSpalte", "")
    # Array of the Schwingungs data
    jsonData = request.POST.get("jsonData", "")
    # ID of the project the new, received from the new.html file and casted to int (just in case :))
    projectId = request.POST.get("projectId", "")

    experiment_name = 'Testname'
    header = json.loads(jsonHeader)
    units = json.loads(jsonEinheiten)
    time_row = zeitreihenSpalte
    data = json.loads(jsonData)

    # @TODO Huy & Maren: Hier die Daten usw. in die Datenbank speichern
    new_experiment = Experiment(project_id=projectId, timerow=time_row, name=experiment_name)
    new_experiment.save()
    experiment_id = new_experiment.id
    i = 0
    while i < len(header):
        new_datarow = Datarow(experiment_id=experiment_id, unit=units[i], name=header[i])
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
