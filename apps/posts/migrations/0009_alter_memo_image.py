# Generated by Django 3.2.6 on 2021-10-23 20:04

from django.db import migrations, models
import pathlib


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_alter_memo_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memo',
            name='image',
            field=models.FilePathField(default='', path=pathlib.PurePosixPath('/Users/minh/PycharmProjects/Minimo')),
        ),
    ]