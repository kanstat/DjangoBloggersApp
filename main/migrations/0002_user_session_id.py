# Generated by Django 4.2.1 on 2023-05-25 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='session_id',
            field=models.CharField(default=0, max_length=100),
        ),
    ]
