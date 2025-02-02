from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from django.conf import settings
import uuid

User = settings.AUTH_USER_MODEL

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    content = models.TextField()
    total_votes = models.PositiveIntegerField(default=0)
    total_score = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def average_rating(self):
        return self.total_score / self.total_votes if self.total_votes > 0 else 0
    
    def __str__(self):
        return self.title
    
class Rating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="ratings")
    score = models.PositiveSmallIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} rated {self.post} {self.score}"