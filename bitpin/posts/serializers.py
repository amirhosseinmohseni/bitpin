from rest_framework import serializers
from .models import Post, Rating

class PostSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    user_rating = serializers.SerializerMethodField()
    total_votes = serializers.IntegerField()

    def get_average_rating(self, obj):
        return round(obj.average_rating(), 1)

    def get_user_rating(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            rating = obj.ratings.filter(user=user).first()
            return rating.score if rating else None
        return None

    class Meta:
        model = Post
        fields = ["id", "title", "average_rating", "total_votes", "user_rating"]
        
class RatingRequestSerializer(serializers.ModelSerializer):
    post = serializers.UUIDField()
    class Meta:
        model = Rating
        fields = ["post", "score"]
        
class RatingResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('user', 'post', 'score')