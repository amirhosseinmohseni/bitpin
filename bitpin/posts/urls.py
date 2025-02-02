from django.urls import path
from .views import PostListView, RatePostView

urlpatterns = [
    path("", PostListView.as_view(), name="post-list"),
    path("rate/", RatePostView.as_view(), name="rate-post"),
]