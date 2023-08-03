from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('user_id', 'user_name', 'email', 'id', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ( 'user_name', 'email', 'id', 'password')}),
        ('Personal Info', {'fields': ('prof_img', 'prof_intro')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'level', 'exp')}),
        ('Important Dates', {'fields': ('last_login', 'created_date')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_name', 'email', 'id', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('user_id', 'user_name', 'email', 'id')
    ordering = ('user_id',)
    filter_horizontal = ()

# CustomUserAdmin을 등록
admin.site.register(CustomUser, CustomUserAdmin)
