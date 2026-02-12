from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
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

class ReviewAPIViewTestCase(APITestCase):
    def setUp(self):
        # 테스트 코드를 작성하기 위해 필요한 것들을 미리 생성해두는 것
        self.user = get_user_model().objects.create_user(
            nickname='testuser', email='test@example.com', password='password1234'
        )
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            description='Test Description',
            address='123 Test St',
            contact='Phone: 010-0000-0000'
        )
        self.data = {
            'user': self.user,
            'restaurant': self.restaurant,
            'title': 'Test Review Title',
            'comment': 'Tasty Yammy Yammy~'
        }

        self.client.login(email='test@example.com', password='password1234')

    def test_get_review_list(self):
        # 작성된 리뷰 리스트를 가져오기 위한 APIView 테스트를 위한 코드 작성
        self.review = Review.objects.create(**self.data)
        url = reverse('review-list', kwargs={'restaurant_id': self.restaurant.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get('results')), 1)
        self.assertEqual(response.data.get('results')[0].get('title'), self.review.title)
        self.assertEqual(response.data.get('results')[0].get('comment'), self.review.comment)
        self.assertEqual(response.data.get('results')[0].get('user'), self.review.user.id)
        self.assertEqual(response.data.get('results')[0].get('restaurant'), self.review.restaurant.id)

    def test_post_review(self):
        # 리뷰를 작성하면 데이터베이스에 저장되는 APIView 테스트를 위한 코드 작성
        url = reverse('review-list', kwargs={'restaurant_id': self.restaurant.id})

        response = self.client.post(url, self.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('title'),  self.data['title'])
        self.assertEqual(response.data.get('comment'), self.data['comment'])
        self.assertEqual(response.data.get('user'), self.data['user'].id)
        self.assertEqual(response.data.get('restaurant'), self.data['restaurant'].id)

    def test_get_review_detail(self):
        # 리뷰 상세 정보를 가져오기 위한 APIView 테스트를 위한 코드 작성
        self.review = Review.objects.create(**self.data)
        url = reverse('review-detail', kwargs={'review_id': self.review.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('title'), self.review.title)
        self.assertEqual(response.data.get('comment'), self.review.comment)
        self.assertEqual(response.data.get('user')['id'], self.review.user.id)
        self.assertEqual(response.data.get('restaurant')['id'], self.review.restaurant.id)

    def test_update_review(self):
        # 리뷰 제목, 내용을 업데이트하기 위한 APIView 테스트를 위한 코드 작성
        self.review = Review.objects.create(**self.data)
        url = reverse('review-detail', kwargs={'review_id': self.review.id})
        updated_data = {
            'title': 'Updated Review Title',
            'comment': 'Updated Tasty Yammy Yammy~'
        }

        response = self.client.put(url, updated_data)

        self.assertEqual(response.status_code, 200)
        self.review.refresh_from_db()
        self.assertEqual(self.review.title, updated_data['title'])
        self.assertEqual(self.review.comment, updated_data['comment'])

    def test_delete_review(self):
        # 리뷰를 삭제하는 APIView 테스트를 위한 코드 작성
        self.review = Review.objects.create(**self.data)
        url = reverse('review-detail', kwargs={'review_id': self.review.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())
        self.assertEqual(Review.objects.count(), 0)