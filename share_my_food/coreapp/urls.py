from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',

    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^updatelocation$', update_location, name='update_location'),

    url(r'^accounts/register/$', SignUpView.as_view(), name='signup'),
    url(r'^accounts/login/$', LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', LogOutView.as_view(), name='logout'),

)
