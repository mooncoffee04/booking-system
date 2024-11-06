# Register your models here.
from django.contrib import admin
from booking.models import User, Patient, Doctor, Appointment, DoctorAvailability, Admin

admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(DoctorAvailability)
admin.site.register(Admin)
