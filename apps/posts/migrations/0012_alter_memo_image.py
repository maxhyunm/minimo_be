# Generated by Django 3.2.6 on 2021-10-23 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_alter_memo_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memo',
            name='image',
            field=models.FileField(null=True, upload_to='media'),
        ),
    ]
