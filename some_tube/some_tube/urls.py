from django.contrib.flatpages import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("posts.urls")),
    path("admin/", admin.site.urls),
    path("__debug__/", include('debug_toolbar.urls')),
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path('about/', include('django.contrib.flatpages.urls')),
]

urlpatterns += [
        path('about-author/', views.flatpage, {'url': '/about-author/'}, name='about'),
        path('about-spec/', views.flatpage, {'url': '/about-spec/'}, name='spec'),
]
