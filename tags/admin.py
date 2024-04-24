from django.contrib import admin
from .models import Tag


@admin.register(Tag)
class TagAdmnin(admin.ModelAdmin):
    search_fields = ['label']