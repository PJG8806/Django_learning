from django.test import TestCase
from users.models import CustomUser
from posts.models import Post
from .models import Comment
from .serializers import CommentSerializer
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='author', password='pass')
        self.post = Post.objects.create(title='Post', content='Content', author=self.user)

    def test_create_comment(self):
        comment = Comment.objects.create(content='Test Comment', post=self.post, author=self.user)
        self.assertEqual(comment.content, 'Test Comment')
        self.assertEqual(comment.post.title, 'Post')

class CommentSerializerTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='author', password='pass')
        self.post = Post.objects.create(title='Post', content='Content', author=self.user)
        self.comment_data = {'content': 'Valid Comment', 'post': self.post.id, 'author': self.user.id}

    def test_valid_serializer(self):
        serializer = CommentSerializer(data=self.comment_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_content(self):
        invalid_data = self.comment_data.copy()
        invalid_data['content'] = 'Short'
        serializer = CommentSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('content', serializer.errors)

class CommentAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient() # API 를 테스트하니까.
        self.user = CustomUser.objects.create_user(username='testuser', password='testpass') # 사전에 준비해야 할 기본 유저
        self.client.force_authenticate(user=self.user) # 인증 무시
        self.post = Post.objects.create(title='Post', content='Content', author=self.user) # 사전에 준비해야 할 블로그 포스트
        self.comment = Comment.objects.create(content='Existing Comment', post=self.post, author=self.user) # 사전에 준비해야 할 블로그 포스트에 달린 이미 달린 댓글

    def test_get_comments(self):
        url = reverse('comment-list')  # basename='comment' 기준
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.count(), 1)

    def test_create_comment(self):
        url = reverse('comment-list')
        # post 필드에 post.id를 전달
        data = {'content': 'New Comment', 'post': self.post.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)
