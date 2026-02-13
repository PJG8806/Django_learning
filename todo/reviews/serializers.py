from rest_framework import serializers
from reviews.models import Review
from users.serializers import UserDetailSerializer

# Review Create, List APIView에 대한 serializer
class ReviewSerializer(serializers.ModelSerializer):
    # 리뷰 제목, 텍스트와 함께 작성자의 정보, 레스토랑의 정보를 함께 보냄
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"
        # user, restaurant 필드는 serializer.save()의 인자로 전달할 것이기 때문에 읽기 전용 필드로 설정
        read_only_fields = ("id", "restaurant")

# Review Update, Retrieve APIView에 사용할 serializer
class ReviewDetailSerializer(serializers.ModelSerializer):
    # 리뷰 제목, 텍스트와 함께 작성자의 정보, 레스토랑의 정보를 함께 보냄
    user = UserDetailSerializer(read_only=True)
    restaurant = ReviewSerializer(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"
