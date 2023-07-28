from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.serializers import serialize
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30, unique=True)
    nickname = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=500)

    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.nickname

    def serialize(self):
        serialized_data = serialize('json', [self])
        return serialized_data


class Book(models.Model):
    name = models.CharField(max_length=255, null=True)
    author = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=500, null=True)
    category_id = models.IntegerField(null=True)
    image = models.CharField(max_length=1000, null=True)
    rating = models.FloatField(null=True)
    price = models.FloatField(null=True)
    status = models.BooleanField(default=False)

    def serialize(self):
        serialized_data = serialize('json', [self])
        return serialized_data


class RentList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def serialize(self):
        serialized_data = serialize('json', [self])
        return serialized_data


