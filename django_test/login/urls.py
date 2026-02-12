from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    path('', views.Login.as_view(),name='login'),
    path('signup/', views.SignUpView.as_view(),name='signup'),
    path('blog/', views.BlogView.as_view(),name='blog'),
]
