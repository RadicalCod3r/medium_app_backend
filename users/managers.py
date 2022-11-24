from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, phone, email, password=None, name=None, is_staff=False, is_superuser=False, is_active=True):
        if not phone:
            raise ValueError('You should provide a phone number.')
        if not email:
            raise ValueError('You should provide an email address.')
        user = self.model(phone = phone, email = email, name = name)
        user.set_password(password)
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.is_active = is_active
        user.save()

        return user

    def create_staffuser(self, phone, email, password=None):
        return self.create_user(
            phone = phone,
            email = email,
            password = password,
            is_staff=True
        )

    def create_superuser(self, phone, email, password=None):
        return self.create_user(
            phone = phone,
            email = email,
            password = password,
            is_staff = True,
            is_superuser = True
        )