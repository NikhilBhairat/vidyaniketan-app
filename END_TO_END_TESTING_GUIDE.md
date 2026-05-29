# End-to-End Testing & Deployment Guide

## 📋 Current Status

✅ **Backend**: Django REST API configured and working (admin login confirmed)
✅ **API Configuration**: Updated with fallback URLs for local testing
✅ **API Service**: Enhanced with logging, retry logic, and better error handling
✅ **Mobile APK**: Ready to test

---

## 🔧 NEXT STEPS - What To Do Now

### **Step 1: Verify Backend is Accessible** (5 minutes)

Test if your backend is reachable from the mobile device:

```bash
# From your computer/laptop (same network as mobile)
curl -v https://vidyaniketan-app-main-f58e2f6.kuberns.cloud/api/

# Expected response: Either 200 OK or 404/405 (means backend is UP)
# If: "Connection refused" or timeout = Backend NOT accessible
```

If backend is **NOT accessible**, you have two options:

#### **Option A: Use Local Backend (Recommended for Development)**

```bash
# 1. Start Django backend locally
cd Backend
python manage.py runserver 0.0.0.0:8000

# 2. Find your machine's IP
# On Windows: ipconfig (look for IPv4 Address)
# On Mac/Linux: ifconfig (look for inet)
# Example: 192.168.1.100

# 3. Update Flutter config
# Edit: Frontend/lib/config/api_config.dart
# Change: static const String baseUrl = 'http://192.168.1.100:8000';
# Set: static const bool USE_LOCAL_BACKEND = true;
```

#### **Option B: Fix Kubernetes Deployment (Production)**

```bash
# Check if Kubernetes pods are running
kubectl get pods
kubectl get svc

# View logs to see errors
kubectl logs -l app=vidyaniketan-app

# Restart deployment if needed
kubectl rollout restart deployment/vidyaniketan-app
```

---

### **Step 2: Update Mobile Configuration** (2 minutes)

**Choose your environment and update the config file:**

```dart
// Frontend/lib/config/api_config.dart

// FOR PRODUCTION (Kubernetes)
static const String baseUrl = 'https://vidyaniketan-app-main-f58e2f6.kuberns.cloud';
static const bool USE_LOCAL_BACKEND = false;

// OR FOR LOCAL TESTING
static const String baseUrl = 'http://192.168.1.100:8000';  // Your machine IP
static const bool USE_LOCAL_BACKEND = true;

// OR FOR ANDROID EMULATOR
static const String baseUrl = 'http://10.0.2.2:8000';
static const bool USE_LOCAL_BACKEND = true;
```

---

### **Step 3: Update Android Manifest Permissions** (2 minutes)

Ensure your app has internet permission:

```xml
<!-- Frontend/android/app/src/main/AndroidManifest.xml -->

<manifest ...>
    <!-- ADD THIS LINE if missing -->
    <uses-permission android:name="android.permission.INTERNET" />
    
    <application>
        ...
    </application>
</manifest>
```

---

### **Step 4: For Local Development - Enable Cleartext Traffic** (2 minutes)

If using HTTP on local network:

**Create file**: `Frontend/android/app/src/main/res/xml/network_security_config.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <!-- Allow HTTP for local development -->
    <domain-config cleartextTrafficPermitted="true">
        <domain includeSubdomains="true">192.168.1.100</domain>
        <domain includeSubdomains="true">10.0.2.2</domain>
    </domain-config>
</network-security-config>
```

**Update AndroidManifest.xml**:

```xml
<application
    android:networkSecurityConfig="@xml/network_security_config"
    ...>
</application>
```

---

### **Step 5: Build and Deploy APK** (5 minutes)

```bash
# Navigate to Flutter project
cd Frontend

# Clean previous builds
flutter clean

# Get dependencies
flutter pub get

# Build APK
flutter build apk --release

# APK location: build/app/outputs/apk/release/app-release.apk

# Install on device
adb install build/app/outputs/apk/release/app-release.apk

# OR just run on connected device
flutter run --release
```

---

### **Step 6: Test Login from Mobile** (5 minutes)

**Test Credentials**:
- Mobile Number: `9876543210`
- Password: `password123`

**What to check**:
1. ✅ App opens without crashing
2. ✅ Enter mobile number and password
3. ✅ Click "Sign In"
4. ✅ Check for these outcomes:

| Outcome | Meaning |
|---------|---------|
| ✅ Login Success → Dashboard | Backend reachable ✓ |
| ❌ "No internet connection" | Backend not reachable |
| ❌ "Invalid credentials" | Backend reachable but wrong credentials |
| ❌ "Connection timeout" | Backend too slow or unreachable |
| ❌ "500 Server Error" | Backend has a bug |

---

### **Step 7: Debug Using Logs** (if login fails)

**Option A: Flutter Logs**
```bash
# Run with verbose logging
flutter run -v

# Look for API errors in console
# You'll see detailed error messages and request/response data
```

**Option B: Check Mobile Logs**
```bash
# View Android logs
adb logcat | grep -i "api\|http\|error"

# This will show HTTP request/response details
```

**Option C: Backend Logs**
```bash
# If using local backend
# Look at console output where you ran: python manage.py runserver

# If using Kubernetes
kubectl logs -f deployment/vidyaniketan-app
```

---

## 🚀 Complete Workflow

### **For Local Testing (Easiest)**

```
1. Get your machine IP (e.g., 192.168.1.100)
   ↓
2. Update Frontend/lib/config/api_config.dart
   baseUrl = 'http://192.168.1.100:8000'
   ↓
3. Start Django backend:
   python manage.py runserver 0.0.0.0:8000
   ↓
4. Build Flutter APK:
   flutter build apk --release
   ↓
5. Install on mobile:
   adb install build/app/outputs/apk/release/app-release.apk
   ↓
6. Test login with:
   Mobile: 9876543210
   Password: password123
   ↓
7. Check console/logcat for errors
```

### **For Production Deployment (Kubernetes)**

```
1. Verify backend is running:
   curl https://vidyaniketan-app-main-f58e2f6.kuberns.cloud/api/
   ↓
2. Keep config as:
   baseUrl = 'https://vidyaniketan-app-main-f58e2f6.kuberns.cloud'
   ↓
3. Build APK:
   flutter build apk --release
   ↓
4. Distribute APK to users
   ↓
5. Users install and login
```

---

## 📊 Troubleshooting Matrix

### Scenario 1: "No internet connection" Error

**Causes & Fixes:**

| Cause | Fix |
|-------|-----|
| Backend URL is wrong | Check api_config.dart |
| Backend not running | Start Django: `python manage.py runserver` |
| Backend not accessible from mobile network | Use local IP or check network access |
| DNS resolution failure | Try using IP instead of domain |
| SSL certificate invalid | Only for HTTPS - check certificate validity |

**Quick Fix**:
```bash
# Test from your computer first
curl -v https://vidyaniketan-app-main-f58e2f6.kuberns.cloud/api/

# If it fails, backend is down - restart it
# If it works, mobile network issue - check firewall
```

---

### Scenario 2: "Invalid Credentials" Error

✅ **Good news**: Backend is reachable!

**Fixes**:
- Verify mobile number in database: `9876543210`
- Verify password is: `password123`
- Check if user is active in admin panel
- Try creating a new test user

```bash
# From Django shell
python manage.py shell

from apps.accounts.models import User
user = User.objects.get(mobile_number='9876543210')
print(user.is_active)  # Should be True
```

---

### Scenario 3: "Connection Timeout" Error

**Causes**:
- Backend is slow
- Network latency
- Firewall blocking

**Fixes**:
```python
# Increase timeout in api_config.dart
static const int connectTimeout = 60;  // Increase from 30
static const int receiveTimeout = 60;
static const int sendTimeout = 60;
```

---

### Scenario 4: "500 Server Error"

❌ **Backend has a bug**

**Check logs**:
```bash
# If local backend
# Look at console where Django is running

# If Kubernetes
kubectl logs deployment/vidyaniketan-app
```

**Common fixes**:
- Check database is initialized
- Run migrations: `python manage.py migrate`
- Check for missing data in database

---

## ✨ Final Checklist Before Going Live

- [ ] Backend is running and accessible
- [ ] Django admin login works
- [ ] `api_config.dart` has correct URL
- [ ] `AndroidManifest.xml` has INTERNET permission
- [ ] Network security config updated (for HTTP)
- [ ] APK built successfully
- [ ] Test credentials created (9876543210 / password123)
- [ ] Login test successful on mobile
- [ ] Can see student dashboard after login
- [ ] Attendance data loads
- [ ] Fees data loads
- [ ] Notifications display
- [ ] All endpoints working without errors

---

## 📞 Support Information

### If Login Still Fails After Following All Steps:

1. **Check these files are updated**:
   - `Frontend/lib/config/api_config.dart` ✅
   - `Frontend/android/app/src/main/AndroidManifest.xml` ✅
   - `Frontend/android/app/src/main/res/xml/network_security_config.xml` ✅

2. **Check logs**:
   ```bash
   flutter run -v  # Run with verbose logging
   adb logcat     # Android logs
   ```

3. **Verify backend**:
   ```bash
   # Test endpoint directly
   curl -X POST https://vidyaniketan-app-main-f58e2f6.kuberns.cloud/api/auth/login/ \
     -H "Content-Type: application/json" \
     -d '{"mobile_number":"9876543210","password":"password123"}'
   ```

4. **Check network**:
   - Test with WiFi (not mobile data)
   - Try from different network
   - Check firewall/proxy settings

---

## 🎯 Success Indicators

When everything is working:

1. ✅ APK launches without errors
2. ✅ Enter credentials: 9876543210 / password123
3. ✅ Click Sign In
4. ✅ See dashboard with student info
5. ✅ Access all menu items (Attendance, Fees, Marks, etc.)
6. ✅ No network errors in logs
7. ✅ Smooth navigation between screens

---

## 📝 Next Commands to Run

```bash
# 1. Find your machine IP
ipconfig              # Windows
ifconfig              # Mac/Linux

# 2. Update config file with your IP
# Edit: Frontend/lib/config/api_config.dart
# Change baseUrl to: http://YOUR_MACHINE_IP:8000

# 3. Start backend (if local testing)
cd Backend
python manage.py runserver 0.0.0.0:8000

# 4. Build APK (in new terminal)
cd Frontend
flutter clean
flutter pub get
flutter build apk --release

# 5. Install on device
adb install build/app/outputs/apk/release/app-release.apk

# 6. Run Flutter with logs
flutter run -v

# 7. Test login on mobile with: 9876543210 / password123
```

---

## 🎓 What Each File Does

| File | Purpose | Status |
|------|---------|--------|
| `Frontend/lib/config/api_config.dart` | API URLs & endpoints | ✅ Updated |
| `Frontend/lib/services/api_service.dart` | HTTP client with retry logic | ✅ Enhanced |
| `Backend/project/settings.py` | Django config | ✅ Ready |
| `Backend/apps/api/views.py` | Login endpoint | ✅ Working |
| `Backend/apps/api/urls.py` | API routes | ✅ Configured |
| `MOBILE_LOGIN_FIX.md` | Detailed fix guide | ✅ Created |

---

## 🚀 Ready to Deploy?

You now have:
1. ✅ Enhanced API configuration with fallback URLs
2. ✅ Improved API service with logging & retries
3. ✅ Comprehensive testing guide
4. ✅ Detailed troubleshooting steps
5. ✅ All necessary configurations

**Next**: Choose local or production setup and follow the workflow above.

Good luck! 🎉
