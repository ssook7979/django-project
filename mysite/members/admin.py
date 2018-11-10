#-*- coding:utf-8 -*-
from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from templates.commons.admin import admin_site

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    
    fieldsets = [
        ('개인정보', {'fields': ['email', 'uname']}),
        ('시간정보', {'fields': ['last_login', 'date_joined']}),
        ('회원등급', {'fields': ['is_superuser', 'is_staff', 'is_active']}),
    ]
    
    list_display = ('email','uname','is_staff','is_active',) #to control which fields are displayed on the change list page of the admin.
    ordering = ['is_superuser', 'is_staff','is_active',]              #specify how lists of objects should be ordered in the Django admin views

admin_site.register(CustomUser, CustomUserAdmin)
