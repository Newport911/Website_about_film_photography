# Generated by Django 5.0.3 on 2024-03-20 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmblog', '0002_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='preview',
            field=models.TextField(default='prew'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='body',
            field=models.TextField(blank=True),
        ),
    ]
