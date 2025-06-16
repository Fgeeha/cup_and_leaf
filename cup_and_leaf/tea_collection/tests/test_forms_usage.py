from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from tea_collection.forms import TeaPostForm


class TeaPostFormUsageTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="u", password="p")

    def test_create_view_uses_form(self):
        self.client.login(username="u", password="p")
        response = self.client.get(reverse("tea_collection:tea_create"))
        self.assertIsInstance(response.context["form"], TeaPostForm)
