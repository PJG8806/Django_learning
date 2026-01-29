from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Blog(models.Model):
    CATEGORY_CHOICES = (
        ('free', '자유'),
        ('travel', '여행'),
        ('cat', '고양이'),
        ('dog', '강아지'),
    )

    category = models.CharField('카테고리', max_length=10, choices=CATEGORY_CHOICES)
    title = models.CharField('제목', max_length=100)
    content = models.TextField('본문')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # models.CASCADE => 같이 삭제
    # models.PROTECT => 삭제 불가능함 (유저를 삭제할때 블로그가 있으면 유저 삭제 불가능)
    # models.SET_NULL => 널값을 넣는다 => 유저 삭제시 블로그의 author가 null이 됨
    created_at = models.DateTimeField('작성일자', auto_now_add=True)
    updated_at = models.DateTimeField('수정일자',auto_now_add=True)

    def __str__(self):
        return f'[{self.get_category_display()}] {self.title[:10]}' # choices 사용시 원하는 값 나오게 하기 위해서 get_(choices컬럼명)_display()

    class Meta:
        verbose_name = '블로그'
        verbose_name_plural = '블로그 목록'


# 제목
# 본문
# 작성자
# 작성일
# 수정일
# 카테고리