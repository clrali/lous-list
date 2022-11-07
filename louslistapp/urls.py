from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from .views import CourseList, CourseCreate
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('department/', views.dept_dropdown, name='department'),
    path('courses/<int:id>/', views.course_detail, name="course"),
    path('selected-courses/', views.CourseList, name="courses"),
    path('schedule/', views.create_schedule, name='create-schedule'),
    path('course-create/', CourseCreate.as_view(), name='course-create'),
    path('', TemplateView.as_view(template_name="login.html")),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view()),
]
