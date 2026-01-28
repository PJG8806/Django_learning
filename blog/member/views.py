from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login as django_login
from django.urls import reverse

def sign_up(request):
    # username = request.POST['username'] # get 요청일때 request.POST.get('username')방식을 사용
    # password1 = request.POST['password1']
    # password2 = request.POST['password2']

    # 밑에 부분을 간소화 값이 있으면 form 에 POST에 저장 POST가 아니면 None로 저장
    # 으로 저장 안함
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(settings.LOGIN_URL)

    # if request.method == 'POST':
    #     form = UserCreationForm(request.POST) # form에 값을 넣어서 유효성 체크
    #     if form.is_valid(): # 값이 유효하면
    #         form.save() # 유저 정보 저장
    #         return redirect('/accounts/login/')
    # else:
    #     form = UserCreationForm() # else일때 폼을 다시 하면 에러 메시지 미출력

    context = {
        'form': form
    }
    return render(request, 'registration/signup.html', context)

def login(request):
    form = AuthenticationForm(request, request.POST or None) # 입력한 유저 정보로 로그인
    if form.is_valid():
        django_login(request, form.get_user())
        return redirect(reverse('blog_list')) # html url 함수처럼 이름을 찾아 url을 설정해준다
        # redirect 페이지 이동
    context = {
        'form': form
    }
    return render(request, 'registration/login.html', context)