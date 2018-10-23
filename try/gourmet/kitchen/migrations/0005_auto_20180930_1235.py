# Generated by Django 2.1.1 on 2018-09-30 12:35

from django.db import migrations, models
import kitchen.models


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0004_auto_20180930_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='everyone',
            name='cover',
            field=models.FileField(null=True, upload_to=kitchen.models.Everyone.user_directory_path_cover),
        ),
        migrations.AlterField(
            model_name='everyone',
            name='dp',
            field=models.FileField(null=True, upload_to=kitchen.models.Everyone.user_directory_path_dp),
        ),
    ]
