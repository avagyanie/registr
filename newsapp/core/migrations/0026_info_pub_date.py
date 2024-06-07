# Generated by Django 4.2.4 on 2023-09-21 15:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_contact_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
