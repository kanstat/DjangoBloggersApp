# Generated by Django 4.2.1 on 2023-06-09 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_tinymce_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tinymce',
            name='title',
            field=models.CharField(default='Untitled', max_length=200),
        ),
    ]
