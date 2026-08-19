from employees.decorators import is_admin, is_hr

class PermissionService:

    @staticmethod
    def is_hr_or_admin(user):
        return ( is_admin(user) or is_hr(user))