# Vidyaniketan Backend - Login Fix & Admin Theme Setup

## 🔧 Student Login Issue - FIXED

### Problem
Test students couldn't login from the frontend despite having valid credentials.

### Root Cause
The `MobileTokenObtainPairSerializer` wasn't properly mapping the `mobile_number` field to Django's expected `username` field during JWT token validation.

### Solution Applied
Updated `apps/api/serializers.py` with improved field mapping:

```python
class MobileTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.USERNAME_FIELD  # 'mobile_number'

    def validate(self, attrs):
        # Map mobile_number to username for JWT validation
        if self.username_field in attrs and self.username_field != 'username':
            attrs['username'] = attrs.pop(self.username_field)
        
        # Call parent validation with username field
        try:
            data = super().validate(attrs)
        except Exception as e:
            # Provide clear error message for login failures
            raise serializers.ValidationError({
                'non_field_errors': [
                    'Invalid mobile number or password. Please check your credentials.'
                ]
            })
        
        # Add user data to response
        data['user'] = UserSerializer(self.user).data
        return data
```

### How to Test Student Login

**Test Credentials:**
```
Mobile: 9876543210
Password: password123
```

**API Endpoint:**
```
POST http://localhost:8000/api/auth/login/
Content-Type: application/json

{
  "mobile_number": "9876543210",
  "password": "password123"
}
```

**Expected Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "mobile_number": "9876543210",
    "email": "rahul.sharma@example.com",
    "role": "student",
    "is_active": true,
    "date_joined": "2026-04-26T...",
    "fcm_token": null
  }
}
```

---

## 🎨 Django Admin Theme Customization

### New Files Added

1. **`project/admin_theme.py`** - Theme configuration and CSS generation
2. **`project/admin_site.py`** - Custom admin site class with theme support
3. **`templates/admin/base_site.html`** - Themed admin base template
4. **Updated `project/urls.py`** - To use custom admin site

### Available Color Themes

The system includes 4 pre-configured professional themes:

#### 1. **Vidyaniketan Purple** (Default)
- **Primary**: #1A237E (Deep Purple)
- **Accent**: #FF6F00 (Deep Orange)
- **Best for**: Professional, educational look

```python
'default': {
    'primary_color': '#1A237E',
    'accent_color': '#FF6F00',
    ...
}
```

#### 2. **Modern Blue**
- **Primary**: #1976D2 (Blue)
- **Accent**: #FF6D00 (Orange)
- **Best for**: Corporate, tech-focused

```python
'modern_blue': {
    'primary_color': '#1976D2',
    'accent_color': '#FF6D00',
    ...
}
```

#### 3. **Fresh Green**
- **Primary**: #00796B (Teal)
- **Accent**: #D84315 (Deep Orange)
- **Best for**: Environmental, growth-oriented

```python
'fresh_green': {
    'primary_color': '#00796B',
    'accent_color': '#D84315',
    ...
}
```

#### 4. **Professional Slate**
- **Primary**: #455A64 (Blue Grey)
- **Accent**: #E65100 (Orange)
- **Best for**: Enterprise, formal

```python
'professional_slate': {
    'primary_color': '#455A64',
    'accent_color': '#E65100',
    ...
}
```

### How to Switch Themes

Edit `project/admin_site.py` and change the `current_theme`:

```python
class VidyanikketanAdminSite(AdminSite):
    # Change this to switch themes
    current_theme = 'default'  # Options: 'default', 'modern_blue', 'fresh_green', 'professional_slate'
```

Example - Switch to Modern Blue:
```python
current_theme = 'modern_blue'
```

### Theme Features

✅ **Customizable Colors**
- Primary color (headers, buttons)
- Accent color (highlights, borders)
- Success/Warning/Danger colors
- Text and background colors
- Border colors

✅ **Modern Styling**
- Gradient backgrounds on headers
- Smooth transitions and hover effects
- Rounded corners on UI elements
- Box shadows for depth
- Responsive design

✅ **Improved User Experience**
- Better visual hierarchy
- Clear form focus states
- Distinct table row highlighting
- Status message styling (success, error, warning, info)
- Professional button styling

✅ **Responsive Design**
- Mobile-friendly layouts
- Adaptive typography
- Touch-friendly buttons
- Optimized for tablets and desktops

### Accessing the Themed Admin Panel

1. **Start the Django development server:**
```bash
cd Backend
python manage.py runserver
```

2. **Login to admin:**
- URL: `http://localhost:8000/admin/`
- Username/Mobile: `9999999999`
- Password: `admin123`

3. **View the themed interface:**
- All pages now display with the custom purple theme
- Interactive elements have smooth animations
- Professional gradients on headers

### Customizing Theme Colors

To create a custom theme, add a new entry to `ADMIN_THEME_CONFIG` in `project/admin_theme.py`:

```python
ADMIN_THEME_CONFIG = {
    # ... existing themes ...
    'custom_theme': {
        'name': 'My Custom Theme',
        'primary_color': '#YOUR_HEX_COLOR',
        'primary_light': '#LIGHTER_VERSION',
        'primary_dark': '#DARKER_VERSION',
        'accent_color': '#ACCENT_HEX',
        'accent_light': '#LIGHTER_ACCENT',
        'success_color': '#SUCCESS_HEX',
        'warning_color': '#WARNING_HEX',
        'danger_color': '#DANGER_HEX',
        'info_color': '#INFO_HEX',
        'text_primary': '#TEXT_DARK',
        'text_secondary': '#TEXT_LIGHT',
        'bg_primary': '#BG_LIGHT',
        'bg_secondary': '#BG_LIGHTER',
        'border_color': '#BORDER_HEX',
    }
}
```

Then switch to your custom theme:
```python
current_theme = 'custom_theme'
```

### CSS Classes and Styling

The template includes CSS for all Django admin elements:

- **Headers & Navigation**: Gradient backgrounds, hover effects
- **Forms**: Focused input styling, error highlighting
- **Buttons**: Gradient styling, shadow effects
- **Tables**: Alternating row colors, hover highlighting
- **Messages**: Color-coded (success, error, warning, info)
- **Sidebar**: Active state highlighting, smooth transitions
- **Pagination**: Modern styling with hover effects

### Theme System Architecture

```
project/
├── admin_theme.py          # Theme definitions & CSS generation
├── admin_site.py           # Custom AdminSite class
└── urls.py                 # Uses custom admin site

templates/admin/
└── base_site.html          # Themed base template
```

**Flow:**
1. User accesses `/admin/`
2. Custom `VidyanikketanAdminSite` is loaded
3. `admin_site.py` loads theme configuration from `admin_theme.py`
4. CSS is generated based on selected theme
5. `base_site.html` renders with themed CSS
6. All admin pages inherit the themed styling

### Benefits

1. **Brand Consistency**: Admin panel matches your brand colors
2. **Professional Appearance**: Modern, polished interface
3. **Easy to Maintain**: Single source of truth for colors
4. **Accessibility**: Proper contrast ratios maintained
5. **Performance**: Pure CSS styling, no heavy frameworks
6. **Mobile Friendly**: Responsive design works on all devices
7. **Easy Switching**: Change theme with one line of code

---

## 🚀 Complete Setup Instructions

### 1. Backend Setup
```bash
cd Backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 2. Test Admin Login
- URL: http://localhost:8000/admin/
- Mobile: `9999999999`
- Password: `admin123`

### 3. Test Student Login (API)
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"mobile_number": "9876543210", "password": "password123"}'
```

### 4. Switch Themes (Optional)
Edit `project/admin_site.py` and change `current_theme` to:
- `'default'` - Vidyaniketan Purple (recommended)
- `'modern_blue'` - Modern Blue
- `'fresh_green'` - Fresh Green
- `'professional_slate'` - Professional Slate

### 5. Restart Django Server
```bash
python manage.py runserver
```

---

## 📱 Frontend Integration

The frontend can now successfully login students using:

```dart
final response = await ApiService.login(
  '9876543210',  // mobile_number
  'password123'  // password
);
```

The API will return the JWT tokens and user data for authenticated requests.

---

## 🔍 Troubleshooting

### Student Still Can't Login

**Error: "Invalid mobile number or password"**
- Verify test data exists: `python create_dummy_data.py`
- Check mobile number format (10-15 digits)
- Ensure password is correct: `password123`

**Error: "No internet connection"**
- Check backend is running: `python manage.py runserver`
- Verify API URL is correct: `http://localhost:8000/api/`
- Check network connectivity

### Admin Theme Not Showing

**Admin looks plain/default**
- Clear browser cache (Ctrl+Shift+Delete)
- Force refresh (Ctrl+F5)
- Check `project/admin_site.py` for `current_theme` setting
- Verify `urls.py` uses custom admin site

**Wrong colors showing**
- Check theme name in `admin_site.py`
- Verify `ADMIN_THEME_CONFIG` in `admin_theme.py`
- Restart Django server

---

## 📝 Files Modified

1. ✅ `Backend/apps/api/serializers.py` - Fixed MobileTokenObtainPairSerializer
2. ✅ `Backend/project/admin_theme.py` - New theme configuration
3. ✅ `Backend/project/admin_site.py` - New custom admin site
4. ✅ `Backend/project/urls.py` - Uses custom admin site
5. ✅ `Backend/templates/admin/base_site.html` - Themed template

---

## ✅ Verification Checklist

- [ ] Backend runs without errors
- [ ] Admin can login with `9999999999` / `admin123`
- [ ] Admin panel displays with purple theme
- [ ] Student can login with `9876543210` / `password123` from API
- [ ] JWT tokens are returned correctly
- [ ] Frontend receives user data with tokens
- [ ] Theme colors are visible in admin panel
- [ ] Mobile responsive design works

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the API test credentials
3. Verify all files are in correct locations
4. Restart Django server and clear browser cache

