"""
Django management command to cleanup daily songs
每日清理歌曲文件的管理命令
Run this command daily at 23:00 via cron or task scheduler
"""
import os
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.schedule.models import Song


class Command(BaseCommand):
    help = '清理今日上传的歌曲音频文件'

    def handle(self, *args, **options):
        today = timezone.now().date()
        
        # Get all songs for today that have audio files
        today_songs = Song.objects.filter(
            schedule__date=today,
            audio_file__isnull=False
        ).exclude(audio_file='')
        
        deleted_count = 0
        for song in today_songs:
            if song.audio_file:
                # Delete the actual file
                if os.path.isfile(song.audio_file.path):
                    os.remove(song.audio_file.path)
                    self.stdout.write(f'Deleted file: {song.audio_file.path}')
                
                # Clear the field
                song.audio_file = None
                song.save()
                deleted_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully cleaned up {deleted_count} audio files for {today}')
        )
