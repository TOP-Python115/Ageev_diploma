from django.shortcuts import render
from .models import Wheat
from datetime import datetime
from django.db.models import Sum

def index(request):
    todey = Wheat.objects.filter(date=datetime.now()).aggregate(Sum('weight'))
    for key, value in todey.items():
        todey = value

    week = 1
    month = 2

    context = {
        'todey': todey,
        'week': week,
        'month': month,
       }

    return render(request, 'index.html', context=context)