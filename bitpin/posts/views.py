from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Rating
from .serializers import PostSerializer, RatingSerializer
from django.db import transaction, models
from django.db.models import Sum



class PostListView(ListAPIView):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
class RatePostView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, post_id):
        user = request.user
        post = Post.objects.get(id=post_id)
        score = request.data.get("score")

        if not (0 <= score <= 5):
            return Response({"error": "Score must be between 0 and 5"}, status=status.HTTP_400_BAD_REQUEST)

        rating, created = Rating.objects.update_or_create(
            user=user, post=post, defaults={"score": score}
        )

        if created:
            post.total_votes += 1
        post.total_score = post.ratings.aggregate(total=models.Sum("score"))["total"]
        post.save(update_fields=["total_votes", "total_score"])

        return Response({"message": "Rating submitted"}, status=status.HTTP_200_OK)