from django.contrib.auth import get_user_model
from django.db import models
from ckeditor.fields import RichTextField
from accounts.models import User
# Create your models here.
User = get_user_model()
from .utils import BaseModel



class Category(BaseModel):
    title = models.CharField(max_length=30)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='category')

    class Meta:
        verbose_name_plural = 'categories'


    def __str__(self):
		    return self.title


class Article(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles', null=True)
    categories = models.ManyToManyField(Category, blank=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField()
    body = RichTextField()
    updated_at = models.DateTimeField()
    min_read = models.PositiveIntegerField()
    description = models.TextField()

    class Meta:
        ordering = ('-created_at', )




