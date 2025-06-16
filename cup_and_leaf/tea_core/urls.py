from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from tea_collection.views import CustomLoginView, logout_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/logout/", logout_view, name="logout"),
    path("auth/login/", CustomLoginView.as_view(), name="login"),
    path("", include("tea_collection.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("pages/", include("pages.urls")),
    path("account/", include("account.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "pages.views.page_not_found"
handler500 = "pages.views.server_error"
