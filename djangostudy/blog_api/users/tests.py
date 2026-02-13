from django.test import TestCase
from django.contrib.auth import get_user_model

class CustomUserTest(TestCase):
    def test_create_user(self):
        # Arrange 사전 작업
        User = get_user_model() # 커스텀 유저여서 사용 해야 한다
        
        # Act 실행
        user = User.objects.create_user(
            username='testuser', 
            password='testpass123', 
            bio='Test bio')
        
        # Assert 검증
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpass123'))
        self.assertEqual(user.bio, 'Test bio')