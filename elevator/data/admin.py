from django.contrib import admin
from .models import Wheat

#admin.site.register(Wheat)
class WheatAdmin(admin.ModelAdmin):
    list_display = ('id', 'weight', 'date')
admin.site.register(Wheat, WheatAdmin)
