import requests
import datetime
from decouple import config

from django.core.cache import cache

from .models import ClientRequestLog


def genereate_cache_key(request):
    return f"{request.GET}-{request.META['REMOTE_ADDR']}"


def get_timestamp(date_str):
    if date_str:
        return int(datetime.datetime.timestamp(datetime.datetime.strptime(date_str, "%d/%m/%Y")))
    return


def get_questions(request):
    identity = request.META['REMOTE_ADDR']
    log = ClientRequestLog.objects.create(identity=identity)
    log.save()
    page = request.GET.get('page', 1)
    fromdate = get_timestamp(request.GET.get('fromdate'))
    todate = get_timestamp(request.GET.get('todate'))
    min = get_timestamp(request.GET.get('min'))
    max = get_timestamp(request.GET.get('max'))
    tagged = request.GET.get('tagged')
    sort = request.GET.get('sort')
    order = request.GET.get('order')
    url = f'https://api.stackexchange.com/2.2/questions?page={page}&pagesize=25&site=stackoverflow'
    if fromdate:
        url += f'&fromdate={fromdate}'
    if todate:
        url += f'&todate={todate}'
    if min:
        url += f'&min={min}'
    if max:
        url += f'&max={max}'
    if tagged:
        url += f'&tagged={tagged}'
    if sort and sort != '--Sort--':
        url += f'&sort={sort}'
    if order and order != '--Order--':
        url += f'&order={order}'

    questions = None
    if cache.get(genereate_cache_key(request)):
        questions = cache.get(genereate_cache_key(request))
        if not questions.get('items'):
            questions = None
    if not questions:
        questions = requests.get(url).json()
        cache.set(genereate_cache_key(request), questions)
    return questions


def get_question_details(request, question_id):
    identity = request.META['REMOTE_ADDR']
    log = ClientRequestLog.objects.create(identity=identity)
    log.save()
    url = f'https://api.stackexchange.com/2.2/questions/{question_id}?site=stackoverflow'
    if cache.get(genereate_cache_key(request)):
        return cache.get(genereate_cache_key(request))
    question = requests.get(url).json()
    cache.set(genereate_cache_key(request), question)
    return question


def check_limits(identity):
    day_limit = int(config('LIMIT_PER_DAY', 100))
    now = datetime.datetime.now()
    day_count = ClientRequestLog.objects.filter(identity=identity, created_at__contains=now.date()).count()
    if day_count > day_limit:
        return 'Day limit exceeded'

    minute_ago = now - datetime.timedelta(seconds=60)
    minute_count = ClientRequestLog.objects.filter(identity=identity, created_at__range=(now, minute_ago)).count()
    minute_limit = int(config('LIMIT_PER_MINUTE', 5))
    if minute_count > minute_limit:
        return 'Minute limit exceeded'

    return 'success'
