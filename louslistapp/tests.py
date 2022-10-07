from django.test import TestCase
import unittest

# Create your tests here.
class BasicTest(unittest.TestCase):
    def test_upper(self):
        self.assertEqual("hello".upper(), "HELLO")
    
if __name__ == "__main__":
    unittest.main()