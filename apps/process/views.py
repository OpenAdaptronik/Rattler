from django.shortcuts import render
from apps.calc.read_data import read
from django.contrib.auth.decorators import login_required

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

        measurement = read.Measurement(jsonData,jsonHeader,jsonEinheiten,zeitreihenSpalte)
        measurement.resample_data()
        measurement.gaussian_filter(1)
        measurement.butterworth_filter(1)

        # Daten zur Übergabe vorbereiten
        dataForRender = {
            #'LOG': measurement.data,
            'jsonHeader': jsonHeader,
            'jsonEinheiten': jsonEinheiten,
            'zeitreihenSpalte': zeitreihenSpalte,
            'jsonData': jsonData,
            'measurementObject': measurement,
            'saveExperiment': saveExperiment,
            'datensatzName': datensatzName,
            'erfassungsDatum': erfassungsDatum,
            #'dataAsString': str(measurement.get_data()).replace('\n', ' ').replace('\r', ''),
            #'headerAsString': str(measurement.get_data()).replace('\n', ' ').replace('\r', ''),
            #'dataAsString': str(measurement.colNames_User).replace('\n', ' ').replace('\r', ''),
            #'unitsAsString': str(measurement.colUnits_User).replace('\n', ' ').replace('\r', ''),
            'expertMode': True
        }

        return render(request, "process/index.html", dataForRender)

def analysis(request):
    return render(request, "process/analysis.html")