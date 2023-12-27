from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.core.paginator import Paginator
from django.urls import reverse

from app.forms import LoginForm, SignUpForm, AskForm
from app.models import *

from django.shortcuts import redirect

QUESTIONS = [
    {
        'id': i,
        'title': f'Question {i}',
        'text': f'Long lorem ipsum {i}',
        'likes': i,
        'tags': [f'tag{i}', f'tag{i + 1}', f'tag{i + 2}']
    } for i in range(30)
]

ANSWERS = [
    {
        'id': i,
        'text': f'Not long answer lorem ipsum {i}',
        'correct': False,
        'likes': i
    } for i in range(30)
]

TAGS = Tags.objects.all()
TAGS_for_base = list(TAGS)[:12]


def paginate(objects, request, per_page=10):
    paginator = Paginator(objects, per_page)
    page_number = request.GET.get('page')
    page_items = paginator.get_page(page_number)
    return page_items


def index(request):
    page = paginate(Questions.new_questions.all(), request)
    return render(request, 'index.html', {'questions': page, 'new': True, 'tags': TAGS_for_base})


def hot(request):
    page = paginate(Questions.hot_questions.all(), request)
    return render(request, 'index.html', {'questions': page, 'new': False, 'tags': TAGS_for_base})


def tag(request, tag_name):
    filtered_questions = Questions.new_questions.filter(tags=Tags.objects.get(name=tag_name))
    page = paginate(filtered_questions, request)
    return render(request, 'by_tag.html', {'questions': page, 'tag': tag_name, 'tags': TAGS_for_base})


def question(request, question_id):
    item = Questions.new_questions.get(id=question_id)
    print(item.tags.all())
    page = paginate(Answers.objects.filter(question=question_id), request, per_page=5)
    return render(request, 'question.html', {'question': item, 'answers': page, 'tags': TAGS_for_base})


def settings(request):
    return render(request, 'settings.html', {'tags': TAGS_for_base})

#
def signup(request):
    if request.method == "GET":
        register_form = SignUpForm()
    elif request.method == "POST":
        register_form = SignUpForm(request.POST)
        if register_form.is_valid():
            user = new_user(request.POST)
            user_info = {'username': user.username, 'password': request.POST['password'], 'first_name': user.first_name}
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                user = auth.authenticate(request=request, **login_form.cleaned_data)
                if user:
                    login(request, user)
                    return redirect(reverse('index'))

    return render(request, 'signup.html', context={'tags': TAGS_for_base, 'form': register_form})


def log_out(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER'))


def log_in(request):
    if request.method == "GET":
        print(request.GET)
        login_form = LoginForm()

    elif request.method == 'POST':
        print(request.POST)
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            if user is not None:
                login(request, user)
                return redirect(reverse('index'))
            else:
                login_form.add_error(None, "Invalid username or password")
    return render(request, 'login.html', {'tags': TAGS_for_base, 'form': login_form})

def ask(request):
    if request.method == 'GET':
        ask_form = AskForm()
    elif request.method == 'POST':
        print(request.POST)
        print(request.user)
        ask_form = AskForm(request.POST)
        if ask_form.is_valid():
            new_quest = new_question(new_quest=request.POST, user=request.user)
            return redirect(reverse('question',args=(new_quest,)))
    return render(request, 'ask.html', context={'tags': TAGS_for_base, 'form': ask_form})
