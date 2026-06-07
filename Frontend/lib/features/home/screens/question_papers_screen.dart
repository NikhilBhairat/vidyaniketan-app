import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:url_launcher/url_launcher_string.dart';

import '../../../core/providers/auth_provider.dart';
import '../../../core/services/api_service.dart';
import '../../../main.dart';

class QuestionPapersScreen extends StatefulWidget {
  const QuestionPapersScreen({super.key});

  @override
  State<QuestionPapersScreen> createState() => _QuestionPapersScreenState();
}

class _QuestionPapersScreenState extends State<QuestionPapersScreen> {
  List<dynamic> _papers = [];
  bool _isLoading = true;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _loadPapers();
  }

  Future<void> _loadPapers() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });
    try {
      _papers = await ApiService.getQuestionPapers();
    } catch (e) {
      _errorMessage = e.toString();
    }
    if (mounted) {
      setState(() => _isLoading = false);
    }
  }

  String? _resolveUrl(dynamic rawUrl) {
    final value = rawUrl?.toString();
    if (value == null || value.trim().isEmpty) return null;

    final trimmed = value.trim();
    final parsed = Uri.tryParse(trimmed);
    if (parsed == null) return null;

    final configuredBaseUri = Uri.tryParse(ApiService.activeBaseUrl);

    if (parsed.hasScheme) {
      final shouldRewriteHost = parsed.host == 'localhost' ||
          parsed.host == '127.0.0.1' ||
          parsed.host == '10.0.2.2';

      if (shouldRewriteHost && configuredBaseUri != null) {
        final rewritten = parsed.replace(
          scheme: configuredBaseUri.scheme,
          host: configuredBaseUri.host,
          port: configuredBaseUri.hasPort ? configuredBaseUri.port : null,
        );
        return rewritten.toString();
      }

      return trimmed;
    }

    final base = ApiService.activeBaseUrl;
    final normalizedBase =
        base.endsWith('/') ? base.substring(0, base.length - 1) : base;
    final normalizedPath = trimmed.startsWith('/') ? trimmed : '/$trimmed';
    return '$normalizedBase$normalizedPath';
  }

  Future<void> _openPaper(dynamic paper) async {
    final fileUrl = _resolveUrl(paper['file']);
    if (fileUrl == null) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Question paper file not available.')),
      );
      return;
    }

    final opened = await launchUrlString(
      fileUrl,
      mode: LaunchMode.externalApplication,
    );

    if (!opened && mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Unable to open question paper.')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F7FA),
      appBar: AppBar(
        title: const Text('Question Papers'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _loadPapers,
          ),
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
          : _errorMessage != null
              ? Center(
                  child: Padding(
                    padding: const EdgeInsets.all(20),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(Icons.error_outline,
                            color: Colors.redAccent, size: 40),
                        const SizedBox(height: 12),
                        const Text('Unable to load question papers.'),
                        const SizedBox(height: 8),
                        Text(
                          _errorMessage!,
                          textAlign: TextAlign.center,
                          style: const TextStyle(color: Colors.black54),
                        ),
                        const SizedBox(height: 16),
                        ElevatedButton(
                          onPressed: _loadPapers,
                          child: const Text('Retry'),
                        ),
                      ],
                    ),
                  ),
                )
          : _papers.isEmpty
              ? const Center(child: Text('No question papers available.'))
              : RefreshIndicator(
                  onRefresh: _loadPapers,
                  child: ListView.builder(
                    padding: const EdgeInsets.all(16),
                    itemCount: _papers.length,
                    itemBuilder: (context, index) {
                      final paper = _papers[index];
                      return Card(
                        margin: const EdgeInsets.only(bottom: 12),
                        child: ListTile(
                          leading: const Icon(Icons.description_outlined,
                              color: Color(0xFF1A237E)),
                          title: Text(paper['title']?.toString() ?? 'Question Paper'),
                          subtitle: Text(
                            '${paper['subject'] ?? '-'} • ${paper['standard'] ?? '-'} • ${paper['year'] ?? '-'}',
                          ),
                          trailing: const Icon(Icons.open_in_new),
                          onTap: () => _openPaper(paper),
                        ),
                      );
                    },
                  ),
                ),
    );
  }
}
