from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from .form import TodoForm, CommentForm, TodoUpdateForm
from .models import Todo, Comment


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
    #queryset = Todo.objects.all().prefetch_related('comments', 'comments__user')
    template_name = 'todo/todo_info.html'
    form_class = CommentForm

    def get(self,request, *args, **kwargs):
        self.object = get_object_or_404(Todo,pk=self.kwargs['pk'])
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Todo.objects.all().prefetch_related('comments','comments__user')

    def get_object(self, queryset = None):
        obj = super().get_object(queryset)

        if self.request.user.username != "admin" and obj.user != self.request.user:
            raise Http404("작성자만 접근이 가능합니다.")
        return obj


    def get_context_data(self, **kwargs):
        comments = self.object.comments.order_by('-created_at')
        paginator = Paginator(comments, 5)
        context = {
            "todo": self.object.__dict__,
            "comment_form": CommentForm(),
            "page_obj": paginator.get_page(self.request.GET.get('page')),
        }
        return context

class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    template_name = 'todo/todo_form.html'
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
    template_name = 'todo/todo_form.html'
    form_class = TodoUpdateForm

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

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'todo_id'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.todo = Todo.objects.get(pk=self.kwargs['todo_id'])
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("todo:cbv_todo_info", kwargs={'pk': self.kwargs['todo_id']})

class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def get_object(self, queryset = None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user and self.request.user.username != "admin":
            raise Http404("작성자 또는 관리자만 수정이 가능합니다.")
        return obj

    def get_success_url(self):
        return reverse_lazy("todo:cbv_todo_info", kwargs={'pk': self.object.todo.id})

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_object(self, queryset = None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user and self.request.user.username != "admin":
            raise Http404("작성자 또는 관리자만 수정이 가능합니다.")
        return obj

    def get_success_url(self):
        return reverse_lazy("todo:cbv_todo_info", kwargs={'pk': self.kwargs['pk']})
