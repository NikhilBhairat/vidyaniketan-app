import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from apps.api.serializers import MobileTokenObtainPairSerializer
from apps.accounts.models import User
from django.contrib.auth import authenticate

# Get the student user
user = User.objects.get(mobile_number='9876543210')
print(f"User found: {user.mobile_number}, is_active={user.is_active}, has_usable_password={user.has_usable_password()}")

# Test authenticate directly
auth_user = authenticate(username='9876543210', password='password123')
print(f"Direct authenticate result: {auth_user}")

# Test with serializer
print("\n--- Testing serializer ---")
data = {
    'mobile_number': '9876543210',
    'password': 'password123'
}

serializer = MobileTokenObtainPairSerializer(data=data)
print(f"Is valid: {serializer.is_valid()}")
print(f"Errors: {serializer.errors}")

if serializer.is_valid():
    print(f"Data: {serializer.validated_data}")
