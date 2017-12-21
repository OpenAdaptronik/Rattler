from django.shortcuts import render
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

        # Daten zur Übergabe vorbereiten
        dataForRender = {
            'jsonHeader': jsonHeader,
            'jsonEinheiten': jsonEinheiten,
            'zeitreihenSpalte': zeitreihenSpalte,
            'jsonData': jsonData,
            'saveExperiment': saveExperiment,
            'datensatzName': datensatzName,
            'erfassungsDatum': erfassungsDatum
        }
        
        return render(request, "process/index.html", dataForRender)