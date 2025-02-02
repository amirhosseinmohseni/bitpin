from django.urls import path
from .views import (
    RegisterUserView,
    UserLoginView
)

urlpatterns = [
    path("register_user/", RegisterUserView.as_view(), name="register_user"),
    path("login_user/", UserLoginView.as_view(), name="login_user"),
] 