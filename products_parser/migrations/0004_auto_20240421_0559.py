# Generated by Django 3.2 on 2024-04-21 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products_parser', '0003_alter_product_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='link',
            field=models.TextField(verbose_name='Ссылка'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.TextField(verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='product',
            name='recording_time',
            field=models.TextField(verbose_name='Время окончания'),
        ),
    ]
