
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse, request
from django.shortcuts import render
from .models import Wheat
from datetime import datetime
from django.db.models import Sum

from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .models import Wheat
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import Group



@login_required
def index(request):
    query_set = Group.objects.filter(user=request.user)
    for g in query_set:
        query_set = g

    context = {
        'query_set': query_set
    }
    return render(request, 'index.html',context=context)
@login_required
def today_open(request):
    today = Wheat.objects.filter(date=datetime.now()).aggregate(Sum('weight'))

    for key, value in today.items():
        if value == None:
              today = 0
        else:
              today = format(value, '.2f')
        query_set = Group.objects.filter(user=request.user)
        for g in query_set:
            query_set = str(g)
    context = {
        'today': today,
        'query_set': query_set,
        }
    return render(request, 'data/today_open.html', context=context)
@login_required
def week_open(request):
    day = datetime.now()
    weekk = day.strftime("%V")
    week = Wheat.objects.filter(date__week=weekk).aggregate(Sum('weight'))
    for key, value in week.items():
        if value == None:
            week = 0
        else:
            week = format(value, '.2f')
    query_set = Group.objects.filter(user=request.user)
    for g in query_set:
        query_set = str(g)

    context = {
        'week': week,
        'query_set': query_set

    }
    return render(request, 'data/week_open.html', context=context)
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
    permission_required = 'data.add_wheat'
    model = Wheat
    fields = ['weight']
    success_url = reverse_lazy('index')




