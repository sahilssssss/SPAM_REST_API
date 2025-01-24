from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, phone_number, password=None, email=None):
        if not phone_number:
            raise ValueError('Users must have a phone number')
        user = self.model(username=username, phone_number=phone_number, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, phone_number, password=None, email=None):
        user = self.create_user(username, phone_number, password, email)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Contact(models.Model):
    owner = models.ForeignKey(User, related_name='contacts', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.name


class Spam(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.phone_number

# many to many

class SpamMarkedBy(models.Model):
    spam = models.ForeignKey(Spam, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('spam', 'user')

    def __str__(self):
        return f'{self.user.username} marked {self.spam.phone_number} as spam'
