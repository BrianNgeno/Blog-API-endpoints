import json
from collections import OrderedDict

from django.core import serializers
from django.core.paginator import Paginator
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.pagination import PageNumberPagination
# Create your views here.
from rest_framework.permissions import (SAFE_METHODS, AllowAny, BasePermission,
                                        IsAuthenticated)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Blog, User
from .serializers import BlogSerializer, RegistrationSerializer


class CustomPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    def get_paginated_response(self, data):
        return Response(OrderedDict({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        }))

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class RegistrationView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer_data = serializer.validated_data
        user = User.objects.create(**serializer_data)
        user.set_password(serializer_data['password'])
        user.save()
        return Response({"success": "User registered successfully"}, status=status.HTTP_201_CREATED)


class BlogAPIView(GenericAPIView,CustomPagination):
    permission_classes = [IsAuthenticated | ReadOnly]
    serializer_class = BlogSerializer
    # queryset = Blog.objects.fi()
    # pagination_class = CustomPagination

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer_data = serializer.validated_data
        blog = Blog(**serializer_data)
        blog.user = request.user
        blog.save()
        blogs_serialized = serializers.serialize(
            'json', Blog.objects.get_queryset())
        blogs = json.loads(blogs_serialized)

        return Response(blogs, status=status.HTTP_201_CREATED)

    def get(self, request):
        def get_paginated_response(self, data):
            return Response(OrderedDict([
                ('count', self.page.paginator.count),
                ('next', self.get_next_link()),
                ('previous', self.get_previous_link()),
                ('results', data),
                
            ]))
        serializer = self.serializer_class(Blog.objects.all(), many=True, allow_empty=True)
        paginated_data = self.paginate_queryset(serializer.data)
        response = self.get_paginated_response(paginated_data)
        return response
        # blogs_serialized = serializers.serialize('json', Blog.objects.get_queryset())
        # blogs = json.loads(blogs_serialized)
        # return Response(self.queryset, status=status.HTTP_201_CREATED)
    def put(self, request):
        blog_id = request.query_params.get('blog_id')
        serializer = self.serializer_class(
            instance=request.user, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer_data = serializer.validated_data
        blog = Blog.objects.filter(id=blog_id).update(
            **serializer.validated_data)
        blog_serialized = serializers.serialize(
            'json', [Blog.objects.get(id=blog_id)])
        blog = json.loads(blog_serialized)
        return Response(blog, status=status.HTTP_200_OK)

    def delete(self, request):
            blog_id = request.query_params.get('blog_id')
            blog = Blog.objects.filter(id=blog_id).delete()
            blogs_serialized = serializers.serialize(
            'json', Blog.objects.get_queryset())
            blogs = json.loads(blogs_serialized)
            message={'success':'Blog deleted successfully',
                     "blogs":blogs}
            return Response(message, status=status.HTTP_200_OK)    
