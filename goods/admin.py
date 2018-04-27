from django.contrib import admin
from .models import *


@admin.register(TypeInfo)
class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


@admin.register(GoodsInfo)
class GoodsInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'unit_price', 'unit', 'stock']
    list_per_page = 15
