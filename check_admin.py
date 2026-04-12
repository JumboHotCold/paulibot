import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paulibot.settings')
django.setup()

from chatbot.models import CustomUser

for u in CustomUser.objects.filter(is_superuser=True):
    print(f"Username: {u.username}, student_id: '{u.student_id}', is_superuser: {u.is_superuser}")
    print(f"  Password hash starts with: {u.password[:30]}...")
    print(f"  check_password('admin'): {u.check_password('admin')}")
    print(f"  check_password('Admin'): {u.check_password('Admin')}")
    print(f"  check_password('password'): {u.check_password('password')}")
    print(f"  check_password('123456'): {u.check_password('123456')}")
    print()
