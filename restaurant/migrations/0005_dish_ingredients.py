# Generated by Django 5.0.7 on 2024-08-25 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='ingredients',
            field=models.TextField(blank=True, null=True),
        ),
    ]
