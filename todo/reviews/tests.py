from django.contrib.auth import get_user_model
from django.test import TestCase

from restaurants.models import Restaurant
from reviews.models import Review


class ReviewModelTest(TestCase):
    def setUp(self):
        # Review 모델 테스트 시 필요한 세팅 기재
        self.user = get_user_model().objects.create_user(
            nickname='testuser',
            email='test@example.com',
            password='password1234'
        )
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            description='Test description',
            address='Test address',
            contact='Test contact',
        )
        self.data={
            'user': self.user,
            'restaurant': self.restaurant,
            'title': 'Test Review Title',
            'comment': 'Test'
        }

    def test_create_review(self):
        # objects의 create 메서드를 테스트하기 위한 코드 기재
        review = Review.objects.create(**self.data)

        self.assertEqual(review.title, self.data['title'])
        self.assertEqual(review.comment, self.data['comment'])
        self.assertEqual(review.user, self.data['user'])
        self.assertEqual(review.restaurant, self.data['restaurant'])
