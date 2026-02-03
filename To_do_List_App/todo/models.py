from io import BytesIO
from pathlib import Path

from PIL import Image
from django.contrib.auth import get_user_model
from django.db import models
from utils.models import TimestampModel

User = get_user_model()

class Todo(TimestampModel):
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed_image = models.ImageField(upload_to='To_do_List_App/%Y/%m/%d', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='To_do_List_App/%Y/%m/%d/thumbnail', null=True, blank=True)

    def __str__(self):
        return self.title

    def get_thumbnail_image_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        elif self.completed_image:
            return self.completed_image.url
        return None

    def save(self, *args, **kwargs):
        if not self.completed_image: # 이미지가 비엇을때
            return super().save(*args, **kwargs)
        image = Image.open(self.completed_image) # pillow 라이브러리의 이용해 이미지 객체 만들기
        image.thumbnail((300,300)) # thumbnail 메서드를 사용하여 썸내일 이미지 만들기

        image_path = Path(self.completed_image.name) # Path 라이브러리를 사용하여 이미지의 경로 가져오기

        thumbnail_name = image_path.stem # 이미지 경로에서 기존 이미지의 이름 가져오기
        thumbnail_extension = image_path.suffix.lower() # 이미지의 확장자명 가져오기
        thumbnail_filename = f'{thumbnail_name}_thumb{thumbnail_extension}' # 이미지 경로 만들기

        if thumbnail_extension in ['.jpg', '.jpeg']: # 파일 타입 설정
            file_type = 'JPEG'
        elif thumbnail_extension == 'png':
            file_type = 'PNG'
        elif thumbnail_extension == 'gif':
            file_type = 'GIF'
        else:
            return super().save(*args, **kwargs)

        temp_thumb = BytesIO() # BytesIO 사용하여 이미지를 bytes 형태로 메모리에 저장할 임시 파일 객체 생성
        image.save(temp_thumb, file_type) # 이미지 데이터를 메모리 파일에 저장
        temp_thumb.seek(0) # 파일 포인터를 처음으로 되돌려서 읽을 수 있게 이동

        self.thumbnail.save(thumbnail_filename, temp_thumb, save=False) # todo에 이미지 저장
        temp_thumb.close() # 메모리 해제
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'To do List App'
        verbose_name_plural = 'To do List App List'

class Comment(TimestampModel):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='comments') # related_name 사용하면 호출시 comment_set -> comment만 해도 작동
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    message = models.TextField(max_length=200)

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = 'Comment App'
        verbose_name_plural = 'Comment App List'
        ordering = ('-created_at',)