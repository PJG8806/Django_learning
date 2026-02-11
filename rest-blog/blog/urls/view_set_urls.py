
from django.urls import path, include
from rest_framework import routers

from blog.views import api_view_set_views

app_name = 'view_set_api'

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', api_view_set_views.UserViewSet, basename='user') # 무조건 앞에 users/가 붙게 처리 => api/users/
# 어떤 HTTP로 들어오는지에 따라 들어오는 방식을 나눠준다
router.register(r'blogs', api_view_set_views.BlogViewSet, basename='blog')
urlpatterns = [
    # path('', api_views.blog_list, name='blog_list'),
    path('', include(router.urls))
]

