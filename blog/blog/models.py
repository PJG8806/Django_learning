from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from utils.models import TimestampModel

User = get_user_model()

class Blog(TimestampModel): # 공통적인 부분은 별도로 models 만드는 것처럼 만들어서 사용 가능
    CATEGORY_CHOICES = (
        ('free', '자유'),
        ('travel', '여행'),
        ('cat', '고양이'),
        ('dog', '강아지'),
    )

    category = models.CharField('카테고리', max_length=10, choices=CATEGORY_CHOICES, default='free')
    title = models.CharField('제목', max_length=100)
    content = models.TextField('본문')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # models.CASCADE => 같이 삭제
    # models.PROTECT => 삭제 불가능함 (유저를 삭제할때 블로그가 있으면 유저 삭제 불가능)
    # models.SET_NULL => 널값을 넣는다 => 유저 삭제시 블로그의 author가 null이 됨


    def __str__(self):
        return f'[{self.get_category_display()}] {self.title[:10]}' # choices 사용시 원하는 값 나오게 하기 위해서 get_(choices컬럼명)_display()

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'blog_pk': self.objects.pk})

    class Meta:
        verbose_name = '블로그'
        verbose_name_plural = '블로그 목록'

    # category update
    # Blog.objects.filter(category='').update(category='free')

# 제목
# 본문
# 작성자
# 작성일
# 수정일
# 카테고리

class Comment(TimestampModel):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    content = models.CharField('본문', max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.blog.title} 댓글'
    
    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글 목록'
        ordering = ('-created_at', '-id') # 데이터 출력 정렬 방식
    # blog
    # 댓글 내용
    # 작성자
    # 작성일자
    # 수정일자