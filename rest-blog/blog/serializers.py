from django.contrib.auth import get_user_model
from rest_framework import serializers

from blog.models import Blog, Comment

User = get_user_model()

class UserSerializer(serializers.ModelSerializer): # 폼의 역할과 리턴값 정해주는 기능
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class BlogSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False, read_only=True) # 입력하면 연결된 모델 출력 # read_only 넣어야 노출 안됨
    comment_count = serializers.SerializerMethodField() # 함수를 만들어서 가지고 있는다(변수명 앞에 get_ 붙여서 만든다
    author_name = serializers.SerializerMethodField()

    def get_comment_count(self, obj):
        return obj.comment_set.count()

    def get_author_name(self, obj):
        return obj.author.username

    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'author', 'published_at', 'updated_at', 'comment_count', 'author_name' ]

# class CommentSerializer(serializers.ModelSerializer):
#     author = UserSerializer(many=False, read_only=True)
#
#     class Meta:
#         model = Comment
#         fields = ['id', 'author', 'content']

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content']

class CommentUpdateSerializer(CommentSerializer): # 상속을 받아서 추가 부분만 추가 가능
    blog = BlogSerializer(many=False, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'blog']
# class CommentUpdateSerializer(serializers.ModelSerializer):
#     author = UserSerializer(many=False, read_only=True)
#     blog = BlogSerializer(many=False, read_only=True)
#
#     class Meta:
#         model = Comment
#         fields = ['id', 'author', 'content', 'blog']