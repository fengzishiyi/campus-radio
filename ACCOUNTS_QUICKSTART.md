# Accounts App Quick Start Guide

## Initial Setup

### 1. Create Superuser (First Time Setup)
```bash
python manage.py createsuperuser
```

### 2. Create Admin Profile (Django Shell)
```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from apps.accounts.models import UserProfile

# Get the superuser
admin = User.objects.get(username='your_username')

# Create profile
UserProfile.objects.create(
    user=admin,
    real_name='管理员姓名',
    student_id='2024001',
    department='broadcast',  # or 'himalaya' or 'both'
    role='admin',
    phone='13800138000',  # optional
    wechat='wechat_id'     # optional
)
```

### 3. Generate Invite Codes

**Option A: Via Admin Interface**
1. Go to http://localhost:8000/admin/
2. Navigate to Accounts → Invite Codes
3. Click "Add Invite Code"
4. Enter a code and select yourself as creator

**Option B: Via Web Interface**
1. Login as admin
2. Go to http://localhost:8000/accounts/invite-codes/
3. Click "生成邀请码" button
4. Enter number of codes to generate (1-100)

**Option C: Via Django Shell**
```python
from django.contrib.auth.models import User
from apps.accounts.forms import InviteCodeGenerationForm

admin = User.objects.get(username='your_username')
form = InviteCodeGenerationForm({'count': 5})
if form.is_valid():
    codes = form.generate_codes(admin, 5)
    for code in codes:
        print(f"Code: {code.code}")
```

## User Registration Flow

1. **User visits registration page**: `/accounts/register/`
2. **User fills out form with**:
   - Username and password
   - Valid invite code
   - Real name and student ID
   - Department and role
   - Optional: phone and WeChat
3. **System validates**:
   - Invite code exists and is unused
   - Student ID is unique
   - All required fields are filled
4. **On success**:
   - User account is created
   - UserProfile is created
   - Invite code is marked as used
   - User is automatically logged in

## Accessing Features

### Public Pages
- `/accounts/login/` - Login page
- `/accounts/register/` - Registration page

### Authenticated Pages
- `/accounts/profile/` - View and edit profile
- `/accounts/members/` - View all members with search/filter
- `/accounts/logout/` - Logout

### Admin-Only Pages
- `/accounts/invite-codes/` - Manage invite codes
- `/admin/` - Django admin panel

## Common Tasks

### Editing Profile
1. Login to the system
2. Click your name in the top right
3. Select "个人信息"
4. Update fields and click "保存修改"

### Searching Members
1. Go to `/accounts/members/`
2. Use search box to find by name, student ID, or username
3. Use dropdown filters for department and role

### Managing Invite Codes
1. Login as admin
2. Go to `/accounts/invite-codes/`
3. View statistics and all codes
4. Generate new codes as needed

## Testing the Implementation

Run the test suite:
```bash
python manage.py test apps.accounts
```

Expected output: 15 tests passed

## Troubleshooting

### Issue: Can't access invite codes page
**Solution**: Ensure your user has `role='admin'` in their UserProfile

### Issue: Invite code marked as used
**Solution**: Generate new codes - each code can only be used once

### Issue: Student ID already exists
**Solution**: Each student ID must be unique across all users

### Issue: Avatar not uploading
**Solution**: Ensure MEDIA_URL and MEDIA_ROOT are configured in settings.py

## URLs Reference

| URL | Name | Description | Auth Required | Admin Only |
|-----|------|-------------|---------------|------------|
| `/accounts/login/` | login | Login page | No | No |
| `/accounts/register/` | register | Registration | No | No |
| `/accounts/logout/` | logout | Logout | Yes | No |
| `/accounts/profile/` | profile | Profile edit | Yes | No |
| `/accounts/members/` | members | Members list | Yes | No |
| `/accounts/invite-codes/` | invite_codes | Manage codes | Yes | Yes |
| `/accounts/invite-codes/generate/` | generate_invite_code | Generate codes | Yes | Yes |

## Security Notes

1. All passwords are hashed using Django's password hashers
2. CSRF protection is enabled on all forms
3. Invite codes prevent unauthorized registration
4. Admin-only views check user role
5. Login required decorator protects authenticated pages

## Next Steps

After setting up accounts:
1. Create additional apps (announcements, broadcast, etc.)
2. Configure permissions for different roles
3. Customize templates to match your branding
4. Set up email notifications (future enhancement)
