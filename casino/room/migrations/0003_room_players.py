# Generated by Django 4.1.5 on 2023-01-20 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0002_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='players',
            field=models.IntegerField(default=0, max_length=3),
        ),
    ]
