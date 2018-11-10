# -*- coding:utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from distributed.core import error_message
import re
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()


class BoardWriteForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('title', 'content',)
        help_texts = {
            'title' : _('제목을 입력하세요'),
        }
        labels = {
            'title' : _('제목'),
            'content' : _('글내용')
        }
        
    def __init__(self, *args, **kwargs):
        super(BoardWriteForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'w3-input w3-border'
        self.fields['content'].widget.attrs['class'] = 'w3-input w3-border'

    def clean(self):
        title = self.cleaned_data['title']
        content = self.cleaned_data['content']
        
        if not title and content:
            raise ValidationError('empty', _('제목 또는 글내용을 작성해주세요.'))
        
class CommentWriteForm(forms.ModelForm):
   
    class Meta:
        model = Comment
        fields = ('content',)
        labels = {
            'content' : _(''),
        }
        widgets = { 
            'content': forms.Textarea(attrs={'class': 'w3-input w3-border w3-bar-item',
                                             'placeholder': '댓글을 입력해주세요',
                                             'style': 'width:90%; margin:0px;',
                                        }),
        }  
    
    def clean_content(self):
        content = self.cleaned_data['content']
        
        if not content:
            raise ValidationError('empty', _('댓글을 작성해주세요.'))
        return content