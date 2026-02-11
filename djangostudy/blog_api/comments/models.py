from django.db import models
from posts.models import Post
from users.models import CustomUser

class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete= models.CASCADE, related_name= 'comments') # post.comments 로 접근 가능
    author = models.ForeignKey(CustomUser, on_delete= models.CASCADE, related_name= 'comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at'] # 최신순 정렬
        indexes = [models.Index(fields=['post', 'author'])]  # 쿼리 최적화 인덱스 추가
