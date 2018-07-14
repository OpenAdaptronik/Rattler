from django.shortcuts import render, HttpResponseRedirect
from apps.calc.measurement import measurement_obj
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from .json import NumPyArangeEncoder
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

    # copied from index function and deleted stuff we don't need here
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
        'zeitreihenSpalte': json.dumps(measurement.timeIndex, cls=NumPyArangeEncoder),
        'jsonHeaderRealJson': json.dumps(header_list, cls=NumPyArangeEncoder),
        'jsonEinheitenRealJson': json.dumps(einheiten_list, cls=NumPyArangeEncoder),
        'jsonHeaderAndUnits': zip(header_list, einheiten_list),
        'data': data,
        'jsonMInstrumentsRealJson': json.dumps(mInstruments_list, cls=NumPyArangeEncoder),
        'experimentId': experimentId,
        'experimentName': experimentName,
        'numOfCols': datarow_amount,
        'projectId': projectId,
        'dateFormat': settings.DATE_FORMAT,
        'dateCreated': dateCreated,
        'timerow': timerow,
        'current_user_id': curruser_id,
        'experiment_owner_id': expowner_id,
    }

    #Safe all Data from the measurement object into the session storage to get them when applying filter
    request.session['measurementData'] = json.dumps(measurement.data, cls=NumPyArangeEncoder)
    request.session['measurementHeader'] = json.dumps(measurement.colNames, cls=NumPyArangeEncoder)
    request.session['measurementUnits'] = json.dumps(measurement.colUnits, cls=NumPyArangeEncoder)
    request.session['measurementTimeIndex'] = json.dumps(measurement.timeIndex, cls=NumPyArangeEncoder)


    return render(request, "analysis/index.html", dataForRender)


@login_required
def renew_data(request):
    if request.method != 'POST':
       return HttpResponseRedirect('/dashboard/')

    #Recreate measurement object from the session storage
    measurement = measurement_obj.Measurement(request.session['measurementData'],request.session['measurementHeader'],
                                   request.session['measurementUnits'],request.session['measurementTimeIndex'])

    # Number of Columns
    anzSpalten = len(measurement.data[0])


    '''
    Modify the Data:

    1. Check and Apply Resample
    2. Filter
        --> Check and Apply Highpass & Lowpass
        --> Check and Apply Highpass
        --> Check and Apply Lowpass
    3. Check and Apply the Fourrier Transformation
    '''


    if request.POST.get('resampling', '') == 'true':
        resamplingScale = request.POST.get('resamplingScale', '')
        if resamplingScale == '': #Check Resampling
            measurement.resample_data() #Apply Resampling
        else:
            measurement.resample_data(float(resamplingScale)) #Apply Resampling with Parameter


    # Iterate over all Data Column and apply the column filter
    for i in range(0, anzSpalten):
        if i != measurement.timeIndex:
            hochpassOrder = request.POST.get('hochpassOrder' + str(i), '')
            hochpassCofreq = request.POST.get('hochpassCofreq' + str(i), '')
            tiefpassOrder = request.POST.get('tiefpassOrder' + str(i), '')
            tiefpassCofreq = request.POST.get('tiefpassCofreq' + str(i), '')
            if request.POST.get('hochpass' + str(i), '') == 'true' and request.POST.get('tiefpass' + str(i),'') == 'true':
                if hochpassOrder != '':
                    if hochpassCofreq != '' and tiefpassCofreq != '':

                        measurement.butterworth_band_filter(data_index=i, lowcut=float(tiefpassCofreq),
                                                          highcut=float(hochpassCofreq), order=int(hochpassOrder))
                    elif hochpassCofreq != '':
                        measurement.butterworth_band_filter(data_index=i,
                                                          highcut=float(hochpassCofreq), order=int(hochpassOrder))
                    elif tiefpassCofreq != '':
                        measurement.butterworth_band_filter(data_index=i,
                                                          lowcut=float(tiefpassCofreq), order=int(hochpassOrder))
                    else:
                        measurement.butterworth_band_filter(data_index=i, order=int(hochpassOrder))
                elif hochpassCofreq != '':
                    if tiefpassCofreq != '':
                        measurement.butterworth_band_filter(data_index=i, lowcut=float(tiefpassCofreq),
                                                          highcut=float(hochpassCofreq))
                    else:
                        measurement.butterworth_band_filter(data_index=i, highcut=float(hochpassCofreq))
                elif tiefpassCofreq != '':
                    measurement.butterworth_band_filter(data_index=i, lowcut=float(tiefpassCofreq))
                else:
                    measurement.log = 'JOJOJO';
                    measurement.butterworth_band_filter(data_index=i)
            else:
                if request.POST.get('hochpass' + str(i), '') == 'true':
                    if hochpassOrder != '' and hochpassCofreq != '':
                        measurement.butterworth_filter(data_index=i, cofreq=float(hochpassCofreq),
                                                     order=int(hochpassOrder), mode='high')
                    elif hochpassOrder != '':
                        measurement.butterworth_filter(data_index=i,
                                                     order=int(hochpassOrder), mode='high')
                    elif hochpassCofreq != '':
                        measurement.butterworth_filter(data_index=i, cofreq=float(hochpassCofreq), mode='high')
                    else:
                        measurement.butterworth_filter(data_index=i, mode='high')
                if request.POST.get('tiefpass' + str(i), '') == 'true':
                    if tiefpassOrder != '' and tiefpassCofreq != '':
                        measurement.butterworth_filter(data_index=i, cofreq=float(tiefpassCofreq),
                                                     order=int(tiefpassOrder), mode='low')
                    elif tiefpassOrder != '':
                        measurement.butterworth_filter(data_index=i,
                                                     order=int(tiefpassOrder), mode='low')
                    elif tiefpassCofreq != '':
                        measurement.butterworth_filter(data_index=i, cofreq=float(tiefpassCofreq), mode='low')
                    else:
                        measurement.butterworth_filter(data_index=i, mode='low')
            #measurement.log = request.POST.get('gauss' + str(i), '')
            if request.POST.get('gauss' + str(i), '') == 'true':
                gaussStd = request.POST.get('gaussStd' + str(i), '')
                gaussM = request.POST.get('gaussM' + str(i), '')
                if gaussStd != '' and gaussM != '':
                    measurement.gaussian_filter(index=i, gauss_M=int(gaussM), gauss_std=float(gaussStd))
                elif gaussStd != '':
                    measurement.gaussian_filter(index=i, gauss_std=float(gaussStd))
                elif gaussM != '':
                    measurement.gaussian_filter(index=i, gauss_M=int(gaussM))
                else:
                    measurement.gaussian_filter(index=i)


    if request.POST.get('fourier') == 'true':
        fourierval =request.POST.get('fourierval', '')
        if fourierval == '':
            measurement.fourier_transform()
        else:
            measurement.fourier_transform(fourierval=fourierval)


    # Daten zum Rendern vorbereiten
    dataForRender = {
        'jsonData': json.dumps(measurement.data, cls=NumPyArangeEncoder),
        'jsonHeader': json.dumps(measurement.colNames, cls=NumPyArangeEncoder),
        'jsonEinheiten': json.dumps(measurement.colUnits, cls=NumPyArangeEncoder),
        'zeitreihenSpalte': json.dumps(measurement.timeIndex, cls=NumPyArangeEncoder),
    }


    # Safe all Data from the measurement object into the session storage to get them when applying filter
    request.session['measurementDataNew'] = json.dumps(measurement.data, cls=NumPyArangeEncoder)
    request.session['measurementHeaderNew'] = json.dumps(measurement.colNames, cls=NumPyArangeEncoder)
    request.session['measurementUnitsNew'] = json.dumps(measurement.colUnits, cls=NumPyArangeEncoder)
    request.session['measurementTimeIndexNew'] = json.dumps(measurement.timeIndex, cls=NumPyArangeEncoder)

    return JsonResponse(dataForRender)


@login_required
def newESave(request):
    # those are the titles of the columns in an array
    jsonHeader = request.session['measurementHeaderNew']
    # those are the units of the columns in an array
    jsonEinheiten = request.session['measurementUnitsNew']
    # those are the units of the columns in an array
    jsonMeasurementInstruments = request.POST.get("jsonMeasurementInstruments", "")
    # this is the column which contains the x axis (= time; also called "timeindex"), MUSS AUCH IN DIE DB!
    zeitreihenSpalte = request.session['measurementTimeIndexNew']
    # Array of the Schwingungs data
    jsonData = request.session['measurementDataNew']
    # ID of the project the new, received from the new.html file and casted to int (just in case :))
    projectId = request.POST.get("projectId", "")
    # Title of the experiment
    experiment_name = request.POST.get("datensatzName", "")
    # Description of the experiment
    description = request.POST.get("experimentDescr", "")



    header = json.loads(jsonHeader)
    units = json.loads(jsonEinheiten)
    # "sensor"/"actuator"/<irgendein anderer String für None>)
    measurement_instruments = json.loads(jsonMeasurementInstruments)
    time_row = json.loads(zeitreihenSpalte)
    data = json.loads(jsonData)
    if len(header) != len(data[0]):
        header.append("undefined")
        units.append("undefined")
        measurement_instruments.append("No")
        
    new_experiment = Experiment(project_id=projectId, timerow=time_row, name=experiment_name, description=description)
    new_experiment.save()
    experiment_id = new_experiment.id
    i = 0
    while i < len(header):
        if measurement_instruments[i] == 'Ac':
            new_datarow = Datarow(experiment_id=experiment_id, unit=units[i],
                                  name=header[i], measuring_instrument='Ac')
        elif measurement_instruments[i] == 'Se':
            new_datarow = Datarow(experiment_id=experiment_id, unit=units[i],
                                  name=header[i], measuring_instrument='Se')
        else:
            new_datarow = Datarow(experiment_id=experiment_id, unit=units[i],
                                  name=header[i], measuring_instrument='No')
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
