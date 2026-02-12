from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from prompt_toolkit.validation import ValidationError
from rest_framework import serializers

User = get_user_model()

class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        user = User(**data)

        errors = dict()
        try:
            validate_password(password=data['password'], user=user)
        except ValidationError as e: # 커스텀 에러
            errors['password'] = list(e.message)

        if errors:
            raise serializers.ValidationError(errors)

        return super().validate(data)

    def create(self,validate_data): # createView에서 인스턴스 없을때 이 함수 호출
        user = User(**validate_data)

        user.set_password(validate_data['password'])

        user.save()

        return user