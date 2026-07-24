from leave.models import LeaveRequest


class LeaveSelector:
    @staticmethod
    def approved_employee_leaves(employee):

        return LeaveRequest.objects.filter(employee=employee, status="APPROVED")

    @staticmethod
    def all_leaves():

        return LeaveRequest.objects.all()

    @staticmethod
    def approved_leaves():

        return LeaveRequest.objects.filter(status="APPROVED")
