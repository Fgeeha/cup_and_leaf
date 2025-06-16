from django.urls import path

from . import views

app_name = "tea_collection"

urlpatterns = [
    path("", views.TeaPostListView.as_view(), name="index"),
    path("tea/", views.TeaPostListView.as_view(), name="tea_post_list"),
    path("tea/<int:pk>/", views.TeaPostDetailView.as_view(), name="tea_detail"),
    path("tea/new/", views.TeaPostCreateView.as_view(), name="tea_create"),
    path("tea/<int:pk>/edit/", views.TeaPostUpdateView.as_view(), name="tea_update"),
    path("tea/<int:pk>/delete/", views.TeaPostDeleteView.as_view(), name="tea_delete"),
    path("tea/<int:pk>/comment/", views.add_comment, name="add_comment"),
    path(
        "tea/<int:pk>/comment/<int:comment_pk>/edit/",
        views.edit_comment,
        name="edit_comment",
    ),
    path(
        "tea/<int:pk>/comment/<int:comment_pk>/delete/",
        views.delete_comment,
        name="delete_comment",
    ),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("register/", views.register, name="register"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("search/", views.search_tea, name="search_tea"),
]
