from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from user.serializers import SignUpSerializer, UsernameSerializer


class SignUpAPIView(CreateAPIView): # CreateAPIView 만 사용시 password 해쉬가 안되지만 serializers 에서 create추가시 해쉬화 가능
    serializer_class = SignUpSerializer

    # 이렇게 추가 하면 입력은 기존 시리얼라이저, 결과 에 새로운 시리얼라이저(페스워드 없앤부분)가 출력된다
    @swagger_auto_schema(request_body=SignUpSerializer, responses={201: UsernameSerializer(many=False)})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def create(self, request, *args, **kwargs): # 별도로 수정할꺼 아니면 이 함수를 여기 안만들어도 되지 않을까?
        # 회원가입시 토큰을 리턴하는 방식으로 커스텀 다만 시리얼 라이저로 한 토큰 추가 부분은 적용이 안된 토큰 출력
        # 별도의 설정 필요 하지만 비추천 하고 유저에서 다시 토큰을 하는 방식이 좋다
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # refresh = RefreshToken.for_user(serializer.instance)
        #
        # response_data = {
        #     'refresh': str(refresh),
        # 'access': str(refresh.access_token),
        # }

        # return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)