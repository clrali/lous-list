from django.shortcuts import render
from django.http import HttpResponse
import requests
from .models import Course


def home(request):
    return render(request, 'home.html')


def login(request):
    return render(request, 'login.html')


def viewdepts(request):
    response = requests.get(
        'http://luthers-list.herokuapp.com/api/deptlist/?format=json').json()
    return render(request, 'dropdown.html', {'response': response})


def viewcourses(request):
    response = requests.get(
        'http://luthers-list.herokuapp.com/api/dept/ENGR?format=json').json()
    return render(request, 'courses.html', {'response': response})

# def viewcourseSections(request):
    # return render(request, 'courseSections.html', {'response': response})


def dept_dropdown(request):
    # For department dropdown
    url = 'http://luthers-list.herokuapp.com/api/deptlist'
    response = requests.get(url)
    departments = response.json()

    # For courses
    query = request.GET
    courses, all_courses = None, None
    if query is not None and 'q' in query:
        dept_name = query.get('q')
        course_num = None
        professor_name = None
        if 'n' in query:
            course_num = query.get('n')
        if 'p' in query:
            professor_name = query.get('p')

        url = 'http://luthers-list.herokuapp.com/api/dept/' + dept_name
        response = requests.get(url)
        courses = response.json()

        # This will make sure that all sections of a course are grouped together
        all_courses = {}
        for course in courses:
            obj, course_data = Course.objects.get_or_create(
                prof_name= course['instructor']['name'],
                prof_email = course['instructor']['email'],
                course_number = course['course_number'],
                semester_code = course['semester_code'],
                course_section = course['course_section'],
                subject = course['subject'],
                catalog_number = course['catalog_number'],
                description = course['description'], 
                units = course['units'],
                component = course['component'],
                class_capacity = course['class_capacity'],
                waitlist = course['wait_list'],
                wait_cap = course['wait_cap'],
                enrollment_total = course['enrollment_total'],
                enrollment_available = course['enrollment_available'],
                days = course['meetings'][0]['days'],
                location = course['meetings'][0]['facility_description']
            )
            if course_num == "" and professor_name == "":
                all_courses = Course.objects.filter(subject=dept_name).order_by('id')
            elif course_num != "" and professor_name != "":
                all_courses = Course.objects.filter(subject=dept_name, catalog_number=course_num, prof_name=professor_name).order_by('id')
            elif course_num != "" and professor_name == "":
                all_courses = Course.objects.filter(subject=dept_name, catalog_number=course_num).order_by('id')
            else:
                all_courses = Course.objects.filter(subject=dept_name, prof_name__contains=professor_name).order_by('id')
    return render(request, 'displayCourses.html', { 'departments': departments, 'all_courses': all_courses})

def course_detail(request, id):
    course = Course.objects.get(id = id)
    return render (
        request, 
        'course_detail.html',
        {'course': course}
    )

# def schedule_builder(request, id):
