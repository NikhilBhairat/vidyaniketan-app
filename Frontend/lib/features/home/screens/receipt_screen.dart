import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:url_launcher/url_launcher_string.dart';

import '../../../core/providers/auth_provider.dart';
import '../../../core/services/api_service.dart';
import '../../../main.dart';

class ReceiptScreen extends StatefulWidget {
  const ReceiptScreen({super.key});

  @override
  State<ReceiptScreen> createState() => _ReceiptScreenState();
}

class _ReceiptScreenState extends State<ReceiptScreen> {
  List<dynamic> _receipts = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadReceipts();
  }

  Future<void> _loadReceipts() async {
    setState(() => _isLoading = true);
    try {
      _receipts = await ApiService.getReceipts();
    } catch (_) {
      setState(() => _receipts = []);
    }
    setState(() => _isLoading = false);
  }

  Widget _receiptRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: const TextStyle(color: Colors.grey, fontSize: 14)),
          Expanded(
            child: Text(
              value,
              textAlign: TextAlign.end,
              style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600),
            ),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F7FA),
      appBar: AppBar(
        title: const Text('Receipts'),
        actions: [
          IconButton(icon: const Icon(Icons.refresh), onPressed: _loadReceipts),
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
          : _receipts.isEmpty
              ? const Center(child: Text('No receipts available.'))
              : RefreshIndicator(
                  onRefresh: _loadReceipts,
                  child: ListView.builder(
                    padding: const EdgeInsets.all(16),
                    itemCount: _receipts.length,
                    itemBuilder: (context, index) {
                      final receipt = _receipts[index];
                      return Card(
                        margin: const EdgeInsets.only(bottom: 12),
                        child: Padding(
                          padding: const EdgeInsets.all(16),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Row(
                                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                children: [
                                  Text('Receipt #${receipt['receipt_number']}', style: const TextStyle(fontWeight: FontWeight.bold)),
                                  if (receipt['receipt_pdf'] != null && (receipt['receipt_pdf'] as String).isNotEmpty)
                                    ElevatedButton.icon(
                                      onPressed: () async {
                                        final url = receipt['receipt_pdf'] as String;
                                        if (await canLaunchUrlString(url)) {
                                          await launchUrlString(url);
                                        } else if (mounted) {
                                          ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Unable to open receipt.')));
                                        }
                                      },
                                      icon: const Icon(Icons.download_rounded, size: 18),
                                      label: const Text('Download'),
                                    ),
                                ],
                              ),
                              const SizedBox(height: 12),
                              _receiptRow('Paid Amount', '₹${receipt['amount']}'),
                              _receiptRow('Payment Date', receipt['payment_date'] ?? '-'),
                              _receiptRow('Payment Mode', receipt['payment_mode'] ?? '-'),
                              _receiptRow('Student', receipt['student_name'] ?? '-'),
                              _receiptRow('School', receipt['school_name'] ?? '-'),
                              const Divider(height: 24),
                              const Text('Fee Details', style: TextStyle(fontWeight: FontWeight.bold)),
                              const SizedBox(height: 8),
                              _receiptRow('Total Fees', '₹${receipt['total_fee']}'),
                              _receiptRow('Amount Paid', '₹${receipt['amount_paid']}'),
                              _receiptRow('Remaining', '₹${receipt['remaining_fee']}'),
                              _receiptRow('Status', receipt['fee_status'] ?? '-'),
                            ],
                          ),
                        ),
                      );
                    },
                  ),
                ),
    );
  }
}