from django.shortcuts import render
from django.http import HttpResponse
import requests

def home(request):
    return render(request, 'home.html')


def dept_dropdown(request):
    # For department dropdown
    url = 'http://luthers-list.herokuapp.com/api/deptlist'
    response = requests.get(url)
    departments = response.json()

    # For courses
    query = request.GET
    courses, course_dict = None, None
    if query is not None and 'q' in query:
        dept_name = query.get('q')
        url = 'http://luthers-list.herokuapp.com/api/dept/' + dept_name
        response = requests.get(url)
        courses = response.json()

        # This will make sure that all sections of a course are grouped together
        course_dict = {}
        for course in courses:
            course_name = (course['subject'], course['catalog_number'], course['description'],
                           course['instructor']['name'], course['instructor']['email'])
            if course_name in course_dict:
                course_dict[course_name].append(course)
            else:
                course_dict[course_name] = [course]

    return render(request, 'dropdown.html', {'departments': departments, 'courses': course_dict})


def login(request):
    return render(request, 'login.html')

def viewdepts(request):
    response = requests.get('http://luthers-list.herokuapp.com/api/deptlist/?format=json').json()
    return render(request, 'dropdown.html', {'response': response})

def viewcourses(request):
    response = requests.get('http://luthers-list.herokuapp.com/api/dept/ENGR?format=json').json()
    return render(request, 'courses.html', {'response': response})

def viewcourseSections(request):
    return render(request, 'courseSections.html', {'response': response})

def dept_dropdown(request):
    # For department dropdown
    url = 'http://luthers-list.herokuapp.com/api/deptlist'
    response = requests.get(url)
    departments = response.json()

    # For courses
    query = request.GET
    courses, course_dict = None, None
    if query is not None and 'q' in query:
        dept_name = query.get('q')
        url = 'http://luthers-list.herokuapp.com/api/dept/' + dept_name
        response = requests.get(url)
        courses = response.json()

        # This will make sure that all sections of a course are grouped together
        course_dict = {}
        for course in courses:
            course_name = (course['subject'], course['catalog_number'], course['description'])
            if course_name in course_dict:
                course_dict[course_name].append(course)
            else:
                course_dict[course_name] = [course]

    return render(request, 'dropdown.html', {'departments': departments, 'courses': course_dict})