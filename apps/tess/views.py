from django.shortcuts import render
from django.shortcuts import render, HttpResponseRedirect
from apps.calc.measurement import measurement_obj
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from apps.analysis.json import NumPyArangeEncoder


@login_required
def index(request):
    if request.method != 'POST':
        return HttpResponseRedirect('/dashboard/')

    # Read Data from POST request
    jsonHeader = request.POST.get("jsonHeader", "")
    jsonEinheiten = request.POST.get("jsonEinheiten", "")
    zeitreihenSpalte = request.POST.get("zeitreihenSpalte", "")
    jsonData = request.POST.get("jsonData", "")
    graph_visibility = request.POST.get("graphVisibilities", "").split(',')


    # Prepare the Data for Rendering
    dataForRender = {
        'jsonData': jsonData,
        'jsonHeader': jsonHeader,
        'jsonEinheiten': jsonEinheiten,
        'zeitreihenSpalte': zeitreihenSpalte,
        'graphVisibility': json.dumps(graph_visibility, cls=NumPyArangeEncoder),
    }

    #Safe all Data from the measurement object into the session storage to get them when applying filter
    request.session['measurementData'] = jsonData
    request.session['measurementHeader'] = jsonHeader
    request.session['measurementUnits'] = jsonEinheiten
    request.session['measurementTimeIndex'] = zeitreihenSpalte


    return render(request, "tess/index.html", dataForRender)



@login_required
def refresh_data(request):
    if request.method != 'POST':
       return HttpResponseRedirect('/dashboard/')

    # Recreate measurement object from the session storage
    measurement = measurement_obj.Measurement(request.session['measurementData'],request.session['measurementHeader'],
                                             request.session['measurementUnits'],request.session['measurementTimeIndex'])

    # Prepare the Data for Rendering
    tess_result = measurement.call_tess(int(request.POST.get('data1',)), int(request.POST.get('data2',)))
    return JsonResponse(tess_result)
