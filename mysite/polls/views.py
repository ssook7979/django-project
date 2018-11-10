 ##-*- coding:utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import Http404
from django.utils import timezone
from .models import Question, Choice
from django.db.models import Q

def index(request):
    new_question_list = Question.objects.filter(Q(end_date__gt=timezone.now()) | Q(end_date__isnull=True) ).order_by('-pub_date')
    old_question_list = Question.objects.filter(end_date__lt=timezone.now()).order_by('-pub_date')
    context = {
        'new_question_list': new_question_list,
        'old_question_list': old_question_list,
        }
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    if request.method == 'GET':
        question = get_object_or_404(Question, pk=question_id)
        return render(request, "polls/detail.html", {'question':question})
    else:
        return HttpResponse('not prepared yet')

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    if request.method == 'POST':
        question=get_object_or_404(Question, pk=question_id)
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except(KeyError, Choice.DoesNotExist):
            return render(request, 'polls/detail.html', { 
                'question':question,
                'error_message':'항목을 선택하지 않았습니다.',
                })
        else:
            selected_choice.votes += 1
            selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
