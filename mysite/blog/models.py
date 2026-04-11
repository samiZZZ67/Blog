from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
from django.db import models
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    status = models.CharField(
    max_length=2,
    choices=Status,
    default=Status.DRAFT
    )
       
    class Meta:
        ordering=['-publish']
    def __str__(self):
        return self.title