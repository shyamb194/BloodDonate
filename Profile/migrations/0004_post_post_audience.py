# Generated by Django 3.1.1 on 2020-09-28 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0003_post_post_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_audience',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
