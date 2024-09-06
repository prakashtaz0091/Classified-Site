from django.contrib import admin

from .models import Account, UserProfile

# from  django.contrib.auth.admin import UserAdmin
# Register your models here.


class Account_admin(admin.ModelAdmin):
    list_display = ("email", "last_login","is_active", "is_superadmin",'is_staff')
    ordering = ("-date_joined",)
    readonly_fields = ("last_login", "date_joined")
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    list_display_links = ("email", "last_login", "is_active", "is_superadmin")


admin.site.register(Account, Account_admin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "phone_number", "email_address")


admin.site.register(UserProfile, UserProfileAdmin)
