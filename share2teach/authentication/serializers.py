from rest_framework import serializers
from .models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'subject_major', 'affiliation']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'user_type']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            user_type='Educator',  # Set default user_type to 'Educator'
            is_active=False  # Initially inactive
        )

        # Generate token and send verification email
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verification_link = f"{settings.FRONTEND_URL}/auth/verify-email/{uid}/{token}/"

        # Send verification email
        send_mail(
            subject="Verify your email address",
            message=f"Click the link to verify your email: {verification_link}",
            from_email=settings.EMAIL_FROM_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

         # If the user should be an admin
        if self.context['request'].user.is_superuser:
            user.user_type = 'Administrator'
            user.is_staff = True
            user.is_superuser = True

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid credentials")
        
        # Ensure only administrators can log in via this serializer
        if user.user_type == 'Administrator':
            if not user.is_superuser:
                raise serializers.ValidationError("Unauthorized access. Admins only.")
        return {'user': user}

        