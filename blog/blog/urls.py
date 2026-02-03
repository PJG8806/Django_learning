from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from blog import cb_views
from blog import views

app_name = 'blog'

urlpatterns=[
    path('', cb_views.BlogListView.as_view(), name='list'),
    path('<int:blog_pk>/', cb_views.BlogDetailView.as_view(), name='detail'),
    path('create/', cb_views.BlogCreateView.as_view(), name='create'),
    path('<int:pk>/update/', cb_views.BlogUpdateView.as_view(), name='update'),
    #path('<int:pk>/update/', views.blog_update, name='update'),
    path('<int:pk>/delete/', cb_views.BlogDeleteView.as_view(), name='delete'),
    path('comment/create/<int:blog_pk>/', cb_views.CommentCreateView.as_view(), name='comment_create'),
    # 별도의 설정 아니면 pk로 해야 제대로 가져온다

]

