from django.shortcuts import render, redirect, get_object_or_404
import requests
from .models import Course, Account, Relationship, Comment
from .forms import CourseSelected
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView, ListView
from django.urls import reverse_lazy
import re
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone


def home(request):
    return render(request, 'louslistapp/home.html')


def login(request):
    return render(request, 'louslistapp/login.html')


def dept_dropdown(request):
    # For department dropdown
    url = 'http://luthers-list.herokuapp.com/api/deptlist'
    response = requests.get(url)
    departments = response.json()

    # For courses
    query = request.GET
    courses, all_courses = None, None
    if query is not None and 'q' in query:
        dept_name = query.get('q').upper()
        course_num = None
        professor_name = None
        if 'n' in query:
            course_num = query.get('n')
        if 'p' in query:
            professor_name = query.get('p')

        url = 'http://luthers-list.herokuapp.com/api/dept/' + dept_name
        response = requests.get(url)
        courses = response.json()

        # This will make sure that all sections of a course are grouped together
        all_courses = {}
        for course in courses:
            meetDays, start_time, end_time, location = '', '', '', ''
            if len(course['meetings']) == 0:
                days = 'tbd'
                start_time = 'tbd'
                end_time = 'tbd'
                location = 'tbd'
            else:
                days = course['meetings'][0]['days']
                start_time = course['meetings'][0]['start_time']
                end_time = course['meetings'][0]['end_time']
                location = course['meetings'][0]['facility_description']

            obj, course_data = Course.objects.get_or_create(
                prof_name=course['instructor']['name'],
                prof_email=course['instructor']['email'],
                course_number=course['course_number'],
                semester_code=course['semester_code'],
                course_section=course['course_section'],
                subject=course['subject'],
                catalog_number=course['catalog_number'],
                description=course['description'],
                units=course['units'],
                component=course['component'],
                class_capacity=course['class_capacity'],
                waitlist=course['wait_list'],
                wait_cap=course['wait_cap'],
                enrollment_total=course['enrollment_total'],
                enrollment_available=course['enrollment_available'],
                days=days,
                start_time=start_time,
                end_time=end_time,
                location=location
            )
        if course_num == "" and professor_name == "":
            all_courses = Course.objects.filter(
                subject=dept_name).order_by('id')
        elif course_num != "" and professor_name != "":
            all_courses = Course.objects.filter(
                subject=dept_name, catalog_number=course_num, prof_name__contains=professor_name).order_by('id')
        elif course_num != "" and professor_name == "":
            all_courses = Course.objects.filter(
                subject=dept_name, catalog_number=course_num).order_by('id')
        else:
            all_courses = Course.objects.filter(
                subject=dept_name, prof_name__contains=professor_name).order_by('id')

    return render(request, 'louslistapp/displayCourses.html', {'departments': departments, 'all_courses': all_courses})


def CourseList(request):
    model = Course
    context_object_name = "courses"
    template_name = "louslistapp/course_list.html"
    title = "Courses"
    context = Course.objects.filter(selected=True, user=request.user)
    return render(request, 'louslistapp/course_list.html', {"all_course": context})


def course_detail(request, id):
    account = Account.objects.get(user=request.user.id)
    course = Course.objects.get(id=id)

    form2 = CourseSelected(request.POST)

    if request.method == 'POST':
        if form2.is_valid():
            if course not in account.get_courses():
                # add it to the course list
                account.courses.add(course)
            else:
                # remove it from the course list
                account.courses.remove(course)
            account.save()

    return render(request, 'louslistapp/course_detail.html', {'course': course,
                                                              'form2': form2,
                                                              'account': account})


def create_schedule(request):
    # start_time and end_time are strings but sorting still works (might be better to switch these DateTimeFields)
    courses = list(Account.objects.get(user=request.user.id).courses.order_by('start_time', 'end_time'))
    # courses = list(Course.objects.filter(selected=True, user=request.user.id).order_by('start_time', 'end_time'))
    print(courses)

    days_map = {'Mo': 'Monday', 'Tu': 'Tuesday',
                'We': 'Wednesday', 'Th': 'Thursday', 'Fr': 'Friday', 'Sa': 'Saturday', 'Su': 'Sunday'}

    courses_per_day = {'Other': [], 'Monday': [], 'Tuesday': [
    ], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [], 'Sunday': []}

    time_conflicts_per_day = {'Other': [], 'Monday': [], 'Tuesday': [
    ], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [], 'Sunday': []}

    course_names = set()

    status_message = ""

    duplicate_courses = set()

    for course in courses:
        print(course.start_time, course.end_time)
        course_identifier = course.subject + course.catalog_number
        # may have to check Topic field
        if course_identifier in course_names:
            duplicate_courses.add(course)
        course_names.add(course_identifier)

    if len(course_names) == len(courses):
        for course in courses:
            days = re.findall('[A-Z][^A-Z]*', course.days)
            if len(days) == 0:
                courses_per_day['Other'].append(course)
                print(f"There is no information regarding what days {course.subject}{course.catalog_number} - "
                      f"Section {course.course_section} will be offered.")
                continue
            else:
                for day in days:
                    # this list is in sorted order because of the initial sort
                    transl_day = days_map[day]
                    courses_per_day[transl_day].append(course)

        contains_time_conflict = False
        for day in courses_per_day:
            time_conflicts = check_validity(courses_per_day[day])
            if len(time_conflicts) > 0:
                contains_time_conflict = True
            time_conflicts_per_day[day] = time_conflicts

        if contains_time_conflict:
            status_message = f"There is a time conflict on {day}."
            return render(request,
                          'louslistapp/schedule.html',
                          {'message': status_message,
                           'schedule': None,
                           'duplicate_courses': None,
                           'course_time_conflicts': time_conflicts_per_day
                           })
        else:
            status_message = "This is a valid schedule"
            return render(request,
                          'louslistapp/schedule.html',
                          {'message': status_message,
                           'schedule': courses_per_day,
                           'duplicate_courses': None,
                           'course_time_conflicts': None
                           })

    else:
        status_message = "You have enrolled in the same class multiple times."
        return render(request,
                      'louslistapp/schedule.html',
                      {'message': status_message,
                       'schedule': None,
                       'duplicate_courses': duplicate_courses,
                       'course_time_conflicts': None
                       })


def check_validity(courses):
    time_conflicts = []
    for i in range(1, len(courses)):
        if courses[i].start_time <= courses[i - 1].end_time:
            time_conflicts.append((courses[i - 1], courses[i]))

    return time_conflicts


@login_required(login_url='login/')
def userPage(request, id):
    # user = User.objects.get(pk=id)
    actual_account = Account.objects.get(user=request.user.id)
    actual_user = actual_account.user

    print(actual_account.get_comments)

    try:
        friend_account = Account.objects.get(user=id)
    except Account.DoesNotExist:
        context = {'error_message': "Sorry, this profile does not exist."}
        return render(request, 'louslistapp/profile.html', context)
    else:
        friend_user = friend_account.user
        if actual_user.id != friend_user.id and friend_user not in actual_account.get_friends():
            context = {'error_message': "Sorry, you are not authorized to view the requested profile."}
            return render(request, 'louslistapp/profile.html', context)
        else:
            # courses = Course.objects.filter(selected=True, user=request.user.id).order_by('start_time', 'end_time')
            total_courses = friend_account.get_course_count()
            total_credits = 0
            for c in friend_account.get_courses():
                total_credits += int(c.units[0])
        # print("Actual User:", request.user, request.user.id)
        # print("Friend User:", user, user.id)
            context = {'account': friend_account,
                       'total_courses': total_courses,
                       'total_credits': total_credits,
                       'actual_user': actual_user,
                       'friend_user': friend_user}



            #comment = Comment.objects.get()

            # if request.method == 'POST':
            #     actual_account.comments.add(comment)
            #     actual_account.save()

            return render(request, 'louslistapp/profile.html', context)


def publish_comment(request, id):
    # we have to create a comment here and then add it to the user's account (user's id)
    comment_text = request.POST['comment']
    account = Account.objects.get(user=id)

    comment = Comment.objects.create(message=comment_text, author=request.user, time=timezone.now())
    account.comments.add(comment)

    # redirect the user to the profile they are currently viewing
    return HttpResponseRedirect(f"/profile/{id}/")
    # return HttpResponseRedirect(reverse('profile'), args=(id,))


def myFriends(request):
    account = Account.objects.get(user=request.user)
    context = {'account': account}
    return render(request, 'louslistapp/my_friends.html', context)


def invitesReceived(request):
    account = Account.objects.get(user=request.user)
    # gets all the friend invitations for the current user
    qs = Relationship.objects.invitations_received(account)
    results = list(map(lambda x: x.sender, qs))
    is_empty = False
    if len(results) == 0:
        is_empty = True
    context = {'qs': results, 'is_empty': is_empty}
    return render(request, 'louslistapp/invitations.html', context)


def accept_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Account.objects.get(pk=pk)
        receiver = Account.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)

        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
    return redirect('/my-invites')


def reject_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        receiver = Account.objects.get(user=request.user)
        sender = Account.objects.get(pk=pk)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('/my-invites')


def viewInvitedProfiles(request):
    user = request.user
    qs = Account.objects.get_all_profiles_to_invite(user)
    context = {'qs': qs}
    return render(request, 'louslistapp/profilesToInvite.html', context)


class AccountListView(ListView):
    model = Account
    template_name = 'louslistapp/profileList.html'
    context_object_name = 'qs'

    # need to override get_queryset method to only get_all_profiles for the qs
    def get_queryset(self):
        qs = Account.objects.get_all_profiles(self.request.user)
        return qs

    # add context details
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # grabs the user
        user = User.objects.get(username__iexact=self.request.user)
        # grabs the related account
        account = Account.objects.get(user=user)
        # relationship where we make the friend request
        rel_r = Relationship.objects.filter(sender=account)
        # relationship where we are receiving the friend request
        rel_s = Relationship.objects.filter(receiver=account)
        rel_receiver = []
        rel_sender = []
        for r in rel_r:
            rel_receiver.append(r.receiver.user)
        for s in rel_s:
            rel_sender.append(s.sender.user)
        
        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender

        # set 'is_empty' to True if we are the only account and there's nobody else available to send a friend request to
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True
        return context


# the current user is sending a friend request to someone else
def send_invitation(request):
    if request.method=='POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Account.objects.get(user=user)
        receiver = Account.objects.get(pk=pk)

        # create the relationship
        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')

        # redirect to the same page you're currently on
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('/profile')


def remove_from_friends(request):
    if request.method=='POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Account.objects.get(user=user)
        receiver = Account.objects.get(pk=pk)

        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )
        rel.delete()

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('/profile')