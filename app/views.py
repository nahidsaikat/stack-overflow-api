import requests

from django.shortcuts import render


def get_questions(request):
    page = request.GET.get('page', 1)
    url = f'https://api.stackexchange.com/2.2/questions?page={page}&pagesize=25&fromdate=1593561600&todate=1595030400&order=desc&min=1593561600&max=1595030400&sort=activity&tagged=python;c&site=stackoverflow'
    questions = requests.get(url)
    return questions.json()


def index(request, *args, **kwargs):
    page = int(request.GET.get('page', 1))
    questions = get_questions(request)
    return render(request, 'index.html', {
        'questions': questions,
        'pre_page': page-1,
        'next_page': page+1,
    })

