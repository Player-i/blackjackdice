# Generated by Django 4.1.5 on 2023-01-20 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0005_alter_room_players_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='players',
            field=models.IntegerField(default=0),
        ),
    ]
