# Generated by Django 4.2.1 on 2023-06-19 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_tinymce_pub_url_active_tinymce_published_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='read_permission',
            field=models.CharField(default='', max_length=50),
        ),
    ]