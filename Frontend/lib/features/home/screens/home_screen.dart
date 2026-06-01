import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:provider/provider.dart';
import 'package:url_launcher/url_launcher_string.dart';

import '../../../core/providers/auth_provider.dart';
import '../../../core/providers/notification_provider.dart';
import '../../../core/services/api_service.dart';
import '../../../main.dart';

const List<String> _monthNames = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December',
];

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final GlobalKey<_DashboardPageState> _dashboardKey = GlobalKey<_DashboardPageState>();
  final GlobalKey<_AttendanceScreenState> _attendanceKey = GlobalKey<_AttendanceScreenState>();

  int _currentIndex = 0;
  late final List<Widget> _pages = [
    DashboardPage(key: _dashboardKey),
    AttendanceScreen(key: _attendanceKey),
    const NotificationsScreen(),
    const ProfileScreen(),
  ];

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<NotificationProvider>().fetchNotifications();
      context.read<NotificationProvider>().startPolling();
      context.read<AuthProvider>().loadUserData();
    });
  }

  @override
  void dispose() {
    context.read<NotificationProvider>().stopPolling();
    super.dispose();
  }

  Future<void> _refreshAllData() async {
    await context.read<AuthProvider>().refreshUserProfile();
    await context.read<NotificationProvider>().fetchNotifications();
    await _dashboardKey.currentState?._loadDashboard();
    await _attendanceKey.currentState?._loadAttendance();
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('All data refreshed successfully')),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(index: _currentIndex, children: _pages),
      bottomNavigationBar: _buildBottomNav(),
      drawer: _buildDrawer(),
    );
  }

  NavigationBar _buildBottomNav() {
    final unreadCount = context.watch<NotificationProvider>().unreadCount;
    return NavigationBar(
      selectedIndex: _currentIndex,
      onDestinationSelected: (index) => setState(() => _currentIndex = index),
      destinations: [
        const NavigationDestination(icon: Icon(Icons.dashboard_outlined), selectedIcon: Icon(Icons.dashboard), label: 'Dashboard'),
        const NavigationDestination(icon: Icon(Icons.calendar_today_outlined), selectedIcon: Icon(Icons.calendar_today), label: 'Attendance'),
        NavigationDestination(
          icon: Stack(
            children: [
              const Icon(Icons.notifications_outlined),
              if (unreadCount > 0)
                Positioned(
                  right: 0,
                  top: 0,
                  child: Container(
                    padding: const EdgeInsets.all(4),
                    decoration: const BoxDecoration(color: Colors.red, shape: BoxShape.circle),
                    child: Text('$unreadCount', style: const TextStyle(color: Colors.white, fontSize: 10)),
                  ),
                ),
            ],
          ),
          selectedIcon: const Icon(Icons.notifications),
          label: 'Alerts',
        ),
        const NavigationDestination(icon: Icon(Icons.person_outline), selectedIcon: Icon(Icons.person), label: 'Profile'),
      ],
    );
  }

  Drawer _buildDrawer() {
    return Drawer(
      child: ListView(
        padding: EdgeInsets.zero,
        children: [
          DrawerHeader(
            decoration: const BoxDecoration(color: Color(0xFF1A237E)),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisAlignment: MainAxisAlignment.end,
              children: const [
                CircleAvatar(radius: 28, backgroundColor: Colors.white24, child: Icon(Icons.person, size: 36, color: Colors.white)),
                SizedBox(height: 12),
                Text('Vidyaniketan Classes & Academy', style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                SizedBox(height: 4),
                Text('Student Portal', style: TextStyle(color: Colors.white70, fontSize: 12)),
              ],
            ),
          ),
          _drawerItem(Icons.calendar_today, 'Attendance', AppRouter.attendance),
          _drawerItem(Icons.account_balance_wallet, 'Fees', AppRouter.fees),
          _drawerItem(Icons.bar_chart, 'Progress Report', AppRouter.marks),
          _drawerItem(Icons.menu_book, 'Study Material', AppRouter.notes),
          _drawerItem(Icons.schedule, 'Timetable', AppRouter.timetable),
          _drawerItem(Icons.play_circle_outline, 'Lectures', AppRouter.lectures),
          _drawerItem(Icons.photo_library, 'Gallery', AppRouter.gallery),
          _drawerItem(Icons.receipt_long, 'Receipts', AppRouter.receipts),
          _drawerItem(Icons.assignment, 'Question Papers', AppRouter.questionPapers),
          _drawerItem(Icons.people, 'Teachers', AppRouter.teachers),
          ListTile(
            leading: const Icon(Icons.refresh, color: Color(0xFF1A237E)),
            title: const Text('Refresh Data', style: TextStyle(color: Colors.black87)),
            onTap: () async {
              Navigator.pop(context);
              await _refreshAllData();
            },
          ),
          const Divider(),
          _drawerItem(Icons.logout, 'Logout', AppRouter.login, color: Colors.red),
        ],
      ),
    );
  }

  ListTile _drawerItem(IconData icon, String title, String route, {Color? color}) {
    return ListTile(
      leading: Icon(icon, color: color ?? const Color(0xFF1A237E)),
      title: Text(title, style: TextStyle(color: color ?? Colors.black87)),
      onTap: () {
        Navigator.pop(context);
        if (route == AppRouter.login) {
          context.read<AuthProvider>().logout();
          Navigator.pushReplacementNamed(context, route);
        } else {
          Navigator.pushNamed(context, route);
        }
      },
    );
  }
}

class DashboardPage extends StatefulWidget {
  const DashboardPage({super.key});

  @override
  State<DashboardPage> createState() => _DashboardPageState();
}

class _DashboardPageState extends State<DashboardPage> {
  Map<String, dynamic>? _dashboardData;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadDashboard();
  }

  Future<void> _loadDashboard({bool showSnackBar = false}) async {
    setState(() => _isLoading = true);
    try {
      final response = await ApiService.getDashboard();
      _dashboardData = response;
      if (showSnackBar && mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Dashboard refreshed successfully')),
        );
      }
    } catch (e) {
      _dashboardData = null;
      print('Dashboard load error: $e');
      if (showSnackBar && mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Unable to load dashboard: $e')),
        );
      }
    }
    setState(() => _isLoading = false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F7FA),
      appBar: AppBar(
        title: const Text('Dashboard'),
        actions: [
          IconButton(icon: const Icon(Icons.refresh), onPressed: () => _loadDashboard(showSnackBar: true)),
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
          : _dashboardData == null
              ? Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Text('No data available'),
                      const SizedBox(height: 20),
                      ElevatedButton(
                        onPressed: () => _loadDashboard(showSnackBar: true),
                        child: const Text('Retry'),
                      ),
                    ],
                  ),
                )
              : RefreshIndicator(
                  onRefresh: () => _loadDashboard(showSnackBar: true),
                  child: DefaultTabController(
                    length: 5,
                    child: SingleChildScrollView(
                      physics: const AlwaysScrollableScrollPhysics(),
                      padding: const EdgeInsets.all(16),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          _buildProfileCard(),
                          const SizedBox(height: 20),
                          _buildStats(),
                          const SizedBox(height: 20),
                          _buildDashboardTabs(),
                        ],
                      ),
                    ),
                  ),
                ),
    );
  }

  String? _cacheBustedUrl(String? url) {
    if (url == null || url.isEmpty) return null;
    final separator = url.contains('?') ? '&' : '?';
    return '$url${separator}ts=${DateTime.now().millisecondsSinceEpoch}';
  }

  Widget _buildProfileCard() {
    final data = _dashboardData ?? {};
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: const LinearGradient(colors: [Color(0xFF1A237E), Color(0xFF3949AB)]),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Row(
        children: [
          CircleAvatar(
            radius: 32,
            backgroundColor: Colors.white24,
            backgroundImage: data['profile_photo_url'] != null ? NetworkImage(_cacheBustedUrl(data['profile_photo_url'])!) : null,
            child: data['profile_photo_url'] == null ? const Icon(Icons.person, size: 36, color: Colors.white) : null,
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(data['full_name'] ?? 'Student', style: const TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold)),
                const SizedBox(height: 6),
                Text(data['standard_display'] ?? '', style: const TextStyle(color: Colors.white70, fontSize: 14)),
                const SizedBox(height: 4),
                Text('School: ${data['school_name'] ?? '-'}', style: const TextStyle(color: Colors.white70, fontSize: 12)),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildStats() {
    final stats = _dashboardData?['quick_stats'] ?? {};
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Quick Stats', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
        const SizedBox(height: 12),
        Row(
          children: [
            _statCard('Attendance', '${stats['attendance_percentage'] ?? 0}%'),
            const SizedBox(width: 12),
            _statCard('Fees due', '₹${stats['fees_due_amount'] ?? 0}'),
            const SizedBox(width: 12),
            _statCard('Unread', '${stats['unread_notifications'] ?? 0}'),
          ],
        ),
      ],
    );
  }

  Widget _buildQuickFeesTab() {
    final fees = List<dynamic>.from(_dashboardData?['recent_fees'] ?? []);
    if (fees.isEmpty) {
      return const Center(child: Text('No fee records found.'));
    }
    return SingleChildScrollView(
      child: Column(
        children: fees.map((fee) {
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
                      Text('Fee #${fee['id']}', style: const TextStyle(fontWeight: FontWeight.bold)),
                      Text(fee['status']?.toString().toUpperCase() ?? '', style: const TextStyle(color: Colors.blue)),
                    ],
                  ),
                  const SizedBox(height: 12),
                  Table(
                    columnWidths: const {0: FlexColumnWidth(0.6), 1: FlexColumnWidth(0.4)},
                    children: [
                      _buildTableRow('Total Fees', '₹${fee['total_fee']}'),
                      _buildTableRow('Amount Paid', '₹${fee['amount_paid']}'),
                      _buildTableRow('Remaining', '₹${fee['remaining_fee']}'),
                      _buildTableRow('Installments', '${fee['number_of_installments'] ?? '-'}'),
                      _buildTableRow('Next Installment', fee['next_installment_date'] ?? '-'),
                      _buildTableRow('Remarks', fee['remarks'] ?? '-'),
                    ],
                  ),
                ],
              ),
            ),
          );
        }).toList(),
      ),
    );
  }

  TableRow _buildTableRow(String label, String value) {
    return TableRow(
      children: [
        Padding(padding: const EdgeInsets.symmetric(vertical: 6), child: Text(label, style: const TextStyle(color: Colors.grey))),
        Padding(padding: const EdgeInsets.symmetric(vertical: 6), child: Text(value, textAlign: TextAlign.right)),
      ],
    );
  }

  Widget _buildQuickReceiptsTab() {
    final receipts = List<dynamic>.from(_dashboardData?['recent_receipts'] ?? []);
    if (receipts.isEmpty) {
      return const Center(child: Text('No receipts found.'));
    }
    return SingleChildScrollView(
      child: Column(
        children: receipts.map((receipt) {
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
                      if ((receipt['receipt_pdf'] as String?)?.isNotEmpty ?? false)
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
                          style: ElevatedButton.styleFrom(padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10)),
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
        }).toList(),
      ),
    );
  }

  Widget _buildQuickGalleryTab() {
    // For now, show a simple navigation to gallery screen
    // TODO: In future, could show recent categories or featured items
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.photo_library, size: 48, color: Colors.grey),
          const SizedBox(height: 16),
          const Text(
            'Browse Gallery',
            style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 8),
          const Text(
            'View photos and videos by category',
            style: TextStyle(color: Colors.grey, fontSize: 14),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 16),
          ElevatedButton(
            onPressed: () => Navigator.pushNamed(context, AppRouter.gallery),
            child: const Text('Open Gallery'),
          ),
        ],
      ),
    );
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

  Widget _statCard(String title, String value) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(16), boxShadow: [BoxShadow(color: const Color.fromRGBO(0, 0, 0, 0.05), blurRadius: 10)]),
        child: Column(
          children: [
            Text(value, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Text(title, style: const TextStyle(color: Colors.grey, fontSize: 12), textAlign: TextAlign.center),
          ],
        ),
      ),
    );
  }

  Widget _buildDashboardTabs() {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(18),
        boxShadow: [BoxShadow(color: const Color.fromRGBO(0, 0, 0, 0.05), blurRadius: 10)],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Quick Access', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          const TabBar(
            isScrollable: true,
            labelColor: Color(0xFF1A237E),
            unselectedLabelColor: Colors.grey,
            indicatorColor: Color(0xFF1A237E),
            tabs: [
              Tab(text: 'Notes'),
              Tab(text: 'Results'),
              Tab(text: 'Fees'),
              Tab(text: 'Gallery'),
              Tab(text: 'Receipts'),
            ],
          ),
          SizedBox(
            height: 260,
            child: TabBarView(
              children: [
                _buildDashboardTab('Notes', 'Read recent notes and updates', Icons.note, AppRouter.notes),
                _buildDashboardTab('Results', 'See exam results and grades', Icons.bar_chart, AppRouter.marks),
                _buildQuickFeesTab(),
                _buildQuickGalleryTab(),
                _buildQuickReceiptsTab(),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildDashboardTab(String title, String subtitle, IconData icon, String route) {
    return Padding(
      padding: const EdgeInsets.only(top: 12),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              CircleAvatar(
                radius: 24,
                backgroundColor: const Color(0xFF1A237E),
                child: Icon(icon, color: Colors.white),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(title, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 6),
                    Text(subtitle, style: const TextStyle(color: Colors.grey, fontSize: 13)),
                  ],
                ),
              ),
            ],
          ),
          const Spacer(),
          Align(
            alignment: Alignment.bottomRight,
            child: TextButton(
              onPressed: () => Navigator.pushNamed(context, route),
              child: const Text('View All'),
            ),
          ),
        ],
      ),
    );
  }
}

class AttendanceScreen extends StatefulWidget {
  const AttendanceScreen({super.key});

  @override
  State<AttendanceScreen> createState() => _AttendanceScreenState();
}

class _AttendanceScreenState extends State<AttendanceScreen> {
  Map<String, dynamic>? _summary;
  List<dynamic> _monthlyAttendance = [];
  DateTime _selectedMonth = DateTime.now();
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadAttendance();
  }

  Future<void> _loadAttendance({bool showSnackBar = false}) async {
    setState(() => _isLoading = true);
    try {
      _summary = await ApiService.getAttendanceSummary(year: _selectedMonth.year);
      _monthlyAttendance = await ApiService.getMonthlyAttendance(_selectedMonth.month, _selectedMonth.year);
      if (showSnackBar && mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Attendance refreshed successfully')),
        );
      }
    } catch (_) {
      _summary = null;
      if (showSnackBar && mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Unable to refresh attendance')),
        );
      }
    }
    setState(() => _isLoading = false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F7FA),
      appBar: AppBar(
        title: const Text('Attendance'),
        actions: [
          IconButton(icon: const Icon(Icons.refresh), onPressed: () => _loadAttendance(showSnackBar: true)),
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
              onRefresh: () => _loadAttendance(showSnackBar: true),
              child: _summary == null
                  ? const Center(child: Text('No attendance data available.'))
                  : ListView(
                      padding: const EdgeInsets.all(16),
                      children: [
                        Container(
                          padding: const EdgeInsets.all(18),
                          decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(18), boxShadow: [BoxShadow(color: const Color.fromRGBO(0, 0, 0, 0.05), blurRadius: 10)]),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const Text('Attendance Summary', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                              const SizedBox(height: 12),
                              Text('Present: ${_summary!['present_days'] ?? '-'}'),
                              Text('Absent: ${_summary!['absent_days'] ?? '-'}'),
                              Text('Attendance : ${(_summary!['attendance_percentage'] ?? 0).round()}%'),
                            ],
                          ),
                        ),
                        const SizedBox(height: 20),
                        _buildMonthlyProjection(),
                      ],
                    ),
            ),
    );
  }

  void _changeMonth(int offset) {
    setState(() {
      _selectedMonth = DateTime(_selectedMonth.year, _selectedMonth.month + offset);
    });
    _loadAttendance();
  }

  Widget _buildMonthlyProjection() {
    final presentCount = _monthlyAttendance.where((item) => item['status'] == 'P').length;
    final absentCount = _monthlyAttendance.where((item) => item['status'] == 'A').length;
    final totalDays = _monthlyAttendance.length;

    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(18), boxShadow: [BoxShadow(color: const Color.fromRGBO(0, 0, 0, 0.05), blurRadius: 10)]),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Monthly Attendance Projection', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          _buildMonthSelector(),
          const SizedBox(height: 16),
          if (totalDays == 0)
            const Padding(
              padding: EdgeInsets.symmetric(vertical: 12),
              child: Text('No attendance records available for this month.'),
            )
          else ...[
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                _buildMiniStat('Present', presentCount, Colors.green),
                _buildMiniStat('Absent', absentCount, Colors.red),
                _buildMiniStat('Total', totalDays, Colors.blueGrey),
              ],
            ),
            const SizedBox(height: 20),
            SizedBox(
              height: 200,
              child: BarChart(
                BarChartData(
                  alignment: BarChartAlignment.spaceAround,
                  maxY: 1.2,
                  barTouchData: BarTouchData(enabled: false),
                  titlesData: FlTitlesData(
                    bottomTitles: AxisTitles(
                      sideTitles: SideTitles(
                        showTitles: true,
                        reservedSize: 30,
                        getTitlesWidget: (value, meta) {
                          return Text(value.toInt().toString(), style: const TextStyle(fontSize: 10));
                        },
                      ),
                    ),
                    leftTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
                    topTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
                    rightTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
                  ),
                  gridData: FlGridData(show: false),
                  borderData: FlBorderData(show: false),
                  barGroups: () {
                    final sortedAttendance = _monthlyAttendance
                        .where((record) => record['date'] != null)
                        .toList()
                        ..sort((a, b) => DateTime.parse(a['date']).compareTo(DateTime.parse(b['date'])));
                    return sortedAttendance.map((record) {
                      DateTime date = DateTime.parse(record['date']);
                      int day = date.day;
                      Color color = record['status'] == 'P' ? Colors.green : Colors.red;
                      return BarChartGroupData(
                        x: day,
                        barRods: [
                          BarChartRodData(
                            toY: 1,
                            color: color,
                            width: 16,
                            borderRadius: BorderRadius.circular(4),
                          ),
                        ],
                      );
                    }).toList();
                  }(),
                ),
              ),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildMonthSelector() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        IconButton(
          icon: const Icon(Icons.chevron_left),
          onPressed: () => _changeMonth(-1),
        ),
        Text(
          '${_monthNames[_selectedMonth.month - 1]} ${_selectedMonth.year}',
          style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600),
        ),
        IconButton(
          icon: const Icon(Icons.chevron_right),
          onPressed: () => _changeMonth(1),
        ),
      ],
    );
  }

  Widget _buildMiniStat(String label, int value, Color color) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(color: color.withAlpha((0.1 * 255).round()), borderRadius: BorderRadius.circular(14)),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(label, style: TextStyle(color: color, fontSize: 12, fontWeight: FontWeight.w600)),
            const SizedBox(height: 8),
            Text(value.toString(), style: TextStyle(color: color, fontSize: 18, fontWeight: FontWeight.bold)),
          ],
        ),
      ),
    );
  }
}

class NotificationsScreen extends StatefulWidget {
  const NotificationsScreen({super.key});

  @override
  State<NotificationsScreen> createState() => _NotificationsScreenState();
}

class _NotificationsScreenState extends State<NotificationsScreen> {
  @override
  Widget build(BuildContext context) {
    final provider = context.watch<NotificationProvider>();
    return Scaffold(
      backgroundColor: const Color(0xFFF5F7FA),
      appBar: AppBar(
        title: const Text('Notifications'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () async {
              await provider.fetchNotifications();
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Notifications refreshed successfully')),
              );
            },
          ),
          IconButton(
            icon: const Icon(Icons.done_all),
            onPressed: provider.unreadCount > 0
                ? () async {
                    await provider.markAllRead();
                    if (mounted) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(content: Text('All notifications marked as read')),
                      );
                    }
                  }
                : null,
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
      body: provider.isLoading
          ? const Center(child: CircularProgressIndicator())
          : provider.notifications.isEmpty
              ? const Center(child: Text('No notifications'))
              : ListView.builder(
                  itemCount: provider.notifications.length,
                  itemBuilder: (context, index) {
                    final notification = provider.notifications[index];
                    final isRead = notification['is_read'] == true;
                    return Container(
                      margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                      decoration: BoxDecoration(
                        color: isRead ? Colors.white : Colors.blue.withOpacity(0.05),
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(
                          color: isRead ? Colors.grey.withOpacity(0.3) : Colors.blue.withOpacity(0.3),
                        ),
                      ),
                      child: ListTile(
                        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                        title: Text(
                          notification['title'] ?? '',
                          style: TextStyle(
                            fontWeight: isRead ? FontWeight.normal : FontWeight.w600,
                            color: isRead ? Colors.grey : Colors.black,
                          ),
                        ),
                        subtitle: Text(
                          notification['message'] ?? '',
                          style: TextStyle(
                            color: isRead ? Colors.grey : Colors.black87,
                          ),
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                        ),
                        trailing: Icon(
                          isRead ? Icons.check_circle : Icons.circle_notifications,
                          color: isRead ? Colors.green : Colors.blue,
                        ),
                        onTap: () async {
                          if (!isRead) {
                            await provider.markRead(notification['id'] as int);
                            if (mounted) {
                              ScaffoldMessenger.of(context).showSnackBar(
                                const SnackBar(
                                  content: Text('Notification marked as read'),
                                  duration: Duration(seconds: 1),
                                ),
                              );
                            }
                          }
                        },
                      ),
                    );
                  },
                ),
    );
  }
}

class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  Map<String, dynamic>? _studentData;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadProfile();
  }

  Future<void> _loadProfile() async {
    setState(() => _isLoading = true);
    try {
      _studentData = await ApiService.getDashboard();
    } catch (_) {
      _studentData = null;
    }
    setState(() => _isLoading = false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F7FA),
      appBar: AppBar(
        title: const Text('Profile'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () async {
              await _loadProfile();
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Profile refreshed successfully')),
              );
            },
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
          : _studentData == null
              ? const Center(child: Text('No profile data available'))
              : SingleChildScrollView(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      _buildProfileHeader(),
                      const SizedBox(height: 24),
                      _buildPersonalDetails(),
                    ],
                  ),
                ),
    );
  }

  String? _cacheBustedUrl(String? url) {
    if (url == null || url.isEmpty) return null;
    final separator = url.contains('?') ? '&' : '?';
    return '$url${separator}ts=${DateTime.now().millisecondsSinceEpoch}';
  }

  Widget _buildProfileHeader() {
    final data = _studentData!;
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: const LinearGradient(colors: [Color(0xFF1A237E), Color(0xFF3949AB)]),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Row(
        children: [
          CircleAvatar(
            radius: 40,
            backgroundColor: Colors.white24,
            backgroundImage: data['profile_photo_url'] != null ? NetworkImage(_cacheBustedUrl(data['profile_photo_url'])!) : null,
            child: data['profile_photo_url'] == null ? const Icon(Icons.person, size: 40, color: Colors.white) : null,
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(data['full_name'] ?? 'Student', style: const TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold)),
                const SizedBox(height: 8),
                Text('Standard: ${data['standard_display'] ?? '-'}', style: const TextStyle(color: Colors.white70, fontSize: 14)),
                Text('Student ID: ${data['student_id'] ?? '-'}', style: const TextStyle(color: Colors.white70, fontSize: 12)),
                Text('School: ${data['school_name'] ?? '-'}', style: const TextStyle(color: Colors.white70, fontSize: 12)),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildPersonalDetails() {
    final data = _studentData!;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Personal Details', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
        const SizedBox(height: 16),
        _infoRow('Student ID', data['student_id'] ?? '-'),
        _infoRow('Standard', data['standard_display'] ?? '-'),
        _infoRow('Full Name', data['full_name'] ?? '-'),
        _infoRow('Mobile Number', data['mobile_number'] ?? '-'),
        _infoRow('Date of Birth', data['date_of_birth'] ?? '-'),
        _infoRow('Gender', data['gender'] ?? '-'),
        _infoRow('Blood Group', data['blood_group'] ?? '-'),
        _infoRow('Address', data['address'] ?? '-'),
        _infoRow('Admission Date', data['admission_date'] ?? '-'),
      ],
    );
  }

  Widget _infoRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Row(
        children: [
          Expanded(child: Text(label, style: const TextStyle(fontWeight: FontWeight.w600))),
          Expanded(child: Text(value, textAlign: TextAlign.right)),
        ],
      ),
    );
  }
}
