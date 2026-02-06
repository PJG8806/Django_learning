from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

from utils.models import TimestampModel


# 커스텀 user 만들기

class UserManger(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError('올바른 이메일을 입력하세요.')

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_active = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password): # super() 할때 사용
        user = self.create_user(email, password)
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)

# 커스텀 user 만들면 위에 메니저 및 만들고  settings 제일 하단 경로 넣는 부분에 AUTH_USER_MODEL = 커스텀 user 위치 추가를 해야 한다
class User(AbstractBaseUser): # password, last_login 지원, user은 여러가지 기능이 있어서 따로 만들어줘야 한다
    email = models.EmailField(
        verbose_name = 'email',
        unique = True
    )
    is_active = models.BooleanField(default = False) # 활성화가 되어 있으면 로그인이 안된다
    is_admin = models.BooleanField(default = False)
    nickname = models.CharField('nickname', max_length=20, unique=True)
    # 나를 팔로우 하는 사람이 팔로워
    # 내가 팔로우 하는 사람이 팔로잉
    # User N:N User

    # 서로 친구가 되면 a <==> b symmetrical = True
    # 한쪽만 친구가 되면 a => b symmetrical = False
    following = models.ManyToManyField(
        'self', symmetrical=False, related_name='followers',
        through='UserFollowing', through_fields=('from_user', 'to_user') # 두 테이블 참조할때 사용 하며 (내가 첫번째, 참조 하는거)
        # 가져올 클래스가 밑에 있으면 못가져 오지만 그럴 경우 텍스트로 만들면 해결된다
    )
    # 유저가 유저를 가지고 있어야 해서 본인이 본인 상속은 안되어서 User을 사용 못하고 'self'를 사용


    objects = UserManger()
    # 매니저는 User.objects.all()에서 objects가 매니저
    USERNAME_FIELD = 'email' # 이 설정으로 유저이름이 이메일 형식으로 된다 계정 만들때 이메일로 유저 네임 대신
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = '유저'
        verbose_name_plural = f'{verbose_name} 목록'

    def get_full_name(self): # 영어 이름 성 이름 합쳐주는 부분 지금은 없으니 닉네임으로
        return self.nickname

    def get_short_name(self):
        return self.nickname

    def __str__(self):
        return self.nickname

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @property # 클래스 변수철 사용 가능하게 하는 함수
    def is_superuser(self):
        return self.is_admin
    # user.is_superuser() -> user.is_superuser 이렇게 사용 가능하게

class UserFollowing(TimestampModel): # 중계 테이블
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_followers') # 팔로워 할 상대 정보
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_following') # 현재 로그인된 유저

    class Meta: # 두가지 필드를 하나로 묶어서 중복 막기
        unique_together = ('to_user', 'from_user')
        # to_user 1, from_user 2
        # to_user 1, from_user 3
        # to_user 1, from_user 2 => 오류