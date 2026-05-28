import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../core/providers/auth_provider.dart';
import '../../../core/services/api_service.dart';
import '../../../main.dart';

class GalleryScreen extends StatefulWidget {
  const GalleryScreen({super.key});

  @override
  State<GalleryScreen> createState() => _GalleryScreenState();
}

class _GalleryScreenState extends State<GalleryScreen> {
  List<dynamic> _categories = [];
  List<dynamic> _galleryItems = [];
  bool _isLoading = true;
  String? _selectedCategoryId;
  String? _selectedCategoryName;

  @override
  void initState() {
    super.initState();
    _loadCategories();
  }

  Future<void> _loadCategories() async {
    setState(() => _isLoading = true);
    try {
      print('Loading categories...');
      final categories = await ApiService.getGalleryCategories();
      print('Categories loaded: $categories');
      setState(() {
        _categories = categories;
        _isLoading = false;
      });
    } catch (e) {
      print('Error loading categories: $e');
      setState(() => _isLoading = false);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to load categories: $e')),
        );
      }
    }
  }

  Future<void> _loadGalleryItems(String categoryId, String categoryName) async {
    setState(() {
      _isLoading = true;
      _selectedCategoryId = categoryId;
      _selectedCategoryName = categoryName;
    });
    try {
      print('Loading gallery items for category: $categoryName');
      final items = await ApiService.getGallery();
      print('Gallery items loaded: $items');
      // Filter items by selected category
      final filteredItems = items.where((item) => item['category'] == categoryName).toList();
      print('Filtered items: $filteredItems');
      setState(() {
        _galleryItems = filteredItems;
        _isLoading = false;
      });
    } catch (e) {
      print('Error loading gallery items: $e');
      setState(() => _isLoading = false);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to load gallery items: $e')),
        );
      }
    }
  }

  void _goBackToCategories() {
    setState(() {
      _selectedCategoryId = null;
      _selectedCategoryName = null;
      _galleryItems = [];
    });
  }

  @override
  Widget build(BuildContext context) {
    print('GalleryScreen build called - isLoading: $_isLoading, categories: ${_categories.length}, selectedCategory: $_selectedCategoryName');
    return Scaffold(
      backgroundColor: const Color(0xFFF5F7FA),
      appBar: AppBar(
        title: Text(_selectedCategoryName ?? 'Gallery'),
        leading: _selectedCategoryId != null
            ? IconButton(
                icon: const Icon(Icons.arrow_back),
                onPressed: _goBackToCategories,
              )
            : null,
        actions: [
          IconButton(
            icon: const Icon(Icons.bug_report),
            onPressed: () async {
              try {
                print('Testing API call...');
                final categories = await ApiService.getGalleryCategories();
                print('API call successful: $categories');
                if (mounted) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text('API Success: ${categories.length} categories')),
                  );
                }
              } catch (e) {
                print('API call failed: $e');
                if (mounted) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text('API Failed: $e')),
                  );
                }
              }
            },
          ),
          IconButton(icon: const Icon(Icons.refresh), onPressed: _selectedCategoryId != null ? () => _loadGalleryItems(_selectedCategoryId!, _selectedCategoryName!) : _loadCategories),
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
          ? const Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  CircularProgressIndicator(),
                  SizedBox(height: 16),
                  Text('Loading gallery...'),
                ],
              ),
            )
          : _selectedCategoryId != null
              ? _buildGalleryItemsView()
              : _buildCategoriesView(),
    );
  }

  Widget _buildCategoriesView() {
    if (_categories.isEmpty && !_isLoading) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.photo_library, size: 64, color: Colors.grey),
            const SizedBox(height: 16),
            const Text(
              'No gallery categories available.',
              style: TextStyle(fontSize: 16, color: Colors.grey),
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: _loadCategories,
              child: const Text('Retry'),
            ),
          ],
        ),
      );
    }
    return GridView.builder(
      padding: const EdgeInsets.all(16),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        crossAxisSpacing: 16,
        mainAxisSpacing: 16,
        childAspectRatio: 1.2,
      ),
      itemCount: _categories.length,
      itemBuilder: (context, index) {
        final category = _categories[index];
        return Card(
          elevation: 4,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          child: InkWell(
            onTap: () => _loadGalleryItems(category['id'].toString(), category['name']),
            borderRadius: BorderRadius.circular(12),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.folder, size: 48, color: Theme.of(context).primaryColor),
                  const SizedBox(height: 12),
                  Text(
                    category['name'],
                    style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                    textAlign: TextAlign.center,
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                  const SizedBox(height: 4),
                  Text(
                    category['description'] ?? '',
                    style: const TextStyle(color: Colors.grey, fontSize: 12),
                    textAlign: TextAlign.center,
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                ],
              ),
            ),
          ),
        );
      },
    );
  }

  Widget _buildGalleryItemsView() {
    if (_galleryItems.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.photo_library, size: 64, color: Colors.grey),
            const SizedBox(height: 16),
            Text('No items in $_selectedCategoryName'),
          ],
        ),
      );
    }
    return GridView.builder(
      padding: const EdgeInsets.all(8),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        crossAxisSpacing: 8,
        mainAxisSpacing: 8,
        childAspectRatio: 1,
      ),
      itemCount: _galleryItems.length,
      itemBuilder: (context, index) {
        final item = _galleryItems[index];
        final hasFile = item['file'] != null && item['file'].toString().isNotEmpty;
        final hasVideoUrl = item['video_url'] != null && item['video_url'].toString().isNotEmpty;

        return Card(
          clipBehavior: Clip.antiAlias,
          child: InkWell(
            onTap: hasFile ? () => _showFullScreenImage(item['file']) : null,
            child: Stack(
              fit: StackFit.expand,
              children: [
                if (hasFile)
                  Image.network(
                    item['file'],
                    fit: BoxFit.cover,
                    errorBuilder: (context, error, stackTrace) => Container(
                      color: Colors.grey[200],
                      child: const Icon(Icons.image_not_supported, size: 48, color: Colors.grey),
                    ),
                  )
                else if (hasVideoUrl)
                  Container(
                    color: Colors.grey[200],
                    child: const Icon(Icons.video_library, size: 48, color: Colors.grey),
                  )
                else
                  Container(
                    color: Colors.grey[200],
                    child: const Icon(Icons.image_not_supported, size: 48, color: Colors.grey),
                  ),
                if (hasVideoUrl)
                  Positioned(
                    top: 8,
                    right: 8,
                    child: Container(
                      padding: const EdgeInsets.all(4),
                      decoration: const BoxDecoration(
                        color: Colors.red,
                        shape: BoxShape.circle,
                      ),
                      child: const Icon(Icons.play_arrow, color: Colors.white, size: 16),
                    ),
                  ),
              ],
            ),
          ),
        );
      },
    );
  }

  void _showFullScreenImage(String imageUrl) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => Scaffold(
          backgroundColor: Colors.black,
          appBar: AppBar(
            backgroundColor: Colors.black,
            iconTheme: const IconThemeData(color: Colors.white),
          ),
          body: Center(
            child: InteractiveViewer(
              child: Image.network(
                imageUrl,
                fit: BoxFit.contain,
                errorBuilder: (context, error, stackTrace) => const Center(
                  child: Text('Failed to load image', style: TextStyle(color: Colors.white)),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}