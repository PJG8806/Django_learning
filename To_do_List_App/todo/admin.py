from django.contrib import admin
from .models import Todo, Comment


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0
    fields = ('message', 'user')

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    # 목록 화면에 보여줄 컬럼
    list_display = ("title", "description", "is_completed", "start_date", "end_date")
    # 오른쪽 사이트 필터
    list_filter = ("is_completed",)
    # 상단 검색창 검색 기준
    search_fields = ("title",)
    # 기본 정렬 순서 (최신순 정렬)
    ordering = ("-start_date",)
    # 상세 페이지 레이아웃
    fieldsets = (
        ("Todo Info", {"fields": ("title", "description", "is_completed")}),
        ("Date Info", {"fields": ("start_date", "end_date")}),
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'todo', 'user', 'message', 'created_at')
    list_filter = ('todo', 'user')
    search_fields = ('message', 'user')
    ordering = ('-created_at',)
    list_editable = ('message',)
    fieldsets = (
    ('Comment Info',{
        'fields': ('todo', 'user', 'message',)
    }),
    )