# Generated by Django 5.1.7 on 2025-03-23 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tableau', '0002_ratingsmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ratingsmodel',
            name='rating',
            field=models.CharField(choices=[('dislike', 0), ('like', 1)], max_length=255),
        ),
    ]
