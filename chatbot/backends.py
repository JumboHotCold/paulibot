from django.contrib.auth.backends import ModelBackend
from .models import CustomUser

class StudentIDBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in using
    their student_id instead of username.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        # In this context, 'username' will contain whatever the user typed
        # in the 'Student ID' field on the login page.
        
        # 1. Try to find user by student_id (Case-insensitive check)
        try:
            # We use __iexact to ensure that "c-2024" and "C-2024" both work
            user = CustomUser.objects.get(student_id__iexact=username)
            if user.check_password(password):
                return user
        except (CustomUser.DoesNotExist, CustomUser.MultipleObjectsReturned):
            pass
            
        # 2. Fallback to standard username authentication (for Admins)
        return super().authenticate(request, username, password, **kwargs)
