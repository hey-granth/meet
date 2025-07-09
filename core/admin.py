from django.contrib import admin

from .models import Room, RoomUser


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("code", "host", "created_at")
    search_fields = ("code", "host__username")
    readonly_fields = ("code", "host", "created_at")


@admin.register(RoomUser)
class RoomUserAdmin(admin.ModelAdmin):
    list_display = ("room", "user", "joined_at")
    search_fields = ("room__code", "user__username")
    readonly_fields = ("room", "user", "joined_at")
