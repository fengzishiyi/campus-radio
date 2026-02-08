from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from apps.accounts.models import UserProfile, InviteCode
from apps.accounts.forms import RegistrationForm, UserProfileForm, InviteCodeGenerationForm


class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.profile = UserProfile.objects.create(
            user=self.user,
            real_name='测试用户',
            student_id='2024001',
            department='broadcast',
            role='anchor'
        )
    
    def test_profile_creation(self):
        self.assertEqual(self.profile.real_name, '测试用户')
        self.assertEqual(self.profile.student_id, '2024001')
    
    def test_is_admin(self):
        self.assertFalse(self.profile.is_admin())
        self.profile.role = 'admin'
        self.assertTrue(self.profile.is_admin())
    
    def test_profile_str(self):
        self.assertIn(self.profile.real_name, str(self.profile))


class InviteCodeModelTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin', password='admin123')
        UserProfile.objects.create(
            user=self.admin,
            real_name='管理员',
            student_id='2024000',
            department='broadcast',
            role='admin'
        )
        self.code = InviteCode.objects.create(
            code='TEST123',
            created_by=self.admin
        )
    
    def test_code_creation(self):
        self.assertEqual(self.code.code, 'TEST123')
        self.assertFalse(self.code.is_used)
    
    def test_code_usage(self):
        user = User.objects.create_user(username='newuser', password='pass123')
        self.code.is_used = True
        self.code.used_by = user
        self.code.save()
        
        self.assertTrue(self.code.is_used)
        self.assertEqual(self.code.used_by, user)


class RegistrationFormTest(TestCase):
    def setUp(self):
        admin = User.objects.create_user(username='admin', password='admin123')
        UserProfile.objects.create(
            user=admin,
            real_name='管理员',
            student_id='2024000',
            department='broadcast',
            role='admin'
        )
        self.invite_code = InviteCode.objects.create(
            code='VALIDCODE',
            created_by=admin
        )
    
    def test_valid_registration(self):
        form_data = {
            'username': 'newuser',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
            'invite_code': 'VALIDCODE',
            'real_name': '新用户',
            'student_id': '2024001',
            'department': 'broadcast',
            'role': 'anchor'
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_invite_code(self):
        form_data = {
            'username': 'newuser',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
            'invite_code': 'INVALIDCODE',
            'real_name': '新用户',
            'student_id': '2024001',
            'department': 'broadcast',
            'role': 'anchor'
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('invite_code', form.errors)


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(username='admin', password='admin123')
        self.admin_profile = UserProfile.objects.create(
            user=self.admin,
            real_name='管理员',
            student_id='2024000',
            department='broadcast',
            role='admin'
        )
    
    def test_login_view(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
    
    def test_register_view(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
    
    def test_profile_view_requires_login(self):
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_profile_view_authenticated(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
    
    def test_members_list_requires_login(self):
        response = self.client.get(reverse('accounts:members'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_invite_codes_requires_admin(self):
        # Create non-admin user
        user = User.objects.create_user(username='user', password='pass123')
        UserProfile.objects.create(
            user=user,
            real_name='用户',
            student_id='2024001',
            department='broadcast',
            role='anchor'
        )
        
        self.client.login(username='user', password='pass123')
        response = self.client.get(reverse('accounts:invite_codes'))
        self.assertEqual(response.status_code, 302)  # Redirect
    
    def test_invite_codes_admin_access(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('accounts:invite_codes'))
        self.assertEqual(response.status_code, 200)


class URLTest(TestCase):
    def test_urls_resolve(self):
        self.assertEqual(reverse('accounts:login'), '/accounts/login/')
        self.assertEqual(reverse('accounts:register'), '/accounts/register/')
        self.assertEqual(reverse('accounts:logout'), '/accounts/logout/')
        self.assertEqual(reverse('accounts:profile'), '/accounts/profile/')
        self.assertEqual(reverse('accounts:members'), '/accounts/members/')
        self.assertEqual(reverse('accounts:invite_codes'), '/accounts/invite-codes/')
        self.assertEqual(reverse('accounts:generate_invite_code'), '/accounts/invite-codes/generate/')

