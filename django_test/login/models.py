from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '블로거'
        verbose_name_plural = f'{verbose_name}목록'