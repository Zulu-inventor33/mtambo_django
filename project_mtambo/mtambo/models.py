from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum


# Enum for account types
class AccountType(Enum):
    DEVELOPER = "developer"
    MAINTENANCE = "maintenance"
    TECHNICIAN = "technician"


# Custom user model extending AbstractUser
class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    account_type = models.CharField(
        max_length=50, choices=[(tag.name, tag.value) for tag in AccountType], default=AccountType.DEVELOPER
    )
    created_at = models.DateTimeField(auto_now_add=True)
    verification_code = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


# Developer Model (for developer account type)
class Developer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    developer_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"Developer: {self.developer_name}"


# Maintenance Provider Model (for maintenance account type)
class MaintenanceProvider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=50)
    company_name = models.CharField(max_length=255)
    company_address = models.CharField(max_length=255)
    company_registration_number = models.CharField(max_length=50)

    def __str__(self):
        return f"Maintenance Provider: {self.company_name}"


# Technician Model (for technician account type)
class Technician(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    equip_specialization = models.CharField(max_length=50)
    maintenance_company = models.ForeignKey(
        MaintenanceProvider, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"Technician: {self.user.username}"

class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_verification_code(self):
        self.verification_code = str(random.randint(100000, 999999))  # Generate 6-digit code
        self.save()

    def __str__(self):
        return f"Verification for {self.user.email}"