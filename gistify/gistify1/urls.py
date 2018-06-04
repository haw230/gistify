# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 22:24:16 2018

@author: Hancheng
"""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]