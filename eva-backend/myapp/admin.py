from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Doctor, Patient, Appointment, Emergency

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'name', 'is_doctor', 'is_verified']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_doctor', 'name', 'age', 'gender', 'location', 'is_verified')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_doctor', 'name', 'age', 'gender', 'location', 'is_verified')}),
    )

admin.site.register(User, CustomUserAdmin)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'specialty', 'hospital', 'is_available']
    search_fields = ['user__name', 'user__email', 'specialty', 'hospital']

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_age', 'get_gender']
    search_fields = ['user__name', 'user__email']

    def get_age(self, obj):
        return obj.user.age
    get_age.short_description = 'Age'

    def get_gender(self, obj):
        return obj.user.gender
    get_gender.short_description = 'Gender'

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'date_time', 'is_canceled', 'is_rescheduled']
    list_filter = ['is_canceled', 'is_rescheduled', 'date_time']
    search_fields = ['patient__user__name', 'doctor__user__name', 'issue']

@admin.register(Emergency)
class EmergencyAdmin(admin.ModelAdmin):
    list_display = ['patient', 'created_at', 'is_resolved']
    list_filter = ['is_resolved', 'created_at']
    search_fields = ['patient__user__name', 'description']