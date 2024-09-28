from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from .models import User, Doctor, Patient, Appointment, Emergency
from .forms import UserRegisterForm, DoctorProfileForm, PatientProfileForm, UserProfileForm, AppointmentForm

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if user.is_doctor:
                return redirect('doctor_dashboard')
            else:
                return redirect('patient_dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_verified = False 
            if user.is_doctor:
                Doctor.objects.create(user=user)
            else:
                Patient.objects.create(user=user)
            login(request, user)
            return redirect('doctor_dashboard' if user.is_doctor else 'patient_dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def doctor_dashboard(request):
    doctor = request.user.doctor
    today = timezone.now().date()
    today_appointments = Appointment.objects.filter(doctor=doctor, date_time__date=today, is_canceled=False)
    return render(request, 'doctor_dashboard.html', {'appointments': today_appointments})

@login_required
def doctor_change_availability(request):
    doctor = request.user.doctor
    if request.method == 'POST':
        doctor.is_available = not doctor.is_available
        doctor.save()
    return redirect('doctor_dashboard')

@login_required
def doctor_view_patient_profile(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    return render(request, 'patient_profile.html', {'patient': patient})

@login_required
def doctor_reschedule_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.is_rescheduled = True
            appointment.save()
            return redirect('doctor_dashboard')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'reschedule_appointment.html', {'form': form, 'appointment': appointment})

@login_required
def doctor_cancel_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.is_canceled = True
    appointment.save()
    return redirect('doctor_dashboard')

@login_required
def doctor_appointment_history(request):
    doctor = request.user.doctor
    appointments = Appointment.objects.filter(doctor=doctor).order_by('-date_time')
    return render(request, 'doctor_appointment_history.html', {'appointments': appointments})

@login_required
def doctor_edit_profile(request):
    doctor = request.user.doctor
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)
        doctor_form = DoctorProfileForm(request.POST, instance=doctor)
        if user_form.is_valid() and doctor_form.is_valid():
            user_form.save()
            doctor_form.save()
            return redirect('doctor_dashboard')
    else:
        user_form = UserProfileForm(instance=request.user)
        doctor_form = DoctorProfileForm(instance=doctor)
    return render(request, 'doctor_edit_profile.html', {'user_form': user_form, 'doctor_form': doctor_form})

@login_required
def patient_dashboard(request):
    patient = request.user.patient
    upcoming_appointments = Appointment.objects.filter(patient=patient, date_time__gte=timezone.now(), is_canceled=False)
    return render(request, 'patient_dashboard.html', {'appointments': upcoming_appointments})

@login_required
def patient_book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient
            appointment.save()
            return redirect('patient_dashboard')
    else:
        form = AppointmentForm()
    available_doctors = Doctor.objects.filter(is_available=True)
    return render(request, 'book_appointment.html', {'form': form, 'doctors': available_doctors})

@login_required
def patient_reschedule_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.is_rescheduled = True
            appointment.save()
            return redirect('patient_dashboard')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'reschedule_appointment.html', {'form': form, 'appointment': appointment})

@login_required
def patient_cancel_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.is_canceled = True
    appointment.save()
    return redirect('patient_dashboard')

@login_required
def patient_appointment_history(request):
    patient = request.user.patient
    appointments = Appointment.objects.filter(patient=patient).order_by('-date_time')
    return render(request, 'patient_appointment_history.html', {'appointments': appointments})

@login_required
def patient_emergency(request):
    if request.method == 'POST':
        description = request.POST['description']
        Emergency.objects.create(patient=request.user.patient, description=description)
        return redirect('patient_dashboard')
    return render(request, 'emergency.html')

@login_required
def patient_first_aid(request):
	# pending.
    return render(request, 'first_aid.html')

@login_required
def patient_edit_profile(request):
    patient = request.user.patient
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)
        patient_form = PatientProfileForm(request.POST, instance=patient)
        if user_form.is_valid() and patient_form.is_valid():
            user_form.save()
            patient_form.save()
            return redirect('patient_dashboard')
    else:
        user_form = UserProfileForm(instance=request.user)
        patient_form = PatientProfileForm(instance=patient)
    return render(request, 'patient_edit_profile.html', {'user_form': user_form, 'patient_form': patient_form})

def verify_email(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_verified = True
        user.save()
        login(request, user)
        return redirect('patient_dashboard' if user.is_patient else 'doctor_dashboard')
    else:
        return render(request, 'invalid_verification.html')