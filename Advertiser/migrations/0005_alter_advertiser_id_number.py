# Generated by Django 5.1.4 on 2025-01-31 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Advertiser', '0004_adrecommendation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertiser',
            name='ID_number',
            field=models.IntegerField(),
        ),
    ]
