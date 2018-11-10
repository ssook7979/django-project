# -*- coding:utf-8 -*-

from django.contrib import admin
from .models import Question, Choice
from datetime import datetime, timedelta
from django.contrib.admin.actions import delete_selected
from templates.commons.admin import admin_site

class ChoiceInline(admin.TabularInline):
    model = Choice
    
def set_end_date(modeladmin, request, queryset):
    queryset.update(end_date=(datetime.now() + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0))
    
set_end_date.short_description = '종료일을 다음 날 자정으로 변경합니다.'
    
class AdminQuestion(admin.ModelAdmin):
    inlines = [
        ChoiceInline,
    ]
    list_display = ['question_text', 'pub_date', 'end_date']
    actions = [set_end_date, delete_selected]
    
admin_site.register(Question, AdminQuestion)
