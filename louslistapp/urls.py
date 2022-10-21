from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('department/', views.dept_dropdown, name='department'),
    path('courses', views.viewcourses, name='courses'),
    #path('courseSections', views.viewcourseSections, name='courseSections'),
]