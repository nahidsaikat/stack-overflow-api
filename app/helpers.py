import requests


def get_questions(request):
    page = request.GET.get('page', 1)
    url = f'https://api.stackexchange.com/2.2/questions?page={page}&pagesize=25&fromdate=1593561600&todate=1595030400&order=desc&min=1593561600&max=1595030400&sort=activity&tagged=python;c&site=stackoverflow'
    questions = requests.get(url)
    return questions.json()


def get_question_details(question_id):
    url = f'https://api.stackexchange.com/2.2/questions/{question_id}?site=stackoverflow'
    questions = requests.get(url)
    return questions.json()
