import 'package:flutter/foundation.dart';
import 'package:vidyaniketan_app/services/api_service.dart';

/// Provider for API Service
/// Use this with Provider package for dependency injection
class ApiProvider extends ChangeNotifier {
  late ApiService _apiService;
  bool _isLoading = false;
  String? _error;
  
  ApiProvider() {
    _apiService = ApiService();
  }
  
  // Getters
  ApiService get apiService => _apiService;
  bool get isLoading => _isLoading;
  String? get error => _error;
  
  // Setters
  void setLoading(bool value) {
    _isLoading = value;
    notifyListeners();
  }
  
  void setError(String? error) {
    _error = error;
    notifyListeners();
  }
  
  void clearError() {
    _error = null;
    notifyListeners();
  }
  
  /// Set authentication token
  void setAuthToken(String token) {
    _apiService.setAuthToken(token);
  }
  
  /// Clear authentication token
  void clearAuthToken() {
    _apiService.clearAuthToken();
  }
}
