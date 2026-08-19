from django.contrib.auth import authenticate

class AuthService:

    @staticmethod
    def authenticate_user(request, username, password):
        return authenticate(
            request,
            username=username,
            password=password
        )

    @staticmethod
    def get_dashboard_redirect(user):

        if user.groups.filter(name="HR").exists():
            return "hr_dashboard"

        return "employee_dashboard"