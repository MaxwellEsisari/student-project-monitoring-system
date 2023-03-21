# Generated by Django 4.1.7 on 2023-03-18 21:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_progressbar_remove_room_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='progressbar',
            name='description',
        ),
        migrations.AddField(
            model_name='progressbar',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='progressbar',
            name='percentage',
            field=models.IntegerField(),
        ),
    ]
