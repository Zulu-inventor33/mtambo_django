from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from enum import Enum as PyEnum


# Account type enum with default set to NONE
class AccountType(PyEnum):
    DEVELOPER = "developer"
    MAINTENANCE = "maintenance"
    TECHNICIAN = "technician"

# We will a afunction in the user class to generate a username based on first name and last name
class User(AbstractUser):
    phone_number = models.CharField(max_length=15)
    account_type = models.CharField(
        max_length=50,
        choices=[(tag, tag.value) for tag in AccountType],
        default=AccountType.MAINTENANCE
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"User: {self.username} ({self.account_type})"
    


# Developer model
class Developer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    developer_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.developer_name


# Specialization Enum
class Specialization(PyEnum):
    HVAC = "hvac"
    LIFTS = "lifts"
    GENERATORS = "generators"


# Maintenance Company model
class MaintenanceCompany(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(
        max_length=50,
        choices=[(tag, tag.value) for tag in Specialization],
        default=Specialization.LIFTS
    )
    company_name = models.CharField(max_length=255)
    company_address = models.CharField(max_length=255)
    company_registration_number = models.CharField(max_length=50)

    def __str__(self):
        return self.company_name


# Technician model (formerly MaintenanceCompany)
class Technician(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    equip_specialization = models.CharField(
        max_length=50,
        choices=[(tag, tag.value) for tag in Specialization],
        default=Specialization.LIFTS
    )
    maintenance_company = models.ForeignKey(
        MaintenanceCompany,
        null=False,
        blank=False,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.user.username


# Building model
class Building(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=20)
    num_floors = models.IntegerField()
    additional_details = models.TextField(blank=True, null=True)
    maintenance_company = models.ForeignKey(MaintenanceCompany, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Lift model
class Lift(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name="lifts")
    lift_id = models.CharField(max_length=50, unique=True)
    lift_serial_number = models.CharField(max_length=100, unique=True)
    next_maintenance_date = models.DateField()
    maintenance_frequency = models.CharField(
        max_length=20,
        choices=[
            ('monthly', 'Monthly'),
            ('60_days', 'Every 60 Days'),
            ('90_days', 'Every 90 Days'),
            ('6_months', 'Every 6 Months')
        ]
    )
    assigned_technician = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'account_type': 'technician'}
    )

    #Incase of a vacancy of the technician and he is fired. Create a function that creates 
    # An Alert to the maintenance company when the maintain date is due so that he can assign the job to another technician

    def __str__(self):
        return f"{self.lift_id} - {self.building.name}"


# Job Status Enum
class JobStatus(PyEnum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    OVERDUE = "Overdue"
    CANCELED = "Canceled"


# Job model
class Job(models.Model):
    description = models.CharField(max_length=255)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE)
    assigned_date = models.DateField(null=True, blank=True)
    scheduled_date = models.DateField()
    completion_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=[(tag, tag.value) for tag in JobStatus],
        default=JobStatus.PENDING
    )

    def is_overdue(self):
        return self.scheduled_date < timezone.now().date() and self.status != JobStatus.COMPLETED

    def __str__(self):
        return f"Job {self.id}: {self.description}"


# Claim model
class Claim(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="claims")
    developer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'account_type': 'developer'})
    description = models.TextField()
    claim_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Claim for Job ID {self.job.id} by Developer {self.developer.username}"


# Logged Issue model
class LoggedIssue(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    lift = models.ForeignKey(Lift, on_delete=models.CASCADE)
    developer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'account_type': 'developer'})
    description = models.TextField()
    logged_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Issue for Lift {self.lift.lift_id} at Building {self.building.name}"


# Alert model
class Alert(models.Model):
    ALERT_TYPE_CHOICES = [
        ('technician_signup', 'Technician Signup'),
        ('logged_issue', 'Logged Issue'),
        ('job_completed', 'Job Completed'),
        ('claim_filed', 'Claim Filed'),
        ('assign_technician', 'Assign Technician')
    ]
    
    alert_type = models.CharField(max_length=50, choices=ALERT_TYPE_CHOICES)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert: {self.alert_type}"

#Below are the Maintenance Log classes. They will be reviewed at a latter date Since they to complex for simple minds
# Maintenance Log Model to track logs of each maintenance task performed
class MaintenanceLog(models.Model):
    # Relations
    lift = models.ForeignKey(Lift, on_delete=models.CASCADE, related_name="maintenance_logs")
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE)
    
    # Maintenance task details
    task_type = models.CharField(max_length=50, choices=TaskType.choices)
    maintenance_date = models.DateTimeField(default=timezone.now)
    
    # Task-specific details (fields will vary depending on the task performed)
    task_description = models.TextField()  # A field to store custom task description if needed
    
    # Checkboxes for specific tasks, using Boolean for simplicity
    is_machine_check_done = models.BooleanField(default=False)
    is_brake_check_done = models.BooleanField(default=False)
    is_controller_check_done = models.BooleanField(default=False)
    is_dust_removed = models.BooleanField(default=False)
    is_cleaning_done = models.BooleanField(default=False)
    is_observation_done = models.BooleanField(default=False)  # e.g., 50 mins operation observation
    
    # Comments section
    additional_comments = models.TextField(blank=True, null=True)
    
    # Client's signature (this could be stored as a URL to a digital signature or just text)
    client_signature = models.CharField(max_length=255, blank=True, null=True)
    
    # Approval details
    caretaker_signature = models.CharField(max_length=255, blank=True, null=True)
    approved_by = models.CharField(max_length=255, blank=True, null=True)
    
    # Task status
    is_completed = models.BooleanField(default=False)  # Whether maintenance is completed or not
    
    # Store the date when the maintenance log was created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Maintenance Log for {self.lift.lift_id} - {self.maintenance_date}"

    def mark_completed(self):
        self.is_completed = True
        self.save()
    
    def get_task_summary(self):
        tasks_completed = []
        if self.is_machine_check_done:
            tasks_completed.append("Machine Check")
        if self.is_brake_check_done:
            tasks_completed.append("Brake Check")
        if self.is_controller_check_done:
            tasks_completed.append("Controller Check")
        if self.is_dust_removed:
            tasks_completed.append("Dust Removal")
        if self.is_cleaning_done:
            tasks_completed.append("Cleaning")
        if self.is_observation_done:
            tasks_completed.append("Observation Done")
        return ", ".join(tasks_completed)


# Maintenance Check Sheet Model for Quality Checks (This could be used for logging quality check sheets)
class QualityCheckSheet(models.Model):
    # Relations
    maintenance_log = models.ForeignKey(MaintenanceLog, on_delete=models.CASCADE, related_name="quality_checks")
    
    # Machine and Lift Details
    building = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    machine_number = models.CharField(max_length=50)
    machine_type = models.CharField(max_length=50)
    controller_type = models.CharField(max_length=50)
    
    # Assignment & Comments for quality checks
    assignments = models.TextField()
    comments = models.TextField()
    
    # Technician and Signature
    technician_name = models.CharField(max_length=255)
    technician_signature = models.CharField(max_length=255, blank=True, null=True)
    
    # Approval details
    approved_by = models.CharField(max_length=255, blank=True, null=True)
    
    # Timestamp for when the quality check was performed
    quality_check_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Quality Check Sheet for {self.machine_number} ({self.quality_check_date})"
