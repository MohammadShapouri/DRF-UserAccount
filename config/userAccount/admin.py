from django.contrib import admin
from .models import UserAccount, UserAccountProfilePicture
# Register your models here.
admin.site.register(UserAccount)
admin.site.register(UserAccountProfilePicture)