from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'nickname', 'email', 'password', 'is_staff', 'is_superuser']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        if password is None:
            raise serializers.ValidationError("Password is required.")
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'nickname', 'email', 'password', 'profile_image']
        READ_ONLY_FIELDS = ['id', 'email']

    def update(self, instance, validated_data):
        # 닉네임 업데이트
        instance.nickname = validated_data.get('nickname', instance.nickname)

        # 비밀번호 업데이트
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        instance.save()
        return instance


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), **attrs)
            if not user:
                raise serializers.ValidationError(
                    detail='Unable to log in with provided credentials.', code='authorization'
                )
        else:
            raise serializers.ValidationError(
                detail='Must be Required "email" and "password".', code='authorization'
            )

        attrs['user'] = user
        return attrs