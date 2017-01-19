from django.shortcuts import render, render_to_response, \
                             redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.views import View

from django.http import HttpResponse, JsonResponse

# local imports
from .models import Event, EventPrevious
from .forms import AuthForm, RegistrationForm, AddEventForm

from django.core.files import File
from django.core.files.storage import FileSystemStorage

from django.conf.urls import url
from django.contrib.staticfiles.templatetags.staticfiles import static
import os


# Base for all View instances in my code,
#   modifies context to render base.html properly
class BaseView(View):
    def render(self, request, template, context):
        context.update({
            'authorized': request.user.is_authenticated,
            'user': {'name': request.user.username},
        })

        return render(request, template, context)


# View displaying 2 forms: AuthForm & RegistrationForm
class LogRegView(BaseView):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)

        return super().render(request, 'registration/login.html', {
                'registration_form': RegistrationForm(),
                'login_form': AuthForm(),
            })


# register new user & login it
def register(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Data should be POSTed to this URL'})

    form = RegistrationForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'error': form.errors.popitem()[1]})

    username = form.cleaned_data.get("username")
    password = form.cleaned_data.get("password1")

    # register now
    user = User.objects.create_user(username=username, password=password)

    # sending auth request
    request.POST = request.POST.copy()
    request.POST['password'] = password
    return auth(request)


# login users
def auth(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return JsonResponse({'error': 'NO'})

    return JsonResponse({'error': 'Неверный логин или пароль.(Валидация работает).'})


# returns requested page
def page_request(request, page_id):
    context = {
        'events': ObjectListView.get_page_dict(page_id),
    }
    return render_to_response('main/base_list.html', context)


# Main Page view, lists all objects
class ObjectListView(BaseView):
    objOnList = 10

    def get_page_dict(page_id):
        page_id = int(page_id)
        st_pos = len(Event.objects.all()) - ObjectListView.objOnList * page_id
        end = st_pos if st_pos > 0 else 0
        if end > ObjectListView.objOnList:
            start = end - ObjectListView.objOnList
        else:
            start = 0

        # need to cut description
        all = Event.objects.all()[start: end: -1]

        for i in all:
            if len(i.desc) > 200:
                i.desc = i.desc[:200] + '...'
        return all

    def get(self, request):
        return super().render(
            request,
            'main/main.html',
            context={
                'name': '', # здесь, если захотим, можно что-то написать ( к зашлавию)
                'events': ObjectListView.get_page_dict(0),
                'add_form': AddEventForm(),
            }
        )

    # Страница добавления объекта
    def post(self, request):
        form = AddEventForm(request.POST)

        if not form.is_valid():
            return JsonResponse(form.errors)

        event = form.fill_object()

        # saving file
        f = request.FILES.get("image")

        if f is None:
            file_url = r'images/default.jpg'
        else:
            file_url = r'images/im/%d%s' % (event.id, '.jpg')
            fs = FileSystemStorage()
            filename = fs.save('main/static/' + file_url, File(f))

        event.imageUrl = file_url
        event.save()
        return redirect('single_object', event_id=event.id)

    # Main Page view, lists all objects
class ObjectListView_history(BaseView):
    objOnList = 10

    def get_page_dict(page_id):
        page_id = int(page_id)
        st_pos = len(EventPrevious.objects.all()) - ObjectListView_history.objOnList * page_id
        end = st_pos if st_pos > 0 else 0
        if end > ObjectListView_history.objOnList:
            start = end - ObjectListView_history.objOnList
        else:
            start = 0

        # need to cut description
        all = EventPrevious.objects.all()[start: end: -1]

        for i in all:
            if len(i.desc) > 200:
                i.desc = i.desc[:200] + '...'
        return all

    def get(self, request):
        return super().render(
            request,
            'main/main.html',
            context={
                'name': '', # здесь, если захотим, можно что-то написать ( к зашлавию)
                'events': ObjectListView_history.get_page_dict(0),
                'add_form': AddEventForm(),
            }
        )

    # Страница добавления объекта
    def post(self, request):
        form = AddEventForm(request.POST)

        if not form.is_valid():
            return JsonResponse(form.errors)

        EventPrevious = form.fill_object()

        # saving file
        f = request.FILES.get("image")

        if f is None:
            file_url = r'images/default.jpg'
        else:
            file_url = r'images/im/%d%s' % (EventPrevious.id, '.jpg')
            fs = FileSystemStorage()
            filename = fs.save('main/static/' + file_url, File(f))

        EventPrevious.imageUrl = file_url
        EventPrevious.save()
        return redirect('single_object', event_id=EventPrevious.id)


# View
class ObjectView(BaseView):
    def get(self, request, event_id):
        obj = get_object_or_404(Event, id=event_id)
        id = request.user.id

        return super().render(
            request,
            'object/object.html',
            context={
                'event': obj,
                'status': obj.participation.filter(id=id).exists(),
            }
        )

    # @login_required(redirect_field_name='login_url')
    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        if request.user.is_authenticated():
            state = request.POST.get('state')
            if state == 'True' \
               and not event.participation.filter(id=request.user.id).exists():
                event.participation.add(request.user)

            if state == 'False' \
               and event.participation.filter(id=request.user.id).exists():
                event.participation.remove(request.user)

        return render_to_response(
            'object/base_user_list.html',
            context={'users': event.participation.all()}
        )
