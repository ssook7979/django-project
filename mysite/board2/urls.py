from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import TemplateView
from . import views
import re

app_name = 'board2'
urlpatterns = [
    url(r'^$', views.index, name='index_default'),
    url(r'^(?P<postClass>[N|F])/(?P<page>\d+)/$', views.index, name='index'),
    url(r'^read/(?P<postClass>[N|F])/(?P<post_id>\d+)/$', views.read, name='read'),
    url(r'^read_comment_page_change/(?P<postClass>[N|F])/(?P<post_id>\d+)/(?P<comment_page>\d+)/$', views.read, name='read_comment_page_change'),
    url(r'^write/(?P<postClass>[N|F])/$', views.write, name='write'),
    url(r'^write/(?P<postClass>[N|F])/(?P<reply_to_id>\d+)/$', views.write_reply, name='write_reply'),
    url(r'^update/(?P<post_id>\d+)/$', views.update, name='update'),
    url(r'^write_comment/(?P<post_id>\d+)/$', views.write_comment, name='write_comment'),
    url(r'^write_comment_reply/(?P<comment_id>\d+)/$', views.write_comment_reply, name='write_comment_reply'),
    url(r'^delete/(?P<post_id>\d+)/$', views.delete, name='delete'),
    url(r'^delete_comment/(?P<comment_id>\d+)/$', views.delete_comment, name='delete_comment'),
    url(r'^comment_page/(?P<post_id>\d+)/$', views.comment_page, name='comment_page'),
    url(r'^comment_page/(?P<post_id>\d+)/(?P<page>\d+)/$', views.comment_page, name='comment_page_with_page'),
    url(r'^update_comment/(?P<comment_id>\d+)/$', views.update_comment, name='update_comment'),
    url(r'^success/\?next=(?P<next>.*)$', TemplateView.as_view(template_name='board2/success.html'), name='success'),
    
    url(r'^test/$', TemplateView.as_view(template_name='board2/test.html'), name='test'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
