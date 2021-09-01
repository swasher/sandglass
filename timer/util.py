import json
import pytz
from datetime import datetime
import urllib.request
from lxml import etree
from .models import Timing, RawData, Manager


def clock_offset():
    """
    DEPRECATED
    Now time delta calculated on client by js, due to big time lag in this function.

    Возвращает разницы между временем компьютера и точным интернет временем. Точно не показывает из-за лага запроса.
    :return:
    """

    server_url = 'http://worldtimeapi.org/api/timezone/Europe/Moscow'
    """ answer:
    {"abbreviation":"MSK",
    "client_ip":"89.208.171.38",
    "datetime":"2021-07-23T16:09:32.509362+03:00",
    "day_of_week":5, "day_of_year":204,
    "dst":false, "dst_from":null, "dst_offset":0, "dst_until":null,
    "raw_offset":10800,
    "timezone":"Europe/Moscow",
    "unixtime":1627045772,
    "utc_datetime":"2021-07-23T13:09:32.509362+00:00",
    "utc_offset":"+03:00",
    "week_number":29}
    """

    from urllib.error import HTTPError
    try:
        response = urllib.request.urlopen(server_url)
    except HTTPError:
        return None
    answer = json.load(response)
    internet_dt = datetime.fromisoformat(answer['datetime'])  # здесь локальное время. Оба имеют тип datetime.datetime

    local_tz = pytz.timezone("Europe/Moscow")
    local_dt = datetime.now(local_tz)  # здесь UTC время

    seconds = (local_dt - internet_dt).total_seconds()  # in seconds with decimals
    delta = f'{seconds:.1f}'
    return delta


def get_fulltime_by_order(order):
    """
    Возвращает время, потраченное на работу (если известен номер заказа)
    :param order: string, number of order
    :return: datetime, время потраченное на заказ
    """
    try:
        obj = Timing.objects.get(order=order)
        # signatime etc. is timedelta object, `seconds` return int
        fulltime = (obj.signatime + obj.designtime + obj.packagetime).seconds
    except Timing.DoesNotExist:
        fulltime = 0
    return fulltime


def get_fulltime_by_manager(managerid, note):
    obj = Timing.objects.filter(manager_id=managerid).filter(jobnote=note)
    if obj.count() == 0:
        fulltime = 0
    elif obj.count() == 1:
        fulltime = (obj.signatime + obj.designtime + obj.packagetime).seconds
    else:
        # для каждого манагера описания работ - уникальны.
        # Если в базе больше одного - значит, что-то пошло не так в системе.
        raise Exception
    return fulltime


def get_order_info(order):
    xml_path = f'http://pim:6092/icsportal/showJDF/ICSPortal?raw=true&format=JDF&qeID={order}'
    xmlroot = etree.parse(xml_path)

    ns = "{http://www.CIP4.org/JDFSchema_1_1}"
    ns2 = {"HDM": "www.heidelberg.com/schema/HDM"}

    info = dict()

    try:
        info['jobname'] = xmlroot.getroot().attrib['DescriptiveName']
        info['manager_email'] = xmlroot.findall(f'./{ns}ResourcePool/{ns}CustomerInfo/{ns}Contact/{ns}ComChannel')[0].get(
            'Locator')
        info['manager_name'] = xmlroot.findall(f'./{ns}ResourcePool/{ns}Person')[0].get('FirstName')
        info['error'] = 'ok'
    except KeyError:
        info['error'] = 'Job not found (or another parse error)'

    return info
