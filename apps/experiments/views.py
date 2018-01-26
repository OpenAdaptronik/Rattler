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

# Create your views here.
@login_required
def index(request, experimentId):
    # The experiment id is passed in the variable experimentId (see urls.py)
    projectId = Experiment.objects.get(id=experimentId).project_id
    if(not request.user.id == Project.objects.get(id=projectId).user_id and not Project.objects.get(id=projectId).visibility):
       return HttpResponseRedirect('/dashboard/')

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

    jsonHeader = json.dumps(jsonHeader, cls=NumPyArangeEncoder)
    jsonEinheiten = json.dumps(jsonEinheiten, cls=NumPyArangeEncoder)
    jsonData = json.dumps(jsonData, cls=NumPyArangeEncoder)
    zeitreihenSpalte = json.dumps(zeitreihenSpalte, cls=NumPyArangeEncoder)

    # Prepare the Data for Rendering
    dataForRender = {
        'jsonData': jsonData,
        'jsonHeader': jsonHeader,
        'jsonEinheiten': jsonEinheiten,
        'zeitreihenSpalte': zeitreihenSpalte
    }

    # Safe all Data from the measurement object into the session storage to get them when applying filter
    request.session['measurementData'] = jsonData
    request.session['measurementHeader'] = jsonHeader
    request.session['measurementUnits'] = jsonEinheiten
    request.session['measurementTimeIndex'] = zeitreihenSpalte

    return render(request, "experiments/index.html", dataForRender)

# the backend derivation and integration function
def intderivate(request):

    if request.method != 'POST':
       return HttpResponseRedirect('/dashboard/')

    # @TODO: the function should get the data directly from the database. the javascript json request shouldnt submit the data but only the experimentId. 



    measurement = measurement_obj.Measurement(request.session['measurementData'], request.session['measurementHeader'],
                                              request.session['measurementUnits'],
                                              request.session['measurementTimeIndex'])


    dataForRender = {
        'jsonData': json.dumps(measurement.data, cls=NumPyArangeEncoder),
        'jsonHeader': json.dumps(measurement.colNames, cls=NumPyArangeEncoder),
        'jsonEinheiten': json.dumps(measurement.colUnits, cls=NumPyArangeEncoder),
        'zeitreihenSpalte': json.dumps(measurement.timeIndex, cls=NumPyArangeEncoder)
    }
    func = int(request.POST.get('function'))
    first =int(request.POST.get('first'))
    second =int(request.POST.get('second'))

    if (func == 1):
        result = calc.trapez_for_each(dataForRender['jsonData'], first , second)
    else:
        result = calc.numerical_approx(dataForRender['jsonData'], first , second)


    result = json.dumps(result, cls=NumPyArangeEncoder)
    x={'result':result}
    dataForRender.update(x)

    #@TODO: hier neue Spalte in DB speichern

    #return render(request, "experiments/start.html",dataForRender)
    return JsonResponse(dataForRender)

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

# page to upload your csv
@login_required
def newE(request, id):
    # check if the current user owns the project. if he doesnt: redirect him to his dashboard
    if not request.user.id == Project.objects.get(id=id).user_id:
        return HttpResponseRedirect('/dashboard')

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
    time_row = zeitreihenSpalte
    data = json.loads(jsonData)
    # @TODO Huy & Maren: Hier die Daten usw. in die Datenbank speichern
    new_experiment = Experiment(project_id=projectId, timerow=time_row, name=experiment_name, description= description)
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

# derivation and integration "app"
@login_required
def derivate(request, experimentId):
    
    # copied from index function and deleted stuff we dont need here
    # Read Data from DB
    header_list = np.asarray(Datarow.objects.filter(experiment_id=experimentId).values_list('name', flat=True))
    einheiten_list = np.asarray(Datarow.objects.filter(experiment_id=experimentId).values_list('unit', flat=True))
    
    # Prepare the Data for Rendering
    dataForRender = {
        'jsonHeader': header_list,
        'jsonEinheiten': einheiten_list,
        'jsonHeaderAndUnits': zip(header_list, einheiten_list)
    }

    return render(request, "experiments/deriv.html", dataForRender)