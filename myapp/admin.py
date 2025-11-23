from django.contrib import admin
from .models import Participant, CleanupEvent, CleanupRegistration, Activity

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'username', 'address', 'birthdate', 'contact_number', 'email', 'registered_at')
    search_fields = ('fullname', 'username', 'contact_number', 'email')
    list_filter = ('address',)


@admin.register(CleanupEvent)
class CleanupEventAdmin(admin.ModelAdmin):
    list_display = ("name", "place", "specific_location", "date", "start_time", "duration", "points", "is_active")
    list_filter = ("place", "date", "is_active")
    search_fields = ("title", "specific_location")


@admin.register(CleanupRegistration)
class CleanupRegistrationAdmin(admin.ModelAdmin):
    list_display = ("participant", "event", "registered_at", "attended", "points_awarded")
    list_filter = ("attended", "points_awarded")
    search_fields = ("participant__name", "event__title")


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("participant", "cleanup_type", "points_earned", "date_participated")
    list_filter = ("cleanup_type",)
    search_fields = ("participant__name",)
