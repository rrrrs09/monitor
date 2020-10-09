from rest_framework import serializers

from .models import *


class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        exclude = ['user']


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'