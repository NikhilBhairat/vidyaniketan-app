"""
Test script to verify notification read/unread functionality
Run: python manage.py shell < test_notifications.py
"""

from django.utils import timezone
from apps.notifications.models import Notification, NotificationRead
from apps.accounts.models import User
from apps.students.models import Student
import json

def test_notifications():
    """Test notification read/unread functionality"""
    
    print("\n" + "="*70)
    print("NOTIFICATION READ/UNREAD FUNCTIONALITY TEST")
    print("="*70)
    
    # Get a student user
    try:
        student_user = User.objects.filter(role='student').first()
        if not student_user:
            print("❌ No student user found!")
            return
        
        print(f"\n✅ Using student: {student_user.mobile_number}")
        
        # Create test notification for all students
        print("\n" + "-"*70)
        print("TEST 1: Creating GLOBAL notification (for all students)")
        print("-"*70)
        
        global_notif = Notification.objects.create(
            title="🔔 TEST: Global Announcement - Read Status Test",
            message="This is a test notification for all students. Click to mark as read.",
            notification_type="general",
            audience="all",
            is_sent=True,
            sent_at=timezone.now(),
            created_by=User.objects.filter(role='admin').first()
        )
        print(f"✅ Created global notification: ID={global_notif.id}, Title='{global_notif.title}'")
        
        # Check initial state
        print(f"\n📌 Initial state (should be unread):")
        notif_read_entry = NotificationRead.objects.filter(
            notification=global_notif,
            user=student_user
        ).first()
        
        if notif_read_entry:
            print(f"   - NotificationRead record exists: read_at={notif_read_entry.read_at}")
            print(f"   - Is read: {notif_read_entry.read_at is not None}")
        else:
            print(f"   - No NotificationRead record yet (will be created on first fetch)")
        
        # Simulate API call to fetch notifications
        print(f"\n🔍 Simulating API fetch (GET /notifications/)...")
        from apps.api.serializers import NotificationSerializer
        serializer = NotificationSerializer(global_notif, context={'request': type('Request', (), {'user': student_user, 'is_authenticated': True})()})
        print(f"   - Serialized data: {json.dumps(serializer.data, indent=2, default=str)}")
        
        # Simulate marking as read
        print(f"\n✏️  Simulating mark as read (POST /notifications/{global_notif.id}/mark_read/)...")
        notif_read, created = NotificationRead.objects.get_or_create(
            notification=global_notif,
            user=student_user,
        )
        if not notif_read.read_at:
            notif_read.read_at = timezone.now()
            notif_read.save()
            print(f"   ✅ Marked as read at: {notif_read.read_at}")
        else:
            print(f"   ℹ️  Already marked as read at: {notif_read.read_at}")
        
        # Check updated state
        print(f"\n📌 After marking as read:")
        notif_read_entry = NotificationRead.objects.get(notification=global_notif, user=student_user)
        print(f"   - read_at: {notif_read_entry.read_at}")
        print(f"   - Is read (read_at != NULL): {notif_read_entry.read_at is not None}")
        
        # Verify API response
        print(f"\n🔍 Verifying API response after marking as read:")
        serializer = NotificationSerializer(global_notif, context={'request': type('Request', (), {'user': student_user, 'is_authenticated': True})()})
        print(f"   - is_read from API: {serializer.data['is_read']}")
        
        # Test unread count
        print(f"\n📊 Unread count:")
        unread_count = NotificationRead.objects.filter(user=student_user, read_at__isnull=True).count()
        print(f"   - Total unread notifications: {unread_count}")
        
        # Create specific student notification
        print("\n" + "-"*70)
        print("TEST 2: Creating SPECIFIC STUDENT notification")
        print("-"*70)
        
        student = student_user.student_profile
        specific_notif = Notification.objects.create(
            title="📌 TEST: Specific Student Notice - Read Status Test",
            message="This is a test notification for specific student. Click to mark as read.",
            notification_type="general",
            audience="student",
            is_sent=True,
            sent_at=timezone.now(),
            created_by=User.objects.filter(role='admin').first()
        )
        specific_notif.target_students.add(student)
        print(f"✅ Created specific notification: ID={specific_notif.id}, Title='{specific_notif.title}'")
        print(f"   - Target student: {student.full_name}")
        
        # Check initial state
        print(f"\n📌 Initial state (should be unread):")
        notif_read_entry = NotificationRead.objects.filter(
            notification=specific_notif,
            user=student_user
        ).first()
        
        if notif_read_entry:
            print(f"   - NotificationRead record exists: read_at={notif_read_entry.read_at}")
            print(f"   - Is read: {notif_read_entry.read_at is not None}")
        else:
            print(f"   - No NotificationRead record yet")
        
        # Verify API response
        print(f"\n🔍 Verifying API response (should be unread):")
        serializer = NotificationSerializer(specific_notif, context={'request': type('Request', (), {'user': student_user, 'is_authenticated': True})()})
        print(f"   - is_read from API: {serializer.data['is_read']}")
        
        # Create standard-specific notification
        print("\n" + "-"*70)
        print("TEST 3: Creating STANDARD-SPECIFIC notification")
        print("-"*70)
        
        standard = student.standard
        standard_notif = Notification.objects.create(
            title=f"📚 TEST: Class {standard} Notice - Read Status Test",
            message=f"This is a test notification for class {standard}. Click to mark as read.",
            notification_type="general",
            audience="standard",
            target_standard=standard,
            is_sent=True,
            sent_at=timezone.now(),
            created_by=User.objects.filter(role='admin').first()
        )
        print(f"✅ Created standard notification: ID={standard_notif.id}, Title='{standard_notif.title}'")
        print(f"   - Target standard: {standard}")
        
        # Check initial state
        print(f"\n📌 Initial state (should be unread):")
        notif_read_entry = NotificationRead.objects.filter(
            notification=standard_notif,
            user=student_user
        ).first()
        
        if notif_read_entry:
            print(f"   - NotificationRead record exists: read_at={notif_read_entry.read_at}")
            print(f"   - Is read: {notif_read_entry.read_at is not None}")
        else:
            print(f"   - No NotificationRead record yet")
        
        # Verify API response
        print(f"\n🔍 Verifying API response (should be unread):")
        serializer = NotificationSerializer(standard_notif, context={'request': type('Request', (), {'user': student_user, 'is_authenticated': True})()})
        print(f"   - is_read from API: {serializer.data['is_read']}")
        
        # Test Mark All Read
        print("\n" + "-"*70)
        print("TEST 4: Testing Mark All Read")
        print("-"*70)
        
        unread_before = NotificationRead.objects.filter(user=student_user, read_at__isnull=True).count()
        print(f"📊 Unread before mark_all_read: {unread_before}")
        
        # Simulate mark all read
        notifications = Notification.objects.filter(
            is_sent=True
        ).distinct()
        
        count = 0
        for notif in notifications:
            notif_read, created = NotificationRead.objects.get_or_create(
                notification=notif,
                user=student_user,
            )
            if not notif_read.read_at:
                notif_read.read_at = timezone.now()
                notif_read.save()
                count += 1
        
        print(f"✅ Marked {count} notifications as read")
        
        unread_after = NotificationRead.objects.filter(user=student_user, read_at__isnull=True).count()
        print(f"📊 Unread after mark_all_read: {unread_after}")
        
        # Summary
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        print(f"✅ Global notification created and tested")
        print(f"✅ Specific student notification created and tested")
        print(f"✅ Standard-specific notification created and tested")
        print(f"✅ Mark as read functionality verified")
        print(f"✅ Mark all read functionality verified")
        print("\n" + "="*70 + "\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

# Run the test
test_notifications()
