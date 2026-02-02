from django.urls import path
from todo import cbv_views

app_name = 'todo'

urlpatterns = [
    path("todo/", cbv_views.TodoList.as_view(), name="cbv_todo_list"),
    path("todo/<int:pk>", cbv_views.TodoDetailView.as_view(), name="cbv_todo_info"),
    path("todo/create/",cbv_views.TodoCreateView.as_view(), name="cbv_todo_create"),
    path("todo/<int:pk>/update/", cbv_views.TodoUpdateView.as_view(), name="cbv_todo_update"),
    path("todo/<int:pk>/delete/", cbv_views.TodoDeleteView.as_view(), name="cbv_todo_delete"),
    path("comment/<int:todo_id>/create/", cbv_views.CommentCreateView.as_view(), name="comment_create"),
    path("comment/<int:pk>/update/", cbv_views.CommentUpdateView.as_view(), name="comment_update"),
    path("comment/<int:pk>/delete/", cbv_views.CommentDeleteView.as_view(), name="comment_delete"),
]