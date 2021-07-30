import datetime

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.exceptions import ObjectDoesNotExist

from .models import Timing, RawData, Manager
from .util import clock_off


def hello(request):
    # delta = clock_off()
    delta = 0
    managers = Manager.objects.all()

    duration = ''
    try:
        last_click = RawData.objects.filter(prepresser=request.user).latest('time')
        if last_click.button == 'start':  # это значит, что старт нажали, и пока бежал секундомер, страница была перезагружена.
            duration = int(abs((datetime.datetime.now() - last_click.time).total_seconds()))
            print('duration', datetime.datetime.now() - last_click.time)
            print('duration in sec', (datetime.datetime.now() - last_click.time).total_seconds())
    except ObjectDoesNotExist:  # empty database
        last_click = ''
    except TypeError:  # user is not logged in
        last_click = ''

    return render(request, 'timer.html', {'delta': delta, 'managers': managers, 'duration': duration})


@login_required
@ensure_csrf_cookie
def click_start(request):
    error = 'all ok'
    if request.is_ajax() and request.method == 'GET':
        GET = request.GET

        if GET['active_tab'] == 'order-tab':
            raw = RawData.objects.create(
                prepresser=request.user,
                button='start',
                order=GET['order'],
                jobtype=GET['jobtype']
            ).save()
        elif GET['active_tab'] == 'managers-tab':
            raw = RawData.objects.create(
                prepresser=request.user,
                button='start',
                manager=Manager.objects.get(pk=int(GET['managerid'])),
                jobnote=GET['jobnote'],
                jobtype = GET['jobtype']
            ).save()
        else:
            error = 'not found `active_tab` in GET'
    else:
        error = 'non ajax or non GET'

    results = {'error': error}
    return JsonResponse(results)


@login_required
@ensure_csrf_cookie
def click_stop(request):
    error = 'all ok'
    if request.is_ajax() and request.method == 'GET':
        GET = request.GET

        user = request.user
        jobtype = GET['jobtype']
        button = 'stop'

        raw = RawData.objects.create(
                prepresser=user,
                button=button,
                jobtype=jobtype
            )

        if GET['active_tab'] == 'order-tab':
            order = GET['order']
            raw.order = order
            raw.save()

            start_time = RawData.objects.filter(prepresser=user,
                                                jobtype=jobtype,
                                                button='start',
                                                order=order,) \
                .latest('time').serializable_value('time')

            obj, created = Timing.objects.get_or_create(
                prepresser=user,
                order=order,
            )

        elif GET['active_tab'] == 'managers-tab':
            manager = Manager.objects.get(pk=int(GET['managerid']))
            jobnote = GET['jobnote']
            raw.manager = manager
            raw.jobnote = jobnote
            raw.save()

            start_time = RawData.objects.filter(prepresser=user,
                                                jobtype=jobtype,
                                                button='start',
                                                manager=manager,
                                                jobnote=jobnote) \
                .latest('time').serializable_value('time')

            obj, created = Timing.objects.get_or_create(
                prepresser=user,
                manager=manager,
                jobnote=jobnote
            )

        else:
            error = 'not found `active_tab` in GET'
            return JsonResponse({'error': error})

        duration = raw.time - start_time

        if jobtype == 'Signa':
            obj.signatime += duration
        elif jobtype == 'Package':
            obj.packagetime += duration
        elif jobtype == 'Design':
            obj.designtime += duration
        else:
            raise Exception
        obj.save()

    else:
        error = 'non ajax or non GET'

    results = {'error': error}
    return JsonResponse(results)


@login_required
@ensure_csrf_cookie
def click_cancel(request):
    error = 'all ok'
    if request.is_ajax() and request.method == 'GET':
        last_raw = RawData.objects.latest('time')
        if last_raw.button == 'start':
            _ = last_raw.__str__()
            last_raw.delete()
            error = f'{_} sucessfully deleted'
        else:
            error = f'Last record not a "start"'
    else:
        error = 'non ajax or non GET'

    results = {'error': error}
    return JsonResponse(results)

