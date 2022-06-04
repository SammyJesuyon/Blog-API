from rest_framework import serializers
from .models import (Blog, BlogComment, BlogTag, )
from User.serializers import UserSerializer


class BlogTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields = ('title',)


class BlogSerializer(serializers.ModelSerializer):
    # tags variable is created so that the tags on the endpoint do not show as index but the object
    # and many is set to true because one blog can have several tags
    tags = BlogTagSerializer(many=True)
    # to be able to tell who the author of this serializer is;
    author = UserSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Blog
        fields = '__all__'


class BlogCommentSerializer(serializers.ModelSerializer):
    blog = BlogSerializer(read_only=True)
    blog_id = serializers.IntegerField(write_only=True)
    # author = UserSerializer(read_only=True)
    # author_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = BlogComment
        fields = '__all__'
