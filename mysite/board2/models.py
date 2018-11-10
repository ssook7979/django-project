
from django.db import models
from django.utils import timezone
from datetime import datetime
from bokeh.themes import default
from members.models import CustomUser

DISPLAY = (
    ('Y','Yes'),
    ('N','No'),
)
    
class Post(models.Model):
    POST_CLASS = (
        ('F','Free'),
        ('N','Notice'),
    )
    title = models.CharField(max_length=200)
    writer = models.CharField(max_length=20)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None, blank = True,null=True)
    content = models.TextField(null=True)
    hit = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None ,  null=True, blank=True)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, blank = True,null=True)
    post_class = models.CharField(max_length=1, choices=POST_CLASS)
    list_order = models.IntegerField(default=0)
    display = models.CharField(max_length=1, choices=DISPLAY, default='Y')
    how_many_replied = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['post_class', 'display', 'list_order']

    def __str__(self):
        return str(self.title)
    
    def get_display_yes_comment_set(self):
        return self.comment_set.filter(display='Y')
 
class Comment(models.Model):
    content = models.TextField(null=True)
    writer = models.CharField(max_length=20)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None)
    list_order = models.IntegerField(default=1)
    #===
    original_comment = models.ForeignKey('self', on_delete=models.CASCADE, blank = True,null=True, related_name='original_cmnt')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, blank = True,null=True, related_name='reply_to')
    #===
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True, default=None)
    display = models.CharField(max_length=1, choices=DISPLAY, default='Y')

    class Meta:
        ordering = ['post', 'display', 'list_order', ]

    def __str__(self):
        return str(self.content)