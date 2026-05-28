import 'package:flutter/foundation.dart';

import '../services/api_service.dart';
import '../services/storage_service.dart';

class AuthProvider extends ChangeNotifier {
  Map<String, dynamic>? _user;
  bool _isLoading = false;
  String? _error;

  Map<String, dynamic>? get user => _user;
  bool get isLoading => _isLoading;
  String? get error => _error;
  bool get isLoggedIn => StorageService.isLoggedIn;

  void _setLoading(bool value) {
    _isLoading = value;
    notifyListeners();
  }

  Future<bool> login(String mobileNumber, String password) async {
    _setLoading(true);
    _error = null;
    try {
      final response = await ApiService.login(mobileNumber, password);
      await StorageService.saveTokens(
        accessToken: response['access'],
        refreshToken: response['refresh'],
      );
      _user = response['user'] as Map<String, dynamic>?;
      if (_user == null) {
        _user = await ApiService.getProfile();
      }
      if (_user != null) {
        await StorageService.saveUserData(_user!);
      }
      // TODO: Register FCM token when Firebase is available
      // _registerFcmToken();
      _setLoading(false);
      return _user != null;
    } catch (e) {
      _error = e.toString();
      _setLoading(false);
      return false;
    }
  }

  Future<void> logout() async {
    _setLoading(true);
    try {
      final refresh = StorageService.getRefreshToken();
      if (refresh != null) {
        await ApiService.logout(refresh);
      }
    } catch (_) {}
    await StorageService.clear();
    _user = null;
    _setLoading(false);
    notifyListeners();
  }

  Future<void> loadUserData() async {
    _user = StorageService.getUserData();
    notifyListeners();
  }

  Future<void> refreshUserProfile() async {
    try {
      final profile = await ApiService.getProfile();
      _user = profile;
      await StorageService.saveUserData(_user!);
      notifyListeners();
    } catch (_) {}
  }

  // TODO: Implement FCM token registration when Firebase is added
  // void _registerFcmToken() async {
  //   try {
  //     final messaging = FirebaseMessaging.instance;
  //     await messaging.requestPermission();
  //     final token = await messaging.getToken();
  //     if (token != null) {
  //       await ApiService.updateFcmToken(token);
  //     }
  //   } catch (_) {}
  // }
}
