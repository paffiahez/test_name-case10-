from django.contrib import admin
from .models import Event, EventRequest

@admin.register(EventRequest)
class EventRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'date', 'status', 'created_at')
    list_filter = ('status', 'event_type', 'format')
    search_fields = ('title', 'organization')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'event_type', 'format', 'org_type', 'organizer')
