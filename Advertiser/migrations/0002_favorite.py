# Generated by Django 5.1.4 on 2025-01-29 07:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Advertiser', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('advertisement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Advertiser.advertisement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Favorite',
                'unique_together': {('user', 'advertisement')},
            },
        ),
    ]
