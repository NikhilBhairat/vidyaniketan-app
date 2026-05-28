import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'core/theme/app_theme.dart';
import 'core/services/api_service.dart';
import 'core/services/storage_service.dart';
import 'core/providers/auth_provider.dart';
import 'core/providers/notification_provider.dart';
import 'features/auth/screens/login_screen.dart';
import 'features/home/screens/gallery_screen.dart';
import 'features/home/screens/fees_screen.dart';
import 'features/home/screens/home_screen.dart';
import 'features/home/screens/notes_screen.dart';
import 'features/home/screens/receipt_screen.dart';
import 'features/home/screens/results_screen.dart';
import 'features/splash/splash_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await StorageService.init();
  ApiService.init();
  runApp(const EduApp());
}

class EduApp extends StatelessWidget {
  const EduApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AuthProvider()),
        ChangeNotifierProvider(create: (_) => NotificationProvider()),
      ],
      child: MaterialApp(
        title: 'Vidyaniketan Classes & Academy',
        debugShowCheckedModeBanner: false,
        theme: AppTheme.lightTheme,
        darkTheme: AppTheme.darkTheme,
        themeMode: ThemeMode.light,
        initialRoute: AppRouter.splash,
        onGenerateRoute: AppRouter.generateRoute,
      ),
    );
  }
}

class AppRouter {
  static const String splash = '/';
  static const String login = '/login';
  static const String home = '/home';
  static const String attendance = '/attendance';
  static const String fees = '/fees';
  static const String marks = '/marks';
  static const String notes = '/notes';
  static const String receipts = '/receipts';
  static const String timetable = '/timetable';
  static const String gallery = '/gallery';
  static const String lectures = '/lectures';
  static const String profile = '/profile';
  static const String notifications = '/notifications';
  static const String teachers = '/teachers';
  static const String questionPapers = '/question-papers';

  static Route<dynamic> generateRoute(RouteSettings settings) {
    switch (settings.name) {
      case splash:
        return MaterialPageRoute(builder: (_) => const SplashScreen());
      case login:
        return MaterialPageRoute(builder: (_) => const LoginScreen());
      case home:
        return MaterialPageRoute(builder: (_) => const HomeScreen());
      case notes:
        return MaterialPageRoute(builder: (_) => const NotesScreen());
      case marks:
        return MaterialPageRoute(builder: (_) => const ResultsScreen());
      case fees:
        return MaterialPageRoute(builder: (_) => const FeesScreen());
      case gallery:
        return MaterialPageRoute(builder: (_) => const GalleryScreen());
      case receipts:
        return MaterialPageRoute(builder: (_) => const ReceiptScreen());
      default:
        return MaterialPageRoute(
          builder: (_) => Scaffold(
            appBar: AppBar(title: const Text('Coming Soon')),
            body: Center(child: Text('Route ${settings.name} not implemented yet')),
          ),
        );
    }
  }
}
