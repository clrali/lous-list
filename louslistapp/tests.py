from django.test import TestCase
import unittest
from .models import Instructor
import requests

# Create your tests here.


class InstructorModelTest(unittest.TestCase):
    def test_api_returns_correct_professor(self):
        url = 'http://luthers-list.herokuapp.com/api/dept/CS'
        response = requests.get(url)
        courses = response.json()[0]

        test_instructor = Instructor(
            prof_name=courses['instructor']['name'], prof_email=courses['instructor']['email'])
        expected_instructor = Instructor(
            prof_name="Derrick Stone", prof_email="djs6d@virginia.edu")

        self.assertEqual(test_instructor.prof_name,
                         expected_instructor.prof_name, "The instructor is not as expected")

    def test_api_returns_incorrect_professor(self):
        url = 'http://luthers-list.herokuapp.com/api/dept/CS'
        response = requests.get(url)
        courses = response.json()[1]

        test_instructor = Instructor.objects.create(
            prof_name=courses['instructor']['name'], prof_email=courses['instructor']['email'])
        expected_instructor = Instructor.objects.create(
            prof_name="Derrick Stone", prof_email="djs6d@virginia.edu")

        self.assertNotEqual(test_instructor.prof_name,
                            expected_instructor.prof_name, "The instructor is the same")


if __name__ == '__main__':
    unittest.main()
