import 'package:flutter/foundation.dart';
import 'package:dio/dio.dart';

import 'storage_service.dart';

class ApiException implements Exception {
  final String message;
  final int? statusCode;
  ApiException(this.message, {this.statusCode});

  @override
  String toString() => message;
}

class ApiService {
  static final String baseUrl = kIsWeb
      ? 'http://127.0.0.1:8000/api'
      : 'http://10.0.2.2:8000/api';
  static late Dio _dio;

  static void init() {
    _dio = Dio(BaseOptions(
      baseUrl: baseUrl,
      connectTimeout: const Duration(seconds: 30),
      receiveTimeout: const Duration(seconds: 30),
      headers: {'Content-Type': 'application/json'},
    ));

    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) async {
        final token = StorageService.getAccessToken();
        print('API Request: ${options.method} ${options.uri}');
        print('Token available: ${token != null}');
        if (token != null) {
          options.headers['Authorization'] = 'Bearer $token';
        }
        return handler.next(options);
      },
      onResponse: (response, handler) {
        print('API Response: ${response.statusCode} for ${response.requestOptions.uri}');
        return handler.next(response);
      },
      onError: (error, handler) async {
        print('API Error: ${error.type} ${error.message} for ${error.requestOptions.uri}');
        if (error.response?.statusCode == 401) {
          final refreshed = await _refreshToken();
          if (refreshed) {
            final token = StorageService.getAccessToken();
            if (token != null) {
              error.requestOptions.headers['Authorization'] = 'Bearer $token';
              final response = await _dio.fetch(error.requestOptions);
              return handler.resolve(response);
            }
          } else {
            await StorageService.clear();
          }
        }
        return handler.next(error);
      },
    ));

    _dio.interceptors.add(LogInterceptor(
      requestBody: true,
      responseBody: true,
      error: true,
      requestHeader: false,
      responseHeader: false,
    ));
  }

  static Future<bool> _refreshToken() async {
    final refresh = StorageService.getRefreshToken();
    if (refresh == null) return false;
    try {
      final response = await Dio().post(
        '$baseUrl/auth/refresh/',
        data: {'refresh': refresh},
      );
      await StorageService.saveTokens(
        accessToken: response.data['access'],
        refreshToken: response.data['refresh'] ?? refresh,
      );
      return true;
    } catch (_) {
      return false;
    }
  }

  static Map<String, dynamic> _extractData(Response response) {
    if (response.data is Map<String, dynamic>) {
      return response.data as Map<String, dynamic>;
    }
    return {'data': response.data};
  }

  static List<dynamic> _getListData(Map<String, dynamic> data, {String? key}) {
    final listData = key != null ? data[key] : null;
    if (listData is List) return List<dynamic>.from(listData);
    final fallbackData = data['results'] ?? data['data'];
    if (fallbackData is List) return List<dynamic>.from(fallbackData);
    return [];
  }

  static Future<Map<String, dynamic>> get(String endpoint,
      {Map<String, dynamic>? params}) async {
    try {
      print('ApiService: Making GET request to $endpoint');
      final response = await _dio.get(endpoint, queryParameters: params);
      print('ApiService: GET response status: ${response.statusCode}');
      final result = _extractData(response);
      print('ApiService: GET response data: $result');
      return result;
    } on DioException catch (e) {
      print('ApiService: GET error: ${e.message}');
      throw _handleError(e);
    }
  }

  static Future<Map<String, dynamic>> post(String endpoint,
      {Map<String, dynamic>? data}) async {
    try {
      final response = await _dio.post(endpoint, data: data);
      return _extractData(response);
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  static ApiException _handleError(DioException e) {
    if (e.type == DioExceptionType.connectionTimeout ||
        e.type == DioExceptionType.receiveTimeout) {
      return ApiException('Connection timed out. Please check your internet.');
    }
    if (e.response != null) {
      final data = e.response!.data;
      String message = 'Something went wrong.';
      if (data is Map && data.containsKey('detail')) {
        message = data['detail'];
      } else if (data is Map && data.containsKey('non_field_errors')) {
        final errors = data['non_field_errors'];
        if (errors is List && errors.isNotEmpty) {
          message = errors.first.toString();
        }
      }
      return ApiException(message, statusCode: e.response!.statusCode);
    }
    return ApiException('No internet connection.');
  }

  static Future<Map<String, dynamic>> login(
      String mobileNumber, String password) async {
    return post('/auth/login/',
        data: {'mobile_number': mobileNumber, 'password': password});
  }

  static Future<void> logout(String refreshToken) async {
    await post('/auth/logout/', data: {'refresh': refreshToken});
  }

  static Future<void> updateFcmToken(String token) async {
    await post('/auth/fcm-token/', data: {'fcm_token': token});
  }

  static Future<Map<String, dynamic>> getDashboard() async {
    return get('/student/dashboard/');
  }

  static Future<Map<String, dynamic>> getProfile() async {
    return get('/auth/profile/');
  }

  static Future<Map<String, dynamic>> getAttendanceSummary({int? year}) async {
    return get('/attendance/summary/', params: year != null ? {'year': year} : null);
  }

  static Future<List<dynamic>> getMonthlyAttendance(int month, int year) async {
    final data = await get('/attendance/monthly/', params: {'month': month, 'year': year});
    final attendanceData = data['attendance'] ?? data['data'] ?? [];
    return List<dynamic>.from(attendanceData);
  }

  static Future<List<dynamic>> getFees() async {
    final data = await get('/fees/');
    return List<dynamic>.from(data['results'] ?? []);
  }

  static Future<Map<String, dynamic>> getFeesSummary() async {
    return get('/fees/summary/');
  }

  static Future<List<dynamic>> getExams() async {
    final data = await get('/marks/exams/');
    return List<dynamic>.from(data['results'] ?? []);
  }

  static Future<Map<String, dynamic>> getResult(int examId) async {
    return get('/marks/result/', params: {'exam': examId});
  }

  static Future<List<dynamic>> getPerformance() async {
    final data = await get('/marks/performance/');
    return List<dynamic>.from(data['performance'] ?? []);
  }

  static Future<List<dynamic>> getSubjects() async {
    final data = await get('/subjects/');
    return List<dynamic>.from(data['results'] ?? []);
  }

  static Future<List<dynamic>> getChapters(int subjectId) async {
    final data = await get('/subjects/$subjectId/chapters/');
    return List<dynamic>.from(data['results'] ?? []);
  }

  static Future<List<dynamic>> getNotes({int? subject, int? chapter, String? type}) async {
    final params = <String, dynamic>{};
    if (subject != null) params['subject'] = subject;
    if (chapter != null) params['chapter'] = chapter;
    if (type != null) params['material_type'] = type;
    final data = await get('/study-materials/', params: params);
    return List<dynamic>.from(data['results'] ?? []);
  }

  static Future<Map<String, dynamic>> getTimetable({int? day}) async {
    return get('/timetable/', params: day != null ? {'day': day} : null);
  }

  static Future<List<dynamic>> getLectures({int? subject, int? chapter}) async {
    final params = <String, dynamic>{};
    if (subject != null) params['subject'] = subject;
    if (chapter != null) params['chapter'] = chapter;
    final data = await get('/lectures/', params: params);
    return List<dynamic>.from(data['results'] ?? []);
  }

  static Future<List<dynamic>> getGalleryCategories() async {
    final data = await get('/gallery-categories/');
    return List<dynamic>.from(data is List ? data : (data['results'] ?? []));
  }

  static Future<List<dynamic>> getGallery({int? category, String? type}) async {
    final params = <String, dynamic>{};
    if (category != null) params['category'] = category;
    if (type != null) params['media_type'] = type;
    final data = await get('/gallery/', params: params);
    return List<dynamic>.from(data is List ? data : (data['results'] ?? []));
  }

  static Future<List<dynamic>> getTeachers({String? search}) async {
    final data = await get('/teachers/', params: search != null ? {'search': search} : null);
    return List<dynamic>.from(data['results'] ?? []);
  }

  static Future<List<dynamic>> getQuestionPapers(
      {int? subject, int? year, String? examType}) async {
    final params = <String, dynamic>{};
    if (subject != null) params['subject'] = subject;
    if (year != null) params['year'] = year;
    if (examType != null) params['exam_type'] = examType;
    final data = await get('/question-papers/', params: params);
    return List<dynamic>.from(data['results'] ?? []);
  }

  static Future<List<dynamic>> getNotifications() async {
    final data = await get('/notifications/');
    return _getListData(data);
  }

  static Future<void> markNotificationRead(int id) async {
    await post('/notifications/$id/mark_read/');
  }

  static Future<void> markAllRead() async {
    await post('/notifications/mark_all_read/');
  }

  static Future<List<dynamic>> getNotesList() async {
    final data = await get('/notes/');
    return List<dynamic>.from(data['results'] ?? []);
  }

  static Future<List<dynamic>> getReceipts() async {
    final data = await get('/receipts/');
    return List<dynamic>.from(data['results'] ?? []);
  }
}
