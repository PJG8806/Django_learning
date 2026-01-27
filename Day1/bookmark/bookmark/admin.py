from django.contrib import admin

from bookmark.models import Bookmark
@admin.register(Bookmark) # -> admin.site.register 같은 효과를 준다
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'url'] # 출력 컬럼 추가
    list_display_links = ['name', 'url'] # 클릭 효과 적용 컬럼명
    list_filter = ['name','url'] # 필터 효과를 추가한다

# admin.site.register(Bookmark, BookmarkAdmin) # DB모델 및 설정 추가

# admin 처음 접속할때 계정을 만들어야 하며 python manage.py createsuperuser로 만든다