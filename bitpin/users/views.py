from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status

from .serializers import UserSerializer, UserLoginSerializer


class RegisterUserView(APIView):
    permission_classes = [AllowAny]
    
    @extend_schema(
        request=UserSerializer,
        responses=UserLoginSerializer
    )

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    
# class UserLoginView(TokenObtainPairView):
#     serializer_class = UserLoginSerializer

class UserLoginView(APIView):
    permission_classes = [AllowAny]
    
    @extend_schema(
        request=UserSerializer,
        responses=UserLoginSerializer
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)