from rest_framework import serializers

from .models import *


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['name']


class ReportSerializer(serializers.ModelSerializer):
    tags = TagSerializer(required=False, many=True)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        report = Report.objects.create(**validated_data)
        for tag in tags:
            Tag.objects.create(report=report, **tag)
        return report

    class Meta:
        model = Report
        exclude = ['user']


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'