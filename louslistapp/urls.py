from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('depts', views.viewdepts, name='depts'),
    path('courses', views.viewcourses, name='courses'),
]