# -*- coding:utf-8 -*-

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

class CustomUser(AbstractUser):
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(unique=True)
    uname = models.CharField(
        max_length = 20,
        null = True,
        blank = False,
        unique = True,
        error_messages = {'unique':"이미 존재하는 사용자이름 입니다."}
        )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.uname