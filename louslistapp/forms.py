from django import forms
from .models import Comment

class CourseSelected(forms.Form):
    delete = forms.CharField(label='', max_length=0).widget = forms.HiddenInput()

class CommentForm(forms.Form):
    class Meta:
        model = Comment
        fields = ('message', 'author')