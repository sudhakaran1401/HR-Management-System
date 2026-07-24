from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.services.auth_service import AuthService
from employees.decorators import is_admin, is_employee, is_hr


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = AuthService.authenticate_user(
            request,
            username,
            password
        )

        if user:
            login(request, user)

            redirect_url = AuthService.get_dashboard_redirect(user)

            return redirect(redirect_url)

        messages.error(request, "Invalid username or password")

    return render(request, "registration/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def home(request):
    return render(request, "home.html")


@login_required
def post_login_redirect(request):

    user = request.user

    if is_admin(user) or is_hr(user):
        return redirect("hr_dashboard")

    if is_employee(user):
        return redirect("employee_dashboard")

    return redirect("home")