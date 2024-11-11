from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Question, Answer, Tag

def base(request):
    return render(request, 'base.html')

def ask(request):
    return render(request, 'ask.html')

def index(request):
    questions = Question.objects.get_new_questions()
    page_obj = paginate_queryset(request, questions, 5)
    return render(request, 'index.html', {'questions': page_obj.object_list, 'page_obj': page_obj})

def question(request, question_id):
    one_question = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.filter(question=one_question).order_by('-created_at')
    return render(request, 'question.html', {'question': one_question, 'answers': answers})

def signup(request):
    return render(request, 'signup.html')

def login(request):
    return render(request, 'login.html')

def settings(request):
    return render(request, 'settings.html')

def tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    filtered_questions = tag.questions.all().order_by('-created_at')
    page_obj = paginate_queryset(request, filtered_questions, 5)
    return render(request, 'tag.html', {'questions': page_obj.object_list, 'page_obj': page_obj, 'tag': tag})

def hot(request):
    hot_questions = Question.objects.get_hot_questions()
    page_obj = paginate_queryset(request, hot_questions, 5)
    return render(request, 'hot.html', {'questions': page_obj.object_list, 'page_obj': page_obj})

def paginate_queryset(request, queryset, items_per_page):
    page_number = request.GET.get('page', 1)
    paginator = Paginator(queryset, items_per_page)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return page_obj
