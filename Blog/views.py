from .serializers import (BlogTag, Blog, BlogComment, BlogCommentSerializer, BlogSerializer, BlogTagSerializer)
from rest_framework.viewsets import ModelViewSet


class BlogView(ModelViewSet):
    # returns all blogs when queried
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'slug'


class BlogCommentView(ModelViewSet):
    # returns all blog comments when queried
    queryset = BlogComment.objects.all()
    serializer_class = BlogCommentSerializer

    def get_queryset(self):
        query = self.request.query_params.dict()
        return self.queryset.filter(**query)


class BlogTagView(ModelViewSet):
    # returns all blog tags when queried
    queryset = BlogTag.objects.all()
    serializer_class = BlogTagSerializer
