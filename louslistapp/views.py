from django.shortcuts import render, redirect
import requests
from .models import Course
from .forms import CourseSelected
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
import re


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
                start_time=course['meetings'][0]['start_time'],
                end_time=course['meetings'][0]['end_time'],
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
    context = Course.objects.filter(selected=True, user=request.user)
    return render(request, 'louslistapp/course_list.html', {"all_course": context})


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


def create_schedule(request):
    # start_time and end_time are strings but sorting still works (might be better to switch these DateTimeFields)
    courses = list(Course.objects.filter(selected=True, user=request.user.id).order_by('start_time', 'end_time'))
    print(courses)

    days_map = {'Mo': 'Monday', 'Tu': 'Tuesday', 'We': 'Wednesday', 'Th': 'Thursday', 'Fr': 'Friday'}
    courses_per_day = {'Other': [], 'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}
    time_conflicts_per_day = {'Other': [], 'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}

    course_names = set()

    status_message = ""

    duplicate_courses = set()

    for course in courses:
        print(course.start_time, course.end_time)
        course_identifier = course.subject + course.catalog_number
        # may have to check Topic field
        if course_identifier in course_names:
            duplicate_courses.add(course)
        course_names.add(course_identifier)

    if len(course_names) == len(courses):
        for course in courses:
            days = re.findall('[A-Z][^A-Z]*', course.days)
            if len(days) == 0:
                courses_per_day['Other'].append(course)
                print(f"There is no information regarding what days {course.subject}{course.catalog_number} - "
                      f"Section {course.course_section} will be offered.")
                continue
            else:
                for day in days:
                    # this list is in sorted order because of the initial sort
                    transl_day = days_map[day]
                    courses_per_day[transl_day].append(course)

        contains_time_conflict = False
        for day in courses_per_day:
            time_conflicts = check_validity(courses_per_day[day])
            if len(time_conflicts) > 0:
                contains_time_conflict = True
            time_conflicts_per_day[day] = time_conflicts

        if contains_time_conflict:
            status_message = f"There is a time conflict on {day}."
            return render(request,
                          'louslistapp/schedule.html',
                          {'message': status_message,
                           'schedule': None,
                           'duplicate_courses': None,
                           'course_time_conflicts': time_conflicts_per_day
                           })
        else:
            status_message = "This is a valid schedule"
            return render(request,
                          'louslistapp/schedule.html',
                          {'message': status_message,
                           'schedule': courses_per_day,
                           'duplicate_courses': None,
                           'course_time_conflicts': None
                           })

    else:
        status_message = "You have enrolled in the same class multiple times."
        return render(request,
                      'louslistapp/schedule.html',
                      {'message': status_message,
                       'schedule': None,
                       'duplicate_courses': duplicate_courses,
                       'course_time_conflicts': None
                       })


def check_validity(courses):
    time_conflicts = []
    for i in range(1, len(courses)):
        if courses[i].start_time <= courses[i - 1].end_time:
            time_conflicts.append((courses[i - 1], courses[i]))

    return time_conflicts