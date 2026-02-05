from django.contrib.auth import get_user_model
from django.db import models
from utils.models import TimestampModel

User = get_user_model()

class Post(TimestampModel):
    content = models.TextField('본문')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'[{self.user}] post' # User models 에서 __str__ 부분을 가져온다

    class Meta:
        verbose_name = '포스트'
        verbose_name_plural = '포스트 목록'

class PostImage(TimestampModel): # post로 PostImage 사용할때 Django가 자동으로 모델명을 소문자 +_set를 붙여서 인식한다 (post.postimage_set)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images') # related_name 안하면 사용할때 post.postimage_set 넣어야 한다 사용시 post.images
    image = models.ImageField('이미지', upload_to = 'post/%Y/%m/%d')

    def __str__(self):
        return f'{self.post} image' # Post __str__ 정보를 가져온다

    class Meta:
        verbose_name = '이미지'
        verbose_name_plural = '이미지 목록'

# post
    # 이미지(여거개)
    # 글
    # 작성자
    # 작성일자
    # 수정일자

# 태그
class Tag(TimestampModel):
    tag = models.CharField('태그', max_length=100)
    posts = models.ManyToManyField(Post, related_name='tags')

    def __str__(self):
        return self.tag
# ManyToManyField는
# class TagPosts(TimestampModel):
#     tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)

# 댓글
class Comment(TimestampModel):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    content = models.CharField('내용', max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post} | {self.user}'
