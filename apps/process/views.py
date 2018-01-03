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
            #'dataAsString': str(measurement.get_data()).replace('\n', ' ').replace('\r', ''),
            #'headerAsString': str(measurement.get_data()).replace('\n', ' ').replace('\r', ''),
            #'dataAsString': str(measurement.colNames_User).replace('\n', ' ').replace('\r', ''),
            #'unitsAsString': str(measurement.colUnits_User).replace('\n', ' ').replace('\r', ''),
            'expertMode': False #@TODO: wirklich den Expert-Mode auslesen! mit request.user
        }
        return render(request, "process/index.html", dataForRender)
    else:
        return render(request, "dashboard/index.html")




def analysis(request):
    '''

    if bool(resampling):

    if bool(hochpass) && tiefpass:
        measurement.butterworth_band_filter(1)
    else:
        if hochpass:
            measurement.butterworth_filter(mode='high')
        if tiefpass:
            measurement.butterworth_filter(mode='low')
    if bool(gauss):
        measurement.gaussian_filter()

    return render(request, "process/analysis.html")'''
    if request.method == 'POST':
        measurement = read.Measurement(request.session['measurementData'],request.session['measurementHeader'],
                                       request.session['measurementUnits'],request.session['measurementTimeIndex'])

        # Experten-Modus?
        expert = True

        # Variablen aus dem Post-Request auslesen
        jsonHeader = request.POST.get("jsonHeader", "")

        # Anz der Spalten
        anzSpalten = len(measurement.data[0])

        # über alle Spalten iterieren
        #for i in xrange(0, anzSpalten-1):
            #usw
        uebergabe = [request.POST.get('hochpass0',''), request.POST.get('tiefpass0','')]


        return render(request, "process/analysis.html", {'info': uebergabe})
    else:
        return render(request, "dashboard/index.html")
