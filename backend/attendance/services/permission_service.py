class AttendancePermissionService:

    @staticmethod
    def is_hr_or_admin(user):
        return (user.is_superuser or user.groups.filter(name__in=["HR", "ADMIN"]).exists())

    @staticmethod
    def is_employee(user):
        return user.groups.filter(name="EMPLOYEE").exists()
