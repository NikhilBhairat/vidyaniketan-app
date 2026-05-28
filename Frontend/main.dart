import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Vidyaniketan',
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Vidyaniketan'),
        ),
        body: const Center(
          child: Text(
            'Flutter APK Build Successful!',
            style: TextStyle(fontSize: 20),
          ),
        ),
      ),
    );
  }
}
