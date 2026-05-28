from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User
from project.admin_site import vidyaniketan_admin_site


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('mobile_number', 'email', 'role')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('mobile_number', 'email', 'role', 'is_active', 'is_staff', 'is_superuser')


class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('mobile_number', 'email', 'role', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('mobile_number', 'email')
    ordering = ('mobile_number',)
    filter_horizontal = ()

    fieldsets = (
        (None, {'fields': ('mobile_number', 'password')}),
        ('Personal info', {'fields': ('email', 'role', 'fcm_token')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile_number', 'email', 'role', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )


# Register with custom admin site
vidyaniketan_admin_site.register(User, CustomUserAdmin)
