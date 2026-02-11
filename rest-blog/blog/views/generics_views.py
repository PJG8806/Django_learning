from django.db.models import Q
from django.utils import timezone
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, \
    ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from blog.models import Blog, Comment
from blog.serializers import BlogSerializer, CommentSerializer, CommentUpdateSerializer
from utils.models import TimeStampedModel
from utils.permissions import IsAuthorOrReadOnly


class BlogQuerySetMixin: # 중복 부분 클래스로 분리 # 제네레이션
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return self.queryset.filter(
            Q(published_at__isnull=True) |
            Q(published_at__gte=timezone.now())
        ).order_by('-created_at').select_related('author')

class BlogListAPIView(BlogQuerySetMixin, ListCreateAPIView): # 리스트와 생성 API 합친거 상속
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class BlogRetrieveUpdateDestroyAPIView(BlogQuerySetMixin, RetrieveUpdateDestroyAPIView): #RetrieveAPIView는 pk로 값 가져오는거
    # pk값 가져오기, 업데이트, 삭제 API 상속
    permission_classes = [IsAuthorOrReadOnly,] # 만들어서 작성자만 수정 삭제 가능, 읽기 가능

class CommentListCreateAPIView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] # 로그인 사람이면 수정 삭제 가능, 읽기 가능

    def perform_create(self, serializer):
        blog = self.get_blog_object()
        serializer.save(author=self.request.user, blog=blog)

    def get_queryset(self):
        queryset = super().get_queryset()
        blog = self.get_blog_object()
        return queryset.filter(blog=blog)

    def get_blog_object(self): # 함수를 만든 이유는 Blog를 여러번 불러오기 때문에
        return get_object_or_404(Blog, pk=self.kwargs.get('blog_pk'))

class CommentUpdateDestroyAPIView(UpdateAPIView, DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentUpdateSerializer
    permission_classes = [IsAuthorOrReadOnly]