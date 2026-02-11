from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from restaurants.models import Restaurant


class RestaurantModelTest(TestCase):
    def setUp(self): # 각 테스트 실행 전에 매번 실행됨
        # Restaurant 모델 테스트 시 필요한 세팅 기재
        self.test_restaurant_info = {
            'name': 'Test Restaurant',
            'description': 'Test description',
            'address': 'Test Address',
            'contact': 'Test Contact',
            'open_time': '10:00:00',
            'close_time': '22:00:00',
            'last_order': '21:00:00',
            'regular_holiday': 'SUM',
        }

    def test_create_restaurant(self):
        # objects의 create 메서드를 테스트하기 위한 코드 기재
        restaurant = Restaurant.objects.create(**self.test_restaurant_info) # dict를 unpack 하여 모델 인스턴스 생성

        self.assertEqual(Restaurant.objects.count(), 1) # DB에 데이터가 1개 생성되었는지 확인
        # 각 필드 값이 정상 저장되었는지 검증
        self.assertEqual(restaurant.name, self.test_restaurant_info['name'])
        self.assertEqual(restaurant.description, self.test_restaurant_info['description'])
        self.assertEqual(restaurant.address, self.test_restaurant_info['address'])
        self.assertEqual(restaurant.contact, self.test_restaurant_info['contact'])
        self.assertEqual(restaurant.open_time, self.test_restaurant_info['open_time'])
        self.assertEqual(restaurant.close_time, self.test_restaurant_info['close_time'])
        self.assertEqual(restaurant.last_order, self.test_restaurant_info['last_order'])
        self.assertEqual(restaurant.regular_holiday, self.test_restaurant_info['regular_holiday'])
        # __str__ 메서드가 name을 반환하는지 확인
        self.assertEqual(restaurant.__str__(), self.test_restaurant_info['name'])


class RestaurantViewTestCase(APITestCase): # DRF API 테스트 클래스
    def setUp(self): # 각 API 테스트 전에 실행
        # 테스트 코드를 작성하기 위해 필요한 것들을 미리 생성해두는 것
        self.restaurant_info = {
            "name": "Test Restaurant",
            "description": "Test Description",
            "address":  "Test Address",
            "contact": "Test Contact",
            "open_time": "10:00:00",
            "close_time": "22:00:00",
            "last_order": "21:00:00",
            "regular_holiday": "MON"
        }

    def test_restaurant_list_view(self):
        # url = reverse를 사용하고 url name은 'restaurant-list' 사용
        # get 메서드를 사용하여 restaurant list를 가져오는 것을 테스트하기 위한 코드를 작성
        url = reverse('restaurant-list') # router에서 자동 생성된 list URL 생성
        Restaurant.objects.create(**self.restaurant_info) # 테스트용 데이터 DB에 미리 생성

        response = self.client.get(url) # GET 요청 실행

        self.assertEqual(response.status_code, status.HTTP_200_OK) # HTTP 상태코드가 200인지 확인
        self.assertEqual(len(response.data), 1) # 반환된 리스트 길이가 1인지 확인
        # 반환된 데이터 필드값 검증
        self.assertEqual(response.data[0]['name'], self.restaurant_info['name'])
        self.assertEqual(response.data[0]['description'], self.restaurant_info['description'])
        self.assertEqual(response.data[0]['address'], self.restaurant_info['address'])
        self.assertEqual(response.data[0]['contact'], self.restaurant_info['contact'])
        self.assertEqual(response.data[0]['open_time'], self.restaurant_info['open_time'])
        self.assertEqual(response.data[0]['close_time'], self.restaurant_info['close_time'])
        self.assertEqual(response.data[0]['last_order'], self.restaurant_info['last_order'])
        self.assertEqual(response.data[0]['regular_holiday'], self.restaurant_info['regular_holiday'])

    def test_restaurant_post_view(self):
        # url = reverse를 사용하고 url name은 'restaurant-list' 사용
        # post 메서드를 사용하여 모델생성을 테스트 하기위한 코드를 작성
        url = reverse('restaurant-list') # list URL 사용 (POST는 list endpoint로 전송)
        response = self.client.post(url, self.restaurant_info, format='json')  # JSON 형식으로 POST 요청

        self.assertEqual(response.status_code, status.HTTP_201_CREATED) # 생성 성공 시 201 반환 확인
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(Restaurant.objects.first().name, self.restaurant_info['name'])

    def test_restaurant_detail_view(self):
        # url = reverse를 사용하고 url name은 'restaurant-detail' 사용
        # get 메서드를 사용하여 특정 restaurant 정보를 가져오는 것을 테스트 하기위한 코드를 작성
        restaurant = Restaurant.objects.create(**self.restaurant_info)
        url = reverse('restaurant-detail', kwargs={'pk': restaurant.id}) # 특정 pk에 해당하는 detail URL 생성

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), self.restaurant_info['name'])

    def test_restaurant_update_view(self):
        # url = reverse를 사용하고 url name은 'restaurant-detail' 사용
        # post 메서드를 사용하여 restaurant 정보를 업데이트하는 것을 테스트 하기위한 코드를 작성
        restaurant = Restaurant.objects.create(**self.restaurant_info) # 기존 데이터 생성
        url = reverse('restaurant-detail', kwargs={'pk': restaurant.id}) # detail URL 생성
        updated_restaurant_info = {
            "name": "Updated Restaurant",
            "description": "Updated Description",
            "address":  "Updated Address",
            "contact": "Updated Contact",
            "open_time": "11:00:00",
            "close_time": "23:00:00",
            "last_order": "22:00:00",
            "regular_holiday": "TUE"
        }

        response = self.client.put(url, updated_restaurant_info, format='json') # PUT 요청으로 전체 수정

        self.assertEqual(response.status_code, status.HTTP_200_OK) # 수정 성공 시 200 확인
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(response.data.get('name'), updated_restaurant_info['name'])
        self.assertEqual(response.data.get('description'), updated_restaurant_info['description'])
        self.assertEqual(response.data.get('address'), updated_restaurant_info['address'])
        self.assertEqual(response.data.get('contact'), updated_restaurant_info['contact'])
        self.assertEqual(response.data.get('open_time'), updated_restaurant_info['open_time'])
        self.assertEqual(response.data.get('close_time'), updated_restaurant_info['close_time'])
        self.assertEqual(response.data.get('last_order'), updated_restaurant_info['last_order'])
        self.assertEqual(response.data.get('regular_holiday'), updated_restaurant_info['regular_holiday'])

    def test_restaurant_delete_view(self):
        # url = reverse를 사용하고 url name은 'restaurant-detail' 사용
        # post 메서드를 사용하여 모델삭제를 테스트하기 위한 코드를 작성
        restaurant = Restaurant.objects.create(**self.restaurant_info)
        url = reverse('restaurant-detail', kwargs={'pk': restaurant.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Restaurant.objects.count(), 0) # DB에서 실제 삭제되었는지 확인