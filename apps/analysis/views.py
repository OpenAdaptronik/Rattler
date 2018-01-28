from django.shortcuts import render, HttpResponseRedirect
from apps.calc.measurement import measurement_obj
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from .json import NumPyArangeEncoder

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
        measurement.fourier_transform();

    # Daten zum Rendern vorbereiten
    dataForRender = {
        'jsonData': json.dumps(measurement.data, cls=NumPyArangeEncoder),
        'jsonHeader': json.dumps(measurement.colNames, cls=NumPyArangeEncoder),
        'jsonEinheiten': json.dumps(measurement.colUnits, cls=NumPyArangeEncoder),
        'zeitreihenSpalte': json.dumps(measurement.timeIndex, cls=NumPyArangeEncoder)
    }

    return JsonResponse(dataForRender)
