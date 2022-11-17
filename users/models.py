from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False)
    title = models.CharField(max_length=100)
    description  = models.CharField(max_length=400)
    image = models.ImageField(upload_to='images/users/', default='images/users/user.jpg')

    def __str__(self):
        return self.email