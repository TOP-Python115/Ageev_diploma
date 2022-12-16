# ИСПОЛЬЗОВАТЬ: импорты эффективно визуально разбивать на три категории: внешние пакеты, стандартная библиотека, локальные — при этом внутри каждой категории осуществлять сортировку по алфавиту
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.db.models.aggregates import Sum
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from datetime import datetime

from .models import Wheat


# https://django.fun/ru/docs/django/4.1/topics/auth/default/#limiting-access-to-logged-in-users-that-pass-a-test
# ИСПОЛЬЗОВАТЬ: тесты на принадлежность пользователя к группе
def _is_foreman(user: User):
    return user.groups.filter(name='weigher_foreman').exists()

def _is_master(user: User):
    return user.groups.filter(name='elevator_master').exists()

def _is_director(user: User):
    return user.groups.filter(name='gen_director').exists()


@login_required
def index(request):
    # ПЕРЕИМЕНОВАТЬ: очень просится другое имя вместо ничего не значащего query_set
    query_set = Group.objects.filter(user=request.user)
    for g in query_set:
        query_set = g

    context = {
        'query_set': query_set
    }
    return render(request, 'index.html', context=context)


# ИСПОЛЬЗОВАТЬ: декоратор прохождения нужных тестов
@user_passes_test(lambda user: any([_is_foreman(user), _is_master(user), _is_director(user)]))
@login_required
def today_open(request):
    today = Wheat.objects.filter(date=datetime.now())\
                         .aggregate(Sum('weight'))
    for key, value in today.items():
        if value == None:
            today = 0
        else:
            today = format(value, '.2f')
        # КОММЕНТАРИЙ: здесь есть проблема в том, что вы сначала получаете данные, и только потом проверяете, а может ли пользователь получить эти данные — это потенциальная уязвимость и  — см. решение выше или используйте объекты Permission (предпочтительнее)
        query_set = Group.objects.filter(user=request.user)
        # УДАЛИТЬ: когда отработал декоратор, мы уже точно знаем, что пользователь относится к какой-то группе, следовательно можем сразу получить единственный объект группы из выборки выше с помощью замыкающего метода get() без аргументов — а этот цикл без надобности
        for g in query_set:
            query_set = str(g)

    context = {
        'today': today,
        'query_set': query_set,
    }
    return render(request, 'data/today_open.html', context=context)


@user_passes_test(lambda user: any([_is_master(user), _is_director(user)]))
@login_required
def week_open(request):
    day = datetime.now()
    weekk = day.strftime("%V")
    week = Wheat.objects.filter(date__week=weekk).aggregate(Sum('weight'))
    for key, value in week.items():
        # ИСПРАВИТЬ: None — это один встроенный объект: когда в какую либо переменную или поле записывается None — это записывается ссылка на тот самый единственный встроенный объект None — поэтому проверку производят с помощью оператора is (корректнее и быстрее)
        if value == None:
            week = 0
        else:
            # ИСПОЛЬЗОВАТЬ: f-строки быстрее, чем функция/метод format()
            week = f'{value:.2f}'
    query_set = Group.objects.filter(user=request.user)
    for g in query_set:
        query_set = str(g)

    context = {
        'week': week,
        'query_set': query_set
    }
    return render(request, 'data/week_open.html', context=context)


@user_passes_test(_is_director)
@login_required
def month_open(request):
    day = datetime.now()
    month = Wheat.objects.filter(date__year=day.year).aggregate(Sum('weight'))
    for key, value in month.items():
        if value == None:
            month = 0
        else:
            month = format(value, '.2f')
    query_set = Group.objects.filter(user=request.user)
    for g in query_set:
        query_set = str(g)

    context = {
        'month': month,
        'query_set': query_set,
    }
    return render(request, 'data/month_open.html', context=context)


class WheatCreate(PermissionRequiredMixin, CreateView):
    # КОММЕНТАРИЙ: а ещё, совершенно верно, есть система разрешений, которые можно назначать группам — это работает не только в CBV, но и в FBV
    permission_required = 'data.add_wheat'
    model = Wheat
    fields = ['weight']
    success_url = reverse_lazy('index')

    # ДОБАВИТЬ: передачу контекста в CBV

