from django.urls import path, include
from .views import (BlogTagView, BlogCommentView, BlogView, )
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# define the route with a name and map it to the view
# when a request is made to 'blogs', it draws from Blogview
router.register('blogs', BlogView)
router.register('blog-tags', BlogTagView)
router.register('blog-comments', BlogCommentView)

urlpatterns = [
    path('', include(router.urls)),
]
