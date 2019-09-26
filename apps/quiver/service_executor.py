from enum import Enum, IntEnum
from apps.quiver.models import AnalyticsService, AnalyticsServiceExecution
import requests
from requests.auth import AuthBase
from urllib.parse import urlparse, urljoin
import base64


#from experiments.serializers import AnalyticsServiceExecutionInputSerializer, \
#    AnalyticsServiceExecutionParameterSerializer, MeasurementChannelSerializer, \
#    AnalyticsServiceExecutionResultSerializer

from django.utils.timezone import now


class EndpointAction(IntEnum):
    STATUS  = 1
    EXECUTE = 2
    TASK    = 3
    RESULT  = 4


class ServiceState(IntEnum):
    READY   = 1
    RUNNING = 2
    ERROR   = 3
    DONE    = 4
    BUSY    = 5

# Very simple authentication. Add an X-QUIVER-AUTH header with an api key, when making a request to a service.
class ServiceAuth(AuthBase):
    def __init__(self, service: AnalyticsService):
        self.api_key = service.api_key

    def __call__(self, r):
        r.headers['X-QUIVER-AUTH'] = self.api_key
        return r


def build_service_enpoint_url(action: EndpointAction, service: AnalyticsServiceExecution):
    if action == EndpointAction.STATUS:
        return urljoin(service.service.url, '/status')
    elif action == EndpointAction.EXECUTE:
        return urljoin(service.service.url, '/execute')
    elif action == EndpointAction.TASK:
        return urljoin(service.service.url, '/task/')
    elif action == EndpointAction.RESULT:
        return urljoin(service.service.url, '/result/')
    else:
        return service.service.url


def get_status_for_service(service: AnalyticsService):
    rsp = requests.get(urljoin(service.url, 'status'), allow_redirects=False, auth=ServiceAuth(service))
    json = rsp.json()

    return ServiceState[json["status"]]

def execute_next_state(service: AnalyticsServiceExecution, task_url, input, parameter):
    # Service was still not executed, execute it with given inputs and parameters
    # and save the task_id as given by the service
    if service.last_state == ServiceState.READY:

        url = build_service_enpoint_url(EndpointAction.EXECUTE, service)
        rsp = requests.post(url, json={
            "inputs": input,
            "parameters": parameter
        }, auth=ServiceAuth(service.service))

        #as long as post hasnt finished do nothing
        while rsp.status_code != 202:
            if rsp.status_code == 500 or rsp.status_code == 404:
                raise ValueError('Something went wrong!')

        task_url = rsp.headers['Location']

        #json = rsp.json()
        service.last_contact = now()
        service.last_state = ServiceState.RUNNING
        service.save()
        return task_url

    elif service.last_state == ServiceState.RUNNING:
        #url = build_service_enpoint_url(EndpointAction.TASK, service)
        url = task_url
        rsp = requests.get(url, allow_redirects=False, auth=ServiceAuth(service.service))
        #raise ValueError(rsp)

        # We have a result
        if rsp.status_code == 303:
            location = rsp.headers['Location']

            r = requests.get(location, allow_redirects=False, auth=ServiceAuth(service.service))
            #slow get? -> old result
            json = r.json()
            json['data'] = base64.b64decode(json['data'])
            service.last_contact = now()


            service.last_state = ServiceState.DONE
            if service.last_state == ServiceState.DONE:
                service.delete()
            return(json['data'])


        else:
            raise ValueError('Error')
