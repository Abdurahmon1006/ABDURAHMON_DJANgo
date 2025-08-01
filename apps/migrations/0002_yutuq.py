# Generated by Django 5.2.4 on 2025-07-30 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='yutuq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomi', models.CharField(max_length=100, verbose_name='Yutuq nomi')),
                ('tavsif', models.TextField(verbose_name='Yutuq haqida')),
                ('sana', models.DateField(verbose_name='Olingan sana')),
                ('rasmi', models.ImageField(upload_to='yutuqlar/', verbose_name='Yutuq rasmi')),
                ('darajasi', models.CharField(choices=[('bronza', 'Bronza'), ('kumush', 'Kumush'), ('oltin', 'Oltin'), ('maxsus', 'Maxsus')], default='bronza', max_length=50, verbose_name='Yutuq darajasi')),
            ],
            options={
                'verbose_name': 'Yutuq',
                'verbose_name_plural': 'Yutuqlar',
                'ordering': ['-sana'],
            },
        ),
    ]
