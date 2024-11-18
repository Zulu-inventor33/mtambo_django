from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm  # Import the AuthenticationForm
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.contrib.sessions.models import Session
from .forms import SignupForm
from .models import User
from .models import EmailVerification
from django.http import HttpResponse
from django.contrib import messages

# Define the index view
def index(request):
    return render(request, 'index.html')

def signup(request):
    """Handle user signup and send email verification code"""
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            # Save the user without committing to the database yet
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Create email verification record
            verification = EmailVerification.objects.create(user=user)
            verification.generate_verification_code()

            # Send the verification code via email
            send_verification_email(user.email, verification.verification_code)

            # Inform the user
            messages.success(request, 'Signup successful! Please verify your email by entering the code sent to your inbox.')

            # Redirect to the email verification page
            return redirect('verify_email')  # Redirect to the page where the user enters the code.
        
        else:
            # Handle form validation errors
            messages.error(request, 'There was an error with your submission. Please try again.')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})

# Send verification email function
def send_verification_email(email, verification_code):
    subject = "Verify your email address"
    message = f"Your verification code is: {verification_code}"
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, [email], fail_silently=False)

def verify_email(request):
    """Handle the email verification process"""
    if request.method == "POST":
        email = request.POST.get('email')
        code = request.POST.get('code')

        # Check if the email exists
        try:
            user = User.objects.get(email=email)
            verification = EmailVerification.objects.get(user=user)

            # Check if the code is correct
            if verification.verification_code == code:
                verification.is_verified = True
                verification.save()
                messages.success(request, "Your email has been verified successfully!")
                return redirect('login')  # Redirect to login after successful verification.
            else:
                messages.error(request, "Invalid verification code. Please try again.")
                return redirect('verify_email')  # Redirect back to verification page

        except User.DoesNotExist:
            messages.error(request, "No user found with that email address.")
            return redirect('verify_email')

    return render(request, 'verify_email.html')

def login(request):
    """Handle user login"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_verified:
                auth_login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Please verify your email before logging in.')
                return redirect('verify_email', user_id=user.id)
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

# Testing views
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
    """Handle user logout"""
    auth_logout(request)
    return redirect('index')  # Redirect to homepage after logout

def dashboard(request):
    return HttpResponse("Welcome to your Dashboard!")

def forgot_password(request):
    return HttpResponse("Don't worry we will help you retrieve your password.")
