from apps.quiver.models import AnalyticsService, AnalyticsServiceExecution
from django.shortcuts import render, HttpResponseRedirect
from django.core.exceptions import PermissionDenied

from django.views.generic import FormView, CreateView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AnalyticsServiceForm
from django.core import serializers
from django.utils.encoding import uri_to_iri

from django.shortcuts import render, HttpResponseRedirect
from apps.calc.measurement import measurement_obj
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from apps.analysis.json import NumPyArangeEncoder
from apps.projects.models import Experiment, Project, Datarow, Value
from apps.projects.serializer import project_serialize
from django.conf import settings
from django.core.exceptions import PermissionDenied
import numpy as np


from apps.quiver import service_executor


# Create your views here.

class NewAnalyticsService(LoginRequiredMixin, CreateView):
    form_class = AnalyticsServiceForm
    template_name = 'quiver/analyticsservice_create.html'

    def get_context_data(self, **kwargs):
        data = super(NewAnalyticsService, self).get_context_data(**kwargs)
        return data

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user

        context = self.get_context_data()

        self.object = form.save()
        return super(NewAnalyticsService, self).form_valid(form)

class UpdateAnalyticsService(LoginRequiredMixin, UpdateView):
    model = AnalyticsService
    form_class = AnalyticsServiceForm
    pk_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.user == self.request.user and not self.object.visibility:
            raise PermissionDenied()
        return super(UpdateAnalyticsService, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(UpdateAnalyticsService, self).get_context_data(**kwargs)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        return super(UpdateAnalyticsService, self).form_valid(form)


class MyAnalyticsService(LoginRequiredMixin, ListView):
    model = AnalyticsService
    allow_empty = True
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        return AnalyticsService.objects.filter(user=user).order_by('updated')

class AnalyticsServiceDetail(DetailView):
    model = AnalyticsService
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        user = self.request.user
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the projects
        context['project_list'] = Project.objects.filter(user=user).order_by('updated')
        return context

    #def get(self, request, *args, **kwargs):
    #    self.object = self.get_object()
    #    if self.object.user != self.request.user and not self.object.visibility:
    #        raise PermissionDenied()
    #    return super(AnalyticsServiceDetail, self).get(request, *args, **kwargs)


def delete_analytics_service(request, analytics_service_id):
    AnalyticsService.objects.get(id=analytics_service_id).delete()

    return HttpResponseRedirect('/quiver/')


@login_required
def analytics_service_detail(request, experimentId):
    if request.method != 'POST':
        return HttpResponseRedirect('/dashboard/')
    # current user
    curruser_id = request.user.id
    projectId = Experiment.objects.get(id=experimentId).project_id
    # owner of experiment
    expowner_id = Project.objects.get(id=projectId).user_id

    # read graph visibility from post
    graph_visibility = request.POST.get("graphVisibilities", "").split(',')

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
        'jsonZeitreihenSpalte': json.dumps(measurement.timeIndex, cls=NumPyArangeEncoder),
        'jsonMeasurementInstruments': json.dumps(mInstruments_list, cls=NumPyArangeEncoder),
        'experimentId': experimentId,
        'experimentName': experimentName,
        'projectId': projectId,
        'dateCreated': dateCreated,
        'current_user_id': curruser_id,
        'experiment_owner_id': expowner_id,
        'graphVisibility': json.dumps(graph_visibility, cls=NumPyArangeEncoder),
    }

    # save experimentId to get it in ajax call when refreshing graph
    request.session['experimentId'] = experimentId

    return render(request, "quiver/index.html", dataForRender)

#def analyticsService(request):
#
#    if request.method == 'POST':
#        form = AnalyticsServiceForm(request.POST)
#        if form.is_valid():
#            print('hi')
#
#    form = AnalyticsServiceForm()
#
#    return render(request, 'analytics_service_detail.html', {'form': form})

def execute_service(request, analytics_service_id):

    #data = request.body
    #data = json.loads(data)
    #read data and get project id:
    if request.method == 'POST':
        project_id = request.POST.get("project_id", )
        rowcounter = int(request.POST.get("rowcounter", ))
        #read out of ajax and adjust format for follwing execution of service

    #raise ValueError(request.POST.get("project_id"))
    #read and prepare parameter data to send it to the service
    parameter = [];
    i = 0;
    while i < rowcounter:
        param_attributes = {
                            'name': request.POST.get('parameter_name_' + str(i), ),
                            'value': request.POST.get('parameter_value_' + str(i), ),
                            'type': request.POST.get('type_select_' + str(i), )
                            }
        parameter.append(param_attributes)
        i = i + 1;

    #serialize project as preparation to send it to the service
    input = project_serialize(project_id)

    service = AnalyticsService.objects.get(id=analytics_service_id)
    status = service_executor.get_status_for_service(service)
    if status == service_executor.ServiceState.READY:
        user = request.user
        service_execution = AnalyticsServiceExecution(service=service, last_state=1, user=user)
        service_execution.save()
        while service_execution.last_state != service_executor.ServiceState.DONE:
            if service_execution.last_state == service_executor.ServiceState.READY:
                task_url = service_executor.execute_next_state(service_execution, None, input, parameter)
            elif service_execution.last_state == service_executor.ServiceState.RUNNING:
                result = service_executor.execute_next_state(service_execution, task_url, None, None).decode('ascii')
                return JsonResponse(result, safe=False)


    else: raise ValueError('Service does not exist right now.')

    return
