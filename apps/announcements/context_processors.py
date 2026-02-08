from django.utils import timezone
from .models import Announcement


def unread_announcements(request):
    """Context processor to add unread announcement count and urgent announcements to all templates"""
    if request.user.is_authenticated:
        # Get unread announcements count
        all_announcements = Announcement.objects.filter(
            target_department__in=['all', request.user.profile.department]
        ).exclude(
            read_by=request.user
        )
        
        # Filter out expired ones
        unread = all_announcements.filter(
            expire_time__isnull=True
        ) | all_announcements.filter(
            expire_time__gt=timezone.now()
        )
        
        # Get urgent announcements
        urgent = unread.filter(type='urgent', is_pinned=True)[:3]
        
        return {
            'unread_announcements_count': unread.count(),
            'urgent_announcements': urgent,
        }
    return {
        'unread_announcements_count': 0,
        'urgent_announcements': [],
    }
