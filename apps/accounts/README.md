# Accounts App Documentation

## Overview
The accounts app handles user authentication, registration, profile management, and invite code system for the campus radio management platform.

## Models

### UserProfile
Extended user profile with the following fields:
- `user`: OneToOne relationship with Django User
- `real_name`: User's real name (姓名)
- `student_id`: Unique student ID (学号)
- `phone`: Phone number (optional)
- `wechat`: WeChat ID (optional)
- `department`: Department (broadcast/himalaya/both)
- `role`: Role (admin/anchor/himalaya)
- `avatar`: Profile picture (optional)
- `bio`: Personal bio (optional)

**Methods:**
- `is_admin()`: Returns True if user is admin
- `is_anchor()`: Returns True if user is anchor
- `is_himalaya()`: Returns True if user is himalaya staff

### InviteCode
Invite codes for registration control:
- `code`: Unique invite code
- `created_by`: User who created the code
- `created_at`: Creation timestamp
- `used_by`: User who used the code (nullable)
- `used_at`: Usage timestamp (nullable)
- `is_used`: Boolean flag for used status

## Forms

### RegistrationForm
User registration form extending UserCreationForm with:
- Username and password fields
- Invite code validation
- Profile fields (real_name, student_id, phone, wechat, department, role)
- Custom validation for invite code availability
- Custom validation for unique student ID

### UserProfileForm
Profile editing form with:
- real_name, phone, wechat, bio
- Avatar upload support
- Tailwind CSS styling

### InviteCodeGenerationForm
Admin form for generating invite codes:
- Count field (1-100)
- `generate_codes()` method to create multiple codes

## Views

### register_view
- Public view for user registration
- Requires valid unused invite code
- Creates User and UserProfile in atomic transaction
- Marks invite code as used
- Redirects authenticated users to profile

### login_view
- Standard Django authentication
- Redirects authenticated users to profile
- Supports next parameter for redirect

### logout_view
- Requires authentication
- Logs out user and redirects to login

### profile_edit_view
- Requires authentication
- View and edit user profile
- Supports avatar upload
- Shows profile information

### members_list_view
- Requires authentication
- Lists all members with profiles
- Search by name, student ID, or username
- Filter by department and role

### invite_codes_view
- Requires admin permission
- Lists all invite codes
- Shows usage statistics
- Allows code generation

### generate_invite_code
- Requires admin permission
- POST endpoint for generating codes
- Creates specified number of codes

## URLs

```
/accounts/login/                  - Login page
/accounts/register/               - Registration page
/accounts/logout/                 - Logout endpoint
/accounts/profile/                - Profile view/edit
/accounts/members/                - Members list
/accounts/invite-codes/           - Invite codes management
/accounts/invite-codes/generate/  - Generate invite codes
```

## Templates

### login.html
- Clean login form
- Link to registration
- Tailwind CSS styled

### register.html
- Two-column registration form
- Invite code field
- Profile information fields
- Field validation display

### profile.html
- Profile information display
- Avatar display
- Edit form
- Grid layout for information

### members.html
- Search and filter form
- Card-based member display
- Avatar display
- Department and role badges

### invite_codes.html
- Statistics dashboard
- Invite code table
- Modal for code generation
- Used/unused status display

## Admin Configuration

### UserProfileAdmin
- List display: real_name, user, student_id, department, role, created_at
- Filters: department, role, created_at
- Search: real_name, student_id, username
- Organized fieldsets

### InviteCodeAdmin
- List display: code, is_used, created_by, created_at, used_by, used_at
- Filters: is_used, created_at
- Search: code, created_by username, used_by username
- Organized fieldsets

## Usage Examples

### Creating an Admin User
```python
from django.contrib.auth.models import User
from apps.accounts.models import UserProfile

admin = User.objects.create_superuser('admin', 'admin@example.com', 'password')
UserProfile.objects.create(
    user=admin,
    real_name='管理员',
    student_id='2024001',
    department='broadcast',
    role='admin'
)
```

### Generating Invite Codes
```python
from apps.accounts.forms import InviteCodeGenerationForm

form = InviteCodeGenerationForm({'count': 5})
if form.is_valid():
    codes = form.generate_codes(admin_user, 5)
```

### Checking User Permissions
```python
if request.user.profile.is_admin():
    # Admin only code
    pass
```

## Security Features

1. **Invite Code System**: Only users with valid invite codes can register
2. **Atomic Transactions**: User and profile creation happens atomically
3. **Permission Checks**: Admin-only views verify user role
4. **CSRF Protection**: All forms include CSRF tokens
5. **Authentication Required**: Most views require login
6. **Password Validation**: Django's built-in password validators

## Styling

All templates use Tailwind CSS for responsive, modern UI:
- Consistent color scheme (blue primary)
- Responsive grid layouts
- Form styling with focus states
- Card-based designs
- Badge components for status display

## Testing

The app has been tested for:
- Model creation and relationships
- Form validation (invite codes, student IDs)
- URL routing
- View access control
- Template rendering
- Admin configuration
- Complete registration workflow

## Future Enhancements

Potential improvements:
- Email verification
- Password reset functionality
- Bulk invite code export
- User activity logs
- Profile completion percentage
- Advanced search filters
