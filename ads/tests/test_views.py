import io
import json
from PIL import Image
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from ads.models import Ad


class TestAdListView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.username = 'amir'
        cls.password = 'test1234'
        cls.user = User.objects.create_user(username='amir', password='test1234')
        cls.ad = Ad.objects.create(title='Iphone', caption='Nice')
        refresh = RefreshToken.for_user(cls.user)
        cls.token = str(refresh.access_token)

    def test_get_ads_list(self):
        url = reverse('ads:ad_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestAdDetailView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.username = 'amir'
        cls.password = 'test1234'
        cls.user = User.objects.create_user(username='amir', password='test1234')
        cls.ad = Ad.objects.create(title='Iphone', caption='Nice')
        refresh = RefreshToken.for_user(cls.user)
        cls.token = str(refresh.access_token)

    def test_get_ad_detail_authorized(self):
        url = reverse('ads:ad_detail', args=(self.ad.id,))
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.ad.title)

    def test_get_ad_detail_unauthorized(self):
        url = reverse('ads:ad_detail', args=(self.ad.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_ad_authorized(self):
        url = reverse('ads:ad_detail', args=(self.ad.id,))
        new_data = {
            'title': 'Fan',
            'caption': 'Nice'
        }
        response = self.client.put(url, data=new_data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], new_data['title'])

    def test_update_ad_unauthorized(self):
        url = reverse('ads:ad_detail', args=(self.ad.id,))
        new_data = {'title': 'Mic'}
        response = self.client.get(url, data=new_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_ad_authorized(self):
        url = reverse('ads:ad_detail', args=(self.ad.id,))
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_ad_unauthorized(self):
        url = reverse('ads:ad_detail', args=(self.ad.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestAdCreateView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.username = 'amir'
        cls.password = 'test1234'
        cls.user = User.objects.create_user(username='amir', password='test1234')
        cls.ad = Ad.objects.create(title='Iphone', caption='Nice')
        refresh = RefreshToken.for_user(cls.user)
        cls.token = str(refresh.access_token)

    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def test_create_ad_with_image_authorized(self):
        url = reverse('ads:ad_create')
        image_file = self.generate_photo_file()
        new_data = {
            'title': 'Fan',
            'caption': 'Nice',
            'image': image_file
        }
        response = self.client.post(url, data=new_data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], new_data['title'])

    def test_create_ad_without_image_authorized(self):
        url = reverse('ads:ad_create')
        image_file = self.generate_photo_file()
        new_data = {
            'title': 'Fan',
            'caption': 'Nice',
        }
        response = self.client.post(url, data=new_data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], new_data['title'])

    def test_create_ad_without_image_unauthorized(self):
        url = reverse('ads:ad_create')
        image_file = self.generate_photo_file()
        new_data = {
            'title': 'Fan',
            'caption': 'Nice',
        }
        response = self.client.post(url, data=new_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
