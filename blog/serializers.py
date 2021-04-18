from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User, Blog


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
            model = Blog
            fields = ['image', 'publisher', 'content', 'title']

