from django.db import models


# Create your models here.
from django.contrib.auth.models import User


countries = (('Беларусь', 'Беларусь'),('Россия','Россия'),('Украина','Украина'))
class Person(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE,)
	
	user_pic = models.ImageField(upload_to='place_icons/', 
								blank=True, 
								verbose_name="Аватарка ", 
								default = 'place_icons/default.png')

	
	home_country =models.CharField(max_length=1000, 
								db_index=True, 
								choices=countries,
								verbose_name='Страна',
								default = countries[0])	

	home_city = models.CharField(max_length=1000, 
								db_index=True, 
								verbose_name='Город',
								default = 'Минск')

	home_street = models.CharField(max_length=1000, 
								db_index=True, 
								verbose_name='Улица',
								default = 'пр.Рокоссовского')

	home_building = models.CharField(max_length=1000, 
								db_index=True, 
								verbose_name='Дом',
								default = 1)

