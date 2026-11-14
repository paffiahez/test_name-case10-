from django.contrib import admin

from .models import Program, ProgramNote


class ProgramNoteInline(admin.TabularInline):
    model = ProgramNote
    extra = 1


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'form', 'places', 'duration', 'price')
    search_fields = ('code', 'title')
    inlines = [ProgramNoteInline]
