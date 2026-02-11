from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission): # DRF 권한 클래스로 요처을 허용할지 말지 역할
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS: # 읽기 전용 요청 전부 허용(GET, HEAD, OPTIONS)
            return True

        try: # API 사용시
            obj = view.get_object(request, *view.args, **view.kwargs) # 요청이 가리키는 실제 객체 가져온다 # get_object -> views/api_views get_object 의미
        except TypeError:
            obj = view.get_object() # 제네리얼 사용시 사용
        return obj.author == request.user # 현재 유저와 객체간의 유저가 같으면 True 아니면 Fals