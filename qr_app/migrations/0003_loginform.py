# Generated by Django 5.0.3 on 2024-04-29 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qr_app', '0002_imagen_delete_website'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
    ]
