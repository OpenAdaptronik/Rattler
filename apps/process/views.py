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
        # measurement-Objekt aus den Session-Variablen auslesen und wieder erstellen
        measurement = read.Measurement(request.session['measurementData'],request.session['measurementHeader'],
                                       request.session['measurementUnits'],request.session['measurementTimeIndex'])

        # Experten-Modus?
        expert = True #@TODO: Wahre Abfrage, ob User Experte ist!

        # Variablen aus dem Post-Request auslesen
        #jsonHeader = request.POST.get("jsonHeader", "")

        # Anz der Spalten
        anzSpalten = len(measurement.data[0])

        # Resampling?
        if request.POST.get('resampling','') == 'on':
            resamplingScale = request.POST.get('resamplingScale','1')
            # Resampling aufrufen

        # über alle Spalten iterieren
        for i in xrange(0, anzSpalten-1):
            hochpassOrder = request.POST.get('hochpassOrder' + str(i),'4')
            hochpassCofreq = request.POST.get('hochpassCofreq' + str(i),'0.1')
            tiefpassOrder = request.POST.get('tiefpassOrder' + str(i),'4')
            tiefpassCofreq = request.POST.get('tiefpassCofreq' + str(i),'0.9')
            if request.POST.get('hochpass' + str(i),'') == 'on' && request.POST.get('tiefpass' + str(i),'') == 'on':
                # hier Bandpass Bro IMMER MIT DEN VARIABLEN hochpassOrder, hochpassCofreq, tiefpassOrder, tiefpassCofreq
            else:
                if request.POST.get('hochpass' + str(i),'') == 'on':
                    # hier hochpass Bro IMMER MIT hochpassOrder, hochpassCofreq
                if request.POST.get('tiefpass' + str(i),'') == 'on':
                    # hier tiefpass Brudi IMMER MIT tiefpassOrder, tiefpassCofreq
            if request.POST.get('gauss' + str(i),'') == 'on':
                gaussStd = request.POST.get('gaussStd' + str(i),'2')
                gaussM = request.POST.get('gaussM' + str(i),'50')
                # hier gauss Vallah IMMER MIT gaussStd, gaussM
        

        # Daten zum Rendern vorbereiten
        dataForRender = {

        }

        return render(request, "process/analysis.html", dataForRender)
    else:
        return render(request, "dashboard/index.html")