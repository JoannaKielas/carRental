# Generated by Django 5.0.4 on 2024-05-12 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rezerwacje', '0008_alter_account_date_joined'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]