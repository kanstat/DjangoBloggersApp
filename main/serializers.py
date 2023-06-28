from rest_framework import serializers
from .models import *
from django.utils.html import strip_tags


class UserAuthSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['email', 'password']


class ViewBlogSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    # content = serializers.TextField()

    class Meta:
        model = Tinymce
        fields = ['title', 'content', 'created_at']

    # def get_parsed_content(self, obj):
    #     return strip_tags(obj.content)
