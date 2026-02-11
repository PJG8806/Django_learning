from django.contrib.auth import get_user_model
from django.test import TestCase

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