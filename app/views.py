from django.shortcuts import render
from django.core.paginator import Paginator

QUESTIONS = [
    {
        'id': i,
        'title': f'Question {i}',
        'text': f'Long lorem ipsum {i}',
        'likes': i,
        'tags': [f'tag{i}', f'tag{i+1}', f'tag{i+2}']
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

TAGS = {tag for question in QUESTIONS for tag in question['tags']}

TAGS_for_base = list(TAGS)[:12]


def paginate(objects, request, per_page=10):
    paginator = Paginator(objects, per_page)
    page_number = request.GET.get('page')
    page_items = paginator.get_page(page_number)
    return page_items

def index(request):
    page = paginate(QUESTIONS, request)
    return render(request, 'index.html', {'questions': page, 'new': True, 'tags': TAGS_for_base})

def hot(request):
    page = paginate(QUESTIONS, request)
    return render(request, 'index.html', {'questions': page, 'new': False, 'tags': TAGS_for_base})

def tag(request, tag_name):
    filtered_questions = [item for item in QUESTIONS if tag_name in item['tags']]
    page = paginate(filtered_questions, request)
    return render(request, 'by_tag.html', {'questions': page, 'tag': tag_name, 'tags': TAGS_for_base})

def question(request, question_id):
    item = QUESTIONS[question_id]
    page = paginate(ANSWERS, request, per_page=5)
    return render(request, 'question.html', {'question': item, 'answers': page, 'tags': TAGS_for_base})

def settings(request):
    return render(request, 'settings.html', {'tags': TAGS_for_base})

def signup(request):
    return render(request, 'signup.html', {'tags': TAGS_for_base})

def login(request):
    return render(request, 'login.html', {'tags': TAGS_for_base})

def ask(request):
    return render(request, 'ask.html', {'tags': TAGS_for_base})
