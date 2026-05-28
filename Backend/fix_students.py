import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from apps.accounts.models import User
from apps.students.models import Student

students_data = [
    {'mobile': '9876543210', 'name': 'Rahul Sharma', 'standard': '8', 'roll_no': '001'},
    {'mobile': '9876543211', 'name': 'Priya Patel', 'standard': '9', 'roll_no': '002'},
    {'mobile': '9876543212', 'name': 'Amit Kumar', 'standard': '10', 'roll_no': '003'},
]

print("Recreating student users with correct passwords...\n")

for data in students_data:
    # Delete old user and student
    User.objects.filter(mobile_number=data['mobile']).delete()
    
    # Create new user with correct password
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
        date_of_birth=date(2010, 6, 15),
        gender='Male' if data['name'].split()[0] in ['Rahul', 'Amit'] else 'Female',
        mobile_number=data['mobile'],
        address='School Address',
        admission_date=date(2025, 6, 1),
        blood_group='O+',
        school_name='Vidyaniketan Public School'
    )
    
    # Test authentication
    from django.contrib.auth import authenticate
    auth_user = authenticate(username=data['mobile'], password='password123')
    status = "✅" if auth_user else "❌"
    
    print(f"{status} Created student: {data['name']} ({data['mobile']})")
    print(f"   Password authentication: {'PASS' if auth_user else 'FAIL'}")
    print()

print("Student user setup complete!")
print("\nLogin credentials:")
for data in students_data:
    print(f"  {data['name']} ({data['standard']}th): {data['mobile']} / password123")
