from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=50)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to=f'{settings.MEDIA_FOLDER}/avatars', blank=True, null=True)


class Advert(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=9000)
    pub_date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='adverts')
    cost = models.IntegerField()

    def __str__(self):
        return self.title


class Media(models.Model):
    image = models.ImageField(upload_to=f'{settings.MEDIA_FOLDER}/media', null=True, blank=True)
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE, related_name='media')

