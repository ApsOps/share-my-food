from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',

    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^location/$', LocationView.as_view(), name='location'),
    url(r'^updatelocation$', update_location, name='update_location'),

    url(r'^add/$', AddFoodView.as_view(), name='add'),
    url(r'^find/$', FindFoodView.as_view(), name='find'),

    url(r'^accounts/register/$', SignUpView.as_view(), name='signup'),
    url(r'^accounts/login/$', LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', LogOutView.as_view(), name='logout'),

)
