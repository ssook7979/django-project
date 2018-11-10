# -*- coding:utf-8 -*-

from django.contrib.admin import AdminSite

class MyAdminSite(AdminSite):
    site_header = 'Django 관리'
       
admin_site = MyAdminSite(name="myadmin")

