from django.db import models
from django.conf import settings


class Curs(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=1000, blank=True, null=True)
    preview = models.ImageField(upload_to='curces', blank=True, null=True)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=1000, blank=True, null=True)
    preview = models.ImageField(upload_to='curces', blank=True, null=True)
    url_video = models.URLField()

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.title
