# Generated by Django 3.1.1 on 2020-09-28 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0002_auto_20200927_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_type',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]