# Generated by Django 4.0.1 on 2023-10-05 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='is_default',
            field=models.BooleanField(default=False),
        ),
    ]