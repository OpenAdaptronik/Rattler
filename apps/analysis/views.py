from django.shortcuts import render, HttpResponseRedirect
from apps.calc.read_data import read
from django.contrib.auth.decorators import login_required
import json
from .json import NumPyArangeEncoder

# Create your views here.
@login_required
def index(request):
    return render(request, "analysis/index.html")