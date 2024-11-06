from django import forms
from .models import User, Appointment, Doctor, DoctorAvailability

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['name', 'email', 'contact_number', 'gender', 'age', 'password']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time_slot']

    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), empty_label="Choose Doctor", widget=forms.Select)

    # Date and Time should be filled dynamically when doctor is selected
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time_slot = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
