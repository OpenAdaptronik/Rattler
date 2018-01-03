from django.shortcuts import render
from apps.calc.read_data import read
from django.contrib.auth.decorators import login_required
import json
from .json import NumPyArangeEncoder


# Create your views here.
@login_required
def fromDashboard(request):
    if request.method == 'POST':
        # Variablen aus dem Post-Request auslesen
        jsonHeader = request.POST.get("jsonHeader", "")
        jsonEinheiten = request.POST.get("jsonEinheiten", "")
        zeitreihenSpalte = request.POST.get("zeitreihenSpalte", "")
        jsonData = request.POST.get("jsonData", "")
        saveExperiment = request.POST.get("saveExperiment", "")
        datensatzName = request.POST.get("datensatzName", "")
        erfassungsDatum = request.POST.get("erfassungsDatum", "")

        # Das Experiment in das Objekt "measurement" einlesen
        measurement = read.Measurement(jsonData,jsonHeader,jsonEinheiten,zeitreihenSpalte)

        #measurement in Session-Variable speichern
        request.session['measurementData'] = json.dumps(measurement.data, cls=NumPyArangeEncoder)
        request.session['measurementHeader'] = json.dumps(measurement.colNames, cls=NumPyArangeEncoder)
        request.session['measurementUnits'] = json.dumps(measurement.colUnits, cls=NumPyArangeEncoder)
        request.session['measurementTimeIndex'] = json.dumps(measurement.timeIndex, cls=NumPyArangeEncoder)

        #measurement.resample_data()
        #measurement.gaussian_filter(1)
        #measurement.butterworth_filter(1)
        #measurement.fourier_transform(1)

        # Daten zur Übergabe vorbereiten
        dataForRender = {
            'jsonHeader': jsonHeader,
            'jsonEinheiten': jsonEinheiten,
            'zeitreihenSpalte': zeitreihenSpalte,
            'jsonData': jsonData,
            #'newData': json.dumps(measurement.data, cls=NumPyArangeEncoder),
            #'measurementObject': measurement,
            #'saveExperiment': saveExperiment,
            'datensatzName': datensatzName,
            'erfassungsDatum': erfassungsDatum,
            'expertMode': False #@TODO: wirklich den Expert-Mode auslesen! mit request.user
        }
        return render(request, "process/index.html", dataForRender)
    else:
        return render(request, "dashboard/index.html")




def analysis(request):

    if request.method == 'POST':
        # measurement-Objekt aus den Session-Variablen auslesen und wieder erstellen
        measurement = read.Measurement(request.session['measurementData'],request.session['measurementHeader'],
                                       request.session['measurementUnits'],request.session['measurementTimeIndex'])

        # Experten-Modus?
        expert = True #@TODO: Wahre Abfrage, ob User Experte ist!

        # Anz der Spalten
        anzSpalten = len(measurement.data[0])

        # Resampling?
        if request.POST.get('resampling','') == 'on':
            resamplingScale = request.POST.get('resamplingScale','1')
            # Resampling aufrufen
            measurement.resample_data(float(resamplingScale))

        # über alle Spalten iterieren
        for i in range(0, anzSpalten-1):
            if i != measurement.timeIndex:
                hochpassOrder = request.POST.get('hochpassOrder' + str(i),4)
                hochpassCofreq = request.POST.get('hochpassCofreq' + str(i),None)
                tiefpassOrder = request.POST.get('tiefpassOrder' + str(i),4)
                tiefpassCofreq = request.POST.get('tiefpassCofreq' + str(i),None)
                if request.POST.get('hochpass' + str(i),'') == 'on' & request.POST.get('tiefpass' + str(i),'') == 'on':
                    if expert == True:
                        measurement.butterworth_band_filter(data_index=i, lowcut=float(tiefpassCofreq),
                                                           highcut=float(hochpassCofreq), order=int(hochpassOrder))
                    else:
                        measurement.butterworth_band_filter(data_index=i)

                else:
                    if request.POST.get('hochpass' + str(i),'') == 'on':
                        if expert == True:
                            measurement.butterworth_filter(data_index=i,cofreq=float(hochpassCofreq),
                                                           order= int(hochpassOrder),moder='high')
                        else:
                            measurement.butterworth_filter(data_index=i,moder='high')

                    if request.POST.get('tiefpass' + str(i),'') == 'on':
                        if expert == True:
                            measurement.butterworth_filter(data_index=i, cofreq=float(tiefpassCofreq),
                                                           order=int(tiefpassOrder),moder='low')
                        else:
                            measurement.butterworth_filter(data_index=i,moder='low')


                if request.POST.get('gauss' + str(i),'') == 'on':
                    gaussStd = request.POST.get('gaussStd' + str(i),'2')
                    gaussM = request.POST.get('gaussM' + str(i),'50')
                    if expert == True:
                        measurement.gaussian_filter_expert(i,gaussM,gaussStd)
                    else:
                        measurement.gaussian_filter(i,gaussStd)

        # Daten zum Rendern vorbereiten
        dataForRender = {
            'jsonData': json.dumps(measurement.data, cls=NumPyArangeEncoder),
            'jsonHeader': json.dumps(measurement.colNames, cls=NumPyArangeEncoder),
            'jsonEinheiten': json.dumps(measurement.colUnits, cls=NumPyArangeEncoder),
            'zeitreihenSpalte': json.dumps(measurement.timeIndex, cls=NumPyArangeEncoder),
            'expertMode': expert
        }

        return render(request, "process/analysis.html", dataForRender)
    else:
        return render(request, "dashboard/index.html")