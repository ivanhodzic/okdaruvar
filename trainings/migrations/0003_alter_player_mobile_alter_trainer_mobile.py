# Generated by Django 4.1.7 on 2023-05-19 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0002_player_mobile_trainer_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='mobile',
            field=models.CharField(blank=True, default=None, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='trainer',
            name='mobile',
            field=models.CharField(blank=True, default=None, max_length=30, null=True),
        ),
    ]
