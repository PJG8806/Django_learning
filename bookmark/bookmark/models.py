from django.db import models

# Create your models here.

class Bookmark(models.Model):
    name = models.CharField('이름', max_length=100)
    url = models.URLField('URL')
    create_at = models.DateTimeField('생성일시',auto_now_add=True)
    update_at = models.DateTimeField('수정일시', auto_now=True)


    def __str__(self):
        return self.name # 추가시 이름이 제대로 보이게 된다

    class Meta:
        verbose_name = '북마크'
        verbose_name_plural = '북마크 목록'

# makemigrations => migration.py 파일 만들기
# 실제 DB에는 영향 X => 실제 DB에 넣기위한 정의를 하는 파일 생성

# migrate => migrations/ 폴더 안에 있는 migration 파일들을 실제 DB에 적용을 한다

# makemigrations => 깃의 commit => github에 적용 X, 커밋 기록 => DB에 적용 X, 적용할 파일 생성
# migrate => 깃의 push => github에 적용 O, 로컬 커밋 기록 => DB 적용 O, migrations 파일들 가지고 적용