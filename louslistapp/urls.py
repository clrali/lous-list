from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('dropdown/', views.dept_dropdown, name='dropdown'),
    path('classes/',views.get_classes, name="class_details"),
]