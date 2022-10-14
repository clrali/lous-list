from django.shortcuts import render
from django.http import HttpResponse
import requests

# Create your views here.
def home(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')

def viewdepts(request):
    response = requests.get('http://luthers-list.herokuapp.com/api/deptlist/?format=json').json()
    return render(request, 'depts.html', {'response': response})

def viewcourses(request):
    response = requests.get('http://luthers-list.herokuapp.com/api/dept/CS?format=json').json()
    return render(request, 'courses.html', {'response': response})

