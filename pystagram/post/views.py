from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView

from post.forms import PostForm, PostImageFormSet
from post.models import Post


class PostListView(ListView):
    # Post가 ForeignKey를 가지고 있으면 select_related가능하다
    # prefetch_related는 역참조로 post 값이 같은 image 값들을 추가로 가져온다

    # Post-User는 JOIN으로 가져오고,
    # Post의 PK에 해당하는 images는 prefetch로 미리 로드하여
    # 반복 접근 시 추가 DB 쿼리(N+1 문제)를 방지한다.

    queryset = Post.objects.all().select_related('user').prefetch_related('images')
    template_name = 'post/list.html'
    paginate_by = 5
    ordering = ('-created_at',)

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