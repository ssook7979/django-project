# -*- coding:utf-8 -*-

from django.views.generic.base import TemplateView
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Max, Min, F, Q
from .forms import BoardWriteForm, CommentWriteForm
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.urls import reverse
import math, re, json
from django.http.response import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from django.utils import timezone
from file.models import File

NUMBER_OF_COMMENT_PER_PAGE = 20
NUMBER_OF_POST_PER_PAGE = 15
NUMBER_OF_PAGE = 5


def page_divinator(paginator, page):
    first_page = (math.ceil(page / NUMBER_OF_PAGE) - 1) * NUMBER_OF_PAGE
    return paginator.page_range[first_page : first_page + NUMBER_OF_PAGE]  


def index(request, postClass='F', page=1):
    post_list = Post.objects.filter(post_class__exact=postClass, display__exact='Y',).order_by('list_order')
    search = request.GET.get('search', None)
    option = request.GET.get('option', None)
    
    if search:
        if option == '제목 + 내용':
            post_list = post_list.filter(Q(title__contains=search) | Q(content__contains=search))
        elif option == '제목만':
            post_list = post_list.filter(title__contains=search)
        else:
            post_list = post_list.filter(writer__contains=search)

    paginator = Paginator(post_list, NUMBER_OF_POST_PER_PAGE)
    
    posts = paginator.get_page(page)
    totalPage = paginator.num_pages
    
    page_list = page_divinator(paginator, int(page))
    
    context = {
        'posts' : posts,
        'postClass' : postClass,
        'post_list' : post_list,
        'page_list' : page_list,
        'page' : int(page),
        'paginator' : paginator,
        'search' : search,
        'option' : option,
    }
    return render(request, 'board2/index.html', context)


def read(request, postClass, post_id=1, comment_page=None):
    post = Post.objects.get(post_class__exact=postClass, id=int(post_id))
    if post.display == 'N':
        return redirect('wrong_path')
    else:
        post.hit = post.hit + 1
        post.save()   
        
        form = CommentWriteForm()
        comment_list = post.comment_set.filter(display="Y") 
        paginator = Paginator(comment_list, NUMBER_OF_COMMENT_PER_PAGE)
        file_list = post.file_set.all()
        
        if not comment_page:
            comment_page = paginator.num_pages
        
        comments = paginator.get_page(comment_page)
        page_list = page_divinator(paginator, int(comment_page))
        
        context = {
                   'post' : post,
                   'form' : form,
                   'comments' : comments,
                   'page' : comment_page,
                   'page_list' : page_list,
                   'paginator' : paginator,
                   'NUMBER_OF_POST_PER_PAGE' : NUMBER_OF_POST_PER_PAGE,
                   'file_list' : file_list,
                   }
        return render(request, 'board2/read.html', context)


@login_required
def write(request, postClass):
        
    if request.method == 'POST':
        form = BoardWriteForm(request.POST)
        if form.is_valid():
            post = form.save()
            try:
                Post.objects.filter(display='Y').update(list_order=F('list_order') + 1)
            except ValueError:
                pass
            
            if postClass == 'N' and request.user.is_staff:
                writer = '관리자'
            else:
                writer = request.user.uname
                
            post.post_class = postClass
            post.list_order = 1
            post.writer = writer
            post.owner = request.user
            post.save()
            
            file_list = File.objects.filter(owner=request.user, on_writing='Y')
            
            if file_list.count() != 0:
                file_list.update(on_writing='N', post=post)
                
            return redirect('board2:success', next=reverse('board2:read', kwargs={'postClass':post.post_class, 'post_id':post.id}))

    else:
        form = BoardWriteForm()
        file_list = File.objects.filter(owner=request.user, on_writing='Y')
        
    context = {
                'form' : form,
                'postClass' : postClass,
                'file_list' : file_list,
               }
    return render(request, 'board2/write.html', context)

    
@login_required
def write_reply(request, postClass, reply_to_id):
    try:
        reply_to = Post.objects.get(id=reply_to_id)
    except(KeyError):
        return redirect('wrong_path')
    
    if reply_to.display == 'N':
        return redirect('board2:index')
    else:
        if request.method == 'POST':
            reply_exist = Post.objects.filter(reply__exact=reply_to, display='Y', how_many_replied__exact=reply_to.how_many_replied + 1)
            if reply_exist:
                list_order_for_post = reply_exist.aggregate(Max('list_order')).get('list_order__max') + 1
            else:
                list_order_for_post = reply_to.list_order + 1
            
            Post.objects.filter(list_order__gte=list_order_for_post, display='Y').update(list_order=F('list_order') + 1)           
            post = Post(title=request.POST['title'],
                        content=request.POST['content'],
                        post_class=postClass,
                        list_order=list_order_for_post,
                        writer=request.user.uname,
                        owner=request.user,
                        reply=reply_to
                    )
            
            post.how_many_replied = reply_to.how_many_replied + 1
            post.save()
            
            file_list = File.objects.filter(owner=request.user, on_writing='Y')
            
            if file_list.count() != 0:
                file_list.update(on_writing='N', post=post)
            return redirect('board2:success', next=reverse('board2:read', kwargs={'postClass':post.post_class, 'post_id':post.id}))
        
        else:
            data = {'title': 'Re:' + reply_to.title, 'content': '원글내용' + '=' * 20 + '\n' + reply_to.content, }
            form = BoardWriteForm(initial=data)
            file_list = File.objects.filter(owner=request.user, on_writing='Y')
            
            context = {
                        'form' : form,
                        'postClass' : postClass,
                        'reply_to_id' : reply_to_id,
                        'file_list' : file_list,
                       }
            return render(request, 'board2/write.html', context)
            

@login_required
def delete(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return HttpResponseRedirect(reverse('wrong_path'))
    else:
        if post.owner == request.user:
            
            Post.objects.filter(display='N', post_class=post.post_class).update(list_order=F('list_order') + 1)
                
            post.display = 'N'
            post.list_order = 1
            post.save()
            
            Post.objects.filter(display='Y', post_class=post.post_class).update(list_order=F('list_order') - 1)
            return redirect('board2:index', postClass=post.post_class, page=math.ceil(post.list_order / 15))
        else:
            return redirect("wrong_path")

        
@login_required
def write_comment(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return redirect("wrong_path")
    
    if request.method == "POST":
        form = CommentWriteForm(request.POST)
        if form.is_valid():
            try:
                new_list_order = post.comment_set.filter(display__exact='Y').aggregate(Max('list_order')).get('list_order__max') + 1
            except TypeError:
                new_list_order = 1
            post.comment_set.create(
                content=form.cleaned_data['content'],
                writer=request.user.uname,
                owner=request.user,
                post=post,
                list_order=new_list_order,
            )
            
            new_comment_list = post.comment_set.filter(display__exact='Y')

            data = {'success' : True,}
            return JsonResponse(data)
        
        else:
            return redirect("wrong_path")
    else:
        return redirect('wrong_path')

    
@login_required
def write_comment_reply(request, comment_id):
    if request.method == 'POST':
        form = CommentWriteForm(request.POST)
        try:
            target_comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return HttpResponseRedirect(reverse('wrong_path'))
        
        if form.is_valid():
            is_parent_comment = target_comment.original_comment
            
            if is_parent_comment:
                original_comment = is_parent_comment
            else:
                original_comment = target_comment
            
            try:
                new_list_order = Comment.objects.filter(original_comment=original_comment, display='Y').aggregate(Max('list_order')).get('list_order__max') + 1
            except TypeError:
                new_list_order = original_comment.list_order + 1
                   
            Comment.objects.filter(list_order__gte=new_list_order, display='Y').update(list_order=F('list_order') + 1)
            
            comment = Comment(
                content=form.cleaned_data['content'],
                writer=request.user.uname,
                owner=request.user,
                post=target_comment.post,
                list_order=new_list_order,
                original_comment=original_comment,
                reply=target_comment,
            )
            comment.save()
            data = {'success' : True,}
            return JsonResponse(data)
        else:
            return redirect("wrong_path")
    else:
        form = CommentWriteForm()
        context = {
            'form' : form,
            'comment_id' : comment_id,
            'type' : 'reply',
        }
        return render(request, 'board2/comment_form.html', context)

    
@login_required
def delete_comment(request, comment_id):
    try:
        target_comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return redirect('wrong_path')
    
    delete_list_order = 1
        
    Comment.objects.filter(display='N').update(list_order=F('list_order') + 1)

    target_comment.display = 'N'
    target_comment.list_order = 1
    target_comment.save()
    
    data = {'success' : True,}

    return JsonResponse(data)


def comment_page(request, post_id, page=None):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return redirect('wrong_path')
    
    comment_list = post.comment_set.filter(display="Y")
    paginator = Paginator(comment_list, NUMBER_OF_COMMENT_PER_PAGE)
    
    if not page:
        page = paginator.num_pages

    comments = paginator.get_page(page)
    page_list = page_divinator(paginator, int(page))
    
    context = {
               'post' : post,
               'comments' : comments,
               'page' : page,
               'page_list' : page_list,
               'paginator' : paginator,
               'post_id' : post_id,
               'form' : CommentWriteForm(),
               }
    return render(request, 'board2/comment_page.html', context)

        
@login_required
def update(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return HttpResponseRedirect(reverse('wrong_path'))
    
    if request.method == 'POST':
        if request.user == post.owner:
            post.title = request.POST['title']
            post.content = request.POST['content']
            post.updated_at = timezone.now()
            post.save()
            return redirect('board2:success', next=reverse('board2:read', kwargs={'postClass':post.post_class, 'post_id':post.id}))
        else:
            return redirect('wrong_path')
    else:
        data = {
            'title' : post.title,
            'content' : post.content,
        }
        form = BoardWriteForm(initial=data)
        
        context = {
            'form' : form,
            'postClass' : post.post_class,
            'post_id' : post_id,
        }
        return render(request, 'board2/write.html', context)

    
def update_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return redirect('wrong_path')
    
    if request.method == 'POST':
        if request.user == comment.owner:
            comment.content = request.POST['content']
            comment.updated_at = timezone.now()
            comment.save()
                
            data = {'success' : True,}
            return JsonResponse(data)
        else:
            return redirect('wrong_path')
    else:
        form = CommentWriteForm(initial={'content' : comment.content, })      
        context = {
            'form' : form,
            'type' : 'update',
            'comment_id' : comment_id,
        }
        return render(request, 'board2/comment_form.html', context)
