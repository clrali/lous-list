from django.shortcuts import render, redirect
from django.http import Http404
import requests
from django.utils import timezone
from datetime import datetime, timedelta 
from .models import Course, UserProfile
from .forms import CourseSelected
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User

def home(request):
    return render(request, 'louslistapp/home.html')


def login(request):
    return render(request, 'louslistapp/login.html')


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
            if course['meetings'][0]['start_time'] == "":
                startTime = "00.00.00"
                endTime = "00.00.00"
            else:
                startTime = (course['meetings'][0]['start_time'])[:8]
                endTime = (course['meetings'][0]['end_time'])[:8]

            obj, course_data = Course.objects.get_or_create(
                prof_name=course['instructor']['name'],
                prof_email=course['instructor']['email'],
                course_number=course['course_number'],
                semester_code=course['semester_code'],
                course_section=course['course_section'],
                subject=course['subject'],
                catalog_number=course['catalog_number'],
                description=course['description'],
                units=course['units'],
                component=course['component'],
                class_capacity=course['class_capacity'],
                waitlist=course['wait_list'],
                wait_cap=course['wait_cap'],
                enrollment_total=course['enrollment_total'],
                enrollment_available=course['enrollment_available'],
                days=course['meetings'][0]['days'],
                start_time=datetime.strptime(startTime, '%H.%M.%S'),
                end_time=datetime.strptime(endTime, '%H.%M.%S'),
                location=course['meetings'][0]['facility_description']
            )
            if course_num == "" and professor_name == "":
                all_courses = Course.objects.filter(
                    subject=dept_name).order_by('id')
            elif course_num != "" and professor_name != "":
                all_courses = Course.objects.filter(
                    subject=dept_name, catalog_number=course_num, prof_name=professor_name).order_by('id')
            elif course_num != "" and professor_name == "":
                all_courses = Course.objects.filter(
                    subject=dept_name, catalog_number=course_num).order_by('id')
            else:
                all_courses = Course.objects.filter(
                    subject=dept_name, prof_name__contains=professor_name).order_by('id')
    return render(request, 'louslistapp/displayCourses.html', {'departments': departments, 'all_courses': all_courses})


def CourseList(request):
    model = Course
    context_object_name = "courses"
    template_name = "louslistapp/course_list.html"
    title = "Courses"
    context = Course.objects.filter(selected = True, user = request.user)
    return render(request, 'louslistapp/course_list.html', {"all_course" : context})


class CourseCreate(CreateView):
    model = Course
    fields = ['user', 'prof_name', 'semester_code',
        'subject', 'catalog_number', ]
    success_url = reverse_lazy('courses')
    


def course_detail(request, id):
    course = Course.objects.get(id=id)
    form2 = CourseSelected(request.POST)

    if request.method == 'POST':
        if form2.is_valid():
            if course.selected == False:
                course.selected = True
                course.user = request.user
            else:
                course.selected = False
            course.save()
    
    return render(request, 'louslistapp/course_detail.html', {'course': course, 'form2': form2})


def profile(request, username):
	try:
		user = User.objects.get(username=username)
	except:
		raise Http404

	return render(request, 'louslistapp/profile.html', {"profile": user})
