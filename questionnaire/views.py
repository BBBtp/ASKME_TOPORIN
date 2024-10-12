from django.shortcuts import render

def base(request):
    return render(request, 'base.html')  # Замените 'index.html' на имя вашего шаблона

def ask(request):
    return render(request, 'ask.html')

def index(request):
    return render(request, 'index.html')

def question(request):
    return render(request, 'question.html')

def signup(request):
    return render(request, 'signup.html')

def login(request):
    return render(request, 'login.html')

def settings(request):
    return render(request, 'settings.html')

def tag(request):
    return render(request, 'tag.html')
