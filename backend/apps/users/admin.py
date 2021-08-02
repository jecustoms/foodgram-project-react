from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'first_name',
                    'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('username', 'email')
    readonly_fields = ('date_joined', 'last_login')

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': ('is_active',
                       'is_staff', 'is_superuser', 'groups'),
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'username',
         'first_name', 'last_name', 'password1', 'password2')}),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()
        if not is_superuser:
            disabled_fields |= {
                'username',
                'is_superuser',
                'user_permissions',
            }
        if (
            not is_superuser
            and obj is not None
            and (obj.is_superuser or obj == request.user)
        ):
            disabled_fields |= {
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            }
        for field in disabled_fields:
            if field in form.base_fields:
                form.base_fields[field].disabled = True
        return form
