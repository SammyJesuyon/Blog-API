from .serializers import (BlogTag, Blog, BlogComment, BlogCommentSerializer, BlogSerializer, BlogTagSerializer)
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from django.db.models import Count, Q  # using Q allows to merge multiple conditions in filter


class BlogView(ModelViewSet):
    # returns all blogs when queried
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'slug'

    # to override the queryset above to enable the search on the front-end
    def get_queryset(self):
        query = self.request.query_params.dict()
        keyword = query.get('keyword', None)
        query_data = self.queryset
        if keyword:
            query_data = query_data.filter(
                # i means case-insensitive / icontains here means if the title in the database contains the keyword
                # iexact means if the search matches the keyword exactly
                Q(title__icontains=keyword) |
                Q(title__iexact=keyword) |
                Q(tags__title__icontains=keyword) |
                Q(tags__title__iexact=keyword)
            ).distinct()  # distinct was added so the search return just one distinct result for a search as the search
            # tends to return multiple of instances of a result because of the use | above
        return query_data


class BlogCommentView(ModelViewSet):
    # returns all blog comments when queried
    queryset = BlogComment.objects.all()
    serializer_class = BlogCommentSerializer

    # overrides the above queryset
    def get_queryset(self):
        query = self.request.query_params.dict()
        return self.queryset.filter(**query)


class BlogTagView(ModelViewSet):
    # returns all blog tags when queried
    queryset = BlogTag.objects.all()
    serializer_class = BlogTagSerializer


class TopBlogs(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def get_queryset(self):
        blogs = self.queryset.annotate(comment_count=Count(
            'blog_comments')).order_by('-comment_count')[:5]
        return blogs


class SimilarBlogs(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def get_queryset(self):
        blog_id = self.kwargs.get('blog_id')
        try:
            blog_tags = self.queryset.get(id=blog_id).tags.all()
        except Exception:
            return None
        # __ used to traverse the tags id because of its relationship with blogs, and as tags has its own id
        blogs = self.queryset.filter(tags__id__in=[tag.id for tag in blog_tags]).exclude(id=blog_id)
        return blogs
