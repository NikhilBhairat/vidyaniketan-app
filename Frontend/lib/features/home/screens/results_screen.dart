import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../core/providers/auth_provider.dart';
import '../../../core/services/api_service.dart';
import '../../../main.dart';

class ResultsScreen extends StatefulWidget {
  const ResultsScreen({super.key});

  @override
  State<ResultsScreen> createState() => _ResultsScreenState();
}

class _ResultsScreenState extends State<ResultsScreen> {
  List<dynamic> _exams = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadExams();
  }

  Future<void> _loadExams() async {
    setState(() => _isLoading = true);
    try {
      _exams = await ApiService.getExams();
    } catch (_) {
      setState(() => _exams = []);
    }
    setState(() => _isLoading = false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F7FA),
      appBar: AppBar(
        title: const Text('Results'),
        actions: [
          IconButton(icon: const Icon(Icons.refresh), onPressed: _loadExams),
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () {
              context.read<AuthProvider>().logout();
              Navigator.pushReplacementNamed(context, AppRouter.login);
            },
          ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _exams.isEmpty
              ? const Center(child: Text('No exams available.'))
              : RefreshIndicator(
                  onRefresh: _loadExams,
                  child: ListView.builder(
                    padding: const EdgeInsets.all(16),
                    itemCount: _exams.length,
                    itemBuilder: (context, index) {
                      final exam = _exams[index];
                      return Card(
                        margin: const EdgeInsets.only(bottom: 12),
                        child: ListTile(
                          title: Text(exam['name'] ?? ''),
                          subtitle: Text('${exam['exam_type']} - ${exam['standard']}'),
                          trailing: const Icon(Icons.arrow_forward),
                          onTap: () => _viewResult(exam['id']),
                        ),
                      );
                    },
                  ),
                ),
    );
  }

  void _viewResult(int examId) async {
    try {
      final result = await ApiService.getResult(examId);
      // Show result dialog or navigate
      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          title: const Text('Exam Result'),
          content: Text('Marks: ${result['total_marks'] ?? 'N/A'}'),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('OK'),
            ),
          ],
        ),
      );
    } catch (_) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Unable to load result')),
      );
    }
  }
}