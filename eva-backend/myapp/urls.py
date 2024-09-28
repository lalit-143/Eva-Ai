# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/availability/', views.doctor_change_availability, name='doctor_change_availability'),
    path('doctor/patient/<int:patient_id>/', views.doctor_view_patient_profile, name='doctor_view_patient_profile'),
    path('doctor/reschedule/<int:appointment_id>/', views.doctor_reschedule_appointment, name='doctor_reschedule_appointment'),
    path('doctor/cancel/<int:appointment_id>/', views.doctor_cancel_appointment, name='doctor_cancel_appointment'),
    path('doctor/history/', views.doctor_appointment_history, name='doctor_appointment_history'),
    path('doctor/profile/', views.doctor_edit_profile, name='doctor_edit_profile'),
    path('patient/', views.patient_dashboard, name='patient_dashboard'),
    path('patient/book/', views.patient_book_appointment, name='patient_book_appointment'),
    path('patient/reschedule/<int:appointment_id>/', views.patient_reschedule_appointment, name='patient_reschedule_appointment'),
    path('patient/cancel/<int:appointment_id>/', views.patient_cancel_appointment, name='patient_cancel_appointment'),
    path('patient/history/', views.patient_appointment_history, name='patient_appointment_history'),
    path('patient/emergency/', views.patient_emergency, name='patient_emergency'),
    path('patient/firstaid/', views.patient_first_aid, name='patient_first_aid'),
    path('patient/profile/', views.patient_edit_profile, name='patient_edit_profile'),
]