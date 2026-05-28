/// API Configuration
/// This file contains all API endpoint configurations
class ApiConfig {
  // Base URL of the backend server
  static const String baseUrl = 'https://vidyaniketan-app-main-f58e2f6.kuberns.cloud';
  
  // API version
  static const String apiVersion = '/api';
  
  // Complete API base URL
  static const String apiBaseUrl = '$baseUrl$apiVersion';
  
  // API Endpoints
  static const String adminEndpoint = '$baseUrl/admin';
  
  // Auth Endpoints
  static const String loginEndpoint = '$apiBaseUrl/login';
  static const String registerEndpoint = '$apiBaseUrl/register';
  static const String logoutEndpoint = '$apiBaseUrl/logout';
  static const String profileEndpoint = '$apiBaseUrl/profile';
  
  // Student Endpoints
  static const String studentsEndpoint = '$apiBaseUrl/students';
  static const String studentDetailsEndpoint = '$apiBaseUrl/students';
  
  // Parent Endpoints
  static const String parentsEndpoint = '$apiBaseUrl/parents';
  static const String parentDetailsEndpoint = '$apiBaseUrl/parents';
  
  // Class Endpoints
  static const String classesEndpoint = '$apiBaseUrl/classes';
  
  // Assignment Endpoints
  static const String assignmentsEndpoint = '$apiBaseUrl/assignments';
  
  // Grade Endpoints
  static const String gradesEndpoint = '$apiBaseUrl/grades';
  
  // Attendance Endpoints
  static const String attendanceEndpoint = '$apiBaseUrl/attendance';
  
  // Notification Endpoints
  static const String notificationsEndpoint = '$apiBaseUrl/notifications';
  
  // Timeout duration in seconds
  static const int connectTimeout = 30;
  static const int receiveTimeout = 30;
  static const int sendTimeout = 30;
}
