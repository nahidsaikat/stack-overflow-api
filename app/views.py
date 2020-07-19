from django.http import JsonResponse
from django.shortcuts import render

from .helpers import get_questions, get_question_details, check_limits


def index(request, *args, **kwargs):
    identity = request.META['REMOTE_ADDR']
    result = check_limits(identity)
    if result == 'success':
        page = int(request.GET.get('page', 1))
        questions = get_questions(request)
        return render(request, 'index.html', {
            'questions': questions,
            'pre_page': page-1,
            'next_page': page+1,
        })
    else:
        return render(request, 'index.html', {'error': result})


def question_detail(request, question_id, **kwargs):
    identity = request.META['REMOTE_ADDR']
    result = check_limits(identity)
    if result == 'success':
        return JsonResponse(get_question_details(request, question_id))
    else:
        return JsonResponse({'message': result})
