from django.http import JsonResponse
from django.shortcuts import render

from .helpers import get_questions, get_question_details


def index(request, *args, **kwargs):
    page = int(request.GET.get('page', 1))
    questions = get_questions(request)
    return render(request, 'index.html', {
        'questions': questions,
        'pre_page': page-1,
        'next_page': page+1,
    })


def question_detail(request, question_id, **kwargs):
    return JsonResponse(get_question_details(question_id))
