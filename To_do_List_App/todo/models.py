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

    def __str__(self):
        return self.title

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