# Generated by Django 3.2.6 on 2021-09-03 16:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timer', '0012_alter_rawdata_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='timing',
            name='perstime',
            field=models.DurationField(default=datetime.timedelta),
        ),
    ]
