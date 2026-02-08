"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        from apps.announcements.models import Announcement
        from django.db.models import Q
        from django.utils import timezone
        
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['recent_announcements'] = Announcement.objects.filter(
                Q(target_department='all') | Q(target_department=self.request.user.profile.department)
            ).filter(
                Q(expire_time__isnull=True) | Q(expire_time__gt=timezone.now())
            )[:5]
        return context

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_required(HomeView.as_view()), name='home'),
    path('accounts/', include('apps.accounts.urls')),
    path('admin/permissions/', include('apps.permissions.urls')),
    path('announcements/', include('apps.announcements.urls')),
    path('broadcast/news/', include('apps.news.urls')),
    path('broadcast/', include('apps.schedule.urls')),
    path('booking/', include('apps.booking.urls')),
    path('himalaya/', include('apps.himalaya.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
