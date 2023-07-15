from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from login.models import KitUser
from checkout.models import Product

class Login(UserAdmin):
    list_display = ('email', 'username','pk', 'is_active', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('created', 'updated')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(KitUser, Login)