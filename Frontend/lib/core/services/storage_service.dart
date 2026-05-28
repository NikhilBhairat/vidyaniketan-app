import 'dart:convert';
import 'package:hive_flutter/hive_flutter.dart';

class StorageService {
  static late Box _box;
  static const String _tokenBox = 'auth_tokens';

  static Future<void> init() async {
    await Hive.initFlutter();
    _box = await Hive.openBox(_tokenBox);
  }

  static Future<void> saveTokens({
    required String accessToken,
    required String refreshToken,
  }) async {
    await _box.put('access_token', accessToken);
    await _box.put('refresh_token', refreshToken);
  }

  static String? getAccessToken() => _box.get('access_token');
  static String? getRefreshToken() => _box.get('refresh_token');

  static Future<void> saveUserData(Map<String, dynamic> data) async {
    await _box.put('user_data', jsonEncode(data));
  }

  static Map<String, dynamic>? getUserData() {
    final data = _box.get('user_data');
    if (data == null) return null;
    return Map<String, dynamic>.from(jsonDecode(data));
  }

  static Future<void> clear() async {
    await _box.clear();
  }

  static bool get isLoggedIn => getAccessToken() != null;
}
