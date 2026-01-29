from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.urls import reverse

from .form import TodoForm
from .models import Todo


@login_required()
def todo_list(request):
    todo = Todo.objects.all().order_by("-updated_at")
    q = request.GET.get("q")
    if q:
        todo = todo.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q)
        )
    paginator = Paginator(todo, 10)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)
    context = {"page_object": page_obj}
    return render(request, "todo/todo_list.html", context)


@login_required()
def todo_info(request, todo_id):
    try:
        todo = get_object_or_404(Todo, pk=todo_id)
        context = {"todo": todo.__dict__}
        return render(request, "todo/todo_info.html", context)
    except Todo.DoesNotExist:
        raise Http404("TOdo does not exist")

@login_required()
def todo_create(request):
    form = TodoForm(request.POST or None)
    if form.is_valid():
        todo = form.save(commit=False)
        todo.user = request.user
        todo.save()
        return redirect(reverse('todo_info', kwargs={'todo_id':todo.pk}))

    context = {
        'form':form
    }
    return render(request, 'todo/todo_create.html', context)


@login_required()
def todo_update(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id, user=request.user)

    form = TodoForm(request.POST or None, instance=todo)
    if form.is_valid():
        form.save()
        return redirect(reverse('todo_info', kwargs={'todo_id':todo.pk}))

    context = {
        'form':form
    }
    return render(request, 'todo/todo_update.html', context)

@login_required()
def todo_delete(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    todo.delete()

    return redirect(reverse('todo_list'))