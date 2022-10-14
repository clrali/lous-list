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

def get_classes(request):
    sub = 'CS'
    url = 'http://luthers-list.herokuapp.com/api/dept/'+sub+'/?format=json'
    classes_data = requests.get(url).json()

    all_courses = {}
    for i in classes_data:
        course = {
            'subject': sub,
            'professor': i['instructor']['name']
        }

    context = {"all_courses": all_courses}

    return render(request, 'courses.html', context)
