from sqlite3 import connect

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.forms import BlogForm, CommentForm
from blog.models import Blog, Comment


class BlogListView(ListView):
    # 이방식을 사용 한다면 object_list로 해야 반복문 받아온다
    # model = Blog #이 방법은 자동 order_by
    queryset = Blog.objects.all()#.order_by('-created_at') # 별도의 조건 또는 다른 정렬을 할려면 이방법
    ordering = ('-created_at',) # 별도로 정렬 주는 방법
    template_name = 'blog_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        q = self.request.GET.get('q')

        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(content__icontains=q)
            )
        return queryset


class BlogDetailView(ListView):
    #model = Blog
    model = Comment
    #queryset = Blog.objects.all().prefetch_related('comment_set', 'comment_set__author')
    # comment_set 과 comment_set__author 조인해서 불러온다 이 방식을 안하면 db를 여러번 호출을 하게 된다
    template_name = 'blog_detail.html'
    paginate_by = 10
    pk_url_kwarg = 'blog_pk'
    # pk_url_kwarg = 'id' # 이렇게 하면 pk가 아닌 다른 값으로도 가져오게 가능하다
    # 이 방식으로 사용은 object.db값으로 처리 한다
    # def get_queryset(self): # 위에 BlogListView 처럼 queryset 가능하다
    #     queryset = super().get_queryset()
    #
    #     return queryset.filter(id__lte=50)

    # def get_object(self, queryset = None):
    #     object = super().get_object()
    #     # object = self.model.objects.get(pk=self.kwargs.get('pk')) 위 내용은 이거랑 같은 의미( kwargs url로 들어오는 부분을 가져온다)
    #     return object

    # def get_context_data(self, **kwargs): # template 사용 부분들은 이 방식으로 context를 추가가 가능하다
    #     context = super().get_context_data(**kwargs)
    #     context['test'] = 'CBV'
    #     return context

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(Blog, pk=kwargs.get('blog_pk'))
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(blog=self.object).prefetch_related('author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['blog'] = self.object
        return context


    # # 댓글 추가 방법 1
    # def get_context_data(self, **kwargs):
    #      context = super().get_context_data(**kwargs)
    #      context['comment_form'] = CommentForm()
    #      return context
    #
    # def post(self, *args, **kwargs):
    #     comment_form = CommentForm(self.request.POST)
    #
    #     if not comment_form.is_valid():
    #
    #         self.object = self.get_object() # 객체를 다시 가져온다
    #         context = self.get_context_data(object=self.object) # 가져와서 템플릿에 넘길 context생성
    #         context['comment_form'] = comment_form # 유효성 검사 실패의 에러 메시지 추가
    #         return self.render_to_response(context) # 에러 메시지 전달후 다시 렌더링
    #
    #     if not self.request.user.is_authenticated: # 로그인 여부 확인
    #         raise Http404
    #
    #     comment = comment_form.save(commit=False)
    #     #comment.author = self.get_object() # 밑에랑 같은 의미
    #     comment.blog_id = self.kwargs['pk']
    #     comment.author = self.request.user
    #     comment.save()
    #
    #     return HttpResponseRedirect(reverse_lazy('blog:detail', kwargs={'pk': self.kwargs['pk']}))



class BlogCreateView(LoginRequiredMixin, CreateView):
    # LoginRequiredMixin은 데코레이터 @login_required() 같은 의미 기능
    model = Blog
    template_name = 'blog_form.html'
    #fields = ('category', 'title', 'content') # fields 오류가 난다면 form을 설정하는거 처럼 filter에 fields 설정을 해야 한다
    form_class = BlogForm
    #success_url = reverse_lazy('cb_blog_list') # class에서는 reverse를 사용하면 두번 호출로 인해 써큘러임폴트 문제가 생겨서 _lazy를 붙여서 사용한다

    def form_valid(self, form): # 외래키 값을 추가하기 위한 방법 또는 폼 검증을 하는 부분(검증 완료시 실행)
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    # def get_success_url(self):
    #       # pk나 별도의 값을 받으면서 reverse를 사용한다면 이 방식으로 해야 한다( 위에 폼의 부분이 다 처리가 될때까지 어떤 페이지인지 모르기 때문에 이렇게 해야 한다
    #     return reverse_lazy('blog:detail', kwargs={'blog_pk':self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_title'] = '작성'
        context['btn_name'] = '생성'
        return context


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    template_name = 'blog_form.html'
    form_class = BlogForm

    def get_queryset(self): # 작성한 사람만 접근이 가능하게 필터기능
        # get_queryset는 어떤 데이터들을 다루는 부분
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(author=self.request.user) # 모두 접근이 가능하게 하면 .filter을 지우면 된다

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    # def get_object(self, queryset=None): 위에 get_queryset의 같은 결과를 내는 방식
    #   get_object는 어떤 하나를 다루는 부분
    #     self.object = super().get_object(queryset)
    #
    #     if self.object.author != self.request.user:
    #         raise Http404
    #     return self.object


    # def get_success_url(self)를 models에 (get_success_url,get_absolute_url 작업 끝나고 어디로 갈지)
    # def get_absolute_url(self):
    #         return reverse('cb_blog_detail', kwargs={'pk': self.objects.pk})
    # 이 방법으로 처리 가능하다

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_title'] = '작성'
        context['btn_name'] = '생성'
        return context

class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(author=self.request.user)
        #return queryset.filter(author=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse_lazy('blog:list')

# 댓글 추가 방법 2
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def get(self, request, *args, **kwargs): # get 요청을 막기 위해 추가
        raise  Http404

    def form_valid(self, form):
        blog = self.get_blog()
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.blog = self.get_blog()
        self.object.save()
        return HttpResponseRedirect(reverse('blog:detail', kwargs={'blog_pk': blog.pk}))


    def get_blog(self): # blog 정보를 가져오기 위해
        pk = self.kwargs['blog_pk']
        blog = get_object_or_404(Blog, pk=pk)
        return blog
