# Generated by Django 4.0 on 2022-07-25 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('individuals', '0011_alter_wallet_type_of_wallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='phone_number',
            field=models.CharField(max_length=12),
        ),
    ]
