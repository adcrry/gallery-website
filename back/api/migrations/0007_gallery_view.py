# Generated by Django 4.1.2 on 2023-09-11 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_face'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallery',
            name='view',
            field=models.CharField(choices=[('galerie', 'Gallery'), ('exposition', 'Exposition')], default='galerie', max_length=20),
        ),
    ]