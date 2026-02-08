from django.contrib import admin
from .models import Group, DailySchedule, Program, Song


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'weekday', 'get_weekday_display', 'leader', 'member_count']
    list_filter = ['weekday']
    search_fields = ['name']
    filter_horizontal = ['members']
    
    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = '组员数量'


@admin.register(DailySchedule)
class DailyScheduleAdmin(admin.ModelAdmin):
    list_display = ['date', 'anchor_count', 'program_count', 'song_count', 'created_by', 'created_at']
    list_filter = ['date', 'created_at']
    search_fields = ['date']
    filter_horizontal = ['anchors']
    date_hierarchy = 'date'
    
    def anchor_count(self, obj):
        return obj.anchors.count()
    anchor_count.short_description = '播音员数量'
    
    def program_count(self, obj):
        return obj.programs.count()
    program_count.short_description = '节目数量'
    
    def song_count(self, obj):
        return obj.songs.count()
    song_count.short_description = '歌曲数量'


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'schedule', 'time_slot', 'order']
    list_filter = ['schedule__date']
    search_fields = ['name', 'time_slot']
    ordering = ['schedule__date', 'order', 'time_slot']


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'schedule', 'order']
    list_filter = ['schedule__date']
    search_fields = ['title', 'artist']
    ordering = ['schedule__date', 'order', 'title']

