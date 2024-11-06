# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

# User model
class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  # Email is unique and will be the USERNAME_FIELD
    contact_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    age = models.PositiveIntegerField()

    # Specify which field is used for authentication (email in this case)
    USERNAME_FIELD = 'email'  # Use email as the username for authentication
    REQUIRED_FIELDS = ['username', 'name']  # Other fields required during user creation

    # Specify related_name to avoid conflicts with auth groups and permissions
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def save(self, *args, **kwargs):
        # If no username is provided, use email as the username
        if not self.username:
            self.username = self.email
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

# Patient model
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.name

# Doctor model
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.name} - {self.specialization}"

# Appointment model
class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    time_slot = models.TimeField()
    status = models.CharField(max_length=20, choices=[('Booked', 'Booked'), ('Cancelled', 'Cancelled'), ('Rescheduled', 'Rescheduled')])

    def __str__(self):
        return f"Appointment with {self.doctor.user.name} on {self.date} at {self.time_slot}"

# Doctor Availability model
class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time_slot = models.TimeField()
    is_available = models.BooleanField(default=True)

# Admin model
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Admin {self.user.username}"
