from django.shortcuts import redirect
from django.urls import reverse

class UserTypeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.user.is_doctor:
                if request.path.startswith('/patient/'):
                    return redirect(reverse('doctor_dashboard'))
            else:
                if request.path.startswith('/doctor/'):
                    return redirect(reverse('patient_dashboard'))
        
        response = self.get_response(request)
        return response