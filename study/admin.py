from django.contrib import admin

from study.models import Lesson, Curs


# Register your models here.
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', )

@admin.register(Curs)
class CursAdmin(admin.ModelAdmin):
    list_display = ('title', )