from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


# Create your models here.
class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISH)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISH = 'PB', 'Publish'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    objects = models.Manager()
    publish = PublishManager()
    tags = TaggableManager()

    class Meta:
        ordering = ['-published']
        indexes = [
            models.Index(fields=['-published'])
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post-detail',
                       args=[self.published.year, self.published.month, self.published.day, self.slug])
