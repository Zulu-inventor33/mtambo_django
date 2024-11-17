# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('developer_dashboard/', views.developer_dashboard, name='developer_dashboard'),
    path('maintenance_dashboard/', views.maintenance_dashboard, name='maintenance_dashboard'),
    path('technician_dashboard/', views.technician_dashboard, name='technician_dashboard'),
    path('elevators/', views.elevators, name='elevators'),
    path('generators/', views.generators, name='generators'),
    path('hvac/', views.hvac, name='hvac'),
    path('contact/', views.contact, name='contact'),
    path('logout/', views.logout, name='logout'),
    path('about/', views.about, name='about'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
]
