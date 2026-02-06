import re

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE) # related_name 설정으로 Jinja 에서 post.comment_set를 post.comments로
    content = models.CharField('내용', max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'[comment]{self.post} | {self.user}'

class Like(TimestampModel):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)

    def __str__(self):
        return f'[like]{self.post} | {self.user}'

@receiver(post_save, sender=Post) # post_save 세이브 한후, pre_save 세이브하기 전
def post_post_save(sender, instance, created, **kwargs):
    hashtags = re.findall(r'#(\w{1,100})(?=\s|$)', instance.content)
    # 본문에 들어가야 하는 내용이 이렇다 설정(#으로 시작하고 텍스트가 1~100 까지 뒤에 공백이 끝)

    instance.tags.clear() # 연결된 태그 모델을 삭제한다

    if hashtags:
        tags = [
            Tag.objects.get_or_create(tag=hashtag) # 태그가 있으나 없으나 만들어 준다
            for hashtag in hashtags
        ]

        tags = [tag for tag, _ in tags] # 태그만 객체만 추출 (안쓰는 변수는 _ 처리)

        instance.tags.add(*tags)
        # tags = [ # 이런 방식으로 들어간다
        #     [Tag, False],
        #     [Tag, True],
        # ]