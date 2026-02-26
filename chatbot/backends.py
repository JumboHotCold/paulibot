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
        
        # 1. Try to find user by student_id
        try:
            user = CustomUser.objects.get(student_id=username)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            pass
            
        # 2. Fallback to standard username authentication (for Admins)
        return super().authenticate(request, username, password, **kwargs)
