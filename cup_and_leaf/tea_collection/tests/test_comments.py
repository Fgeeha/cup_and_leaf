from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from tea_collection.models import TeaPost, TeaComment


class CommentViewTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="user", password="pass")
        self.post = TeaPost.objects.create(
            title="Test Tea",
            type="green",
            origin="china",
            production_year=2021,
            tea_grade="first",
            appearance="leaves",
            description="good",
            author=self.user,
        )
        self.comment = TeaComment.objects.create(
            text="old comment",
            tea_post=self.post,
            author=self.user,
        )

    def test_edit_comment(self):
        self.client.login(username="user", password="pass")
        url = reverse(
            "tea_collection:edit_comment", args=[self.post.pk, self.comment.pk]
        )
        response = self.client.post(url, {"text": "new", "rating": 5})
        self.assertRedirects(
            response, reverse("tea_collection:tea_detail", args=[self.post.pk])
        )
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.text, "new")
        self.assertEqual(self.comment.rating, 5)

    def test_delete_comment(self):
        self.client.login(username="user", password="pass")
        url = reverse(
            "tea_collection:delete_comment", args=[self.post.pk, self.comment.pk]
        )
        response = self.client.get(url)
        self.assertRedirects(
            response, reverse("tea_collection:tea_detail", args=[self.post.pk])
        )
        self.assertFalse(TeaComment.objects.filter(pk=self.comment.pk).exists())
