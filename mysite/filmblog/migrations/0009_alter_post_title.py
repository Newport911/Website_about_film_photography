# Generated by Django 5.0.3 on 2024-03-25 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmblog', '0008_post_original_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.TextField(max_length=250),
        ),
    ]
