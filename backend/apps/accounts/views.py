from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer
from django.contrib.auth import login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema


class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입 성공"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    @extend_schema(request=UserLoginSerializer)
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({"message": "로그인 성공"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        logout(request)
        return Response({"message": "로그아웃 성공"}, status=status.HTTP_200_OK)

class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

@ensure_csrf_cookie
def get_csrf_token(request):
    print('==== CSRF DEBUG START ====')
    print('user:', request.user)
    print('is_authenticated:', getattr(request.user, 'is_authenticated', None))
    print('META:', {k: v for k, v in request.META.items() if 'CSRF' in k or 'COOKIE' in k})
    csrf_token = request.META.get('CSRF_COOKIE', '')
    print('csrfToken:', csrf_token)
    print('==== CSRF DEBUG END ====')
    return JsonResponse({'csrfToken': csrf_token})
