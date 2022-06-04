from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.utils.text import slugify


class BlogTag(models.Model):
    # title is unique so that we don't have duplicates
    title = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Blog(models.Model):
    tags = models.ManyToManyField(BlogTag, related_name='blog_tags')
    cover = models.ImageField(null=True, blank=True)
    # title is unique so that we don't have duplicates
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(default='', editable=False, max_length=255)
    author = models.ForeignKey(User, related_name='blog_author', on_delete=models.CASCADE)
    content = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class meta:
        # the ordering is negative because we want our list to be in descending order, with the
        # latest coming first
        ordering = ("-created_at")

    def __str__(self):
        return f'{self.title} by {self.author.username}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)


class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, related_name='blog_comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default="Anonymous")
    ip = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class meta:
        # the ordering is negative because we want our list to be in descending order, with the
        # latest coming first
        ordering = ("-created_at")

    def __str__(self):
        return f'{self.blog.title} - {self.name}'
