from django.contrib import admin
from .models import OTPCode, OTPTypeSetting
# Register your models here.

class OTPCodeAdmin(admin.ModelAdmin):
    list_display = ('otp_code', 'otp_usage', 'otp_type_setting', 'otp_creation_date', 'last_attempt', 'attempt_counter')
    list_filter = ('otp_usage', 'otp_type_setting', 'otp_creation_date', 'last_attempt', 'attempt_counter')
    search_fields = ('otp_code', 'otp_usage', 'otp_type_setting')

class OTPTypeSettingAdmin(admin.ModelAdmin):
    list_display = ('otp_type', 'max_attempt_count', 'expire_after', 'creation_date', 'update_date')

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj = None):
        return False


admin.site.register(OTPCode, OTPCodeAdmin)
admin.site.register(OTPTypeSetting, OTPTypeSettingAdmin)
