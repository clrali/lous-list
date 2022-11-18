from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from .views import CourseList, CourseCreate, AccountListView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),    

    path('department/', views.dept_dropdown, name='department'),
    path('courses/<int:id>/', views.course_detail, name="course"),
    path('schedule/', views.create_schedule, name='create-schedule'),
    path('course-create/', CourseCreate.as_view(), name='course-create'),
    path('profile/<int:id>/', views.userPage, name='profile'),

    path('my-invites/', views.invitesReceived, name='my-invites'),
    path('all-profiles/', AccountListView.as_view(), name='all-profiles'),
    path('make-friends/', views.viewInvitedProfiles, name='make-friends'),
    path('send-invite/', views.send_invitation, name='send-invite'),
    path('remove-friend/', views.remove_from_friends, name='remove-friend'),
    path('my-invites/accept', views.accept_invitation, name='accept-invite'),
    path('my-invites/reject', views.reject_invitation, name='reject-invite'),
    path('my-friends/', views.myFriends, name='my-friends'),
    path('profile/<int:id>/comment/', views.publish_comment, name='comment'),

    # path('comments/', views.schedule_comment_create_and_list_view, name='comments'),
    # path('sched-test/', views.add_remove_courses, name='change-courses'),
]
