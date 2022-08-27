# Generated by Django 3.2.6 on 2021-08-22 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Memo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contents', models.TextField(verbose_name='Memo')),
                ('number', models.IntegerField(verbose_name='Title Number')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
