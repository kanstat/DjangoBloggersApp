# Generated by Django 4.2.1 on 2023-05-30 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_user_password_alter_user_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tinymce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now_add=True)),
                ('content', models.TextField()),
            ],
        ),
    ]
