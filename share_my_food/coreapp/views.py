from django.http import HttpResponse
from django.views import generic
from .forms import RegistrationForm, LoginForm, EntryForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render

from braces import views

from .models import *

# Create your views here.


class HomePageView(generic.TemplateView):
    template_name = "home.html"


class LocationView(generic.TemplateView):
    template_name = "location.html"


class SignUpView(views.AnonymousRequiredMixin, views.FormValidMessageMixin,
                 generic.CreateView):
    form_class = RegistrationForm
    form_valid_message = "Account created successfully. Please login and set your location first!"
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
    user_model = UserModel.objects.get(user=user)
    user_model.longitude = lng
    user_model.latitude = lat
    user_model.save()
    messages = ["Your location has been saved!"]
    params = { "messages" : messages }
    return render(request, 'home.html', params)


class AddFoodView(views.LoginRequiredMixin, views.FormValidMessageMixin,
               generic.CreateView):
    form_class = EntryForm
    form_valid_message = "Data added successfully."
    model = Food
    success_url = reverse_lazy('add')
    template_name = "add/entry.html"

    def form_valid(self, form):
        if UserModel.objects.get(user=self.request.user).longitude is None:
            messages = ["You need to set your location first!"]
            params = { "messages" : messages }
            return render(self.request, 'location.html', params)
        else:
            form.instance.owner = self.request.user
            return super(AddFoodView, self).form_valid(form)


class FindFoodView(views.LoginRequiredMixin, views.MessageMixin,
                 generic.RedirectView):

    def get(self, request, *args, **kwargs):
        return find_food(request)


def find_food(request):
    user = UserModel.objects.get(user=request.user)
    if user.longitude is None:
        messages = ["You need to set your location first!"]
        params = { "messages" : messages }
        return render(request, 'location.html', params)
    else:
        lng = user.longitude
        lat = user.latitude 
        foods = Food.objects.all()
        users = []
        for x in foods:
            user1 = UserModel.objects.get(pk=x.owner.pk)
            users.append(user1)
        data = zip(foods, users)
        params = {'lng': lng, 'lat': lat, 'data': data }
        return render(request, 'find.html', params)
