from io import BytesIO
from pathlib import Path

from PIL import Image
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

    image = models.ImageField('이미지', null=True, blank=True, upload_to='blog/%Y/%m/%d')
    thumbnail = models.ImageField('썸네일', null=True, blank=True, upload_to='blog/%Y/%m/%d/thumbnail')
    # models.CASCADE => 같이 삭제
    # models.PROTECT => 삭제 불가능함 (유저를 삭제할때 블로그가 있으면 유저 삭제 불가능)
    # models.SET_NULL => 널값을 넣는다 => 유저 삭제시 블로그의 author가 null이 됨


    def __str__(self):
        return f'[{self.get_category_display()}] {self.title[:10]}' # choices 사용시 원하는 값 나오게 하기 위해서 get_(choices컬럼명)_display()

    def get_absolute_url(self): # success_url이 없어도 가능하게 설정
        return reverse('blog:detail', kwargs={'blog_pk': self.pk})

    def get_thumbnail_image_url(self): # 이 함수를 만들면 html에서 blog.thumbnail.url 아니라 blog.get_thumbnail_image_url 만으로 호출 가능함
        if self.thumbnail:
            return self.thumbnail.url
        elif self.image:
            return self.image.url
        return None

    def save(self, *args, **kwargs): # 이미지 썸내일 저장 및 db 저장(용량을 줄이는 방법)
        if not self.image:
            return super().save(*args, **kwargs)
        image = Image.open(self.image)
        image.thumbnail((300,300))
        
        image_path = Path(self.image.name)

        thumbnail_name = image_path.stem # /blog/2024/4/23/database.png => database
        thumbnail_extension = image_path.suffix.lower() # /blog/2024/4'23'database.png => .png
        thumbnail_filename = f'{thumbnail_name}_thumb{thumbnail_extension}' # database_thumb.png 원본 이름으로 저장

        if thumbnail_extension in ['.jpg', 'jpeg']:
            file_type = 'JPEG'
        elif thumbnail_extension == '.gif':
            file_type = 'GIF'
        elif thumbnail_extension == '.png':
            file_type = 'PNG'
        else:
            return super().save(*args, **kwargs)

        temp_thumb = BytesIO()
        image.save(temp_thumb, file_type)
        temp_thumb.seek(0)

        self.thumbnail.save(thumbnail_filename, temp_thumb, save=False)
        temp_thumb.close()
        return super().save(*args, **kwargs)

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

    # 자료형 정보
    # 텍스트
    # CharField: 짧은 글 / 길이 제한 O
    # TextField: 긴글 / 길이 제한 X
    # URLField: URL 저장 / CharField
    # SlugField: Slug저장 / CharField / 잘 안씀
    # UUIDField: UUID 저장 / 잘 안씀

    # 파일
    # EmaiField: 이메일을 저장
    # FileField: 파일 저장
    # ImageField: 이미지 저장

    # 숫자
    # IntegerField: 숫자 필드
    # PositiveIntegerField: 양수만 가능함
    # BigIntegerField: 큰 숫자 필드
    # PositiveBigIntegerField: 양수만 가능한 큰 숫자
    # DecimalField: Decimal 저장
    # Float => 부동(떠서 움직일 부) 수수점 조금 부정확하지만 큰 수
    # Decimal => 고정 소수점 정확하지만 상대적으로 작은 수

    # 날짜 시간
    # DateTimeField: 날짜 및 시간을 저장
    # DateField: 날짜만 저장
    # TimeField: 시간만 저장

    # 연결
    # Foreignkey: 1:N관계 / 내가 N
    # ManyToManyField: N:N관계
    # OneToOneField: 1:1관계

    # 기타
    # JSONField: JSON형태의 데이터를 저장

    # DB 설계를 잘하는 법
    # 제일 중요한 것은 중복된 데이터를 많이 적지 않습니다
    # Join을 과하게 많이하지 않습니다