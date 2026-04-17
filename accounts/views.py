from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import LoginForm, SignupForm


class UserSignupView(CreateView):
    form_class = SignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('queues:services')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Welcome to Navbat.uz!')
        return redirect(self.success_url)


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        messages.success(self.request, 'You are logged in successfully.')
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('landing')

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, 'You have been logged out.')
        return redirect(self.next_page)
