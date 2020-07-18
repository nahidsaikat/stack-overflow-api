import requests

from django.shortcuts import render
from django.http.response import JsonResponse


def get_questions(request):
    url = 'https://api.stackexchange.com/2.2/questions?page=1&pagesize=25&fromdate=1593561600&todate=1595030400&order=desc&min=1593561600&max=1595030400&sort=activity&tagged=python;c&site=stackoverflow'
    question_list = requests.get(url)
    return question_list.json()


def index(request, *args, **kwargs):
    return render(request, 'base.html', context={})

