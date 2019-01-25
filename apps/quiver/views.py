from django.shortcuts import render, HttpResponseRedirect
from apps.calc.measurement import measurement_obj
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from apps.analysis.json import NumPyArangeEncoder
from apps.projects.models import Experiment, Project, Datarow, Value
from django.conf import settings
from django.core.exceptions import PermissionDenied
import numpy as np

# Create your views here.
@login_required
def index(request, experimentId):
    if request.method != 'POST':
        return HttpResponseRedirect('/dashboard/')
    # current user
    curruser_id = request.user.id
    projectId = Experiment.objects.get(id=experimentId).project_id
    # owner of experiment
    expowner_id = Project.objects.get(id=projectId).user_id

    # read graph visibility from post
    graph_visibility = request.POST.get("graphVisibilities", "").split(',')

    # Read Data from DB
    header_list = np.asarray(Datarow.objects.filter(experiment_id=experimentId).values_list('name', flat=True))
    einheiten_list = np.asarray(Datarow.objects.filter(experiment_id=experimentId).values_list('unit', flat=True))
    mInstruments_list = np.asarray(
        Datarow.objects.filter(experiment_id=experimentId).values_list('measuring_instrument', flat=True))
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

    # Create/Initialize the measurement object
    measurement = measurement_obj.Measurement(json.dumps(data, cls=NumPyArangeEncoder),json.dumps(header_list, cls=NumPyArangeEncoder),
                                              json.dumps(einheiten_list, cls=NumPyArangeEncoder),timerow)


    # Prepare the Data for Rendering
    dataForRender = {
        'jsonData': json.dumps(measurement.data, cls=NumPyArangeEncoder),
        'jsonHeader': json.dumps(measurement.colNames, cls=NumPyArangeEncoder),
        'jsonEinheiten': json.dumps(measurement.colUnits, cls=NumPyArangeEncoder),
        'jsonZeitreihenSpalte': json.dumps(measurement.timeIndex, cls=NumPyArangeEncoder),
        'jsonMeasurementInstruments': json.dumps(mInstruments_list, cls=NumPyArangeEncoder),
        'experimentId': experimentId,
        'experimentName': experimentName,
        'projectId': projectId,
        'dateCreated': dateCreated,
        'current_user_id': curruser_id,
        'experiment_owner_id': expowner_id,
        'graphVisibility': json.dumps(graph_visibility, cls=NumPyArangeEncoder),
    }

    # save experimentId to get it in ajax call when refreshing graph
    request.session['experimentId'] = experimentId

    return render(request, "quiver/index.html", dataForRender)
