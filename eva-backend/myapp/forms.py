from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Doctor, Patient

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'name', 'password1', 'password2', 'is_doctor', 'age', 'gender', 'location']

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['specialty', 'hospital']

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [] 

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'age', 'gender', 'location']