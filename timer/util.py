import json
import pytz
from datetime import datetime
import urllib.request


def clock_off():
    """
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
