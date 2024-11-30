"""Admin Site"""

from django.contrib import admin

from .models import (
        User,
        JobCategory,
    )

class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email']
    list_filter = ['user_type', 'gender']


admin.site.register(User, UserAdmin)
admin.site.register(JobCategory)
