from django import template
from apps.permissions.models import ModulePermission

register = template.Library()


@register.simple_tag
def can_edit(module_name, user):
    """Returns True/False if user can edit module"""
    try:
        module_perm = ModulePermission.objects.get(module_name=module_name, is_active=True)
        return module_perm.can_edit(user)
    except ModulePermission.DoesNotExist:
        return False


@register.simple_tag
def is_admin(user):
    """Returns True/False if user is admin"""
    if not hasattr(user, 'profile'):
        return False
    return user.profile.is_admin()
