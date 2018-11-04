from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from first_app.models import Person

class PersonsInline(admin.StackedInline):
    model = Person
    can_delete = False



class UserAdmin(UserAdmin):
	inlines = (PersonsInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)