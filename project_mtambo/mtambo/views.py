from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import SignUpForm, LoginForm
from .models import Developer, MaintenanceProvider, Technician, User
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, 'index.html')

# Signup View
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            account_type = form.cleaned_data.get('account_type')

            # Create account type-specific models
            if account_type == AccountType.DEVELOPER.value:
                Developer.objects.create(user=user, developer_name=request.POST['developer_name'], address=request.POST['address'])
            elif account_type == AccountType.MAINTENANCE.value:
                MaintenanceProvider.objects.create(
                    user=user,
                    specialization=request.POST['specialization'],
                    company_name=request.POST['company_name'],
                    company_address=request.POST['company_address'],
                    company_registration_number=request.POST['company_registration_number']
                )
            elif account_type == AccountType.TECHNICIAN.value:
                technician = Technician.objects.create(user=user, equip_specialization=request.POST['equip_specialization'])
                maintenance_company_id = request.POST.get('maintenance_company_id')
                technician.maintenance_company = MaintenanceProvider.objects.get(id=maintenance_company_id)
                technician.save()

            messages.success(request, 'Signup successful! Please log in.')
            return redirect('login')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

# Login View
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                # Redirect to user-specific dashboard
                if user.account_type == AccountType.DEVELOPER.value:
                    return redirect('developer_dashboard')
                elif user.account_type == AccountType.MAINTENANCE.value:
                    return redirect('maintenance_dashboard')
                elif user.account_type == AccountType.TECHNICIAN.value:
                    return redirect('technician_dashboard')
                else:
                    messages.warning(request, 'Unknown account type. Please contact support.')
                    return redirect('login')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

#Testing views
def developer_dashboard(request):
    return HttpResponse("This is the Developer Dashboard.")

def maintenance_dashboard(request):
    return HttpResponse("This is the Maintenance Dashboard.")

def technician_dashboard(request):
    return HttpResponse("This is the Technician Dashboard.")

def about(request):
    return HttpResponse("This is the About Us Page.")

def elevators(request):
    return HttpResponse("Elevator services page content goes here.")

def generators(request):
    return HttpResponse("Power backup generators service content goes here.")

def hvac(request):
    return HttpResponse("HVAC system services page content goes here.")

def contact(request):
    return HttpResponse("Contact us for more information.")

def logout(request):
    return HttpResponse("You have logged out successfully!")  # Dummy logout message

def dashboard(request):
    return HttpResponse("Welcome to your Dashboard!")

def forgot_password(request):
    return HttpResponse("Don't worry we will help you retrive you password")