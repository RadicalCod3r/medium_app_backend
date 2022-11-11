from django.db import models
from ckeditor.fields import RichTextField
from accounts.models import User
# Create your models here.


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    category = models.ForeignKey('self', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField()
    body = RichTextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    min_read = models.PositiveIntegerField()

    class Meta:
        ordering = ('-created_at', )


class Category(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='category')


    def __str__(self):
		    return self.title


