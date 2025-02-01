from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User
from utils.utils import validate_phone_number

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone_number", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    def validate_phone_number(self, phone_number):
        if validate_phone_number(phone_number):
            if User.objects.filter(phone_number=phone_number).exists():
                raise serializers.ValidationError("Phone number already exists!")
            else: 
                return phone_number
        else:
            raise serializers.ValidationError("Invalid phone number")
   
class UserLoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token