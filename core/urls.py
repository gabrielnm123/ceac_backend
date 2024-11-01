from django.contrib import admin
from django.urls import path, include
from .views import (
    UserViewSet,
    GroupViewSet,
    PermissionViewSet,
    ContentTypeViewSet,
    get_current_user,
    check_password,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    logout_view,
)
from capacita.views import FichaViewSet, ModulosCapacitaViewSet, download_ficha_view
from rest_framework import routers
from django.views.generic import RedirectView

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"groups", GroupViewSet)
router.register(r"permissions", PermissionViewSet)
router.register(r"contenttypes", ContentTypeViewSet)
router.register(r"capacita/fichas", FichaViewSet)
router.register(r"capacita/modulos_capacita", ModulosCapacitaViewSet)

urlpatterns = [
    path("", RedirectView.as_view(url="/admin/")),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/current_user/", get_current_user, name="current_user"),
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("api/logout/", logout_view, name="logout"),
    path(
        "api/users/<int:user_id>/check-password/", check_password, name="check_password"
    ),
    path(
        "api/capacita/fichas/<int:ficha_id>/download/",
        download_ficha_view,
        name="download_ficha",
    ),
]
