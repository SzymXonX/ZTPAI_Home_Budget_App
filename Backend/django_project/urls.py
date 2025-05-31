from django.contrib import admin
from django.urls import path, include
from myapp.views import CreateUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.conf import settings
from django.conf.urls.static import static

from myapp.views import UserInfoView, ChangePasswordView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/user/register/", CreateUserView.as_view(), name="register"),
    path("api/token/", TokenObtainPairView.as_view(), name="get_token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("api-auth/", include("rest_framework.urls")),
    path("api/user-info/", UserInfoView.as_view(), name="user_info"),
    path("api/user/change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("api/", include("myapp.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)