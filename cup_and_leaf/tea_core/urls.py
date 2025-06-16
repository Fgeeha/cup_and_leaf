from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("tea_collection.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("pages/", include("pages.urls")),
    path("account/", include("account.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "pages.views.page_not_found"
handler500 = "pages.views.server_error"
