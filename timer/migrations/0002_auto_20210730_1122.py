# Generated by Django 3.2.5 on 2021-07-30 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawdata',
            name='description',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='rawdata',
            name='jobtype',
            field=models.CharField(blank=True, choices=[('Signa', 'Signa'), ('Design', 'Design'), ('Package', 'Package')], max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='rawdata',
            name='order',
            field=models.CharField(blank=True, max_length=7, null=True),
        ),
    ]
