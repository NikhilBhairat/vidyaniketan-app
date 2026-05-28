import os
import django
from datetime import date, datetime, timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from apps.accounts.models import User
from apps.students.models import Student
from apps.fees.models import Fee, FeeStructure, FeeReceipt
from apps.attendance.models import Attendance
from apps.notifications.models import Notification

# Current year
CURRENT_YEAR = 2026

def create_dummy_data():
    print("Creating dummy data...")

    # Create admin user first
    print("\n=== Creating Admin User ===")
    admin_user = User.objects.filter(mobile_number='9999999999').first()
    if not admin_user:
        admin_user = User.objects.create_superuser(
            mobile_number='9999999999',
            password='admin123',
            role=User.ADMIN,
            email='admin@vidyaniketan.com'
        )
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.is_active = True
        admin_user.save()
        print("✅ Created admin user: 9999999999 / admin123")
    else:
        # Ensure existing admin has all permissions
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.is_active = True
        admin_user.save()
        print("✅ Admin user exists and permissions updated: 9999999999 / admin123")

    # Create users and students
    students_data = [
        {
            'mobile': '9876543210',
            'name': 'Rahul Sharma',
            'standard': '8',
            'roll_no': '001',
            'tuition_fee': 10000
        },
        {
            'mobile': '9876543211',
            'name': 'Priya Patel',
            'standard': '9',
            'roll_no': '002',
            'tuition_fee': 12000
        },
        {
            'mobile': '9876543212',
            'name': 'Amit Kumar',
            'standard': '10',
            'roll_no': '003',
            'tuition_fee': 15000
        }
    ]

    created_students = []

    for data in students_data:
        # Check if student user already exists
        existing_user = User.objects.filter(mobile_number=data['mobile']).first()
        if existing_user:
            print(f"⚠️  User {data['name']} ({data['mobile']}) already exists, skipping")
            # Get the student record for this user
            student = Student.objects.filter(user=existing_user).first()
            if student:
                created_students.append({
                    'student': student,
                    'tuition_fee': data['tuition_fee']
                })
            continue
        
        # Create user
        user = User.objects.create_user(
            mobile_number=data['mobile'],
            password='password123',
            role=User.STUDENT,
            email=f"{data['name'].lower().replace(' ', '.')}@example.com"
        )

        # Create student
        student = Student.objects.create(
            user=user,
            student_id=f"STD{data['standard']}{data['roll_no']}",
            full_name=data['name'],
            standard=data['standard'],
            roll_number=data['roll_no'],
            date_of_birth=date(CURRENT_YEAR-15, random.randint(1, 12), random.randint(1, 28)),
            gender='Male' if data['name'].split()[0] in ['Rahul', 'Amit'] else 'Female',
            mobile_number=data['mobile'],
            address=f"{random.randint(100, 999)} {random.choice(['Main Street', 'Park Avenue', 'Garden Road', 'Church Street'])}, City, State - {random.randint(100000, 999999)}",
            admission_date=date(CURRENT_YEAR-1, 6, 1),
            blood_group=random.choice(['O+', 'A+', 'B+', 'AB+', 'O-', 'A-', 'B-', 'AB-']),
            school_name='Vidyaniketan Public School'
        )

        created_students.append({
            'student': student,
            'tuition_fee': data['tuition_fee']
        })

        print(f"Created student: {student.full_name} ({student.standard}th Standard)")

    # Create fee structures (only tuition fees)
    for std in ['8', '9', '10']:
        fee_amounts = {'8': 10000, '9': 12000, '10': 15000}
        FeeStructure.objects.create(
            standard=std,
            academic_year=f"{CURRENT_YEAR-1}-{CURRENT_YEAR}",
            term='Annual',
            tuition_fee=fee_amounts[std],
            exam_fee=0,
            library_fee=0,
            sports_fee=0,
            other_fee=0,
            due_date=date(CURRENT_YEAR, 3, 31)
        )
        print(f"Created fee structure for {std}th standard: ₹{fee_amounts[std]}")

    # Create fees and receipts (3 installments each)
    for student_data in created_students:
        student = student_data['student']
        total_fee = student_data['tuition_fee']

        # Check if fee already exists for this student
        existing_fee = Fee.objects.filter(student=student).first()
        if existing_fee:
            print(f"⚠️  Fees for {student.full_name} already exist, skipping")
            continue

        # Calculate installments (divide by 3)
        installment_amount = total_fee // 3
        remaining = total_fee % 3

        # Create fee record with partial payment (2 installments paid, 1 remaining)
        amount_paid = installment_amount * 2
        fee = Fee.objects.create(
            student=student,
            total_fee=total_fee,
            amount_paid=amount_paid,
            number_of_installments=3,
            status='partial'
        )

        # Create 2 paid installments
        for i in range(2):
            payment_date = date(CURRENT_YEAR, random.randint(1, 3), random.randint(1, 28))
            FeeReceipt.objects.create(
                receipt_number=f"REC{student.student_id}{i+1}",
                fee=fee,
                amount=installment_amount,
                payment_date=payment_date,
                payment_mode=random.choice(['Cash', 'Online', 'UPI']),
                transaction_id=f"TXN{random.randint(100000, 999999)}",
                issued_by="Admin"
            )

        print(f"Created fees for {student.full_name}: Total ₹{total_fee}, Paid ₹{amount_paid}, Remaining ₹{total_fee - amount_paid}")

    # Create attendance for April 2026
    april_2026 = date(CURRENT_YEAR, 4, 1)
    working_days = []

    # Get all weekdays in April (excluding Saturdays)
    for day in range(1, 31):
        current_date = date(CURRENT_YEAR, 4, day)
        if current_date.weekday() < 5:  # Monday to Friday
            working_days.append(current_date)

    print(f"Working days in April {CURRENT_YEAR}: {len(working_days)}")

    # Attendance percentages: 76%, 87%, 92%
    attendance_data = [
        {'student': created_students[0]['student'], 'percentage': 76},
        {'student': created_students[1]['student'], 'percentage': 87},
        {'student': created_students[2]['student'], 'percentage': 92}
    ]

    for data in attendance_data:
        student = data['student']
        attendance_percent = data['percentage']

        # Check if attendance already exists for this month
        existing_attendance = Attendance.objects.filter(student=student, date__month=4).first()
        if existing_attendance:
            print(f"⚠️  Attendance for {student.full_name} (April) already exists, skipping")
            continue

        # Calculate number of present days
        present_days = int((attendance_percent / 100) * len(working_days))

        # Randomly select present days
        present_dates = random.sample(working_days, present_days)

        for work_date in working_days:
            status = 'P' if work_date in present_dates else 'A'
            Attendance.objects.create(
                student=student,
                date=work_date,
                status=status
            )

        actual_percent = (len(present_dates) / len(working_days)) * 100
        print(f"Created attendance for {student.full_name}: {len(present_dates)}/{len(working_days)} days ({actual_percent:.1f}%)")

    # Create notifications for testing
    # Common notification (holiday)
    holiday_notif = Notification.objects.filter(title="Diwali Holiday Notice").first()
    if not holiday_notif:
        Notification.objects.create(
            title="Diwali Holiday Notice",
            message="School will remain closed from 25th October to 5th November for Diwali celebrations.",
            notification_type="holiday",
            audience="all",
            is_sent=True,
            sent_at=datetime.now()
        )
        print("Created Diwali Holiday Notice")

    # Standard-specific notifications
    for std in ['8', '9', '10']:
        exam_notif = Notification.objects.filter(title=f"Class {std} - Mid-term Exam Schedule").first()
        if not exam_notif:
            Notification.objects.create(
                title=f"Class {std} - Mid-term Exam Schedule",
                message=f"Mid-term examinations for class {std} will start from 15th March {CURRENT_YEAR}.",
                notification_type="event",
                audience="standard",
                target_standard=std,
                is_sent=True,
                sent_at=datetime.now()
            )

        fee_notif = Notification.objects.filter(title=f"Class {std} - Fee Payment Reminder").first()
        if not fee_notif:
            Notification.objects.create(
                title=f"Class {std} - Fee Payment Reminder",
                message=f"Last date for fee payment for class {std} is 31st March {CURRENT_YEAR}.",
                notification_type="fees",
                audience="standard",
                target_standard=std,
                is_sent=True,
                sent_at=datetime.now()
            )

    print("Created notifications for testing")

    print("Dummy data creation completed!")
    print("\nLogin credentials:")
    print("Admin: 9999999999 / admin123")
    for data in students_data:
        print(f"{data['name']} ({data['standard']}th): {data['mobile']} / password123")

if __name__ == "__main__":
    create_dummy_data()