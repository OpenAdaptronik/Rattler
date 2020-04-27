import logging
from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from .forms import RegisterForm
from .forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from apps.projects.models import Experiment, Project, Datarow, Value
from apps.user.models import User
import bcrypt
from django.contrib.auth.hashers import check_password
import base64
import json


logger = logging.getLogger(__name__)

@csrf_exempt
def index(request):
    logger.info('home')

    if request.method == 'POST':
        data = json.loads(request.body.decode())
        if "username" in data and "password" in data and "project_name" in data and "experiment_name" in data and "timerow" in data and "numofdatarows" in data:
            username = data["username"]
            password = data["password"]
            project_name = data["project_name"]
            experiment_name = data["experiment_name"]
            timerow = int(data["timerow"])
            numofdatarows = int(data["numofdatarows"])
            hashed_password_db = User.objects.filter(username=username).values_list("password", flat=True)[0]
            if check_password(password, hashed_password_db):
                if Project.objects.filter(name=project_name).exists():
                    project_id = Project.objects.filter(name=project_name).filter(user=User.objects.filter(username=username).values_list("id", flat=True)[0]).values_list("id", flat=True)[0]
                    i = 0
                    while i < numofdatarows:
                        if not ("datarow" + str(i) in data):
                            return HttpResponse("datarow " + str(i) + " missing.")
                        if not("title" in data["datarow" + str(i)] and "unit" in data["datarow" + str(i)] and "measuring_instrument" in data["datarow" + str(i)] and "value" in data["datarow" + str(i)]):
                            return HttpResponse("datarow " + str(i) + " is wrongly formatted.")
                        i += 1

                    new_experiment = Experiment(project_id=project_id, timerow=timerow, name=experiment_name)
                    new_experiment.save()
                    experiment_id = new_experiment.id
                    i = 0
                    while i < numofdatarows:
                        new_datarow = Datarow(experiment_id=experiment_id, unit=data["datarow" + str(i)]["unit"], name=data["datarow" + str(i)]["title"], measuring_instrument=data["datarow" + str(i)]["measuring_instrument"])
                        new_datarow.save()
                        j = 0
                        values_list = []
                        data_array = json.loads(data["datarow" + str(i)]["value"])
                        while j < len(data_array):
                            values_list.append(Value(value=data_array[j], datarow_id=new_datarow.id))
                            j += 1
                        Value.objects.bulk_create(values_list)
                        i += 1
                    return HttpResponse("Successfully created new experient!")

                else:
                    return HttpResponse("Project doesn't exist.")
            else:
                return HttpResponse("Invalid username or password.")


            # curl --data "post1=value1&post2=value2&etc=valetc&url=testurl" https://rattler.openadaptronik.de
            return HttpResponse()
        else:
            #return HttpResponse(str(type(request.body)) + "400", status=400) ["url"]
            return HttpResponse("Wrong data format used.")

    if request.user.is_authenticated:
        return HttpResponseRedirect('/dashboard')

    return render(
        request,
        'index/index.html',
        {
            'login_form': AuthenticationForm(),
            'registration_form': RegisterForm()
        }
    )
