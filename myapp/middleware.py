from django.utils import timezone
from django.shortcuts import redirect
from django.conf import settings
import time

class AdminSessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user is accessing admin pages
        admin_paths = ['/admin/', 'custom_admin_panel', 'admin_add_edit', 'give_points', 'confirm_delete']
        is_admin_path = any(path in request.path for path in admin_paths)
        
        if is_admin_path and request.user.is_authenticated and request.user.is_staff:
            # Get last activity time from session
            last_activity = request.session.get('admin_last_activity')
            current_time = time.time()
            
            # If no activity recorded, set it now
            if not last_activity:
                request.session['admin_last_activity'] = current_time
            else:
                # Check if 5 minutes (300 seconds) have passed
                if current_time - last_activity > 300:
                    # Clear the session and redirect to login
                    request.session.flush()
                    return redirect('myapp:admin_login')
                else:
                    # Update last activity time
                    request.session['admin_last_activity'] = current_time
        
        response = self.get_response(request)
        return response
