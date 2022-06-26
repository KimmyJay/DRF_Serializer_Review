from django.contrib import admin

# Register your models here.
from user.models import User, UserType, HobbyUser, Hobby

admin.site.register(User)
admin.site.register(UserType)
admin.site.register(HobbyUser)
admin.site.register(Hobby)