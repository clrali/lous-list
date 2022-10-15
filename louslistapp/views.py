from django.shortcuts import render
from django.http import HttpResponse
import requests

# Create your views here.git


def home(request):
    return render(request, 'home.html')


def dept_dropdown(request):
    # For department dropdown
    url = 'http://luthers-list.herokuapp.com/api/deptlist'
    response = requests.get(url)
    departments = response.json()

    # For courses
    query = request.GET
    courses = None
    if query is not None and 'q' in query:
        dept_name = query.get('q')
        url = 'http://luthers-list.herokuapp.com/api/dept/' + dept_name
        response = requests.get(url)
        courses = response.json()

    return render(request, 'dropdown.html', {'departments': departments, 'courses': courses})


def login(request):
    return render(request, 'login.html')