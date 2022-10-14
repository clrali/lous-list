from django.shortcuts import render
from django.http import HttpResponse
import requests

# Create your views here.git
def home(request):
    return render(request, 'home.html')

def dept_dropdown(request):
    response = requests.get('http://luthers-list.herokuapp.com/api/deptlist')
    depts = response.json()

    return render(request, 'dropdown.html', {'depts': depts})

def login(request):
    return render(request, 'login.html')
