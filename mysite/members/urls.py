from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from django.conf import settings 
from .forms import CustomAuthenticationForm, CustomUserCreationForm, CustomPasswordChangeForm
from . import views
import re


app_name = 'members'
urlpatterns = [
    #url(r'^signup/$', TemplateView.as_view(template_name='members/signup.html', extra_context={'form': CustomUserCreationForm}), name='signup'),
    #member managements
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    #warning page
    url(r'^login_necessary/$', TemplateView.as_view(template_name='members/login_necessary.html'), name='login_necessary'),
    #token and email
    url(r'^send_email/$', TemplateView.as_view(template_name='members/send_email.html'), name='send_email'),
    url(r'^send_email_again/$', views.send_email_again, name='send_email_again'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    #password reset
    #user change
    url(r'^user_change/$', views.user_change, name='user_change'),
    url(r'^password_change/$', views.password_change, name='password_change'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)