from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .models import Post, Rating
from .serializers import PostSerializer, RatingRequestSerializer, RatingResponseSerializer
from django.db import transaction, models
from django.db.models import Sum



class PostListView(ListAPIView):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
class RatePostView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        request=RatingRequestSerializer,
        responses=RatingResponseSerializer
    )

    @transaction.atomic
    def post(self, request):
        try:
            user = request.user
            serializer = RatingRequestSerializer(data=request.data)
            if serializer.is_valid():
                
                post = Post.objects.get(id=serializer.validated_data["post"])
                score = serializer.validated_data["score"]

                if not (0 <= score <= 5):
                    return Response({"error": "Score must be between 0 and 5"}, status=status.HTTP_400_BAD_REQUEST)

                rating, created = Rating.objects.update_or_create(
                    user=user, post=post, defaults={"score": score}
                )
                
                if created:
                    post.total_votes += 1
                post.total_score = post.ratings.aggregate(total=models.Sum("score"))["total"]
                post.save(update_fields=["total_votes", "total_score"])
                
                response = RatingResponseSerializer(data={
                        "user": user.id,
                        "post": post.id,
                        "score": score,
                })
                
                # print(response)
                
                if response.is_valid():
                    return Response(
                        response.data, 
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(response.errors, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)