from django.db import models

# Create your models here.

class User(models.Model):
        ID = models.IntegerField()
        email = models.EmailField(max_length=255, unique=True)
        phone_number = models.CharField(max_length=11, unique=True)
        first_name = models.CharField(max_length=100)
        last_name = models.CharField(max_length=100)
        title = models.CharField(max_length=200)
        description = models.TextField()

        def __str__(self):
            return self.email


class OtpCode(models.Model):
	phone_number = models.CharField(max_length=11, unique=True)
	code = models.PositiveSmallIntegerField()
	created = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.phone_number} - {self.code} - {self.created}'
        
	