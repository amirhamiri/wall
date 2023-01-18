import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.otp_service import OTP
from rest_framework.test import APITestCase
from django.core.cache import cache
from accounts import views

class TestUserView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.phone = '12345678901'
        cls.username = 'amir'
        cls.password = 'test1234'
        cls.user = User.objects.create_user(phone='12345678901', username='amir', password='test1234')
        refresh = RefreshToken.for_user(cls.user)
        cls.token = str(refresh.access_token)

    def test_profile_detail_authorized(self):
        url = reverse('accounts:profile_view')
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['username'])
        self.assertEqual(json.loads(response.content), {'username': 'amir'})

    def test_profile_detail_unauthorized(self):
        url = reverse('accounts:profile_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_profile_update_authorized(self):
        url = reverse('accounts:profile_view')
        data = {
            'username': 'Karim'
        }
        response = self.client.put(url, data=data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_update_unauthorized(self):
        url = reverse('accounts:profile_view')
        data = {
            'username': 'Karim'
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login(self):
        url = reverse('accounts:login')
        data = {
            'phone': self.phone,
            'password': self.password
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.failUnless(response.data['access'])



class UserRegisterViewTest(APITestCase):
    def setUp(self):
        self.valid_payload = {
            'phone': '12345678901',
            'username': 'test_user',
            'password': 'test_password'
        }
        self.invalid_payload = {
            'phone': '',
            'username': '',
            'password': ''
        }

    def test_register_valid_payload(self):
        url = reverse('accounts:register')
        request = self.client.post(url, data=self.valid_payload)
        self.assertEqual(request.status_code, 202)
        self.assertEqual(cache.get(key='register')['phone'], '12345678901')
        self.assertEqual(request.data, {'phone': '12345678901', 'result': 'otp sended'})

    def test_register_invalid_payload(self):
        url = reverse('accounts:register')
        request = self.client.post(url, data=self.invalid_payload)
        self.assertEqual(request.status_code, 406)



class CheckOtpCodeViewTest(APITestCase):
    def setUp(self):
        self.valid_payload = {
            'code': '123456',
        }
        self.invalid_payload = {
            'code': '',
        }
        self.valid_otp = OTP().generate_otp('12345678901')
        self.user_data = {
            'phone': '12345678901', 
            'password': 'test_password', 
            'username': 'test_user'
        }
        cache.set(key='register', value=self.user_data, timeout=300)

    def test_check_otp_code_valid_payload_and_valid_otp(self):
        url = reverse('accounts:check-otp')
        response = self.client.post(url, data={'code': self.valid_otp})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.filter(phone=self.user_data['phone']).exists(), True)

    def test_check_otp_code_valid_payload_and_invalid_otp(self):
        url = reverse('accounts:check-otp')
        response = self.client.post(url, data={'code': 1000})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {'error': 'this code not exist or invalid'})

    def test_check_otp_code_invalid_payload(self):
        url = reverse('accounts:check-otp')
        response = self.client.post(url, data=self.invalid_payload)

        self.assertEqual(response.status_code, 406)

    def test_check_otp_code_cache_not_exist(self):
        url = reverse('accounts:check-otp')
        cache.delete(key='register')
        response = self.client.post(url, data={'code': self.valid_otp})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {'error': 'this code not exist or invalid'})