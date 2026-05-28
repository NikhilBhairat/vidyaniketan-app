# Backend Integration Guide

## Overview
This guide explains how the Flutter frontend is connected to the Django backend deployed on Kubernetes.

## Backend Service Details

- **Base URL**: `https://vidyaniketan-app-main-f58e2f6.kuberns.cloud`
- **API Endpoint**: `/api`
- **Full API URL**: `https://vidyaniketan-app-main-f58e2f6.kuberns.cloud/api`
- **Admin Panel**: `https://vidyaniketan-app-main-f58e2f6.kuberns.cloud/admin`

## Project Structure

### Configuration Files
- **`lib/config/api_config.dart`**: Centralized API configuration with all endpoints
- **`.env.example`**: Environment variables template

### Services
- **`lib/services/api_service.dart`**: HTTP client service using Dio library
  - Handles GET, POST, PUT, DELETE, PATCH requests
  - Manages timeouts and error handling
  - Supports authorization tokens

### Providers
- **`lib/providers/api_provider.dart`**: State management provider for API service
  - Integrates with Provider package
  - Manages loading states and errors

## Using the API Service

### Basic Setup

1. **Install Dio** (already in `pubspec.yaml`):
   ```yaml
   dio: ^5.9.2
   provider: ^6.0.6
   ```

2. **Initialize in main.dart**:
   ```dart
   import 'package:provider/provider.dart';
   import 'package:vidyaniketan_app/providers/api_provider.dart';

   void main() {
     runApp(
       MultiProvider(
         providers: [
           ChangeNotifierProvider(create: (_) => ApiProvider()),
         ],
         child: const MyApp(),
       ),
     );
   }
   ```

### Making API Calls

#### Example: Login Request
```dart
import 'package:vidyaniketan_app/config/api_config.dart';
import 'package:vidyaniketan_app/services/api_service.dart';

Future<void> login(String username, String password) async {
  try {
    ApiService apiService = ApiService();
    
    final response = await apiService.post(
      ApiConfig.loginEndpoint,
      data: {
        'username': username,
        'password': password,
      },
    );
    
    if (response.statusCode == 200) {
      // Handle successful login
      String token = response.data['token'];
      apiService.setAuthToken(token);
    }
  } catch (e) {
    print('Login failed: $e');
  }
}
```

#### Example: Get Students
```dart
Future<void> fetchStudents() async {
  try {
    ApiService apiService = ApiService();
    
    final response = await apiService.get(
      ApiConfig.studentsEndpoint,
    );
    
    if (response.statusCode == 200) {
      List students = response.data['results']; // Adjust based on your API response
      // Process students data
    }
  } catch (e) {
    print('Failed to fetch students: $e');
  }
}
```

#### Example: Create Assignment
```dart
Future<void> createAssignment(Map<String, dynamic> assignmentData) async {
  try {
    ApiService apiService = ApiService();
    
    final response = await apiService.post(
      ApiConfig.assignmentsEndpoint,
      data: assignmentData,
    );
    
    if (response.statusCode == 201) {
      // Handle successful creation
      print('Assignment created: ${response.data}');
    }
  } catch (e) {
    print('Failed to create assignment: $e');
  }
}
```

### Using with Provider (Recommended)

```dart
import 'package:provider/provider.dart';
import 'package:vidyaniketan_app/providers/api_provider.dart';
import 'package:vidyaniketan_app/config/api_config.dart';

class MyWidget extends StatefulWidget {
  @override
  State<MyWidget> createState() => _MyWidgetState();
}

class _MyWidgetState extends State<MyWidget> {
  @override
  void initState() {
    super.initState();
    _loadData();
  }

  void _loadData() {
    final apiProvider = context.read<ApiProvider>();
    apiProvider.setLoading(true);
    
    apiProvider.apiService.get(ApiConfig.studentsEndpoint).then((response) {
      apiProvider.setLoading(false);
      // Process response
    }).catchError((error) {
      apiProvider.setError(error.toString());
      apiProvider.setLoading(false);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<ApiProvider>(
      builder: (context, apiProvider, child) {
        if (apiProvider.isLoading) {
          return const CircularProgressIndicator();
        }
        
        if (apiProvider.error != null) {
          return Text('Error: ${apiProvider.error}');
        }
        
        return const Text('Data loaded successfully');
      },
    );
  }
}
```

## Available Endpoints

### Authentication
- `POST /api/login` - User login
- `POST /api/register` - User registration
- `POST /api/logout` - User logout
- `GET /api/profile` - Get current user profile

### Students
- `GET /api/students` - List all students
- `GET /api/students/{id}` - Get student details
- `POST /api/students` - Create new student
- `PUT /api/students/{id}` - Update student
- `DELETE /api/students/{id}` - Delete student

### Parents
- `GET /api/parents` - List all parents
- `GET /api/parents/{id}` - Get parent details
- `POST /api/parents` - Create new parent
- `PUT /api/parents/{id}` - Update parent
- `DELETE /api/parents/{id}` - Delete parent

### Classes
- `GET /api/classes` - List all classes
- `GET /api/classes/{id}` - Get class details

### Assignments
- `GET /api/assignments` - List all assignments
- `GET /api/assignments/{id}` - Get assignment details
- `POST /api/assignments` - Create new assignment
- `PUT /api/assignments/{id}` - Update assignment
- `DELETE /api/assignments/{id}` - Delete assignment

### Grades
- `GET /api/grades` - List all grades
- `GET /api/grades/{id}` - Get grade details

### Attendance
- `GET /api/attendance` - List attendance records
- `POST /api/attendance` - Create attendance record

### Notifications
- `GET /api/notifications` - List notifications

## Error Handling

The API service automatically handles common errors:

1. **Connection Timeout**: When server doesn't respond in 30 seconds
2. **Receive Timeout**: When receiving response takes too long
3. **Bad Response**: When server returns error status codes
4. **Network Errors**: When there's no internet connection

You can customize error handling in `lib/services/api_service.dart` by modifying the `_handleError` method.

## Authentication

To set authentication token after login:

```dart
ApiService apiService = ApiService();
apiService.setAuthToken(token); // After successful login

// Clear token on logout
apiService.clearAuthToken();
```

## Environment Variables

1. Copy `.env.example` to `.env`
2. Update the backend URL if needed
3. Use a package like `flutter_dotenv` to load environment variables

## Troubleshooting

### 502 Bad Gateway Error
- Ensure the backend service is running on Kubernetes
- Check Kuberns dashboard for service status
- Verify the backend URL is correct

### Connection Timeout
- Check internet connectivity
- Increase timeout values in `ApiConfig` if backend is slow
- Verify server is accessible from your network

### CORS Issues
- Add CORS headers to Django backend
- In Django: `CORS_ALLOWED_ORIGINS` should include your app's origin

### 401 Unauthorized
- Token might have expired
- Implement token refresh logic
- Store token securely using Hive or Secure Storage

## Next Steps

1. Implement repository patterns for cleaner architecture
2. Add error handling and retry logic
3. Implement token refresh mechanism
4. Add unit and integration tests
5. Set up CI/CD with GitHub Actions
