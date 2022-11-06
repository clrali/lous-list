from django.urls import path
from .views import CourseList, CourseCreate
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('department/', views.dept_dropdown, name='department'),
    path('courses/<int:id>/', views.course_detail, name="course"),
    path('schedule/', CourseList.as_view(), name="courses"),
    path('course-create/', CourseCreate.as_view(), name='course-create'),
]
