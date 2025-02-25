from django.contrib import admin
from .models import UserAccount, UserAccountProfilePicture
from django.contrib.admin import ModelAdmin
# Register your models here.

class UserAccountAdmin(ModelAdmin):
    list_display = ('first_name', 'username', 'phone_number', 'email', 'is_account_verified', 'new_phone_number', 'is_new_phone_verified', 'creation_date', 'update_date')
    list_filter = ('is_account_verified', 'new_phone_number', 'is_new_phone_verified', 'creation_date', 'update_date')
    search_fields = ('first_name', 'username', 'phone_number', 'email')

admin.site.register(UserAccount, UserAccountAdmin)
admin.site.register(UserAccountProfilePicture)