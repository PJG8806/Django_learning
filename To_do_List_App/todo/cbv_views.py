from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from .form import TodoForm
from .models import Todo


class TodoList(LoginRequiredMixin, ListView):
    queryset = Todo.objects.all()
    ordering = ('-created_at',)
    template_name = 'todo/todo_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        q = self.request.GET.get('q')

        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q)
            )
        if self.request.user.username == "admin":
            return queryset
        return queryset.filter(user=self.request.user)

class TodoDetailView(LoginRequiredMixin, DetailView):
    model = Todo
    template_name = 'todo/todo_info.html'

    def get_object(self, queryset = None):
        obj = super().get_object(queryset)

        if self.request.user.username != "admin" and obj.user != self.request.user:
            raise Http404("작성자만 접근이 가능합니다.")
        return obj

    def get_context_data(self, **kwargs):
        context = {'todo' : self.object.__dict__}
        return context

class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    template_name = 'todo/todo_create.html'
    form_class = TodoForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('todo:cbv_todo_info', kwargs={'pk':self.object.pk})

class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    template_name = 'todo/todo_update.html'
    form_class = TodoForm

    def get_object(self, queryset = None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user and self.request.user.username != "admin":
            raise Http404("작성자 또는 관리자만 수정이 가능합니다.")
        return obj

    def get_success_url(self):
        return reverse_lazy('todo:cbv_todo_info', kwargs={'pk':self.object.pk})


class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo

    def get_object(self, queryset = None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user and self.request.user.username != "admin":
            raise Http404("작성자 또는 관리자만 수정이 가능합니다.")
        return obj

    def get_success_url(self):
        return reverse_lazy('todo:cbv_todo_list')