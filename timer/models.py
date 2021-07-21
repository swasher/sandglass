from django.db import models


class Timer(models.Model):
    prepresser: models.CharField(max_length=50)  # ЭТО КЛЮЧ В АДМИН ПОЛЬЗОВАТЕЛЕЙ
    job: models.CharField(max_length=7)  # на это поле
    laststarttime: models.TimeField()

    PRODUCE_WORK = [
        ('prepresstime', 'Prepress'),
        ('designtime', 'Design'),
        ('packagetime', 'Package')
    ]

    prepresstime: models.TimeField()
    designtime: models.TimeField()
    packagetime: models.TimeField()

    def alltime(self):
        return self.designtime + self.packagetime + self.designtime
