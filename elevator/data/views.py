from django.http import HttpResponse
from django.shortcuts import render
from .models import Wheat
from datetime import datetime
from django.db.models import Sum

from django.views.generic.edit import CreateView, FormView
from django.urls import reverse_lazy

from .models import Wheat
from django.contrib.auth.decorators import login_required

@login_required
def index(request):

    return render(request, 'index.html',)

def today_open(request):

    today = Wheat.objects.filter(date=datetime.now()).aggregate(Sum('weight'))
    for key, value in today.items():
        today = value

    context = {
        'today': today
    }
    return render(request, 'data/today_open.html', context=context)

def week_open(request):
    week = 1
    context = {
        'week': week
    }
    return render(request, 'data/week_open.html', context=context)

def month_open(request):
    month = 2
    context = {
        'month': month
    }
    return render(request, 'data/month_open.html', context=context)

class WheatCreate(CreateView):
    model = Wheat
    fields = ['weight']
    success_url = reverse_lazy('index')



