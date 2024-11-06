# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegistrationForm, AppointmentForm
from .models import Patient, User, Doctor, Appointment, DoctorAvailability

def home(request):
    return render(request, 'booking/home.html')

# booking/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import User

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Check if a user with this email already exists
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                messages.info(request, "This email is already registered. Please log in.")
                return redirect('login')

            # Create new user
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Registration failed. Please check the information provided.")
    else:
        form = UserRegistrationForm()
    
    return render(request, 'booking/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Attempt to authenticate user by email
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid credentials.")
        except User.DoesNotExist:
            messages.error(request, "No account found with this email. Please register.")

    return render(request, 'booking/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')

def dashboard(request):
    return render(request, 'booking/dashboard.html')

from .models import Doctor, DoctorAvailability, Patient
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AppointmentForm

def book_appointment(request):
    # Get all doctors
    doctors = Doctor.objects.all()

    # Fetch the available slots for each doctor
    doctors_with_available_slots = []
    for doctor in doctors:
        # Filter available slots where 'is_available' is True
        available_slots = doctor.doctoravailability_set.filter(is_available=True)
        doctors_with_available_slots.append({
            'doctor': doctor,
            'available_slots': available_slots
        })

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            doctor_id = form.cleaned_data['doctor']
            date = form.cleaned_data['date']
            time_slot = form.cleaned_data['time_slot']

            # Check if the patient exists for the logged-in user
            try:
                patient = Patient.objects.get(user=request.user)
            except Patient.DoesNotExist:
                # If the patient doesn't exist, create a new Patient instance for the logged-in user
                patient = Patient.objects.create(user=request.user)

            # Check if the doctor is available at the selected time
            doctor_availability = DoctorAvailability.objects.filter(
                doctor_id=doctor_id,
                date=date,
                time_slot=time_slot,
                is_available=True
            ).first()

            if doctor_availability:
                # Create the appointment
                appointment = form.save(commit=False)
                appointment.patient = patient  # Associate the logged-in user as the patient
                appointment.save()

                # Optionally, mark the availability as taken (you can update the availability as needed)
                doctor_availability.is_available = False
                doctor_availability.save()

                messages.success(request, "Your appointment has been booked successfully!")
                return redirect('dashboard')
            else:
                messages.error(request, "Selected doctor is not available at this time.")
    else:
        form = AppointmentForm()

    return render(request, 'booking/book_appointment.html', {
        'form': form,
        'doctors_with_available_slots': doctors_with_available_slots  # Pass the available slots to the template
    })



from django.http import JsonResponse
from .models import DoctorAvailability
from datetime import datetime

from django.http import JsonResponse
from booking.models import DoctorAvailability
from django.shortcuts import render

from django.http import JsonResponse
from booking.models import DoctorAvailability

def check_availability(request):
    doctor_id = request.GET.get('doctor_id')
    date = request.GET.get('date')

    if doctor_id and date:
        # Get the available time slots for the selected doctor and date
        available_slots = DoctorAvailability.objects.filter(
            doctor_id=doctor_id,
            date=date,
            is_available=True
        ).values_list('time_slot', flat=True)

        # Return the available slots as a JSON response
        return JsonResponse({'available_slots': list(available_slots)})
    return JsonResponse({'available_slots': []})

# Ensure this view is linked to a URL in your urls.py


