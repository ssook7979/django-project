 # -*- coding:utf-8 -*-
from django import template
from datetime import datetime
import math

register = template.Library()

@register.filter
def vote_percentage(value, choice_set):
    sum=0
    for choice in choice_set:
        sum += choice.votes
    if sum == 0:
        return '{0:.0%}'.format(0)
    else:
        return_value = value/sum
        return '{0:.0%}'.format(return_value)
    
@register.filter
def colorChange(x):
    if x == 1:
        color = 'w3-green'
    elif x == 2:
        color = 'w3-orange'
    elif x == 3:
        color = 'w3-red'
    elif x == 4:
        color = 'w3-blue'
    else:
        color = 'w3-tilt'
    return color
    