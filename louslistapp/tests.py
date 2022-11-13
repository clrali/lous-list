from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Instructor, Course
import requests
from django.test import TestCase, RequestFactory, Client, TransactionTestCase
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from . import views


# Create your tests here.


class SearchFunctionalityTest(TestCase):
    def test_if_search_links_to_correct_page(self):
        response = self.client.get(reverse('department'))
        self.assertEqual(response.status_code, 200)


class InstructorModelTest(TestCase):
    def test_if_api_returns_correct_professor(self):
        url = 'http://luthers-list.herokuapp.com/api/dept/CS'
        response = requests.get(url)
        courses = response.json()[0]

        test_instructor = Instructor(
            prof_name=courses['instructor']['name'], prof_email=courses['instructor']['email'])
        expected_instructor = Instructor(
            prof_name="Derrick Stone", prof_email="djs6d@virginia.edu")

        self.assertEqual(test_instructor.prof_name,
                         expected_instructor.prof_name, "The instructor is not as expected")

    def test_if_api_returns_incorrect_professor(self):
        url = 'http://luthers-list.herokuapp.com/api/dept/CS'
        response = requests.get(url)
        courses = response.json()[1]

        test_instructor = Instructor.objects.create(
            prof_name=courses['instructor']['name'], prof_email=courses['instructor']['email'])
        expected_instructor = Instructor.objects.create(
            prof_name="Derrick Stone", prof_email="djs6d@virginia.edu")

        self.assertNotEqual(test_instructor.prof_name,
                            expected_instructor.prof_name, "The instructor is the same")


"""
    def test_course_search_instructor(self):
        response = self.client.get('/department/?q=APMA&n=3100&p=')
        courses = response.json()[1]
        print(courses)
        test_instructor = Instructor.objects.create(
            prof_name=courses['instructor']['name'], prof_email=courses['instructor']['email'])
        expected_instructor = Instructor.objects.create(
            prof_name="Cong Shen", prof_email="cs7dt@virginia.edu")

        self.assertNotEqual(test_instructor.prof_name,
                            expected_instructor.prof_name, "The instructor is the same")
"""

class URLTest(TestCase):
    def test_URL(self):
        response = self.client.get('/')
        # verify that the base url will send out a 200 HTTP status code
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "louslistapp/home.html")

    def test_GoogleLoginURL(self):
        response = self.client.get('/accounts/google/login/')
        # verify that the  accounts url will send out a 200 HTTP status code
        self.assertEqual(response.status_code, 200)


class CourseDisplayTest(TestCase):
    def test_to_access_my_courses_when_logged_in(self):
        self.user = User.objects.create_user(username='admin', password='pass@123', email='admin@admin.com')
        self.client = Client() 
        self.client.login(username=self.user.username, password='pass@123')
        response = self.client.get(('/selected-courses'), {'user_id': self.user.id})
        self.assertEqual(response.status_code, 301)

    def test_invalid_course_search(self):
        response = self.client.get('/department/?q=APMA&n=&p=hagrid')
        self.assertEqual(response.status_code, 200)


class ScheduleBuilderTest(TransactionTestCase):
    fixtures = ['course_data.json', 'user_data.json']

    def test_course_data_retrieval(self):
        self.user = User.objects.get(pk=1)
        self.client = Client()
        self.client.login(username=self.user.username, password='pass@123')

        course = Course.objects.get(pk=1)
        self.assertEqual(course.description, "Introduction to Programming")

    def test_valid_schedule(self):
        self.user = User.objects.get(pk=1)
        self.client = Client()
        self.client.login(username=self.user.username, password='pass@123')

        # course_1, course_2 = Course.objects.get(pk=1), Course.objects.get(pk=2)

        schedule = {'Other': [],
                    'Monday': [],
                    'Tuesday': [],
                    'Wednesday': [],
                    'Thursday': [],
                    'Friday': [],
                    'Saturday': [],
                    'Sunday': []}

        response = self.client.get(reverse('create-schedule'), {'user_id': self.user.id}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.id, 1)

        self.assertTemplateUsed(response, "louslistapp/schedule.html")

        self.assertEqual(response.context['message'], 'This is a valid schedule')
        self.assertEqual(response.context['schedule'], schedule)
        self.assertEqual(response.context['duplicate_courses'], None)
        self.assertEqual(response.context['course_time_conflicts'], None)

class CourseSchedulingTest(TransactionTestCase):  
    def test_to_access_schedule_when_logged_in(self):
        self.user = User.objects.create_user(username='admin', password='pass@123', email='admin@admin.com')
        self.client = Client() 
        self.client.login(username=self.user.username, password='pass@123')
        response = self.client.post(reverse('create-schedule'), {'user_id': self.user.id})
        self.assertEqual(response.status_code, 200)

    def test_to_access_schedule_when_not_logged_in(self):
        self.user = User.objects.create_user(username='admin', password='pass@123', email='admin@admin.com')
        self.client = Client()
        response = self.client.post(('schedule'), {'user_id': self.user.id})
        # should be 404 because page cannot be accessed when not logged in
        self.assertEqual(response.status_code, 404)