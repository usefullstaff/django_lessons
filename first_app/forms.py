#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms


COUNTRIES = (('Беларусь','Беларусь'),('Россия','Россия'),('Украина','Украина'))


class LocForm(forms.Form):
	country = forms.TypedChoiceField(label='Выберите страну', choices=COUNTRIES)
	city = forms.CharField(label='City', max_length=100)
	street = forms.CharField(label='Street', max_length=100)
	building = forms.CharField(label='Building', max_length=100)





