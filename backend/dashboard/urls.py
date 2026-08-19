from django.urls import path
from . import views

urlpatterns = [
    
    path('me/dashboard/', views.employee_dashboard, name='employee_dashboard'),

    path('hr/dashboard/', views.hr_dashboard, name='hr_dashboard'),
 ]