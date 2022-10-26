from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("posts.urls")),
    path("admin/", admin.site.urls),
    path("__debug__/", include('debug_toolbar.urls')),
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
]
