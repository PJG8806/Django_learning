from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        # 유저 모델 테스트 시 필요한 세팅 기재
        self.test_user ={
            'email': 'test@example.com',
            'nickname': 'test',
            'password': 'password1234',
        }

        self.test_admin_user = {
            'email': 'admin@example.com',
            'nickname': 'adminuser',
            'password': 'password1234',
        }

    def test_user_manager_create_user(self):
        # UserManager의 create_user 메서드를 테스트하기 위한 코드 기재
        # 유저 매니저를 사용하여 setUp 데이터를 바탕으로 유저 모델을 생성
        user = User.objects.create_user(**self.test_user)
        # 유저 모델이 생성되었는지 카운트를 확인
        self.assertEqual(User.objects.count(), 1)

        # 생성된 유저 모델의 속성을 확인
        self.assertEqual(user.email, self.test_user['email'])
        self.assertEqual(user.nickname, self.test_user['nickname'])
        self.assertTrue(user.password, self.test_user['password']) # assertTrue 참 여부 검사
        self.assertFalse(user.is_staff) # assertFalse False일때 테스트 통과
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

        self.assertEqual(user.profile_image.url, '/media/users/blank_profile_image.png')


    def test_user_manager_create_superuser(self):
        # UserManager의 create_superuser 메서드를 테스트하기 위한 코드 기재
        # 관리자 권한을 가진 유저 모델을 생성
        admin_user = User.objects.create_superuser(**self.test_admin_user)

        # 어드민 유저 모델이 생성되었는지 카운트를 확인
        self.assertEqual(User.objects.filter(is_superuser=True, is_staff=True).count(), 1)
        self.assertEqual(admin_user.email, self.test_admin_user['email'])
        self.assertEqual(admin_user.nickname, self.test_admin_user['nickname'])
        self.assertTrue(admin_user.password, self.test_admin_user['password'])
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_active)

        # 프로필 이미지는 따로 넣지 않았기 때문에 디폴트 이미지인지 확인
        self.assertEqual(admin_user.profile_image.url, '/media/users/blank_profile_image.png')

class UserAPIViewTestCase(APITestCase):
    def setUp(self):
        # 테스트 코드를 작성하기 위해 필요한 것들을 미리 생성해두는 것
        self.test_data ={
            'nickname': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword1234'
        }

    def test_jwt_login(self):
        # JWT 로그인 API 테스트 코드 작성
        user = User.objects.create_user(**self.test_data)
        data = {
            'email': user.email,
            'password': 'testpassword1234'
        }

        response = self.client.post(reverse('jwt-login'), data)
        last_login = user.last_login
        user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertNotEqual(user.last_login, last_login)

    def test_jwt_verify(self):
        # JWT 검증(verify) API 테스트 코드 작성
        user = User.objects.create_user(**self.test_data)
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        response = self.client.post(
            path=reverse('token-verify'),
            data={'token': access}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_jwt_refresh(self):
        # JWT 갱신(refresh) API 테스트 코드 작성
        user = User.objects.create_user(**self.test_data)
        refresh = RefreshToken.for_user(user)

        response = self.client.post(
            path=reverse('token-refresh'),
            data={'refresh': str(refresh)}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_user_signup(self):
        # 회원가입 APIView 테스트를 위한 코드 작성
        response = self.client.post(reverse('user-signup'), data=self.test_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.data.get('nickname'), 'testuser')
        self.assertEqual(response.data.get('email'), 'test@example.com')


    def test_user_login(self):
        # 로그인 성공 시 APIView 테스트를 위한 코드 작성
        user = User.objects.create_user(**self.test_data)
        data = {
            'email': user.email,
            'password': 'testpassword1234'
        }
        response = self.client.post(reverse('user-login'), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data.get('message'), 'login successful.')

    def test_user_login_invalid_credentials(self):
        # 로그인 실패 시 APIView 테스트를 위한 코드 작성
        data = {
            'email': 'test@example.com',
            'password': 'worongpassword'
        }
        response = self.client.post(reverse('user-login'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_details(self):
        # 유저 정보를 가져오는 APIView 테스트를 위한 코드 작성
        user = User.objects.create_user(**self.test_data)
        self.client.login(email='test@example.com', password='testpassword1234')

        response = self.client.get(reverse('user-detail', kwargs={'pk': user.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('nickname'), 'testuser')
        self.assertEqual(response.data.get('email'), 'test@example.com')

    def test_update_user_details(self):
        # 유저 정보를 업데이트 하는 APIView 테스트를 위한 코드 작성
        user = User.objects.create_user(**self.test_data)
        self.client.login(email='test@example.com', password='testpassword1234')
        data = {
            'nickname': 'updateduser',
            'password': 'updatepw1234'
        }

        response = self.client.patch(reverse('user-detail', kwargs={'pk': user.id}), data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('nickname'), 'updateduser')
        # 요청으로 인한 변경사항을 db로 부터 가져옴
        user.refresh_from_db()
        self.assertTrue(check_password('updatepw1234', user.password))

    def test_delete_user(self):
        # 유저 회원 탈퇴(모델 삭제)를 진행하는 APIView 테스트를 위한 코드 작성
        user = User.objects.create_user(**self.test_data)
        self.client.login(email='test@example.com', password='testpassword1234')

        response = self.client.delete(reverse('user-detail', kwargs={'pk': user.id}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(email='test@example.com').exists())