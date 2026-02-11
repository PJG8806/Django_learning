from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Comment
from .serializers import CommentSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # 인증 제한 베스트 프랙티스
    filter_backends = [filters.SearchFilter] # 검색어를 포함 시켜서 해당하는 부분만 리턴
    search_fields = ['content']# 검색어 필드 설정 ?search=나올 숫자 및 content:내용

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # 생성 시 author 자동 설정 오버라이드

