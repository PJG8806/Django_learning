"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.urls import path
from django.shortcuts import redirect
from bookmark import views


movie_list = [
    {'title':'파묘', 'director': '장재현'},
    {'title':'윙카', 'director': '폴 킹'},
    {'title':'듄: 파트2', 'director': '드니 빌뇌브'},
    {'title':'시민덕희', 'director': '박영주'},
]


def index(request):
    return HttpResponse("<h1>Hello</h1>")

def book_list(request):

    # book_text = ''
    #
    # for i in range(0, 10):
    #     book_text += f'book {i}<br>'

    return render(request, template_name='book_list.html', context= {'range': range(0, 10)})

def book(request, num):
    return render(request, template_name='book_detail.html', context= {'num': num})

def language(request, lang):
    return HttpResponse(f"<h1>{lang} 언어 페이지입니다.")

def python(request):
    return HttpResponse('python 페이지 입니다.')

def movies(request):
    # movie_title = [
    #     f'<a href="/movie/{index}/">{movie["title"]}</a>'
    #     for index, movie in enumerate(movie_list)
    # ]
    #
    # # movie_titles = []
    # # for movie in movie_list:
    # #     movie_titles.append(movie['title'])
    #
    # response_text = '<br>'.join(movie_title)
    # return HttpResponse(response_text)

    from django.shortcuts import render
    return render(request, template_name= 'movies.html', context= {'movie_list': movie_list})


def movie_detail(request, index):
    if index > len(movie_list)-1:
        raise Http404

    movie = movie_list[index]
    context = {'movie': movie}

    return render(request, template_name='movie.html', context= context)


def gugu(request, num):
    if num <2:
        return redirect('/gugu/2/') # 2 이하로 들어오면 /gugu/2/로 다시 보내기

    context = {
        'num': num,
        'results': [(i, num * i) for i in range(1, 10)]
        #'range': range(1, 10)
    }
    return render(request, template_name='gogo.html', context= context)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('book_list/', book_list),
    path('book_list/<int:num>/', book),
    path('language/python/', python),
    path('language/<str:lang>/', language),
    path('movie/', movies),
    path('movie/<int:index>/', movie_detail),
    path('gugu/<int:num>/', gugu),
    path('bookmark/', views.bookmark_list),
    path('bookmark/<int:pk>/', views.bookmark_detail),

]


# ipython 패키지 설치  사용시 터미널 shell 작업을 편하게 가능하다
# python manage.py shell 실행
# python manage.py shell_plus 여러가지 임폴트를 바로 해준다