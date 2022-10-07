from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Welcome to Lou's List!")

def home(request):
    return render(request, 'home.html')
