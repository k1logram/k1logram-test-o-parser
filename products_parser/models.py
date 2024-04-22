from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.TextField(verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    image_url = models.TextField(blank=True, null=True, verbose_name='url изображения')
    price = models.IntegerField(default=0, verbose_name='Цена')
    discount = models.TextField(default=None, blank=True, null=True, verbose_name='Скидка в %')
    link = models.TextField(verbose_name='Ссылка')
    recording_time = models.TextField(verbose_name='Время окончания')
