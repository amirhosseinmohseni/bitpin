from django.contrib import admin
from .models import Post, Rating



class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'total_votes', 'total_score', 'created_at', 'average_rating')
    
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'score')


admin.site.register(Post, PostAdmin)
admin.site.register(Rating, RatingAdmin)