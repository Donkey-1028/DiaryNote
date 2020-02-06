from django.contrib import admin
from .models import Diary


class DiaryAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'date', 'title', 'created', 'updated']


admin.site.register(Diary, DiaryAdmin)
# Register your models here.
