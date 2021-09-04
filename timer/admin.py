from django.contrib import admin
from .models import Timing, RawData, Manager
from django.contrib.auth.models import User


@admin.register(Timing)
class TimingAdmin(admin.ModelAdmin):

    def signatime_(self, obj):
        return str(obj.signatime).split('.', 2)[0]

    def designtime_(self, obj):
        return str(obj.designtime).split('.', 2)[0]

    def packagetime_(self, obj):
        return str(obj.packagetime).split('.', 2)[0]

    def perstime_(self, obj):
        return str(obj.packagetime).split('.', 2)[0]

    signatime_.admin_order_field = 'timefield'
    signatime_.short_description = 'Signa time'

    designtime_.admin_order_field = 'timefield'
    designtime_.short_description = 'Design time'

    packagetime_.admin_order_field = 'timefield'
    packagetime_.short_description = 'Package time'

    perstime_.admin_order_field = 'timefield'
    perstime_.short_description = 'Pers time'

    list_display = ('prepresser', 'order', 'manager', 'jobnote', 'signatime_', 'designtime_', 'packagetime_', 'perstime_', 'is_order', 'design_is_paid')
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

    list_display = ('name', 'email', 'asystem_name')