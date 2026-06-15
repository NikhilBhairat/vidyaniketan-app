import 'package:flutter/foundation.dart';

/// API Configuration with multiple fallback URLs
/// This file contains all API endpoint configurations with support for multiple environments
class ApiConfig {
  // Primary URL - Production Render (UPDATED FOR YOUR LIVE BACKEND)
  static const String _productionUrl =
      'https://vidyaniketan-app-2.onrender.com';

  // Optional runtime override: flutter run --dart-define=API_BASE_URL=https://example.com
  static const String _runtimeBaseUrl =
      String.fromEnvironment('API_BASE_URL', defaultValue: '');

  // Fallback URLs for local development
  static const String _localhostUrl = 'http://localhost:8000';
  static const String _localIpUrl =
      'http://192.168.1.100:8000'; // Change to your machine IP
  static const String _emulatorUrl = 'http://10.0.2.2:8000'; // Android emulator

  // Use this to switch environments
  // Change to _localhostUrl, _localIpUrl, or _emulatorUrl for testing
  static const String baseUrl = _productionUrl;

  // For easy switching between environments
  static const bool USE_LOCAL_BACKEND = false; // Set to true for local testing

  static String getBaseUrl() {
    if (_runtimeBaseUrl.trim().isNotEmpty) {
      return _runtimeBaseUrl.trim();
    }
    if (USE_LOCAL_BACKEND) {
      return _localhostUrl; // Change this to _localIpUrl or _emulatorUrl as needed
    }
    return baseUrl;
  }

  static String _normalizeBaseUrl(String url) {
    return url.endsWith('/') ? url.substring(0, url.length - 1) : url;
  }

  // Keeps production as primary, then tries local options as fallback.
  static List<String> get apiBaseUrlCandidates {
    final rawBaseUrls = kIsWeb
        ? <String>[
            getBaseUrl(),
            _localhostUrl,
            _localIpUrl,
            _productionUrl,
          ]
        : <String>[
            getBaseUrl(),
            _emulatorUrl,
            _localIpUrl,
            _localhostUrl,
            _productionUrl,
          ];

    final normalized = <String>[];
    for (final url in rawBaseUrls) {
      final clean = _normalizeBaseUrl(url);
      if (!normalized.contains(clean)) {
        normalized.add(clean);
      }
    }

    return normalized.map((url) => '$url$apiVersion').toList();
  }

  // API version (Fixed to ensure it begins with a slash properly)
  static const String apiVersion = '/api';

  // Complete API base URL
  static String get apiBaseUrl => '${getBaseUrl()}$apiVersion';

  // API Endpoints - Admin
  static String get adminEndpoint => '${getBaseUrl()}/admin';

  // Auth Endpoints
  static String get loginEndpoint => '$apiBaseUrl/auth/login/';
  static String get registerEndpoint => '$apiBaseUrl/auth/register/';
  static String get logoutEndpoint => '$apiBaseUrl/auth/logout/';
  static String get profileEndpoint => '$apiBaseUrl/auth/profile/';
  static String get refreshTokenEndpoint => '$apiBaseUrl/auth/refresh/';
  static String get fcmTokenEndpoint => '$apiBaseUrl/auth/fcm-token/';

  // Student Endpoints
  static String get studentsEndpoint => '$apiBaseUrl/students';
  static String get studentDetailsEndpoint => '$apiBaseUrl/students';
  static String get studentDashboardEndpoint =>
      '$apiBaseUrl/student/dashboard/';

  // Parent Endpoints
  static String get parentsEndpoint => '$apiBaseUrl/parents';
  static String get parentDetailsEndpoint => '$apiBaseUrl/parents';

  // Class Endpoints
  static String get classesEndpoint => '$apiBaseUrl/classes';

  // Assignment Endpoints
  static String get assignmentsEndpoint => '$apiBaseUrl/assignments';

  // Grade Endpoints
  static String get gradesEndpoint => '$apiBaseUrl/grades';

  // Attendance Endpoints
  static String get attendanceEndpoint => '$apiBaseUrl/attendance';
  static String get attendanceSummaryEndpoint =>
      '$apiBaseUrl/attendance/summary/';
  static String get attendanceMonthlyEndpoint =>
      '$apiBaseUrl/attendance/monthly/';

  // Fees Endpoints
  static String get feesEndpoint => '$apiBaseUrl/fees';
  static String get feesSummaryEndpoint => '$apiBaseUrl/fees/summary/';
  static String get receiptsEndpoint => '$apiBaseUrl/receipts/';

  // Exams & Marks Endpoints
  static String get examsEndpoint => '$apiBaseUrl/exams';
  static String get marksEndpoint => '$apiBaseUrl/marks';
  static String get marksExamsEndpoint => '$apiBaseUrl/marks/exams/';
  static String get marksResultEndpoint => '$apiBaseUrl/marks/result/';
  static String get marksPerformanceEndpoint =>
      '$apiBaseUrl/marks/performance/';

  // Notification Endpoints
  static String get notificationsEndpoint => '$apiBaseUrl/notifications';
  static String get notificationUnreadCountEndpoint =>
      '$apiBaseUrl/notifications/unread_count/';

  // Lectures & Gallery Endpoints
  static String get lecturesEndpoint => '$apiBaseUrl/lectures';
  static String get galleryEndpoint => '$apiBaseUrl/gallery';
  static String get galleryCategoriesEndpoint =>
      '$apiBaseUrl/gallery-categories/';
  static String get questionPapersEndpoint => '$apiBaseUrl/question-papers';

  // Notes & Others Endpoints
  static String get notesEndpoint => '$apiBaseUrl/notes/';
  static String get dashboardStatsEndpoint => '$apiBaseUrl/dashboard/stats/';

  // Timeout duration in seconds
  static const int connectTimeout = 30;
  static const int receiveTimeout = 30;
  static const int sendTimeout = 30;

  // Retry configuration
  static const int maxRetries = 3;
  static const int retryDelay = 1000; // milliseconds

  // Additional configuration
  static const bool enableLogging = true;
  static const bool validateSSL =
      true; // Set to false for local development with self-signed certs
}
