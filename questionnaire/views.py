import copy
from audioop import reverse

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

QUESTIONS = [
{
    'title': f'Как установить Linux на Windows? '   + str(i),
    'id': i,
    'tag': 'Linux',
    'text': 'Я пытаюсь установить Linux через dual boot, но система не отображает загрузчик. Как это исправить? '  + str(i)
  } for i in range(52)
]

ANSWERS = [
{
    'id': i,
    'text': 'Я сначала скачивал виртуальную машину и делал все там. Попробуй это '  + str(i)
  } for i in range(5)
]

def base(request):
    return render(request, 'base.html')

def ask(request):
    return render(request, 'ask.html')

def index(request):
    page_obj = paginate_queryset(request, QUESTIONS, 5)
    return render(request, 'index.html', {'questions': page_obj.object_list, 'page_obj': page_obj})

def question(request, question_id):
    one_question = QUESTIONS[question_id]
    return render(request, 'question.html',context={'question': one_question, 'answers': ANSWERS})

def signup(request):
    return render(request, 'signup.html')

def login(request):
    return render(request, 'login.html')

def settings(request):
    return render(request, 'settings.html')

def tag(request,tag_name):
    filtered_questions = [q for q in QUESTIONS if q['tag'] == tag_name]
    page_obj = paginate_queryset(request, filtered_questions, 5)
    has_questions = filtered_questions
    return render(request, 'tag.html', {'questions': page_obj.object_list, 'page_obj': page_obj, 'tag': tag_name, 'has_questions': has_questions})

def hot(request):
    hot_questions = copy.deepcopy(QUESTIONS)
    hot_questions.reverse()
    page_obj = paginate_queryset(request, hot_questions, 5)
    return render(request, 'hot.html', {'questions': page_obj.object_list, 'page_obj': page_obj})


def paginate_queryset(request, queryset, items_per_page):
    page_number = request.GET.get('page', 1)
    paginator = Paginator(queryset, items_per_page)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # Если page_number не является целым числом, возвращаем первую страницу
        page_obj = paginator.page(1)
    except EmptyPage:
        # Если page_number больше максимального количества страниц, возвращаем последнюю страницу
        page_obj = paginator.page(paginator.num_pages)

    return page_obj
