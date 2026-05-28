#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.test import Client

print('=' * 60)
print('TESTING ALL DJANGO ADMIN TABLES')
print('=' * 60)

client = Client()

# Test login
login_success = client.login(username='9999999999', password='admin123')
print(f'\n✓ Admin Login: {login_success}')

if login_success:
    # List of all model admin URLs to test
    models_to_test = [
        ('/admin/accounts/user/', 'Users'),
        ('/admin/students/student/', 'Students'),
        ('/admin/attendance/attendance/', 'Attendance'),
        ('/admin/fees/fee/', 'Fees'),
        ('/admin/fees/feereceipt/', 'Fee Receipts'),
        ('/admin/notifications/notification/', 'Notifications'),
        ('/admin/gallery/gallerycategory/', 'Gallery Categories'),
        ('/admin/gallery/galleryitem/', 'Gallery Items'),
        ('/admin/results/exam/', 'Exams'),
        ('/admin/results/mark/', 'Marks'),
        ('/admin/study_material/note/', 'Notes'),
        ('/admin/study_material/questionpaper/', 'Question Papers'),
        ('/admin/lectures/recordedlecture/', 'Recorded Lectures'),
    ]
    
    print('\n' + '=' * 60)
    print('TESTING MODEL ACCESS:')
    print('=' * 60)
    
    accessible = 0
    errors = []
    
    for url, label in models_to_test:
        try:
            response = client.get(url)
            if response.status_code == 200:
                print(f'✓ {label:25s} - Status: 200 OK')
                accessible += 1
            elif response.status_code == 404:
                print(f'✗ {label:25s} - Status: 404 NOT FOUND')
                errors.append(f'{label}: 404')
            else:
                print(f'? {label:25s} - Status: {response.status_code}')
                errors.append(f'{label}: {response.status_code}')
        except Exception as e:
            print(f'✗ {label:25s} - Error: {str(e)[:40]}')
            errors.append(f'{label}: {str(e)[:40]}')
    
    print('\n' + '=' * 60)
    print(f'SUMMARY: {accessible}/{len(models_to_test)} models accessible')
    print('=' * 60)
    
    if errors:
        print('\nErrors found:')
        for error in errors:
            print(f'  - {error}')
    else:
        print('\n✓ ALL MODELS ACCESSIBLE!')
        print('✓ All admin tables working properly')
        print('✓ No field reference errors')
else:
    print('✗ Login failed')
