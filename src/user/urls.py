from django.urls import path
from .views import (
    UserRegisterView,
    UserLoginView,
    UserListView,
    UserDetailView,
    RefreshTokenView,
)


urlpatterns = [
    path("user/register/", UserRegisterView.as_view(), name="user-register"),
    path("user/login/", UserLoginView.as_view(), name="user-login"),
    path("user/", UserListView.as_view(), name="user-list"),
    path("user/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("user/refresh-token/", RefreshTokenView.as_view(), name="refresh-token"),
]
