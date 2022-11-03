from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('department/', views.dept_dropdown, name='department'),
    path('courses', views.viewcourses, name='courses'),
    path('courses/<int:id>/',views.course_detail, name = "course_detail")

    #path('courseSections', views.viewcourseSections, name='courseSections'),
]