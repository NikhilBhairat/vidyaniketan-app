import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

mobile = "9999999999"
password = "admin123"

if not User.objects.filter(mobile_number=mobile).exists():
    User.objects.create_superuser(
        mobile_number=mobile,
        password=password
    )
    print("Superuser created")
else:
    print("Superuser already exists")import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

mobile = "9999999999"
password = "admin123"

if not User.objects.filter(mobile_number=mobile).exists():
    User.objects.create_superuser(
        mobile_number=mobile,
        password=password
    )
    print("Superuser created")
else:
    print("Superuser already exists")
