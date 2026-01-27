from django.shortcuts import render
from django.http import Http404
from .models import Todo


def todo_list(request):
    todo_list = Todo.objects.all().values_list("id", "title")
    result = [{"id": todo[0], "title": todo[1]} for i, todo in enumerate(todo_list)]
    context = {"data": result}

    return render(request, "todo_list.html", context)


def todo_info(request, todo_id):
    try:
        todo = Todo.objects.get(id=todo_id)
        info = {
            "title": todo.title,
            "description": todo.description,
            "start_date": todo.start_date,
            "end_date": todo.end_date,
            "is_completed": todo.is_completed,
        }
        context = {"data": info}

        return render(request, "todo_info.html", context)
    except Todo.DoesNotExist:
        raise Http404("TOdo does not exist")
