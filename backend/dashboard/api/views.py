from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from employees.models import EmployeeProfile
from dashboard.services.Empdashboard_service import EmployeeDashboardService
from dashboard.api.serializers import EmployeeDashboardSerializer, HRDashboardSerializer
from employees.decorators import is_admin, is_hr
from dashboard.services.HRDashboard_service import HRDashboardService 

class EmployeeDashboardAPIView(APIView):

    permission_classes = [IsAuthenticated]

    serializer_class = EmployeeDashboardSerializer

    def get(self, request):

        if request.user.is_authenticated:

            profile = EmployeeProfile.objects.select_related(
                "employee"
            ).filter(user=request.user).first()

        else:

            employee_id = request.GET.get("employee_id")

            if not employee_id:

                return Response(
                    {
                        "error": "employee_id is required for anonymous testing"
                    },
                    status=400
                )

            profile = EmployeeProfile.objects.select_related(
                "employee"
            ).filter(employee_id=employee_id).first()


        if not profile:
            return Response(
                {"error": "Employee profile not found"},
                status=404
            )

        emp = profile.employee

        year = request.GET.get("year")
        month = request.GET.get("month")
        day = request.GET.get("day")

        year = int(year) if year else None
        month = int(month) if month else None

        attendance_data = EmployeeDashboardService.get_attendance_data( emp, year, month, day, )
        

        leave_data = EmployeeDashboardService.get_leave_data( emp, year, month, day, )
        

        payroll_data = EmployeeDashboardService.get_payroll_data( emp, year, month, )
        

        latest_salary = payroll_data.get("latest_salary")

        latest_salary_data = None

        if latest_salary:

            latest_salary_data = {
                "id": latest_salary.id,
                "net_pay": float(latest_salary.stored_net_pay),
                "pay_month": latest_salary.pay_month.strftime("%B %Y"),
            }

        response_data = {

            **attendance_data,

            **leave_data,

            **payroll_data,

            "latest_salary": latest_salary_data,
        }

        serializer = EmployeeDashboardSerializer(response_data)

        return Response(serializer.data)
    

class HRDashboardAPIView(APIView):

    permission_classes = [IsAuthenticated]

    serializer_class = HRDashboardSerializer

    def get(self, request):

        if not (is_admin(request.user) or is_hr(request.user)):

            return Response(
                {"error": "Permission denied"},
                status=403
            )

        year = request.GET.get("year")
        month = request.GET.get("month")
        day = request.GET.get("day")

        leave_stats = HRDashboardService.get_leave_statistics( year, month, day, )
        

        employee_stats = HRDashboardService.get_employee_statistics( year, month, day, )
        

        attendance_stats = HRDashboardService.get_attendance_statistics( year, month, day, )
        

        payroll_stats = HRDashboardService.get_payroll_statistics( year, month, )
        

        response_data = {

            **leave_stats,

            **employee_stats,

            **attendance_stats,

            **payroll_stats,
        }

        serializer = HRDashboardSerializer(response_data)

        return Response(serializer.data)