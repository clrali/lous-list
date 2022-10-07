from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("Welcome to Lou's List")

def login(request):
    return render(request, 'login.html')
