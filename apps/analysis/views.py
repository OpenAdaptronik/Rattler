from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt

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

    # measurement-Objekt aus den Session-Variablen auslesen und wieder erstellen
    #measurement = read.Measurement(request.session['measurementData'],request.session['measurementHeader'],
    #                               request.session['measurementUnits'],request.session['measurementTimeIndex'])
    
    # Daten aus POST-Request auslesen
    jsonHeader = request.POST.get("jsonHeader", "")
    jsonEinheiten = request.POST.get("jsonEinheiten", "")
    zeitreihenSpalte = request.POST.get("zeitreihenSpalte", "")
    jsonData = request.POST.get("jsonData", "")

    # measurement-Objekt anlegen
    measurement = measurement_obj.Measurement(jsonData,jsonHeader,jsonEinheiten,zeitreihenSpalte)
    
    # Anz der Spalten
    anzSpalten = len(measurement.data[0])
    
    # Resampling?
    if request.POST.get('resampling','') == 'on':
        resamplingScale = request.POST.get('resamplingScale','')
        # Resampling aufrufen
        if resamplingScale == '':
            measurement.resample_data()
        else:
            measurement.resample_data(float(resamplingScale))

    # über alle Spalten iterieren (von 0 bis anzSpalten)
    for i in range(0, anzSpalten):
        if i != measurement.timeIndex:
            hochpassOrder = request.POST.get('hochpassOrder' + str(i),'')
            hochpassCofreq = request.POST.get('hochpassCofreq' + str(i),'')
            tiefpassOrder = request.POST.get('tiefpassOrder' + str(i),'')
            tiefpassCofreq = request.POST.get('tiefpassCofreq' + str(i),'')
            if request.POST.get('hochpass' + str(i),'') == 'on' and request.POST.get('tiefpass' + str(i),'') == 'on':
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
                if request.POST.get('hochpass' + str(i),'') == 'on':
                    if hochpassOrder != '' and hochpassCofreq != '':
                        measurement.butterworth_filter(data_index=i,cofreq=float(hochpassCofreq),
                                                       order= int(hochpassOrder),mode='high')
                    elif hochpassOrder != '':
                        measurement.butterworth_filter(data_index=i,
                                                       order= int(hochpassOrder),mode='high')
                    elif hochpassCofreq != '':
                        measurement.butterworth_filter(data_index=i,cofreq=float(hochpassCofreq),mode='high')
                    else:
                        measurement.butterworth_filter(data_index=i,mode='high')
                if request.POST.get('tiefpass' + str(i),'') == 'on':
                    if tiefpassOrder != '' and tiefpassCofreq != '':
                        measurement.butterworth_filter(data_index=i,cofreq=float(tiefpassCofreq),
                                                       order= int(tiefpassOrder),mode='low')
                    elif tiefpassOrder != '':
                        measurement.butterworth_filter(data_index=i,
                                                       order= int(tiefpassOrder),mode='low')
                    elif tiefpassCofreq != '':
                        measurement.butterworth_filter(data_index=i,cofreq=float(tiefpassCofreq),mode='low')
                    else:
                        measurement.butterworth_filter(data_index=i,mode='low')

            if request.POST.get('gauss' + str(i),'') == 'on':
                gaussStd = request.POST.get('gaussStd' + str(i),'')
                gaussM = request.POST.get('gaussM' + str(i),'')
                if gaussStd != '' and gaussM != '':
                    measurement.gaussian_filter(index=i,gauss_M=gaussM,gauss_std=gaussStd)
                elif gaussStd != '':
                    measurement.gaussian_filter(index=i,gauss_std=gaussStd)
                elif gaussM != '':
                    measurement.gaussian_filter(index=i,gauss_M=gaussM)
                else:
                    measurement.gaussian_filter(index=i)

    # Daten zum Rendern vorbereiten
    dataForRender = {
        'jsonData': json.dumps(measurement.data, cls=NumPyArangeEncoder),
        'jsonHeader': json.dumps(measurement.colNames, cls=NumPyArangeEncoder),
        'jsonEinheiten': json.dumps(measurement.colUnits, cls=NumPyArangeEncoder),
        'zeitreihenSpalte': json.dumps(measurement.timeIndex, cls=NumPyArangeEncoder)
    }


    #measurement in Session-Variable speichern
    request.session['measurementData'] = json.dumps(measurement.data, cls=NumPyArangeEncoder)
    request.session['measurementHeader'] = json.dumps(measurement.colNames, cls=NumPyArangeEncoder)
    request.session['measurementUnits'] = json.dumps(measurement.colUnits, cls=NumPyArangeEncoder)
    request.session['measurementTimeIndex'] = json.dumps(measurement.timeIndex, cls=NumPyArangeEncoder)


    return render(request, "analysis/index.html", dataForRender)


def renew_data(request):
    if request.method != 'POST':
       return HttpResponseRedirect('/dashboard/')




    #measurement-Objekt aus den Session-Variablen auslesen und wieder erstellen
    measurement = measurement_obj.Measurement(request.session['measurementData'],request.session['measurementHeader'],
                                   request.session['measurementUnits'],request.session['measurementTimeIndex'])

    # Anz der Spalten
    anzSpalten = len(measurement.data[0])

    # Resampling?
    if request.POST.get('resampling', '') == 'on':
        resamplingScale = request.POST.get('resamplingScale', '')
        # Resampling aufrufen
        if resamplingScale == '':
            measurement.resample_data()
        else:
            measurement.resample_data(float(resamplingScale))

    # über alle Spalten iterieren (von 0 bis anzSpalten)
    for i in range(0, anzSpalten):
        if i != measurement.timeIndex:
            hochpassOrder = request.POST.get('hochpassOrder' + str(i), '')
            hochpassCofreq = request.POST.get('hochpassCofreq' + str(i), '')
            tiefpassOrder = request.POST.get('tiefpassOrder' + str(i), '')
            tiefpassCofreq = request.POST.get('tiefpassCofreq' + str(i), '')
            if request.POST.get('hochpass' + str(i), '') == 'on' and request.POST.get('tiefpass' + str(i),
                                                                                    '') == 'on':
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
                if request.POST.get('hochpass' + str(i), '') == 'on':
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
                if request.POST.get('tiefpass' + str(i), '') == 'on':
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

            if request.POST.get('gauss' + str(i), '') == 'on':
                gaussStd = request.POST.get('gaussStd' + str(i), '')
                gaussM = request.POST.get('gaussM' + str(i), '')
                if gaussStd != '' and gaussM != '':
                    measurement.gaussian_filter(index=i, gauss_M=gaussM, gauss_std=gaussStd)
                elif gaussStd != '':
                    measurement.gaussian_filter(index=i, gauss_std=gaussStd)
                elif gaussM != '':
                    measurement.gaussian_filter(index=i, gauss_M=gaussM)
                else:
                    measurement.gaussian_filter(index=i)

    # Daten zum Rendern vorbereiten
    dataForRender = {
        'log': request.POST.get('resampling', '') ,
        'jsonData': json.dumps(measurement.data, cls=NumPyArangeEncoder),
        'jsonHeader': json.dumps(measurement.colNames, cls=NumPyArangeEncoder),
        'jsonEinheiten': json.dumps(measurement.colUnits, cls=NumPyArangeEncoder),
        'zeitreihenSpalte': json.dumps(measurement.timeIndex, cls=NumPyArangeEncoder)
    }



    return JsonResponse(dataForRender)