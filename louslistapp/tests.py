from django.test import TestCase
from django.urls import reverse
from .models import Instructor
import requests

# Create your tests here.

class SearchFunctionalityTest(TestCase):
    def test_if_search_links_to_correct_page(self):
        response=self.client.get(reverse('department'))
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