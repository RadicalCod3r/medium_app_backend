from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from users.models import User
from ckeditor.fields import RichTextField

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=80)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=100)
    caption = models.CharField(max_length=150)
    image = models.ImageField(upload_to="images/posts/", default="images/users/user.jpg")
    body = RichTextField(null=True, blank=True)
    slug = models.SlugField(null=True, blank=True, max_length=250)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    read_time = models.PositiveIntegerField(default=0, null=True, blank=True)
    
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = f'{slugify(self.title)}-{get_random_string(8,"0123456789")}'
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-created_at',)