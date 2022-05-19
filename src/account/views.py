from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView as _LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, resolve_url
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import SignUpForm


class LoginView(auth_views.LoginView):
    template_name = "account/login.html"

    def get_success_url(self):
        return resolve_url("petition:home")


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("petition:home")
    template_name = "account/signup.html"

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password1"]
        user = authenticate(email=email, password=password)
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())


class LogoutView(_LogoutView):
    def get_next_page(self):
        return reverse("petition:home")
