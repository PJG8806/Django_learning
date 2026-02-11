from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Post
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer # 이것과 이 밑에께 핵심적이다
    permission_classes = [IsAuthenticatedOrReadOnly]  # 인증 제한 베스트 프랙티스 (인증이 된 유저에 대해서 crud 다 가능하고 아니면 r만)

    def perform_create(self, serializer): # author은 외래키로 인증된 정보로 꺼내기 때문에 상속 받아서 사용
        serializer.save(author=self.request.user)  # 생성 시 author 자동 설정 오버라이드

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)  # 수정 시 author 자동 설정 오버라이드