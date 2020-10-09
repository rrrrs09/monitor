from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .models import *
from .serializers import *


class ReportView(GenericAPIView):
    '''View for listing or creating reports'''
    serializer_class = ReportSerializer

    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return Report.objects.filter(user=self.request.user)


class ReportDetailView(GenericAPIView):
    '''View for retrieving or deleting reports'''
    serializer_class = ReportSerializer

    def get(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def delete(self, request, pk):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        return Report.objects.filter(user=self.request.user)


class PostDetailView(GenericAPIView):
    '''View for retrieving post'''
    def get(self, request, pk):
        instance = get_object_or_404(Post, pk=pk)
        if instance.report.user != request.user:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(instance)
        return Response(serializer.data)


class PostlistView(GenericAPIView):
    '''View for listing all, favorite, spam or archive posts'''
    model = None
    serializer_class = PostSerializer

    def get(self, request, pk):
        '''Returns paginated list of posts'''
        report = Report.objects.get(pk=pk)
        if report.user != request.user:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if self.model is not None:
            posts_ids = self.model.objects.filter(post__report=report) \
                                          .values('post')
            queryset = Post.objects.filter(pk__in=posts_ids)
        else:
            queryset = Post.objects.filter(report=pk)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CategoryToggleView(APIView):
    '''
    View for creating and deleting posts from favorites, spam or archive
    '''
    model = None

    def post(self, request):
        '''Adds post to category or delete if one exists'''
        post_id = request.data.get('post')
        if post_id is None:
            return Response({'error': 'post ID is not passed'},
                            status=status.HTTP_400_BAD_REQUEST)

        post = Post.objects.get(pk=post_id)
        instance, created = self.model.objects.get_or_create(post=post)
        if created:
            return Response(status=status.HTTP_201_CREATED)

        self.model.objects.get(post=post).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
