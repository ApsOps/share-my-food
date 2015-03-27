from django.http import HttpResponse
from django.views import generic
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render

from braces import views

from .models import *

# Create your views here.


class HomePageView(generic.TemplateView):
    template_name = "home.html"


class ProfileView(generic.TemplateView):
    template_name = "profile.html"


class SignUpView(views.AnonymousRequiredMixin, views.FormValidMessageMixin,
                 generic.CreateView):
    form_class = RegistrationForm
    form_valid_message = "Account created successfully! Go ahead and login."
    model = User
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'


class LoginView(views.AnonymousRequiredMixin, views.FormValidMessageMixin,
                generic.FormView):
    form_class = LoginForm
    form_valid_message = "You're logged into your account."
    success_url = reverse_lazy('home')
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)


class LogOutView(views.LoginRequiredMixin, views.MessageMixin,
                 generic.RedirectView):
    url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        logout(request)
        self.messages.success("You've been successfully logged out.")
        return super(LogOutView, self).get(request, *args, **kwargs)


def update_location(request):
    user = request.user
    lng = request.POST.get("lng", "")
    lat = request.POST.get("lat", "")
    user_model = UserModel.objects.get(pk=user.pk)
    user_model.longitude = lng
    user_model.latitude = lat
    user_model.save()
    messages = ["Your location has been saved!"]
    params = { "messages" : messages }
    return render(request, 'profile.html', params)