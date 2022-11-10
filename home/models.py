from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.


class Article(models.Model):
    category = models.ForeignKey('self', on_delete=models.CASCADE)
    ID = models.IntegerField()
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField()
    body = RichTextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    min_read = models.PositiveIntegerField()


class Category(models.Model):
    ID = models.IntegerField()
    title = models.CharField(max_length=200)


    def __str__(self):
		    return self.title


