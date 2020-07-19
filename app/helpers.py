import requests
import datetime
from decouple import config

from django.core.cache import cache

from .models import ClientRequestLog


def genereate_cache_key(request):
    return 'cache'


def get_questions(request):
    identity = request.META['REMOTE_ADDR']
    log = ClientRequestLog.objects.create(identity=identity)
    log.save()
    page = request.GET.get('page', 1)
    url = f'https://api.stackexchange.com/2.2/questions?page={page}&pagesize=25&fromdate=1593561600&todate=1595030400&order=desc&min=1593561600&max=1595030400&sort=activity&tagged=python;c&site=stackoverflow'
    if cache.get(genereate_cache_key(request)):
        return cache.get(genereate_cache_key(request))
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
