from datetime import timedelta

from django.db import models
from django.conf import settings


class Manager(models.Model):
    email = models.EmailField(unique=False, max_length=50)
    name = models.CharField(max_length=30)
    asystem_name = models.CharField(max_length=30)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


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
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, null=True, blank=True)
    jobnote = models.CharField(max_length=100, null=True, blank=True)
    is_order = models.BooleanField()

    def alltime(self):
        return self.designtime + self.packagetime + self.designtime

    def __str__(self):
        return ' '.join([self.prepresser.username, str(self.alltime())])


class RawData(models.Model):
    PRODUCE_WORK = [
        ('Signa', 'Signa'),
        ('Design', 'Design'),
        ('Package', 'Package')
    ]
    prepresser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    button = models.CharField(max_length=10, choices=[('start', 'start'), ('stop', 'stop')])
    time = models.DateTimeField(auto_now_add=True, help_text="Время нажатия на кнопку")
    order = models.CharField(max_length=7, null=True, blank=True)
    jobtype = models.CharField(max_length=12, choices=PRODUCE_WORK, null=True, blank=True)
    manager = models.ForeignKey(Manager, null=True, on_delete=models.CASCADE)
    jobnote = models.CharField(max_length=100, null=True, blank=True)
    is_order = models.BooleanField()

    def __str__(self):
        return '%s %s %s %s' % (self.prepresser, self.order, self.button, self.time)


