from employees.decorators import is_admin, is_hr

class EmployeePermission:

    @staticmethod
    def can_manage_employee(user):
        return is_admin(user) or is_hr(user)
    
    @staticmethod
    def can_view_employee(user):
        return is_admin(user) or is_hr(user)

    @staticmethod
    def can_edit_employee(user):
        return is_admin(user) or is_hr(user)

    @staticmethod
    def can_view_reports(user):
        return is_admin(user) or is_hr(user)

    @staticmethod
    def can_export_reports(user):
        return is_admin(user) or is_hr(user)

    @staticmethod
    def can_delete_employee(user):
        return is_admin(user) or is_hr(user)