from employees.models import Employee

class EmployeeSelector:

    @staticmethod
    def all_employees():

        return Employee.objects.all()
