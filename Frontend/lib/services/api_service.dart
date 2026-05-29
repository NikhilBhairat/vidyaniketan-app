import 'package:dio/dio.dart';
import 'package:vidyaniketan_app/config/api_config.dart';

/// Enhanced API Service for handling all HTTP requests with retry logic and better error handling
class ApiService {
  late Dio _dio;
  int _retryCount = 0;
  
  ApiService() {
    _initDio();
  }
  
  /// Initialize Dio with configurations
  void _initDio() {
    _dio = Dio(
      BaseOptions(
        baseUrl: ApiConfig.apiBaseUrl,
        connectTimeout: Duration(seconds: ApiConfig.connectTimeout),
        receiveTimeout: Duration(seconds: ApiConfig.receiveTimeout),
        sendTimeout: Duration(seconds: ApiConfig.sendTimeout),
        contentType: 'application/json',
        validateStatus: (status) {
          return status != null && status < 500;
        },
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
      ),
    );
    
    // Add interceptors
    _addInterceptors();
  }
  
  /// Add request/response interceptors with logging
  void _addInterceptors() {
    _dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) {
          if (ApiConfig.enableLogging) {
            print('═══════════════════════════════════════════');
            print('🔵 API REQUEST');
            print('Method: ${options.method}');
            print('URL: ${options.uri}');
            if (options.data != null) {
              print('Data: ${options.data}');
            }
            print('Headers: ${options.headers}');
            print('═══════════════════════════════════════════');
          }
          return handler.next(options);
        },
        onResponse: (response, handler) {
          if (ApiConfig.enableLogging) {
            print('═══════════════════════════════════════════');
            print('✅ API RESPONSE');
            print('Status Code: ${response.statusCode}');
            print('URL: ${response.requestOptions.uri}');
            print('Response: ${response.data}');
            print('═══════════════════════════════════════════');
          }
          _retryCount = 0;
          return handler.next(response);
        },
        onError: (DioException e, handler) {
          _handleError(e);
          return handler.next(e);
        },
      ),
    );
  }
  
  /// Handle DIO errors with detailed logging
  void _handleError(DioException error) {
    if (ApiConfig.enableLogging) {
      print('═══════════════════════════════════════════');
      print('❌ API ERROR');
      print('Error Type: ${error.type}');
      print('Message: ${error.message}');
      print('Response Code: ${error.response?.statusCode}');
      print('Response Data: ${error.response?.data}');
      print('Request URL: ${error.requestOptions.uri}');
      print('Base URL: ${_dio.options.baseUrl}');
      
      switch (error.type) {
        case DioExceptionType.connectionTimeout:
          print('⏱️ Issue: Backend server not responding (Connection Timeout)');
          print('Fix: Check if backend is running and accessible from your network');
          break;
        case DioExceptionType.receiveTimeout:
          print('⏱️ Issue: Backend server is slow to respond (Receive Timeout)');
          print('Fix: Backend might be overloaded or slow network');
          break;
        case DioExceptionType.badResponse:
          print('❌ Issue: Server returned error status ${error.response?.statusCode}');
          break;
        case DioExceptionType.badCertificate:
          print('🔒 Issue: SSL Certificate validation failed');
          print('Fix: Backend might have invalid/self-signed certificate');
          break;
        case DioExceptionType.unknown:
          print('🔌 Issue: Network error - Backend URL might be unreachable');
          print('Fix: Check if backend domain/IP is correct and accessible');
          break;
        default:
          print('Other error: ${error.type}');
      }
      print('═══════════════════════════════════════════');
    }
  }
  
  /// GET request with retry logic
  Future<Response> get(
    String path, {
    Map<String, dynamic>? queryParameters,
    Options? options,
    CancelToken? cancelToken,
    ProgressCallback? onReceiveProgress,
  }) async {
    try {
      return await _dio.get(
        path,
        queryParameters: queryParameters,
        options: options,
        cancelToken: cancelToken,
        onReceiveProgress: onReceiveProgress,
      );
    } on DioException catch (e) {
      if (_shouldRetry(e) && _retryCount < ApiConfig.maxRetries) {
        _retryCount++;
        if (ApiConfig.enableLogging) {
          print('🔄 Retrying request... (Attempt $_retryCount/${ApiConfig.maxRetries})');
        }
        await Future.delayed(Duration(milliseconds: ApiConfig.retryDelay));
        return get(path, queryParameters: queryParameters, options: options, cancelToken: cancelToken, onReceiveProgress: onReceiveProgress);
      }
      rethrow;
    }
  }
  
  /// POST request with retry logic
  Future<Response> post(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
    CancelToken? cancelToken,
    ProgressCallback? onSendProgress,
    ProgressCallback? onReceiveProgress,
  }) async {
    try {
      return await _dio.post(
        path,
        data: data,
        queryParameters: queryParameters,
        options: options,
        cancelToken: cancelToken,
        onSendProgress: onSendProgress,
        onReceiveProgress: onReceiveProgress,
      );
    } on DioException catch (e) {
      if (_shouldRetry(e) && _retryCount < ApiConfig.maxRetries) {
        _retryCount++;
        if (ApiConfig.enableLogging) {
          print('🔄 Retrying request... (Attempt $_retryCount/${ApiConfig.maxRetries})');
        }
        await Future.delayed(Duration(milliseconds: ApiConfig.retryDelay));
        return post(path, data: data, queryParameters: queryParameters, options: options, cancelToken: cancelToken, onSendProgress: onSendProgress, onReceiveProgress: onReceiveProgress);
      }
      rethrow;
    }
  }
  
  /// PUT request
  Future<Response> put(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
    CancelToken? cancelToken,
    ProgressCallback? onSendProgress,
    ProgressCallback? onReceiveProgress,
  }) async {
    return await _dio.put(
      path,
      data: data,
      queryParameters: queryParameters,
      options: options,
      cancelToken: cancelToken,
      onSendProgress: onSendProgress,
      onReceiveProgress: onReceiveProgress,
    );
  }
  
  /// DELETE request
  Future<Response> delete(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
    CancelToken? cancelToken,
  }) async {
    return await _dio.delete(
      path,
      data: data,
      queryParameters: queryParameters,
      options: options,
      cancelToken: cancelToken,
    );
  }
  
  /// PATCH request
  Future<Response> patch(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
    CancelToken? cancelToken,
    ProgressCallback? onSendProgress,
    ProgressCallback? onReceiveProgress,
  }) async {
    return await _dio.patch(
      path,
      data: data,
      queryParameters: queryParameters,
      options: options,
      cancelToken: cancelToken,
      onSendProgress: onSendProgress,
      onReceiveProgress: onReceiveProgress,
    );
  }
  
  /// Determine if request should be retried
  bool _shouldRetry(DioException error) {
    return error.type == DioExceptionType.connectionTimeout ||
        error.type == DioExceptionType.receiveTimeout ||
        (error.response?.statusCode ?? 0) >= 500;
  }
  
  /// Set authorization token
  void setAuthToken(String token) {
    _dio.options.headers['Authorization'] = 'Bearer $token';
    if (ApiConfig.enableLogging) {
      print('✅ Auth token set');
    }
  }
  
  /// Clear authorization token
  void clearAuthToken() {
    _dio.options.headers.remove('Authorization');
    if (ApiConfig.enableLogging) {
      print('🔓 Auth token cleared');
    }
  }
  
  /// Get Dio instance (useful for advanced operations)
  Dio getDioInstance() {
    return _dio;
  }
  
  /// Test backend connectivity
  Future<bool> testConnection() async {
    try {
      final response = await _dio.get(
        '${ApiConfig.getBaseUrl()}/api/',
        options: Options(
          connectTimeout: const Duration(seconds: 5),
          receiveTimeout: const Duration(seconds: 5),
        ),
      );
      if (ApiConfig.enableLogging) {
        print('✅ Backend is reachable');
      }
      return true;
    } catch (e) {
      if (ApiConfig.enableLogging) {
        print('❌ Backend is not reachable: $e');
      }
      return false;
    }
  }
}
