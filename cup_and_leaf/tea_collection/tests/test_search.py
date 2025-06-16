from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from tea_collection.models import TeaPost


class SearchTeaViewTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="user", password="pass")

        TeaPost.objects.create(
            title="Green Tea",
            type="green",
            origin="china",
            production_year=2021,
            tea_grade="first",
            appearance="long leaves",
            description="Delicious green tea",
            author=self.user,
        )
        TeaPost.objects.create(
            title="Black Tea",
            type="black",
            origin="india",
            production_year=2022,
            tea_grade="second",
            appearance="dark leaves",
            description="Strong black tea",
            author=self.user,
        )

    def test_search_by_query(self):
        url = reverse("tea_collection:search_tea")
        response = self.client.get(url, {"query": "Delicious"})
        self.assertEqual(response.status_code, 200)
        object_list = response.context["page_obj"].object_list
        titles = {obj.title for obj in object_list}
        self.assertIn("Green Tea", titles)
        self.assertNotIn("Black Tea", titles)
