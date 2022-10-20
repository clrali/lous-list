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
    #print(response)

    # For courses
    query = request.GET
    courses, course_dict = None, None
    if query is not None and 'q' in query:
        dept_name = query.get('q')
        print(dept_name)
        course_num = None
        prof_name = None
        if('n' in query):
            course_num = query.get('n')
        if ('p' in query):
            prof_name = query.get('p')
        print(course_num)
        print(prof_name)
        url = 'http://luthers-list.herokuapp.com/api/dept/' + dept_name
        response = requests.get(url)
        courses = response.json()


        # This will make sure that all sections of a course are grouped together
        course_dict = {}
        for course in courses:
            print(course['instructor']["name"])
            if(course_num == "" and prof_name==""):
                course_name = (course['subject'], course['catalog_number'], course['description'])
                if course_name in course_dict:
                    course_dict[course_name].append(course)
                else:
                    course_dict[course_name] = [course]

            elif (course_num == course['catalog_number'] and prof_name == ""):
                course_name = (course['subject'], course['catalog_number'], course['description'])
                if course_name in course_dict:
                    course_dict[course_name].append(course)
                else:
                    course_dict[course_name] = [course]

            elif (course_num == "" and prof_name.lower() in course['instructor']["name"].lower()):
                course_name = (course['subject'], course['catalog_number'], course['description'])
                if course_name in course_dict:
                    course_dict[course_name].append(course)
                else:
                    course_dict[course_name] = [course]

            elif (course_num == course['catalog_number'] and prof_name in course['instructor']["name"]):
                course_name = (course['subject'], course['catalog_number'], course['description'])
                if course_name in course_dict:
                    course_dict[course_name].append(course)
                else:
                    course_dict[course_name] = [course]

    return render(request, 'dropdown.html', {'departments': departments, 'courses': course_dict})