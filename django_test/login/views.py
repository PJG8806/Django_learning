from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView, ListView

from login.forms import LoginForm, SignUp
from login.models import Blog


class Login(FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('login:blog')

    def form_valid(self, form):
        # username = form.cleaned_data['username']
        # user = User.objects.get(username=username)
        user = form.user # forms에 __init__ 사용으로 위에 내용 미사용
        login(self.request, user)
        return HttpResponseRedirect(reverse_lazy('blog:blog'))

class SignUpView(CreateView):
    model = User
    form_class = SignUp
    template_name = 'signup.html'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse_lazy('login:login'))

class BlogView(LoginRequiredMixin ,ListView):
    queryset = Blog.objects.all()
    context_object_name = 'blogs'
