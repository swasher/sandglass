from django.contrib import admin
from .models import Timing, RawData, Manager
from django.contrib.auth.models import User


@admin.register(Timing)
class TimingAdmin(admin.ModelAdmin):

    list_display = ('prepresser', 'order', 'manager', 'jobnote', 'signatime', 'designtime', 'packagetime')
    search_fields = ['order']


@admin.register(RawData)
class RawDataAdmin(admin.ModelAdmin):

    def time_seconds(self, obj):
        return obj.time.strftime("%d %b %Y %H:%M:%S")

    time_seconds.admin_order_field = 'timefield'
    time_seconds.short_description = 'Precise Time'

    list_display = ('prepresser', 'order', 'jobtype', 'button', 'time_seconds', 'manager', 'jobnote')


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):

    list_display = ('name',)