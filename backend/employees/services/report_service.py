from employees.models import Employee

class EmployeeReportService:

    @staticmethod
    def filter_by_joining(month=None, year=None):

        qs = Employee.objects.all()

        if year:
            qs = qs.filter(joining_date__year=int(year))

        if month:
            qs = qs.filter(joining_date__month=int(month))

        return qs

    
