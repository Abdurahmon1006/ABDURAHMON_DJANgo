# Generated by Django 5.2.4 on 2025-07-30 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0002_yutuq'),
    ]

    operations = [
        migrations.AddField(
            model_name='yutuq',
            name='link',
            field=models.URLField(blank=True, max_length=250, null=True, verbose_name='Yutuq havolasi'),
        ),
    ]
