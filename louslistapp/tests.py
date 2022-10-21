from django.test import TestCase
from django.urls import reverse
from .models import Instructor
import requests

# Create your tests here.

class SearchFunctionalityTest(TestCase):
    def test_if_search_department_returns_corrent_results(self):
        response=self.client.get(reverse('department'))
        self.assertEqual(response.status_code, 200) 
        self.assertContains(response, "Search by Department")

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