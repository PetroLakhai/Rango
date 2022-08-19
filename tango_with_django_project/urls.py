"""tango_with_django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path, reverse_lazy

from rango import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("rango/", include("rango.urls")),
    path("training/", views.TrainingView.as_view(), name="training"),
    # The above maps any URLs starting with rango/ to be handled by rango.
    path("admin/", admin.site.urls),
    path("accounts/", include("registration.backends.simple.urls")),
    path(
        "accounts/password/change/",
        auth_views.PasswordChangeView.as_view(
            success_url=reverse_lazy("auth_password_change_done")
        ),
        name="auth_password_change",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
