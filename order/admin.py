from django.contrib import admin
from .models import *


@admin.register(OrderInfo)
class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ['oid', 'user', 'date', 'is_pay']