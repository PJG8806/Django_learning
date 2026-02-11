
from rest_framework import status
from rest_framework.decorators import api_view, schema
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.views import APIView

from blog.models import Blog
from blog.serializers import BlogSerializer
from utils.permissions import IsAuthorOrReadOnly


class BlogListCreateAPIView(APIView): # 쉬프트 F6 전체 리네임 기능
    permission_classes = [IsAuthenticatedOrReadOnly] # 로그인 체크
    # 모든 권한이 필요하면 IsAuthenticated, IsAuthenticatedOrReadOnly 읽기 제외 권한 필요하다

    def get(self, request, format=None):
        blog_list = Blog.objects.all().order_by('-created_at').select_related('author')
        paginator = PageNumberPagination() # 페이지네비게이션 정보 가져오기
        queryset = paginator.paginate_queryset(blog_list, request) # 적용

        serializer = BlogSerializer(queryset, many=True)
        return paginator.get_paginated_response(serializer.data) # 적용된 페이지네이션 형식 출력

    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            blog = serializer.save(author=request.user) # serializer author=request.user 방식으로 데이터를 넣어야 한다

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST) # 시리얼라이즈에 검증 실패하면 오류 메시지 출력

class BlogDetailAPIView(APIView):
    object = None
    permission_classes = [IsAuthorOrReadOnly]

    def get(self, request, format=None, *args, **kwargs):
        blog = self.get_object(request, *args, **kwargs)
        serializer = BlogSerializer(blog, many=False)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        blog = self.get_object(request, *args, **kwargs)
        serializer = BlogSerializer(blog, data=request.data, partial=True)  # 일부 값만 들어와도 괜찮다
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        blog = self.get_object(request, *args, **kwargs)
        blog.delete()

        return Response(
            {'deleted': True,
             'pk': kwargs.get('pk',0)
             }, status=status.HTTP_200_OK)

    def get_object(self, request, *args, **kwargs):
        if self.object: # db에 한번만 가게 한다
            return self.object

        blog_list = Blog.objects.all().select_related('author')
        pk = kwargs.get('pk', 0)
        # if not pk: # 블로그가 0이면 걸러져서 미사용
        #     raise Http404

        # blog = blog_list.filter(pk=pk).first()
        # if not blog:
        #     raise Http404
        blog = get_object_or_404(blog_list, pk=pk) # Blog 넣어도 된다
        self.object = blog
        return blog

@api_view(['GET', 'POST']) # FBV 방식
@schema(AutoSchema())
def detail_view(request, pk):
    if request.method == 'POST': # 이렇게 많아져서 CBV 방식 추천
        pass
    elif request.method == 'GET':
        blog_list = Blog.objects.all().select_related('author')

        blog = get_object_or_404(blog_list, pk=pk) # Blog 넣어도 된다

        serializer = BlogSerializer(blog, many=False)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        pass
    elif request.method == 'DELETE':
        pass
