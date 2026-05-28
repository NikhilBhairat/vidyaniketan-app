import 'package:flutter/foundation.dart';
import 'dart:async';

import '../services/api_service.dart';

class NotificationProvider extends ChangeNotifier {
  List<Map<String, dynamic>> _notifications = [];
  int _unreadCount = 0;
  bool _isLoading = false;
  Timer? _pollTimer;
  static const Duration _pollInterval = Duration(seconds: 30);

  List<Map<String, dynamic>> get notifications => _notifications;
  int get unreadCount => _unreadCount;
  bool get isLoading => _isLoading;

  Future<void> fetchNotifications() async {
    _isLoading = true;
    notifyListeners();
    try {
      print('NotificationProvider: Fetching notifications...');
      final data = await ApiService.getNotifications();
      print('NotificationProvider: Received data: $data');
      _notifications = List<Map<String, dynamic>>.from(data);
      _unreadCount = _notifications.where((n) => n['is_read'] == false).length;
      print('NotificationProvider: Processed ${_notifications.length} notifications, $_unreadCount unread');
    } catch (e) {
      print('NotificationProvider: Error fetching notifications: $e');
      _notifications = [];
      _unreadCount = 0;
    }
    _isLoading = false;
    notifyListeners();
  }

  Future<void> markRead(int id) async {
    await ApiService.markNotificationRead(id);
    final idx = _notifications.indexWhere((n) => n['id'] == id);
    if (idx != -1) {
      _notifications[idx]['is_read'] = true;
      _unreadCount = _notifications.where((n) => n['is_read'] == false).length;
      notifyListeners();
    }
  }

  Future<void> markAllRead() async {
    await ApiService.markAllRead();
    for (var n in _notifications) {
      n['is_read'] = true;
    }
    _unreadCount = 0;
    notifyListeners();
  }

  void startPolling() {
    print('NotificationProvider: Starting auto-polling');
    _pollTimer?.cancel();
    _pollTimer = Timer.periodic(_pollInterval, (_) async {
      try {
        final data = await ApiService.getNotifications();
        final newNotifications = List<Map<String, dynamic>>.from(data);
        if (newNotifications.length != _notifications.length ||
            (newNotifications.isNotEmpty && newNotifications.first['id'] != _notifications.firstOrNull?['id'])) {
          print('NotificationProvider: New notifications detected via polling');
          _notifications = newNotifications;
          _unreadCount = _notifications.where((n) => n['is_read'] == false).length;
          notifyListeners();
        }
      } catch (e) {
        print('NotificationProvider: Polling error: $e');
      }
    });
  }

  void stopPolling() {
    print('NotificationProvider: Stopping auto-polling');
    _pollTimer?.cancel();
    _pollTimer = null;
  }

  @override
  void dispose() {
    stopPolling();
    super.dispose();
  }
}
