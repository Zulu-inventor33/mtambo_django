from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import User, MaintenanceProvider, Technician


class SignupForm(forms.ModelForm):
    # Custom field for phone number validation
    phone_number = forms.CharField(max_length=15, required=True, 
                                   validators=[RegexValidator(r'^\+?1?\d{9,15}$', message="Enter a valid phone number.")])
    
    # Fields for account types
    account_type_choices = [
        ('developer', 'Developer'),
        ('maintenance', 'Maintenance Technician'),
        ('building_owner', 'Building Owner'),
    ]
    account_type = forms.ChoiceField(choices=account_type_choices, required=True)
    
    company_name = forms.CharField(max_length=100, required=False)
    company_registration_number = forms.CharField(max_length=50, required=False)
    specialization = forms.CharField(max_length=100, required=False)
    maintenance_company_id = forms.CharField(max_length=50, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password', 'account_type', 
                  'company_name', 'company_registration_number', 'specialization', 'maintenance_company_id']
    
    def clean(self):
        cleaned_data = super().clean()
        
        account_type = cleaned_data.get('account_type')
        
        # Ensure company name and registration are required for developers/building owners
        if account_type in ['developer', 'building_owner']:
            if not cleaned_data.get('company_name') or not cleaned_data.get('company_registration_number'):
                raise ValidationError("Company Name and Registration Number are required for this account type.")

        # Ensure specialization and company ID are required for maintenance technicians
        if account_type == 'maintenance':
            if not cleaned_data.get('specialization') or not cleaned_data.get('maintenance_company_id'):
                raise ValidationError("Specialization and Maintenance Company ID are required for this account type.")

        return cleaned_data