from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class LogoutViewTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="u", password="p")

    def test_logout_via_get(self):
        self.client.login(username="u", password="p")
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("tea_collection:index"))
        self.assertNotIn("_auth_user_id", self.client.session)
