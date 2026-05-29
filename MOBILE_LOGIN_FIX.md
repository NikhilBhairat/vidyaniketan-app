# Mobile APK Login Issue - Root Cause & Complete Fix

## Problem Summary
**Error**: "No internet connection" when logging in from mobile APK, even though Django admin works fine.

**Root Cause**: The backend URL `https://vidyaniketan-app-main-f58e2f6.kuberns.cloud` is either:
1. Not accessible from the mobile device's network
2. The Kubernetes service is down/unreachable
3. SSL certificate issues (mobile clients are stricter)
4. DNS resolution failures on mobile network

---

## PART 1: Diagnosis & Testing

### Step 1: Test Backend Accessibility

```bash
# Check if your backend is actually running
curl -v https://vidyaniketan-app-main-f58e2f6.kuberns.cloud/api/auth/login/

# Expected: Should return something, not "connection refused" or timeout
# If timeout/connection refused: Your backend is NOT accessible
```

### Step 2: Check Kubernetes Status

```bash
# List running pods
kubectl get pods

# Check services
kubectl get svc

# View service details
kubectl describe svc vidyaniketan-app

# Check logs
kubectl logs -l app=vidyaniketan-app
```

### Step 3: Debug from Mobile

**Option A: Add detailed logging to Flutter app**
```dart
// In Frontend/lib/services/api_service.dart
void _handleError(DioException error) {
  print('═══ API ERROR DEBUG ═══');
  print('Type: ${error.type}');
  print('Message: ${error.message}');
  print('Response Code: ${error.response?.statusCode}');
  print('Response Data: ${error.response?.data}');
  print('Base URL: ${_dio.options.baseUrl}');
  print('Path: ${error.requestOptions.path}');
  print('Full URL: ${error.requestOptions.uri}');
  print('═══════════════════════');
}
```

**Option B: Test from desktop**
```bash
# On same network as mobile device
curl -v https://vidyaniketan-app-main-f58e2f6.kuberns.cloud/api/auth/login/
```

---

## PART 2: Fix #1 - Local Development Setup

If backend is running locally and not accessible from mobile:

### Update Flutter Configuration

```dart
// Frontend/lib/config/api_config.dart
class ApiConfig {
  // For LOCAL DEVELOPMENT - use your machine's IP
  // Replace XXX.XXX.XXX.XXX with your machine's IP (e.g., 192.168.1.100)
  static const String baseUrl = 'http://192.168.1.100:8000';  // ← Change this
  
  // Alternative for testing on same machine with emulator
  // static const String baseUrl = 'http://10.0.2.2:8000';  // Android emulator special IP
  
  static const String apiVersion = '/api';
  static const String apiBaseUrl = '$baseUrl$apiVersion';
  
  // Rest of endpoints...
}
```

### Update Android Network Security

```xml
<!-- Frontend/android/app/src/main/AndroidManifest.xml -->
<!-- Add INTERNET permission if missing -->
<uses-permission android:name="android.permission.INTERNET" />
```

Create file: `Frontend/android/app/src/main/res/xml/network_security_config.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <domain-config cleartextTrafficPermitted="true">
        <domain includeSubdomains="true">192.168.1.100</domain>
    </domain-config>
    <domain-config cleartextTrafficPermitted="true">
        <domain includeSubdomains="true">10.0.2.2</domain>
    </domain-config>
</network-security-config>
```

### Update AndroidManifest.xml

```xml
<application
    android:networkSecurityConfig="@xml/network_security_config"
    ...>
```

---

## PART 3: Fix #2 - Production Kubernetes Deployment

If using Kubernetes (`kuberns.cloud`):

### Check Backend Settings

```python
# Backend/project/settings.py
ALLOWED_HOSTS = [
    "vidyaniketan-app-main-f58e2f6.kuberns.cloud",
    "localhost",
    "127.0.0.1",
    # Add your server IPs if any
]

CORS_ALLOWED_ORIGINS = [
    "https://vidyaniketan-app-main-f58e2f6.kuberns.cloud",
    "http://vidyaniketan-app-main-f58e2f6.kuberns.cloud",
]
```

### Verify SSL Certificate

```bash
# Check SSL certificate validity
openssl s_client -connect vidyaniketan-app-main-f58e2f6.kuberns.cloud:443

# Mobile apps require valid certificates
# Make sure it's not expired or self-signed
```

### Check Kubernetes Ingress

```bash
# View ingress configuration
kubectl get ingress

# Describe ingress
kubectl describe ingress <ingress-name>

# Check if endpoint is reachable
kubectl port-forward svc/vidyaniketan-app 8000:8000
```

---

## PART 4: Complete Working Configuration

### Backend - Django Settings (Final)

```python
# Backend/project/settings.py
import os
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-change-this-in-production")
DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1", "yes")

# Allow both localhost and production domain
ALLOWED_HOSTS = [
    "vidyaniketan-app-main-f58e2f6.kuberns.cloud",
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SAMESITE = "None"

CSRF_TRUSTED_ORIGINS = [
    "https://vidyaniketan-app-main-f58e2f6.kuberns.cloud",
    "http://vidyaniketan-app-main-f58e2f6.kuberns.cloud",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_filters",
    "corsheaders",
    "apps.accounts",
    "apps.students",
    "apps.attendance",
    "apps.fees",
    "apps.results",
    "apps.study_material",
    "apps.lectures",
    "apps.gallery",
    "apps.notifications",
    "apps.api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# CORS - Allow mobile app
CORS_ALLOW_ALL_ORIGINS = True  # Or restrict to specific origins
# CORS_ALLOWED_ORIGINS = [
#     "https://vidyaniketan-app-main-f58e2f6.kuberns.cloud",
#     "http://vidyaniketan-app-main-f58e2f6.kuberns.cloud",
# ]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
SECURE_SSL_REDIRECT = False  # Set to True in production with HTTPS

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_USER_MODEL = "accounts.User"
AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
```

### Frontend - Flutter Configuration (Final)

```dart
// Frontend/lib/config/api_config.dart
class ApiConfig {
  // Production URL
  static const String baseUrl = 'https://vidyaniketan-app-main-f58e2f6.kuberns.cloud';
  
  // For local testing, uncomment and update with your machine IP
  // static const String baseUrl = 'http://192.168.1.100:8000';
  
  // For Android emulator testing
  // static const String baseUrl = 'http://10.0.2.2:8000';
  
  static const String apiVersion = '/api';
  static const String apiBaseUrl = '$baseUrl$apiVersion';
  
  // Auth Endpoints
  static const String loginEndpoint = '$apiBaseUrl/auth/login/';
  static const String registerEndpoint = '$apiBaseUrl/auth/register/';
  static const String logoutEndpoint = '$apiBaseUrl/auth/logout/';
  static const String profileEndpoint = '$apiBaseUrl/auth/profile/';
  
  // Student Endpoints
  static const String studentsEndpoint = '$apiBaseUrl/students';
  
  // Other Endpoints
  static const String attendanceEndpoint = '$apiBaseUrl/attendance';
  static const String feesEndpoint = '$apiBaseUrl/fees';
  static const String examsEndpoint = '$apiBaseUrl/exams';
  static const String marksEndpoint = '$apiBaseUrl/marks';
  static const String notificationsEndpoint = '$apiBaseUrl/notifications';
  
  // Timeouts
  static const int connectTimeout = 30;
  static const int receiveTimeout = 30;
  static const int sendTimeout = 30;
}
```

### Frontend - Enhanced API Service

```dart
// Frontend/lib/services/api_service.dart
import 'package:dio/dio.dart';
import 'package:vidyaniketan_app/config/api_config.dart';

class ApiService {
  late Dio _dio;
  
  ApiService() {
    _initDio();
  }
  
  void _initDio() {
    _dio = Dio(
      BaseOptions(
        baseUrl: ApiConfig.apiBaseUrl,
        connectTimeout: Duration(seconds: ApiConfig.connectTimeout),
        receiveTimeout: Duration(seconds: ApiConfig.receiveTimeout),
        sendTimeout: Duration(seconds: ApiConfig.sendTimeout),
        contentType: 'application/json',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
      ),
    );
    
    _addInterceptors();
  }
  
  void _addInterceptors() {
    _dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) {
          print('REQUEST: ${options.method} ${options.path}');
          print('Full URL: ${options.uri}');
          return handler.next(options);
        },
        onResponse: (response, handler) {
          print('RESPONSE: ${response.statusCode}');
          return handler.next(response);
        },
        onError: (DioException e, handler) {
          _handleError(e);
          return handler.next(e);
        },
      ),
    );
  }
  
  void _handleError(DioException error) {
    print('═══ API ERROR ═══');
    print('Type: ${error.type}');
    print('Message: ${error.message}');
    print('Response Code: ${error.response?.statusCode}');
    print('Response: ${error.response?.data}');
    print('Base URL: ${_dio.options.baseUrl}');
    print('═════════════════');
    
    if (error.type == DioExceptionType.connectionTimeout) {
      print('❌ Connection Timeout - Backend not responding');
    } else if (error.type == DioExceptionType.receiveTimeout) {
      print('❌ Receive Timeout - Response taking too long');
    } else if (error.type == DioExceptionType.badResponse) {
      print('❌ Bad Response: ${error.response?.statusCode}');
    } else if (error.type == DioExceptionType.unknown) {
      print('❌ Network Error: ${error.message}');
    }
  }
  
  Future<Response> get(String path, {
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    return await _dio.get(path, queryParameters: queryParameters, options: options);
  }
  
  Future<Response> post(String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    return await _dio.post(path, data: data, queryParameters: queryParameters, options: options);
  }
  
  void setAuthToken(String token) {
    _dio.options.headers['Authorization'] = 'Bearer $token';
  }
  
  void clearAuthToken() {
    _dio.options.headers.remove('Authorization');
  }
}
```

---

## PART 5: Testing Checklist

### Backend Tests

```bash
# 1. Test endpoint directly
curl -X POST https://vidyaniketan-app-main-f58e2f6.kuberns.cloud/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"mobile_number":"9876543210","password":"password123"}'

# Expected response: {"refresh":"...", "access":"...", "user":{...}}

# 2. Test from Django shell
python Backend/manage.py shell

from apps.accounts.models import User
from django.contrib.auth import authenticate

user = User.objects.get(mobile_number='9876543210')
print(f"User exists: {user}")
print(f"Is active: {user.is_active}")

auth = authenticate(username='9876543210', password='password123')
print(f"Authentication result: {auth}")
```

### Mobile Tests

1. **Clear app data and cache**
   - Settings > Apps > VidyaNiketan > Clear Data/Cache

2. **Check network connectivity first**
   - Open browser → google.com
   - Should load successfully

3. **Check with test login**
   ```
   Mobile: 9876543210
   Password: password123
   ```

4. **Monitor logs in Flutter**
   - Run: `flutter run -v`
   - Look for API error messages

5. **Test with local setup first** (easier debugging)
   - Update `api_config.dart` with local IP
   - Run backend locally: `python manage.py runserver 0.0.0.0:8000`
   - Try login from mobile

---

## PART 6: Quick Decision Tree

```
Try to login from mobile
  │
  ├─ "No internet connection" error
  │   │
  │   ├─ Can you access backend URL from browser? 
  │   │   ├─ YES → CORS issue or certificate issue (see PART 3)
  │   │   └─ NO → Backend not accessible from your network
  │   │
  │   └─ Solution: Update baseUrl in api_config.dart to local IP
  │
  ├─ "Invalid credentials" error  
  │   └─ Backend is reachable ✓, but wrong username/password
  │
  ├─ "500 Server Error"
  │   └─ Backend running but has code error (check logs)
  │
  └─ "401 Unauthorized" (after successful login attempt)
      └─ Token issue, check JWT configuration
```

---

## PART 7: Final Verification

Once you implement the fix:

1. **Verify backend is running**
   ```bash
   curl -v https://vidyaniketan-app-main-f58e2f6.kuberns.cloud/api/auth/login/
   # Should return 405 Method Not Allowed (POST required, not GET) - This means backend is UP!
   ```

2. **Verify Flutter configuration**
   - Check `lib/config/api_config.dart` has correct URL
   - Check `android/app/src/main/AndroidManifest.xml` has INTERNET permission

3. **Test login**
   - Mobile: `9876543210`
   - Password: `password123`
   - Should see access/refresh tokens

4. **Check logs**
   - Backend: Check Django logs for any errors
   - Mobile: Run `flutter run -v` and check logs

---

## Summary

| Component | Status | Fix |
|-----------|--------|-----|
| Django Backend | ✓ Configured | Update ALLOWED_HOSTS, CORS |
| API Endpoints | ✓ Configured | `/api/auth/login/` ready |
| Flutter App | ✓ Configured | Update api_config.dart |
| Android Manifest | ✓ Required | Add INTERNET permission |
| Network Security | ⚠️ May need fix | Add network_security_config.xml |
| JWT Authentication | ✓ Configured | Working in views.py |

**Most likely issue**: Backend URL not accessible from mobile device's network or local machine.

**Most likely fix**: Update `Frontend/lib/config/api_config.dart` with your actual IP address or fix Kubernetes deployment.

---

## Emergency Fallback Test

```dart
// Temporary test - add to your login button
void testConnection() async {
  try {
    final dio = Dio();
    final response = await dio.get(
      'https://vidyaniketan-app-main-f58e2f6.kuberns.cloud/api/auth/login/',
      options: Options(
        connectTimeout: Duration(seconds: 5),
        receiveTimeout: Duration(seconds: 5),
      ),
    ).catchError((e) {
      print('Connection error: $e');
    });
    print('Server is reachable: ${response?.statusCode}');
  } catch (e) {
    print('Cannot reach server: $e');
  }
}
```

Run this to confirm backend accessibility before attempting full login.
