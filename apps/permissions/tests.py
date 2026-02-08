from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from apps.accounts.models import UserProfile
from apps.permissions.models import ModulePermission
from apps.permissions.decorators import module_permission_required, admin_required
from apps.permissions.templatetags.perm_tags import can_edit, is_admin


class ModulePermissionTestCase(TestCase):
    """Test ModulePermission model"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.profile = UserProfile.objects.create(
            user=self.user,
            real_name='Test User',
            student_id='123456',
            department='broadcast',
            role='anchor'
        )
        self.module = ModulePermission.objects.create(
            module_name='test_module',
            module_label='Test Module',
            allowed_roles=['admin', 'anchor'],
            is_active=True
        )
    
    def test_can_edit_with_permission(self):
        """Test user with permission can edit"""
        self.assertTrue(self.module.can_edit(self.user))
    
    def test_can_edit_without_permission(self):
        """Test user without permission cannot edit"""
        self.profile.role = 'himalaya'
        self.profile.save()
        self.assertFalse(self.module.can_edit(self.user))


class DecoratorTestCase(TestCase):
    """Test permission decorators"""
    
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.profile = UserProfile.objects.create(
            user=self.user,
            real_name='Test User',
            student_id='123456',
            department='broadcast',
            role='admin'
        )
        ModulePermission.objects.create(
            module_name='test_module',
            module_label='Test Module',
            allowed_roles=['admin'],
            is_active=True
        )
    
    def test_admin_required_decorator(self):
        """Test admin_required decorator"""
        @admin_required
        def test_view(request):
            return 'success'
        
        request = self.factory.get('/test/')
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        result = test_view(request)
        self.assertEqual(result, 'success')
    
    def test_module_permission_required_decorator(self):
        """Test module_permission_required decorator"""
        @module_permission_required('test_module')
        def test_view(request):
            return 'success'
        
        request = self.factory.get('/test/')
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        result = test_view(request)
        self.assertEqual(result, 'success')


class TemplateTagTestCase(TestCase):
    """Test template tags"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.profile = UserProfile.objects.create(
            user=self.user,
            real_name='Test User',
            student_id='123456',
            department='broadcast',
            role='admin'
        )
        ModulePermission.objects.create(
            module_name='test_module',
            module_label='Test Module',
            allowed_roles=['admin'],
            is_active=True
        )
    
    def test_can_edit_tag(self):
        """Test can_edit template tag"""
        self.assertTrue(can_edit('test_module', self.user))
    
    def test_is_admin_tag(self):
        """Test is_admin template tag"""
        self.assertTrue(is_admin(self.user))


class DefaultPermissionsTestCase(TestCase):
    """Test default permissions created by migration"""
    
    def test_default_permissions_exist(self):
        """Test all default module permissions were created"""
        expected_modules = ['news', 'schedule', 'booking', 'himalaya', 'announcements', 'groups', 'user_management']
        
        for module_name in expected_modules:
            self.assertTrue(
                ModulePermission.objects.filter(module_name=module_name).exists(),
                f'Module {module_name} should exist'
            )
    
    def test_default_permissions_values(self):
        """Test default permissions have correct allowed_roles"""
        permissions = {
            'news': ['admin', 'anchor'],
            'schedule': ['admin', 'anchor'],
            'booking': ['admin', 'anchor', 'himalaya'],
            'himalaya': ['admin', 'himalaya'],
            'announcements': ['admin'],
            'groups': ['admin'],
            'user_management': ['admin'],
        }
        
        for module_name, expected_roles in permissions.items():
            module = ModulePermission.objects.get(module_name=module_name)
            self.assertEqual(
                module.allowed_roles,
                expected_roles,
                f'Module {module_name} should have roles {expected_roles}'
            )

