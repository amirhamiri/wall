from django.urls import resolve, reverse
from rest_framework.test import APITestCase
from ads import views
from ads.models import Ad


class TestUrls(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.ad = Ad.objects.create(title='Iphone', caption='Nice')


    def test_ad_list_url(self):
        url = reverse('ads:ad_list')
        self.assertEqual(resolve(url).func.view_class, views.AdListView)

    def test_ad_create_url(self):
        url = reverse('ads:ad_create')
        self.assertEqual(resolve(url).func.view_class, views.AdCreateView)

    def test_ad_detail_url(self):
        url = reverse('ads:ad_detail', args=(self.ad.id,))
        self.assertEqual(resolve(url).func.view_class, views.AdDetailView)