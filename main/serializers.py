from rest_framework import serializers
from .models import *


class UserAuthSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['email', 'password']
