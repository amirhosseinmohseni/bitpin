from django.urls import path
from .views import (
    RegisterUserView,
    UserLoginView
)

urlpatterns = [
    path("users/register_user/", RegisterUserView.as_view(), name="register_user"),
    path("users/login_user/", UserLoginView.as_view(), name="login_user"),
] 