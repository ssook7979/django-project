# -*- coding:utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from distributed.core import error_message
from django.contrib.auth import get_user_model
from .models import Question
import re

User = get_user_model()

class PollsListForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
