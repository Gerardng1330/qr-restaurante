# Generated by Django 5.0.3 on 2024-08-14 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qr_app', '0008_imagenmuelle_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
