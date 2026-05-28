import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../core/providers/auth_provider.dart';
import '../../../core/services/api_service.dart';
import '../../../main.dart';

class FeesScreen extends StatefulWidget {
  const FeesScreen({super.key});

  @override
  State<FeesScreen> createState() => _FeesScreenState();
}

class _FeesScreenState extends State<FeesScreen> {
  List<dynamic> _fees = [];
  Map<String, dynamic>? _summary;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadFees();
  }

  Future<void> _loadFees() async {
    setState(() => _isLoading = true);
    try {
      _fees = await ApiService.getFees();
      _summary = await ApiService.getFeesSummary();
    } catch (_) {
      setState(() => _fees = []);
      _summary = null;
    }
    setState(() => _isLoading = false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F7FA),
      appBar: AppBar(
        title: const Text('Fees'),
        actions: [
          IconButton(icon: const Icon(Icons.refresh), onPressed: _loadFees),
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
          : RefreshIndicator(
              onRefresh: _loadFees,
              child: ListView(
                padding: const EdgeInsets.all(16),
                children: [
                  if (_summary != null) ...[
                    Container(
                      padding: const EdgeInsets.all(18),
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.circular(18),
                        boxShadow: [BoxShadow(color: const Color.fromRGBO(0, 0, 0, 0.05), blurRadius: 10)],
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text('Fees Summary', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                          const SizedBox(height: 12),
                          Text('Total Fees Decided: ₹${_summary!['total_fee'] ?? 0}'),
                          Text('Total Paid: ₹${_summary!['total_paid'] ?? 0}'),
                          Text('Remaining Fees: ₹${_summary!['total_balance'] ?? 0}'),
                        ],
                      ),
                    ),
                    const SizedBox(height: 20),
                  ],
                  ..._fees.map((fee) => Card(
                        margin: const EdgeInsets.only(bottom: 12),
                        child: Padding(
                          padding: const EdgeInsets.all(16),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Row(
                                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                children: [
                                  Text('Fee #${fee['id']}', style: const TextStyle(fontWeight: FontWeight.bold)),
                                  Text(fee['status']?.toString().toUpperCase() ?? '', style: const TextStyle(color: Colors.blue)),
                                ],
                              ),
                              const SizedBox(height: 12),
                              Table(
                                columnWidths: const {
                                  0: FlexColumnWidth(0.6),
                                  1: FlexColumnWidth(0.4),
                                },
                                children: [
                                  TableRow(children: [
                                    const Padding(
                                      padding: EdgeInsets.symmetric(vertical: 6),
                                      child: Text('Total Fees'),
                                    ),
                                    Padding(
                                      padding: const EdgeInsets.symmetric(vertical: 6),
                                      child: Text('₹${fee['total_fee']}'),
                                    ),
                                  ]),
                                  TableRow(children: [
                                    const Padding(
                                      padding: EdgeInsets.symmetric(vertical: 6),
                                      child: Text('Amount Paid'),
                                    ),
                                    Padding(
                                      padding: const EdgeInsets.symmetric(vertical: 6),
                                      child: Text('₹${fee['amount_paid']}'),
                                    ),
                                  ]),
                                  TableRow(children: [
                                    const Padding(
                                      padding: EdgeInsets.symmetric(vertical: 6),
                                      child: Text('Remaining Fees'),
                                    ),
                                    Padding(
                                      padding: const EdgeInsets.symmetric(vertical: 6),
                                      child: Text('₹${fee['remaining_fee']}'),
                                    ),
                                  ]),
                                  TableRow(children: [
                                    const Padding(
                                      padding: EdgeInsets.symmetric(vertical: 6),
                                      child: Text('Installments'),
                                    ),
                                    Padding(
                                      padding: const EdgeInsets.symmetric(vertical: 6),
                                      child: Text('${fee['number_of_installments'] ?? '-'}'),
                                    ),
                                  ]),
                                  TableRow(children: [
                                    const Padding(
                                      padding: EdgeInsets.symmetric(vertical: 6),
                                      child: Text('Next Installment'),
                                    ),
                                    Padding(
                                      padding: const EdgeInsets.symmetric(vertical: 6),
                                      child: Text('${fee['next_installment_date'] ?? '-'}'),
                                    ),
                                  ]),
                                ],
                              ),
                              if (fee['remarks'] != null && fee['remarks'].toString().isNotEmpty) ...[
                                const SizedBox(height: 12),
                                Text('Remarks: ${fee['remarks']}', style: const TextStyle(color: Colors.grey)),
                              ],
                            ],
                          ),
                        ),
                      )),
                ],
              ),
            ),
    );
  }
}