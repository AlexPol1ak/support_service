from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    date_joined = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('id','login', 'first_name', 'last_name', 'email',
                  'date_joined', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value: str) -> str:
         return make_password(value)


class UserDataUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user registration data."""

    login = serializers.CharField(max_length=40, required=False)
    first_name = serializers.CharField(max_length=30, required=False)
    last_name = serializers.CharField(max_length=30, required=False)
    email = serializers.CharField(max_length=40, required=False)

    class Meta:
        model = User
        fields = ('login', 'first_name', 'last_name', 'email',)


class UserChangePasswordSerializer(serializers.ModelSerializer):
    """Serializer to change the password."""

    password = serializers.CharField(max_length=20, min_length=5, required=True, write_only=True,) # validators=[validate_password]
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('password', 'old_password', 'id')
        extra_kwargs = {
                        'password': {'read_only': True},
                        'old_password': {'read_only':True},
                        'id': {'read_only': True},
                        }

    def validate(self, attrs):
        if attrs['password'] == attrs['old_password']:
            raise serializers.ValidationError({'error': 'The new password matches the old password.'})
        return attrs


    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

class SupportsControlSerializer(serializers.ModelSerializer):
    """Serializer for assigning helpdesk staff."""

    is_support = serializers.BooleanField()

    class Meta:
        model = User
        fields = ('id', 'login', 'is_support')
        extra_kwargs = {'id': {'read_only': True}, 'login':{'read_only': True}}

