# Generated by Django 5.0.4 on 2024-05-10 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rezerwacje', '0004_auto_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='auto',
            name='brand',
            field=models.CharField(default='fiat', max_length=16),
            preserve_default=False,
        ),
    ]
