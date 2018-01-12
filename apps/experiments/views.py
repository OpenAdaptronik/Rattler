from django.shortcuts import render, HttpResponseRedirect
from apps.calc.measurement import measurement_obj
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from apps.analysis.json import NumPyArangeEncoder

# Create your views here.
@login_required
def index(request):
    if request.method != 'POST':
        return HttpResponseRedirect('/dashboard/')

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
