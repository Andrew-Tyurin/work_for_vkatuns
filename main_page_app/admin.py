from django.contrib import admin

from main_page_app.models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'vacancy', 'written_username', 'written_phone')
