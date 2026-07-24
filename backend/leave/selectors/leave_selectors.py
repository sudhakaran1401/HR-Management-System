from leave.models import LeaveRequest

class LeaveSelector:

    @staticmethod
    def filtered_leave_queryset( month=None, year=None, employee=None, employee_id=None, ):

        queryset = LeaveRequest.objects.select_related("employee").all() 

        if year:
            queryset = queryset.filter( applied_at__year=int(year) )

        if month:
            queryset = queryset.filter( applied_at__icontains=f"-{int(month):02d}-" )

        if employee:
            queryset = queryset.filter(employee=employee)

        if employee_id:
            queryset = queryset.filter( employee_id=employee_id )

        return queryset.order_by("-applied_at")

    @staticmethod
    def leave_requests( employee=None, employee_id=None, status=None, ):

        queryset = LeaveRequest.objects.select_related("employee").all() 

        if employee:
            queryset = queryset.filter(employee=employee)

        if employee_id:
            queryset = queryset.filter( employee_id=employee_id )

        if status:
            queryset = queryset.filter(status=status)

        return queryset.order_by("-applied_at")
    
    @staticmethod
    def leave_list_query(employee):

        return (
            LeaveRequest.objects
        .select_related("employee")
        .filter(employee=employee)
        .order_by("-applied_at")
        )