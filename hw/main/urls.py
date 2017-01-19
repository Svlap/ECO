"""hw URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views


urlpatterns = [

    url(r'^login/register$', views.register, name='register_url'),
    url(r'^login/auth$', views.auth, name='auth_url'),
    url(r'^login$', views.LogRegView.as_view(), name='login_url'),
    url(r'^event/(?P<event_id>[0-9]+)', views.ObjectView.as_view(), name='single_object'),

    url(r'^page/(?P<page_id>[0-9]+)', views.page_request, name='page_request'),
    url(r'^history$', views.ObjectListView_history.as_view(), name='main_page_history'),
    url(r'^$', views.ObjectListView.as_view(), name='main_page'),
]
