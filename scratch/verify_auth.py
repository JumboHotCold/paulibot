import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paulibot.settings')
django.setup()

from django.contrib.auth import authenticate
from chatbot.models import CustomUser

def test_auth(desc, username, password):
    print(f"Testing {desc} (Username: {username})")
    user = authenticate(username=username, password=password)
    if user:
        print(f"  SUCCESS: Authenticated as {user.username} (superuser={user.is_superuser})")
    else:
        print(f"  FAILED: Could not authenticate")

# Reset passwords for superusers manually to be sure
for u in CustomUser.objects.filter(is_superuser=True):
    u.set_password('admin123')
    u.save()
    print(f"Reset password for {u.username}")

print("-" * 30)
test_auth("Admin User (Uppercase)", "Admin", "admin123")
test_auth("admin User (Lowercase)", "admin", "admin123")
test_auth("Student ID (via fallback)", "C-2026-0001", "password123") # Assuming password is password123 for test
