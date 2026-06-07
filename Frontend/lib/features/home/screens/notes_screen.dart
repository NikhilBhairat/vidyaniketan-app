import 'dart:io';

import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:open_filex/open_filex.dart';
import 'package:path_provider/path_provider.dart';
import 'package:provider/provider.dart';
import 'package:url_launcher/url_launcher_string.dart';

import '../../../core/providers/auth_provider.dart';
import '../../../core/services/api_service.dart';
import '../../../main.dart';

class NotesScreen extends StatefulWidget {
  const NotesScreen({super.key});

  @override
  State<NotesScreen> createState() => _NotesScreenState();
}

class _NotesScreenState extends State<NotesScreen> {
  List<dynamic> _notes = [];
  bool _isLoading = true;
  String? _errorMessage;
  String? _selectedSubject;
  String? _selectedChapter;
  String? _studentStandard;

  @override
  void initState() {
    super.initState();
    _loadNotes();
  }

  Future<void> _loadNotes() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });
    try {
      _notes = await ApiService.getNotesList(
        subject: _selectedSubject,
        chapter: _selectedChapter,
      );
    } catch (e) {
      _notes = [];
      _errorMessage = e.toString();
    }

    try {
      final dashboard = await ApiService.getDashboard();
      _studentStandard = dashboard['standard']?.toString();
    } catch (_) {}

    setState(() => _isLoading = false);
  }

  Future<void> _clearFilters() async {
    _selectedSubject = null;
    _selectedChapter = null;
    await _loadNotes();
  }

  String? _resolvePdfUrl(Map<String, dynamic> note) {
    final raw = (note['pdf_file_url'] ?? note['pdf_file'])?.toString();
    if (raw == null || raw.trim().isEmpty) return null;

    final value = raw.trim();
    final parsed = Uri.tryParse(value);
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

      return value;
    }

    final base = ApiService.activeBaseUrl;
    final normalizedBase =
        base.endsWith('/') ? base.substring(0, base.length - 1) : base;
    final normalizedPath = value.startsWith('/') ? value : '/$value';
    return '$normalizedBase$normalizedPath';
  }

  Future<void> _previewPdf(Map<String, dynamic> note) async {
    final url = _resolvePdfUrl(note);
    if (url == null) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('PDF is not available for this note.')),
      );
      return;
    }

    final opened =
        await launchUrlString(url, mode: LaunchMode.externalApplication);
    if (!opened && mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Could not open PDF preview.')),
      );
    }
  }

  Future<void> _downloadPdf(Map<String, dynamic> note) async {
    final url = _resolvePdfUrl(note);
    if (url == null) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('PDF is not available for this note.')),
      );
      return;
    }

    final tempName = (note['title']?.toString().trim().isNotEmpty ?? false)
        ? note['title']
            .toString()
            .trim()
            .replaceAll(RegExp(r'[^A-Za-z0-9_-]'), '_')
        : 'note';
    final fileName = '${tempName}_${DateTime.now().millisecondsSinceEpoch}.pdf';

    if (kIsWeb) {
      final opened = await launchUrlString(url, webOnlyWindowName: '_blank');
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            opened
                ? 'Opened PDF in browser. Use browser download to save it.'
                : 'Could not open PDF in browser.',
          ),
        ),
      );
      return;
    }

    try {
      final dir = await getApplicationDocumentsDirectory();
      final savePath = '${dir.path}${Platform.pathSeparator}$fileName';

      await Dio().download(url, savePath);

      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Downloaded: $fileName'),
          action: SnackBarAction(
            label: 'Open',
            onPressed: () {
              OpenFilex.open(savePath);
            },
          ),
        ),
      );
    } catch (error) {
      final opened = await launchUrlString(url, mode: LaunchMode.externalApplication);
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            opened
                ? 'Could not save locally. Opened PDF in browser/app instead.'
                : 'Failed to download PDF: $error',
          ),
        ),
      );
    }
  }

  Future<void> _showNoteActions(Map<String, dynamic> note) async {
    await showModalBottomSheet<void>(
      context: context,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(18)),
      ),
      builder: (context) {
        final hasPdf = _resolvePdfUrl(note) != null;
        return SafeArea(
          child: Padding(
            padding: const EdgeInsets.symmetric(vertical: 10),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                ListTile(
                  leading: const Icon(Icons.picture_as_pdf, color: Colors.red),
                  title: Text(note['title']?.toString() ?? 'Chapter-wise Note'),
                  subtitle: Text(
                    '${note['subject'] ?? '-'} • ${note['chapter'] ?? '-'}',
                  ),
                ),
                const Divider(height: 4),
                ListTile(
                  enabled: hasPdf,
                  leading: const Icon(Icons.visibility_outlined),
                  title: const Text('Preview PDF'),
                  onTap: () async {
                    Navigator.pop(context);
                    await _previewPdf(note);
                  },
                ),
                ListTile(
                  enabled: hasPdf,
                  leading: const Icon(Icons.download_outlined),
                  title: const Text('Download PDF'),
                  onTap: () async {
                    Navigator.pop(context);
                    await _downloadPdf(note);
                  },
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  List<String> _subjectOptions() {
    final subjects = _notes
        .map((e) => (e['subject'] ?? '').toString().trim())
        .where((e) => e.isNotEmpty)
        .toSet()
        .toList();
    subjects.sort();
    return subjects;
  }

  List<String> _chapterOptions() {
    final chapters = _notes
        .map((e) => (e['chapter'] ?? '').toString().trim())
        .where((e) => e.isNotEmpty)
        .toSet()
        .toList();
    chapters.sort();
    return chapters;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F7FA),
      appBar: AppBar(
        title: const Text('Notes'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _loadNotes,
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
                        const Icon(Icons.lock_outline,
                            color: Colors.redAccent, size: 40),
                        const SizedBox(height: 10),
                        const Text(
                          'Unable to load notes.',
                          textAlign: TextAlign.center,
                        ),
                        const SizedBox(height: 8),
                        Text(
                          _errorMessage!,
                          textAlign: TextAlign.center,
                          style: const TextStyle(color: Colors.black54),
                        ),
                        const SizedBox(height: 16),
                        ElevatedButton(
                          onPressed: _loadNotes,
                          child: const Text('Retry'),
                        ),
                      ],
                    ),
                  ),
                )
          : _notes.isEmpty
              ? Center(
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(
                        _studentStandard == null
                            ? 'No notes available.'
                            : 'No notes available for standard $_studentStandard.',
                        textAlign: TextAlign.center,
                      ),
                      if (_selectedSubject != null ||
                          _selectedChapter != null) ...[
                        const SizedBox(height: 12),
                        OutlinedButton.icon(
                          onPressed: _clearFilters,
                          icon: const Icon(Icons.filter_alt_off),
                          label: const Text('Clear filters'),
                        ),
                      ],
                    ],
                  ),
                )
              : RefreshIndicator(
                  onRefresh: _loadNotes,
                  child: ListView(
                    padding: const EdgeInsets.all(16),
                    children: [
                      _buildFiltersCard(),
                      const SizedBox(height: 12),
                      ..._notes.map((note) => _buildNoteCard(note)).toList(),
                    ],
                  ),
                ),
    );
  }

  Widget _buildFiltersCard() {
    final subjects = _subjectOptions();
    final chapters = _chapterOptions();
    final standard = (_notes.first['standard'] ?? '-').toString();

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Standard: $standard',
                style: const TextStyle(fontWeight: FontWeight.w600)),
            const SizedBox(height: 10),
            Row(
              children: [
                Expanded(
                  child: DropdownButtonFormField<String?>(
                    initialValue: _selectedSubject,
                    decoration: const InputDecoration(
                      labelText: 'Subject',
                      border: OutlineInputBorder(),
                      isDense: true,
                    ),
                    items: [
                      const DropdownMenuItem<String?>(
                          value: null, child: Text('All Subjects')),
                      ...subjects.map((subject) => DropdownMenuItem<String?>(
                            value: subject,
                            child: Text(subject),
                          )),
                    ],
                    onChanged: (value) async {
                      _selectedSubject = value;
                      _selectedChapter = null;
                      await _loadNotes();
                    },
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: DropdownButtonFormField<String?>(
                    initialValue: _selectedChapter,
                    decoration: const InputDecoration(
                      labelText: 'Chapter',
                      border: OutlineInputBorder(),
                      isDense: true,
                    ),
                    items: [
                      const DropdownMenuItem<String?>(
                          value: null, child: Text('All Chapters')),
                      ...chapters.map((chapter) => DropdownMenuItem<String?>(
                            value: chapter,
                            child: Text(chapter),
                          )),
                    ],
                    onChanged: (value) async {
                      _selectedChapter = value;
                      await _loadNotes();
                    },
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildNoteCard(dynamic note) {
    final hasPdf = _resolvePdfUrl(Map<String, dynamic>.from(note)) != null;
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: ListTile(
        onTap: () => _showNoteActions(Map<String, dynamic>.from(note)),
        leading: Icon(
          hasPdf ? Icons.picture_as_pdf : Icons.note_alt_outlined,
          color: hasPdf ? Colors.red : const Color(0xFF1A237E),
        ),
        title: Text(note['title']?.toString() ?? ''),
        subtitle: Text(
          '${note['subject'] ?? '-'} • ${note['chapter'] ?? '-'}\n${note['content'] ?? ''}',
          maxLines: 3,
          overflow: TextOverflow.ellipsis,
        ),
        isThreeLine: true,
        trailing: note['is_important'] == true
            ? const Icon(Icons.star, color: Colors.amber)
            : const Icon(Icons.chevron_right),
      ),
    );
  }
}
