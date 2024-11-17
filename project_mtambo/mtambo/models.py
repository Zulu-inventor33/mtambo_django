from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum
# Create your models here.


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
        max_length=50, choices=[(tag, tag.value) for tag in AccountType], default=AccountType.DEVELOPER
    )
    created_at = models.DateTimeField(auto_now_add=True)

class Developer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    developer_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

class MaintenanceProvider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=50)
    company_name = models.CharField(max_length=255)
    company_address = models.CharField(max_length=255)
    company_registration_number = models.CharField(max_length=50)

class Technician(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    equip_specialization = models.CharField(max_length=50)
    maintenance_company = models.ForeignKey(MaintenanceProvider, on_delete=models.SET_NULL, null=True, blank=True)

