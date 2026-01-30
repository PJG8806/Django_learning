from django.urls import path
from todo import cbv_views

app_name = 'todo'

urlpatterns = [
    path("todo/", cbv_views.TodoList.as_view(), name="cbv_todo_list"),
    path("todo/<int:pk>", cbv_views.TodoDetailView.as_view(), name="cbv_todo_info"),
    path("todo/create/",cbv_views.TodoCreateView.as_view(), name="cbv_todo_create"),
    path("todo/<int:pk>/update/", cbv_views.TodoUpdateView.as_view(), name="cbv_todo_update"),
    path("todo/<int:pk>/delete/", cbv_views.TodoDeleteView.as_view(), name="cbv_todo_delete"),
]