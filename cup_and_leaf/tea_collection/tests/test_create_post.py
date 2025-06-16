from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from tea_collection.models import TeaPost


class TeaPostCreateTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="creator", password="pass")

    def test_create_post(self):
        self.client.login(username="creator", password="pass")
        url = reverse("tea_collection:tea_create")
        data = {
            "title": "New Tea",
            "type": "green",
            "origin": "china",
            "production_year": 2024,
            "tea_grade": "first",
            "appearance": "leaves",
            "description": "tasty",
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("tea_collection:index"))
        self.assertTrue(TeaPost.objects.filter(title="New Tea").exists())
