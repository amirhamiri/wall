from accounts import views
from django.urls import resolve, reverse
from rest_framework.test import APISimpleTestCase
from rest_framework_simplejwt.views import TokenObtainPairView

class TestUrls(APISimpleTestCase):
    def test_login(self):
        url = reverse('accounts:login')
        self.assertEqual(resolve(url).func.view_class, TokenObtainPairView)

    def test_profile_detail(self):
        url = reverse('accounts:profile_view')
        self.assertEqual(resolve(url).func.view_class, views.UserView)

