from django import forms 

class CourseSelected(forms.Form):
    delete = forms.CharField(label='', max_length=0).widget = forms.HiddenInput()