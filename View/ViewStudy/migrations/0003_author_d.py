# Generated by Django 4.0.8 on 2022-11-30 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ViewStudy', '0002_author_last_accessed'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='d',
            field=models.IntegerField(null=True),
        ),
    ]
