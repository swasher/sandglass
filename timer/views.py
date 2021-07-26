from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import Timing, RawData, Manager
from .util import clock_off


def hello(request):
    delta = clock_off()
    # delta = 0
    managers = Manager.objects.all()

    last_click = RawData.objects.filter(prepresser=request.user).latest('time')
    if last_click.button == 'start':  # это значит, что старт нажали, и пока бежал секундомер, страница была перезагружена.
        pass

    return render(request, 'timer.html', {'delta': delta, 'managers': managers})


@login_required
@ensure_csrf_cookie
def click_startz(request):
    error = 'all ok'
    if request.is_ajax() and request.method == 'GET':
        GET = request.GET
        if 'order' in GET and 'jobtype' in GET:

            raw = RawData.objects.create(
                prepresser=request.user,
                button='start',
                order=GET['order'],
                jobtype=GET['jobtype']
            ).save()

        else:
            error = 'no needed data in GET'
    else:
        error = 'non ajax or non GET'

    results = {'error': error}
    return JsonResponse(results)


@login_required
@ensure_csrf_cookie
def click_stopz(request):
    error = 'all ok'
    if request.is_ajax() and request.method == 'GET':
        GET = request.GET
        if 'order' in GET and 'jobtype' in GET:

            user = request.user
            order = GET['order']
            jobtype = GET['jobtype']
            button = 'stop'

            raw = RawData.objects.create(
                prepresser=user,
                button=button,
                order=order,
                jobtype=jobtype
            )
            raw.save()

            start_time = RawData.objects.filter(prepresser=user,
                                                order=order,
                                                jobtype=jobtype,
                                                button='start')\
                .latest('time').serializable_value('time')

            duration = raw.time - start_time

            obj, created = Timing.objects.get_or_create(
                prepresser=user,
                order=order,
            )
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
            error = 'no needed data in GET'
    else:
        error = 'non ajax or non GET'

    results = {'error': error}
    return JsonResponse(results)


@login_required
@ensure_csrf_cookie
def click_startm(request):
    error = 'all ok'
    if request.is_ajax() and request.method == 'GET':
        GET = request.GET
        if 'order' in GET and 'jobtype' in GET:

            raw = RawData.objects.create(
                prepresser=request.user,
                button='start',
                order=GET['order'],
                jobtype=GET['jobtype']
            ).save()

        else:
            error = 'no needed data in GET'
    else:
        error = 'non ajax or non GET'

    results = {'error': error}
    return JsonResponse(results)


@login_required
@ensure_csrf_cookie
def click_stopm(request):
    error = 'all ok'
    if request.is_ajax() and request.method == 'GET':
        GET = request.GET
        if 'order' in GET and 'jobtype' in GET:

            user = request.user
            order = GET['order']
            jobtype = GET['jobtype']
            button = 'stop'

            raw = RawData.objects.create(
                prepresser=user,
                button=button,
                order=order,
                jobtype=jobtype
            )
            raw.save()

            start_time = RawData.objects.filter(prepresser=user,
                                                order=order,
                                                jobtype=jobtype,
                                                button='start')\
                .latest('time').serializable_value('time')

            duration = raw.time - start_time

            obj, created = Timing.objects.get_or_create(
                prepresser=user,
                order=order,
            )
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
            error = 'no needed data in GET'
    else:
        error = 'non ajax or non GET'

    results = {'error': error}
    return JsonResponse(results)
