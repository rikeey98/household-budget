from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'nickname', 'phone')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        # 디버깅: 사용자 존재 확인
        print(f"[LOGIN DEBUG] Attempting login for username: {username}")
        try:
            from .models import User
            user_exists = User.objects.filter(username=username).exists()
            print(f"[LOGIN DEBUG] User exists: {user_exists}")
            if user_exists:
                db_user = User.objects.get(username=username)
                print(f"[LOGIN DEBUG] User active: {db_user.is_active}")
                print(f"[LOGIN DEBUG] Password hash starts with: {db_user.password[:20]}")
        except Exception as e:
            print(f"[LOGIN DEBUG] Error checking user: {e}")

        user = authenticate(username=username, password=password)
        print(f"[LOGIN DEBUG] Authenticate result: {user}")

        if not user:
            raise serializers.ValidationError("아이디 또는 비밀번호가 올바르지 않습니다.")
        data['user'] = user
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'nickname', 'phone')
