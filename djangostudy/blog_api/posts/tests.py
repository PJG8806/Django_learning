from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from users.models import CustomUser
from .models import Post
from .serializers import PostSerializer
from django.urls import reverse
from rest_framework import status

# class MyAPITests(APITestCase):
#     def setUp(self): # 처음 시작
#         #self.client = APIClient()
#         print("setUp()")

#     def test_emample(self):
#         self.assertEqual(1 + 1, 2)
   
#     def test2_emample(self):
#         self.assertEqual(1 + 1, 2)

#     def tearDown(self): # 끝에 시작
#         print("tearDown()")

# # 결과 setUp() -> test_emample() -> tearDown() -> setUp() -> test2_emample() -> tearDown()

class PostModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='author', password='pass')
    
    def test_create_post(self):
        # ACT
        post = Post.objects.create(title='Test Title', content='Test Content', author=self.user)

        # Assert
        self.assertEqual(post.title, 'Test Title')
        self.assertEqual(post.author.username, 'author')
    
class PostSerializerTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='author', password='pass')
        self.post_data = {'title': 'Valid Title', 'content': 'Valid Content', 'author': self.user.id}

    def test_valid_serializer(self):
        serializer = PostSerializer(data=self.post_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_title(self):
        invalid_data = self.post_data.copy()
        invalid_data['title'] = '4444'
        serializer = PostSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)

class PostAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='author', password='pass')
        self.client.force_authenticate(user=self.user) # 인증이 되었다고 강제로 설정
        self.post = Post.objects.create(title='Test Title', content='Test Content', author=self.user)

    def test_get_posts(self):
        url = reverse('post-list')
        response = self.client.get(url) # post-list는 urls.py에서 router로 설정한 이름 정보를 가져온다
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data['results'][0]['title'], self.post.title) pagination 있을 때
        # self.assertEqual(response.data[0]['title'], self.post.title) # pagination 없을
    
    def test_create_post(self):
        url = reverse('post-list')
        data = {'title': 'New Post', 'content': 'New Content'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)