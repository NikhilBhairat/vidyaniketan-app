import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.accounts.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers

class DebugMobileTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.USERNAME_FIELD  # 'mobile_number'

    def validate(self, attrs):
        print(f"\n=== Serializer.validate() called ===")
        print(f"Initial attrs: {attrs}")
        print(f"self.username_field: {self.username_field}")
        
        # Check what the parent class expects
        print(f"\nAttempting super().validate()...")
        
        try:
            # The parent class expects self.username_field in attrs
            # But if we don't have it, it might fail
            username = attrs.get(self.username_field)
            password = attrs.get('password')
            print(f"Username from attrs['{self.username_field}']: {username}")
            print(f"Password: {password}")
            
            # Try direct authenticate
            auth_result = authenticate(username=username, password=password)
            print(f"Direct authenticate result: {auth_result}")
            
            # Now call parent
            data = super().validate(attrs)
            print(f"Parent validate succeeded: {data.keys()}")
            
        except Exception as e:
            print(f"Parent validate failed with: {type(e).__name__}: {e}")
            raise serializers.ValidationError({
                'non_field_errors': [
                    'Invalid mobile number or password. Please check your credentials.'
                ]
            })
        
        data['user'] = {
            'id': self.user.id,
            'mobile_number': self.user.mobile_number,
            'email': self.user.email,
            'role': self.user.role,
        }
        return data


# Test
data = {
    'mobile_number': '9876543210',
    'password': 'password123'
}

serializer = DebugMobileTokenObtainPairSerializer(data=data)
print(f"\nSerializer.is_valid(): {serializer.is_valid()}")
print(f"Errors: {serializer.errors}")
if serializer.is_valid():
    print(f"Token data keys: {serializer.validated_data.keys()}")
