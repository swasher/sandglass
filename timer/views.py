import datetime
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize

from .models import Timing, RawData, Manager
from .util import clock_offset
from .util import get_fulltime_by_order, get_fulltime_by_manager, get_order_info
from .forms import UserLoginForm


@login_required
def hello(request):
    managers = Manager.objects.all()

    restoring = dict()
    restoring['needed'] = False
    try:
        last_click = RawData.objects.filter(prepresser=request.user).latest('time')
        if last_click.button == 'start':  # это значит, что старт нажали, и пока бежал секундомер, страница была перезагружена.
            restoring['needed'] = True
            restoring['duration'] = int(abs((datetime.datetime.now() - last_click.time).total_seconds()))
            # нужно возвращать (кроме секундомера)
            # активная вкладка
            # если первая вкладка - то order
            # если вторая, то манагер + описание
            # ИЛИ можно попробовать возвращать всю запись из таблицы RAW и все делать уже на клиенте

            restoring['order'] = last_click.order
            try:
                restoring['managerid'] = last_click.manager.id
            except AttributeError:
                restoring['managerid'] = None
            restoring['jobnote'] = last_click.jobnote
            restoring['jobtype'] = last_click.jobtype
            restoring = json.dumps(restoring)

            """
            Тут таки говнокод. Я is_order в Timing добавил, в в RawData нет, типа он там не сильно нужен...
            И поэтому у меня логика тут опирается не на явный is_order, а на косвенный признак - 
            есть jobnote или нет. Решил пока так оставить, должно работать.
            
            Изменения записей возможны в таблице Timings, но не в RawData - это просто лог и ничего меняться
            тут не должно. 
            """

            if restoring['jobnote']:
                restoring['fulltime'] = get_fulltime_by_manager(restoring['managerid'], restoring['jobnote'])
                restoring['tab'] = 'second'
            else:
                restoring['fulltime'] = get_fulltime_by_order(restoring['order'])
                restoring['tab'] = 'first'

            # print('duration', datetime.datetime.now() - last_click.time)
            # print('duration in sec', (datetime.datetime.now() - last_click.time).total_seconds())
    except ObjectDoesNotExist:  # empty database
        last_click = ''
    except TypeError:  # user is not logged in
        last_click = ''

    a = 1

    return render(request, 'timer.html', {'managers': managers, 'restoring': restoring})


@login_required
@ensure_csrf_cookie
def click_start(request):
    error = 'ok'
    if request.is_ajax() and request.method == 'GET':
        GET = request.GET

        if GET['is_order'] == 'true':
            RawData.objects.create(
                prepresser=request.user,
                button='start',
                order=GET['order'],
                jobtype=GET['jobtype'],
            ).save()
        elif GET['is_order'] == 'false':
            RawData.objects.create(
                prepresser=request.user,
                button='start',
                manager=Manager.objects.get(pk=int(GET['managerid'])),
                jobnote=GET['jobnote'],
                jobtype=GET['jobtype'],
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
    error = 'ok'
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

        if GET['is_order'] == 'true':
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
                is_order=True
            )

        elif GET['is_order'] == 'false':
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
                jobnote=jobnote,
                is_order=False
            )

        else:
            error = 'not found `is_order` in GET'
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
    if request.is_ajax() and request.method == 'GET':
        last_raw = RawData.objects.latest('time')
        if last_raw.button == 'start':
            _ = last_raw.__str__()
            last_raw.delete()
            error = f'{_} sucessfully deleted'
        else:
            error = 'Last record not a "start"'
    else:
        error = 'non ajax or non GET'

    results = {'error': error}
    return JsonResponse(results)


@login_required
@ensure_csrf_cookie
def get_latest_jobnotes(request):
    days = 30
    results = {'error': 'ok'}

    if request.is_ajax() and request.method == 'GET':
        GET = request.GET
        managerid = GET['managerid']
        two_month = datetime.datetime.now() - datetime.timedelta(days=days)
        latest_jobnotes = RawData.objects.filter(manager_id=managerid, button='start', time__gt=two_month).values_list('jobnote', flat=True)
        latest_jobnotes = list(dict.fromkeys(latest_jobnotes))  # remove duplicates
        results['latest_jobnotes'] = json.dumps(list(latest_jobnotes), ensure_ascii=False)
    else:
        results['error'] = 'non ajax or non GET'

    return JsonResponse(results)


@login_required
@ensure_csrf_cookie
def get_info(request):
    results = dict()

    if request.is_ajax() and request.method == 'GET':
        GET = request.GET
        order = GET['order']
        results = get_order_info(order)
    else:
        results['error'] = 'non ajax or non GET'

    return JsonResponse(results)
