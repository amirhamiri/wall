from rest_framework.test import APITestCase
from django.utils.translation import gettext_lazy as _
from ads.models import Ad
from accounts.models import User


class AuthorModelTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='Pedi')
        cls.ad = Ad.objects.create(title='Iphone', caption='nice', publisher=cls.user)

    def test_title_label(self):
        field_label = self.ad._meta.get_field('title').verbose_name
        self.assertEqual(field_label, _('title'))

    def test_caption_label(self):
        field_label = self.ad._meta.get_field('caption').verbose_name
        self.assertEqual(field_label, _('caption'))

    def test_image_label(self):
        field_label = self.ad._meta.get_field('image').verbose_name
        self.assertEqual(field_label, _('image'))

    def test_str_method(self):
        expected_result = self.ad.title
        self.assertEqual(self.ad.__str__(), expected_result)
