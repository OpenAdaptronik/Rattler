from django.shortcuts import render, HttpResponseRedirect
from apps.calc.measurement import measurement_obj
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from apps.analysis.json import NumPyArangeEncoder
from apps.projects.models import Experiment

# Create your views here.
@login_required
def index(request):
    
    if request.method != 'POST':
        return HttpResponseRedirect('/dashboard/')

    # The experiment id is passed in the variable experimentId (see urls.py)
    
    # @TODO: Überprüfen, ob der angemeldete User überhaupt Zugriff auf das Projekt hat, dem das Experiment angehört!
    
    # @TODO: stattdessen Daten aus der Datenbank rauslesen
    # Read Data from POST request
    jsonHeader = request.POST.get("jsonHeader", "")
    jsonEinheiten = request.POST.get("jsonEinheiten", "")
    zeitreihenSpalte = request.POST.get("zeitreihenSpalte", "")
    jsonData = request.POST.get("jsonData", "")

    # Create/Initialize the measurement object
    measurement = measurement_obj.Measurement(jsonData,jsonHeader,jsonEinheiten,zeitreihenSpalte)


    # Prepare the Data for Rendering
    dataForRender = {
        'jsonData': json.dumps(measurement.data, cls=NumPyArangeEncoder),
        'jsonHeader': json.dumps(measurement.colNames, cls=NumPyArangeEncoder),
        'jsonEinheiten': json.dumps(measurement.colUnits, cls=NumPyArangeEncoder),
        'zeitreihenSpalte': json.dumps(measurement.timeIndex, cls=NumPyArangeEncoder)
    }

    #Safe all Data from the measurement object into the session storage to get them when applying filter
    request.session['measurementData'] = json.dumps(measurement.data, cls=NumPyArangeEncoder)
    request.session['measurementHeader'] = json.dumps(measurement.colNames, cls=NumPyArangeEncoder)
    request.session['measurementUnits'] = json.dumps(measurement.colUnits, cls=NumPyArangeEncoder)
    request.session['measurementTimeIndex'] = json.dumps(measurement.timeIndex, cls=NumPyArangeEncoder)


    return render(request, "experiments/index.html", dataForRender)

@login_required
def newE(request, id):
    # @TODO Huy & Maren: Hier bitte überprüfen, ob die id (=das Projekt) auch dem angemeldeten User gehört, wenn nicht: Redirect auf die Projektübersicht oder das Dashboard etc. (damit man keine Experimente in fremde Projekte einfügen kann!). Ansonsten die return-Zeile hier drunter ausführen
    return render(request, "experiments/new.html", { 'projectId': id })

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
    projectId = int(request.POST.get("projectId", ""))

    # @TODO Huy & Maren: Hier die Daten usw. in die Datenbank speichern
    new_experiment = Experiment(project_id=projectId)
    new_experiment.save()
    # @TODO Diesem Redirect muss noch die ID des neuen Experimentes angegeben werden. Die Seite die da aufgerufen wird, ist die Experiment-Detail-Seite!
    # Zudem müssen wir dann noch die experiments/index.html-Seite und die Funktion index(request) (in diesem File) anpassen, damit sie das Experiment aus der DB liest!
    return HttpResponseRedirect('/experiments/HIER_ID_DES_NEUEN_EXPERIMENTES_EINGEBEN')