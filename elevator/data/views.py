from django.shortcuts import render
from .models import Wheat
from datetime import datetime

def index(request):
    todey = Wheat.objects.filter(date=datetime.now()).count()
    week = 1
    month = 2

    context = {
        'todey': todey,
        'week': week,
        'month': month,
       }

    return render(request, 'index.html', context=context)