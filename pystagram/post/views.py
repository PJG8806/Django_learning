from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView

from post.forms import PostForm, PostImageFormSet, CommentForm
from post.models import Post, Like


class PostListView(ListView):
    # Post가 ForeignKey를 가지고 있으면 select_related가능하다
    # prefetch_related는 역참조로 post 값이 같은 image 값들을 추가로 가져온다

    # Post-User는 JOIN으로 가져오고,
    # Post의 PK에 해당하는 images는 prefetch로 미리 로드하여
    # 반복 접근 시 추가 DB 쿼리(N+1 문제)를 방지한다.

    queryset = Post.objects.all().select_related('user').prefetch_related('images','comments', 'likes')
    template_name = 'post/list.html'
    paginate_by = 5
    ordering = ('-created_at',)

    def get_context_data(self, *args, **kwargs): # html 쪽으로 던져주는 부분
        data = super().get_context_data(*args, **kwargs) # super() -> 부모 클래스의 .뒤에 내용 실행
        data['comment_form'] = CommentForm()
        return data

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    template_name = 'post/form.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['formset'] = PostImageFormSet()
        return data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        image_formset = PostImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        if image_formset.is_valid(): # 묶음에서 전부 규칙이 맞는지 확인
            image_formset.save()

        return HttpResponseRedirect(reverse('main'))

class PostUpdateView(LoginRequiredMixin,UpdateView):
    model = Post
    template_name = 'post/form.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['formset'] = PostImageFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        self.object = form.save()

        image_formset = PostImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        if image_formset.is_valid():
            image_formset.save()

        return HttpResponseRedirect(reverse('main'))

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

@csrf_exempt # 이 뷰에서만 csrf 무시
@login_required()
def toggle_like(request):
    post_pk = request.POST.get('post_pk')
    if not post_pk:
        raise Http404

    post = get_object_or_404(Post, pk=post_pk)
    user = request.user

    like, created = Like.objects.get_or_create(user=user, post=post)
    if not created:
        like.delete()

    return JsonResponse({'created': created}) # 자바스크립트에 값을 넘긴다
