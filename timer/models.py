from datetime import timedelta

from django.db import models
from django.conf import settings


class Timing(models.Model):
    PRODUCE_WORK = [
        ('Signa', 'Signa'),
        ('Design', 'Design'),
        ('Package', 'Package')
    ]

    # laststarttime: models.TimeField()
    prepresser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.CharField(max_length=7)
    signatime = models.DurationField(default=timedelta)
    designtime = models.DurationField(default=timedelta)
    packagetime = models.DurationField(default=timedelta)

    def alltime(self):
        return self.designtime + self.packagetime + self.designtime

    def __str__(self):
        return self.prepresser + str(self.alltime())


class RawData(models.Model):
    PRODUCE_WORK = [
        ('Signa', 'Signa'),
        ('Design', 'Design'),
        ('Package', 'Package')
    ]
    prepresser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.CharField(max_length=7)
    jobtype = models.CharField(max_length=12, choices=PRODUCE_WORK)
    time = models.DateTimeField(auto_now_add=True, help_text="Время нажатия на кнопку")
    button = models.CharField(max_length=10, choices=[('start', 'start'), ('stop', 'stop')])

    def __str__(self):
        return '%s %s % s%s' % (self.prepresser, self.order, self.button, self.time)


class Manager(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        ordering = ('name',)