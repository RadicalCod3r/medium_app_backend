from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
                    ID = models.IntegerField()
                    email = models.EmailField(max_length=255, unique=True)
                    phone_number = models.CharField(max_length=11, unique=True, validators=[
                    RegexValidator(
                        regex=r'^\+?1?\d{9,15}$',
                        message="Phone number must be entered in the format '+123456789'. Up to 15 digits allowed."
                    ),
                    ],)
                    first_name = models.CharField(max_length=100)
                    last_name = models.CharField(max_length=100)
                    title = models.CharField(max_length=200)
                    description = models.TextField()
                    is_active = models.BooleanField(default=True)
                    is_admin = models.BooleanField(default=False)

                    USERNAME_FIELD = 'phone_number'
                    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

                    def __str__(self):
                        return self.email

                    @property
                    def is_staff(self):
                        return self.is_admin


class OtpCode(models.Model):
	phone_number = models.CharField(max_length=11, unique=True)
	code = models.PositiveSmallIntegerField()
	created = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.phone_number} - {self.code} - {self.created}'
        
	