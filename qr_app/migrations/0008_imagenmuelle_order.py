# Generated by Django 5.0.3 on 2024-08-13 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qr_app', '0007_alter_imagen_options_imagen_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagenmuelle',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
