# Generated by Django 3.2.6 on 2021-09-04 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timer', '0013_timing_perstime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawdata',
            name='jobtype',
            field=models.CharField(blank=True, choices=[('Signa', 'Signa'), ('Design', 'Design'), ('Package', 'Package'), ('Pers', 'Pers')], max_length=12, null=True),
        ),
    ]
