"""Admin Site"""

from django.contrib import admin

from .models import (
        User,
        JobCategory,
    )

class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email']
    list_filter = ['user_type', 'gender']


class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'created_at']


admin.site.register(User, UserAdmin)
admin.site.register(JobCategory, JobCategoryAdmin)
