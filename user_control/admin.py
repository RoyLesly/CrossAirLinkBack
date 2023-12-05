from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

class CustomUserAdminConfig(UserAdmin):
    model = CustomUser
    list_display = ('username', 'id', 'custom_groups', 'last_login', 'is_active', 'is_staff', 'is_superuser',)
    search_fields = ('username')
    list_filter = ('username', 'is_active', 'is_staff', 'is_superuser', 'is_admin')
    ordering = ('id',)
    exclude = ('date_joined', )

# admin.site.register(CustomUser, CustomUserAdminConfig)
admin.site.register(( CustomUser, UserProfile, UserActivities, ))
