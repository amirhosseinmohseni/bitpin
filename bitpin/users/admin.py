from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
	list_display = ('phone_number', 'is_active')


admin.site.register(User, UserAdmin)