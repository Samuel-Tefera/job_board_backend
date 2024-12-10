"""Admin Site"""

from django.contrib import admin

from .models import (
        User,
        JobCategory,
        Job,
        Application
    )


class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email']
    list_filter = ['user_type', 'gender']


class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name']


class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    list_filter = ['status', 'type', 'job_category']


class ApplicationAdmin(admin.ModelAdmin):
    list_filter = ['status']


admin.site.register(User, UserAdmin)
admin.site.register(JobCategory, JobCategoryAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Application, ApplicationAdmin)
