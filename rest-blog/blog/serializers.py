from django.contrib.auth import get_user_model
from rest_framework import serializers

from blog.models import Blog

User = get_user_model()

class UserSerializer(serializers.ModelSerializer): # 폼의 역할과 리턴값 정해주는 기능
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class BlogSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False) # 입력하면 연결된 모델 출력

    class Meta:
        model = Blog
        fields = ['title', 'content', 'author', 'published_at', 'updated_at' ]