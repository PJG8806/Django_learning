from django.shortcuts import render, get_object_or_404
from blog.models import Blog

def blog_list(request):
    blogs = Blog.objects.all()

    visits = int(request.COOKIES.get('visits', 0)) + 1
    # visits 키값으로 만들며 0은 널일때 디폴트 값을 넣고 +1로 1을 더해준다
    # 쿠키 값은 웹 브라우저에 저장 되어서 보안 문제가 있다

    request.session['count'] = request.session.get('count', 0) +1
    # 세션 추가

    context = {
        'blogs': blogs,
        'count': request.session['count'],
    }

    response = render(request, 'blog_list.html', context)

    response.set_cookie('visits', visits)

    return response

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    context = {'blog': blog}
    return render(request, 'blog_detail.html', context)