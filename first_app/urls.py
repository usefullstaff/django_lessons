#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.urls import path, re_path

from django.views.generic import TemplateView
from first_app.views import LogoutView, LoginFormView, UserRegistrationForm, UserProfile


urlpatterns = [
				path('', TemplateView.as_view(template_name = 'base.html')),
				path('about', TemplateView.as_view(template_name = 'template_details/body.html')),
				re_path(r'^accounts/(?P<id>\d+)$', UserProfile),
				path('accounts/logout', LogoutView.as_view()),
				path('accounts/login', LoginFormView.as_view()),
				path('accounts/registration', UserRegistrationForm.as_view()),
				]




				
#    url(r'^(?P<id>\d+)$', OwnerProfile.as_view(), name='detali'),

#    url(r'^places/(?P<slug>[-\w]+)/$', views.show_tavern, name='detali'), 
