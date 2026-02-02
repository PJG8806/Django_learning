from IPython.core.release import author
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from blog.forms import BlogForm
from blog.models import Blog

def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')

    q = request.GET.get('q')
    if q:
        # or 검색 아니면 Q 빼고 하나만 넣기
        blogs = blogs.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q)
        )

    paginator = Paginator(blogs, 10) # 페이지네이터 효과
    page = request.GET.get('page')
    page_object = paginator.get_page(page)

    visits = int(request.COOKIES.get('visits', 0)) + 1
    # visits 키값으로 만들며 0은 널일때 디폴트 값을 넣고 +1로 1을 더해준다
    # 쿠키 값은 웹 브라우저에 저장 되어서 보안 문제가 있다

    #request.session['count'] = request.session.get('count', 0) +1
    # 세션 추가

    context = {
        #'blogs': blogs,
        'object_list': page_object,
        'pag_obj': page_object,
    }

    response = render(request, 'blog_list.html', context)

    #response.set_cookie('visits', visits) # 쿠키 추가

    return response

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    context = {'blog': blog}
    return render(request, 'blog_detail.html', context)


@login_required()
def blog_create(request):
    # if not request.user.is_authenticated:
    #     return redirect(reverse('login'))
    # @login_required() 위에 부분과 같은 효과

    form = BlogForm(request.POST or None)
    if form.is_valid():
        blog = form.save(commit=False) # DB에 저장은 안하고 모델만 만든다
        blog.author = request.user
        blog.save()
        return redirect(reverse('fb:detail', kwargs={'pk' : blog.pk}))

    context = {'form': form}
    return render(request, 'blog_form.html', context)


@login_required()
def blog_update(request, pk):
    blog = get_object_or_404(Blog, pk=pk, author=request.user)
    # if request.user != blog.author:
    #     raise HTTp404

    form = BlogForm(request.POST or None, instance=blog) # instance 넣으면 값에 맞게 form에 넣어준다 (기초 데이터, 수정 전 값)
    if form.is_valid():
        blog = form.save() # DB에 저장은 안하고 모델만 만든다
        return redirect(reverse('fb:detail', kwargs={'pk' : blog.pk}))

    context = {
        'form': form,
    }
    return render(request, 'blog_form.html', context)

@login_required()
@require_http_methods(['POST']) # POST 값만 받는다
def blog_delete(request, pk):
    # if request.method != 'POST':
    #     raise Http404()

    blog = get_object_or_404(Blog, pk=pk, author=request.user)
    blog.delete()

    return redirect(reverse('fb:list'))