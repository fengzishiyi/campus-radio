# Generated migration for adding is_live and audio_file fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyschedule',
            name='is_live',
            field=models.BooleanField(default=False, help_text='16:00-18:00直播标记', verbose_name='是否直播'),
        ),
        migrations.AddField(
            model_name='song',
            name='audio_file',
            field=models.FileField(blank=True, help_text='上传的MP3等音频文件', null=True, upload_to='daily_songs/%Y/%m/%d/', verbose_name='音频文件'),
        ),
    ]
