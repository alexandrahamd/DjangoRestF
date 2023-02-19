from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    phone = models.CharField(max_length=10, verbose_name='телефон', blank=True, null=True)
    city = models.CharField(max_length=20, verbose_name='город', blank=True, null=True)
    foto = models.ImageField(upload_to='users/', verbose_name='фотография', blank=True, null=True)
    username = None
    email = models.EmailField(verbose_name='Почта', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []