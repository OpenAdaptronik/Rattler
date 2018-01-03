from django.shortcuts import render
from apps.calc.read_data import read
from django.contrib.auth.decorators import login_required
import json
import numpy as np

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
        request.session['measurementObject'] = measurement

        #measurement.resample_data()
        #measurement.gaussian_filter(1)
        #measurement.butterworth_filter(1)
        #measurement.fourier_transform(1)


        # @TODO Beschreibung!!
        class NumPyArangeEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, np.ndarray):
                    return obj.tolist()  # or map(int, obj)
                return json.JSONEncoder.default(self, obj)


        #json.dumps(measurement.data.tolist(),separators=(',', ':'), sort_keys=True, indent=4),


        # Daten zur Übergabe vorbereiten
        dataForRender = {
            #'LOG': measurement.data,
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
    if request.method == 'POST':
        # measurement-Objekt aus der Session holen
        measurement = request.session['measurementObject']

        # Experten-Modus?
        expert = True

        # Variablen aus dem Post-Request auslesen
        jsonHeader = request.POST.get("jsonHeader", "")

        # Anz der Spalten
        anzSpalten = len(measurement.data[0])

        # über alle Spalten iterieren
        #for i in xrange(0, anzSpalten-1):
            #usw
        uebergabe = [request.session['hochpass0'], request.session['tiefpass0']]
            
        return render(request, "process/analysis.html", 'info' = uebergabe)
    else:
        return render(request, "dashboard/index.html")
