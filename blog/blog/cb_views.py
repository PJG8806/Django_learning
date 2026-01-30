from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.forms import BlogForm
from blog.models import Blog


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


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog_detail.html'
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


class BlogCreateView(LoginRequiredMixin, CreateView):
    # LoginRequiredMixin은 데코레이터 @login_required() 같은 의미 기능
    model = Blog
    template_name = 'blog_create.html'
    fields = ('category', 'title', 'content') # fields 오류가 난다면 form을 설정하는거 처럼 filter에 fields 설정을 해야 한다
    #success_url = reverse_lazy('cb_blog_list') # class에서는 reverse를 사용하면 두번 호출로 인해 써큘러임폴트 문제가 생겨서 _lazy를 붙여서 사용한다

    def form_valid(self, form): # 외래키 값을 추가하기 위한 방법 또는 폼 검증을 하는 부분(검증 완료시 실행)
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        # pk나 별도의 값을 받으면서 reverse를 사용한다면 이 방식으로 해야 한다( 위에 폼의 부분이 다 처리가 될때까지 어떤 페이지인지 모르기 때문에 이렇게 해야 한다
        return reverse_lazy('blog:detail', kwargs={'pk':self.object.pk})


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    template_name = 'blog_update.html'
    fields = ('category', 'title','content')

    def get_queryset(self): # 작성한 사람만 접근이 가능하게 필터기능
        # get_queryset는 어떤 데이터들을 다루는 부분
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(author=self.request.user) # 모두 접근이 가능하게 하면 .filter을 지우면 된다

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