from django.contrib import admin
from .models import Album, AudioTrack, Script


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'get_track_count', 'created_at', 'updated_at']
    list_filter = ['created_at', 'created_by']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_track_count(self, obj):
        return obj.tracks.count()
    get_track_count.short_description = '音频数量'


@admin.register(AudioTrack)
class AudioTrackAdmin(admin.ModelAdmin):
    list_display = ['title', 'album', 'audio_source', 'duration', 'order', 'play_count', 'uploaded_by', 'uploaded_at']
    list_filter = ['audio_source', 'uploaded_at', 'album']
    search_fields = ['title', 'album__title']
    readonly_fields = ['play_count', 'uploaded_at']
    ordering = ['album', 'order']
    list_select_related = ['album', 'uploaded_by']


@admin.register(Script)
class ScriptAdmin(admin.ModelAdmin):
    list_display = ['title', 'track', 'author', 'created_at', 'updated_at']
    list_filter = ['created_at', 'author']
    search_fields = ['title', 'content', 'track__title']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    list_select_related = ['track', 'author']
