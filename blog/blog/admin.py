from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from blog.models import Blog, Comment

admin.site.register(Comment)

class CommentInline(admin.TabularInline):
    model = Comment
    fields = ['content', 'author']
    extra = 1 # 댓글 입력 창에 하나씩 보이게

@admin.register(Blog)
class BlogAdmin(SummernoteModelAdmin):
    summernote_fields = ['content',]
    inlines = [
        CommentInline, # 댓글을 사용하게 해주는 부분
    ]
